=  CloudEvents Policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-json-to-json/"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-cloud-events/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-cloud-events.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-cloud-events"]
endif::[]

== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onMessageRequest
^|onMessageResponse

^.^|
^.^|
^.^| X
^.^| X
|===

== Description

You can use the `cloud-events` policy to create a cloud-events `JSON` object from  messages. The `datacontenttype` will be set accordingly to the message `Content-type` if any.

This policy relies on the specification https://cloudevents.io and use https://github.com/cloudevents/sdk-java library.

In APIM, you need to provide the cloud-events information in the policy configuration.

NOTE: You can use APIM EL in the configuration.

== Configuration

You can configure the policy with the following options:

[cols="5*", options=header]
|===
^| Property
^| Required
^| Description
^| Type
^| Default

.^|id
^.^|-
.^|The id of the cloud-events object. See https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id

If the property is not defined, the policy is looking at the `ce_id` from the message header (can contain EL).
^.^|string
|{#message.headers['ce_id']}

.^|type
^.^|-
.^|The type of the cloud-events object. See https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type

If the property is not defined, the policy is looking at the `ce_type` from the message header (can contain EL).
^.^|string
|{#message.headers['ce_type']}

.^|source
^.^|
.^|The source of the cloud-events object. See https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1

If the property is not defined, the policy is looking at the `ce_source` from the message header (can contain EL).
^.^|string
|{#message.headers['ce_source']}

.^|subject
^.^|
.^|The subject of the cloud-events object. See https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject`.

If the property is not defined, the policy is looking at the `ce_subject` from the message header (can contain EL).
^.^|string
|{#message.headers['ce_subject']}

.^|extensions
^.^|
.^|A key-value structure to manage custom extensions context attributes of the cloud-events object. See https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#extension-context-attributes`.

^.^|map
|N/A

|===

Example configuration:

[source, json]
----
{
    "cloud-events": {
        "type": "demo-events",
        "id": "{#message.metadata['key']}",
        "source": "kafka://{#message.metadata['topic']}/{#message.metadata['partition']}/{#message.metadata['offset']}"
    }
}
----

== Errors

|===
|Phase | Code | Error template key | Description

.^| *
.^| ```500```
.^| CLOUD_EVENTS_TRANSFORMATION_ERROR
.^| Unable to create cloud-events object

|===
