---
description: Guide on applying policies related to mtls.
metaLinks:
  alternates:
    - mtls.md
---

# mTLS

### Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse |
| --------- | ---------- |
| X         |            |

### Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `mtls` policy to verify a client certificate exists as part of the request.

This policy does not ensure that certificates are valid, since it is done directly by the server.

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 2.x            | 4.10 to latest |
| 1.x            | 4.5 to 4.9    |

{% hint style="info" %}
**Kafka Native API Support**

mTLS policy version 2.0.0-alpha.2 or later supports Kafka Native APIs and is compatible with APIM 4.10+. The policy validates certificates for both HTTP and Kafka protocols using unified logic. Version 1.x does not support Kafka Native APIs.

mTLS for Kafka Native APIs is an Enterprise Edition feature.
{% endhint %}

### Errors <a href="#user-content-errors" id="user-content-errors"></a>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Entrypoints > Response Templates** menu).

The error keys sent by this policy are as follows:

| Key                          | Parameters |
| ---------------------------- | ---------- |
| CLIENT\_CERTIFICATE\_MISSING | -          |
| CLIENT\_CERTIFICATE\_INVALID | -          |
| SSL\_SESSION\_REQUIRED       | -          |

### Kafka Native API Support

The mTLS policy validates client certificates for both HTTP and Kafka protocols using unified certificate validation logic. Version 2.0.0-alpha.2 or later is required for Kafka Native API support and is compatible with APIM 4.10+.

The policy implements both `HttpSecurityPolicy` and `KafkaSecurityPolicy` interfaces. For Kafka connections, the `authenticate(KafkaConnectionContext)` method extracts the TLS session from the connection context and delegates to the same certificate validation logic used for HTTP requests.

{% hint style="info" %}
mTLS for Kafka Native APIs is an Enterprise Edition feature.
{% endhint %}

#### Prerequisites

- Gravitee API Management 4.10 or later
- mTLS policy version 2.0.0-alpha.2 or later
- Kafka Native API with Kafka listener type configured
- Server truststore containing the CA that signed client certificates
- Client certificates signed by a trusted CA

#### Gateway Configuration

Configure the Gateway to require client certificates and specify the truststore containing trusted CAs. The `clientAuth` property must be set to `required` to enforce certificate validation.

```yaml
kafka:
  ssl:
    clientAuth: required
    truststore:
      type: jks
      password: gravitee
      path: /path/to/server.truststore.jks
```

**Kafka SSL Settings**

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Client certificate requirement mode | `required` |
| `kafka.ssl.truststore.type` | Truststore format | `jks` |
| `kafka.ssl.truststore.password` | Truststore password | `gravitee` |
| `kafka.ssl.truststore.path` | Absolute path to truststore file | `/path/to/server.truststore.jks` |

<!-- GAP: No documentation of how to configure server.truststore.jks or generate client certificates -->
<!-- GAP: No specification of supported certificate formats beyond JKS keystores -->

#### Creating an mTLS Plan for Kafka APIs

1. Navigate to the API's Plans section in the Console UI and select **Create Plan**.
2. Choose **mTLS** from the security type dropdown.
3. Configure plan details such as name, description, and rate limits.
4. When publishing the plan, the Console validates that no conflicting plan types are already published.

If a Keyless or authentication plan exists, the system displays a confirmation dialog: "A Keyless or authentication plan is already published for the Native API. mTLS plans cannot be combined with Keyless or authentication plans." Confirm to auto-close conflicting plans and publish the mTLS plan.

**Plan Type Mutual Exclusion**

Kafka Native APIs enforce strict segregation of plan types when published. Multiple plans of the same type are allowed.

| Plan Type Being Published | Conflicts With | Allowed With |
|:--------------------------|:---------------|:-------------|
| Keyless | mTLS, Authentication (OAuth2/JWT/API Key) | Other Keyless plans |
| mTLS | Keyless, Authentication (OAuth2/JWT/API Key) | Other mTLS plans |
| Authentication (OAuth2/JWT/API Key) | Keyless, mTLS | Other Authentication plans |

#### Creating a Subscription with mTLS

API consumers must provide a valid client certificate when subscribing to an mTLS plan.

1. In the subscription request, include the Base64-encoded client certificate in the `clientCertificate` field.
2. The Gateway calculates the MD5 hash of the certificate and uses it as the security token for subscription lookup.
3. When the client connects, the Gateway validates the presented certificate against the subscription's stored certificate.

Ensure the client certificate is signed by a CA present in the Gateway's truststore.

#### Client Configuration

Kafka clients connecting to mTLS-protected APIs must configure SSL properties to present their certificate during the TLS handshake.

```properties
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.truststore.location=/path/to/client.truststore.jks
```

**Client SSL Properties**

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to client keystore containing certificate | `/path/to/client.keystore.jks` |
| `ssl.keystore.password` | Keystore password | `gravitee` |
| `ssl.truststore.location` | Path to client truststore containing Gateway CA | `/path/to/client.truststore.jks` |

#### Certificate Validation

The Gateway validates client certificates by checking the TLS session, extracting peer certificates, and verifying the certificate chain. Validation failures return specific error keys:

- `SSL_SESSION_REQUIRED`: No TLS session exists
- `CLIENT_CERTIFICATE_INVALID`: SSLPeerUnverifiedException occurred
- `CLIENT_CERTIFICATE_MISSING`: Certificate array is empty

The subscription must include a Base64-encoded client certificate, with the certificate MD5 hash used as the security token for subscription lookup.

<!-- GAP: No explanation of certificate validation chain (CA requirements, expiration handling) -->

#### Restrictions

- mTLS plans are only available for Kafka listener types.
- PUSH plan types remain blocked for Kafka APIs regardless of mTLS support.
- Only one plan type category (Keyless, mTLS, or Authentication) can be published at a time for a Kafka API.
- Publishing a conflicting plan type requires manual confirmation and auto-closes existing incompatible plans.
- Client certificates must be Base64-encoded when included in subscription requests.
- The Gateway uses MD5 hashing for certificate-based subscription lookup.