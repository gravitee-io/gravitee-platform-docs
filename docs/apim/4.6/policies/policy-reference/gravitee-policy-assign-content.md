= Assign content policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-assign-content/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-assign-content/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-assign-content/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-assign-content.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-assign-content"]
endif::[]

== Phase

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|-
|-
|X
|X

|===

== Description

You can use the `assign-content` policy to change or transform the content of the request/response body or message.

This policy is compatible with the https://freemarker.apache.org[Freemarker^] template engine, which allows you to apply
complex transformations, such as transforming from XML to JSON and vice versa.

By default, you can access multiple objects from the template context -- request and response bodies, dictionaries, context
attributes and more.

== Compatibility with APIM

|===
|Plugin version | APIM version

| Up to 1.6.x   | Up to 3.9.x
| 1.7.x         | 3.10.x to 3.20.x
| 2.x           | 4.0 to latest
|===

== Configuration

|===
|Property |Required |Description |Type |Default

.^|scope
^.^|X
|The execution scope of the policy.
^.^|scope
^.^|REQUEST

.^|body
^.^|X
|The data to push as request or response body content.
^.^|string
^.^|-

|===

[source, json]
.Sample
----
"policy-assign-content": {
    "scope":"REQUEST",
    "body":"Put your content here"
}
----

== Examples

=== Inject a dictionary value and the application into the request payload

[source, json]
----
{
  "example": "${context.dictionaries['my-dictionary']['my-value']}",
  "application": "${context.attributes['application']}"
}
----

TIP: You can find more information about default attributes in the Expression Language documentation in the *API Publisher Guide*.

=== Incoming request body content

[source, json]
----
{
  "symbol": "EUR"
}
----

=== Policy example to transform from JSON to XML

Input:

[source, xml]
----
<#assign body = request.content?eval >
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.webserviceX.NET/">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetQuote>
         ${body.symbol}
      </web:GetQuote>
   </soapenv:Body>
</soapenv:Envelope>
----

Expected output:

[source, xml]
----
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.webserviceX.NET/">
 <soapenv:Header/>
 <soapenv:Body>
 <web:GetQuote>
 EUR
 </web:GetQuote>
 </soapenv:Body>
</soapenv:Envelope>
----

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```500```
| The body content cannot be transformed.

|===
