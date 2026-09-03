---
hidden: false
noIndex: false
description: >-
  Declare what good looks like for a proxy or an agent. A performance target
  names the traffic it judges, the window it judges it over, and the rules that
  set each threshold.
---

# Performance targets

Observability tells you what your proxies and agents did. On its own it doesn't tell you whether what they did was acceptable, because the expectation lives in someone's head instead of in the platform. A performance target moves that expectation into the product. It declares the metrics that matter for one subject and the thresholds beyond which the subject's behavior stops being acceptable, and each evaluation records whether those thresholds were met.

A rule's metric comes from the analytics vocabulary the platform already publishes per API type. Every threshold is therefore written against telemetry the gateway recorded for the APIs in the subject.

## What a target declares

Every target names the traffic it judges, the period and sampling floor it judges that traffic over, and at least one rule.

<table>
    <thead>
        <tr>
            <th width="200">Declaration</th>
            <th>What it sets</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Subject</td>
            <td>The APIs whose gateway telemetry the target evaluates. A subject holds several APIs, so one target covers both an agent's A2A Proxy and the LLM Proxy its calls are routed through.</td>
        </tr>
        <tr>
            <td>Window</td>
            <td>The rolling period each evaluation measures.</td>
        </tr>
        <tr>
            <td>Evaluation interval</td>
            <td>How often the target is evaluated. The window is at least as long as the interval.</td>
        </tr>
        <tr>
            <td>Minimum sample size</td>
            <td>The number of samples a rule needs inside the window before its result counts. A rule with fewer samples than this floor returns no verdict rather than a pass.</td>
        </tr>
        <tr>
            <td>Rules</td>
            <td>One or more comparisons of a measured metric against a threshold. A target carries at least one.</td>
        </tr>
    </tbody>
</table>

## How a rule is built

A rule is a single comparison: take one measure of one metric over the window, and compare it against a threshold.

<table>
    <thead>
        <tr>
            <th width="180">Part</th>
            <th>What it sets</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Metric</td>
            <td>What is measured, drawn from the analytics metric vocabulary rather than from a list specific to targets. See <a href="#available-metrics">Available metrics</a>.</td>
        </tr>
        <tr>
            <td>Measure</td>
            <td>Which statistic of that metric to read, for example <code>P95</code> or <code>AVG</code>. Each metric declares the measures it supports.</td>
        </tr>
        <tr>
            <td>Operator</td>
            <td>The comparison to apply: <code>LT</code> (below), <code>LTE</code> (at most), <code>GT</code> (above), or <code>GTE</code> (at least).</td>
        </tr>
        <tr>
            <td>Threshold</td>
            <td>The value the measure is compared against.</td>
        </tr>
        <tr>
            <td>API types</td>
            <td>Optional. Restricts the rule to the subject's APIs of the named types. A rule that names no type applies to the whole subject.</td>
        </tr>
        <tr>
            <td>Filters</td>
            <td>Optional. Narrows the measure further using the analytics filter vocabulary, for example a single MCP tool.</td>
        </tr>
    </tbody>
</table>

### Scope a rule to one API type

On a subject that mixes API types, a rule that names no type mixes inbound and outbound traffic. Scoping a rule to an API type keeps each comparison on the traffic it belongs to. Latency stays on the A2A Proxy that fronts the agent, and token cost stays on the LLM Proxy the agent calls. A rule that names API types is evaluated only against the subject's APIs of those types, and it names only types the subject already holds.

### Narrow a rule with a filter

A filter cuts the measure down to part of the traffic before the comparison runs, so a target speaks about one tool or one model instead of the whole proxy. Filters come from the analytics filter vocabulary, and each metric publishes the filters it accepts:

* On an MCP Proxy, `MCP_PROXY_TOOL` and `MCP_PROXY_METHOD` scope a rule to a single tool or method.
* On an LLM Proxy, `LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` scope a rule to a single model or provider.

All four of these filters accept the `EQ` and `IN` operators.

## Target outcomes

Every rule produces its own outcome, and the target's status is the worst status among its rules.

<table>
    <thead>
        <tr>
            <th width="200">Outcome</th>
            <th width="180">Recorded status</th>
            <th>Meaning</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Met</td>
            <td><code>PASS</code></td>
            <td>The observed value satisfied the rule's comparison.</td>
        </tr>
        <tr>
            <td>Missed</td>
            <td><code>BREACH</code></td>
            <td>The observed value didn't satisfy the rule's comparison.</td>
        </tr>
        <tr>
            <td>No verdict</td>
            <td><code>NOT_EVALUABLE</code></td>
            <td>The rule had fewer samples than the target's minimum, or no data at all. This outcome is never reported as a pass.</td>
        </tr>
    </tbody>
