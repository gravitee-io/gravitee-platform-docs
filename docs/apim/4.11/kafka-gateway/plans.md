---
description: An overview about plans.
metaLinks:
  alternates:
    - plans.md
---

# Plans

## Overview

A **plan** provides a service and access layer on top of your API that specifies access limits, subscription validation modes, and other configurations to tailor it to an application. To expose your Kafka API to internal or external consumers, it must have at least one plan. Gravitee offers the following types of plans for Kafka APIs:

* **Keyless.** For more information about the keyless plan, see [keyless.md](../secure-and-expose-apis/plans/keyless.md "mention").
* **API Key.** For more information about the API Key plan, see [api-key.md](../secure-and-expose-apis/plans/api-key.md "mention").
* **OAuth2.** For more information about the OAuth2 plan, see [oauth2.md](../secure-and-expose-apis/plans/oauth2.md "mention").
* **JWT.** For more information about the JWT plan, see [jwt.md](../secure-and-expose-apis/plans/jwt.md "mention").
* **mTLS.** For more information about the mTLS plan, see the [mTLS plan security](#mtls-plan-security) section below.

For Kafka APIs, these plans correspond directly to Kafka authentication methods:

<table><thead><tr><th width="201">Plan</th><th>Corresponding Kafka Authentication</th></tr></thead><tbody><tr><td>Keyless (public)</td><td>PLAINTEXT</td></tr><tr><td>API Key</td><td>The API key is used as the password, and the md5 hash of the API key is used as the username, as part of the SASL/SSL with SASL PLAIN authentication method.</td></tr><tr><td>JWT</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication, where the JWT is used as the OAuth token.</td></tr><tr><td>OAuth2</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication.</td></tr><tr><td>mTLS</td><td>Mutual TLS authentication using client certificates validated against the gateway's truststore.</td></tr></tbody></table>

To authenticate users, each plan must include at least one security type. A security type is a policy that is integrated directly into a plan. Once a plan is created, the security type cannot be changed. Also, your Kafka APIs cannot have conflicting authentication.

{% hint style="warning" %}
Kafka Native APIs enforce strict separation between three plan security categories. Only one category may have published plans at any time: **Keyless**, **mTLS**, or **Authentication** (OAuth2, JWT, API Key). Publishing a plan from one category automatically closes all published plans from the other two categories.
{% endhint %}

### Plan security mutual exclusion

The following table describes the plan security categories and their coexistence rules:

<table><thead><tr><th>Category</th><th>Plan Types</th><th>Can Coexist With</th></tr></thead><tbody><tr><td>Keyless</td><td><code>KEY_LESS</code></td><td>Other Keyless plans only</td></tr><tr><td>mTLS</td><td><code>MTLS</code></td><td>Other mTLS plans only</td></tr><tr><td>Authentication</td><td><code>OAUTH2</code>, <code>JWT</code>, <code>API_KEY</code></td><td>Other Authentication plans only</td></tr></tbody></table>

## Plan stages

A plan can exist in one of four stages:

* STAGING. This is the draft mode of a plan, where it can be configured but won't be accessible to users.
* PUBLISHED. API consumers can view a published plan on the Developer Portal. Once subscribed, they can use it to consume the API. A published plan can still be edited.
* DEPRECATED. A deprecated plan won't be available on the Developer Portal and API consumers won't be able to subscribe to it. This cannot be undone. Existing subscriptions are not impacted, giving current API consumers time to migrate without breaking their application.
* CLOSED. Once a plan is closed, all associated subscriptions are closed. API consumers subscribed to this plan won't be able to use the API. This cannot be undone.

Depending on the stage it's in, a plan can be edited, published, deprecated, or closed. See [this](create-and-configure-kafka-apis/configure-kafka-apis/consumers.md#plans) documentation for specific instructions.

### Edit a plan

To edit a plan, click on the pencil icon:

<figure><img src="../.gitbook/assets/plan_edit (1).png" alt=""><figcaption><p>Edit a plan</p></figcaption></figure>

### Publish a plan

To publish a plan, click on the icon of a cloud with an arrow:

<figure><img src="../.gitbook/assets/plan_publish (1).png" alt=""><figcaption><p>Publish a plan</p></figcaption></figure>

Once a plan has been published, it must be redeployed.

{% hint style="info" %}
Publishing a plan from one security category (Keyless, mTLS, or Authentication) automatically closes all published plans from the other two categories. The Console UI displays a confirmation dialog that lists plans to be closed and requires typing the new plan name to proceed.
{% endhint %}

### Deprecate a plan

To deprecate a plan, click on the icon of a cloud with an 'x':

<figure><img src="../.gitbook/assets/plan_deprecate (1).png" alt=""><figcaption><p>Deprecate a plan</p></figcaption></figure>

### Close a plan

To close a plan, click on the 'x' icon:

<figure><img src="../.gitbook/assets/plan_close (1).png" alt=""><figcaption><p>Close a plan</p></figcaption></figure>

## Plan selection rules

Unlike with HTTP APIs, there is only ever one set of policies per plan. Once the plan is defined, you can add one set of policies on that plan, but you can only remove it or edit it. The plan is selected based on the credential defined by the client in their connection properties.

## mTLS plan security

Kafka Native APIs support mutual TLS (mTLS) authentication as a plan security type. Administrators can publish mTLS plans to enforce client certificate authentication for Kafka connections, enabling certificate-based access control alongside existing authentication methods (OAuth2, JWT, API Key) and Keyless plans.

### Prerequisites

Before you configure Kafka SSL client authentication, ensure you have the following:

* Kafka gateway configured with SSL client authentication enabled (`kafka.ssl.clientAuth: required`)
* Server truststore containing the CA certificate that signed client certificates
* Server keystore with the gateway's SSL certificate
* Client certificates signed by a CA trusted by the gateway
* V4 API definition with Kafka listener type

### Restrictions

mTLS plans for Kafka Native APIs are subject to the following restrictions:

* mTLS plans are available only for V4 APIs with Kafka listener type.
* Publishing an mTLS plan automatically closes all published Keyless and Authentication plans.
* Publishing a Keyless or Authentication plan automatically closes all published mTLS plans.
* Multiple mTLS plans may be published simultaneously, but they cannot coexist with Keyless or Authentication plans.
* Certificate validation failures return asynchronous errors for Kafka connections and synchronous 401 responses for HTTP connections.
* The gateway requires JKS truststore and keystore formats (configured via `kafka.ssl.truststore.type` and `kafka.ssl.keystore.type`).

### Certificate validation flow

The mTLS policy extracts the client certificate from the TLS session, validates the certificate chain, and computes an MD5 digest of the certificate encoding to generate a security token. For Kafka connections, validation failures return asynchronous errors wrapped in `MtlsPolicyException`. For HTTP connections, validation failures interrupt the request with a 401 Unauthorized response.

### Kafka SSL properties

Configure the Kafka gateway to require client certificate authentication. All properties must be set in the gateway configuration file.

<table><thead><tr><th>Property</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code>kafka.ssl.clientAuth</code></td><td>Require client certificate authentication</td><td><code>required</code></td></tr><tr><td><code>kafka.ssl.truststore.type</code></td><td>Truststore format for verifying client certificates</td><td><code>jks</code></td></tr><tr><td><code>kafka.ssl.truststore.password</code></td><td>Password for the truststore</td><td><code>gravitee</code></td></tr><tr><td><code>kafka.ssl.truststore.path</code></td><td>Path to truststore containing CA certificates</td><td><code>/path/to/server.truststore.jks</code></td></tr><tr><td><code>kafka.ssl.keystore.type</code></td><td>Keystore format for server certificate</td><td><code>jks</code></td></tr><tr><td><code>kafka.ssl.keystore.password</code></td><td>Password for the keystore</td><td><code>gravitee</code></td></tr><tr><td><code>kafka.ssl.keystore.path</code></td><td>Path to server keystore</td><td><code>/path/to/server.keystore.jks</code></td></tr></tbody></table>

### Client configuration

Configure Kafka clients to present the client certificate during the SSL handshake. The gateway validates the certificate and establishes the connection if validation succeeds.

<table><thead><tr><th>Property</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code>ssl.keystore.location</code></td><td>Path to client certificate keystore</td><td><code>/path/to/client.keystore.jks</code></td></tr><tr><td><code>ssl.keystore.type</code></td><td>Client keystore format</td><td><code>JKS</code></td></tr><tr><td><code>ssl.keystore.password</code></td><td>Client keystore password</td><td><code>client-password</code></td></tr><tr><td><code>ssl.truststore.location</code></td><td>Path to truststore for verifying server certificates</td><td><code>/path/to/client.truststore.jks</code></td></tr></tbody></table>

### Console UI changes

The Console UI includes the following changes to support mTLS plans for Kafka Native APIs:

* The plan list displays "mTLS" as a security type label.
* The plan creation menu filters available security types to show mTLS only for Kafka Native APIs. For V4 APIs with Kafka listeners, the `PUSH` plan type is hidden and `MTLS` is available. For V4 APIs with other listeners or V2 APIs, both `PUSH` and `MTLS` are hidden.
* The plan creation wizard banner text was updated to: "Kafka APIs cannot mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans."
* Publishing a conflicting plan triggers a confirmation dialog that lists plans to be closed and requires typing the new plan name to proceed.
* Subscription creation errors now display server-provided error messages instead of generic failure text.

### mTLS policy upgrade

The mTLS policy was upgraded to version 2.0.0-alpha.2 with the following enhancements:

* `KafkaSecurityPolicy` interface support for Kafka authentication flows.
* Custom exception handling for Kafka authentication failures via `MtlsPolicyException`.


