---
description: An overview about message filtering.
metaLinks:
  alternates:
    - message-filtering.md
---

# Message Filtering

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../readme/enterprise-edition.md)**.**
{% endhint %}

## Overview

The `message-filtering` policy enables the API publisher to create and enforce a filter that controls which messages are streamed to the subscriber/consumer, given a defined set of criteria.

## Examples

{% hint style="warning" %}
This policy can be applied to v4 message APIs. It cannot be applied to v2 APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="Basic example: Match subscription metadata" %}
If this is my message:

```json
{
    "productId": "1234",
    "value": "any value"
}
```

I can use the following configuration to filter any messages according to subscriptions metadata `productId`:

```json
 {
    "name": "Products filter",
    "description": "Filter messages based on subscription product id",
    "enabled": true,
    "policy": "message-filtering",
    "configuration": {
        "filter": "{#jsonPath(#message.content, '$.productId') == '#subscription.metadata.productId'}"
    }
}
```
{% endtab %}

{% tab title="How to filter different payloads" %}
If a Kafka topic includes messages with different payloads, you can use the Message Filtering policy to selectively consume and forward only messages that match your filters.

Consider a Kafka topic with the following payloads:

```
{
  "account": {
    "id": 112131,
    "product": "remember",
    "type": "card",
    "creditLimit": 30000,
    "status": "active"
  }
}
```

```
{
  "card": {
    "id": 12345,
    "accountId": 987654321,
    "product": "remember",
    "cardHolder": "John Smith",
    "status": "active"
  }
}
```

```
{
  "contact": {
    "id": 6789,
    "personId": 192838475,
    "email": "john.smith@bigbank.com"
  }
}
```

To consume and forward only the "account" and "card" messages, you can use the following Expression Language in the "Filter condition" field of the Message Filtering policy:

`{(#jsonPath(#message.content, "$.account")!= null && #jsonPath(#message.content, "$.account.product")=='remember') || (#jsonPath(#message.content, "$.contact")!=null && #jsonPath(#message.content, "$.contact.id") > 1)}`

This filters out messages that do not meet the specified criteria, such as the "contact" message and any "card" messages that do not include an "id" value.

**Explanation**

Since the message could contain either the `$.account` or `$.contact` payloads, you must first check for `null` values to avoid referencing an attribute that may not exist. Then you can evaluate your desired filter or condition(s).

<figure><img src="../../../.gitbook/assets/image (37) (1).png" alt="" width="375"><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
{
  "name": "Message filtering",
  "description": "Apply filter to messages",
  "enabled": true,
  "policy": "message-filtering",
  "configuration": {
    "filter": "{#jsonPath(#message.content, '$.feature') == #subscription.metadata.feature}"
  }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `message-filtering` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `message-filtering` policy with the following options:

<table><thead><tr><th width="116">Property</th><th width="105" data-type="checkbox">Required</th><th width="152">Description</th><th width="100">Type</th><th>Default</th></tr></thead><tbody><tr><td>filter</td><td>true</td><td>The filter's rule</td><td>string</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-message-filtering/blob/master/CHANGELOG.md" %}
