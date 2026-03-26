---
description: This page provides the technical details of the RBAC policy
hidden: true
---

# Role-based Access Control (RBAC)

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../overview/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `role-based-access-control` policy (RBAC policy) to control access to a resource by specifying the required roles to access it. The roles are checked against request attribute `gravitee.attribute.user.roles`. The policy can be configured to either:

* Allow only incoming requests with roles exactly matching the configured roles (strict mode)
* Allow incoming requests with at least one role matching the configured roles

Functional and implementation information for the `role-based-access-control` policy is organized into the following sections:

* [Examples](role-based-access-control-rbac.md#examples)
* [Configuration](role-based-access-control-rbac.md#configuration)
* [Compatibility Matrix](role-based-access-control-rbac.md#compatibility-matrix)
* [Errors](role-based-access-control-rbac.md#errors)
* [Changelogs](role-based-access-control-rbac.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "rbac": {
    "roles": ["read", "write", "admin"],
    "strict": true
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `role-based-access-control` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="129" data-type="checkbox">Compatible?</th><th width="205.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `role-based-access-control` policy can be configured with the following options:

<table><thead><tr><th width="120">Property</th><th data-type="checkbox">Required</th><th width="253">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>roles</td><td>true</td><td>The list of required roles</td><td>Array of strings</td><td></td></tr><tr><td>strict</td><td>true</td><td>Validation mode — strict or not (must or should)</td><td>boolean</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `role-based-access-control` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

## Errors

<table><thead><tr><th width="205.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>400</code></td><td>* The roles associated with the request are not valid</td></tr><tr><td><code>403</code></td><td><p>* No roles are associated with the current request</p><p>* Role(s) associated with the request do not match required role(s)</p></td></tr></tbody></table>

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="347.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>RBAC_NO_USER_ROLE (403)</td><td>-</td></tr><tr><td>RBAC_INVALID_USER_ROLES (400)</td><td>-</td></tr><tr><td>RBAC_FORBIDDEN (403)</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-role-based-access-control/blob/master/CHANGELOG.md" %}
