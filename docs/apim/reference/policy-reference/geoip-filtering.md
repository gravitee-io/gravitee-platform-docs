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

Functional and implementation information for the GeoIP Filtering policy is organized into the following sections:

* [Configuration](geoip-filtering.md#configuration)
* [Compatibility Matrix](geoip-filtering.md#compatibility-matrix)
* [Errors](geoip-filtering.md#errors)

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

### Reference

<table data-full-width="false"><thead><tr><th width="140">Property</th><th width="104" data-type="checkbox">Required</th><th width="207">Description</th><th width="111" data-type="select">Type</th><th width="247">Options</th></tr></thead><tbody><tr><td>name</td><td>false</td><td>Provide a descriptive name for your policy</td><td></td><td>N/a</td></tr><tr><td>description</td><td>false</td><td>Provide a description for your policy</td><td></td><td>N/a</td></tr><tr><td>rootElement</td><td>true</td><td>XML root element name that encloses content.</td><td></td><td>N/a<br><strong>root</strong></td></tr><tr><td>scope</td><td>true</td><td>The execution scope</td><td></td><td><strong>REQUEST</strong> RESPONSE</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the GeoIP-Filtering policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelogs/changelogs/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `geoip-filtering` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x and upper</td><td>4.0.x to latest</td></tr><tr><td>1.x</td><td>Up to 3.20.x</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>403</code></td><td>You’re not allowed to access this resource</td></tr></tbody></table>

