mTLS (mutual TLS) for native Kafka APIs is an additional security layer that enables the Gateway to verify Kafka client identities using certificates. This strengthens authentication beyond standard TLS, which only verifies the Gateway's identity.

The mTLS behavior for native Kafka APIs works the same way as for classic APIs.


**TLS only (before mTLS)**
- The client verifies the Gateway identity
- One-way authentication

**TLS + mTLS (after mTLS)**
- Both the client and the Gateway must present valid certificates
- The Kafka client must prove its identity using a client certificate
- Two-way authentication

mTLS is an additional security layer on top of the TLS already required for native Kafka APIs.


mTLS for native Kafka APIs provides:

- **Strong authentication of Kafka clients**: Client identity is verified using certificates.
- **Improved security for Kafka traffic**: Mutual TLS authentication adds an additional security layer on top of standard TLS.
- **Alignment with existing APIM mTLS mechanisms**: The behavior is identical to classic V4 APIs using mTLS.


Enabling mTLS for native Kafka APIs introduces the following operational impacts:

- **Stricter SSL configuration**: Both the Gateway and Kafka clients must be configured with keystores and truststores.
- **Mandatory client certificate management**: Applications must provide valid client certificates to establish connections.
- **Limited plan combination options**: Kafka APIs cannot expose simultaneously a Keyless plan, an mTLS plan, and an authentication plan (OAuth2, JWT, API Key).


Before configuring mTLS for native Kafka APIs, ensure the following technical prerequisites are met.


The Kafka Gateway must be configured with:
- **Keystore**: Contains the Gateway private key and certificate
- **Truststore**: Contains the CAs that signed client certificates
- **clientAuth enabled**: Required to enforce mTLS


The Kafka client must be configured with:
- **Keystore**: Contains the client private key and certificate
- **Truststore**: Contains the CA that signed the Gateway certificate

<!-- GAP: SSL Files table referenced in draft but table content not provided in source material -->


Configure the Kafka client to use SSL with a client keystore. The following properties are required:

```properties
security.protocol=SSL

ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```


Once the SSL/mTLS configuration is complete:

1. Add an mTLS plan to the Kafka API. The process is the same as for a classic V4 API.
2. Publish the plan.

{% hint style="warning" %}
Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
{% endhint %}


After publishing the mTLS plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection.