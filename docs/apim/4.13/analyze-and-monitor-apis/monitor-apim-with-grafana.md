---
description: Monitor APIM 4.13 APIs, consumers, and Gateways in Grafana with the Gravitee dashboard pack, SLO recording rules, and alerts.
---

# Monitor APIM with Grafana

## Overview

The Gravitee Grafana dashboard pack gives you six linked dashboards, from the program-wide view down to the headers and payloads of a single API call. It also includes Prometheus recording rules for service level objectives (SLOs) and ready-to-route alerts.

The following table lists the six dashboards and the question each one answers:

| Dashboard | What it answers |
| --- | --- |
| **API Program Overview** | How are all your APIs doing, who calls them, from where, and what does the Gateway reject and why? |
| **API Drill-down** | What's wrong with one API: which path, which consumer, which call? |
| **Consumers, Plans & Tenants** | Which applications and plans drive traffic, with what quality of service, and who hits their limits? |
| **Gateway Fleet & Runtime** | Are the Gateway nodes healthy: JVM, garbage collection, CPU, connections, backend connection pool? |
| **SLOs & Error Budgets** | Are your APIs meeting the availability objective, how fast is the error budget burning, and which API breaches it? |
| **Call Logs** | What exactly did one call send and receive, on the client side and on the backend side? |

