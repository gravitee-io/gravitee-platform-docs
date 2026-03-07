### Overview

mTLS (mutual TLS) authentication enables certificate-based client authentication for Native Kafka APIs in Gravitee APIM. Clients present X.509 certificates during the TLS handshake, and the gateway validates these certificates before allowing access to Kafka topics. This feature extends the existing mTLS policy to support both HTTP and Kafka protocol authentication.

### Key Concepts

#### Plan Type Mutual Exclusion

Native Kafka APIs enforce strict separation between authentication strategies. A published API cannot mix Keyless plans with mTLS or authentication plans (OAuth2, JWT, API Key), and vice versa. Multiple plans of the same authentication category may coexist (e.g., multiple mTLS plans or multiple OAuth2 plans), but cross-category combinations are blocked at publish time.

| Plan Category | Can Coexist With | Cannot Coexist With |
|:--------------|:-----------------|:--------------------|
| Keyless | Other Keyless plans | mTLS, OAuth2, JWT, API Key |
| mTLS | Other mTLS plans | Keyless, OAuth2, JWT, API Key |
| Authentication (OAuth2, JWT, API Key) | Other authentication plans | Keyless, mTLS |

#### Certificate Validation Flow

The gateway validates client certificates in three stages:

1. Verify a TLS session exists
2. Extract peer certificates from the session
3. Confirm the certificate array is non-empty

Failures at any stage return specific error keys:

* `SSL_SESSION_REQUIRED` — No TLS session found
* `CLIENT_CERTIFICATE_INVALID` — Peer certificate extraction failed
* `CLIENT_CERTIFICATE_MISSING` — Certificate array is null or empty

On success, the gateway extracts the certificate's MD5 hash as the security token for subscription matching.

#### Kafka vs HTTP Authentication

The mTLS policy implements both `HttpSecurityPolicy` and `KafkaSecurityPolicy` interfaces. For HTTP requests, the policy interrupts with HTTP 401 on validation failure. For Kafka connections, the policy throws `KafkaServerAuthenticationException` and closes the socket. Kafka authentication occurs once per connection and sets a `plainTextAuthenticated` flag to skip re-validation on subsequent frames.

### Prerequisites

* Gravitee API Management 4.10.1 or later
* `gravitee-policy-mtls` 2.0.0-alpha.2 or later
* `gravitee-reactor-native-kafka` 5.1.0-alpha.3 or later
* A Java KeyStore (JKS) truststore containing the CA certificate that signed client certificates
* Client certificates signed by the trusted CA
