---
hidden: false
noIndex: false
description: Rank the users, budgets, and models of an AI Workspace by spend, drill into one user's models, and export the user and model rankings as a CSV file.
---

# Track AI workspace spend

The **Spend** page of an AI Workspace ranks the users, budgets, and models of the workspace by what they cost over a time range. It also exports the user and model rankings as a CSV file. Spend is the token cost the gateway records for each call. For how the gateway computes it, see [Where cost comes from](../observe/monitor-your-llm-proxy.md#where-cost-comes-from).

The page counts the LLM traffic that runs through the workspace. For charts of the same traffic over time, open the workspace dashboard. See [Monitor your AI workspaces](../observe/monitor-your-ai-workspaces.md).

## Open the Spend page

To open the **Spend** page of a workspace, complete the following steps:

1. From the Gamma console sidebar, open **Agent Management**.
2. Under **Secure**, open **AI Workspaces**.
3. Select the workspace.
4. Under **Observability**, click **Spend**.

    <!-- TODO: Screenshot of the Spend page of a workspace with traffic: the Spend, Tokens, Requests, and Users figures, the Users table, and the Budgets table -->

The page opens on the last 30 days. Change the range with the time range control in the page header, and every spend, token, and request figure follows it.

## What the figures cover

Note the following points before you read the page:

* The figures count only traffic on APIs you can view.
* The **Users** table lists the current users of the workspace, and the **Budgets** table counts them. A user whose access was revoked drops out of both tables, but their spend in the time range still counts in the **Spend** figure. The tables can therefore add up to less than that figure.
* A user who spent nothing is listed at zero. Each user is listed by display name, or by an ID when the name can't be read.
* The **Budgets** table groups each user's spend under the budget they're on now. Moving a user to another budget moves their spend for the whole time range with them.
* The page reads up to 10,000 users. When a workspace has more, an alert above the **Users** table says so. The **Users** figure, the **Users** table, the budget totals, and the export then cover the users that were read.
* When the analytics engine doesn't answer, the page shows a dash in place of each figure it couldn't read, or a message in place of the **Models** table.

To see how much of their own budget each user has used, open the **Users** page of the workspace. See [Read the Users list](assign-users-to-an-ai-workspace.md#read-the-users-list).

## Drill into one user

To see what each model cost one user, complete the following steps:

1. In the **Users** table, click the user's name.

    A panel opens beside the page. It sets the user's spend, tokens, and requests against the workspace totals, and shows what each model cost them.

2. Optional: To manage the user's access, click **Open Users page**.

Closing the panel keeps the user selected, so a later export still carries their models. To clear the selection, click **Clear selection of**, followed by the user's name, under the **Users** heading.

## Export spend as a CSV file

To export the spend of a workspace, complete the following steps:

1. Set the time range the export covers.
2. Optional: To add one user's models to the file, select the user in the **Users** table.
3. Click **Export CSV**.

The file is named `ai-workspace-<workspace ID>-spend-<start date>_<end date>.csv`, with each date written as `YYYY-MM-DD` in UTC. It holds the following tables, one after the other, each with the columns `Name`, `Requests`, `Tokens`, and `Spend (USD)` and each ranked by spend:

* `Users`: every user the page read, not only the users on screen.
* `Models`: every model in the **Models** table.
* `Models for` followed by the user's name: the models of the selected user, when one is selected.

The **Budgets** table isn't part of the file. Note the following points before you process it:

* Spend is written in dollars with six decimal places.
* A figure the analytics engine didn't return for a model is written as `0`, where the page shows a dash. When the **Models** table couldn't be read at all, the `Models` table of the file has no rows.
* A name that starts with `=`, `+`, `-`, `@`, a tab, or a carriage return is written with a leading `'`, so a spreadsheet reads it as text.
* When the workspace has more users than the page reads, the file opens with the line `Partial export: this workspace holds more members than one read covers.`

**Export CSV** is unavailable while the workspace has no users, and while the spend of its users can't be read. When the analytics engine stops answering between opening the page and clicking the button, the export fails, and the page gives the reason under **Could not export**.

## Open the workspace dashboard

To read the same traffic as charts, click **Open in dashboard** in the page header. The AI Workspace Overview dashboard opens in a new tab, filtered to the workspace and set to the time range the **Spend** page shows. See [Monitor your AI workspaces](../observe/monitor-your-ai-workspaces.md).

## Verification

To verify the **Spend** page is working as expected, follow these steps:

1. Call the workspace entrypoint with a user's API key. See [Assign users to an AI workspace](assign-users-to-an-ai-workspace.md).
2. Open the **Spend** page of the workspace.
3. Confirm the **Requests** figure and the user's row in the **Users** table count the call.
4. Click **Export CSV**, and confirm the `Users` table of the file carries the user's row.

    <!-- TODO: Screenshot of the Spend page after a call, with the user's row in the Users table showing the request -->