Download the latest pack as [`gravitee-grafana-dashboards.zip`](https://github.com/gravitee-io-labs/gravitee-grafana-prometheus/releases/latest/download/gravitee-grafana-dashboards.zip). The dashboards, rules, and a Docker Compose demo stack are maintained in the [gravitee-grafana-prometheus](https://github.com/gravitee-io-labs/gravitee-grafana-prometheus) repository under the Apache 2.0 license. To try it on a local Docker Compose stack first, see [Monitor APIM with Prometheus and Grafana using Docker Compose](../how-to-guides/use-case-tutorials/monitor-apim-with-prometheus-and-grafana.md).

{% hint style="warning" %}
The dashboard pack is a Gravitee Labs project, provided as templates to adapt to your environment. Gravitee doesn't offer support for it.
{% endhint %}

{% hint style="info" %}
Without Elasticsearch or OpenSearch, use the OpenTelemetry edition of the pack. See [Monitor without Elasticsearch](#monitor-without-elasticsearch).
{% endhint %}

<figure><img src="../.gitbook/assets/grafana-api-program-overview.png" alt="The API Program Overview dashboard, with KPI tiles for calls, availability, error rates, response time and gateway overhead, followed by traffic, latency attribution, leaderboards, policy outcomes, and a world map of calls by country."><figcaption><p>The API Program Overview is the program-wide view, and the starting point for drilling down to one API.</p></figcaption></figure>

### Data sources

The dashboards add nothing to the request path. They read the following four sources that APIM already produces:

| Source | Content | Used for |
| --- | --- | --- |
| **API analytics**: `gravitee-v4-metrics-*` index in Elasticsearch or OpenSearch | One record per API call: API, application, plan, subscription, status, total, backend and Gateway latency, backend connect time and time to first byte, payload sizes, error key, rejecting component, client country and city, user agent, URI, transaction ID | Everything per API, per consumer, and per call |
| **Gateway metrics**: Prometheus endpoint of each Gateway | Gateway-wide request rates and status codes, connections, backend HTTP client, JVM, CPU, file descriptors | Real-time throughput, Gateway health, SLO burn rates, alerts |
| **Node monitoring**: `gravitee-monitor-*` index in Elasticsearch or OpenSearch | Per-node JVM, CPU, and memory snapshots | Gateway health where Prometheus isn't deployed |
| **API logs**, optional: `gravitee-v4-log-*` index in Elasticsearch or OpenSearch | Headers and payloads of logged calls, between the client and the Gateway and between the Gateway and the backend. Written only for APIs with logging enabled. | The Call Logs dashboard |

{% hint style="info" %}
The dashboards read v4 API analytics. v2 APIs report to the `gravitee-request-*` and `gravitee-log-*` indexes with a different structure, and aren't covered.
{% endhint %}

## Prerequisites

Before you begin, ensure you have met the following requirements:

* APIM 4.13 or later with the Elasticsearch or OpenSearch reporter enabled, which is the default. The pack is tested on APIM 4.13.5. Without the reporter, see [Monitor without Elasticsearch](#monitor-without-elasticsearch).
* Grafana. The pack is tested on Grafana 12.2.
* Prometheus, for the Gateway metrics, SLOs, and alerts. The pack is tested on Prometheus 3.5.

{% hint style="info" %}
A few panels use data available only with [Enterprise Edition](../introduction/enterprise-edition.md), for example the business dimensions set by the [Assign Metrics](../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md) policy. Without it, those panels stay empty and explain how to enable them.
{% endhint %}

## Install the dashboards

To install the dashboards, complete the following steps:

1. [Enable the Gateway metrics endpoint](#enable-the-gateway-metrics-endpoint)
2. [Configure Prometheus](#configure-prometheus)
3. [Add the data sources in Grafana](#add-the-data-sources-in-grafana)
4. [Import the dashboards](#import-the-dashboards)
5. [Enable API logging](#enable-api-logging)

### Enable the Gateway metrics endpoint

Enable the Prometheus metrics service and make the Gateway internal API reachable by Prometheus. For all the options, see [Expose metrics to Prometheus](logging/expose-metrics-to-prometheus.md).

{% code title="gravitee.yml" %}
```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
  core:
    http:
      host: 0.0.0.0
      port: 18082
      authentication:
        type: basic
        users:
          admin: <your-password>
```
{% endcode %}

{% hint style="warning" %}
Port `18082` serves the Gateway internal API. Restrict network access to it to your monitoring infrastructure.
{% endhint %}

### Configure Prometheus

1. Add a scrape job named `gravitee`. The node count, the node table, the **Node** selection and every Gateway Fleet & Runtime panel that depends on it, and the Gateway down, heap, GC, CPU, and backend error alerts select Gateways with `job="gravitee"`.
2. Load the rule files from the pack's `prometheus-rules` folder.

The following `prometheus.yml` example contains the scrape job and the rule files:

{% code title="prometheus.yml" %}
```yaml
rule_files:
  - /etc/prometheus/rules/gravitee-slo.rules.yml
  - /etc/prometheus/rules/gravitee-alerts.rules.yml

scrape_configs:
  - job_name: gravitee
    metrics_path: /_node/metrics/prometheus
    basic_auth:
      username: admin
      password: <your-password>
    static_configs:
      - targets: ['<gateway-1>:18082', '<gateway-2>:18082']
```
{% endcode %}

On Kubernetes, use your usual service discovery and keep the job name `gravitee`.

### Add the data sources in Grafana

You choose the data source names, because each dashboard lets you select them. Create the following data sources:

| Type | Index or URL | Time field |
| --- | --- | --- |
| Elasticsearch | `gravitee-v4-metrics-*` | `@timestamp` |
| Elasticsearch | `gravitee-monitor-*` | `@timestamp` |
| Elasticsearch, optional, for Call Logs | `gravitee-v4-log-*` | `@timestamp` |
| Prometheus | Your Prometheus URL | – |

To provision them instead, adapt the files in the pack's `grafana-provisioning/datasources` folder.

### Import the dashboards

1. In Grafana, open **Dashboards**.
2. Click **New**.
3. Select **Import dashboard**.
4. Upload a JSON file from the pack's `dashboards` folder.
5. Repeat for the six files.

To provision the dashboards instead, mount the `dashboards` folder and use `grafana-provisioning/dashboards/gravitee.yml`.

### Enable API logging

This step is optional. The **Call Logs** dashboard shows calls only for APIs with logging enabled. To enable it, see [Configure API-level logs](logging/configure-api-level-logs.md). Choose the modes, phases, and content to log, and set a request phase condition to limit the volume.

{% hint style="warning" %}
Before you enable logging, consider the following:

* The condition is evaluated in the request phase. It can select on request headers, path, method, or time, for example `{#request.headers['X-Debug'] != null}`, but not on the response status.
* A logged call with headers and payloads is several times larger than its analytics record. Log only what you need, and keep a short retention on the log index.
* Logs can contain personal data and credentials. The dashboard hides only the `X-Gravitee-Api-Key`, `Authorization`, `Proxy-Authorization`, `Cookie`, and `Set-Cookie` headers. An API key sent in another header, or credentials inside a payload, stay visible, and the index stores everything. Restrict access to the data source, and add your own header names to the Call Logs panels if needed.
{% endhint %}

## Verification

1. Open **Gravitee · API Program Overview**.
2. In the data source selectors, select your analytics and Prometheus data sources.
3. Check that **API calls** and **Gateway nodes up** show values.

## Use the dashboards

The following table lists the dashboard controls and their effect:

| Control | Effect |
| --- | --- |
| **Data source selectors** | Switch the analytics, node monitoring, and Prometheus data sources, for example between environments |
| **API** | Restrict all analytics panels to one or more APIs. In the API Drill-down, select the API to investigate. |
| **Filter (any field)** | In **API Program Overview**, **API Drill-down**, and **Consumers, Plans & Tenants**, add conditions on any analytics field. The filter applies to every analytics panel. Useful fields: `application-name.keyword`, `plan-id`, `status`, `error-key`, `geoip.country_iso_code`, `custom.<name>` |
| **Node** | In Gateway Fleet & Runtime, restrict panels to one or more Gateway instances |
| **API name** | In the API latency table, the top APIs leaderboards, and the per-API SLO table, opens the API Drill-down for that API with the same time range |
| **Gravitee dashboards** menu | Moves between the six dashboards, keeping the time range and selections |
| **A logged call** | In the **Call logs of this API** section of API Drill-down and in Call Logs, a call's time, URI, or request ID opens its headers and payloads in the **Call detail** section of Call Logs |
| **Call logs of this API** | In the API Drill-down controls, opens Call Logs filtered on the selected API |
| **Search payloads** | In Call Logs, a Lucene query on logged calls: payload content with wildcards, for example `*ORD-1234*`, or any field, for example `entrypoint-response.status:503` |
| **Panel ⓘ icon** | Explains what the panel measures and how to read it |
| **Inspect**, and then **Data** | Shows or exports the data behind a panel as CSV |

In a typical investigation, an alert fires, **SLOs & Error Budgets** shows which API burns its budget, and you select it. **API Drill-down** then shows the affected paths and applications, whether the time is spent in the backend or the Gateway, and the failing calls. Select a logged call to see in **Call Logs** what the client sent, what the backend received, and what it returned.

## Dashboard reference

### API Program Overview

The API Program Overview dashboard has the following sections:

| Section | Content | How to read it |
| --- | --- | --- |
| At a glance | Calls, availability, 5xx and 4xx share, P95 response time, P95 Gateway overhead, active APIs and applications, rate-limited calls, rejected credentials, data served, Gateway nodes up | 4xx are consumer errors and don't count against availability. |
| Traffic | Calls by status class and by API, 5xx rate by API, real-time Gateway throughput | A 5xx spike on one API points to its backend. A spike on all APIs points to the platform. |
| Latency attribution | Response time percentiles, total vs backend vs Gateway overhead, share of time in each, latency per API | When total follows the backend, the slowness is upstream. When it follows the Gateway overhead, review the API's policies. |
| Leaderboards | Top APIs by calls, 5xx, and P95; top applications, plans, and paths | |
| Policy & security outcomes | Rejections by [error key](gateway-error-key-reference.md) and by policy, 429 by application, credential failures by API, backend failures by API | Separates calls the Gateway refused, for example for a rate limit or invalid credentials, from calls the backend failed. |
| Consumers & geography | Calls by country on a map, top countries with their P95, client types | |

### API Drill-down

The API Drill-down dashboard has the following sections:

| Section | Content |
| --- | --- |
| API health | Calls, availability, error rate, P95 total, backend, and Gateway overhead |
| Traffic & errors | Status classes and codes over time, HTTP methods, error keys, payload sizes |
| Latency deep-dive | P95 split into total, backend, backend time to first byte, backend connect, and Gateway overhead; response time heatmap; per-path table with calls, P50, P95, max, and 5xx |
| Consumers of this API | Applications with calls, P95, and errors; traffic by application, plan, country, and client type |
| Investigate | Latest failed calls and calls slower than 500 ms, with request ID, status, method, URI, error key, application, plan, timings, and client IP. When the call was logged, the request ID opens it in Call Logs. |
| Call logs of this API | Failed calls and latest calls of this API that have a call log. Select a call's time, URI, or request ID to open its headers and payloads in Call Logs. Empty when logging isn't enabled on the API. |

{% hint style="info" %}
Connect time spikes point to network, DNS, or TLS issues toward the backend. A rising time to first byte with a flat connect time means the backend itself is slow.
{% endhint %}

### Consumers, Plans & Tenants

The Consumers, Plans & Tenants dashboard has the following sections:

* **Applications**. The **Application scorecard** shows calls, P95, number of APIs used, bytes served, 4xx, 5xx, and rate-limited calls for each application.
* **Plans & subscriptions**. Shows usage by API and plan, number of applications per plan, and most active subscriptions.
* **Business dimensions**. Shows traffic by tenant, channel, and plan name. These panels need custom metrics, as described in [Add business dimensions](#add-business-dimensions).
* **Where consumers are**. Shows a map, operating systems and devices, and user agents.

### Gateway Fleet & Runtime

The following table lists the sections of the Gateway Fleet & Runtime dashboard and what to watch for in each:

| Section | Watch for |
| --- | --- |
| Fleet at a glance | Nodes down, uneven load, heap above 75%, recent restarts |
| Inbound traffic | Request rate and status codes per node, response time, client connections, network throughput |
| Outbound traffic | Backend calls by status, backend response time, connection pool. A pool pinned at its maximum while latency rises indicates backend saturation. |
| JVM | Heap against its maximum, GC time per second, allocation rate, threads, off-heap buffers. GC time above 5% sustained affects tail latency. |
| Host & process | CPU, load against CPU count, open file descriptors |
| Node monitoring | Heap, memory, and CPU per node from the monitoring index, without Prometheus |

### SLOs & Error Budgets

The default objective is 99.5% of calls without a server error over 30 days, an error budget of 0.5%. The dashboard has the following panels:

* **Availability SLI (30d)** and **Error budget remaining** show the position against the monthly objective.
* **Error budget burn rate** compares the error rate with the allowed pace. At `1`, the budget lasts exactly 30 days.
* **Per-API SLO compliance** lists availability, the share of the budget used, P95, P99, and slow calls for each API over the selected range. Above 100% used, the API missed its objective for the period.

### Call Logs

The Call Logs dashboard has the following sections:

| Section | Content |
| --- | --- |
| Logged calls | Logged calls and their share of all calls, logged failures, calls the Gateway answered without calling the backend, and rejections by error key |
| Call log explorer | Latest logged failed calls and all logged calls, with the client status and the backend status. `not called` means the Gateway rejected the call, for example for plan security or rate limiting. |
| Call detail | One call, selected by request ID, or the latest call: a summary, the body at each hop, and the headers at each hop |

The hops are client to Gateway, Gateway to backend, backend to Gateway, and Gateway to client. Compare the first two, or the last two, to see what the API's policies changed.

<figure><img src="../.gitbook/assets/grafana-call-logs.png" alt="The Call Logs dashboard, with logged call counts, a list of logged failed calls with client and backend status, and the detail of one call: summary, payloads, and headers at each hop."><figcaption><p>Compare the headers and payloads at each hop to see what the API's policies changed.</p></figcaption></figure>

## Alerts

Route the alerts with Alertmanager or Grafana alerting. The `gravitee-alerts.rules.yml` file defines the following alerts:

| Alert | Condition | Severity |
| --- | --- | --- |
| `GraviteeGatewayDown` | A Gateway can't be scraped for 1 minute | critical |
| `GraviteeErrorBudgetFastBurn` | Burn rate above 14.4 on both the 5-minute and 1-hour windows | critical |
| `GraviteeErrorBudgetSlowBurn` | Burn rate above 6 on both the 30-minute and 6-hour windows | warning |
| `GraviteeHighLatency` | Average response time above 500 ms for 5 minutes | warning |
| `GraviteeHeapPressure` | Heap above 90% for 10 minutes | warning |
| `GraviteeGcPressure` | More than 10% of time in garbage collection for 10 minutes | warning |
| `GraviteeHighCpu` | Process CPU above 85% for 10 minutes | warning |
| `GraviteeBackendErrors` | More than 10% of backend calls return 5xx for 5 minutes | warning |

## Customize

### Add business dimensions

The [Assign Metrics](../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md) policy, available with [Enterprise Edition](../introduction/enterprise-edition.md), adds a value to the analytics record of each call, as `custom.<name>`. The **Consumers, Plans & Tenants** dashboard charts `custom.tenant`, `custom.plan`, and `custom.channel`. Use any other name in the **Filter** bar.

```json
{
  "policy": "policy-assign-metrics",
  "configuration": {
    "scope": "REQUEST",
    "metrics": [
      {
        "name": "tenant",
        "value": "{#request.headers['X-Tenant-ID'] != null ? #request.headers['X-Tenant-ID'][0] : 'unknown'}"
      }
    ]
  }
}
```

{% hint style="warning" %}
When the expression returns `null`, the metric is dropped from the record. Always provide a fallback value.
{% endhint %}

To show plan names instead of plan IDs, add the policy to each plan's flow with a fixed value, for example `"name": "plan", "value": "Gold"`.

### Change the objectives and thresholds

To change the defaults, edit the following:

* **SLO objective**. Replace `0.005` in `gravitee-slo.rules.yml`, for example with `0.001` for 99.9%, and in the **Error budget used** calculation of the per-API SLO table.
* **Colors**. Edit a panel, and then change its **Thresholds**.
* **Alerts**. Edit the conditions in `gravitee-alerts.rules.yml`.

## Monitor without Elasticsearch

The OpenTelemetry edition of the pack gives six matching dashboards, titled `Gravitee OTel · <name>`, without an analytics store. **Consumers, Plans & Tenants** becomes **Consumers & Plans**. The Gateway sends OpenTelemetry traces and logs to an OpenTelemetry Collector. The collector derives per-API metrics from the spans for Prometheus, stores the traces in Tempo, and stores the logged payloads in Loki.

```text
Gateway ─ OTLP traces + logs ─► OpenTelemetry Collector ─┬─ metrics derived from spans ─► Prometheus
        │                                                ├─ traces                      ─► Tempo
        │                                                └─ OpenTelemetry logs          ─► Loki
        └─ /_node/metrics/prometheus (JVM, CPU, HTTP) ──────────────────────────────────► Prometheus
```

Download the OpenTelemetry pack as [`gravitee-grafana-dashboards-otel.zip`](https://github.com/gravitee-io-labs/gravitee-grafana-prometheus/releases/latest/download/gravitee-grafana-dashboards-otel.zip). Its `README.md` contains the complete installation guide, and the [`otel` folder](https://github.com/gravitee-io-labs/gravitee-grafana-prometheus/tree/main/otel) of the repository contains a Docker Compose demo stack.

Every call can be opened as a trace that shows its phases, plan flow, each policy with its duration, and the backend call. The pack also includes per-API SLO recording rules, per-API burn-rate and latency alerts, and alerts on the telemetry pipeline itself.

To set up the OpenTelemetry edition, complete the following steps:

1. [Configure APIM](#configure-apim)
2. [Deploy the collector, Prometheus, Tempo, and Loki](#deploy-the-collector-prometheus-tempo-and-loki)

### Prerequisites

Before you begin, ensure you have met the following requirements:

| Component | Version or setting |
| --- | --- |
| APIM | 4.13 or later, v4 APIs, with the OpenTelemetry reporter. Tested on 4.13.5. |
| OpenTelemetry Collector | *contrib* distribution, for the `spanmetrics` connector. Tested on 0.115. |
| Prometheus | Tested on 3.5 |
| Tempo | 2.7 or later. The trace tables use the `most_recent` search hint. |
| Loki | 3.0 or later, with structured metadata allowed |
| Grafana | Tested on 12.2 |

### Configure APIM

1.  Configure the Gateway to send traces and logs to the collector, enable the OpenTelemetry reporter, and disable the Elasticsearch reporter:

    {% code title="gravitee.yml" %}
    ```yaml
    services:
      opentelemetry:
        enabled: true
        exporter:
          endpoint: http://otel-collector:4317
          protocol: grpc
          logsEndpoint: http://otel-collector:4318/v1/logs
      metrics:
        enabled: true
        prometheus:
          enabled: true
    reporters:
      otel:
        enabled: true
      elasticsearch:
        enabled: false
    ```
    {% endcode %}

    The `logsEndpoint` always uses OTLP over HTTP. For the Gateway internal API settings, see [Enable the Gateway metrics endpoint](#enable-the-gateway-metrics-endpoint).
2.  On the Management API, set `repositories.analytics.type` to `none` to run without an analytics store.
3.  On each API, enable tracing, and enable OpenTelemetry logs where you want payloads. In the Management Console, open the API's reporter settings. With the Management API, set the `analytics` block of the v4 API:

    ```json
    "analytics": {
      "enabled": true,
      "tracing": { "enabled": true, "verbose": false },
      "otelLogs": { "enabled": true },
      "logging": {
        "mode": { "entrypoint": true, "endpoint": true },
        "phase": { "request": true, "response": true },
        "content": { "payload": true },
        "condition": "{#request.id.hashCode() % 5 == 0}"
      }
    }
    ```

    Tracing must be enabled on every call, because the per-API metrics are computed from the spans. OpenTelemetry logs follow the API's logging settings and condition. For more information, see [OpenTelemetry](opentelemetry.md) and [Enable and use OpenTelemetry logs for APIs](enable-and-use-opentelemetry-logs-for-apis.md).

### Deploy the collector, Prometheus, Tempo, and Loki

1. Run the OpenTelemetry Collector with the pack's `collector/collector.yaml`. It exposes `gravitee_calls_total` and `gravitee_duration_milliseconds` on port `8889`, and sends traces to Tempo and logs to Loki. Adjust the Tempo and Loki addresses.
2. In Prometheus, add the scrape jobs from `prometheus-rules/scrape-config.example.yml` and load the rule files from `prometheus-rules`.
3. Deploy Tempo and Loki. The pack's `collector/tempo.yaml` and `collector/loki.yaml` are single-process examples. Loki must allow structured metadata.
4. In Grafana, add the Prometheus, Tempo, and Loki data sources and import the dashboards. The pack's `grafana-provisioning/datasources/datasources.yml` links traces to logs and logs to traces.

### Differences with the Elasticsearch edition

OpenTelemetry signals don't carry everything the analytics record contains, and the dashboards don't chart everything the signals carry. The following table lists what isn't charted and the closest alternative:

| Not charted | Closest alternative |
| --- | --- |
| Client country, city, and world map | The client IP is on each trace. |
| User agents and per-path tables | Search traces in Tempo by `span.user_agent.original` or `span.http.target`. As metric labels, they create too many series. |
| Plan IDs | Plans appear through their flow name, for example `plan-gold plan`. A plan without a flow isn't counted. |
| Business dimensions from Assign Metrics | – |
| The **Filter (any field)** bar | – |
| Headers in Call Logs | OpenTelemetry logs contain bodies only. The trace shows the call's path through the Gateway. |
| Rejection reason for plan security failures | The 401 and 403 counts. |
| Payload sizes | The server span carries `http.request.body.size` and `http.response.body.size`, from `Content-Length`. They show on each trace. |
| Backend connect time and time to first byte | The backend time from the client span. |

The Gateway overhead is an average, the server span minus the backend span, because percentiles can't be subtracted.

{% hint style="warning" %}
Before you deploy the OpenTelemetry edition, consider the following:

* Every call is traced, at about 13 spans per call. Size Tempo's retention accordingly.
* The number of metric series grows with APIs, applications, status codes, and methods. Each dimension added in `collector.yaml` multiplies it.
* Traces contain client IPs and URLs, and OpenTelemetry logs contain payloads. Restrict access to the Tempo and Loki data sources.
{% endhint %}

## Troubleshooting

The following table lists common symptoms and what to check:

| Symptom | Check |
| --- | --- |
| Analytics panels are empty | The data source uses the `gravitee-v4-metrics-*` index and the `@timestamp` time field. The APIs are v4 APIs with analytics enabled. The time range contains traffic. |
| **Gateway nodes up** is `0` | The metrics service is enabled, the internal API listens on a reachable interface, the job is named `gravitee`, and the credentials match. To check the target in Prometheus, open **Status**, and then click **Target health**. |
| Throughput is higher than the API traffic | HTTP server metrics include the scrapes of the internal API. The HTTP server panels, the SLO recording rules, and the `GraviteeHighLatency` alert keep `local` values ending in `:8082`. If your Gateway listens on another port, update the filter in the dashboards, in `gravitee-slo.rules.yml`, and in `gravitee-alerts.rules.yml`. |
| SLO panels are empty | The recording rules are loaded. The 30-day SLI fills as history accumulates. |
| Tenant, channel, or plan name panels are empty | These panels need the Assign Metrics policy, which requires Enterprise Edition. |
| The map has no background | The basemap loads public Esri tiles. The browser needs access to `services.arcgisonline.com`. |
| Call Logs is empty | Logging is enabled on the API and its condition matches calls. The data source uses the `gravitee-v4-log-*` index. A request ID opened from API Drill-down shows nothing when that call wasn't logged. |
| A Call Logs search finds nothing | Payloads are split on spaces only: use wildcards, for example `*EUR*`. Headers are stored but not searchable. |
