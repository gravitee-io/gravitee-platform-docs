---
description: This page provides the technical details of the GeoIP Filtering policy
---

# GeoIP Filtering

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

{% hint style="warning" %}
To use this policy, you must first install the plugin [gravitee-service-geoip](https://download.gravitee.io/#plugins/services/). This plugin loads the `geoip` databases in memory, so you need to adjust the JVM Heap settings of your APIM Gateways accordingly.
{% endhint %}

You can use the `geoip-filtering` policy to control access to your API by filtering IP addresses. You can allow IPs by country or distance.

Whitelist mode excludes all IP addresses except the addresses included in the whitelist.

Functional and implementation information for the `geoip-filtering` policy is organized into the following sections:

* [Examples](geoip-filtering.md#examples)
* [Configuration](geoip-filtering.md#configuration)
* [Compatibility Matrix](geoip-filtering.md#compatibility-matrix)
* [Errors](geoip-filtering.md#errors)

## Examples

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
```
"geoip-filtering": {
  "failOnUnknown": true,
  "whitelistRules": [
    {
        "type": "COUNTRY",
        "country": "FR"
    },
   {
       "type": "DISTANCE",
       "distance": "50000"
   }
  ],
}
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Filters IP addresses",
  "policy": "geoip-filtering",
  "configuration": {
    "failOnUnknown": true,
    "whitelistRules": [
      {
          "type": "COUNTRY",
          "country": "FR"
      },
     {
         "type": "DISTANCE",
         "distance": "50000"
     }
    ],
  }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `geoip-filtering` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="200.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `geoip-filtering` policy can be configured with the following options:

<table data-full-width="false"><thead><tr><th width="170">Property</th><th width="105" data-type="checkbox">Required</th><th width="207">Description</th><th width="150">Type</th><th width="247">Default</th></tr></thead><tbody><tr><td>failOnUnknown</td><td>true</td><td>If set to <code>true</code>, each unknown IP is rejected</td><td>boolean</td><td><code>true</code></td></tr><tr><td>whitelistRules</td><td>false</td><td>A list of allowed rules</td><td>Whitelist Rule</td><td><code>empty</code></td></tr></tbody></table>

### Whitelist rule

The `geoip-filtering` policy has the following whitelist rules:

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="104" data-type="checkbox">Required</th><th width="207">Description</th><th width="111" data-type="select">Type</th><th width="247">Default</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a<br><strong>root</strong></td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td><strong>REQUEST</strong> RESPONSE</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `geoip-filtering` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.20.x</td></tr><tr><td>2.x+</td><td>4.0.x+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td><code>403</code></td><td>You’re not allowed to access this resource</td></tr></tbody></table>
