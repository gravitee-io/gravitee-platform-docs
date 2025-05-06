= Data logging masking policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-data-logging-masking/"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-groovy/releases"]
endif::[]

[label label-enterprise]#Enterprise feature#

== Phase

[cols="2*", options="header"]
|===
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X

|===

== Description

*If you enable logging on APIs*, you can use the `data-logging-masking` policy to configure rules to conceal sensitive data.
You can use `json-path`, `xml-path` or a regular expression to identify the information to hide.

CAUTION: The policy must be the last to run.
Don't forget to add it in final position on both the request and the response.

Additional information:

 - If you use the `path` property in a rule without regex then all the data corresponding to this path will be hidden.
 - If you use a `MaskPattern` type property or a custom regular expression without a `path`, then the transformation will apply to all the raw data.
 - We provide some patterns that you can use and adapt as required:
    * `_CUSTOM_`: use to write your own regular expression
    * `_CREDIT_CARD_`: use to catch and hide credit card numbers (supports Visa, Mastercard and American Express)
    * `_EMAIL_`: use to pick up and hide email addresses (doesn't support Unicode)
    * `_IP_`: use to pick up and hide IP addresses (supports IPv4 and IPv6 format)
    * `_Uri_`: use to catch and hide sensitive addresses (supports HTTP, HTTPS, FTP, mailto and file)


== Compatibility with APIM

|===
|Plugin version | APIM version

|3.x and upper                  | 4.0.x to latest
|2.x and upper                  | 3.18.x to 3.20.x
|1.x and upper                  | Up to 3.17.x
|===

=== Policy identifier

You can enable or disable the policy with policy identifier `policy-data-logging-masking`.

== Configuration

|===
|Property |Required |Description |Type| Default

.^|scope
^.^|X
|Scope where the policy is executed
^.^|Policy scope
|REQUEST_CONTENT

.^|headerRules
^.^|
|List of mask rules to apply on client and proxy headers
^.^|List<MaskHeaderRule>
|

.^|bodyRules
^.^|
|List of mask rules to apply on client and proxy body
^.^|List<MaskBodyRule>
|
|===

=== Mask header rule

|===
|Property |Required |Description |Type| Default

.^|path
^.^|
|Header name to transform
^.^|String
|

.^|replacer
^.^|
|Replacement character
^.^|String
|*
|===

=== Mask body rule

|===
|Property |Required |Description |Type| Default

.^|path
^.^|
|Context-dependent. If "Content-type" is `application / json` you must use `json-path`, if it is "application / xml" you must use `xml-path`, otherwise not used.
^.^|String
|

.^|type
^.^|
|Value selector type
^.^|MaskPattern
|

.^|regex
^.^|
|Custom value selector (use regular expression)
^.^|String
|

.^|replacer
^.^|
|Replacement character
^.^|String
|*
|===
