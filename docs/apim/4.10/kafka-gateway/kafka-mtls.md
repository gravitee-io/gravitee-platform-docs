## Overview

Gravitee API Management supports **mTLS (mutual TLS) authentication** as a plan security type for Kafka Native APIs. mTLS enables certificate-based mutual authentication between Kafka clients and the Gravitee Kafka Gateway.

In mTLS authentication:
- The **gateway** presents its server certificate to the Kafka client
- The **Kafka client** presents its client certificate to the gateway
- The gateway verifies the client certificate against a configured truststore
- The client certificate is matched against a subscription's registered certificate to authorize access

Previously, mTLS plans were only supported for HTTP-based APIs. This update makes mTLS a first-class plan type for the Kafka Native Gateway, enabling organizations that require strict certificate-based authentication to use the Kafka Native Gateway securely.

## Plan Security Type Mutual Exclusion

Kafka Native APIs enforce mutual exclusion between three categories of plan security types:

| Category | Security Types | Description |
|:---------|:---------------|:------------|
| **Keyless** | Keyless | No authentication required |
| **mTLS** | mTLS | Certificate-based mutual authentication |
| **Authentication** | API Key, OAuth2, JWT | Token or key-based authentication |

These categories are **mutually exclusive**. Only plans from one category can be published at a time. Publishing a plan from a different category automatically closes any plans from conflicting categories.

Examples:
- If an mTLS plan is published and you publish an API Key plan, the mTLS plan closes automatically
- If a Keyless plan is published and you publish an mTLS plan, the Keyless plan closes automatically

