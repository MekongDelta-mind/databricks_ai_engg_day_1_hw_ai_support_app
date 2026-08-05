- [x] Your Databricks App URL: https://databricks-day-1-hw-1-7474660520510840.aws.databricksapps.com

- [x] Your source code zipped up.

    Github repo link: 
    
    https://github.com/MekongDelta-mind/databricks_ai_engg_day_1_hw_ai_support_app

- [x] A screenshot of the deployed application

<img width="1915" height="1074" alt="image" src="https://github.com/user-attachments/assets/6d6299a0-83d0-4489-8d1e-5047ce1ddb60" />


- [x] A screenshot showing the Lakebase tables and sample records

<img width="1920" height="996" alt="image" src="https://github.com/user-attachments/assets/c2c6d38c-69dc-436b-a654-38c00a825771" />

<img width="1916" height="996" alt="image" src="https://github.com/user-attachments/assets/2979222b-e35c-4ac2-900c-45cacb25c84a" />


---

# Deploy and test the app

Deploy the app using Databricks Apps and confirm that:
---
- [x] Existing tickets load from Lakebase
<img width="1920" height="957" alt="image" src="https://github.com/user-attachments/assets/97f81c3c-4068-46e7-9372-6268cb095535" />

---
- [x] A new ticket can be created
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4a9ea403-5b73-41bd-b37c-59fcce365d29" />

---
- [x] A message can be added
<img width="1920" height="1078" alt="image" src="https://github.com/user-attachments/assets/ae2746c4-3a91-47a3-b933-10cb2bbf285b" />

---

- [x]A ticket’s status can be updated

Before
<img width="1920" height="953" alt="image" src="https://github.com/user-attachments/assets/50c8f2d6-fbd1-4c46-b76c-5d3c665c8dce" />

After
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7c932867-65b2-48a2-8fd5-7fd8076471ec" />

---
- [x] Changes remain after refreshing the app
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/48d82d64-374a-413e-8542-466ce7d0fc0d" />




---

A short reflection of 3–5 sentences answering:

What was the most difficult part?
- As I’m used to building apps in local and then deploying them into the production, directly deploying into the productions was a bit overwhelming. It would be better if we could build the app locally and connect the production lakebase from the local itself. I don’t know if it can be done now or not. I’m very new to Databricks.
- The creating Databricks App workflow is bit confusing/buggy.
    - first we create a App using the Git
    - Then again once the app is ready to be deployed we again need to add the repo link by using the Deploy>> link a source >> use the From workspace tab and then select the project from the workspace.
    - the problem here is , if the app is configured to a particular github repo / workspace while creating the app, then when we want to deploy the app, the system automatically should fetch the whole folder from the respective link.
    - NOTE: this happens only when we tend to create the app for the first time. from the subsequent iterations, the deploy takes the files from the respective repo/workspace.
- The logs are not shown properly when the app crashes. When an app crashes, the Logs in the Side bar doesn’t show the log properly. We have to click the link under here in the message `You can also click here to view the logs in a new tab.`  to show the logs in a different window to actutally see the logs
    <img width="1915" height="888" alt="image" src="https://github.com/user-attachments/assets/a7063d9c-74ba-4b12-bd6d-7c298bc0ad5b" />


How is Lakebase different from storing this data in a traditional analytics table?

I don't work with Lakebase or other traditional analytics table. So can't compare. The most interesting thing is the tables are added with a new row automatically which contains the table name of the foreign table both in the parent table and the child table. Like in the present example, the `tickets` table had a column named `ticket_messages` with values as "ticket_messages" and vice versa. This is a very useful feature when there are numerous tables and checking each table and ER relationship makes it a tiresome activity.

What feature would you add next?
I think the features are already good enough. Although I would like to refine the existing feature a bit more such as below. 
- Like while editing the Python/ipynb file in the Workspace, i think it sometimes activates the SQL Editor in the side panel and sometimes it shows the Workspace tab in the side panel.
- To push my changes to github i need to open the github folder in Git Editor using `Open in Git Folder Editor`, then click on the button showing the branch on the git and only then a windows pops up with the changed files along with commit messages. There should be a button at the github folder level to push the changes.


