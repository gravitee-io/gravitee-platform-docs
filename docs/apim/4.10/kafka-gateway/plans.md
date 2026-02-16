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
* **mTLS.** For more information about the mTLS plan, see [mtls.md](../secure-and-expose-apis/plans/mtls.md "mention").

{% hint style="info" %}
mTLS plans are supported for Kafka APIs starting in APIM 4.10.
{% endhint %}

For Kafka APIs, these plans correspond directly to Kafka authentication methods:

<table><thead><tr><th width="201">Plan</th><th>Corresponding Kafka Authentication</th></tr></thead><tbody><tr><td>Keyless (public)</td><td>PLAINTEXT</td></tr><tr><td>API Key</td><td>The API key is used as the password, and the md5 hash of the API key is used as the username, as part of the SASL/SSL with SASL PLAIN authentication method.</td></tr><tr><td>JWT</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication, where the JWT is used as the OAuth token.</td></tr><tr><td>OAuth2</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication.</td></tr></tbody></table>

To authenticate users, each plan must include at least one security type. A security type is a policy that is integrated directly into a plan. Once a plan is created, the security type cannot be changed. Also, your Kafka APIs cannot have conflicting authentication. For example, If your Kafka API has the Keyless plan, you must have Keyless authentication. However, you can use policies to add additional security at the API or plan level.

{% hint style="warning" %}
You cannot have multiple published plans with conflicting authentication. For example, you cannot have a Keyless plan and a JWT plan for a Kafka API. However, you can have multiple plans with authentication for a Kafka API. For example, OAuth and JWT.
{% endhint %}

## Plan stages

A plan can exist in one of four stages:

* STAGING. This is the draft mode of a plan, where it can be configured but won’t be accessible to users.
* PUBLISHED. API consumers can view a published plan on the Developer Portal. Once subscribed, they can use it to consume the API. A published plan can still be edited.
* DEPRECATED. A deprecated plan won’t be available on the Developer Portal and API consumers won’t be able to subscribe to it. This cannot be undone. Existing subscriptions are not impacted, giving current API consumers time to migrate without breaking their application.
* CLOSED. Once a plan is closed, all associated subscriptions are closed. API consumers subscribed to this plan won’t be able to use the API. This cannot be undone.

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

### What is mTLS for Native Kafka APIs?

Mutual TLS (mTLS) for Native Kafka APIs is an authentication mechanism that requires both the Gateway and the Kafka client to present valid certificates during the TLS handshake. This differs from standard TLS authentication, where only the Gateway's identity is verified by the client.

**Security model comparison:**

- **TLS only (standard):** The Kafka client verifies the Gateway's identity using the Gateway's certificate.
- **TLS + mTLS (mutual authentication):** Both the Gateway and the Kafka client must present valid certificates. The Gateway verifies the client's identity using the client certificate, and the client verifies the Gateway's identity.

mTLS for Native Kafka APIs works the same way as mTLS for classic APIs in APIM. It provides an additional security layer on top of the TLS already required for Native Kafka APIs.

<!-- GAP: Draft does not specify if this feature is Enterprise-only or available in Community Edition -->

### Prerequisites

Before configuring mTLS for Native Kafka APIs, ensure the following technical requirements are met:

**Gateway requirements:**

- A keystore containing the Gateway's private key and certificate
- A truststore containing the Certificate Authorities (CAs) that signed client certificates
- `clientAuth` enabled in the Gateway configuration

**Kafka client requirements:**

- A keystore containing the client's private key and certificate
- A truststore containing the CA that signed the Gateway's certificate

{% hint style="warning" %}
The Gateway must have `clientAuth` set to `required` to enforce mTLS. Without this setting, the Gateway will reject any client connection that doesn't present a valid certificate.
{% endhint %}

### Gateway configuration

