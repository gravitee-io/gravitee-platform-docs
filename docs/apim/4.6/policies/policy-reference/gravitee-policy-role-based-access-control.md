= Role-based access control policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-role-based-access-control/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-role-based-access-control/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-role-based-access-control/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-role-based-access-control.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-role-based-access-control"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

== Description

You can use the `role-based-access-control` policy (RBAC policy) to control access to a resource by specifying the required roles to access it.

The policy can be configured to either:

* allow only incoming requests with roles exactly matching the configured roles (strict mode)

* allow incoming requests with at least one role matching the configured roles

The roles are checked against request attribute `gravitee.attribute.user.roles`.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|roles
^.^|X
|The list of required roles
^.^|Array of strings
|

.^|strict
^.^|X
|Validation mode -- strict or not (must or should)
^.^|boolean
^.^|true

|===


=== Configuration example

[source, json]
----
{
  "rbac": {
    "roles": ["read", "write", "admin"],
    "strict": true
  }
}
----

==== Gateway configuration (gravitee.yml)
[source, yaml]
----
  policy:
    rbac:
      attributes:
        roles: gateway.roles
----

The `policy.rbac.attributes.roles` allow to configure the context attribute from which the gateway would extract the user's roles.

== Errors

=== HTTP status codes

|===
|Code |Message

.^| ```400```
| Applies if:

* The roles associated with the request are not valid

.^| ```403```
| Applies if:

* No roles are associated with the current request

* Role(s) associated with the request do not match required role(s)

|===

=== Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|RBAC_NO_USER_ROLE (403)
^.^|-
.^|RBAC_INVALID_USER_ROLES (400)
^.^|-
.^|RBAC_FORBIDDEN (403)
^.^|-

|===
