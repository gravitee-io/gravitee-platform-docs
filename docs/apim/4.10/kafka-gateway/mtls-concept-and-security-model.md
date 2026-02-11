## mTLS for Native Kafka APIs: Concept and Security Model

### What is mTLS?

Mutual TLS (mTLS) extends standard TLS by requiring both parties in a connection to authenticate using certificates. In a standard TLS connection, only the server presents a certificate to prove its identity. With mTLS, the client must also present a valid certificate.

For native Kafka APIs in APIM, mTLS adds a security layer on top of the TLS already required for Kafka connections.

### TLS vs mTLS

**TLS only:**
- Client verifies the Gateway identity
- Gateway does not verify client identity

**TLS + mTLS:**
- Both client and Gateway present valid certificates
- Gateway verifies client identity using the client certificate
- Client verifies Gateway identity using the Gateway certificate

### Security Benefits

mTLS for native Kafka APIs provides:
- Strong authentication of Kafka clients
- Certificate-based client identification
- Proper subscription resolution for metrics and analytics
- Alignment with existing APIM mTLS mechanisms for HTTP/Message APIs

### Plan Restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.

You cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)

### How mTLS Works for Kafka APIs

The mTLS behavior for native Kafka APIs works the same way as for HTTP/Message APIs:

1. Application subscribes to an mTLS plan on a Kafka API
2. Application provides a PEM client certificate
3. Certificate is associated with the subscription
4. At runtime:
    - Client initiates TLS connection with client certificate
    - Gateway validates certificate against known subscription certificates
    - On match: connection authorized, context populated with plan/app/subscription
    - Metrics and analytics reflect the resolved subscription