Configure mTLS for native Kafka APIs in the `kafka.ssl` section of `gravitee.yml`. The Gateway requires a keystore containing its private key and certificate, and a truststore containing the certificate authorities (CAs) that signed client certificates.

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee

    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee

    # Client authentication mode
    clientAuth: required             # required | request | none
```

#### Configuration parameters

<table>
  <thead>
    <tr>
      <th width="200">Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>keystore.type</code></td>
      <td>Keystore format. Supported values: <code>jks</code>, <code>pkcs12</code>, <code>pem</code></td>
    </tr>
    <tr>
      <td><code>keystore.path</code></td>
      <td>File path to the Gateway keystore</td>
    </tr>
    <tr>
      <td><code>keystore.password</code></td>
      <td>Password for the Gateway keystore</td>
    </tr>
    <tr>
      <td><code>truststore.type</code></td>
      <td>Truststore format. Supported values: <code>jks</code>, <code>pkcs12</code>, <code>pem</code></td>
    </tr>
    <tr>
      <td><code>truststore.path</code></td>
      <td>File path to the Gateway truststore</td>
    </tr>
    <tr>
      <td><code>truststore.password</code></td>
      <td>Password for the Gateway truststore</td>
    </tr>
    <tr>
      <td><code>clientAuth</code></td>
      <td>Client authentication mode. Set to <code>required</code> to enforce mTLS. The Gateway will reject any client connection without a valid certificate when set to <code>required</code>.</td>
    </tr>
  </tbody>
</table>

{% hint style="warning" %}
Set `clientAuth` to `required` to enforce mTLS authentication. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

### Kafka client configuration

Configure Kafka clients to use SSL with a client keystore and truststore. The client keystore contains the client's private key and certificate. The client truststore contains the CA that signed the Gateway certificate.

```properties

security.protocol=SSL



ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS



ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

### Required SSL files

<table>
  <thead>
    <tr>
      <th width="150">Component</th>
      <th width="200">File Type</th>
      <th>Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Gateway</td>
      <td>Keystore</td>
      <td>Gateway private key and certificate</td>
    </tr>
    <tr>
      <td>Gateway</td>
      <td>Truststore</td>
      <td>CAs that signed client certificates</td>
    </tr>
    <tr>
      <td>Kafka client</td>
      <td>Keystore</td>
      <td>Client private key and certificate</td>
    </tr>
    <tr>
      <td>Kafka client</td>
      <td>Truststore</td>
      <td>CA that signed the Gateway certificate</td>
    </tr>
  </tbody>
</table>

### Create an mTLS plan

After configuring SSL/mTLS on the Gateway and Kafka clients:

1. Add an mTLS plan to the Kafka API. The process is the same as for HTTP APIs.
2. Publish the plan.

{% hint style="warning" %}
Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published simultaneously.
{% endhint %}

### Create a subscription

After publishing the mTLS plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to HTTP APIs using mTLS.

### mTLS Plans for Kafka APIs

mTLS (mutual TLS) plans enable certificate-based authentication for Kafka APIs in APIM. This plan type provides strong client authentication by requiring both the Gateway and the Kafka client to present valid certificates during the TLS handshake.

#### How mTLS Differs from Standard TLS

Standard TLS for Kafka APIs:
- The client verifies the Gateway identity
- One-way authentication

mTLS for Kafka APIs:
- Both the client and the Gateway must present valid certificates
- The Kafka client must prove its identity using a client certificate
- Two-way authentication

mTLS is an additional security layer on top of the TLS already required for native Kafka APIs.

#### Technical Prerequisites

For mTLS to work correctly, both the Gateway and Kafka client must be configured with specific SSL components.

**Gateway Requirements**

The Kafka Gateway must be configured with:
- A keystore containing the Gateway private key and certificate
- A truststore containing the CAs that signed client certificates
- `clientAuth` enabled

**Client Requirements**

The Kafka client must be configured with:
- A keystore containing the client private key and certificate
- A truststore containing the CA that signed the Gateway certificate

#### Gateway Configuration

