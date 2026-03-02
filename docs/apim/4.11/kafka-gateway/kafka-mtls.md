## Overview

Gravitee API Management supports **mTLS (mutual TLS) authentication** as a plan security type for Kafka Native APIs. mTLS enables certificate-based mutual authentication between Kafka clients and the Gravitee Kafka Gateway.

In mTLS authentication:
- The **gateway** presents its server certificate to the Kafka client
- The **Kafka client** presents its client certificate to the gateway
- The gateway verifies the client certificate against a configured truststore
- The client certificate is matched against a subscription's registered certificate to authorize access

Previously, mTLS plans were only supported for HTTP-based APIs. This update makes mTLS a first-class plan type for the Kafka Native Gateway, enabling organizations that require strict certificate-based authentication to use the Kafka Native Gateway securely.

**Supported versions:**
- APIM 4.10+
- mTLS Policy 2.x

## Plan Security Type Mutual Exclusion

Kafka Native APIs enforce mutual exclusion between three categories of plan security types:

| Category | Security Types | Description |
|:---------|:---------------|:------------|
| **Keyless** | Keyless | No authentication required |
| **mTLS** | mTLS | Certificate-based mutual authentication |
| **Authentication** | API Key, OAuth2, JWT | Token or key-based authentication |

These categories are **mutually exclusive**. Only plans from one category can be published at a time. Publishing a plan from a different category automatically closes any plans from conflicting categories.

An API can publish multiple plans of the same category, but can't mix categories:

| Plan Type to Publish | Conflicting Published Plan Types | Allowed |
|:---------------------|:--------------------------------|:--------|
| Keyless | mTLS, OAuth2, JWT, API Key | ❌ |
| mTLS | Keyless, OAuth2, JWT, API Key | ❌ |
| OAuth2/JWT/API Key | Keyless, mTLS | ❌ |
| Keyless | Keyless | ✅ |
| mTLS | mTLS | ✅ |
| OAuth2/JWT/API Key | OAuth2/JWT/API Key | ✅ |

Examples:
- If an mTLS plan is published and you publish an API Key plan, the mTLS plan closes automatically
- If a Keyless plan is published and you publish an mTLS plan, the Keyless plan closes automatically

## Prerequisites

Before configuring mTLS for a Kafka Native API:

1. **Enterprise License**: mTLS plans require a Gravitee Enterprise Edition license. The `gravitee-policy-mtls` plugin is an Enterprise feature.
2. **TLS Certificates**: You need:
   - A **server keystore** (JKS format) containing the gateway's private key and certificate
   - A **server truststore** (JKS format) containing the Certificate Authority (CA) certificates that signed the client certificates
   - **Client certificates** (generated and signed by the CA in the truststore) for each Kafka client that will connect

## Gateway Configuration

Configure the following properties in your Gravitee gateway configuration to enable mTLS for the Kafka Gateway.

### Server Keystore (Gateway Identity)

The server keystore contains the gateway's private key and certificate, which the gateway presents to Kafka clients during the TLS handshake.

| Property | Description | Example | Required |
|:---------|:------------|:--------|:---------|
| `kafka.ssl.keystore.type` | Keystore format | `jks` | Yes |
| `kafka.ssl.keystore.path` | Path to the server keystore file | `/path/to/server.keystore.jks` | Yes |
| `kafka.ssl.keystore.password` | Keystore password | `changeit` | Yes |

### Server Truststore (Client Certificate Verification)

The server truststore contains the Certificate Authority (CA) certificates that signed client certificates. The gateway uses this truststore to verify client certificates during the TLS handshake.

| Property | Description | Example | Required |
|:---------|:------------|:--------|:---------|
| `kafka.ssl.clientAuth` | Client authentication mode | `required` | Yes (for mTLS) |
| `kafka.ssl.truststore.type` | Truststore format | `jks` | Yes (for mTLS) |
| `kafka.ssl.truststore.path` | Path to the server truststore file (contains CAs that signed client certs) | `/path/to/server.truststore.jks` | Yes (for mTLS) |
| `kafka.ssl.truststore.password` | Truststore password | `changeit` | Yes (for mTLS) |

Setting `kafka.ssl.clientAuth` to `required` means the gateway rejects any connection that doesn't present a valid client certificate signed by a CA in the truststore.

**Example configuration:**

```yaml
kafka:
  ssl:
    # Gateway server certificate
    keystore:
      type: jks
      path: /opt/gravitee/config/server.keystore.jks
      password: changeit

    # Client certificate validation
    clientAuth: required
    truststore:
      type: jks
      path: /opt/gravitee/config/server.truststore.jks
      password: changeit
```

