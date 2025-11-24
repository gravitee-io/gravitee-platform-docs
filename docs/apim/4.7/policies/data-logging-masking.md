---
description: An overview about ---.
hidden: true
---

# Data Logging Masking

## Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequestContent | onResponseContent |
| ---------------- | ----------------- |
| X                | X                 |

## Overview <a href="#user-content-description" id="user-content-description"></a>

**If you enable logging on APIs**, you can use the `data-logging-masking` policy to configure rules to conceal sensitive data. You can use `json-path`, `xml-path` or a regular expression to identify the information to hide.

| Caution | The policy must be the last to run. Don’t forget to add it in final position on both the request and the response. |
| ------- | ------------------------------------------------------------------------------------------------------------------ |

Additional information:

* If you use the `path` property in a rule without regex then all the data corresponding to this path will be hidden.
* If you use a `MaskPattern` type property or a custom regular expression without a `path`, then the transformation will apply to all the raw data.
* We provide some patterns that you can use and adapt as required:
  * _`CUSTOM`_: use to write your own regular expression
  * _`CREDIT_CARD`_: use to catch and hide credit card numbers (supports Visa, Mastercard and American Express)
  * _`EMAIL`_: use to pick up and hide email addresses (doesn’t support Unicode)
  * _`IP`_: use to pick up and hide IP addresses (supports IPv4 and IPv6 format)
  * _`Uri`_: use to catch and hide sensitive addresses (supports HTTP, HTTPS, FTP, mailto and file)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 TCP proxy APIs or v4 message APIs.
{% endhint %}

## Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version     |
| -------------- | ---------------- |
| 3.x and upper  | 4.0.x to latest  |
| 2.x and upper  | 3.18.x to 3.20.x |
| 1.x and upper  | Up to 3.17.x     |

### Policy identifier <a href="#user-content-policy-identifier" id="user-content-policy-identifier"></a>

You can enable or disable the policy with policy identifier `policy-data-logging-masking`.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

| Property    | Required | Description                                             | Type                  | Default          |
| ----------- | -------- | ------------------------------------------------------- | --------------------- | ---------------- |
| scope       | X        | Scope where the policy is executed                      | Policy scope          | REQUEST\_CONTENT |
| headerRules |          | List of mask rules to apply on client and proxy headers | List\<MaskHeaderRule> |                  |
| bodyRules   |          | List of mask rules to apply on client and proxy body    | List\<MaskBodyRule>   |                  |

## Mask header rule <a href="#user-content-mask-header-rule" id="user-content-mask-header-rule"></a>

| Property | Required | Description              | Type   | Default |
| -------- | -------- | ------------------------ | ------ | ------- |
| path     |          | Header name to transform | String |         |
| replacer |          | Replacement character    | String | \*      |

## Mask body rule <a href="#user-content-mask-body-rule" id="user-content-mask-body-rule"></a>

| Property | Required | Description                                                                                                                                                      | Type        | Default |
| -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------- |
| path     |          | Context-dependent. If "Content-type" is `application / json` you must use `json-path`, if it is "application / xml" you must use `xml-path`, otherwise not used. | String      |         |
| type     |          | Value selector type                                                                                                                                              | MaskPattern |         |
| regex    |          | Custom value selector (use regular expression)                                                                                                                   | String      |         |
| replacer |          | Replacement character                                                                                                                                            | String      | \*      |