<!-- GAP: The exact user experience for the auto-close flow (confirmation dialog, warnings) is implemented in the console UI but the specific UI screenshots and step-by-step flow are not available from the code alone. -->

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

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.keystore.type` | Keystore format | `jks` |
| `kafka.ssl.keystore.path` | Path to the server keystore file | `/path/to/server.keystore.jks` |
| `kafka.ssl.keystore.password` | Keystore password | `changeit` |

### Server Truststore (Client Certificate Verification)

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Client authentication mode | `required` |
| `kafka.ssl.truststore.type` | Truststore format | `jks` |
| `kafka.ssl.truststore.path` | Path to the server truststore file (contains CAs that signed client certs) | `/path/to/server.truststore.jks` |
| `kafka.ssl.truststore.password` | Truststore password | `changeit` |

Setting `kafka.ssl.clientAuth` to `required` means the gateway rejects any connection that doesn't present a valid client certificate signed by a CA in the truststore.

<!-- GAP: Whether kafka.ssl.clientAuth supports values other than "required" (e.g., "requested", "none") is not clear from the code. The test code only shows "required". -->

## Create an mTLS Plan

To create an mTLS plan for a Kafka Native API:

1. Navigate to the API's **Plans** section in the API Management Console.
2. Click **Add new plan**.
3. Select **mTLS** as the security type.
4. Configure the plan settings (name, description, validation mode).
5. Publish the plan.

When publishing an mTLS plan, the console warns you if there are conflicting plans (Keyless or Authentication plans) currently published. You can confirm the publish action, which automatically closes the conflicting plans.

The console displays the security type as **mTLS** in the plan list.

## Create a Subscription with mTLS

To subscribe to an mTLS-secured Kafka API, the subscription must include a **client certificate**. The certificate is base64-encoded and stored with the subscription.

When a Kafka client connects:
1. The client presents its certificate during the TLS handshake.
2. The gateway extracts the certificate and computes its MD5 fingerprint.
3. The fingerprint is matched against registered subscription certificates.
4. If a match is found, the connection is authorized under that subscription.

<!-- GAP: The exact API call or console UI flow for creating a subscription with a client certificate is not visible in the code diffs. The test code shows programmatic certificate registration via SubscriptionTrustStoreLoaderManager. -->

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

### Enterprise Edition

mTLS plans for Kafka Native APIs are an **Enterprise Edition** feature. The `gravitee-policy-mtls` plugin (version 2.0.0-alpha.2 or later) must be installed and licensed.

## Restrictions

- **PUSH plans** remain unsupported for Kafka Native APIs (unrelated to mTLS)
- **Plan category mixing** isn't allowed (see Plan Security Type Mutual Exclusion)
- mTLS plans use the `gravitee-policy-mtls` plugin version 2.0.0 or later (the 1.x version doesn't support Kafka)

## Related Changes

- The API Management Console UI has been updated to display mTLS as a plan option for Kafka APIs and to show security types with human-readable labels (e.g., "API Key" instead of "API_KEY")
- Plan conflict validation has been extended from a two-category model (Keyless vs Authentication) to a three-category model (Keyless vs mTLS vs Authentication)
- The error messages for plan conflicts have been updated to reflect the new three-way mutual exclusion

### mTLS Authentication for Kafka

mTLS (mutual TLS) requires both the client and server to present certificates during the TLS handshake. For Kafka Native APIs in Gravitee API Management:

- **Client → Gateway**: Clients must present a valid certificate signed by a trusted Certificate Authority (CA)
- **Gateway verification**: The gateway validates client certificates against a configured truststore
- **Gateway → Broker**: The gateway uses its own certificate when connecting to Kafka brokers

**How it works:**

1. Client initiates TLS connection to gateway
2. Gateway requests client certificate
3. Gateway validates certificate against truststore
4. If valid, gateway extracts certificate fingerprint (MD5 hash)
5. Gateway looks up subscription using API ID + certificate fingerprint
6. If subscription exists and is active, connection proceeds
7. Gateway forwards requests to Kafka broker using its own certificate

**Prerequisites:**

- Gateway must be configured with server keystore (gateway identity)
- Gateway must be configured with truststore containing CA certificates
- Clients must possess certificates signed by a CA in the gateway truststore
- Subscriptions must be created with client certificates registered

### Plan Type Mutual Exclusion

Kafka Native APIs enforce strict separation between security plan types. You can't publish plans of different security categories simultaneously.

**Security categories:**

- **Keyless**: No authentication required (`KEY_LESS`)
- **mTLS**: Certificate-based authentication (`MTLS`)
- **Authentication**: Token/key-based authentication (`OAUTH2`, `JWT`, `API_KEY`)

**Mutual exclusion rules:**

- Publishing a Keyless plan automatically closes any published mTLS or authentication plans
- Publishing an mTLS plan automatically closes any published Keyless or authentication plans
- Publishing an authentication plan automatically closes any published Keyless or mTLS plans

**Rationale:** Kafka's connection model doesn't support mixing authentication methods within a single API deployment.

### Certificate-Based Subscription Lookup

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

<!-- GAP: Exact UI workflow for uploading client certificate during subscription creation -->

### Create an mTLS plan

1. Navigate to **APIs** > select your Kafka Native API > **Plans**.
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Click **Add new plan**.
3. Configure plan details:
   - **Name**: Enter a plan name.
   - **Description**: (Optional) Describe the plan purpose.
4. In the **Security** section, select **mTLS** as the security type.
5. Click **Create**.
6. Configure plan settings (rate limits, quotas, etc.).
7. Click **Save**.

{% hint style="warning" %}
Kafka APIs can't mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans. To automatically deploy your API, choose one type: either Keyless, mTLS, or authentication plans.
{% endhint %}

### Publish an mTLS plan with conflicting plans

1. Navigate to **APIs** > select your Kafka Native API > **Plans**.
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Locate the mTLS plan you want to publish.
3. Click **Publish**.
4. If conflicting plans exist, a confirmation dialog appears:

   **Publish plan and close current one(s)**
   
   > Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
   > 
   > Are you sure you want to publish the **mTLS** plan **[Plan Name]**?
   > 
   > The following plan(s) will be closed automatically:
   > - **[Conflicting Plan Name]** (Keyless/OAuth2/JWT/API Key)

5. Review the list of plans that will be closed.
6. Click **Publish and Close** to confirm.

The mTLS plan is published, and all conflicting plans are automatically closed.

### Create a subscription with client certificate

1. Navigate to **Applications** > select your application > **Subscriptions**.
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Click **Create Subscription**.
3. Select the API and mTLS plan.
4. Upload the client certificate:
   - Format: Base64-encoded PEM
   - The certificate must be signed by a CA in the gateway's truststore
5. Click **Create**.

<!-- GAP: Exact UI field name and upload mechanism for client certificate -->
<!-- GAP: Certificate validation feedback during upload -->

The subscription is created, and the client certificate is registered in the gateway's subscription truststore manager.

### Revoke a subscription

1. Navigate to **Applications** > select your application > **Subscriptions**.
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Locate the subscription.
3. Click **Revoke**.
4. Confirm revocation.

The subscription is revoked, and the client certificate is unregistered from the gateway's subscription truststore manager. Clients using this certificate can no longer connect.

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

### Certificate Validation Chain

**HTTP context (Console/Portal):**

1. Extract `TlsSession` from `HttpPlainExecutionContext`
2. Call `validateClientCertificate(tlsSession)`
3. If invalid, return 401 Unauthorized with error key
4. If valid, compute MD5 hash and create `SecurityToken`

**Kafka context (Gateway):**

1. Extract `TlsSession` from `KafkaConnectionContext`
2. Call `validateClientCertificate(tlsSession)`
3. If invalid, throw `MtlsPolicyException` with error key
4. If valid, compute MD5 hash and create `SecurityToken`

**Validation logic:**
- Check if TLS session exists → error key: `SSL_SESSION_REQUIRED`
- Check if client certificate present → error key: `CLIENT_CERTIFICATE_MISSING`
- Verify certificate chain → error key: `CLIENT_CERTIFICATE_INVALID` (on `SSLPeerUnverifiedException`)

### Subscription Certificate Handling

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

<!-- GAP: Encoding/decoding logic for certificate storage -->
<!-- GAP: Implementation details of SubscriptionTrustStoreLoaderManager -->

### Publish an mTLS Plan (with Conflicting Plans)

1. Navigate to **APIs** > Select your Kafka Native API > **Plans**
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Locate the mTLS plan you want to publish
3. Click **Publish**
4. If conflicting plans exist, a confirmation dialog appears:

   **Title:** "Publish plan and close current one(s)"
   
   **Content:**
   > Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
   > 
   > Are you sure you want to publish the **mTLS** plan **[Plan Name]**?
   > 
   > The following plan(s) will be closed automatically:
   > - **[Conflicting Plan Name]** (Keyless/OAuth2/JWT/API Key)

5. Review the list of plans that will be closed
6. Click **Publish and Close** to confirm

**Result:** The mTLS plan is published, and all conflicting plans are automatically closed.

### Create a Subscription with Client Certificate

1. Navigate to **Applications** > Select your application > **Subscriptions**
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Click **Create Subscription**
3. Select the API and mTLS plan
4. Upload the client certificate:
   - Format: Base64-encoded PEM
   - The certificate must be signed by a CA in the gateway's truststore
5. Click **Create**

<!-- GAP: Exact UI field name and upload mechanism for client certificate -->
<!-- GAP: Certificate validation feedback during upload -->

**Result:** The subscription is created, and the client certificate is registered in the gateway's subscription truststore manager.

### Revoke a Subscription

1. Navigate to **Applications** > Select your application > **Subscriptions**
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Locate the subscription
3. Click **Revoke**
4. Confirm revocation

**Result:** The subscription is revoked, and the client certificate is unregistered from the gateway's subscription truststore manager. Clients using this certificate can't connect.

### Version Requirements

| Component | Minimum Version |
|-----------|----------------|
| APIM | 4.10.0 |
| mTLS Policy | 2.0.0 |

**Policy compatibility matrix:**

| mTLS Policy Version | APIM Version |
|---------------------|--------------|
| 2.x | 4.10 to latest |
| 1.x | 4.5 to 4.9 |

### Plan Type Limitations

**Kafka Native APIs can't have the following plan types published simultaneously:**
- Keyless + mTLS
- Keyless + Authentication (OAuth2, JWT, API Key)
- mTLS + Authentication (OAuth2, JWT, API Key)

**Enforcement:** Publishing a plan of one type automatically closes published plans of conflicting types.

### Certificate Format Restrictions

**Supported formats:**
- Keystore/Truststore: JKS only
- Client certificates: Base64-encoded PEM

<!-- GAP: Support for PKCS12, PEM keystores -->
<!-- GAP: Certificate chain depth limits -->
<!-- GAP: Supported signature algorithms -->

### Known Limitations

- Certificate revocation lists (CRLs) aren't supported
- OCSP (Online Certificate Status Protocol) isn't supported
- Certificate rotation requires gateway restart
- Subscription certificate updates require re-registration

<!-- GAP: Workarounds for certificate rotation -->
<!-- GAP: Grace period behavior during certificate updates -->

### UI Updates

**Plan list display:**
- Plan security type now displays human-readable labels:
  - `KEY_LESS` → "Keyless"
  - `MTLS` → "mTLS"
  - `API_KEY` → "API Key"
  - `OAUTH2` → "OAuth2"
  - `JWT` → "JWT"

**Plan creation wizard:**
- Updated banner message for Kafka APIs:
  > "Kafka APIs can't mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans. In order to automatically deploy your API, choose one type: either Keyless, mTLS, or authentication plans."

**Plan publish dialog:**
- Shows list of plans that will be automatically closed
- Displays security type labels for each plan
- Includes subscription warning when closing mTLS or authentication plans

### Version Requirements

| Component | Minimum Version |
|-----------|----------------|
| APIM | 4.10.0 |
| mTLS Policy | 2.0.0 |

**Policy compatibility matrix:**

| mTLS Policy Version | APIM Version |
|---------------------|--------------|
| 2.x | 4.10 to latest |
| 1.x | 4.5 to 4.9 |

### Plan Type Limitations

Kafka Native APIs can't have the following plan types published simultaneously:
- Keyless + mTLS
- Keyless + Authentication (OAuth2, JWT, API Key)
- mTLS + Authentication (OAuth2, JWT, API Key)

Publishing a plan of one type automatically closes published plans of conflicting types.

### Certificate Format Restrictions

**Supported formats:**
- Keystore/Truststore: JKS only
- Client certificates: Base64-encoded PEM

<!-- GAP: Support for PKCS12 keystores -->
<!-- GAP: Support for PEM keystores -->
<!-- GAP: Certificate chain depth limits -->
<!-- GAP: Supported signature algorithms -->

### Known Limitations

- Certificate revocation lists (CRLs) aren't supported
- OCSP (Online Certificate Status Protocol) isn't supported
- Certificate rotation requires gateway restart
- Subscription certificate updates require re-registration

<!-- GAP: Workarounds for certificate rotation -->
<!-- GAP: Grace period behavior during certificate updates -->

### Certificate Validation Flow

When a Kafka client connects to an mTLS-secured API, the gateway performs certificate validation in the following sequence:

1. **TLS session check** → If no TLS session exists, reject with error key: `SSL_SESSION_REQUIRED`
2. **Certificate presence check** → If no client certificate is provided, reject with error key: `CLIENT_CERTIFICATE_MISSING`
3. **Certificate chain verification** → If verification fails (e.g., `SSLPeerUnverifiedException`), reject with error key: `CLIENT_CERTIFICATE_INVALID`

### Subscription Certificate Handling

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

<!-- GAP: Encoding/decoding logic for certificate storage -->
<!-- GAP: Implementation details of SubscriptionTrustStoreLoaderManager -->

### Version Requirements

| Component | Minimum Version |
|-----------|----------------|
| APIM | 4.10.0 |
| mTLS Policy | 2.0.0 |

**Policy compatibility matrix:**

| mTLS Policy Version | APIM Version |
|---------------------|--------------|
| 2.x | 4.10 to latest |
| 1.x | 4.5 to 4.9 |

### Plan Type Limitations

Kafka Native APIs can't have the following plan types published simultaneously:
- Keyless + mTLS
- Keyless + Authentication (OAuth2, JWT, API Key)
- mTLS + Authentication (OAuth2, JWT, API Key)

**Enforcement:** Publishing a plan of one type automatically closes published plans of conflicting types.

### Certificate Format Restrictions

**Supported formats:**
- Keystore/Truststore: JKS only
- Client certificates: Base64-encoded PEM

<!-- GAP: Support for PKCS12, PEM keystores -->
<!-- GAP: Certificate chain depth limits -->
<!-- GAP: Supported signature algorithms -->

### Known Limitations

- Certificate revocation lists (CRLs) aren't supported
- OCSP (Online Certificate Status Protocol) isn't supported
- Certificate rotation requires gateway restart
- Subscription certificate updates require re-registration

<!-- GAP: Workarounds for certificate rotation -->
<!-- GAP: Grace period behavior during certificate updates -->

### UI Updates

**Plan list display:**
- Plan security type now displays human-readable labels:
  - `KEY_LESS` → "Keyless"
  - `MTLS` → "mTLS"
  - `API_KEY` → "API Key"
  - `OAUTH2` → "OAuth2"
  - `JWT` → "JWT"

**Plan creation wizard:**
- Updated banner message for Kafka APIs:
  > "Kafka APIs can't mix Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans. In order to automatically deploy your API, choose one type: either Keyless, mTLS, or authentication plans."

**Plan publish dialog:**
- Shows list of plans that will be automatically closed
- Displays security type labels for each plan
- Includes subscription warning when closing mTLS or authentication plans

**Subscription error messages:**
- Subscription creation errors now display specific error messages instead of generic "An error occurred during subscription creation"

### Console Changes

**Error handling:**
- New error key: `CLIENT_ABORTED_DURING_RESPONSE_ERROR` (gateway error keys)
- Certificate validation error keys:
  - `SSL_SESSION_REQUIRED`
  - `CLIENT_CERTIFICATE_MISSING`
  - `CLIENT_CERTIFICATE_INVALID`

**Exception types:**
- New: `MtlsPolicyException` (package: `io.gravitee.policy.mtls.exception`)
  - Message format: `"Certificate validation failed for Kafka connection: {errorKey}"`
- Enhanced: `KafkaServerAuthenticationException` now includes connection context

### API Changes

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

### Dependency Updates

**mTLS Policy:**
- `gravitee-parent`: 22.1.5 → 23.5.0
- `gravitee-apim.version`: 4.5.0-SNAPSHOT → 4.10.1
- BOM change: `gravitee-bom` → `gravitee-apim-bom`

**APIM:**
- `gravitee-policy-mtls.version`: 1.0.0 → 2.0.0-alpha.2

<!-- GAP: Final version number for gravitee-reactor-native-kafka with mTLS support -->

### Error Messages Reference

#### Plan Publishing Errors

**Error:** `NativePlanAuthenticationConflictException`

**When publishing Keyless plan:**
> "A plan with mTLS or authentication is already published for the Native API. Keyless plans can't be combined with mTLS or authentication plans."

**When publishing mTLS plan:**
> "A Keyless or authentication plan is already published for the Native API. mTLS plans can't be combined with Keyless or authentication plans."

**When publishing authentication plan (OAuth2/JWT/API Key):**
> "A Keyless or mTLS plan is already published for the Native API. Authentication plans can't be combined with Keyless or mTLS plans."

#### Certificate Validation Errors

| Error Key | Description | User Impact |
|-----------|-------------|-------------|
| `SSL_SESSION_REQUIRED` | TLS session is null | Connection rejected; client must use TLS |
| `CLIENT_CERTIFICATE_MISSING` | No client certificate provided | Connection rejected; client must present certificate |
| `CLIENT_CERTIFICATE_INVALID` | Certificate verification failed | Connection rejected; certificate not trusted or expired |

**Error message format (Kafka):**
```
Certificate validation failed for Kafka connection: {errorKey}
```

#### Authentication Errors

**Log message (gateway):**
```
Authentication failed {mostSpecificCauseMessage}
```

**Log level:** `WARN`

**Context:** Logged when `KafkaServerAuthenticationException` is caught during connection authentication.

### Overview

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

### Plan Security Type Mutual Exclusion

Kafka Native APIs enforce mutual exclusion between three categories of plan security types:

| Category | Security Types | Description |
|:---------|:---------------|:------------|
| **Keyless** | Keyless | No authentication required |
| **mTLS** | mTLS | Certificate-based mutual authentication |
| **Authentication** | API Key, OAuth2, JWT | Token or key-based authentication |

These categories are **mutually exclusive**. Only plans from one category can be published at a time. Publishing a plan from a different category automatically closes any plans from conflicting categories.

Examples:
- If an mTLS plan is published and you publish an API Key plan, the mTLS plan closes automatically
- If a Keyless plan is published and you publish an mTLS plan, the Keyless plan closes automatically

### Prerequisites

Before configuring mTLS for a Kafka Native API:

1. **Enterprise License**: mTLS plans require a Gravitee Enterprise Edition license. The `gravitee-policy-mtls` plugin is an Enterprise feature.
2. **TLS Certificates**: You need:
   - A **server keystore** (JKS format) containing the gateway's private key and certificate
   - A **server truststore** (JKS format) containing the Certificate Authority (CA) certificates that signed the client certificates
   - **Client certificates** (generated and signed by the CA in the truststore) for each Kafka client that will connect

### Gateway Configuration

Configure the following properties in your Gravitee gateway configuration to enable mTLS for the Kafka Gateway.

#### Server Keystore (Gateway Identity)

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.keystore.type` | Keystore format | `jks` |
| `kafka.ssl.keystore.path` | Path to the server keystore file | `/path/to/server.keystore.jks` |
| `kafka.ssl.keystore.password` | Keystore password | `changeit` |