**Notes:**
- The truststore must contain the CA certificate(s) that signed client certificates
- The keystore contains the gateway's own certificate for outbound connections to Kafka brokers
- Both keystore and truststore must use JKS format

### Shared API Configuration

Set the security protocol in the Kafka Native API's shared configuration. For mTLS with plaintext Kafka protocol (TLS termination at gateway), use `PLAINTEXT`.

```json
{
    "security": {
        "protocol": "PLAINTEXT"
    }
}
```

## Create an mTLS Plan

To create an mTLS plan for a Kafka Native API:

1. Navigate to the API's **Plans** section in the API Management Console.
2. Click **Add new plan**.
3. Select **mTLS** as the security type.
4. Configure the plan settings (name, description, validation mode).
5. Click **Save**.

When publishing an mTLS plan, the console warns you if there are conflicting plans (Keyless or Authentication plans) currently published. A confirmation dialog appears:

**Title:** "Publish plan and close current one(s)"

**Content:**
> Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
>
> Are you sure you want to publish the **mTLS** plan **[Plan Name]**?
>
> The following plan(s) will be closed automatically:
> - **[Conflicting Plan Name]** (Keyless/OAuth2/JWT/API Key)

Review the list of plans that will be closed, then click **Publish and Close** to confirm.

The console displays the security type as **mTLS** in the plan list.

**Example plan definition:**

```json
{
    "id": "plan-mtls-id",
    "name": "mTLS plan",
    "security": {
        "type": "mtls",
        "configuration": {}
    },
    "mode": "standard",
    "status": "published"
}
```

## Create a Subscription with mTLS

To subscribe to an mTLS-secured Kafka API, the subscription must include a **client certificate**. The certificate is base64-encoded PEM format and stored with the subscription.

When a Kafka client connects:
1. The client presents its certificate during the TLS handshake.
2. The gateway extracts the certificate and computes its MD5 fingerprint.
3. The fingerprint is matched against registered subscription certificates.
4. If a match is found, the connection is authorized under that subscription.

## Kafka Client Configuration

Kafka clients connecting to an mTLS-secured API must configure SSL client authentication:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to the client keystore (JKS) | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Keystore format | `JKS` |
| `ssl.keystore.password` | Client keystore password | `changeit` |

The client must also trust the gateway's server certificate. Configure the client truststore:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.truststore.location` | Path to the client truststore | `/path/to/client.truststore.jks` |
| `ssl.truststore.password` | Client truststore password | `changeit` |

## Architecture Notes

### Gateway-to-Broker Independence

The mTLS configuration applies to the connection between the **Kafka client and the Gravitee Gateway** only. The connection between the Gravitee Gateway and the backend Kafka broker cluster is configured independently. This means:

- You can use mTLS for client-to-gateway encryption while using a plaintext or different security protocol for gateway-to-broker communication
- The `sharedConfiguration` on the endpoint group controls the gateway-to-broker connection security

### Authentication Flow

When a Kafka client connects to an mTLS-secured API:

1. The TLS handshake occurs, during which the client presents its certificate.
2. The gateway's security chain validates the certificate.
3. If validation succeeds, the connection is marked as `plainTextAuthenticated`.
4. The principal is set to the certificate identity.
5. If authentication fails, the gateway logs a warning and gracefully closes the connection.

Authentication failures are handled gracefully. The connection is closed without propagating error frames to the client. The error is logged at WARN level:
```
Authentication failed [reason]
```

### Certificate Validation

The gateway validates client certificates using the following process:

1. Extract `TlsSession` from the connection context
2. Verify TLS session exists
3. Verify client certificate is present
4. Verify certificate chain against truststore
5. Compute MD5 hash of certificate
6. Look up subscription by API ID + certificate hash

**Certificate validation errors:**

| Error Key | Description | User Impact |
|-----------|-------------|-------------|
| `SSL_SESSION_REQUIRED` | TLS session is null | Connection rejected; client must use TLS |
| `CLIENT_CERTIFICATE_MISSING` | No client certificate provided | Connection rejected; client must present certificate |
| `CLIENT_CERTIFICATE_INVALID` | Certificate verification failed | Connection rejected; certificate not trusted or expired |

### Subscription Certificate Handling

Subscriptions for mTLS plans are identified by:
- API ID
- Client certificate fingerprint (MD5 hash of the certificate)

