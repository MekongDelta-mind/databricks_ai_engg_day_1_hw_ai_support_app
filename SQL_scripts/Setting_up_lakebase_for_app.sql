-- -------------------------------
-- 1. Create the schema if needed
-- -------------------------------
--CREATE SCHEMA IF NOT EXISTS ai_ticket_support_sys_schema;
-- here the Schema concept is not there. This is inside the Lakebase. 

-- -------------------------------
-- 2. Create tables
-- -------------------------------

-- Tickets table
CREATE TABLE tickets (
    ticket_id BIGSERIAL PRIMARY KEY,              -- auto-incrementing bigint
    title TEXT NOT NULL,                          -- TEXT = unlimited, or use VARCHAR(255)
    status TEXT DEFAULT 'open',
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    priority TEXT DEFAULT 'medium',
    -- PostgreSQL supports CHECK constraints
    CONSTRAINT status_chk CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    CONSTRAINT priority_chk CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);

-- Ticket messages table
CREATE TABLE ticket_messages (
    message_id BIGSERIAL PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    message_text TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Foreign key with optional ON DELETE CASCADE (now supported in PG)
    CONSTRAINT fk_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
);



-- -------------------------------
-- 3. Insert sample data
-- -------------------------------

-- Insert tickets
INSERT INTO tickets (title, status, created_by, created_at, updated_at, priority) VALUES
    ('Unable to process return for defective item', 'open', 'john.doe@retail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'high'),
    ('POS system offline at store #42', 'in_progress', 'store.manager@retail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'critical'),
    ('Question about bulk discount policy', 'resolved', 'alice.smith@retail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'low');

-- Insert messages (referencing the ticket IDs from above)
INSERT INTO ticket_messages (ticket_id, message_text, author, created_at) VALUES
    (1, 'Customer returned a laptop with a cracked screen, but our system says the return window closed yesterday.', 'john.doe@retail.com', CURRENT_TIMESTAMP),
    (1, 'I checked the return policy – we can make a one‑time exception. Please offer store credit.', 'support.agent@retail.com', CURRENT_TIMESTAMP),
    (2, 'Store #42 POS terminals have been offline since 9 AM. No transactions can be processed.', 'store.manager@retail.com', CURRENT_TIMESTAMP),
    (2, 'We’ve contacted the network provider. A technician is on the way. ETA 2 hours.', 'it.support@retail.com', CURRENT_TIMESTAMP),
    (3, 'What is the discount for ordering 500+ units of the same SKU?', 'alice.smith@retail.com', CURRENT_TIMESTAMP),
    (3, 'Our bulk discount is 15% for orders over 500 units. I’ve attached the policy document.', 'support.agent@retail.com', CURRENT_TIMESTAMP),
    (3, 'Got it, thank you!', 'alice.smith@retail.com', CURRENT_TIMESTAMP);