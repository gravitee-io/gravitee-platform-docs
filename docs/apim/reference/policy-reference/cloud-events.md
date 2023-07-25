---
description: This page provides the technical details of the Cloud Events policy
---

# Cloud Events

## Overview

Functional and implementation information for the Cloud Events policy is organized into the following sections:

* [Configuration](cloud-events.md#user-content-configuration)
* [Errors](cloud-events.md#user-content-errors)

You can use the `cloud-events` policy to create a cloud-events `JSON` object from messages. The `datacontenttype` will be set accordingly to the message `Content-type` if any.

This policy relies on the specification [https://cloudevents.io](https://cloudevents.io/) and use [https://github.com/cloudevents/sdk-java](https://github.com/cloudevents/sdk-java) library.

In APIM, you need to provide the cloud-events information in the policy configuration.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
    "cloud-events": {
        "type": "demo-events",
        "id": "{#message.metadata['key']}",
        "source": "kafka://{#message.metadata['topic']}/{#message.metadata['partition']}/{#message.metadata['offset']}"
    }
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>id</td><td>true</td><td><p>The id of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id</a></p><p>Can contain EL.</p></td><td>string</td><td></td></tr><tr><td>type</td><td>true</td><td><p>The type of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type</a></p><p>Can contain EL.</p></td><td>string</td><td></td></tr><tr><td>source</td><td>true</td><td><p>The source of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1</a></p><p>Can contain EL.</p></td><td>string</td><td></td></tr><tr><td>subject</td><td>false</td><td><p>The subject of the cloud-events object. See <a href="https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject%60">https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject`</a>.</p><p>Can contain EL.</p></td><td>string</td><td></td></tr></tbody></table>

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

<table><thead><tr><th width="183">Code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td>CLOUD_EVENTS_TRANSFORMATION_ERROR</td><td>Unable to create cloud-events object</td></tr></tbody></table>

##
