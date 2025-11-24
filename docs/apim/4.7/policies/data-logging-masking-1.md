---
description: An overview about ---.
hidden: true
---

# Data Logging Masking

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../overview/enterprise-edition.md)**.**
{% endhint %}

## Overview

If you enable logging on APIs, you can use the `data-logging-masking` policy to configure rules to conceal sensitive data. You can use `json-path`, `xml-path` or a regular expression to identify the information to hide.

{% hint style="info" %}
The `data-logging-masking` policy must be the last to run. Don’t forget to add it in final position on both the request and the response.
{% endhint %}

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs. It cannot be applied to v4 proxy APIs or v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="v2 API example" %}
Sample policy configuration:

```json
{
    "name": "Data Logging Masking",
    "description": "Data Logging Masking configured for RAW or JSON",
    "enabled": true,
    "policy": "policy-data-logging-masking",
    "configuration": {
        "scope": "REQUEST_CONTENT",
        "headerRules": [
            {
                "path": "reqHeaderToHide",
                "replacer": "*"
            }
        ],
        "bodyRules": [
            {
                "path": "$.field",
                "replacer": "-"
            },
            {
                "type": "EMAIL",
                "replacer": "@"
            },
            {
                "type": "URI",
                "replacer": "U"
            },
            {
                "type": "IP",
                "replacer": "IP"
            },
            {
                "type": "CREDIT_CARD",
                "replacer": "$"
            },
            {
                "regex": "(proto?:/.w*)(:\\d*)?\\/?(.*?)",
                "replacer": "S"
            }
        ]
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration

When configuring the `data-logging-masking` policy, note the following:

* If you use the `path` property in a rule without regex, all the data corresponding to this path will be hidden.
* If you use a `MaskPattern` type property or a custom regular expression without a `path`, the transformation will apply to all the raw data.
* We provide some patterns that you can use and adapt as required:
  * `CUSTOM`: Use to write your own regular expression
  * `CREDIT_CARD`: Use to catch and hide credit card numbers (supports Visa, Mastercard and American Express)
  * `EMAIL`: Use to pick up and hide email addresses (doesn’t support Unicode)
  * `IP`: Use to pick up and hide IP addresses (supports IPv4 and IPv6 format)
  * `Uri`: Use to catch and hide sensitive addresses (supports HTTP, HTTPS, FTP, mailto and file)

You can enable or disable the policy with policy identifier `policy-data-logging-masking`.

### Phases

The phases checked below are supported by the `data-logging-masking` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `data-logging-masking` policy with the following options:

<table><thead><tr><th width="153">Property</th><th data-type="checkbox">Required</th><th width="164">Description</th><th width="209">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Scope where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>headerRules</td><td>false</td><td>List of mask rules to apply on client and proxy headers</td><td>List&#x3C;MaskHeaderRule></td><td></td></tr><tr><td>bodyRules</td><td>false</td><td>List of mask rules to apply on client and proxy body</td><td>List&#x3C;MaskBodyRule></td><td></td></tr></tbody></table>

#### Mask header rule

<table><thead><tr><th width="129">Property</th><th data-type="checkbox">Required</th><th width="165">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>path</td><td>false</td><td>Header name to transform</td><td>String</td><td></td></tr><tr><td>replacer</td><td>false</td><td>Replacement character</td><td>String</td><td>*</td></tr></tbody></table>

#### Mask body rule

<table><thead><tr><th width="121">Property</th><th width="104" data-type="checkbox">Required</th><th width="261">Description</th><th width="129">Type</th><th>Default</th></tr></thead><tbody><tr><td>path</td><td>false</td><td>Context-dependent. If "Content-type" is <code>application / json</code> you must use <code>json-path</code>, if it is "application / xml" you must use <code>xml-path</code>, otherwise not used.</td><td>String</td><td></td></tr><tr><td>type</td><td>false</td><td>Value selector type</td><td>MaskPattern</td><td></td></tr><tr><td>regex</td><td>false</td><td>Custom value selector (use regular expression)</td><td>String</td><td></td></tr><tr><td>replacer</td><td>false</td><td>Replacement character</td><td>String</td><td>*</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `data-logging-masking` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>Up to 3.17.x</td></tr><tr><td>2.0 to 2.x</td><td>3.18.x to 3.20.x</td></tr><tr><td>3.0+</td><td>4.0+</td></tr></tbody></table>

xx
