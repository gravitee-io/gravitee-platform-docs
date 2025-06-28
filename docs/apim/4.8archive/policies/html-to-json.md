---
hidden: true
---

# HTML to JSON

## Overview

You use the `html-json` transformation policy to transform the response content.

This policy is based on the [jsoup](https://jsoup.org/) HTML parser. In APIM, all you need to do is provide your JSON field names with the associated selectors.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"html-json": {
    "selectors":
        [
            {
                "array": false,
                "jsonName": "test",
                "selector": ".class h1"
            },
            {
                "array": true,
                "jsonName": "testArray",
                "selector": ".container ul"
            }
        ]
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `html-json` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `html-json` policy can be configured with the following options:

<table><thead><tr><th width="136">Property</th><th width="105" data-type="checkbox">Required</th><th width="349">Description</th><th>Type</th></tr></thead><tbody><tr><td><code>jsonName</code></td><td>true</td><td>Name of the JSON field to contain the result of the selection</td><td>String</td></tr><tr><td><code>selector</code></td><td>true</td><td>HTML/CSS selector used to select an element and retrieve the text</td><td>String</td></tr><tr><td><code>array</code></td><td>false</td><td>Used to determine whether the selection needs to be returned as an array</td><td>Boolean</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `html-json` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All supported versions</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-html-json/blob/master/CHANGELOG.md" %}
