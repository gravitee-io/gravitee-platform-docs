---
description: >-
  This page provides the technical details of the WS Security Authentication
  policy
---

# WS Security Authentication

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

You can use the `wssecurity-authentication` policy to manage the security of SOAP API calls. The policy compares the username and password sent in the soap header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* Configure an LDAP, inline, or http resource for your API plan, which specifies where the APIM users are stored
* Configure a WS-Security authentication policy for the API flows

{% hint style="info" %}
LDAP, inline and http resources are not part of the default APIM configuration, so you must download these resource plugins [here](https://download.gravitee.io/#graviteeio-apim/plugins/resources/).
{% endhint %}

Functional and implementation information for the `wssecurity-authentication` policy is organized into the following sections:

* [Examples](ws-security-authentication.md#examples)
* [Configuration](ws-security-authentication.md#configuration)
* [Compatibility Matrix](ws-security-authentication.md#compatibility-matrix)
* [Errors](ws-security-authentication.md#errors)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
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

Sample policy configuration:

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

### Phases

The phases checked below are supported by the `wssecurity-authentication` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="208.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `wssecurity-authentication` policy can be configured with the following options:

<table data-full-width="false"><thead><tr><th width="234">Property</th><th width="104" data-type="checkbox">Required</th><th width="313">Description</th><th width="111">Type<select><option value="5f4171f5365a4e328c37990512178470" label="list of strings" color="blue"></option></select></th><th width="247">Options</th></tr></thead><tbody><tr><td>authenticationProviders</td><td>false</td><td>List the authentication providers</td><td><span data-option="5f4171f5365a4e328c37990512178470">list of strings</span></td><td>N/a</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `wssecurity-authentication` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x</td><td>3.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Errors

There are no out-of-the-box errors returned by this policy.
