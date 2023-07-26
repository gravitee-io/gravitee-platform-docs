---
description: This page provides the technical details of the SSL Enforcement policy
---

# SSL Enforcement

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](ssl-enforcement.md#configuration)
* [Compatibility](ssl-enforcement.md#compatibility-matrix)
* [Errors](ssl-enforcement.md#errors)
* [Changelogs](ssl-enforcement.md#changelogs)

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `ssl-enforcement` policy to filter incoming SSL requests. It allows you to restrict or allow access only to requests with client certificate authentication or only to a subset of valid clients.

This policy is mainly used in plan configuration to allow access to consumers for a given set of certificates.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"ssl-enforcement" : {
    "requiresSsl": true,
    "requiresClientAuthentication": true,
    "whitelistClientCertificates": [
        "CN=localhost,O=GraviteeSource,C=FR"
    ]
}
```
{% endcode %}

#### Ant style path pattern

URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>requiresSsl</td><td>false</td><td>Is SSL requires to access this resource?</td><td>boolean</td><td>true</td></tr><tr><td>requiresClientAuthentication</td><td>false</td><td>Is client authentication required to access this resource?</td><td>boolean</td><td>false</td></tr><tr><td>whitelistClientCertificates</td><td>false</td><td>List of allowed X.500 names (from client certificate)</td><td>array of strings</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the SSL Enforcement policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### HTTP status codes

| Code  | Message                                                          |
| ----- | ---------------------------------------------------------------- |
| `401` | Access to the resource is unauthorized according to policy rules |
| `403` | Access to the resource is forbidden according to policy rules    |

#### Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                                        | Parameters                                |
| ------------------------------------------ | ----------------------------------------- |
| SSL\_ENFORCEMENT\_SSL\_REQUIRED            | -                                         |
| SSL\_ENFORCEMENT\_AUTHENTICATION\_REQUIRED | -                                         |
| SSL\_ENFORCEMENT\_CLIENT\_FORBIDDEN        | name (X.500 name from client certificate) |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/blob/master/CHANGELOG.md" %}