**Workflow:**
1. Administrator creates subscription and uploads client certificate (Base64-encoded PEM format)
2. Gateway computes MD5 hash of certificate
3. Gateway registers certificate in subscription truststore manager
4. On connection, gateway extracts client certificate from TLS session
5. Gateway computes MD5 hash and queries subscription service
6. If matching subscription found and active, authentication succeeds

**Registration:**
```java
SubscriptionTrustStoreLoaderManager.registerSubscription(subscription, Set.of())
```

**Unregistration:**
```java
SubscriptionTrustStoreLoaderManager.unregisterSubscription(subscription)
```

**Certificate format:**
- Stored in `Subscription.clientCertificate` field
- Format: Base64-encoded PEM
- Lookup key: MD5 hash of certificate (`SecurityToken.CERTIFICATE` type)

### Connection Topology

```
[Client with Certificate]
    ↓ (mTLS handshake)
[Gravitee Gateway]
    ↓ (validates against truststore)
    ↓ (looks up subscription by cert fingerprint)
    ↓ (connects with gateway certificate)
[Kafka Broker]
```

**Certificate flow:**
- **Client → Gateway**: Client presents certificate from `client.keystore.jks`
- **Gateway verification**: Gateway validates certificate using `server.truststore.jks` (contains CA)
- **Gateway → Broker**: Gateway presents certificate from `server.keystore.jks`

### Security Chain Execution

**Plaintext authentication flow (Kafka protocol):**

1. Check if connection is already authenticated (`plainTextAuthenticated` flag)
2. If not authenticated:
   - Execute `kafkaSecurityChain.execute(ctx)`
   - Extract TLS session from connection context
   - Validate client certificate
   - Compute MD5 hash of certificate
   - Look up subscription by API ID + certificate hash
3. On success:
   - Set `plainTextAuthenticated = true`
   - Assign `KafkaPrincipal.ANONYMOUS` to connection
4. On error:
   - Wrap exception in `KafkaServerAuthenticationException`
   - Log warning with error details
   - Close connection

**Error handling:**
- `KafkaSecurityException` → wrapped in `KafkaServerAuthenticationException`
- Other exceptions → wrapped in `KafkaServerAuthenticationException(new Exception(e), ctx)`
- Authentication failures are logged at `WARN` level (not `ERROR`)

## Enterprise Edition

mTLS plans for Kafka Native APIs are an **Enterprise Edition** feature. The `gravitee-policy-mtls` plugin (version 2.0.0 or later) must be installed and licensed.

## Restrictions

