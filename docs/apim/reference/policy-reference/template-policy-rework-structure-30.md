---
description: This page provides the technical details of the RBAC policy
---

# Role-based Access Control (RBAC)

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the RBAC policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-30.md#configuration)
* [Compatibility](template-policy-rework-structure-30.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-30.md#errors)
* [Changelogs](template-policy-rework-structure-30.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `role-based-access-control` policy (RBAC policy) to control access to a resource by specifying the required roles to access it.

The policy can be configured to either:

* allow only incoming requests with roles exactly matching the configured roles (strict mode)
* allow incoming requests with at least one role matching the configured roles

The roles are checked against request attribute `gravitee.attribute.user.roles`.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
  "rbac": {
    "roles": ["read", "write", "admin"],
    "strict": true
  }
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>roles</td><td>true</td><td>The list of required roles</td><td>Array of strings</td><td></td></tr><tr><td>strict</td><td>true</td><td>Validation mode — strict or not (must or should)</td><td>boolean</td><td>true</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the RBAC policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### HTTP status codes

| Code  | Message                                                                                                                                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `400` | <p>Applies if:</p><p>* The roles associated with the request are not valid</p>                                                                        |
| `403` | <p>Applies if:</p><p>* No roles are associated with the current request</p><p>* Role(s) associated with the request do not match required role(s)</p> |

#### Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                              | Parameters |
| -------------------------------- | ---------- |
| RBAC\_NO\_USER\_ROLE (403)       | -          |
| RBAC\_INVALID\_USER\_ROLES (400) | -          |
| RBAC\_FORBIDDEN (403)            | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-role-based-access-control/blob/master/CHANGELOG.md" %}
