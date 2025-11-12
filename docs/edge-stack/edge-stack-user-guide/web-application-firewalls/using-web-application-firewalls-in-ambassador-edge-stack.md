---
noIndex: true
---

# Using Web Application Firewalls in Ambassador Edge Stack

[Ambassador Edge Stack](https://www.getambassador.io/products/edge-stack/api-gateway) comes fully equipped with a Web Application Firewall solution (commonly referred to as WAF) that is easy to set up and can be configured to help protect your web applications by preventing and mitigating many common attacks. To accomplish this, the [Coraza Web Application Firewall library](https://coraza.io/docs/tutorials/introduction) is used to check incoming requests against a user-defined configuration file containing rules and settings for the firewall to determine whether to allow or deny incoming requests.

Ambassador Edge Stack also has additional authentication features such as filters (see [using-filters-and-filterpolicies.md](../../technical-reference/filters/using-filters-and-filterpolicies.md "mention")) and rate limiting (see [rate-limiting-reference.md](docs/edge-stack/edge-stack-user-guide/rate-limiting/rate-limiting-reference.md "mention")). When `Filters`, `Ratelimits`, and `WebApplicationFirewalls` are all used at the same time, the order of operations is as follows and is not currently configurable.

1. `WebApplicationFirewalls` are always executed first
2. `Filters` are executed next (so long as any configured `WebApplicationFirewalls` did not already reject the request)
3. Lastly `Ratelimits` are executed (so long as any configured `WebApplicationFirewalls` and Filters did not already reject the request)

### Quickstart <a href="#quickstart" id="quickstart"></a>

See [webapplicationfirewall.md](../../crd-api-references/gateway.getambassador.io-v1alpha1/webapplicationfirewall.md "mention") and [webapplicationfirewallpolicy.md](../../crd-api-references/gateway.getambassador.io-v1alpha1/webapplicationfirewallpolicy.md "mention") for an overview of all the supported fields of the following custom resources.

1.  First, start by creating your firewall configuration. The example will download the firewall rules in [configuring-web-application-firewall-rules-in-ambassador-edge-stack.md](configuring-web-application-firewall-rules-in-ambassador-edge-stack.md "mention"), but you are free to write your own or use the published rules as a reference.

    ```yaml
    kubectl apply -f -<<EOF
    ---
    apiVersion: gateway.getambassador.io/v1alpha1
    kind: WebApplicationFirewall
    metadata:
      name: "example-waf"
      namespace: "default"
    spec:
      firewallRules:
        - sourceType: "http"
          http:
            url: "https://app.getambassador.io/download/waf/v1-20230825/aes-waf.conf"
        - sourceType: "http"
          http:
            url: "https://app.getambassador.io/download/waf/v1-20230825/crs-setup.conf"
        - sourceType: "http"
          http:
            url: "https://app.getambassador.io/download/waf/v1-20230825/waf-rules.conf"
    EOF
    ```
2.  Next create a `WebApplicationFirewallPolicy` to control which requests the firewall should run on. The example will run the firewall on all requests, but you can customize the policy to only run for specific requests.

    ```yaml
    kubectl apply -f -<<EOF
    ---
    apiVersion: gateway.getambassador.io/v1alpha1
    kind: WebApplicationFirewallPolicy
    metadata:
      name: "example-waf-policy"
      namespace: "default"
    spec:
      rules:
      - wafRef: # This rule will be executed on all paths and hostnames
          name: "example-waf"
          namespace: "default"
    EOF
    ```
3.  Finally, send a request that will be blocked by the Web Application Firewall

    ```bash
    curl https://<HOSTNAME>/test -H 'User-Agent: Arachni/0.2.1'
    ```

Congratulations, you've successfully set up a Web Application Firewall to secure all requests coming into Ambassador Edge Stack.

{% hint style="info" %}
After applying your `WebApplicationFirewall` and `WebApplicationFirewall` resources, check their statuses to make sure that they were not rejected due to any configuration errors.
{% endhint %}

### Rules for Web Application Firewalls <a href="#rules-for-web-application-firewalls" id="rules-for-web-application-firewalls"></a>

Since the [Coraza Web Application Firewall library](https://coraza.io/docs/tutorials/introduction) Ambassador Edge Stack's Web Application Firewall implementation, the firewall rules configuration uses [Coraza's Seclang syntax](https://coraza.io/docs/seclang/directives) which is compatible with the OWASP Core Rule Set.

Ambassador Labs publishes and maintains a list of rules to be used with the Web Application Firewall that should be a good solution for most users and [Coraza also provides their own ruleset](https://coraza.io/docs/tutorials/coreruleset) based on the [OWASP](https://owasp.org/) core rule set. It also satisifies [PCI 6.6](https://listings.pcisecuritystandards.org/documents/information_supplement_6.6.pdf) compliance requirements.

Ambassador Labs rules differ from the OWASP Core ruleset in the following areas:

* WAF engine is enabled by default.
* A more comprehensive set of rules is enabled, including rules related to compliance with PCI DSS 6.5 and 12.1 requirements.

See [configuring-web-application-firewall-rules-in-ambassador-edge-stack.md](configuring-web-application-firewall-rules-in-ambassador-edge-stack.md "mention")for more information about installing Ambassador Labs rules.

For specific information about rule configuration, please refer to [Coraza's Seclang documentation](https://coraza.io/docs/seclang)

### Observability <a href="#observability" id="observability"></a>

To make using Ambassador Edge Stack's Web Application Firewall system easier and to enable automated workflows and alerts, there are three main methods of observability for Web Application Firewall behavior.

#### Logging <a href="#logging" id="logging"></a>

Ambassador Edge Stack will log information about requests approved and denied by any `WebApplicationFirewalls` along with the reason why the request was denied. You can configure the logging policies in the [coraza rules configuration](https://coraza.io/docs/seclang/directives/#secauditlog) where logs are sent to and how much information is logged. Ambassador Labs' default ruleset sends the WAF logs to stdout so they show up in the container logs.

#### Metrics <a href="#metrics" id="metrics"></a>

Ambassador Edge Stack also outputs metrics about the Web Application Firewall, including the number of requests approved and denied, and performance information.

| Metric                              | Type      | Description                                 |
| ----------------------------------- | --------- | ------------------------------------------- |
| `waf_configuration_errors`          | Counter   | Number of configuration errors              |
| `waf_created_wafs`                  | Gauge     | Number of running web application firewalls |
| `waf_managed_wafs_total`            | Counter   | Number of transactions processed            |
| `waf_added_latency_ms`              | Histogram | Added latency in milliseconds               |
| `waf_total_denied_requests_total`   | Counter   | Number of requests denied                   |
| `waf_total_denied_responses_total`  | Counter   | Number of responses denied                  |
| `waf_denied_breakdown_total`        | Counter   | Breakdown of requests/responses denied      |
| `waf_total_allowed_requests_total`  | Counter   | Number of requests allowed                  |
| `waf_total_allowed_responses_total` | Counter   | Number of responses allowed                 |
| `waf_allowed_breakdown_total`       | Counter   | Breakdown of requests/responses allowed     |

#### Grafana Dashboard <a href="#grafana-dashboard" id="grafana-dashboard"></a>

Ambassador Edge Stack provides a [Grafana dashboard](https://grafana.com/grafana/dashboards/4698-ambassador-edge-stack) that can be imported to [Grafana](https://grafana.com/). In addition, the dashboard has pre-built panels that help visualize the metrics that are collected about Web Application Firewall activity. For more information about getting [Prometheus](https://prometheus.io/docs/introduction/overview) and Grafana set up for gathering and visualizing metrics from Ambassador Edge Stack please refer to the [monitoring-with-prometheus-and-grafana.md](docs/edge-stack/edge-stack-user-guide/service-monitoring/monitoring-with-prometheus-and-grafana.md "mention") documentation.
