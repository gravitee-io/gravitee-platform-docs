# Deploying the Hazelcast Rate-Limit Repository with Helm and Kubernetes Discovery

## Helm Chart Overrides

| Property | Description | Example |
|:---------|:------------|:--------|
| `gateway.ratelimit.hazelcast.configPath` | Overrides the Hazelcast config file path in Helm deployments | `${gravitee.home}/config/hazelcast-ratelimit.xml` |
| `gateway.ratelimit.hazelcast.port` | Hazelcast member port and Kubernetes discovery service port | `5901` |

## Hazelcast System Properties

The plugin auto-configures the following Hazelcast system properties:

| Property | Value | Description |
|:---------|:------|:------------|
| `hazelcast.logging.type` | `slf4j` | Integrates Hazelcast logs with SLF4J |
| `hazelcast.shutdownhook.enabled` | `false` | Disables JVM shutdown hook |
| `hazelcast.health.monitoring.level` | `OFF` | Disables health monitoring |
| `hazelcast.discovery.enabled` | `true` (Kubernetes only) | Enables Hazelcast discovery in Kubernetes |

## Creating a Hazelcast Rate-Limit Repository

### Helm Deployments

Set `ratelimit.type: hazelcast` in `values.yaml` and ensure `apim.managedServiceAccount: true` (default). The chart automatically:

* Renders `hazelcast-ratelimit.xml` with Kubernetes discovery pointing to the `{{ .Release.Name }}-gateway-hz` service
* Creates a ClusterIP service (`{{ .Release.Name }}-gateway-hz`) exposing port 5901
* Creates a namespace-scoped Role and RoleBinding granting `get`/`list` permissions on endpoints, pods, nodes, and services
* Mounts the configuration at `/opt/graviteeio-gateway/config/hazelcast-ratelimit.xml`

The gateway loads the configuration on startup and joins the Hazelcast cluster.

## Configuring Hazelcast Discovery

### Kubernetes Discovery

In Kubernetes, the Helm chart auto-generates a Hazelcast XML configuration with the `<kubernetes>` join strategy enabled:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
           http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">
    <cluster-name>graviteeio-apim-ratelimit</cluster-name>
    <properties>
        <property name="hazelcast.discovery.enabled">true</property>
        <property name="hazelcast.logging.type">slf4j</property>
    </properties>
    <network>
        <port auto-increment="true" port-count="100">5901</port>
        <join>
            <multicast enabled="false"/>
            <tcp-ip enabled="false"/>
            <kubernetes enabled="true">
                <namespace>YOUR_NAMESPACE</namespace>
                <service-name>YOUR_GATEWAY_HZ_SERVICE</service-name>
                <service-port>5901</service-port>
            </kubernetes>
        </join>
    </network>
</hazelcast>
```

The configuration specifies:

* **Namespace**: The release namespace
* **Service name**: `{{ template "gravitee.gateway.fullname" . }}-hz`
* **Service port**: Default 5901 (configurable via `gateway.ratelimit.hazelcast.port`)

Each gateway pod joins the cluster by querying the service for peer addresses.

### Manual Kubernetes Deployment

For Kubernetes deployments without Helm, reproduce the XML configuration by hand and ensure the gateway ServiceAccount has `get`/`list` permissions on endpoints, pods, and services in the namespace.

### RBAC Requirements

Kubernetes discovery requires a ServiceAccount with `get`/`list` permissions on endpoints, pods, nodes, and services in the release namespace. The Helm chart provisions this via a Role and RoleBinding when `apim.managedServiceAccount: true` (default).

{% hint style="warning" %}
When `apim.managedServiceAccount: false`, the chart prints a NOTES.txt warning. Each gateway pod falls back to a single-member cluster, causing rate-limit budgets to be multiplied by the replica count (each pod enforces the limit independently).
{% endhint %}


