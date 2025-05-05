= XML validation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-xml-validation/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-xml-validation/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-xml-validation/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-xml-validation.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-xml-validation"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequestContent
^|onResponseContent

^.^| X
^.^|

|===

== Description

You can use the `xml-validation` policy to validate XML using an XSD schema. This policy uses `javax.xml`.
A 400 BAD REQUEST error is received with a custom error message body with a custom error message body when validation fails.
Injects processing report messages into request metrics for analytics.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===


== Configuration

|===
|Property |Required |Description |Type| Default

.^|errorMessage
^.^|
|Custom error message in XML format. Spel is allowed.
^.^|string
|validation/internal

.^|xsdSchema
^.^|X
|Xsd schema.
^.^|string
|

|===

== Error

=== HTTP status code

|===
|Code |Message

.^| ```400```
| Applies to:

* Invalid payload

* Invalid XSD schema

* Invalid error message XML format

|===
