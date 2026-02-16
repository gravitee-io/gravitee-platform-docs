---
description: Configuration guide for kafka gateway.
metaLinks:
  alternates:
    - ./
---

# Kafka Gateway

The Gravitee Kafka Gateway applies Gravitee's API management capabilities directly to native Kafka to address the security, cost, and scalability issues that exist in traditional Kafka deployments.

With the Kafka Gateway, you can apply [policies](create-and-configure-kafka-apis/configure-kafka-apis/policies.md) on native Kafka topics at runtime. These policies are designed for Kafka-specific use cases. For example, you can easily restrict topic access to approved tenants or require client certificates for mTLS as an additional security layer.

The Kafka Gateway supports mTLS authentication for native Kafka APIs, allowing the Gateway to verify Kafka client identities using certificates. This provides strong authentication and improved security for Kafka traffic.

## mTLS authentication support

The Kafka Gateway supports mTLS plans for native Kafka APIs. mTLS (mutual TLS) is an additional security layer that allows the Gateway to verify Kafka client identities using certificates. This works the same way as for classic APIs.

With mTLS enabled:
- Both the client and the Gateway must present valid certificates
- The Kafka client must prove its identity using a client certificate
- The Gateway validates the certificate against known subscription certificates

mTLS requires SSL/mTLS configuration on both the Gateway and Kafka clients. For configuration details, see [Configure the Kafka Client & Gateway](configure-the-kafka-client-and-gateway.md).

<!-- GAP: Link to mTLS plan configuration documentation if available -->

## Developer Portal integration

The Kafka Gateway is linked to Gravitee's Developer Portal to facilitate topic availability and knowledge sharing. For example, you can publish [documentation](create-and-configure-kafka-apis/configure-kafka-apis/documentation.md) on Kafka topics, infrastructure, and client connections, or use a self-service mechanism to manage [subscriptions](subscriptions.md) to Kafka topics.

## Native Kafka protocol support

The Kafka Gateway natively supports the Kafka protocol and is treated like a traditional Kafka broker by consumers and producers. As a Gravitee user, you expose Kafka topics using the Gravitee concept of an API, called a [Kafka API](create-and-configure-kafka-apis/create-kafka-apis.md#introduction). However, consumers and producers see a regular client connection to a Kafka bootstrap server, so don't need to change existing application logic.

You can expose multiple Kafka topics within a single Kafka API, and expose multiple Kafka APIs through the Gravitee Kafka Gateway. Using the Kafka Gateway, data is processed in real time, and virtual topics and partitions enable scalable, cost-effective deployments.

## Learn more

To learn more about the Kafka Gateway, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Configure the Kafka Client &#x26; gateway</td><td><a href="configure-the-kafka-client-and-gateway.md">configure-the-kafka-client-and-gateway.md</a></td></tr><tr><td>Create &#x26; Configure Kafka APIs</td><td><a href="create-and-configure-kafka-apis/">create-and-configure-kafka-apis</a></td></tr><tr><td>Plans</td><td><a href="plans.md">plans.md</a></td></tr><tr><td>Applications</td><td><a href="applications.md">applications.md</a></td></tr><tr><td>Subscriptions</td><td><a href="subscriptions.md">subscriptions.md</a></td></tr><tr><td>Other ways Gravitee supports Kafka</td><td><a href="other-ways-gravitee-supports-kafka.md">other-ways-gravitee-supports-kafka.md</a></td></tr></tbody></table>

### mTLS for Native Kafka APIs

mTLS (mutual TLS) authentication for native Kafka APIs strengthens security by requiring both the Gateway and Kafka clients to present valid certificates. This additional security layer builds on the TLS already required for native Kafka APIs.

#### Overview

mTLS for native Kafka APIs works the same way as for classic APIs. Before enabling mTLS, TLS is used and only the client verifies the Gateway identity. After enabling mTLS, both the client and the Gateway must present valid certificates, and the Kafka client must prove its identity using a client certificate.

#### Prerequisites

For mTLS to work correctly, the Kafka Gateway must be configured with:

- A keystore (Gateway private key and certificate)
- A truststore (CAs that signed client certificates)
- `clientAuth` enabled

The Kafka client must be configured with:

- A keystore (client private key and certificate)
- A truststore (CA that signed the Gateway certificate)

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

#### mTLS Plan Configuration

Once the SSL/mTLS configuration is complete:

1. Add an mTLS plan to the Kafka API (same as for a classic v4 API).
2. Publish the plan.

{% hint style="warning" %}
Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together. Kafka APIs can't expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
{% endhint %}

#### Subscription

After publishing the plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to classic v4 APIs using mTLS.

#### Impacts and Benefits

**Impacts:**

- Stricter SSL configuration
- Mandatory client certificate management
- Limited plan combination options

**Benefits:**

- Strong authentication of Kafka clients
- Improved security for Kafka traffic
- Alignment with existing APIM mTLS mechanisms