# Kafka Virtual Cluster Gateway Configuration Reference

## Gateway Configuration

### Routing Mode

Configure the routing mode in `gravitee.yml` to determine how the gateway maps client connections to backend brokers:

```yaml
kafka:
  routingMode: host   # or "port"
```

| Property | Description | Default |
|:---------|:------------|:--------|
| `kafka.routingMode` | Determines how the gateway selects backend brokers. Values: `host` (route by hostname), `port` (route by port). Parsed case-insensitively. | `host` |

### Host Routing Mode Properties

When `kafka.routingMode` is set to `host`, configure the following companion properties to define how the gateway builds per-broker hostnames using your wildcard TLS certificate:

| Property | Description | Default |
|:---------|:------------|:--------|
| `kafka.routingHostMode.defaultDomain` | Wildcard suffix used for broker hostname resolution. | `kafka.local` |
| `kafka.routingHostMode.defaultPort` | Listener port for the Kafka gateway. | `9092` |
| `kafka.routingHostMode.brokerPrefix` | Prefix used to build per-broker hostnames. | `broker-` |
| `kafka.routingHostMode.domainSeparator` | Separator between the broker ID and the API host. | `-` |
| `kafka.routingHostMode.bootstrapDomainPattern` | Bootstrap hostname pattern for client connections. | |
| `kafka.routingHostMode.brokerDomainPattern` | Per-broker hostname pattern for partition leader routing. | |
