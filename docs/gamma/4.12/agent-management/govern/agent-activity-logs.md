---
hidden: true
noIndex: true
description: Read the record of one request an agent handled, with the calls it made through the AI Gateway and every decision a rule, a Guardian, or a person took on it. Learn where the record lives and what it carries.
---

# Audit agent activity logs

Every request an agent handles through the AI Gateway leaves a record: the call that reached the agent, the model and tool calls the agent made to answer it, and each decision a rule, a Guardian Agent, or a person took along the way. The agent's **Activity** page lists those records under **Requests**, and each one opens into a panel that names the identifiers, the decisions, and the gateway records behind it.

The record is assembled from what the gateway reported, not declared by anyone. The calls come from the gateway's request metrics, and the decisions from the decision stream that the authorization, human approval, and AI Guardian policies write to. Nothing here is edited after the fact.

## Open the Requests list

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Operations** section of the agent's sidebar, click **Activity**.
5. Scroll to **Requests**.

The list needs an A2A Proxy that fronts the agent. Without one it reads **This agent has no gateway proxy yet. Deploy an A2A proxy to see Activity here.** An agent with a proxy but no traffic in the time range reads **This agent has no activity yet.**

The list follows the time range picker at the top of the page and shows the 25 most recent requests, grouped by UTC day with times in UTC.

<!-- TODO: Screenshot of the Requests list of an agent with one row expanded to its steps, and the technical details panel open beside it -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-activity-record.png" alt=""><figcaption><p>A request in the Requests list, expanded, with its technical details panel</p></figcaption></figure>

## How a record is assembled

A record joins two kinds of gateway records:

* **The calls**. The inbound call the A2A Proxy received for the agent, and the model calls and tool calls the agent's gateway application made through the LLM and MCP Proxies. Calls that carry the same conversation ID are grouped into one request. A call with no conversation ID stands as a request of its own.
* **The decisions**. Every decision written to the decision stream for those calls, joined by request ID: the authorization policy's, a human's through the HITL inbox, and an AI Guardian's. A human decision that was asked for and then taken appears once, with the outcome of the decision and the reason it was asked for.

An authorization permit that carries no reason is treated as routine. It isn't listed among the decisions, and it doesn't count as someone stepping in.

## Read the outcome

Each row opens with an outcome badge. The outcome is derived from the decisions the request carries, in this order:

<table>
    <thead>
        <tr>
            <th width="220">Outcome</th>
            <th>When the record reads it</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Waiting for sign-off</strong></td>
            <td>A human decision was asked for and nobody has taken it yet. The row offers <strong>Review sign-off</strong>, which opens the held call in the HITL inbox.</td>
        </tr>
        <tr>
            <td><strong>Stopped</strong></td>
            <td>A decision denied the call, or the gateway enforced a denial.</td>
        </tr>
        <tr>
            <td><strong>Done with changes</strong></td>
            <td>A person approved a held call, or a Guardian rewrote what was screened.</td>
        </tr>
        <tr>
            <td><strong>Done</strong></td>
            <td>Everything was permitted and nobody stepped in.</td>
        </tr>
    </tbody>
</table>

The **Outcome** filter also lists **Handed to a person**, **Nobody decided**, and **Didn't finish**. The feed derives none of them in this build, so those filters match no row.

The **Asked by** field and filter read **Not recorded** for every request in this build. The **Stepped in** filter narrows the list to requests where **A rule**, **A Guardian**, or **A person** decided something, and the **Show routine requests** switch, on by default, controls whether requests that finished with nobody stepping in are listed at all.

## Read a record

Expand a row to read the request as a sequence of steps, each with its UTC time:

* What the agent received or served, as **The agent received a request** or **The agent served its card**.
* Each call the agent made, as **The agent called** followed by the model or the tool.
* Each decision, as **Rule**, **Guardian**, or **Person** followed by what it did: **proposed**, **held**, **recommended**, **approved**, **declined**, **modified**, **called**, or **error**, and the decider when the decision names one. The reason follows in quotes when the decision recorded one.

**View technical details** opens the record's panel. Its title is the outcome and its subtitle names what the agent called. The panel has four sections:

<table>
    <thead>
        <tr>
            <th width="220">Section</th>
            <th>What it carries</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Request</strong></td>
            <td><strong>Asked by</strong>, <strong>Outcome</strong>, the <strong>Conversation ID</strong> when the calls carried one, and the <strong>Request ID</strong> of the first call, each identifier with a copy control.</td>
        </tr>
        <tr>
            <td><strong>Decisions</strong></td>
            <td>One card per decision, shown only when the request carries a decision that isn't routine. The card is badged <strong>Policy</strong>, <strong>Guardian</strong>, or <strong>Sign-off</strong>, and carries the decision's outcome, <code>ALLOW</code>, <code>DENY</code>, <code>TRANSFORM</code>, <code>INDETERMINATE</code>, or <code>PENDING</code>, its UTC time, the decider, and the reason in quotes. A human decision carries an <strong>Open decision record</strong> link, which opens the held call in the HITL inbox while it's pending and in the decision history once it's taken.</td>
        </tr>
        <tr>
            <td><strong>Correlated tool call</strong></td>
            <td>The last tool call of the request, when there is one: the <strong>Tool</strong>, the <strong>Resource</strong> it addressed, and the <strong>Request</strong> ID of the call.</td>
        </tr>
        <tr>
            <td><strong>Trace</strong></td>
            <td>One line per call, with the count of gateway records the request left, calls and decisions together. Each line carries the UTC time, an <strong>A2A</strong>, <strong>LLM</strong>, or <strong>MCP</strong> badge, the call's label, and its HTTP status, then the <strong>Tool</strong>, <strong>Provider</strong>, or <strong>Resource</strong> the call named and its <strong>Request</strong> ID.</td>
        </tr>
    </tbody>
</table>

The call labels are what the gateway recorded: **Inbound:** followed by the path, **LLM call:** followed by the model, and **MCP tool:** followed by the tool. A call the gateway couldn't name reads **Inbound request**, **LLM call**, or **MCP tool call**.

**View in Logs** at the bottom of the panel opens the Logs page on a window that starts two minutes before the request and ends two minutes after its last call, with the agent's application and proxies already selected.

## What the record doesn't carry

* **Cost**. The record on this page carries no price. What the request cost is read on the agent's **Cost** page and on the **Agent — Overview** dashboard.
* **Older requests**. The list shows the 25 most recent requests of the time range. Narrow the range to reach earlier ones.

## Next steps

* [Require human approval for MCP tool calls](require-human-approval-for-mcp-tool-calls.md). Take the decision a request is waiting for, and read the decision history.
* [Guard agent actions with Guardian Agents](guard-agent-actions-with-guardian-agents.md). Add the Guardian whose verdicts appear here.
* [Read what an agent cost](../cost-and-value/read-what-an-agent-cost.md). Price the requests this page lists.