- **PUSH plans** remain unsupported for Kafka Native APIs (unrelated to mTLS)
- **Plan category mixing** isn't allowed (see Plan Security Type Mutual Exclusion)
- mTLS plans use the `gravitee-policy-mtls` plugin version 2.0.0 or later (the 1.x version doesn't support Kafka)
- **Certificate formats**: Keystore/Truststore must be JKS format; client certificates must be Base64-encoded PEM
- Certificate revocation lists (CRLs) are not supported
- OCSP (Online Certificate Status Protocol) is not supported
- Certificate rotation requires gateway restart
- Subscription certificate updates require re-registration
- Client certificates must be signed by a CA present in the gateway's truststore
- Certificate validation failures result in immediate connection closure with no retry mechanism
- Closing mTLS or authentication plans may invalidate active subscriptions; the Console displays a warning before proceeding

## Related Changes

### Console Updates

- The API Management Console UI has been updated to display mTLS as a plan option for Kafka APIs and to show security types with human-readable labels (e.g., "API Key" instead of "API_KEY")
- Plan conflict validation has been extended from a two-category model (Keyless vs Authentication) to a three-category model (Keyless vs mTLS vs Authentication)
- The error messages for plan conflicts have been updated to reflect the new three-way mutual exclusion
- Subscription creation errors now display specific error messages instead of generic "An error occurred during subscription creation"
- Updated banner message for Kafka APIs in the plan creation wizard:
  > "Kafka APIs can't mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans. In order to automatically deploy your API, choose one type: either Keyless, mTLS, or authentication plans."
- Plan publish confirmation dialogs show which plans will be automatically closed and warn if subscriptions will be affected
- The plan list table displays "mTLS" as the security type label for mTLS plans

### Policy Updates

The mTLS policy has been upgraded to version 2.0.0-alpha.2 with Kafka security policy support and APIM 4.10+ compatibility.

**New interfaces:**
- `KafkaSecurityPolicy` (package: `io.gravitee.gateway.reactive.api.policy.kafka`)
  - Methods:
    - `Maybe<SecurityToken> extractSecurityToken(KafkaConnectionContext ctx)`
    - `Completable authenticate(KafkaConnectionContext ctx)`
- `HttpSecurityPolicy` (package: `io.gravitee.gateway.reactive.api.policy.http`)
  - Methods:
    - `Maybe<SecurityToken> extractSecurityToken(HttpPlainExecutionContext ctx)`
    - `Completable onRequest(HttpPlainExecutionContext ctx)`

**Context type changes:**
- `HttpExecutionContext` → `HttpPlainExecutionContext`
- New: `KafkaConnectionContext` with `TlsSession tlsSession()` method

**Policy implementation:**
- `MtlsPolicy` now implements both `HttpSecurityPolicy` and `KafkaSecurityPolicy`
- Supports dual-context authentication (HTTP and Kafka)

### Logging Updates

Authentication error logging now uses WARN level for `KafkaServerAuthenticationException` and includes the most specific cause message.

### Dependency Updates

**mTLS Policy:**
- `gravitee-parent`: 22.1.5 → 23.5.0
- `gravitee-apim.version`: 4.5.0-SNAPSHOT → 4.10.1
- BOM change: `gravitee-bom` → `gravitee-apim-bom`

**APIM:**
- `gravitee-policy-mtls.version`: 1.0.0 → 2.0.0-alpha.2

## Error Messages Reference

### Plan Publishing Errors

**Error:** `NativePlanAuthenticationConflictException`

This error occurs when attempting to publish a plan that conflicts with an already-published plan from a different security category.

**When publishing a Keyless plan:**
> "A plan with mTLS or authentication is already published for the Native API. Keyless plans can't be combined with mTLS or authentication plans."

**When publishing an mTLS plan:**
> "A Keyless or authentication plan is already published for the Native API. mTLS plans can't be combined with Keyless or authentication plans."

**When publishing an authentication plan (OAuth2/JWT/API Key):**
> "A Keyless or mTLS plan is already published for the Native API. Authentication plans can't be combined with Keyless or mTLS plans."

### Certificate Validation Errors

The following error keys are returned when client certificate validation fails during mTLS authentication:

| Error Key | Description | User Impact |
|:----------|:------------|:------------|
| `SSL_SESSION_REQUIRED` | TLS session is null | Connection rejected; client must use TLS |
| `CLIENT_CERTIFICATE_MISSING` | No client certificate provided | Connection rejected; client must present certificate |
| `CLIENT_CERTIFICATE_INVALID` | Certificate verification failed | Connection rejected; certificate not trusted or expired |

**Error message format (Kafka):**
```
Certificate validation failed for Kafka connection: {errorKey}
```

### Gateway Error Keys

**Error key:** `CLIENT_ABORTED_DURING_RESPONSE_ERROR`

This error key is used when a client connection is aborted during response processing.

### Authentication Errors

When authentication fails during a Kafka connection attempt, the gateway logs the following message:

**Log message:**
```
Authentication failed {mostSpecificCauseMessage}
```

**Log level:** `WARN`

**Context:** Logged when `KafkaServerAuthenticationException` is caught during connection authentication. The connection is gracefully closed without propagating error frames to the client.

## Version Requirements

| Component | Minimum Version |
|-----------|----------------|
| APIM | 4.10.0 |
| mTLS Policy | 2.0.0 |

**Policy compatibility matrix:**

| mTLS Policy Version | APIM Version |
|---------------------|--------------|
| 2.x | 4.10 to latest |
| 1.x | 4.5 to 4.9 |

### Overview

Kafka Native APIs support mutual TLS (mTLS) authentication as a plan security type. mTLS requires both the Kafka client and the Gravitee Kafka Gateway to present certificates during the TLS handshake, enabling certificate-based mutual authentication.

In mTLS authentication:
- The gateway presents its server certificate to the Kafka client
- The Kafka client presents its client certificate to the gateway
- The gateway verifies the client certificate against a configured truststore
- The client certificate is matched against a subscription's registered certificate to authorize access

### Plan Security Mutual Exclusion

Kafka Native APIs enforce strict separation between three plan security categories. An API can publish multiple plans of the same category, but can't mix categories.

| Plan Type to Publish | Conflicting Published Plan Types | Allowed |
|:---------------------|:--------------------------------|:--------|
| Keyless | mTLS, OAuth2, JWT, API Key | ❌ |
| mTLS | Keyless, OAuth2, JWT, API Key | ❌ |
| OAuth2/JWT/API Key | Keyless, mTLS | ❌ |
| Keyless | Keyless | ✅ |
| mTLS | mTLS | ✅ |
| OAuth2/JWT/API Key | OAuth2/JWT/API Key | ✅ |

Publishing a plan from one category automatically closes all published plans from conflicting categories.

### Certificate Validation

The gateway validates client certificates during connection establishment. Validation checks for the presence of a TLS session, extracts peer certificates, and verifies them against the configured truststore. Failures result in connection rejection with specific error keys:

| Error Key | Description |
|:----------|:------------|
| `SSL_SESSION_REQUIRED` | No TLS session present |
| `CLIENT_CERTIFICATE_MISSING` | No certificate provided |
| `CLIENT_CERTIFICATE_INVALID` | Verification failed |

### Authentication Flow

When a Kafka client connects with SSL/TLS:

1. The gateway verifies the client certificate against its truststore
2. The security chain executes the mTLS policy, which extracts the TLS session from the connection context and validates the certificate
3. On success, the connection proceeds with an authenticated principal
4. On failure, the policy throws `MtlsPolicyException`, which is wrapped in `KafkaServerAuthenticationException` and the connection is closed with an authentication error logged at WARN level

### Prerequisites

Before configuring mTLS for a Kafka Native API:

- Gravitee API Management 4.10+
- Kafka Native Gateway with SSL/TLS enabled
- Server truststore containing the Certificate Authority (CA) that signed client certificates
- Client certificates signed by a CA trusted by the gateway

### Gateway Configuration

#### SSL/TLS Settings

Configure the Kafka gateway to require client certificate authentication and specify the truststore for verifying client certificates.

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Require client certificate authentication | `required` |
| `kafka.ssl.truststore.type` | Truststore format for verifying client certificates | `jks` |
| `kafka.ssl.truststore.password` | Truststore password | `gravitee` |
| `kafka.ssl.truststore.path` | Path to truststore file containing CA certificates | `/path/to/server.truststore.jks` |

#### Shared API Configuration

Set the security protocol in the Kafka Native API's shared configuration. For mTLS with plaintext Kafka protocol (TLS termination at gateway), use `PLAINTEXT`.

```json
{
    "security": {
        "protocol": "PLAINTEXT"
    }
}
```

### Creating an mTLS Plan

Define an mTLS plan in the API configuration by setting the security type to `mtls`. The plan definition includes an ID, name, security configuration, mode, and status.

To create an mTLS plan:

1. Navigate to the API's plan configuration
2. Add a new plan and select **mTLS** as the security type
3. Configure the plan mode (standard) and tags as needed
4. Publish the plan

If conflicting plan types (Keyless or authentication-based) are already published, the Console prompts you to close them automatically before publishing the mTLS plan.

```json
{
    "id": "plan-mtls-id",
    "name": "mTLS plan",
    "security": {
        "type": "mtls",
        "configuration": {}
    },
    "mode": "standard",
    "status": "published"
}
```

### Client Configuration

Kafka clients must provide a keystore containing their certificate and private key to authenticate with the gateway.

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to client keystore file | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Keystore format | `JKS` |
| `ssl.keystore.password` | Keystore password | `gravitee` |

### Restrictions

- mTLS plans can't coexist with published Keyless plans on the same Kafka Native API
- mTLS plans can't coexist with published authentication plans (OAuth2, JWT, API Key) on the same Kafka Native API
- Publishing an mTLS plan automatically closes all conflicting published plans
- Closing mTLS or authentication plans may invalidate active subscriptions; the Console displays a warning before proceeding
- Client certificates must be signed by a CA present in the gateway's truststore
- Certificate validation failures result in immediate connection closure with no retry mechanism
- PUSH plan type isn't available for Kafka Native APIs

### Related Changes

#### Console Updates

The Management Console displays updated banner messages in the API creation wizard, clarifying that Kafka APIs can't mix Keyless, mTLS, and authentication plans. Plan publish confirmation dialogs show which plans will be automatically closed and warn if subscriptions will be affected. The plan list table displays "mTLS" as the security type label for mTLS plans. Subscription creation error messages now display server-provided details (e.g., plan conflict errors) instead of generic messages.

#### Policy Updates

The mTLS policy has been upgraded to version 2.0.0-alpha.2 with Kafka security policy support and APIM 4.10+ compatibility.

#### Logging Updates

Authentication error logging now uses WARN level for `KafkaServerAuthenticationException` and includes the most specific cause message.
