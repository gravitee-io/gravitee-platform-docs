---
description: This page provides the technical details of the IP Filtering policy
---

# IP filtering

## Overview

Functional and implementation information for the IP Filtering policy is organized into the following sections:

* [Examples](template-policy-rework-structure-17.md#examples)
* [Configuration](template-policy-rework-structure-17.md#configuration)
* [Errors](template-policy-rework-structure-17.md#errors)
* [Changelogs](template-policy-rework-structure-17.md#changelogs)

## Examples

You can use the `ip-filtering` policy to control access to your API by filtering IP addresses. You can allow or deny a specific IP address or range of IP addresses with [CIDR](https://tools.ietf.org/html/rfc1519).

Whitelist mode excludes all IP addresses except the addresses included in the whitelist. Blacklist mode allows all IP addresses except the addresses included in the blacklist.

The blacklist takes precedence, so if an IP address is included in both lists, the policy rejects the request.

You can specify a host to be resolved and checked against the remote IP.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

```
"ip-filtering": {
  "matchAllFromXForwardedFor": true,
  "whitelistIps": [
    "10.0.0.1",
    "10.0.0.2/10",
    "gravitee.io"
  ],
  "blacklistIps": [
    null
  ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"ip-filtering": {
  "matchAllFromXForwardedFor": true,
  "whitelistIps": [
    "10.0.0.1",
    "10.0.0.2/10",
    "gravitee.io"
  ],
  "blacklistIps": [
    null
  ]
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>matchAllFromXForwardedFor</td><td>false</td><td>If set to <code>true</code>, each IP from the <code>X-Forwarded-For</code> header parameter is parsed</td><td>boolean</td><td><code>false</code></td></tr><tr><td>whitelistIps</td><td>false</td><td>A list of allowed IPs with or without CIDR notation (host is allowed)</td><td>string list</td><td><code>empty</code></td></tr><tr><td>blacklistIps</td><td>false</td><td>A list of denied IPs with or without CIDR notation (host is allowed)</td><td>string list</td><td><code>empty</code></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the IP Filtering policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td>onRequest</td><td><code>403</code></td><td>Your IP (0.0.0.0) or one of the proxies your request passed through is not allowed to reach this resource</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ipfiltering/blob/master/CHANGELOG.md" %}
