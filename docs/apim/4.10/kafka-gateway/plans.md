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

<table><thead><tr><th width="201">Plan</th><th>Corresponding Kafka Authentication</th></tr></thead><tbody><tr><td>Keyless (public)</td><td>PLAINTEXT</td></tr><tr><td>API Key</td><td>The API key is used as the password, and the md5 hash of the API key is used as the username, as part of the SASL/SSL with SASL PLAIN authentication method.</td></tr><tr><td>JWT</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication, where the JWT is used as the OAuth token.</td></tr><tr><td>OAuth2</td><td>Equivalent to SASL/SSL with SASL OAUTHBEARER authentication.</td></tr><tr><td>mTLS</td><td>Mutual TLS authentication where both the Kafka client and Gateway present valid certificates.</td></tr></tbody></table>

To authenticate users, each plan must include at least one security type. A security type is a policy that is integrated directly into a plan. Once a plan is created, the security type cannot be changed. Also, your Kafka APIs cannot have conflicting authentication.

## Plan restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans published together. Specifically, you cannot simultaneously publish:

* A Keyless plan
* An mTLS plan
* An authentication plan (OAuth2, JWT, or API Key)

This restriction ensures consistent authentication behavior across all published plans for a Kafka API. However, you can have multiple authentication plans for a Kafka API (for example, OAuth2 and JWT).

{% hint style="warning" %}
If you need to add an mTLS plan to a Kafka API that already has a Keyless or authentication plan published, you must first deprecate or close the conflicting plan before publishing the mTLS plan.
{% endhint %}

## Plan stages

A plan can exist in one of four stages:

* STAGING. This is the draft mode of a plan, where it can be configured but won't be accessible to users.
* PUBLISHED. API consumers can view a published plan on the Developer Portal. Once subscribed, they can use it to consume the API. A published plan can still be edited.
* DEPRECATED. A deprecated plan won't be available on the Developer Portal and API consumers won't be able to subscribe to it. This cannot be undone. Existing subscriptions are not impacted, giving current API consumers time to migrate without breaking their application.
* CLOSED. Once a plan is closed, all associated subscriptions are closed. API consumers subscribed to this plan won't be able to use the API. This cannot be undone.

Depending on the stage it's in, a plan can be edited, published, deprecated, or closed. See [this](create-and-configure-kafka-apis/configure-kafka-apis/consumers.md) documentation for specific instructions.

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

## mTLS plans

{% hint style="info" %}
mTLS plan behavior for Kafka APIs is identical to classic V4 APIs. For detailed configuration and subscription workflows, see [mtls.md](../secure-and-expose-apis/plans/mtls.md "mention").
{% endhint %}

Mutual TLS (mTLS) for native Kafka APIs is an additional security layer on top of the TLS already required for native Kafka APIs. With mTLS enabled, both the Kafka Gateway and the Kafka client must present valid certificates to establish a connection. The Kafka client must prove its identity using a client certificate, allowing the Gateway to verify client identities.

### Before: TLS only

- The Kafka client verifies the Gateway's identity using the Gateway's certificate.
- The Gateway does not verify the client's identity.

### After: TLS + mTLS

- The Kafka client verifies the Gateway's identity.
- The Gateway verifies the Kafka client's identity using the client's certificate.
- Both parties must present valid certificates signed by trusted certificate authorities (CAs).

### Technical prerequisites

For mTLS to work correctly, both the Kafka Gateway and Kafka clients must be configured with the appropriate keystores and truststores.

#### Gateway requirements

The Kafka Gateway must be configured with:

- **Keystore**: Contains the Gateway's private key and certificate
- **Truststore**: Contains the CAs that signed client certificates
- **clientAuth**: Must be enabled to enforce client certificate validation

#### Client requirements

The Kafka client must be configured with:

- **Keystore**: Contains the client's private key and certificate
- **Truststore**: Contains the CA that signed the Gateway's certificate

### Gateway configuration (gravitee.yml)

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

### Kafka client configuration

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

### Adding an mTLS plan

Once SSL/mTLS configuration is complete, you must add an mTLS plan to the Kafka API. The process is the same as for classic V4 APIs.

### Subscription workflow

After publishing the mTLS plan:

1. Create an application that contains a client certificate. The client certificate is used by APIM to identify the application during the Kafka connection.
2. Create a subscription to the Kafka API using the mTLS plan.

{% hint style="info" %}
The behavior is identical to classic V4 APIs using mTLS. For detailed instructions on creating applications with client certificates and managing subscriptions, see [mtls.md](../secure-and-expose-apis/plans/mtls.md "mention").
{% endhint %}

### Benefits

mTLS for native Kafka APIs provides the following security and operational benefits:

- **Strong authentication of Kafka clients**: Client certificates verify the identity of connecting applications.
- **Improved security for Kafka traffic**: mTLS encrypts and authenticates all Kafka connections.
- **Alignment with existing APIM mTLS mechanisms**: The behavior is identical to classic V4 APIs using mTLS.

### Impacts

Enabling mTLS for native Kafka APIs introduces the following operational impacts:

- **Stricter SSL configuration**: Both the Gateway and Kafka clients must be configured with SSL/mTLS settings, including keystores and truststores.
- **Mandatory client certificate management**: Applications must provide valid client certificates to establish connections.
- **Limited plan combination options**: Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published simultaneously.

### Summary

The following steps summarize the complete mTLS workflow for native Kafka APIs:

1. Configure SSL/mTLS on the Gateway by defining the `kafka.ssl` section in `gravitee.yml`, including keystore, truststore, and `clientAuth: required`.
2. Configure the Kafka client with SSL settings, including the client keystore and truststore.
3. Add an mTLS plan to the Kafka API in APIM.
4. Publish the mTLS plan.
5. Create an application that contains a client certificate.
6. Create a subscription to the Kafka API using the mTLS plan.
7. The client certificate is used by APIM to identify the application during the Kafka connection.
