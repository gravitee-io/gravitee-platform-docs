# Regex Threat Protection

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../4.6/overview/gravitee-apim-enterprise-edition/)**.**
{% endhint %}

## Overview

You can use the `regex-threat-protection` policy to extract information from a request (headers, path, query parameters, body payload) and evaluate that content against pre-defined regular expressions. If any content matches the specified regular expression, the request is considered a threat and rejected with a 400 BAD REQUEST. The policy injects processing report messages into request metrics for analytics.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration for SQL Injection regex detection:

```json
{
        "name" : "Regex Threat Protection",
        "enabled" : true,
        "policy" : "regex-threat-protection",
        "configuration" : {
          "regex" : ".*[\\s]*((delete)|(exec)|(drop\\s*table)|(insert)|(shutdown)|(update)|(\\bor\\b)).*",
          "checkPath" : true,
          "checkBody" : true,
          "caseSensitive" : false,
          "checkHeaders" : true
        }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `regex-threat-protection` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="133" data-type="checkbox">Compatible?</th><th width="211.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `regex-threat-protection` policy can be configured with the following options:

<table><thead><tr><th width="174">Property</th><th data-type="checkbox">Required</th><th width="306">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>regex</td><td>true</td><td>Regex used to detect malicious injections. You can enable this regular expression on headers, path and body or add multiple Regex threat protection policies with different regex, depending on your needs.</td><td>string</td><td></td></tr><tr><td>caseSensitive</td><td>false</td><td>Perform case-sensitive matching. <strong>WARNING</strong>: Use with caution. Enabling case sensitive matching may miss some risky patterns such as <code>DrOp TaBlE</code>.</td><td>boolean</td><td>false</td></tr><tr><td>checkHeaders</td><td>false</td><td>Evaluate regex on request headers</td><td>boolean</td><td>true</td></tr><tr><td>checkPath</td><td>false</td><td>Evaluate regex on request path and query parameters</td><td>boolean</td><td>true</td></tr><tr><td>checkBody</td><td>false</td><td>Evaluate regex on request body content</td><td>boolean</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `regex-threat-protection` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="224.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>400</code></td><td><p>Applies to:</p><ul><li>Matching request headers</li><li>Matching request path or query parameters</li><li>Matching request body</li></ul></td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

| Key                      | Parameters |
| ------------------------ | ---------- |
| HEADER\_THREAT\_DETECTED | -          |
| PATH\_THREAT\_DETECTED   | -          |
| BODY\_THREAT\_DETECTED   | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-regex-threat-protection/blob/master/CHANGELOG.md" %}