</table>

The third outcome is what keeps a target honest about an idle subject. A rule with no data at all is reported the same way. A subject that saw no traffic in the window is reported as having no verdict, not as meeting its thresholds.

## What an evaluation records

An evaluation is stored per window, and it keeps enough of the rule alongside the number to stay readable on its own.

<table>
    <thead>
        <tr>
            <th width="200">Recorded</th>
            <th>What it holds</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Observed value</td>
            <td>The value measured for the rule's metric and measure.</td>
        </tr>
        <tr>
            <td>Threshold and operator</td>
            <td>The comparison the rule declared.</td>
        </tr>
        <tr>
            <td>Deviation</td>
            <td>How far the observed value sits from the threshold, as an absolute value in the metric's unit and as a ratio of the threshold.</td>
        </tr>
        <tr>
            <td>Sample count</td>
            <td>How many samples the rule was computed from.</td>
        </tr>
        <tr>
            <td>Rule status</td>
            <td>The outcome of that rule.</td>
        </tr>
        <tr>
            <td>Window bounds</td>
            <td>The start and end of the period measured.</td>
        </tr>
        <tr>
            <td>Covered APIs</td>
            <td>The APIs the evaluation covered.</td>
        </tr>
        <tr>
            <td>Evaluation time</td>
            <td>When the evaluation ran.</td>
        </tr>
    </tbody>
</table>

## Available metrics

A rule's metric and measure come from the analytics definition, the same vocabulary the dashboards and the analytics endpoints publish. A metric is available to a rule only on the API types the definition declares it for, so the vocabulary differs per proxy type.

### Available on LLM, MCP, and A2A Proxies

These metrics are declared for all three agent proxy types:

<table>
    <thead>
        <tr>
            <th width="290">Metric</th>
            <th width="180">Label</th>
            <th width="230">Measures</th>
            <th>Unit</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>HTTP_REQUESTS</code></td>
            <td>HTTP Requests</td>
            <td><code>COUNT</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>HTTP_ERRORS</code></td>
            <td>HTTP Errors</td>
            <td><code>COUNT</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>HTTP_ERROR_RATE</code></td>
            <td>Error Rate</td>
            <td><code>PERCENTAGE</code></td>
            <td><code>PERCENT</code></td>
        </tr>
        <tr>
            <td><code>HTTP_GATEWAY_RESPONSE_TIME</code></td>
            <td>Gateway response time</td>
            <td><code>AVG</code>, <code>MIN</code>, <code>MAX</code>, <code>P90</code>, <code>P95</code>, <code>P99</code></td>
            <td><code>MILLISECONDS</code></td>
        </tr>
        <tr>
            <td><code>HTTP_GATEWAY_LATENCY</code></td>
            <td>Latency</td>
            <td><code>AVG</code>, <code>MIN</code>, <code>MAX</code>, <code>P90</code>, <code>P95</code>, <code>P99</code></td>
            <td><code>MILLISECONDS</code></td>
        </tr>
        <tr>
            <td><code>HTTP_ENDPOINT_RESPONSE_TIME</code></td>
            <td>Endpoint response time</td>
            <td><code>AVG</code>, <code>MIN</code>, <code>MAX</code>, <code>P90</code>, <code>P95</code>, <code>P99</code></td>
            <td><code>MILLISECONDS</code></td>
        </tr>
        <tr>
            <td><code>HTTP_REQUEST_CONTENT_LENGTH</code></td>
            <td>Request content length</td>
            <td><code>AVG</code>, <code>MIN</code>, <code>MAX</code>, <code>P90</code>, <code>P95</code>, <code>P99</code></td>
            <td><code>BYTES</code></td>
        </tr>
        <tr>
            <td><code>HTTP_RESPONSE_CONTENT_LENGTH</code></td>
            <td>Response content length</td>
            <td><code>AVG</code>, <code>MIN</code>, <code>MAX</code>, <code>P90</code>, <code>P95</code>, <code>P99</code></td>
            <td><code>BYTES</code></td>
        </tr>
    </tbody>
</table>

### Available on LLM Proxies only

Token and cost metrics are declared for the LLM API type alone, so a rule that uses one is rejected on a subject that holds no LLM Proxy:

