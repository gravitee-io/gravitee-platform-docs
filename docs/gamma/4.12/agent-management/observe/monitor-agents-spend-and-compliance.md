---
description: The Overview page is the Agent Management landing page. Read what its Agents, Spend through the gateway, and Compliance sections report across the environment.
---

# Monitor agents, spend, and compliance on the Overview page

**Overview** is the page Agent Management opens on. It reports across every agent and proxy in the environment, so what the environment costs and where it's failing are visible without opening anything.

This is a different surface from the **Overview** page of a single proxy, which reports on that one proxy over a fixed 24 hours. See [Monitor proxy and agent activity](monitor-proxy-activity.md) for that page.

## Open the Overview page

1. From the Gamma console sidebar, select **Agent Management**. The module opens on **Overview**.
2. To return to it from anywhere in the module, find the **General** group in the sidebar and select **Overview**.

<!-- TODO: Screenshot of the Agent Management Overview page showing the Agents, Spend through the gateway, and Compliance sections -->
<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-overview-page.png" alt=""><figcaption><p>The <strong>Overview</strong> page, with the <strong>Agents</strong>, <strong>Spend through the gateway</strong>, and <strong>Compliance</strong> sections.</p></figcaption></figure>

The line beside the page title reports when the figures were last updated. Select **Refresh** to read them again.

## What the page reports

The page carries three sections, each covering the whole environment and each linking out to the pages behind it.

### Agents

**Agents** counts the agents in the catalog, as of now.

When every agent is fronted by a proxy that's deployed and started, the section reads that they all run through the gateway. Otherwise it breaks out what's wrong:

* Agents that no proxy fronts are reported as bypassing the gateway, with the note that Gravitee can't rate-limit, hold, or stop their calls. **See the agents** opens the catalog filtered to them.
* Agents that missed a performance target are listed with a link to those agents. See [Performance targets](performance-targets.md).
* Agents stopped in Gravitee are listed with a link to them.

**Explore all agents** opens the full catalog.

### Spend through the gateway

**Spend through the gateway** reports cost in USD over a window you choose. Select **7 d**, **30 d**, or **90 d**. The default is **30 d**.

Switching the window keeps the figures already on screen while the new ones load, so the section doesn't fall back to a placeholder.

**Explore in Observability** opens the dashboards over the same time range.

### Compliance

**Compliance** reports how many agents fail at least one framework, as of now. When nothing has been assessed yet, the section says so instead of reporting a count.

Below the count, each active framework and ruleset carries its own verdict, one of **Pass**, **Fail**, or **Not assessed**.

**Open Compliance** opens the Compliance page. See [Score agent compliance with the EU AI Act framework](../govern/score-agent-compliance-with-the-eu-ai-act.md).

## Quick links

Below the three sections, the page offers shortcuts to the actions an operator reaches for most:

* **Add an agent**
* **Connect an integration**
* **Set up an LLM proxy**
* **Switch on a compliance framework**
* **Open Observability dashboards**

## When the environment has no agents

With no agents in the catalog, the three sections are replaced by a **Set up this page** panel that walks through the steps that populate it.

**Spend through the gateway** still appears once the gateway has recorded spend, because an LLM Proxy produces cost data before any agent is registered.

## When a section can't load

A section that fails to load reports its own error and offers a retry, and the rest of the page keeps working.

When all three fail together, the page replaces them with a single message. It reads **The Overview couldn't be loaded** when the browser is online, and **You're offline** when it isn't. Select **Details** to see what each section reported, and **Try again** to retry all three. The line beside the page title then reports when the last attempt failed rather than when the figures were updated.
