= XML threat protection policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-xml-threat-protection/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-xml-threat-protection/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-xml-threat-protection/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-xml-threat-protection.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-xml-threat-protection"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onRequestContent
^.^|
^.^| X

|===

== Description

You can use the `xml-threat-protection` policy to validate an XML request body by applying limits on XML structures such as elements, entities, attributes and string values.
When an invalid request is detected (meaning the limit is reached), the request will be considered a threat and rejected with a 400 BAD REQUEST.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

|===
|Property |Required |Description |Type| Default

.^|maxElements
^.^|
|Maximum number of elements allowed in an XML document. Example: ```<root><a>1</a>2<b></b></root>``` has 3 elements.
^.^|integer (-1 to specify no limit)
^.^|1000

.^|maxDepth
^.^|
|Maximum depth of XML structure. Example: ```<root><a><b>1</b></a></root>``` has a depth of 2.
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxLength
^.^|
|Maximum number of characters allowed for the whole XML document.
^.^|integer (-1 to specify no limit)
^.^|1000

.^|maxAttributesPerElement
^.^|
|Maximum number of attributes allowed for single XML element.
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxAttributeValueLength
^.^|
|Maximum length of individual attribute values.
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxChildrenPerElement
^.^|
|Maximum number of child elements for a given element. Example: ```<code><root><a><b>1</b><c>2</c></a></root></code>``` `a` element has 2 children.
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxTextValueLength
^.^|
|Maximum length of individual text value.
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxEntities
^.^|
|Maximum number of entity expansions allowed. XML entities are a type of macro and vulnerable to entity expansion attacks (for more information on XML entity expansion attacks, see https://en.wikipedia.org/wiki/Billion_laughs_attack[Billion laughs attack^]).
^.^|integer (-1 to specify no limit)
^.^|100

.^|maxEntityDepth
^.^|
|Maximum depth of nested entity expansions allowed.
^.^|integer (-1 to specify no limit)
^.^|100

.^|allowExternalEntities
^.^|
|Whether to allow inclusion of external entities. WARNING: Since XML can be vulnerable to https://en.wikipedia.org/wiki/XML_external_entity_attack[XXE injection^], only enable this feature if you can really trust your consumers.
^.^|boolean
^.^|false

|===

== Errors

=== HTTP status code

|===
|Code |Message

.^| ```400 Bad Request```
a| Applies to:

* Invalid xml structure
* Maximum xml elements exceeded
* Maximum xml depth exceeded
* Maximum xml length exceeded
* Maximum attributes per element exceeded
* Maximum attribute value length exceeded
* Maximum children per element exceeded
* Maximum text value length exceeded
* Maximum xml entities exceeded
* Maximum xml entity depth exceeded
* External entity is used when prohibited

|===

=== Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console *Response Templates*
option in the API *Proxy* menu).

=== Error keys

The error keys sent by this policy are as follows:

[cols="2*", options="header"]
|===
^|Key
^|Parameters

.^|XML_THREAT_DETECTED
^.^|-

.^|XML_THREAT_MAX_DEPTH
^.^|-

.^|XML_THREAT_MAX_LENGTH
^.^|-

.^|XML_THREAT_MAX_ATTRIBUTES
^.^|-

.^|XML_THREAT_MAX_ATTRIBUTE_VALUE_LENGTH
^.^|-

.^|XML_MAX_CHILD_ELEMENTS
^.^|-

.^|XML_THREAT_MAX_TEXT_VALUE_LENGTH
^.^|-

.^|XML_THREAT_MAX_ENTITIES
^.^|-

.^|XML_THREAT_MAX_ENTITY_DEPTH
^.^|-

.^|XML_THREAT_EXTERNAL_ENTITY_FORBIDDEN
^.^|-

|===
