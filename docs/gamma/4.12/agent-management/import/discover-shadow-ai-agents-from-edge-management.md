---
hidden: true
noIndex: true
description: Turn the AI provider domains the Edge Daemon detects into shadow AI agents in the Agent Management Catalog. Learn how the synchronization runs and what a shadow AI agent's page shows.
---

# Discover shadow AI agents from Edge Management

Edge Management's shadow AI detection reports every direct connection an employee device makes to a monitored AI provider domain, bypassing the AI Gateway. Agent Management turns those detections into Catalog entries, so unsanctioned AI usage sits in the same list as the agents you govern. Each entry is one intercepted domain, and its page shows which processes and devices reached it.

A shadow AI agent is a domain and nothing more. Nobody registered it, no platform describes it, it publishes no agent card, and no traffic reaches it through the gateway. The Catalog holds its address, the risk classification you give it, and the dates it was first and last seen, and reads the detected traffic live when you open its page.

## Before you start

* Configure shadow AI monitoring in Edge Management, and deploy the Edge Daemon on the devices to watch. The domains the daemon reports are the ones listed under **Monitored domains**. See [Configure Edge Management](../../edge-management/connect/configure-edge-management.md#configure-shadow-ai-monitoring).
* Turn on the synchronization in the Management API configuration, as described in the next section. Without it, detected domains never reach the Catalog.

## Turn on the synchronization

The synchronization runs inside the Management API on two schedules, and both are off until you set their delay. Set them in the `modules.aim.shadow-ai.sync` block of the Management API configuration:

```yaml
modules:
  aim:
    shadow-ai:
      sync:
        incremental:
          delay: 30
          unit: SECONDS
        full:
          delay: 60
          unit: MINUTES
```

<table>
    <thead>
        <tr>
            <th width="330">Property</th>
            <th>What it sets</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>modules.aim.shadow-ai.sync.incremental.delay</code></td>
            <td>How often the incremental pass runs. The incremental pass reads the detections that arrived since the previous run and creates an entry for each new domain. It never removes anything.</td>
        </tr>
        <tr>
            <td><code>modules.aim.shadow-ai.sync.incremental.unit</code></td>
            <td>The unit of the incremental delay. Defaults to <code>SECONDS</code>.</td>
        </tr>
        <tr>
            <td><code>modules.aim.shadow-ai.sync.full.delay</code></td>
            <td>How often the full pass runs. The full pass reads the last 30 days of detections, creates or updates an entry for each domain, and removes every entry whose domain had no detection in those 30 days. It removes nothing when the read returns no domain at all, so an unreachable telemetry store never empties the Catalog.</td>
        </tr>
        <tr>
            <td><code>modules.aim.shadow-ai.sync.full.unit</code></td>
            <td>The unit of the full delay. Defaults to <code>MINUTES</code>.</td>
        </tr>
    </tbody>
</table>

A delay that is absent, blank, not a number, zero, or negative turns that pass off. A unit that isn't recognized falls back to the default unit. When both passes are off, the Management API logs that the shadow AI synchronization is disabled and imports nothing.

Three more rules govern when a pass runs:

* One node runs the synchronization. In a cluster, that's the primary node.
* An environment is synchronized only after the Management API has served an Agent Management request for it since the node started.
* The first pass on a node is always a full pass, whichever schedule triggered it. A restart therefore applies the 30-day retention rule even when only the incremental schedule is on.

## What a synchronization writes

Each detected domain becomes one agent under a source named **Shadow AI**, which Gamma creates in the environment the first time it's needed. On the **Integrations** page, the source appears only under **All sources**, with **No read configured** in its **Imports** column and **Remove** as its only action, because it isn't an integration you connect. The agent is named after the domain. A run reads at most 500 domains, and treats what it read as the complete set, so an environment with more distinct domains than that has the rest left out and can lose entries on a full pass. A pass that finds the domain again leaves the entry untouched, so the classification you set, the owner you assign, and any other field you write survive every run. A full pass removes the entry once the domain has had no detection for 30 days, and removes the performance targets declared on it at the same time.

## Find shadow AI agents in the list

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.

In the **Agents** list, the **Source** column reads **Shadow AI** for a detected domain, in a highlighted badge, where an agent registered from the console reads **Manual** and an imported one reads its platform's name.

The actions menu at the end of the row still offers **Edit** and **Remove**. **Edit** is refused with a notification that Edge Management detected the agent and the next synchronization would write over an edit. **Remove** deletes the entry, and a later pass recreates it while the domain is still being detected.

<!-- TODO: Screenshot of the Agents list with a shadow AI agent row showing the Shadow AI source badge -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-agents-list-shadow-ai.png" alt=""><figcaption><p>A shadow AI agent in the Agents list</p></figcaption></figure>

## Read a shadow AI agent's page

Click the domain in the **Agents** list to open it. The page is built around having only an address, so it carries less than a registered agent's page:

* The header shows the domain as the title, a **Shadow AI** badge, and the **Owner** row.
* The sidebar holds **Overview** and nothing else. The bar of actions at the top of a registered agent's page isn't shown.
* The **About** section opens with a note that nobody registered the agent, that Edge Management detected the domain carrying agent traffic and re-checks it on every synchronization, and that the sections describing a declared agent aren't shown. Its card holds four rows: **Source**, which reads `edge.shadow-ai`, **Classification**, **Created**, and **Updated**.
* The **Detected traffic** section holds the traffic that produced the entry.

<!-- TODO: Screenshot of a shadow AI agent's page showing the About card and the Detected traffic section -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-shadow-agent-page.png" alt=""><figcaption><p>The page of a shadow AI agent</p></figcaption></figure>

### Rate the risk

**Classification** is the one field you write on a shadow AI agent, and the synchronization keeps it. To rate the domain, click the **Classification** badge, select **Negligible risk**, **Limited risk**, **Moderate risk**, or **High risk** in the **Classification** panel, and then click **Save**. A rating can be changed but not cleared.

### Read the detected traffic

The **Detected traffic** section reads the last 30 days of detections for the domain when the page opens, and it answers who inside the company is talking to the domain. The counts are the Edge Daemons' own tallies of connections, not the number of reports they sent.

<table>
    <thead>
        <tr>
            <th width="180">Table</th>
            <th>Columns</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Processes</strong></td>
            <td><strong>Process</strong>, the process as the daemon saw it, which on most systems is a path, and <strong>Detections</strong>.</td>
        </tr>
        <tr>
            <td><strong>Devices</strong></td>
            <td><strong>Device</strong>, the identifier the daemon authenticates with, <strong>OS</strong>, read from the device's own heartbeats, and <strong>Detections</strong>. A device that reached the domain but sent no heartbeat in the window keeps its row and shows a dash for the OS.</td>
        </tr>
    </tbody>
</table>

Each table lists up to 100 rows, heaviest first. When nothing reached the domain in the window, the tables read **No process reached this domain over the window.** and **No device reached this domain over the window.** When the telemetry can't be read, the section shows **Could not read what reached this domain** with the reason.

## Next steps

* [Monitor your shadow AI traffic](../../edge-management/observe/monitor-shadow-ai-traffic.md). Read the fleet-wide shadow AI view in Edge Management.
* [Configure Edge Management](../../edge-management/connect/configure-edge-management.md). Change the monitored domains and the report interval.
* [Register an agent](import-an-agent.md). Bring a sanctioned agent into the Catalog from the agent card it publishes.
