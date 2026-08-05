"""
Support Ticket App – Flask server with Lakebase backend.

Endpoints:
- GET /                     – list all tickets + form to create a new ticket
- GET /tickets/<ticket_id>  – view a single ticket with its messages
- POST /tickets             – create a new ticket
- POST /tickets/<ticket_id>/messages – add a message to a ticket
- POST /tickets/<ticket_id>/status   – update ticket status
"""

import logging
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request, redirect, url_for
from databricks.sdk import WorkspaceClient

import lakebase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("support-app")

app = Flask(__name__)
_w = WorkspaceClient()


def _current_user_email() -> str:
    """Get the current authenticated user's email (from header or SDK)."""
    header_email = request.headers.get("X-Forwarded-Email")
    if header_email:
        return header_email
    return _w.current_user.me().user_name


@app.errorhandler(Exception)
def handle_exception(err):
    """Return JSON for any unhandled error."""
    logger.exception("Unhandled exception")
    return jsonify({"error": str(err)}), 500


@app.route("/")
def index():
    """Show all tickets and a form to create a new one."""
    tickets = lakebase.run_query(
        "SELECT ticket_id, title, status, created_by, created_at, updated_at, priority "
        "FROM tickets ORDER BY created_at DESC"
    )
    return render_template("index.html", tickets=tickets)


@app.route("/tickets/<int:ticket_id>")
def ticket_detail(ticket_id):
    """Show a single ticket with all its messages."""
    # Fetch ticket
    ticket_rows = lakebase.run_query(
        "SELECT ticket_id, title, status, created_by, created_at, updated_at, priority "
        "FROM tickets WHERE ticket_id = %s",
        (ticket_id,)
    )
    if not ticket_rows:
        return jsonify({"error": "Ticket not found"}), 404
    ticket = ticket_rows[0]

    # Fetch messages
    messages = lakebase.run_query(
        "SELECT message_id, message_text, author, created_at "
        "FROM ticket_messages WHERE ticket_id = %s ORDER BY created_at ASC",
        (ticket_id,)
    )

    return render_template("ticket_detail.html", ticket=ticket, messages=messages)


@app.route("/tickets", methods=["POST"])
def create_ticket():
    """Create a new ticket."""
    title = request.form.get("title", "").strip()
    status = request.form.get("status", "open")
    priority = request.form.get("priority", "medium")
    created_by = _current_user_email()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Insert ticket (created_at/updated_at default to now())
    lakebase.run_write(
        """
        INSERT INTO tickets (title, status, created_by, priority)
        VALUES (%s, %s, %s, %s)
        """,
        (title, status, created_by, priority)
    )

    # Redirect back to index (or show success)
    return redirect(url_for("index"))


@app.route("/tickets/<int:ticket_id>/messages", methods=["POST"])
def add_message(ticket_id):
    """Add a message to an existing ticket."""
    message_text = request.form.get("message_text", "").strip()
    author = request.form.get("author") or _current_user_email()

    if not message_text:
        return jsonify({"error": "Message text is required"}), 400

    # Check that the ticket exists
    ticket = lakebase.run_query(
        "SELECT ticket_id FROM tickets WHERE ticket_id = %s",
        (ticket_id,)
    )
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    lakebase.run_write(
        """
        INSERT INTO ticket_messages (ticket_id, message_text, author)
        VALUES (%s, %s, %s)
        """,
        (ticket_id, message_text, author)
    )

    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
def update_status(ticket_id):
    """Update the status of a ticket."""
    new_status = request.form.get("status", "").strip()
    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    # Optionally validate against allowed values
    allowed = {"open", "in_progress", "resolved", "closed"}
    if new_status not in allowed:
        return jsonify({"error": f"Invalid status. Allowed: {', '.join(allowed)}"}), 400

    rows_updated = lakebase.run_write(
        """
        UPDATE tickets
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE ticket_id = %s
        """,
        (new_status, ticket_id)
    )
    if rows_updated == 0:
        return jsonify({"error": "Ticket not found"}), 404

    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 8000))
    app.run(debug=True, host=host, port=port)