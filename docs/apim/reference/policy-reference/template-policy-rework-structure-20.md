---
description: This page provides the technical details of the JSON-to-XML policy
---

# XML Threat Protection

## Overview

Functional and implementation information for the JSON-to-XML policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-20.md#configuration)
* [Compatibility](template-policy-rework-structure-20.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-20.md#errors)
* [Changelogs](template-policy-rework-structure-20.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `xml-threat-protection` policy to validate an XML request body by applying limits on XML structures such as elements, entities, attributes and string values. When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a 400 BAD REQUEST.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>maxElements</td><td>false</td><td>Maximum number of elements allowed in an XML document. Example: <code>&#x3C;root>&#x3C;a>1&#x3C;/a>2&#x3C;b>&#x3C;/b>&#x3C;/root></code> has 3 elements.</td><td>integer (-1 to specify no limit)</td><td>1000</td></tr><tr><td>maxDepth</td><td>false</td><td>Maximum depth of XML structure. Example: <code>&#x3C;root>&#x3C;a>&#x3C;b>1&#x3C;/b>&#x3C;/a>&#x3C;/root></code> has a depth of 2.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxLength</td><td>false</td><td>Maximum number of characters allowed for the whole XML document.</td><td>integer (-1 to specify no limit)</td><td>1000</td></tr><tr><td>maxAttributesPerElement</td><td>false</td><td>Maximum number of attributes allowed for single XML element.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxAttributeValueLength</td><td>false</td><td>Maximum length of individual attribute values.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxChildrenPerElement</td><td>false</td><td>Maximum number of child elements for a given element. Example: <code>&#x3C;code>&#x3C;root>&#x3C;a>&#x3C;b>1&#x3C;/b>&#x3C;c>2&#x3C;/c>&#x3C;/a>&#x3C;/root>&#x3C;/code></code> <code>a</code> element has 2 children.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxTextValueLength</td><td>false</td><td>Maximum length of individual text value.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxEntities</td><td>false</td><td>Maximum number of entity expansions allowed. XML entities are a type of macro and vulnerable to entity expansion attacks (for more information on XML entity expansion attacks, see <a href="https://en.wikipedia.org/wiki/Billion_laughs_attack">Billion laughs attack</a>).</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>maxEntityDepth</td><td>false</td><td>Maximum depth of nested entity expansions allowed.</td><td>integer (-1 to specify no limit)</td><td>100</td></tr><tr><td>allowExternalEntities</td><td>false</td><td>Whether to allow inclusion of external entities. WARNING: Since XML can be vulnerable to <a href="https://en.wikipedia.org/wiki/XML_external_entity_attack">XXE injection</a>, only enable this feature if you can really trust your consumers.</td><td>boolean</td><td>false</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### HTTP status code

| Code              | Message                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `400 Bad Request` | <p>Applies to:</p><ul><li>Invalid xml structure</li><li>Maximum xml elements exceeded</li><li>Maximum xml depth exceeded</li><li>Maximum xml length exceeded</li><li>Maximum attributes per element exceeded</li><li>Maximum attribute value length exceeded</li><li>Maximum children per element exceeded</li><li>Maximum text value length exceeded</li><li>Maximum xml entities exceeded</li><li>Maximum xml entity depth exceeded</li><li>External entity is used when prohibited</li></ul> |

#### Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                                        | Parameters |
| ------------------------------------------ | ---------- |
| XML\_THREAT\_DETECTED                      | -          |
| XML\_THREAT\_MAX\_DEPTH                    | -          |
| XML\_THREAT\_MAX\_LENGTH                   | -          |
| XML\_THREAT\_MAX\_ATTRIBUTES               | -          |
| XML\_THREAT\_MAX\_ATTRIBUTE\_VALUE\_LENGTH | -          |
| XML\_MAX\_CHILD\_ELEMENTS                  | -          |
| XML\_THREAT\_MAX\_TEXT\_VALUE\_LENGTH      | -          |
| XML\_THREAT\_MAX\_ENTITIES                 | -          |
| XML\_THREAT\_MAX\_ENTITY\_DEPTH            | -          |
| XML\_THREAT\_EXTERNAL\_ENTITY\_FORBIDDEN   | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-xml-threat-protection/blob/master/CHANGELOG.md" %}
