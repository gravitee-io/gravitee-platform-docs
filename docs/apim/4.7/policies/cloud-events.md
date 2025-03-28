---
description: This page provides the technical details of the Cloud Events policy
hidden: true
---

# Cloud Events

## Overview

You can use the `cloud-events` policy to create a cloud-events `JSON` object from messages. The `datacontenttype` will be set accordingly to the message `Content-type` if any.

This policy relies on the specification [https://cloudevents.io](https://cloudevents.io/) and uses [https://github.com/cloudevents/sdk-java](https://github.com/cloudevents/sdk-java) library.

In APIM, you need to provide the cloud-events information in the policy configuration.

Functional and implementation information for the `cloud-events` policy is organized into the following sections:

* [Examples](cloud-events.md#examples)
* [Configuration](cloud-events.md#user-content-configuration)
* [Errors](cloud-events.md#user-content-errors)

## Examples

{% hint style="warning" %}
This policy can be applied to v4 message APIs. It cannot be applied to v2 APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="Message API example" %}
Sample policy configuration:

```json
{
    "cloud-events": {
        "type": "demo-events",
        "id": "{#message.metadata['key']}",
        "source": "kafka://{#message.metadata['topic']}/{#message.metadata['partition']}/{#message.metadata['offset']}"
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

### Phases

The phases checked below are supported by the `cloud-events` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `cloud-events` policy with the following options:

<table><thead><tr><th width="115">Property</th><th width="112" data-type="checkbox">Required</th><th width="175">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>id</td><td>true</td><td>The id of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id">here</a>. Can contain EL.</td><td>string</td><td></td></tr><tr><td>type</td><td>true</td><td>The type of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type">here</a>. Can contain EL.</td><td>string</td><td></td></tr><tr><td>source</td><td>true</td><td>The source of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1">here</a>. Can contain EL.</td><td>string</td><td></td></tr><tr><td>subject</td><td>false</td><td>The subject of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject%60">here</a>. Can contain EL.</td><td>string</td><td></td></tr></tbody></table>

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

<table><thead><tr><th width="183">Code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>CLOUD_EVENTS_TRANSFORMATION_ERROR</td><td>Unable to create cloud-events object</td></tr></tbody></table>
