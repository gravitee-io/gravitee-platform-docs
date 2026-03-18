# DB-less mode

DB-less mode deploys a lightweight Gateway designed for the ingress controller and Gateway API use case. With no database dependencies, the gateway starts faster, enabling better autoscaling in Kubernetes environments. Only an operator running in the same cluster or namespace is required. ManagementContext is irrelevant in this mode, as API definitions sync directly from Kubernetes CRDs.

{% hint style="warning" %}
DB-less mode cannot be used with SaaS gateways running in Gravitee Cloud.
{% endhint %}

## Limitations

DB-less mode disables the Management API, Management Console, and Developer Portal. The following features are not available:

| Feature                     | Impact                                                                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Applications                | No application creation, update, deletion, or metadata management.                                                                                            |
| Subscriptions and API keys  | No subscription lifecycle management or API key generation.                                                                                                   |
| Analytics and reporting     | No built-in analytics or request tracking. Elasticsearch is disabled. To collect analytics, configure a custom reporter such as Datadog or TCP with Logstash. |
| Shared policy groups        | No shared policy group creation or management.                                                                                                                |
| Notifications               | No notification creation or management.                                                                                                                       |
| Groups and members          | No group or member management. No API ownership assignment.                                                                                                   |
| Distributed rate limiting   | Set to `none` by default in the minimum configuration. To enable distributed rate limiting, configure a Redis-backed rate limit store.                        |
| Management context sync     | No synchronization with an external APIM instance. The `ManagementContext` resource serves no purpose.                                                        |
| Multi-gateway orchestration | No centralized management of multiple gateways. Each gateway independently syncs API definitions from Kubernetes.                                             |
| Health checks and logging   | No health check endpoints or centralized logging configuration.                                                                                               |
| Categories and metadata     | No API category or metadata management.                                                                                                                       |

## What is available in DB-less mode

The following features remain fully supported:

* API definition management (v2 and v4) through Kubernetes CRDs, including create, update, delete, start, and stop operations
* Ingress controller with support for multiple hosts, TLS, and path-based routing
* Policy enforcement at the gateway level
* Kubernetes secret integration
* ConfigMap and secret templating for API definitions
* Prometheus metrics scraping
* Gateway heartbeat monitoring

## When to use DB-less mode

DB-less was designed with the ingress controller in mind, where autoscaling capabilities are a must. Not having to connect to datasources on startup lowers the startup time and make the system respond better to Kubernetes autoscaling requests.

### When not to use DB-less mode

DB-less mode does not support multi-cluster or multi-region API exposure, or application and subscription management.

### Minimum configuration

Below is the minimum `value-dbless.yml` APIM configuration required by a DB-less deployment. Run the following command:

<pre class="language-bash"><code class="lang-bash"><strong>helm install gravitee-apim graviteeio/apim -f values-dbless.yml
</strong></code></pre>

{% code title="values-dbless.yaml" %}
```yaml
api:
  enabled: false

portal:
  enabled: false

ui:
  enabled: false

es:
  enabled: false

ratelimit:
  type: none

gateway:
  image:
    repository: graviteeio/apim-gateway
    tag: 4.1
    pullPolicy: Always
  services:
    sync:
      kubernetes:
        enabled: true
        dbLess: true
  reporters:
    elasticsearch:
      enabled: false
```
{% endcode %}

{% hint style="info" %}
The above is just one example of a DB-less mode configuration. Note that if DB-less mode is configured without a running APIM instance with which to sync, the `management-context` resource serves no purpose.
{% endhint %}
