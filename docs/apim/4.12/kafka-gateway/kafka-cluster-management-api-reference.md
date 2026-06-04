# Kafka Cluster Management API Reference

## Management API

The `/clusters` REST endpoint creates both Kafka Clusters and Kafka Virtual Clusters. The entity type is determined by a discriminator in the request body (`type` field: `KAFKA_CLUSTER` or `KAFKA_VIRTUAL_CLUSTER`).

### Deployed Clusters Endpoint

`GET /environments/{envId}/clusters/deployed` returns a list of deployed clusters with the following response schema:

| Field | Type | Description |
|:------|:-----|:------------|
| `crossId` | string | External identifier for the cluster |
| `name` | string | Cluster name |
| `description` | string | Cluster description |
| `type` | string | Cluster type: `KAFKA_CLUSTER_STANDALONE`, `KAFKA_CLUSTER`, or `KAFKA_VIRTUAL_CLUSTER` |
| `deployedAt` | string | ISO-8601 timestamp of deployment |
| `version` | integer | Cluster version number |
| `connections` | array | List of connection objects, each containing `crossId` and `name` |

**Example Response:**


```json
{
  "crossId": "string",
  "name": "string",
  "description": "string",
  "type": "KAFKA_CLUSTER_STANDALONE | KAFKA_CLUSTER | KAFKA_VIRTUAL_CLUSTER",
  "deployedAt": "ISO-8601 timestamp",
  "version": "integer",
  "connections": [
    {
      "crossId": "string",
      "name": "string"
    }
  ]
}
```

**Error Responses:**

| Status Code | Description |
|:------------|:------------|
| 400 | Bad Request - Invalid environment ID or request parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Environment does not exist |
| 500 | Internal Server Error |

**Error Response Schema:**

```json
{
  "message": "string",
  "code": "string"
}
```
