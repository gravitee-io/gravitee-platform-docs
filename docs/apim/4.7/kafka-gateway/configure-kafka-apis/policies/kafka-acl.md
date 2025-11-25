---
description: An overview about kafka acl.
---

# Kafka ACL

## Overview

The Kafka ACL policy is used to define [ACLs](https://kafka.apache.org/documentation/#security_authz) on cluster resources that are proxied by the Gateway. You can define ACLs on topics, clusters, consumer groups, and transactional IDs.

ACLs are restrictive because once they are applied, proxy clients must be authorized to perform the actions they are taking. If there is no ACL defined for the action taken by the user, the action is prohibited. This is the same behavior as with regular Kafka clusters. For more information about ACLs and authorization, see[ the Kafka documentation](https://kafka.apache.org/24/documentation.html#security_authz).

## How to formulate ACLs in the policy

To create and apply an ACL, complete the following steps. These steps configure options that correspond to the operations defined in Kafka, as listed in the [Confluent documentation](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#operations).

1. Select the **resource type** for which you want to apply the ACLs (topics, clusters, or groups).
2. Choose the **pattern** used to name the resource. This pattern can be:
   * `Any`: All resources of the specified type receive the ACL on proxy connections.
   * `Match`: Resources matching the pattern (prefixed, literal, or wildcard "\*") receive the ACL.
   * `Literal`: Resources whose name is an exact match to the specified string receive the ACL.
   * `Prefixed`: Resources whose name starts with the specified string receive the ACL.
   * `Expression`: Resources that match the specified expression receive the ACL. For example, `foo.*.bar.?` matches `foo.42.bar.x`.
     * `*` matches zero or more characters
     * `?` matches exactly one character
3. Define the **action** that the ACL permits.

You can add more than one ACL in the same policy.

{% hint style="info" %}
Kafka follows the rule that if there is an ACL that denies an action, it takes precedence over ACLs that allow an action. If more than one ACL applies to the client connection to the Gateway, the most restrictive ACL is applied.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image%20(154)%20(1).png" alt=""><figcaption><p>Kafka ACL Policy UI</p></figcaption></figure>

## Examples

* If you want to allow only reads and not writes to all topics, set the `Resource` to `Topic`, the `Pattern` to `ANY`, and the `Action` to `Read`.
* If you want to allow read-only access to all topic names starting with "integrator," then set the `Resource` to `Topic`, the `Pattern Type` to `PREFIXED`, and the `Pattern` to `integrator`.
* If you want to allow only certain application users to delete consumer groups, enable `Delete` on the `Group` resource option.
* If you want to create a dynamic ACL that can match complicated conditions, you can specify an expression pattern on the `Group`, `Topic`, or `Transactional ID` resources.

## Using expressions in the condition

Gravitee Expression Language (EL) can be used to define conditions on each ACL. This is an easy way to define ACLs for multiple applications, or to define dynamic conditions. For example:

* To set the ACL for a specific application, set the condition to `{#context.attributes['application'] == 'abcd-1234'}`, where `'abcd-1234`' is the application ID. You can obtain this ID in the UI by checking the URL for the application.
* To set the ACL based on a specific subscription for an API Key plan, set the condition to `{#context.attributes['user-id'] == 'abcd-1234'}`, where `'abcd-1234'` is the subscription ID.
* To set the ACL based on the claim in a JWT token, set the condition to, e.g.,`{#context.attributes['jwt.claims']['iss']}`, changing the `iss` to the desired claim.
* To set the ACL based on the claim in an OAuth2 token, set the condition to, e.g., `{#jsonPath(#context.attributes['oauth.payload']['custom_claim'])}`, changing the `custom_claim` to the desired claim.
* To set the ACL to match an expression pattern, you can use wildcards. For example, `auto.?.syncx.*` will match `auto.x.syncx.interop.xyz`, `auto.y.syncx.interop.yzx`, or `auto.z.syncx.interop.zyx`, but it will not match `auto.xx.syncx.interop.xyz`.

## Using resources

### Token resource

ACLs on the `Token` resource determine whether the user can manage [delegation tokens](https://docs.confluent.io/platform/current/security/authentication/delegation-tokens/overview.html#kafka-sasl-delegate-auth) in the cluster. When added to the policy, proxy clients are either permitted or restricted from using delegation tokens to perform clustered operations through the proxy.

For example, when using a clustered processing framework like [Apache Spark](https://spark.apache.org/), delegation tokens can be used to share resources across the same application without requiring the distribution of Kerberos keytabs across the cluster when mTLS is used.

### Transactional ID resource

The `Transactional ID` resource is used when producers encounter application restarts, and is necessary for exactly-once semantics. For more information, see the [Confluent documentation](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#resources).

## In combination with the Kafka Topic Mapping policy

When using the Kafka ACL policy together with the [Kafka Topic Mapping](kafka-topic-mapping.md) policy, order is important. If topic mapping occurs before ACL, the ACL policy must use the broker-side name of the topic mapping. Conversely, if ACL occurs before topic mapping, the ACL policy must use the mapped name, which is the client-side name of the topic mapping.

The following examples show how you can place the topic mapping and ACL policies in relation to one another to achieve specific results.

### Example 1: I want to execute the ACL policy after topic mapping

An API Gateway enforces Kafka ACL rules to control access to topics. However, if ACL checks happen before topic mapping, requests may be rejected because the client-side topic name isn't recognized.

To ensure that ACL rules are applied correctly, the ACL policy should be executed after the Topic Mapping policy so that it evaluates the actual broker-side topic.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console.

Kafka Topic Mapping configuration:

<figure><img src="../../../.gitbook/assets/00 3.png" alt=""><figcaption><p>Kafka Topic Mapping policy configuration UI</p></figcaption></figure>

Kafka ACL configuration:

<figure><img src="../../../.gitbook/assets/00 5.png" alt=""><figcaption><p>Kafka ACL policy configuration UI</p></figcaption></figure>

Here is how the policies should be ordered in the policy chain:

<figure><img src="../../../.gitbook/assets/00 ta.png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [    
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "orders",
                    "broker": "internal.orders.processing.12345"
                  }
                ]
              }
            },
            {
              "name": "Kafka ACL Policy",
              "enabled": true,
              "policy": "kafka-acl",
              "configuration": {
                "authorizedTopics": [
                  "internal.orders.processing.12345"
                ],
                "authorizationType": "READ"
              }
            }
          ]
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Example 2: I want to enforce ACL before topic mapping with wildcard permissions

Suppose a security-first organization requires Kafka ACL rules to be enforced before topic mapping, but some applications need wildcard-based access control to produce or consume messages from any topic that matches a pattern.

In this scenario, the ACL policy must be able to handle wildcard rules for groups of topics. In addition, topics must be mapped after authorization so that consumers don’t need to know internal topic names.

With this configuration:

* ACL ensures users can access only `internal.orders.*` topics.
* Topic mapping consolidates all internal topics into a single `orders` topic for external consumers.

{% tabs %}
{% tab title="Using the APIM Console" %}
This shows how to implement the example above using the APIM Console.

ACL configuration:

<figure><img src="../../../.gitbook/assets/00 6.png" alt=""><figcaption></figcaption></figure>

Topic mapping configuration:

<figure><img src="../../../.gitbook/assets/00 4.png" alt=""><figcaption></figcaption></figure>

Here is how the policies should be ordered in the policy chain:

<figure><img src="../../../.gitbook/assets/00 at.png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="v4 API definition" %}
This shows how to implement the example above in a v4 API definition:

```json
{
  "api": {
    ...
  },
  "plans: [    
    {
      "flows": [
        {
          "interact": [
            {
              "name": "Kafka ACL Policy",
              "enabled": true,
              "policy": "kafka-acl",
              "configuration": {
                "authorizedTopics": [
                  "internal.orders.*"
                ],
                "authorizationType": "READ_WRITE"
              }
            },
            {
              "name": "Kafka Topic Mapping",
              "enabled": true,
              "policy": "kafka-topic-mapping",
              "configuration": {
                "mappings": [
                  {
                    "client": "orders",
                    "broker": "internal.orders.global"
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}
