# Kafka Virtual Cluster Gateway Configuration Reference

## Gateway Configuration

### Routing Mode

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.services.kafka.routing.mode` | Kafka routing mode. Determines how the gateway selects backend brokers. Valid values: `HOST` (route by hostname), `PORT` (route by port). | `HOST` |

### Endpoint Attributes

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.attributes.endpoint.nativekafkacluster` | Attribute prefix for native Kafka cluster endpoint configuration. | N/A |
| `gravitee.attributes.endpoint.nativekafkavirtualcluster` | Attribute prefix for native Kafka virtual cluster endpoint configuration. | N/A |