#### Server Truststore (Client Certificate Verification)

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Client authentication mode | `required` |
| `kafka.ssl.truststore.type` | Truststore format | `jks` |
| `kafka.ssl.truststore.path` | Path to the server truststore file (contains CAs that signed client certs) | `/path/to/server.truststore.jks` |
| `kafka.ssl.truststore.password` | Truststore password | `changeit` |

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

### Create an mTLS Plan

To create an mTLS plan for a Kafka Native API:

1. Navigate to the API's **Plans** section in the API Management Console.
2. Click **Add new plan**.
3. Select **mTLS** as the security type.
4. Configure the plan settings (name, description, validation mode).
5. Click **Save**.

When publishing an mTLS plan, the console warns you if there are conflicting plans (Keyless or Authentication plans) currently published. A confirmation dialog appears:

**Title:** "Publish plan and close current one(s)"

**Content:**
> Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
> 
> Are you sure you want to publish the **mTLS** plan **[Plan Name]**?
> 
> The following plan(s) will be closed automatically:
> - **[Conflicting Plan Name]** (Keyless/OAuth2/JWT/API Key)

Review the list of plans that will be closed, then click **Publish and Close** to confirm.

The console displays the security type as **mTLS** in the plan list.

### Create a Subscription with mTLS

To subscribe to an mTLS-secured Kafka API, the subscription must include a **client certificate**. The certificate is base64-encoded PEM format and stored with the subscription.