<table>
    <thead>
        <tr>
            <th width="290">Metric</th>
            <th width="180">Label</th>
            <th width="230">Measures</th>
            <th>Unit</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>LLM_PROMPT_TOKEN_SENT</code></td>
            <td>Sent token count</td>
            <td><code>COUNT</code>, <code>AVG</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>LLM_PROMPT_TOKEN_RECEIVED</code></td>
            <td>Received token count</td>
            <td><code>COUNT</code>, <code>AVG</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>LLM_PROMPT_TOTAL_TOKEN</code></td>
            <td>Total token count</td>
            <td><code>COUNT</code>, <code>AVG</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>LLM_PROMPT_TOKEN_SENT_COST</code></td>
            <td>Sent token cost</td>
            <td><code>COUNT</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>LLM_PROMPT_TOKEN_RECEIVED_COST</code></td>
            <td>Received token cost</td>
            <td><code>COUNT</code></td>
            <td><code>NUMBER</code></td>
        </tr>
        <tr>
            <td><code>LLM_PROMPT_TOKEN_TOTAL_COST</code></td>
            <td>Total token cost</td>
            <td><code>COUNT</code>, <code>AVG</code></td>
            <td><code>NUMBER</code></td>
        </tr>
    </tbody>
</table>

For what the gateway records behind the token and cost metrics, and how cost is derived from the model prices, see [Monitor your LLM proxy](monitor-your-llm-proxy.md).

## What a target rejects

A target is checked against the analytics definition and against the APIs of its subject, both when it's created and when it's changed. A rule that no telemetry answers is refused rather than left to evaluate to nothing.

<table>
    <thead>
        <tr>
            <th width="330">Rejected</th>
            <th>Reason</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>An evaluation interval of zero or less</td>
            <td>The interval is positive.</td>
        </tr>
        <tr>
            <td>A window shorter than the evaluation interval</td>
            <td>The window is at least as long as the interval.</td>
        </tr>
        <tr>
            <td>A minimum sample size below <code>1</code></td>
            <td>The minimum sample size is at least <code>1</code>.</td>
        </tr>
        <tr>
            <td>A target with no rules</td>
            <td>A target carries at least one rule.</td>
        </tr>
        <tr>
            <td>A subject naming an API from another environment</td>
            <td>A target evaluates only APIs of its own environment.</td>
        </tr>
        <tr>
            <td>A subject naming an API that isn't a v4 API</td>
            <td>A target evaluates v4 APIs.</td>
        </tr>
        <tr>
            <td>A rule naming an API type the subject doesn't hold</td>
            <td>Scoping resolves against the subject's own APIs.</td>
        </tr>
        <tr>
            <td>A rule naming a metric the analytics definition doesn't declare</td>
            <td>Metrics come from the published vocabulary.</td>
        </tr>
        <tr>
            <td>A rule naming a measure the metric doesn't support</td>
            <td>Each metric declares its own measures.</td>
        </tr>
        <tr>
            <td>A rule naming a metric that isn't declared for one of the rule's API types</td>
            <td>Each metric declares the API types it applies to. An LLM cost rule on an A2A-only subject is refused for this reason.</td>
        </tr>
        <tr>
            <td>A threshold below <code>0</code></td>
            <td>No metric unit takes a negative threshold.</td>
        </tr>
        <tr>
            <td>A threshold above <code>100</code> on a metric whose unit is <code>PERCENT</code></td>
            <td>A <code>PERCENT</code> threshold stays between <code>0</code> and <code>100</code>.</td>
        </tr>
        <tr>
            <td>A filter with no value</td>
            <td>A filter compares against a value.</td>
        </tr>
        <tr>
            <td>A filter the analytics definition doesn't declare</td>
            <td>Filters come from the published vocabulary.</td>
        </tr>
        <tr>
            <td>A filter the rule's metric doesn't accept</td>
            <td>Each metric declares the filters it accepts.</td>
        </tr>
        <tr>
            <td>A filter operator the filter doesn't support</td>
            <td>Each filter declares its own operators.</td>
        </tr>
        <tr>
            <td>A filter that isn't declared for one of the rule's API types</td>
            <td>Each filter declares the API types it applies to.</td>
        </tr>
    </tbody>
</table>

## Limitations

Two limits shape what a target is able to say.

MCP and A2A traffic is measured at the HTTP level. The analytics definition declares no MCP-specific or A2A-specific metric, so targets on those proxy types are built from request volume, error counts, error rate, latency, and payload size. Protocol-level signals such as JSON-RPC errors returned inside a successful HTTP response, or A2A task states, aren't part of the metric vocabulary, so no threshold reads them.

Deleting an API removes it from the subject of every target that named it. The target itself stays, including when the deletion leaves it with no APIs.

## What's next

* [Monitor your LLM proxy](monitor-your-llm-proxy.md): read token usage, cost, and model and provider mix for LLM Proxies on the LLM Overview dashboard.
* [Monitor your MCP servers](monitor-your-mcp-servers.md): monitor tool invocation metrics, error rates, and latency for your MCP Proxies.
* [Inspect your agent log](inspect-your-agent-log.md): trace every agent invocation through the AI Gateway with OpenTelemetry spans.
