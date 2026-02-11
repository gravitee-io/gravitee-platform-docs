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

{% hint style="info" %}
mTLS plans are not yet supported for Kafka APIs.
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
## mTLS Plans

mTLS plans are supported for Kafka native APIs. An mTLS plan allows the Gateway to verify Kafka client identities using certificates, providing strong authentication and enabling proper subscription resolution for metrics and analytics.


mTLS for Kafka APIs works the same way as for HTTP/Message APIs:

1. An application subscribes to an mTLS plan on a Kafka API
2. The application provides a PEM client certificate
3. The certificate is associated with the subscription
4. At runtime, the client initiates a TLS connection with the client certificate
5. The Gateway validates the certificate against known subscription certificates
6. On match, the connection is authorized and the context is populated with plan/app/subscription information
7. Metrics and analytics reflect the resolved subscription

mTLS adds mutual TLS authentication on top of the TLS already required for native Kafka APIs. Both the client and the Gateway must present valid certificates.


Before configuring an mTLS plan, ensure:

- The Kafka Gateway is configured with a keystore (Gateway private key + certificate) and truststore (CAs that signed client certificates)
- `clientAuth` is enabled in the Gateway configuration
- Client applications have a keystore (client private key + certificate) and truststore (CA that signed the Gateway certificate)


The Kafka Gateway must be configured with SSL/mTLS settings in `gravitee.yml`:

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

`clientAuth: required` is mandatory to enforce mTLS. The Gateway will reject any client connection without a valid certificate.


To create and publish an mTLS plan:

1. Add an mTLS plan to the Kafka API (same process as for a V4 API)
2. Publish the plan
3. Redeploy the API

{% hint style="warning" %}
Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together. You cannot expose a Keyless plan, an mTLS plan, and an authentication plan simultaneously on the same Kafka API.
{% endhint %}


After publishing the mTLS plan:

1. Create an application that contains a client certificate
2. Create a subscription to the Kafka API using the mTLS plan

The client certificate is used by APIM to identify the application during the Kafka connection.


Kafka clients must be configured to use SSL with a client keystore. Example configuration:

```properties

security.protocol=SSL


ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS


ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```


- Strong authentication of Kafka clients
- Proper subscription resolution for metrics and analytics
- Correct attribution of plan/application/subscription dimensions in analytics
- Improved security for Kafka traffic