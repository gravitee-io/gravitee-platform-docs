Mutual TLS (mTLS) for native Kafka APIs adds certificate-based client authentication to the existing TLS encryption layer. This strengthens security by requiring both the Gateway and the Kafka client to present valid certificates during connection establishment.

mTLS for native Kafka APIs works the same way as for classic APIs in APIM.

**Before (TLS only)**

- The client verifies the Gateway identity
- One-way authentication

**After (TLS + mTLS)**

- Both the client and the Gateway must present valid certificates
- The Kafka client must prove its identity using a client certificate
- Two-way authentication

mTLS is an additional security layer on top of the TLS already required for native Kafka APIs.


Enabling mTLS for native Kafka APIs introduces the following operational changes:

- **Stricter SSL configuration**: The Gateway requires both a keystore and truststore, with `clientAuth` set to `required`.
- **Mandatory client certificate management**: Applications must provide valid client certificates to establish connections.
- **Limited plan combination options**: Kafka APIs cannot publish Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) simultaneously.


mTLS provides the following security and operational improvements:

- **Strong authentication of Kafka clients**: The Gateway verifies client identities using certificates, preventing unauthorized access.
- **Improved security for Kafka traffic**: Mutual authentication ensures both the Gateway and client prove their identities.
- **Alignment with existing APIM mTLS mechanisms**: The behavior matches classic V4 APIs, ensuring consistent subscription resolution and metrics attribution.


For mTLS to work correctly, both the Gateway and Kafka clients must be configured with keystores and truststores.

**Gateway requirements:**

- Keystore containing the Gateway private key and certificate
- Truststore containing the certificate authorities (CAs) that signed client certificates
- `clientAuth` enabled in the Gateway configuration

**Kafka client requirements:**

- Keystore containing the client private key and certificate
- Truststore containing the CA that signed the Gateway certificate


mTLS plans are added to Kafka APIs the same way as for classic V4 APIs. After configuring the plan, you must publish it before applications can subscribe.

{% hint style="warning" %}
**Plan combination restriction**

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.
{% endhint %}


To subscribe to an mTLS plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection.


Kafka clients connecting to an mTLS-enabled Gateway must be configured to use SSL and provide both a truststore and a keystore.

Set the security protocol to SSL:

```properties
security.protocol=SSL
```

The truststore contains the CA that signed the Gateway certificate. Configure the following properties:

```properties
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS
```

The keystore contains the client private key and certificate. Configure the following properties:

```properties
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

Complete example of Kafka client properties for mTLS:

```properties
security.protocol=SSL

ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```