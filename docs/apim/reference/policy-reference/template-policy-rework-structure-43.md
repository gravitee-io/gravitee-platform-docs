---
description: >-
  This page provides the technical details of the WS Security Authentication
  policy
---

# WS Security Authentication

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

You can use the `wssecurity-authentication` policy to manage the security of SOAP API calls. The policy compares the username and password sent in the soap header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline, or http resource for your API plan, which specifies where the APIM users are stored
* configure a WS-Security authentication policy for the API flows

{% hint style="info" %}
LDAP, inline and http resources are not part of the default APIM configuration, so you must download these resource plugins from [here](https://download.gravitee.io/#graviteeio-apim/plugins/resources/).
{% endhint %}

Functional and implementation information for the WS Security Authentication policy is organized into the following sections:

* [Examples](template-policy-rework-structure-43.md#examples)
* [Configuration](template-policy-rework-structure-43.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-43.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-43.md#errors)
* [Changelogs](template-policy-rework-structure-43.md#changelogs)

## Examples

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

In the example below, the policy will extract **foo** & **bar** from the payload.

{% code title="Default response" %}
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2003/06/secext">
            <wsse:UsernameToken>
                <wsse:Username>foo</wsse:Username>
                <wsse:Password>bar</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header>
    <soap:Body>
        ...
    </soap:Body>
</soap:Envelope>
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Manage the security of SOAP API calls",
  "policy": "policy-wssecurity-authentication",
  "configuration": {
   "authenticationProviders" : [ "authProvider" ]
  }
}
```
{% endcode %}

### Reference

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="104" data-type="checkbox">Required</th><th width="207">Description</th><th width="111" data-type="select">Type</th><th width="247">Options</th></tr></thead><tbody><tr><td>authenticationProviders</td><td>false</td><td>List the authentication providers</td><td></td><td>N/a</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the WS Security Authentication policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

There are no out-of-the-box errors returned by this policy.
