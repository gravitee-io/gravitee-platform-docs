# Configuring the Hazelcast Rate-Limit Repository for Standalone Gateways

## Gateway Configuration

### Rate-Limit Repository Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `ratelimit.type` | Enables Hazelcast-backed rate-limit repository | `hazelcast` |
| `ratelimit.hazelcast.config-path` | Path to Hazelcast XML or YAML configuration file | `${gravitee.home}/config/hazelcast-ratelimit.xml` |
| `ratelimit.hazelcast.instance-name` | Name of the Hazelcast instance | `gio-apim-ratelimit-hz` |

### Hazelcast System Properties

The plugin auto-configures the following Hazelcast system properties:

| Property | Value | Description |
|:---------|:------|:------------|
| `hazelcast.logging.type` | `slf4j` | Integrates Hazelcast logs with SLF4J |
| `hazelcast.shutdownhook.enabled` | `false` | Disables JVM shutdown hook |
| `hazelcast.health.monitoring.level` | `OFF` | Disables health monitoring |
| `hazelcast.discovery.enabled` | `true` (Kubernetes only) | Enables Hazelcast discovery in Kubernetes |

## Configuring Hazelcast Discovery

For standalone deployments, disable auto-detection and multicast in the XML configuration, enable TCP-IP join, and list the IP addresses or hostnames of all gateway nodes under `<tcp-ip><interface>`. Each gateway must use the same `<cluster-name>` (default: `graviteeio-apim-ratelimit`) to form a single logical cluster.

For multi-host TCP-IP, replace `<interface>127.0.0.1</interface>` with explicit member entries:

```xml
<tcp-ip enabled="true">
    <member>gw-host-1:5901</member>
    <member>gw-host-2:5901</member>
</tcp-ip>
```

## Restrictions

- Only XML (`.xml`) and YAML (`.yaml`, `.yml`) Hazelcast configuration file formats are supported; other formats throw an error.
- The repository supports only `Scope.RATE_LIMIT`; attempting to use it for other scopes (e.g., `Scope.MANAGEMENT`) throws an error.
- When running multiple Hazelcast subsystems (cluster, cache, rate-limit) in the same JVM, each must use a distinct `<port>` range and `<cluster-name>` in its XML configuration to avoid collisions (defaults: cluster 5701, cache 5801, rate-limit 5901).
- The repository propagates Hazelcast failures to the calling rate-limit policy; the policy's own configuration determines whether to allow (fail-open) or reject (fail-closed) requests on error.
- Entries with `resetTime <= 0` are assigned a TTL of 1ms (immediate eviction) instead of infinite retention.
