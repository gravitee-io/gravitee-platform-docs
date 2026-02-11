## mTLS for Native Kafka APIs: Concept and Security Model

Mutual TLS (mTLS) extends standard TLS by requiring both parties in a connection to authenticate using certificates. In a standard TLS connection, only the server presents a certificate to prove its identity. With mTLS, the client must also present a valid certificate.

For native Kafka APIs in APIM, mTLS adds a security layer on top of the TLS already required for Kafka connections.


**TLS only:**
- Client verifies the Gateway identity
- Gateway does not verify client identity

**TLS + mTLS:**
- Both client and Gateway present valid certificates
- Gateway verifies client identity using the client certificate
- Client verifies Gateway identity using the Gateway certificate


mTLS for native Kafka APIs provides:
- Strong authentication of Kafka clients
- Certificate-based client identification
- Proper subscription resolution for metrics and analytics
- Alignment with existing APIM mTLS mechanisms for HTTP/Message APIs


Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.

You cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)


The mTLS behavior for native Kafka APIs works the same way as for HTTP/Message APIs:

1. Application subscribes to an mTLS plan on a Kafka API
2. Application provides a PEM client certificate
3. Certificate is associated with the subscription
4. At runtime:
    - Client initiates TLS connection with client certificate
    - Gateway validates certificate against known subscription certificates
    - On match: connection authorized, context populated with plan/app/subscription
    - Metrics and analytics reflect the resolved subscription


Before mTLS plan support, the workaround was to:
- Enable mTLS at Gateway listener level
- Configure API as Keyless
- Use `context.ssl.client.*` EL in policies

This approach had significant limitations:
- No subscription resolution → metrics show ANONYMOUS
- No application/plan/subscription attribution in analytics
- Cannot combine with other plan security types


## Impacts and Benefits

### Impacts

Enabling mTLS for native Kafka APIs introduces the following changes:

- **Stricter SSL configuration**: Both Gateway and Kafka clients must be configured with keystores and truststores.
- **Mandatory client certificate management**: Applications must provide valid client certificates to establish connections.
- **Limited plan combination options**: Kafka APIs cannot publish Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) simultaneously.

### Benefits

mTLS for native Kafka APIs provides:

- **Strong authentication of Kafka clients**: Certificate-based verification ensures only authorized clients can connect.
- **Proper subscription resolution**: Metrics and analytics correctly attribute traffic to the resolved subscription, application, and plan (eliminating ANONYMOUS metrics).
- **Improved security for Kafka traffic**: Mutual authentication adds a security layer on top of standard TLS.
- **Alignment with existing APIM mTLS mechanisms**: Kafka APIs use the same mTLS behavior as HTTP/Message APIs.
