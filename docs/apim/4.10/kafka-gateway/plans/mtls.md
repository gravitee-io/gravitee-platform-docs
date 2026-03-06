### What is mTLS authentication for Kafka native APIs?

mTLS authentication for Kafka native APIs is certificate-based client authentication that validates client certificates during connection establishment. The gateway extracts the TLS session, verifies peer certificates, and computes an MD5 digest of the certificate for subscription matching.

### Plan security mutual exclusion

Kafka APIs enforce a three-way mutual exclusion rule for published plans. Only one authentication category can be active at a time:

* **Keyless**: No authentication
* **mTLS**: Certificate-based authentication
* **Authentication**: OAuth2, JWT, or API Key

When you publish a plan in one category, all published plans in other categories are automatically closed.

| Plan Category | Conflicts With | Allowed Alongside |
|:--------------|:---------------|:------------------|
| Keyless | mTLS, Authentication | Other Keyless plans |
| mTLS | Keyless, Authentication | Other mTLS plans |
| Authentication (OAuth2, JWT, API Key) | Keyless, mTLS | Other Authentication plans |

### Certificate validation

The gateway validates client certificates during connection establishment:

1. Extract the TLS session from the Kafka connection context
2. Verify that peer certificates are present
3. Compute an MD5 digest of the certificate for subscription matching

Validation failures return specific error keys:

| Error Key | Condition |
|:----------|:----------|
| `SSL_SESSION_REQUIRED` | TLS session is null |
| `CLIENT_CERTIFICATE_MISSING` | Peer certificates array is null or empty |
| `CLIENT_CERTIFICATE_INVALID` | Certificate verification fails |

### Security token extraction

After successful certificate validation, the gateway extracts a security token by computing the MD5 digest of the client certificate's encoded bytes. This digest serves as the client identifier for subscription lookup and authorization.

If certificate encoding fails, the gateway returns an invalid security token of type `CERTIFICATE`.

### Restrictions

* You can't publish plans from different authentication categories simultaneously
* Publishing a plan in one category automatically closes all published plans in other categories
* PUSH plans are not available for Kafka native APIs
* Client certificates must be signed by a CA in the gateway's truststore
* Certificate validation occurs during the TLS handshake before Kafka protocol messages are exchanged
* Subscriptions must include the client certificate in the `clientCertificate` field
* The MD5 digest of the subscription's client certificate must match the digest computed from the TLS session
* Certificate rotation requires updating the subscription with the new certificate

## Overview

Kafka native APIs now support mutual TLS (mTLS) authentication, enabling certificate-based client authentication for Kafka connections. This feature allows administrators to enforce client certificate validation at the gateway level, providing an alternative to keyless or token-based authentication schemes. mTLS plans operate under mutual exclusion rules with other authentication types to ensure consistent security posture across published plans.
