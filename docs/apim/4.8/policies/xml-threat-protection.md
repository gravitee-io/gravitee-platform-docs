---
hidden: true
---

# XML Threat Protection

## Overview

You can use the `xml-threat-protection` policy to validate an XML request body by applying limits on XML structures such as elements, entities, attributes and string values. When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a 400 BAD REQUEST.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
        "name" : "XML Threat Protection",
        "enabled" : true,
        "policy" : "xml-threat-protection",
        "configuration" : {
          "maxDepth" : 90,
          "maxChildrenPerElement" : 90,
          "maxEntities" : 90,
          "maxAttributesPerElement" : 90,
          "allowExternalEntities" : false,
          "maxElements" : 900,
          "maxEntityDepth" : 90,
          "maxAttributeValueLength" : 90,
          "maxTextValueLength" : 90,
          "maxLength" : 900
        }
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `xml-threat-protection` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `xml-threat-protection` policy can be configured with the following options:

<table><thead><tr><th width="245">Property</th><th data-type="checkbox">Required</th><th width="275">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>maxElements</td><td>false</td><td>Maximum number of elements allowed in an XML document. Example: <code>&#x3C;root>&#x3C;a>1&#x3C;/a>2&#x3C;b>&#x3C;/b>&#x3C;/root></code> has 3 elements.</td><td>integer (-1 to specify no limit)</td><td>1000</td></tr><tr><td>maxDepth</td><td>false</td><td>Maximum depth of XML structure. Example: <code>&#x3C;root>&#x3C;a>&#x3C;b>1&#x3C;/b>&#x3C;/a>&#x3C;/root></code> has a depth of 2.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxLength</td><td>false</td><td>Maximum number of characters allowed for the whole XML document.</td><td>integer (-1 to specify no limit)</td><td>1000</td></tr><tr><td>maxAttributesPerElement</td><td>false</td><td>Maximum number of attributes allowed for single XML element.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxAttributeValueLength</td><td>false</td><td>Maximum length of individual attribute values.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxChildrenPerElement</td><td>false</td><td>Maximum number of child elements for a given element. Example: <code>&#x3C;code>&#x3C;root>&#x3C;a>&#x3C;b>1&#x3C;/b>&#x3C;c>2&#x3C;/c>&#x3C;/a>&#x3C;/root>&#x3C;/code></code> <code>a</code> element has 2 children.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxTextValueLength</td><td>false</td><td>Maximum length of individual text value.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxEntities</td><td>false</td><td>Maximum number of entity expansions allowed. XML entities are a type of macro and vulnerable to entity expansion attacks (for more information on XML entity expansion attacks, see <a href="https://en.wikipedia.org/wiki/Billion_laughs_attack">Billion laughs attack</a>).</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxEntityDepth</td><td>false</td><td>Maximum depth of nested entity expansions allowed.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>allowExternalEntities</td><td>false</td><td>Whether to allow inclusion of external entities. WARNING: Since XML can be vulnerable to <a href="https://en.wikipedia.org/wiki/XML_external_entity_attack">XXE injection</a>, only enable this feature if you can really trust your consumers.</td><td>boolean</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `xml-threat-protection` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="204.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>400 Bad Request</code></td><td><ul><li>Invalid xml structure</li><li>Maximum xml elements exceeded</li><li>Maximum xml depth exceeded</li><li>Maximum xml length exceeded</li><li>Maximum attributes per element exceeded</li><li>Maximum attribute value length exceeded</li><li>Maximum children per element exceeded</li><li>Maximum text value length exceeded</li><li>Maximum xml entities exceeded</li><li>Maximum xml entity depth exceeded</li><li>External entity is used when prohibited</li></ul></td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="421.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>XML_THREAT_DETECTED</td><td>-</td></tr><tr><td>XML_THREAT_MAX_DEPTH</td><td>-</td></tr><tr><td>XML_THREAT_MAX_LENGTH</td><td>-</td></tr><tr><td>XML_THREAT_MAX_ATTRIBUTES</td><td>-</td></tr><tr><td>XML_THREAT_MAX_ATTRIBUTE_VALUE_LENGTH</td><td>-</td></tr><tr><td>XML_MAX_CHILD_ELEMENTS</td><td>-</td></tr><tr><td>XML_THREAT_MAX_TEXT_VALUE_LENGTH</td><td>-</td></tr><tr><td>XML_THREAT_MAX_ENTITIES</td><td>-</td></tr><tr><td>XML_THREAT_MAX_ENTITY_DEPTH</td><td>-</td></tr><tr><td>XML_THREAT_EXTERNAL_ENTITY_FORBIDDEN</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-xml-threat-protection/blob/master/CHANGELOG.md" %}
