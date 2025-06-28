# CloudEvents

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
|           |            | X                | X                 |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `cloud-events` policy to create a cloud-events `JSON` object from messages. The `datacontenttype` will be set accordingly to the message `Content-type` if any.

This policy relies on the specification [https://cloudevents.io](https://cloudevents.io/) and use [https://github.com/cloudevents/sdk-java](https://github.com/cloudevents/sdk-java) library.

In APIM, you need to provide the cloud-events information in the policy configuration.

| Note | You can use APIM EL in the configuration. |
| ---- | ----------------------------------------- |

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property   | Required | Description                                                                                                                                                                                                                                                                                                                                                        | Type   | Default                            |
| ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ---------------------------------- |
| id         | -        | <p>The id of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id</a></p><p>If the property is not defined, the policy is looking at the <code>ce_id</code> from the message header (can contain EL).</p>                          | string | {#message.headers\['ce\_id']}      |
| type       | -        | <p>The type of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type</a></p><p>If the property is not defined, the policy is looking at the <code>ce_type</code> from the message header (can contain EL).</p>                  | string | {#message.headers\['ce\_type']}    |
| source     |          | <p>The source of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1</a></p><p>If the property is not defined, the policy is looking at the <code>ce_source</code> from the message header (can contain EL).</p>      | string | {#message.headers\['ce\_source']}  |
| subject    |          | <p>The subject of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject%60">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject`</a>.</p><p>If the property is not defined, the policy is looking at the <code>ce_subject</code> from the message header (can contain EL).</p> | string | {#message.headers\['ce\_subject']} |
| extensions |          | A key-value structure to manage custom extensions context attributes of the cloud-events object. See [https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#extension-context-attributes\`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#extension-context-attributes%60).                                                    | map    | N/A                                |

### Example configuration:

```
{
    "cloud-events": {
        "type": "demo-events",
        "id": "{#message.metadata['key']}",
        "source": "kafka://{#message.metadata['topic']}/{#message.metadata['partition']}/{#message.metadata['offset']}"
    }
}
```

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

| Phase | Code  | Error template key                   | Description                          |
| ----- | ----- | ------------------------------------ | ------------------------------------ |
| \*    | `500` | CLOUD\_EVENTS\_TRANSFORMATION\_ERROR | Unable to create cloud-events object |
