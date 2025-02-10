# DB-less mode

DB-less mode lets you deploy a Gateway with no dependencies, assuming only that there is an operator running in the same cluster or namespace. Although the setup does not include Elasticsearch or MongoDB, analytics can still be configured using a custom reporter such as Datadog, TCP with Logstash, etc.

Note that DB-less mode cannot be used with SaaS gateways running in Gravitee Cloud.&#x20;

Below is the minimum `value-dbless.yml` APIM configuration required by a DB-less deployment. Run the following command:

<pre><code><strong>helm install gravitee-apim graviteeio/apim -f values-dbless.yml
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
  replicaCount: 1
  autoscaling:
    enabled: false
  ingress:
    enabled: false
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
