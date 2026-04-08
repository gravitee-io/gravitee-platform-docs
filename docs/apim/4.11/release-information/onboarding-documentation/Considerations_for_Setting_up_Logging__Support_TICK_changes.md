# Setting Up Logging and Support

This page outlines the strategy for implementing a robust logging and support model for your Gravitee deployment. Learn how to configure gateway and API-level logging, implement memory safeguards like **LogGuard**, and define a multi-tier support model to handle incidents effectively without compromising system stability.

## Deliverables

* **Logging Policy:** A configured policy that balances observability with system performance.
* **LogGuard Protection:** Automated protection against memory-related crashes.
* **Support Matrix:** A defined L1–L3 matrix for incident resolution.
* **Observability Integration:** Integration with external platforms for long-term retention and audit compliance.

## Stakeholders

Involve the following stakeholders in logging and support planning:

* **Platform Engineers:** To configure gateway infrastructure and LogGuard settings.
* **API Developers:** To define per-API logging requirements and data masking.
* **Security and Compliance Officers:** To verify log retention and PII masking policies.
* **Support and Operations Teams:** To execute the multi-tier support model.

## Prerequisites

* **License:** Gravitee Enterprise Edition is required for advanced features like LogGuard and specific external reporters.
* **People:** Access to infrastructure leads and API product owners.
* **Knowledge:** Familiarity with Gravitee Expression Language (EL) and your chosen observability backend.

## Anticipated Duration

* **Minimum one week:** This includes environment-specific testing of logging thresholds and alignment of support responsibilities across teams.

## Potential Risks and Challenges

* **Performance Degradation:** Excessive logging in production can increase heap pressure and latency.
* **Storage Costs:** High-volume logging can exceed budgets in external observability tools.
* **Security Leaks:** Failure to use the **Data Logging Masking** policy can lead to PII or credentials appearing in plain text logs.

## Actions and Activities

### Configure Gateway Logging Thresholds
Define global limits in `gravitee.yml` to prevent logs from consuming excessive memory. If you use Gravitee Cloud, some of these limits are managed automatically.

1. Navigate to the reporters section of your configuration.
2. Set the `max_size` property to 256 KB for production environments.
3. Enable **LogGuard** to prevent out-of-memory crashes.

### Implement Per-API Logging
For specific APIs that require deeper visibility:

1. In the Management Console, select your API.
2. Navigate to **Proxy > Logging**.
3. Choose the logging level, such as **Headers and payloads**.
4. Apply a condition using EL to log only non-200 responses and conserve resources.

### Secure and Route Data
1. Add the **Data Logging Masking** policy to your API flow to scrub sensitive fields.
2. Configure your reporters, such as Elasticsearch, Splunk, or Datadog, to forward logs asynchronously.
3. Synchronize all components to a single NTP source using UTC to ensure consistent trace correlation.

### Establish the Support Matrix
Assign responsibilities according to the following tiers:

* **L1 (Service Desk):** Uses Developer Portal logs to assist with login or API key issues.
* **L2 (API Platform Team):** Monitors gateway health, LogGuard events, and infrastructure saturation.
* **L3 (Producers):** Investigates 500-level errors originating from backend services.

## Best Practices

{% hint style="info" %}
Ensure your backend services accept the `X-Gravitee-Request-Id`. Propagating this trace ID allows your support team to search a single ID across Gravitee, firewalls, and microservices.
{% endhint %}

### Define Log Retention Periods
Gravitee recommends a minimum of 30 days for log retention. Configure your external backend, such as Elasticsearch, to match your specific industry compliance requirements, such as GDPR, HIPAA, or PCI DSS.

### Monitor for Memory Pressure
If a gateway crashes due to memory pressure, check your LogGuard logs. Ensure the `gc-pressure` health probe is active. The default 15% threshold is usually sufficient, but you can adjust the `cooldown` duration based on your traffic patterns.