When a Kafka client connects:
1. The client presents its certificate during the TLS handshake.
2. The gateway extracts the certificate and computes its MD5 fingerprint.
3. The fingerprint is matched against registered subscription certificates.
4. If a match is found, the connection is authorized under that subscription.

<!-- GAP: Exact UI workflow for uploading client certificate during subscription creation -->

### Kafka Client Configuration

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

### Architecture Notes

#### Gateway-to-Broker Independence

The mTLS configuration applies to the connection between the **Kafka client and the Gravitee Gateway** only. The connection between the Gravitee Gateway and the backend Kafka broker cluster is configured independently. This means:

- You can use mTLS for client-to-gateway encryption while using a plaintext or different security protocol for gateway-to-broker communication
- The `sharedConfiguration` on the endpoint group controls the gateway-to-broker connection security

#### Authentication Flow

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

#### Certificate Validation

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

#### Subscription Certificate Handling

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

### Enterprise Edition

mTLS plans for Kafka Native APIs are an **Enterprise Edition** feature. The `gravitee-policy-mtls` plugin (version 2.0.0 or later) must be installed and licensed.

### Restrictions

- **PUSH plans** remain unsupported for Kafka Native APIs (unrelated to mTLS)
- **Plan category mixing** isn't allowed (see Plan Security Type Mutual Exclusion)
- mTLS plans use the `gravitee-policy-mtls` plugin version 2.0.0 or later (the 1.x version doesn't support Kafka)
- **Certificate formats**: Keystore/Truststore must be JKS format; client certificates must be Base64-encoded PEM
- Certificate revocation lists (CRLs) are not supported
- OCSP (Online Certificate Status Protocol) is not supported
- Certificate rotation requires gateway restart
- Subscription certificate updates require re-registration

### Related Changes

- The API Management Console UI has been updated to display mTLS as a plan option for Kafka APIs and to show security types with human-readable labels (e.g., "API Key" instead of "API_KEY")
- Plan conflict validation has been extended from a two-category model (Keyless vs Authentication) to a three-category model (Keyless vs mTLS vs Authentication)
- The error messages for plan conflicts have been updated to reflect the new three-way mutual exclusion
- Subscription creation errors now display specific error messages instead of generic "An error occurred during subscription creation"

### Gateway SSL Configuration

Configure the gateway's SSL settings in `gravitee.yml` to enable mTLS authentication for Kafka Native APIs.

#### Server Certificate (Gateway Identity)

The server keystore contains the gateway's private key and certificate, which the gateway presents to Kafka clients during the TLS handshake.

| Property | Description | Example | Required |
|:---------|:------------|:--------|:---------|
| `kafka.ssl.keystore.type` | Keystore format | `jks` | Yes |
| `kafka.ssl.keystore.path` | Path to keystore file | `/path/to/server.keystore.jks` | Yes |
| `kafka.ssl.keystore.password` | Keystore password | `changeit` | Yes |

#### Client Certificate Validation (mTLS)

The server truststore contains the Certificate Authority (CA) certificates that signed client certificates. The gateway uses this truststore to verify client certificates during the TLS handshake.

| Property | Description | Example | Required |
|:---------|:------------|:--------|:---------|
| `kafka.ssl.clientAuth` | Enforce client certificate authentication | `required` | Yes (for mTLS) |
| `kafka.ssl.truststore.type` | Truststore format | `jks` | Yes (for mTLS) |
| `kafka.ssl.truststore.path` | Path to truststore containing CA certificates | `/path/to/server.truststore.jks` | Yes (for mTLS) |
| `kafka.ssl.truststore.password` | Truststore password | `changeit` | Yes (for mTLS) |

Setting `kafka.ssl.clientAuth` to `required` enforces client certificate authentication. The gateway rejects any connection that doesn't present a valid client certificate signed by a CA in the truststore.

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

The truststore must contain the CA certificate(s) that signed client certificates. Both keystore and truststore must use JKS format.

<!-- GAP: Instructions for generating/importing certificates into JKS keystores -->
<!-- GAP: Broker-side SSL configuration requirements -->

### Error Messages Reference

#### Plan Publishing Errors

**Error:** `NativePlanAuthenticationConflictException`

This error occurs when attempting to publish a plan that conflicts with an already-published plan from a different security category.

**When publishing a Keyless plan:**
> "A plan with mTLS or authentication is already published for the Native API. Keyless plans cannot be combined with mTLS or authentication plans."

**When publishing an mTLS plan:**
> "A Keyless or authentication plan is already published for the Native API. mTLS plans cannot be combined with Keyless or authentication plans."

**When publishing an authentication plan (OAuth2/JWT/API Key):**
> "A Keyless or mTLS plan is already published for the Native API. Authentication plans cannot be combined with Keyless or mTLS plans."

#### Certificate Validation Errors

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

#### Gateway Error Keys

**Error key:** `CLIENT_ABORTED_DURING_RESPONSE_ERROR`

This error key is used when a client connection is aborted during response processing.

#### Authentication Errors

When authentication fails during a Kafka connection attempt, the gateway logs the following message:

**Log message:**
```
Authentication failed {mostSpecificCauseMessage}
```

**Log level:** `WARN`

**Context:** Logged when `KafkaServerAuthenticationException` is caught during connection authentication. The connection is gracefully closed without propagating error frames to the client.

### Publish an mTLS Plan (with Conflicting Plans)

When you publish an mTLS plan for a Kafka Native API, the console checks for conflicting published plans. If any Keyless or Authentication plans (API Key, OAuth2, JWT) are currently published, a confirmation dialog appears.

**To publish an mTLS plan:**

1. Navigate to **APIs** > Select your Kafka Native API > **Plans**.
<!-- NEED CLARIFICATION: This navigation path was not found in the source draft. Verify the exact UI path before publishing. -->
2. Locate the mTLS plan you want to publish.
3. Click **Publish**.
4. If conflicting plans exist, a confirmation dialog appears with the title **"Publish plan and close current one(s)"**.
    
    The dialog content explains:
    
    > Kafka APIs cannot have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
    > 
    > Are you sure you want to publish the **mTLS** plan **[Plan Name]**?
    > 
    > The following plan(s) will be closed automatically:
    > - **[Conflicting Plan Name]** (Keyless/OAuth2/JWT/API Key)
    
5. Review the list of plans that will be closed.
6. Click **Publish and Close** to confirm.

**Result:** The mTLS plan is published, and all conflicting plans are automatically closed.

<!-- GAP: Screenshot showing the "Publish plan and close current one(s)" confirmation dialog -->