# Kafka ACL

This policy is used to define [ACLs](https://kafka.apache.org/documentation/#security_authz) on resources in the cluster that are proxied by the gateway. You can can define ACLs on topics, clusters, consumer groups, and transactional IDs.

The ACLs are restrictive in that once they are applied, clients of the proxy must be authorized to perform the actions they are taking. If there is no ACL defined for the action taken by the user, the action is prohibited. This is the same behavior as with regular Kafka clusters, as we see in the above documentation:

> By default, if no ResourcePatterns matches a specific Resource "R", then "R" has no associated ACLs, and therefore no one other than super users is allowed to access "R".

### How to formulate ACLs in the policy

In order to create and apply and ACL, configure the following options:

* First, you select the resource type for which you want to apply the ACLs (topics, clusters, or groups).
* Next, you choose the **pattern** used to name the resource. This pattern can be:
  * `Any`: All resources of the specified type receive the ACL on proxy connections.
  * `Match`: Resources matching the pattern (prefixed, literal, or wildcard i.e. "\*") receive the ACL.
  * `Literal`: Resources whose name is an exact match for the specified string receive the ACL.
  * `Prefixed`: Resources whose name starts with the specified string receive the ACL.
* Lastly, you define the **action** that the ACL permits. These options correspond to the operations defined in Kafka, as listed [here](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#operations).

You can add more than one ACL in the same policy. The principle in Kafka is that if there is an ACL that denies an action, then that takes precedence over ACLs that allow an action. So, if more than one ACL applies to the client connection to the gateway, the least permissive ACL is applied.

<figure><img src="../../.gitbook/assets/image (154).png" alt=""><figcaption><p>Kafka ACL Policy UI</p></figcaption></figure>

### Examples

* If you want to allow only reads and not writes to all topics, set the `Resource` to `Topic`, the `Pattern` to `ANY`, and the `Action` to `Read`.
* If you want to allow read-only access to all topic names starting with "integrator", then set the `Resource` to `Topic`, the `Pattern Type` to `PREFIXED`, and the `Pattern` to "`integrator`".
* If you want to allow only certain application users to delete consumer groups, enable `Delete` on the `Groups` resource option.

### Using Expressions in the Condition

The expression language (EL) functionality in Gravitee can be used to define conditions on each ACL. This is an easy way to define ACLs for multiple applications, or to define dynamic conditions. Some examples are as follows:

* To set the ACL for a specific application ID, set the condition to `{#context.attributes['application'] == 'abcd-1234'}`, where `'abcd-1234`' is the application ID. You can obtain this ID in the UI by checking the URL for the application.
* To set the ACL based on a specific subscription for an API key plan, set the condition to `{#context.attributes['user-id'] == 'abcd-1234'}`, where `'abcd-1234'` is the subscription ID.
* To set the ACL based on the claim in a JWT token, set the condition to e.g. `{#context.attributes['jwt.claims']['iss']}`, changing the `iss` to the desired claim.
* To set the ACL based on the claim in an OAuth2 token, set the condition to e.g. `{#jsonPath(#context.attributes['oauth.payload']['custom_claim'])}`, changing the `custom_claim` to the desired claim.

### Using the Token Resource

ACLs on the `Token` resource determine whether the user can manage [delegation tokens](https://docs.confluent.io/platform/current/security/authentication/delegation-tokens/overview.html#kafka-sasl-delegate-auth) in the cluster. When added to the policy, proxy clients are either enabled or restricted from using delegation tokens in order to perform clustered operations through the proxy. For example, if using a clustered processing framework like [Apache Spark](https://spark.apache.org/), delegation tokens may be used to share resources across the same application without requiring distributing Kerberos keytabs across the cluster when mTLS is used.

### Using the Transaction ID Resource

The `Transactional ID` resource is used when producers encounter application restarts and is necessary for exact-once semantics. From the [Confluent documentation](https://docs.confluent.io/platform/current/security/authorization/acls/overview.html#resources):

> A transactional ID (transactional.id) identifies a single producer instance across application restarts and provides a way to ensure a single writer; this is necessary for exactly-once semantics (EOS). Only one producer can be active for each transactional.id. When a producer starts, it first checks whether or not there is a pending transaction by a producer with its own transactional.id. If there is, then it waits until the transaction has finished (abort or commit). This guarantees that the producer always starts from a consistent state. When used, a producer must be able to manipulate transactional IDs and have all the permissions set.

### Important Notes <a href="#user-content-supported-kafka-apikeys" id="user-content-supported-kafka-apikeys"></a>

When using the _Kafka Topic Mapping_ policy together with the _Kafka ACL_ policy, it is important to place the _Kafka ACL_ policy **before** the _Kafka Topic Mapping_ policy, as shown below:

<figure><img src="../../.gitbook/assets/image (160).png" alt=""><figcaption><p>Screenshot of the Kafka ACL policy placed before the Kafka Topic Mapping policy</p></figcaption></figure>
