## Overview

mTLS (mutual TLS) for native Kafka APIs adds an additional security layer on top of the TLS already required for native Kafka APIs. With mTLS enabled, both the Kafka client and the Gateway must present valid certificates during the connection handshake.

### TLS vs. mTLS

**TLS only (default)**

- The client verifies the Gateway identity.
- The Gateway does not verify the client identity.

**TLS + mTLS**

- Both the client and the Gateway must present valid certificates.
- The Kafka client must prove its identity using a client certificate.
- The Gateway validates the client certificate against known subscription certificates.

### How mTLS Works for Native Kafka APIs

The mTLS behavior for native Kafka APIs works the same way as for HTTP/Message APIs:

1. An application subscribes to an mTLS plan on a Kafka API.
2. The application provides a PEM client certificate.
3. The certificate is associated with the subscription.
4. At runtime, the client initiates a TLS connection with the client certificate.
5. The Gateway validates the certificate against known subscription certificates.
6. On match, the connection is authorized and the context is populated with plan, application, and subscription information.
7. Metrics and analytics reflect the resolved subscription.

### Benefits

- **Strong authentication**: Kafka clients are authenticated using certificates.
- **Subscription resolution**: Metrics and analytics correctly attribute traffic to the application, plan, and subscription.
- **Alignment with existing APIM mechanisms**: mTLS for native Kafka APIs uses the same subscription and certificate management as HTTP/Message APIs.

### Limitations

Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together. You cannot expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)