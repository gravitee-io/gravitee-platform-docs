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
* **mTLS.** For more information about the mTLS plan, see the [mTLS Plans](#mtls-plans) section below.

For Kafka APIs, these plans correspond directly to Kafka authentication methods:

<table><thead><tr><th width="201">Plan</th><th>Corresponding Kafka Authentication</th></tr></thead><tbody><tr><td>Keyless (public)</td><td>PLAINTEXT</td></tr><tr><td>API Key</td><td>The API key is used as the password, and the md5 hash of the API key is used as the username, as part of the SASL/SSL with SASL PLAIN authentication method.</td></tr><tr><td>JWT</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication, where the JWT is used as the OAuth token.</td></tr><tr><td>OAuth2</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication.</td></tr><tr><td>mTLS</td><td>Certificate-based mutual authentication using TLS client certificates.</td></tr></tbody></table>

To authenticate users, each plan must include at least one security type. A security type is a policy that is integrated directly into a plan. Once a plan is created, the security type cannot be changed. Also, your Kafka APIs cannot have conflicting authentication. For example, if your Kafka API has the Keyless plan, you must have Keyless authentication. However, you can use policies to add additional security at the API or plan level.

## Plan Mutual Exclusion

Kafka Native APIs enforce mutual exclusion between three categories of plan security types:

| Category | Security Types | Description |
|:---------|:---------------|:------------|
| **Keyless** | Keyless | No authentication required |
| **mTLS** | mTLS | Certificate-based mutual authentication |
| **Authentication** | API Key, OAuth2, JWT | Token or key-based authentication |

These categories are **mutually exclusive**: only plans from one category can be published at a time. Publishing a plan from a different category automatically closes any plans from conflicting categories.

### Automatic Plan Closure Rules

When you publish a plan, the gateway automatically closes any published plans from conflicting categories:

- **Publishing a Keyless plan** closes any published mTLS or authentication plans
- **Publishing an mTLS plan** closes any published Keyless or authentication plans
- **Publishing an authentication plan** (API Key, OAuth2, or JWT) closes any published Keyless or mTLS plans

### Example Scenarios

**Scenario 1: Publishing an mTLS plan when a Keyless plan is active**

1. You have a published Keyless plan
2. You create and publish an mTLS plan
3. The gateway automatically closes the Keyless plan
4. Only the mTLS plan remains published

**Scenario 2: Publishing an API Key plan when an mTLS plan is active**

1. You have a published mTLS plan
2. You create and publish an API Key plan
3. The gateway automatically closes the mTLS plan
4. Only the API Key plan remains published

### Rationale

Kafka's connection model does not support mixing authentication methods within a single API deployment. Each Kafka client connection uses a single authentication mechanism, and the gateway must enforce consistent authentication across all connections to the same API.

### Plan Creation Wizard Warning

When creating or publishing plans for Kafka Native APIs, the Console displays a warning banner to inform you about plan type mutual exclusion:

{% hint style="warning" %}
Kafka APIs cannot mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans. In order to automatically deploy your API, choose one type: either Keyless, mTLS, or authentication plans.
{% endhint %}

This warning appears in the plan creation wizard and reminds you that:

- Only plans from one security category (Keyless, mTLS, or Authentication) can be published simultaneously
- Publishing a plan from a different category automatically closes any published plans from conflicting categories
- You must choose a single security approach for your Kafka Native API

For example, if you have a published API Key plan and attempt to publish an mTLS plan, the Console displays a confirmation dialog listing the plans that will be automatically closed.

### Console Warnings

When you attempt to publish a plan that conflicts with existing published plans, the console displays a confirmation dialog:

**Dialog title:** "Publish plan and close current one(s)"

**Dialog content:**
> Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
> 
> Are you sure you want to publish the **[Security Type]** plan **[Plan Name]**?
> 
> The following plan(s) will be closed automatically:
> - **[Conflicting Plan Name]** ([Security Type])

Review the list of plans that will be closed, then click **Publish and Close** to confirm.

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

### Deprecate a plan

To deprecate a plan, click on the icon of a cloud with an 'x':

<figure><img src="../.gitbook/assets/plan_deprecate (1).png" alt=""><figcaption><p>Deprecate a plan</p></figcaption></figure>

### Close a plan

To close a plan, click on the 'x' icon:

<figure><img src="../.gitbook/assets/plan_close (1).png" alt=""><figcaption><p>Close a plan</p></figcaption></figure>

## Plan selection rules

Unlike with HTTP APIs, there is only ever one set of policies per plan. Once the plan is defined, you can add one set of policies on that plan, but you can only remove it or edit it. The plan is selected based on the credential defined by the client in their connection properties.

## mTLS Plans

{% hint style="info" %}
**Enterprise Edition**

mTLS plans for Kafka Native APIs require:
- **Enterprise Edition license**: mTLS plans are an Enterprise Edition feature
- **Plugin version**: `gravitee-policy-mtls` version 2.0.0 or later (version 1.x does not support Kafka Native APIs)
{% endhint %}

Gravitee API Management supports **mTLS (mutual TLS) authentication** as a plan security type for Kafka Native APIs. This enables certificate-based mutual authentication between Kafka clients and the Gravitee Kafka Gateway, providing a strong security option for organizations that require strict certificate-based authentication, such as those in financial services, healthcare, and other regulated industries.

### How mTLS Works

mTLS is a security mechanism where both the client and the server authenticate each other using TLS certificates:

- The **gateway** presents its server certificate to the Kafka client
- The **Kafka client** presents its client certificate to the gateway
- The gateway verifies the client certificate against a configured truststore
- The client certificate is matched against a subscription's registered certificate to authorize access

### Prerequisites

Before configuring mTLS for a Kafka Native API:

1. **Enterprise License**: Verify you have a Gravitee Enterprise Edition license
2. **TLS Certificates**: Prepare:
   - A **server keystore** (JKS format) containing the gateway's private key and certificate
   - A **server truststore** (JKS format) containing the Certificate Authority (CA) certificates that signed the client certificates
   - **Client certificates** (generated and signed by the CA in the truststore) for each Kafka client

### Gateway Configuration

Configure the following properties in your Gravitee gateway configuration to enable mTLS for the Kafka Gateway:

**Server Keystore (Gateway Identity)**

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.keystore.type` | Keystore format | `jks` |
| `kafka.ssl.keystore.path` | Path to the server keystore file | `/path/to/server.keystore.jks` |
| `kafka.ssl.keystore.password` | Keystore password | `changeit` |

**Server Truststore (Client Certificate Verification)**

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Client authentication mode | `required` |
| `kafka.ssl.truststore.type` | Truststore format | `jks` |
| `kafka.ssl.truststore.path` | Path to the server truststore file (contains CAs that signed client certs) | `/path/to/server.truststore.jks` |
| `kafka.ssl.truststore.password` | Truststore password | `changeit` |

Setting `kafka.ssl.clientAuth` to `required` means the gateway rejects any connection that doesn't present a valid client certificate signed by a CA in the truststore.

### Creating an mTLS Plan

To create an mTLS plan for a Kafka Native API:

1. Navigate to the API's **Plans** section in the API Management Console
2. Click **Add new plan**
3. Select **mTLS** as the security type
4. Configure the plan settings (name, description, validation mode)
5. Publish the plan

When publishing an mTLS plan, the console warns you if conflicting plans (Keyless or Authentication plans) are currently published. Confirm the publish action to automatically close the conflicting plans.

### Creating a Subscription with mTLS

To subscribe to an mTLS-secured Kafka API, the subscription must include a **client certificate**. The certificate is base64-encoded and stored with the subscription.

<!-- GAP: The exact API call or console UI flow for creating a subscription with a client certificate is not fully documented in the source material. -->

When a Kafka client connects:

1. The client presents its certificate during the TLS handshake
2. The gateway extracts the certificate and computes its MD5 fingerprint
3. The fingerprint is matched against registered subscription certificates
4. If a match is found, the connection is authorized under that subscription

### Kafka Client Configuration

Kafka clients connecting to an mTLS-secured API must configure SSL client authentication. The client must present a certificate during the TLS handshake and trust the gateway's server certificate.

#### Client Keystore Configuration

Configure the following properties to enable the client to present its certificate:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to the client keystore file | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Keystore format | `JKS` |
| `ssl.keystore.password` | Client keystore password | `changeit` |

#### Client Truststore Configuration

Configure the following properties to enable the client to trust the gateway's server certificate:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.truststore.location` | Path to the client truststore file | `/path/to/client.truststore.jks` |
| `ssl.truststore.password` | Client truststore password | `changeit` |

The client truststore must contain the Certificate Authority (CA) certificate that signed the gateway's server certificate, or the gateway's server certificate itself.

#### Example Client Configuration

```properties
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.type=JKS
ssl.keystore.password=changeit
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=changeit
```

During the TLS handshake:

1. The gateway presents its server certificate to the client
2. The client verifies the server certificate against its truststore
3. The client presents its client certificate to the gateway
4. The gateway validates the client certificate and matches it against registered subscription certificates
5. If validation succeeds, the connection is authorized under the matched subscription

### Gateway-to-Broker Independence

The mTLS configuration applies to the connection between the **Kafka client and the Gravitee Gateway** only. The connection between the Gravitee Gateway and the backend Kafka broker cluster is configured independently. This means:

- You can use mTLS for client-to-gateway encryption while using a plaintext or different security protocol for gateway-to-broker communication
- The `sharedConfiguration` on the endpoint group controls the gateway-to-broker connection security

### Authentication Flow

When a Kafka client connects to an mTLS-secured API:

1. The TLS handshake occurs, during which the client presents its certificate
2. The gateway's security chain validates the certificate
3. If validation succeeds, the connection is marked as `plainTextAuthenticated`
4. The principal is set to the certificate identity
5. If authentication fails, the gateway logs a warning and gracefully closes the connection

Authentication failures are handled gracefully—the connection is closed without propagating error frames to the client. The error is logged at WARN level:
```
Authentication failed [reason]
```