## Overview

mTLS (mutual TLS) plans for native Kafka APIs enable certificate-based client authentication and proper subscription resolution. This feature aligns Kafka native APIs with the mTLS behavior already available for HTTP and Message APIs.

### What mTLS adds to native Kafka APIs

mTLS extends the existing TLS security layer by requiring both the Gateway and the Kafka client to present valid certificates:

- **TLS only**: The client verifies the Gateway identity
- **TLS + mTLS**: Both the client and the Gateway must present valid certificates, and the Kafka client must prove its identity using a client certificate

### Why mTLS plans are required

Without mTLS plans, native Kafka APIs cannot resolve subscriptions based on client certificates. This limitation affects:

- **Metrics attribution**: Connections appear as ANONYMOUS in analytics
- **Subscription tracking**: No application, plan, or subscription dimensions in metrics
- **Security enforcement**: Cannot combine certificate-based authentication with other plan security types

The current workaround (enabling mTLS at the Gateway listener level with a Keyless plan and using `context.ssl.client.*` EL in policies) does not resolve subscriptions, making it unsuitable for production environments that require accurate metrics and subscription tracking.

### How mTLS plans work

The subscription and runtime flows for native Kafka APIs match the behavior of HTTP mTLS plans:

**Subscription flow**:
1. Application subscribes to an mTLS plan on a Kafka API
2. Application provides a PEM client certificate
3. Certificate is associated with the subscription

**Runtime flow**:
1. Client initiates a TLS connection with a client certificate
2. Gateway validates the certificate against known subscription certificates
3. On match: connection is authorized, and the context is populated with plan, application, and subscription details
4. Metrics and analytics reflect the resolved subscription