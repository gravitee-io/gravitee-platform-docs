= JSON threat protection policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-json-threat-protection/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-json-threat-protection/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-json-threat-protection/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-json-threat-protection.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-json-threat-protection"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onRequestContent
^.^|
^.^| X

|===

== Description

You can use the `json-threat-protection` policy to validate a JSON request body by specifying limits for various JSON structures (such as arrays, field names and string values).
When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a `400 BAD REQUEST`.

== Configuration

|===
|Property |Required |Description |Type| Default

.^|maxEntries
^.^|
|Maximum number of entries allowed for a JSON object. Example: In ```{ "a":{ "b":1, "c":2, "d":3 }}```, ```a``` has 3 entries
^.^|integer (-1 to specify no limit)
|100

.^|maxArraySize
^.^|
|Maximum number of elements allowed in an array
^.^|integer (-1 to specify no limit)
|100

.^|maxDepth
^.^|
|Maximum depth of JSON structure. Example: ```{ "a":{ "b":{ "c":true }}}``` has a depth of 3.
^.^|integer (-1 to specify no limit)
|100

.^|maxNameLength
^.^|
|Maximum string length allowed for a JSON property name
^.^|integer (-1 to specify no limit)
|100

.^|maxValueLength
^.^|
|Maximum string length allowed for a JSON property value
^.^|integer (-1 to specify no limit)
|500

|===

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```400```

a| Received in the following cases:

* Invalid JSON structure
* Maximum depth exceeded
* Maximum JSON entries exceeded
* Maximum JSON array size exceeded
* Maximum JSON field name length exceeded
* Maximum JSON field value length exceeded

|===

You can override the default response provided by the policy with the response templates feature. These templates must be defined at API level (see the API Console *Response Templates* option in the API *Proxy* menu).

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|JSON_THREAT_DETECTED
^.^|-

.^|JSON_THREAT_MAX_DEPTH
^.^|-

.^|JSON_THREAT_MAX_ENTRIES
^.^|-

.^|JSON_THREAT_MAX_NAME_LENGTH
^.^|-

.^|JSON_THREAT_MAX_VALUE_LENGTH
^.^|-

.^|JSON_MAX_ARRAY_SIZE
^.^|-

|===
