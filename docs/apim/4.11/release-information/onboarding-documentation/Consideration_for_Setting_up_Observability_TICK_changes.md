# Setting Up Observability

This page outlines the strategy for implementing monitoring, analytics, and alerting across your Gravitee ecosystem. Learn how to identify core metrics, use built-in dashboards, and integrate external observability stacks to ensure platform health and track business value.

## Deliverables

* **Monitoring Framework:** A defined set of key performance indicators (KPIs) and metrics.
* **Alerting System:** Real-time notifications for critical system events and threshold breaches.
* **Observability Pipeline:** Functional data export to external tools for long-term storage and advanced analysis.
* **Operational Dashboards:** Visibility into API usage, latency, error rates, and infrastructure health.

## Stakeholders

Involve the following stakeholders in observability planning:

* **Platform Engineers:** To deploy and manage infrastructure-level monitoring.
* **API Developers:** To define specific metrics and thresholds for individual APIs.
* **DevOps and SRE Teams:** To manage alerting rules and incident response.
* **Business Owners:** To define and track business-centric KPIs and revenue impact.

## Prerequisites

* **License:** Gravitee Enterprise Edition is required for Alert Engine and advanced reporters.
* **People:** Personnel with knowledge of Gravitee architecture and experience with observability tools.
* **Knowledge:** Understanding of your organization's Service Level Objectives (SLOs) and existing observability stack.

## Anticipated Duration

* **Two weeks:** Minimum one week for initial configuration, with additional time for fine-tuning and external integration.

## Potential Risks and Challenges

* **Log Volume and Cost:** High-detail logging can lead to significant storage costs in external platforms.
* **Metric Cardinality:** Excessive per-API labels in external tools can impact monitoring performance.
* **Blind Spots:** Over-reliance on internal gateway metrics without synthetic monitoring for external reachability.
* **Security and PII:** Capturing sensitive data in logs if masking policies are incorrectly applied.

## Actions and Activities

### Review Observability Options
Review the following Gravitee observability options:
* [Analyze and monitor APIs](https://documentation.gravitee.io/apim/analyze-and-monitor-apis)
* [In-platform audit trails and dashboards](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/audit-trail)
* [Integrating with reporters](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/reporters)
* [OpenTelemetry](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/opentelemetry)

### Define Key Metrics
Identify the core data points required for your environment, including:
* API usage
* Error codes (4xx, 5xx)
* Latency
* Request volumes
* Quota consumption

### Use Built-in Dashboards
Access the Management Console to view the Platform Overview, API Traffic, and API Health-check dashboards for immediate insights into performance and availability.

### Configure Alert Engine
Set up real-time alerts for critical events, such as unhealthy gateway instances, error rate spikes, or SLO breaches. Configure notifications for your preferred communication channels.

### Enable External Integrations
Select your enterprise observability stack. Use Gravitee reporters to export data to external databases or monitoring platforms. For Prometheus and Grafana, enable the Prometheus endpoint in your gateway configuration and set up your scraper.

### Implement Advanced Logging
Configure per-API logging for headers and payloads. Use the Data Masking policy to ensure PII is obfuscated before logs are routed to your centralized platform.

### Set Up Distributed Tracing
Enable OpenTelemetry to trace requests across your microservices architecture. Ensure your backend services are instrumented to propagate the Trace ID received from the gateway.

### Establish Baselines
Analyze normal API behavior to set realistic thresholds for alerts. This reduces false positives while ensuring critical issues are identified early.

## Best Practices

{% hint style="info" %}
Focus on the four golden signals: latency, traffic, errors, and saturation at the infrastructure level.
{% endhint %}

### Use Outside-In Monitoring
Do not rely solely on gateway metrics. Use regional synthetic probes to confirm the reachability and uptime of your APIs from the public internet.

### Correlate Technical and Business Data
Link API failures to business outcomes. For example, analyze how a 5% error rate impacts revenue or customer transactions.

### Integrate with Security Tools
Pipe your logs into a Security Information and Event Management (SIEM) tool for anomaly detection and immutable audit trails.

### Maintain Your Configuration
Regularly test alert rules and update thresholds as your traffic patterns evolve.
