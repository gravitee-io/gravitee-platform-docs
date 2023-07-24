---
description: This page provides the technical details of the XSLT policy
---

# XSLT

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)**.**
{% endhint %}

## Overview

Functional and implementation information for the XSLT policy is organized into the following sections:

* [Examples](xslt.md#examples)
* [Configuration](xslt.md#configuration)
* [Compatibility Matrix](xslt.md#compatibility)
* [Errors](xslt.md#errors)
* [Changelogs](xslt.md#changelogs)

## Examples

You can use the `xslt` policy to apply an XSL transformation to an incoming XML request body or to the response body if your backend is exposing XML content.

This policy is based on the [Saxon](https://sourceforge.net/projects/saxon/) library.

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

#### Remove SOAP elements when calling a WS

```
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

\

{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

#### Gateway

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

Configuration

```
policy:
  xslt:
    secure-processing: false
```

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Execution scope (<code>request</code> or <code>response</code>)</td><td>string</td><td><code>RESPONSE</code></td></tr><tr><td>stylesheet</td><td>true</td><td>XSLT stylesheet to apply</td><td>string</td><td></td></tr><tr><td>parameters</td><td>false</td><td>Parameters to inject while running XSL transformation</td><td>Array of XSLT parameters</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the XSLT policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td><code>500</code></td><td>Bad stylesheet file or XSLT transformation cannot be executed properly</td></tr></tbody></table>
