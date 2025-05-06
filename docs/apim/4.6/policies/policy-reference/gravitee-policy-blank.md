= Blank Policy

ifdef::env-github[]
image:https://ci.gravitee.io/buildStatus/icon?job=gravitee-io/gravitee-policy-blank/master["Build status", link="https://ci.gravitee.io/job/gravitee-io/job/gravitee-policy-blank"]
image:https://badges.gitter.im/Join Chat.svg["Gitter", link="https://gitter.im/gravitee-io/gravitee-io?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"]
endif::[]

== Scope

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^| X

|===

== Description



== Configuration

You can configure the policy with the following options :

|===
|Property |Required |Description |Type| Default

.^|scope
^.^|X
|The execution scope (`request` or `response`).
^.^|string
^.^|`REQUEST`


|===


== Http Status Code

|===
|Code |Message

.^| ```500```
| Server error

|===