The mTLS configuration is defined in the `kafka.ssl` section of `gravitee.yml`:

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee
    
    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee
    
    # Client authentication mode
    clientAuth: required             # required | request | none
```

{% hint style="warning" %}
`clientAuth: required` is mandatory to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

#### Kafka Client Configuration

The Kafka client must be configured to use SSL with a client keystore:

```properties

security.protocol=SSL



ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS



ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

#### Creating and Publishing an mTLS Plan

Once the SSL/mTLS configuration is complete:

1. Add an mTLS plan to the Kafka API (same process as for a classic V4 API)
2. Publish the plan

{% hint style="warning" %}
**Plan Combination Restriction**

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. A Kafka API cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
{% endhint %}

#### Subscription Process

After publishing the mTLS plan:

1. Create an application that contains a client certificate
2. Create a subscription to the Kafka API using the mTLS plan

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to classic V4 APIs using mTLS.

#### Impacts and Benefits

**Impacts**
- Stricter SSL configuration requirements
- Mandatory client certificate management
- Limited plan combination options

**Benefits**
- Strong authentication of Kafka clients
- Improved security for Kafka traffic
- Alignment with existing APIM mTLS mechanisms

### mTLS plan support for Kafka APIs

mTLS plans are now supported for Kafka APIs in addition to classic and V4 HTTP APIs. The behavior is identical to classic V4 APIs.

#### Prerequisites

For mTLS to work correctly, the following configuration is required:

**Gateway configuration:**
- Keystore (Gateway private key and certificate)
- Truststore (CAs that signed client certificates)
- `clientAuth` enabled

**Kafka client configuration:**
- Keystore (client private key and certificate)
- Truststore (CA that signed the Gateway certificate)

#### Gateway configuration

The mTLS configuration is defined in the `kafka.ssl` section of `gravitee.yml`:

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee
    
    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee
    
    # Client authentication mode
    clientAuth: required             # required | request | none
```

{% hint style="warning" %}
`clientAuth: required` is mandatory to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

#### Kafka client configuration

The Kafka client must be configured to use SSL with a client keystore:

```properties

security.protocol=SSL



ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS



ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

#### APIM configuration

Once the SSL/mTLS configuration is complete:

1. Add an mTLS plan to the Kafka API (same as for a classic V4 API).
2. Publish the plan.

{% hint style="warning" %}
Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
{% endhint %}

#### Subscription

After publishing the plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to classic V4 APIs using mTLS.

### mTLS plan support

{% hint style="info" %}
mTLS plans are supported for Kafka APIs starting in APIM 4.10.
{% endhint %}

An mTLS plan provides mutual TLS authentication for Kafka APIs, allowing the Gateway to verify Kafka client identities using certificates. This strengthens security by adding an additional authentication layer on top of the TLS already required for native Kafka APIs.

#### Prerequisites

For mTLS to work correctly, the following configuration is required:

**Kafka Gateway configuration:**
- A keystore containing the Gateway private key and certificate
- A truststore containing the CAs that signed client certificates
- `clientAuth` enabled

**Kafka client configuration:**
- A keystore containing the client private key and certificate
- A truststore containing the CA that signed the Gateway certificate

#### Gateway configuration

The mTLS configuration is defined in the `kafka.ssl` section of `gravitee.yml`:

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee
    
    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee
    
    # Client authentication mode
    clientAuth: required             # required | request | none
```

{% hint style="warning" %}
`clientAuth: required` is mandatory to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

#### Kafka client configuration

The Kafka client must be configured to use SSL with a client keystore:

```properties

security.protocol=SSL



ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS



ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

#### Creating an mTLS plan

Once the SSL/mTLS configuration is complete:

1. Add an mTLS plan to the Kafka API (same as for a classic V4 API).
2. Publish the plan.

{% hint style="danger" %}
**Plan combination restriction**

Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.

A Kafka API cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
{% endhint %}

#### Subscription

After publishing the plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to classic V4 APIs using mTLS.