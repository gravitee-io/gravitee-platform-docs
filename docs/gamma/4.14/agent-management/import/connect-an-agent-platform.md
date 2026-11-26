---
hidden: false
noIndex: false
description: Connect a cloud provider to Agent Discovery and sync its agents into the Catalog. Follow the steps to add a source, run a sync, and read its sync activity.
---

# Connect a cloud provider

Agent Discovery connects a cloud provider as a source, and syncs the agents it hosts into the Catalog. A sync discovers the agents in the project, and then imports all of them into the Catalog. Each source holds one connection, and you can connect the same provider more than once.

Agent Discovery appears in the **Connect** group of the Agent Management sidebar when the `agent-discovery` feature is switched on. It lists three providers: **Azure AI Foundry**, **Gemini Enterprise Agent Platform**, and **Amazon Bedrock AgentCore**. A provider is offered only when its plugin is deployed and licensed. When none is, the wizard reads **No cloud providers available** and asks you to have your administrator add one.

## Add a source

1. In the Gamma console, open **Agent Management**.
2. In the **Connect** group of the sidebar, select **Agent Discovery**.
3. Click **Add source**. The button appears only when you can create sources.
4. In the **Overview** step, select the provider, and enter a **Display name**. The name is required and must be unique in the environment.
5. Click **Next**.
6. In the **Authentication** step, fill in the connection fields. The fields depend on the provider.
7. Click **Test connection**. When the provider answers, a **Connection successful** alert shows how long the call took.
8. Click **Next**.
9. In the **Settings** step, choose the **Sync schedule**: **Manual**, **Daily**, or **Weekly**. For **Weekly**, choose the **Day of the week**.
10. Click **Next**.
11. In the **Review** step, check the **Display name**, the **Provider**, the connection details, the **Connection test**, and the **Schedule**.
12. Optional: Clear **Run first sync after creation**. It's selected by default, and it appears when you can sync.
13. Click **Create source**.

A **Manual** source imports agents only when you trigger a sync. A **Daily** source runs once a day, and a **Weekly** source runs once a week on the day you choose. The server picks the time of day. All agents in the configured region or project are included.

A source with a name that's already taken is refused with **A source with this name already exists in this environment.**

## Read a source

The **Agent Discovery** page lists the sources of the environment with their **Name**, **Status**, **Last updated**, **Agents**, **Source type**, and **Updates**. **View agents** opens the Agents page. Click a source's name to open it.

A source page opens on four tabs: **Overview**, **Authentication**, **Settings**, and **Sync activity**. The **Overview** tab shows the following details:

<table>
    <thead>
        <tr>
            <th width="220">Detail</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Name</strong></td>
            <td>The display name of the source.</td>
        </tr>
        <tr>
            <td><strong>Source type</strong></td>
            <td>The provider.</td>
        </tr>
        <tr>
            <td><strong>Imported agents</strong></td>
            <td>The number of agents the source brought in, as a link to them.</td>
        </tr>
        <tr>
            <td><strong>Updates</strong></td>
            <td>The sync schedule: <strong>Manual</strong>, <strong>Daily</strong>, or <strong>Weekly on</strong> a day.</td>
        </tr>
        <tr>
            <td><strong>Next scheduled sync</strong></td>
            <td>When the next sync runs. A <strong>Manual</strong> source has no next sync, so the row is omitted.</td>
        </tr>
        <tr>
            <td><strong>Updated</strong></td>
            <td>When the source was last changed.</td>
        </tr>
    </tbody>
</table>

The **Agents from this source** panel lists the agents the source imported. Before the first sync, it reads **No agents imported yet.**

## Sync the agents

1. In the **Connect** group of the sidebar, select **Agent Discovery**.
2. Click the source's name.
3. Click **Sync now**. The button appears only when you can sync agents.

While the sync runs, the button reads **Sync running…**, and the **Sync activity** panel reads **Syncing agents…**. When the run ends, the panel reads **Sync complete**, **Sync finished with failures**, **Sync failed**, or **Sync canceled**. It also shows the counts of the run: **imported**, **updated**, **unchanged**, **skipped**, and **failed**.

A sync that can't start reads **Could not start the sync** with the reason, for example that the provider's plugin isn't installed. When the page can't follow a sync, it reads **Could not follow the sync**. The sync goes on on the server, so reload the page later to see its agents.

### Read the sync activity

The **Sync activity** tab lists the runs of the source. Search them with **Search sync activity…**. The list has the following columns:

<table>
    <thead>
        <tr>
            <th width="220">Column</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Started</strong></td>
            <td>When the run started.</td>
        </tr>
        <tr>
            <td><strong>Outcome</strong></td>
            <td><strong>In progress</strong>, <strong>Success</strong>, <strong>Partial</strong>, <strong>Failed</strong>, or <strong>Canceled</strong>.</td>
        </tr>
        <tr>
            <td><strong>Trigger</strong></td>
            <td><strong>Manual</strong> for a run you started, or <strong>Scheduled</strong> for a run the schedule started.</td>
        </tr>
        <tr>
            <td><strong>Duration</strong></td>
            <td>How long the run took.</td>
        </tr>
        <tr>
            <td><strong>Changes</strong></td>
            <td>The count of agents <strong>added</strong>, <strong>updated</strong>, <strong>unchanged</strong>, <strong>rejected</strong>, and <strong>failed</strong>.</td>
        </tr>
    </tbody>
</table>

A source with no run reads **This source has no sync run yet.**

## Change a source

* To change the connection, open the **Authentication** tab. It holds the connection fields of the wizard. Change them, click **Test connection** to check the change, and then save.
* To rename the source or change its schedule, open the **Settings** tab, change the **Display name** or the sync schedule, and then save.

## Delete a source

1. In the **Connect** group of the sidebar, select **Agent Discovery**.
2. Click the source's name.
3. In the **Delete source** card, click **Delete**.
4. In the **Delete \<name>?** dialog, read the warning, and then click **Delete source**.

When you delete a source, its imported agents, its discovered agents, and its sync history are deleted too. You can't undo it.

## Next steps

* [Manage a registered agent](manage-a-registered-agent.md). Open an imported agent's page.
* [Agent kill switch](../build/agent-killswitch.md). Stop an agent imported from Azure AI Foundry on the platform itself.
* [Connect integrations](connect-integrations.md). Connect a model provider or Azure AI Foundry for its models.
