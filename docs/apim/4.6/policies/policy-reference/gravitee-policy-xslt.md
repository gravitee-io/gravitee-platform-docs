= XSLT transformer policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-xslt/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-xslt/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-xslt/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-xslt.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-xslt"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^| X

|===

== Description

You can use the `xslt` policy to apply an XSL transformation to an incoming XML request body
or to the response body if your backend is exposing XML content.

This policy is based on the https://sourceforge.net/projects/saxon/[Saxon^] library.

By default, a DOCTYPE declaration will cause an error. This is for security.
If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

== Compatibility with APIM

|===
| Plugin version | APIM version
| 2.x            | 3.x
| 3.x            | 4.0 to latest
|===

== Configuration

=== Policy
You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

.^|scope
^.^|X
|Execution scope (`request` or `response`)
^.^|string
^.^|`RESPONSE`

.^|stylesheet
^.^|X
|XSLT stylesheet to apply
^.^|string
^.^|

.^|parameters
|
|Parameters to inject while running XSL transformation
^.^|Array of XSLT parameters
^.^|-

|===

=== Configuration example

[source, json]
----
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
----


=== Gateway

By default, a DOCTYPE declaration will cause an error. This is for security.
If you want to allow it, you can set `policy.xslt.secure-processing` to `false` in the Gateway configuration file (`gravitee.yml`).

[source, yaml]
.Configuration
----
policy:
  xslt:
    secure-processing: false
----

== Example

=== XSL to remove SOAP elements when calling a WS

[source, xml]
----
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
----

== Error

=== HTTP status code

|===
|Code |Message

.^| ```500```
| Bad stylesheet file or XSLT transformation cannot be executed properly

|===
