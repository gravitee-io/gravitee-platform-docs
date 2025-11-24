---
description: Configuration guide for ---.
hidden: true
---

# XSLT

## Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse |
| --------- | ---------- |
| X         | X          |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `xslt` policy to apply an XSL transformation to an incoming XML request body or to the response body if your backend is exposing XML content.

This policy is based on the [Saxon](https://sourceforge.net/projects/saxon/) library.

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 2.x            | 3.x           |
| 3.x            | 4.0 to latest |

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

### Policy <a href="#user-content-policy" id="user-content-policy"></a>

You can configure the policy with the following options:

| Property   | Required | Description                                           | Type                     | Default    |
| ---------- | -------- | ----------------------------------------------------- | ------------------------ | ---------- |
| scope      | X        | Execution scope (`request` or `response`)             | string                   | `RESPONSE` |
| stylesheet | X        | XSLT stylesheet to apply                              | string                   |            |
| parameters |          | Parameters to inject while running XSL transformation | Array of XSLT parameters | -          |

### Configuration example <a href="#user-content-configuration-example" id="user-content-configuration-example"></a>

```
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

### Gateway <a href="#user-content-gateway" id="user-content-gateway"></a>

By default, a DOCTYPE declaration will cause an error. This is for security. If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

Configuration

```
policy:
  xslt:
    secure-processing: false
```

### Example <a href="#user-content-example" id="user-content-example"></a>

#### XSL to remove SOAP elements when calling a WS <a href="#user-content-xsl-to-remove-soap-elements-when-calling-a-ws" id="user-content-xsl-to-remove-soap-elements-when-calling-a-ws"></a>

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

## Error <a href="#user-content-error" id="user-content-error"></a>

### HTTP status code <a href="#user-content-http-status-code" id="user-content-http-status-code"></a>

| Code  | Message                                                                |
| ----- | ---------------------------------------------------------------------- |
| `500` | Bad stylesheet file or XSLT transformation cannot be executed properly |
