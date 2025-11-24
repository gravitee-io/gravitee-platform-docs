---
description: An overview about kafka acl.
---

# Kafka ACL

## Overview

The Kafka ACL policy is used to define [ACLs](https://kafka.apache.org/documentation/#security_authz) on cluster resources that are proxied by the Gateway. You can can define ACLs on topics, clusters, consumer groups, and transactional IDs.

ACLs are restrictive in that once they are applied, proxy clients must be authorized to perform the actions they are taking. If there is no ACL defined for the action taken by the user, the action is prohibited. This is the same behavior as with regular Kafka clusters, [as noted in the Kafka documentation](https://kafka.apache.org/24/documentation.html#security_authz).

{% hint style="info" %}
**Policy order**

When using the Kafka Topic Mapping policy together with the Kafka ACL policy, it is important to place the Kafka ACL policy **before** the Kafka Topic Mapping policy, as shown below.
{% endhint %}

<figure><img src="../../.gitbook/assets/policy order.png" alt=""><figcaption><p>Screenshot of the Kafka ACL policy placed before the Kafka Topic Mapping policy</p></figcaption></figure>

## How to formulate ACLs in the policy

To create and apply an ACL, follow the steps below. These steps configure options that correspond to the operations defined in Kafka, as listed [here](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#operations).

1. Select the **resource type** for which you want to apply the ACLs (topics, clusters, or groups).
2. Choose the **pattern** used to name the resource. This pattern can be:
   * `Any`: All resources of the specified type receive the ACL on proxy connections.
   * `Match`: Resources matching the pattern (prefixed, literal, or wildcard, i.e., "\*") receive the ACL.
   * `Literal`: Resources whose name is an exact match to the specified string receive the ACL.
   * `Prefixed`: Resources whose name starts with the specified string receive the ACL.
3. Define the **action** that the ACL permits.

You can add more than one ACL in the same policy. Kafka follows the rule that if there is an ACL that denies an action, it takes precedence over ACLs that allow an action. If more than one ACL applies to the client connection to the Gateway, the most restrictive ACL is applied.

<figure><img src="../../.gitbook/assets/image (154).png" alt=""><figcaption><p>Kafka ACL Policy UI</p></figcaption></figure>

## Examples

* If you want to allow only reads and not writes to all topics, set the `Resource` to `Topic`, the `Pattern` to `ANY`, and the `Action` to `Read`.
* If you want to allow read-only access to all topic names starting with "integrator," then set the `Resource` to `Topic`, the `Pattern Type` to `PREFIXED`, and the `Pattern` to `integrator`.
* If you want to allow only certain application users to delete consumer groups, enable `Delete` on the `Groups` resource option.

## Using expressions in the condition

Gravitee Expression Language (EL) can be used to define conditions on each ACL. This is an easy way to define ACLs for multiple applications, or to define dynamic conditions. For example:

* To set the ACL for a specific application, set the condition to `{#context.attributes['application'] == 'abcd-1234'}`, where `'abcd-1234`' is the application ID. You can obtain this ID in the UI by checking the URL for the application.
* To set the ACL based on a specific subscription for an API Key plan, set the condition to `{#context.attributes['user-id'] == 'abcd-1234'}`, where `'abcd-1234'` is the subscription ID.
* To set the ACL based on the claim in a JWT token, set the condition to, e.g.,`{#context.attributes['jwt.claims']['iss']}`, changing the `iss` to the desired claim.
* To set the ACL based on the claim in an OAuth2 token, set the condition to, e.g., `{#jsonPath(#context.attributes['oauth.payload']['custom_claim'])}`, changing the `custom_claim` to the desired claim.

## Using resources

### `Token` resource

ACLs on the `Token` resource determine whether the user can manage [delegation tokens](https://docs.confluent.io/platform/current/security/authentication/delegation-tokens/overview.html#kafka-sasl-delegate-auth) in the cluster. When added to the policy, proxy clients are either permitted or restricted from using delegation tokens to perform clustered operations through the proxy.

For example, when using a clustered processing framework like [Apache Spark](https://spark.apache.org/), delegation tokens can be used to share resources across the same application without requiring the distribution of Kerberos keytabs across the cluster when mTLS is used.

### `Transactional ID` resource

The `Transactional ID` resource is used when producers encounter application restarts, and is necessary for exactly-once semantics. See the [Confluent documentation](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#resources) for more information.
