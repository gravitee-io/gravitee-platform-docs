---
hidden: true
noIndex: true
description: The Cost page of an agent adds up its model spend, tool spend, and human decisions over a period, and the Agent Overview dashboard charts them. Follow the steps to read both.
---

# Read what an agent cost

An agent's spend crosses the AI Gateway in three kinds of priced events: the model calls its LLM Proxies route, the tool calls its MCP Proxies serve, and the human decisions its held tool calls wait for. The agent's **Cost** page adds them up for a period, says what changed since the period before, and shows where the money went. The **Agent — Overview** dashboard charts the same figures over time.

Both read the traffic attributed to the agent's gateway application through the proxies that carry its calls, the same scope as the agent's **Activity** page. Model and tool calls are priced from the catalog. See [Agent FinOps](agent-finops.md) for where each price is set.

## Open the Cost page

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Operations** section of the agent's sidebar, click **Cost**.

The time range picker opens on the last 30 days, and a period can span up to 366 days.

<figure><img src="../.gitbook/assets/gamma-aim-agent-cost.png" alt="The Cost page of a registered agent, with the Last 30 days window, the Spend, Runs, and Avg cost per run figures, the What changed card, the Where the money goes card, and the Value declared card"><figcaption><p>The Cost page of an agent</p></figcaption></figure>

## What the page needs

Like the **Activity** page, the **Cost** page reads nothing until the agent's traffic can be told apart:

* **Nothing carries this agent's calls yet**. No proxy fronts the agent and it depends on no model or tool proxy. The **Proxy and tools** button opens the agent's **Proxies** page.
* **This agent's spend cannot be told apart yet**. The agent has no gateway application, so a shared proxy's bill can't be credited to it. The **Create its application** button opens the agent's **Identity** page.

## Read the page

<table>
    <thead>
        <tr>
            <th width="230">Section</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Key figures</td>
            <td><strong>Spend</strong>, <strong>Runs</strong>, and <strong>Avg cost per run</strong> for the period, each with its trend against the period before when that period had runs or spend. Spend is the model, tool, and human-decision cost on the proxies this agent uses, attributed to its gateway application. Runs are the POST requests on the proxy that fronts the agent, whoever sent them. The two can disagree: spend without runs means the agent called models or tools but received no inbound POST in the window. <strong>Avg cost per run</strong> is a dash when <strong>Runs</strong> is 0, not $0.00.</td>
        </tr>
        <tr>
            <td><strong>What changed</strong></td>
            <td>Up to four sentences, each tagged <strong>Needs attention</strong>, <strong>Worth a look</strong>, <strong>Looking good</strong>, or <strong>Info</strong>. Which ones appear depends on the period:<ul><li><strong>Nothing ran in this period</strong> when spend and runs are both 0.</li><li><strong>Nothing to compare with</strong> when the period before saw no runs and no spend.</li><li><strong>Spend up</strong> or <strong>Spend down</strong> with the percentage, <strong>Spend held steady</strong> when the change is under 10%, or <strong>Spending started this period</strong> when the period before spent nothing.</li><li><strong>Models</strong>, <strong>Tools</strong>, or <strong>Human decision</strong> <strong>added</strong> or <strong>saved</strong> an amount, only when that part moved by at least 10% of the previous period's spend.</li><li><strong>Human decisions are N% of spend</strong>, only when human cost is at least half of spend. It's tagged <strong>Info</strong>, not <strong>Needs attention</strong>.</li><li><strong>Peak on</strong> a date or hour, only when one bucket carries at least 25% of the spend and the period has at least three buckets.</li></ul></td>
        </tr>
        <tr>
            <td><strong>Where the money goes</strong></td>
            <td>The spend split into <strong>Models</strong>, <strong>Tools</strong>, and <strong>Human decision</strong>, with the <strong>Total spend</strong>.</td>
        </tr>
        <tr>
            <td><strong>Value declared</strong></td>
            <td>Tiles for <strong>Model spend</strong>, <strong>Tool spend</strong>, and <strong>Human decision cost</strong>, each with its share of spend, and <strong>Value delivered</strong>, the value the tools' owners declared for the successful tool calls in the period. The tile says <strong>Declared, not measured</strong>.</td>
        </tr>
        <tr>
            <td><strong>Spend over the period</strong></td>
            <td>The three parts stacked per bucket. Buckets are hourly for a period of up to two days and daily beyond.</td>
        </tr>
    </tbody>
</table>

Amounts are in US dollars. **View more in Observability** at the top of the page opens the **Agent — Overview** dashboard with the agent already selected.

## Read the Agent Overview dashboard

The **Agent — Overview** dashboard charts one agent across its MCP and LLM traffic. Open it from **Dashboards** in the **Observability** section of the sidebar, or from the **Cost** page. Its **Agent** filter selects the agent and is empty until you pick one.

The dashboard opens on the last 30 days and carries the following widgets:

* **Key Metrics**: **Total Model Spend**, **Total Tool Spend**, **Total Human Decision Cost**, **Total Tool Value**, **Approvals**, and **Total Calls**. **Total Tool Value** sums the value declared for the tool calls that were credited, which is the successful ones, so it's declared rather than measured.
* Over time: **Model Spend Over Time (USD)**, **Tool Cost Over Time (USD)**, **Human Decision Cost Over Time (USD)**, **Value Over Time (USD)**, and **Total Spend Over Time (USD)**, which stacks model, tool, and human cost.
* **Model Spend** and **Tool Spend** metric groups, each a row of tiles: **Cost (USD)**, **Tokens** or **Calls**, **Tokens / Call** or **Cost / Call**, and **Avg Time**.
* **Cost by Model**, **Top 5 Tools by Cost**, and **Human Decision Cost** by verdict.
* **Input vs Output Cost (USD)**, **Tool Calls Over Time**, and **Model Calls Over Time**.

The **MCP — Overview** dashboard also prices tool calls now. Its **Key Metrics** carry **Tool Cost** and **Avg Cost / Billed Call**, and it adds **Top 5 Tools by Cost**, **Tool Price Coverage**, and **Tool Cost Over Time**. **Tool Price Coverage** compares the calls that carried a rate with the calls that didn't, within the proxies that price at least one tool.

## Next steps

* [Agent FinOps](agent-finops.md). Set the prices the figures are built from.
* [Attribute business value to agent runs](attribute-business-value-to-agent-runs.md). Declare the value behind **Value delivered**.
* [Require human approval for MCP tool calls](../govern/require-human-approval-for-mcp-tool-calls.md). Price the human decisions that appear here.
