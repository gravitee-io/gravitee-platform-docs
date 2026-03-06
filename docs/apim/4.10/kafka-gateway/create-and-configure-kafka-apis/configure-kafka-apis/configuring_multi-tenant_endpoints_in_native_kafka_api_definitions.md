### Creating a Multi-Tenant Native Kafka API

Define endpoint groups with tenant-specific endpoints in your API definition:

1. Create an endpoint group of type `native-kafka`.
2. Add multiple endpoints to the group, each with a `tenants` array containing one or more tenant IDs.
3. Configure each endpoint's `bootstrapServers` and other Native Kafka settings.
4. Deploy the API.

Gateways automatically select the first endpoint matching their configured tenant. If a gateway has no tenant configured, it matches the first endpoint in the group regardless of tenant assignments.

```json
{
  "endpointGroups": [
    {
      "name": "multi-tenant-kafka-group",
      "type": "native-kafka",
      "endpoints": [
        {
          "name": "internal-endpoint",
          "type": "native-kafka",
          "tenants": ["internal"],
          "configuration": {
            "bootstrapServers": "internal-kafka.example.com:9092"
          }
        },
        {
          "name": "external-endpoint",
          "type": "native-kafka",
          "tenants": ["external"],
          "configuration": {
            "bootstrapServers": "external-kafka.example.com:9092"
          }
        }
      ]
    }
  ]
}
```

