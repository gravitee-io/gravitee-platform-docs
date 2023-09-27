---
description: This page provides the technical details of the IP Filtering policy
---

# IP filtering

## Overview

You can use the `ip-filtering` policy to control access to your API by filtering IP addresses. You can allow or deny a specific IP address or range of IP addresses with [CIDR](https://tools.ietf.org/html/rfc1519).

Whitelist mode excludes all IP addresses except the addresses included in the whitelist. Blacklist mode allows all IP addresses except the addresses included in the blacklist.

The blacklist takes precedence, so if an IP address is included in both lists, the policy rejects the request.

You can specify a host to be resolved and checked against the remote IP.

Functional and implementation information for the `ip-filtering` policy is organized into the following sections:

* [Examples](ip-filtering.md#examples)
* [Configuration](ip-filtering.md#configuration)
* [Compatibility Matrix](ip-filtering.md#compatibility-matrix)
* [Errors](ip-filtering.md#errors)
* [Changelogs](ip-filtering.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
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
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `ip-filtering` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `ip-filtering`  policy can be configured with the following options:

<table><thead><tr><th width="275">Property</th><th width="125" data-type="checkbox">Required</th><th width="254">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>matchAllFromXForwardedFor</td><td>false</td><td>If set to <code>true</code>, each IP from the <code>X-Forwarded-For</code> header parameter is parsed</td><td>boolean</td><td><code>false</code></td></tr><tr><td>whitelistIps</td><td>false</td><td>A list of allowed IPs with or without CIDR notation (host is allowed)</td><td>string list</td><td><code>empty</code></td></tr><tr><td>blacklistIps</td><td>false</td><td>A list of denied IPs with or without CIDR notation (host is allowed)</td><td>string list</td><td><code>empty</code></td></tr></tbody></table>

## Compatibility matrix

&#x20;The following is the compatibility matrix for APIM and the `ip-filtering` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>403</code></td><td>Your IP (0.0.0.0) or one of the proxies your request passed through is not allowed to reach this resource</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ipfiltering/blob/master/CHANGELOG.md" %}
