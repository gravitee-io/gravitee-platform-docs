# Event-native API Management example use cases

This document assumes you are familiar with synchronous APIs, asynchronous APIs, and the OpenAPI specification.

This page describes some example use cases for event-native API management.

## Prerequisites

### Kafka

These examples all depend on Kafka. To set up a Kafka Docker container with the [AKHQ](https://github.com/tchiotludo/akhq) UI, follow these steps.

1. Download [https://raw.githubusercontent.com/tchiotludo/akhq/master/docker-compose.yml](../../v4-beta/docker-compose.yml).
2. Run it locally.

```bash
docker-compose pull
docker-compose up
```

You can now access the AKHQ UI at [http://localhost:8080](http://localhost:8080).

### Enabling event-native API management

To run these examples, you must enable the [new V4 BETA policy execution engine](v4-beta-new-policy-execution-engine-introduction.md) first by setting the `gravitee_api_jupiterMode_enabled` environment variable to `true` on the Management API and the API Gateway.

See [Environment variables](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html#environment\_variables) on the Management API and [Environment variables](https://docs.gravitee.io/apim/3.x/apim\_installguide\_gateway\_configuration.html#environment\_variables) on the API Gateway for more detail about setting environment variables.

### V4 BETA 3.20.x Postman Collection

These examples use the Gravitee V4 BETA 3.20.x Postman Collection, available from the [Gravitee Public Workspace](https://www.postman.com/gravitee-io/workspace/gravitee-public-workspace/overview) in Postman.

This collection uses the following four variables:

| Variable              | Description                            | Example                 |
| --------------------- | -------------------------------------- | ----------------------- |
| `management_host`     | The host for the Management API        | `http://localhost:8083` |
| `management_username` | The username for a management user     | `admin`                 |
| `management_password` | The password for `management_username` |                         |
| `gateway_host`        | The gateway host                       | `http://loalhost:8082`  |

## Data ingestion

Some data ingestion examples are illustrated in the following diagram.

![Event-native API Management - Data Ingestion](../../../../images/apim/3.x/event-native/event-native-api-management-data-ingestion.png)

For data ingestion, run the requests in the _01 - Data Ingestion_ folder of the Postman Collection.

You can also use `curl` to `POST` data to the endpoint, as shown in the example below.

```
curl -X POST -d "my_payload" http://localhost:8082/data/ingestion
```

## Event consumption

### Streaming: server-sent events (SSE)

For streaming with server-sent events (SSE), run the requests in the _02 - Event Consumption - SSE_ folder of the Postman Collection.

You can test it with `curl`.

```
curl -N -H "Accept:text/event-stream" http://localhost:8082/demo/sse
```

### Streaming: WebSocket

For streaming with WebSocket, run the requests in the _03 - Event Consumption - Websocket_ folder of the Postman Collection.

You can test it through a WebSocket connection in Postman, or you can use the `websocat` command-line tool as shown in the example below.

```
websocat ws://localhost:8082/demo/ws
```

### Webhooks

For webhooks, run the requests in the _04 - Event Consumption - Webhook_ folder of the Postman Collection.

This request group uses a webhook callback that is called by the API Gateway. The unique callback URL is generated via [https://webhook.site](https://webhook.site/).

To use these requests, go to [https://webhook.site](https://webhook.site/) to get your unique callback URL, and update the Postman Collection to use it. For example:

```
{
  "configuration": {
    "type": "webhook",
    "callbackUrl": "https://webhook.site/891490b9-1e37-4b5e-8f91-4d40b9187710"
  }
}
```

#### Webhooks with subscription filter

For webhooks with subscription filters, run the requests in the _05 - Event Consumption - Webhook - Message Filtering_ folder of the Postman Collection.

Use the following policy configuration.

```
{
  "name": "Message filtering",
  "description": "Apply filter to messages",
  "enabled": true,
  "policy": "message-filtering",
  "configuration": {
    "filter": "{#jsonPath(#message.content, '$.feature') == #subscription.metadata.feature}"
  }
}
```
