---
description: An overview about xslt.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/xslt
---

# XSLT

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../readme/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `xslt` policy to apply an XSL transformation to an incoming XML request body or to the response body if your backend is exposing XML content.

This policy is based on the [Saxon](https://sourceforge.net/projects/saxon/) library.

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Remove SOAP elements when calling a WS:

```xml
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"
    exclude-result-prefixes="fn xsl">

    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />

    <!-- template to copy elements -->
    <xsl:template match="*">
        <xsl:if test="normalize-space(string(.)) != ''">
            <xsl:element name="{local-name()}">
                <xsl:apply-templates select="@* | node()"/>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <!-- template to copy attributes -->
    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

    <!-- template to copy the rest of the nodes -->
    <xsl:template match="comment() | text() | processing-instruction()">
        <xsl:copy/>
    </xsl:template>

    <xsl:template match="soapenv:*">
        <xsl:apply-templates select="@* | node()" />
    </xsl:template>

    <xsl:template match="@xsi:nil[.='true']"/>
</xsl:stylesheet>
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
"xslt": {
    "scope": "RESPONSE",
    "stylesheet": "<xsl:stylesheet \n  version=\"2.0\"\n  xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\"\n  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"   xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:fn=\"http://www.w3.org/2005/xpath-functions\" exclude-result-prefixes=\"fn xsl\">\n  <xsl:output method=\"xml\" version=\"1.0\" encoding=\"UTF-8\" indent=\"yes\"/>\n\n  <!-- template to copy elements -->\n    <xsl:template match=\"*\">\n<xsl:if test=\"normalize-space(string(.)) != ''\">\n        <xsl:element name=\"{local-name()}\">\n            <xsl:apply-templates select=\"@* | node()\"/>\n        </xsl:element>\n</xsl:if>\n    </xsl:template>\n\n    <!-- template to copy attributes -->\n    <xsl:template match=\"@*\">\n        <xsl:attribute name=\"{local-name()}\">\n            <xsl:value-of select=\".\"/>\n        </xsl:attribute>\n    </xsl:template>\n\n    <!-- template to copy the rest of the nodes -->\n    <xsl:template match=\"comment() | text() | processing-instruction()\">\n        <xsl:copy/>\n    </xsl:template>\n\n  <xsl:template match=\"soapenv:*\">\n    <xsl:apply-templates select=\"@* | node()\" />\n  </xsl:template>\n\n  <xsl:template match=\"@xsi:nil[.='true']\"/>\n</xsl:stylesheet>",
    "parameters": [
        {
            "name": "my-parameter",
            "value": "my-value"
        }
    ]
}
```
{% endcode %}

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`):

```yaml
policy:
  xslt:
    secure-processing: false
```

### Phases

The phases checked below are supported by the `xslt` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="134" data-type="checkbox">Compatible?</th><th width="196.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `xslt` policy can be configured with the following options:

<table><thead><tr><th width="148">Property</th><th data-type="checkbox">Required</th><th width="205">Description</th><th width="135">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>RESPONSE</code></td></tr><tr><td>stylesheet</td><td>true</td><td>XSLT stylesheet to apply</td><td>string</td><td></td></tr><tr><td>parameters</td><td>false</td><td>Parameters to inject while running XSL transformation</td><td>Array of XSLT parameters</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `xslt` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x</td><td>3.x</td></tr><tr><td>3.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="188.5">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>Bad stylesheet file or XSLT transformation cannot be executed properly</td></tr></tbody></table>
