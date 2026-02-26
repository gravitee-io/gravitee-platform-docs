# Certificates

## Overview

Cryptographic algorithms such as KeyStore (private/public key) are used to sign using JSON-based data structures (JWT) tokens. Certificates are used as part of the OAuth 2.0 and OpenID Connect protocol to sign access, create and renew ID tokens and ensure the integrity of a token’s payload.

Certificate definitions apply at the _security domain_ level.

By default AM is able to load certificate using JKS or PKCS12 format you can upload ugin the console or the REST API. An Enterprise prise plugin also exist to load PCKS12 certificate from [AWS Secret Manager](aws-certificate-plugin.md).

## Create certificates

### Java KeyStore (JKS)

Storage for cryptographic keys and certificates is managed in a (`.jks`) file.

{% hint style="info" %}
To generate a new keystore, you can use the Key and Certificate Management Tool `keytool`.
{% endhint %}

```sh
keytool -genkeypair
          -alias mytestkey
          -keyalg RSA
          -dname "CN=Web Server,OU=Unit,O=Organization,L=City,S=State,C=US"
          -keypass changeme
          -keystore server.jks
          -storepass letmein
```

{% hint style="info" %}
Default keys are RS256 (SHA256withRSA). For RS512 keys, add the following options: `-sigalg SHA512withRSA -keysize 4096`
{% endhint %}

### Create a new certificate with AM Console

1. Log in to AM Console.
2. Click **Settings > Certificates**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Choose the certificate type and click **Next**.
5. Give your certificate a name, then enter the details of the keystore file.
6.  Click **Create**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-create-certificate.png" alt=""><figcaption><p>Create new certificate</p></figcaption></figure>

### Create a new certificate with AM API

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{
           "type": "javakeystore-am-certificate",
           "name": "Java KeyStore",
           "configuration": "{\"jks\":\"{\"name\":\"server.jks\",\"type\":\"\",\"size\":2236,\"content\":\"base64EncodingFile\",\"storepass\":\"letmein\",\"alias\":\"mytestkey\",\"keypass\":\"changeme\"}"
         }'
     http://GRAVITEEIO-AM-MGT-API-HOST/management/certificates
```
{% endcode %}

### Public keys

You can use public keys to verify a token payload’s integrity. To obtain the public key for your certificate:

1. In AM Console, click **Settings > Certificates**.
2.  Next to your certificate, click the key icon.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-profile-public-key.png" alt=""><figcaption><p>Certificates list</p></figcaption></figure>
3.  You can copy/paste the public key to use with third-party libraries to verify your tokens.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-public-key.png" alt=""><figcaption><p>Certificate public key</p></figcaption></figure>

{% hint style="info" %}
Gravitee API Management (APIM) comes with a JWT Policy to verify and decode tokens that can be used for your APIs.
{% endhint %}

### Apply the certificate to your application

1. In AM Console, click **Applications**.
2. In the **Settings** tab, click **Certificates**.
3. Choose your certificate and click **SAVE**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-certificate-app.png" alt=""><figcaption><p>Apply certificate to application</p></figcaption></figure>

### Certificate for Mutual TLS authentication <a href="#certificate-for-mutual-tls-authentication" id="certificate-for-mutual-tls-authentication"></a>

To mark a certificate as usable for mTLS, you just have to check the "mTLS" usage in the configuration form of your certificate.

{% hint style="info" %}
System certificates can't be used for mTLS authentication as they are self signed certificates generated internally by Access Management.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

### Custom certificates

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-custom-certificate.png" alt=""><figcaption><p>Custom certificate diagram</p></figcaption></figure>

AM is designed to be extended based on a pluggable modules architecture. You can develop your own certificate and provide a sign method for tokens.

## System certificates

When a new domain is created, a certificate is generated for use by the domain applications to sign the tokens. Such certificates are marked as "system" certificates.

### How to define system certificate properties

System certificates are generated based on the Management API settings that allow the definition of:

* the key size (default value: `2048`)
* the certificate alias (default value: `default`)
* the validity of the certificate, measured in days (default value: `365`)
* the algorithm used to sign tokens (default value: `SHA256withRSA`)
* the X.500 name of the certificate (default value: `cn=Gravitee.io`)

To set or modify these values, update the `domains.certificates` section in the `gravitee.yaml` file of the Management API service.

```yaml
domains:
  certificates:
    default:
      keysize: 2048
      alias: default
      keypass: gravitee
      storepass: gravitee
      validity: 365             # Validity of the certificate
      algorithm: SHA256withRSA  # Algorithm used to sign certificate
      name: cn=Gravitee.io      # Certificate X.500 name
```

You can define these properties in the `values.yaml` file of the AM Helm Chart.

```yaml
api:
  domains:
    certificates:
      default:
        keysize: 2048
        alias: default
        keypass: gravitee
        storepass: gravitee
        validity: 365             # Validity of the certificate
        algorithm: SHA256withRSA  # Algorithm used to sign certificate
        name: cn=Gravitee.io      # Certificate X.500 name
```

### Certificate rotation

Like all certificates, a system certificate has a given validity period, after which tokens will not be valid anymore. The certificate rotation feature enables you to generate a new system certificate quickly and easily when the previous one is about to expire - just click the "Rotate system key" button to create a new system certificate and assign it to the applications of your domain that are currently using the previous system certificate. The applications update is done asynchronously 10 minutes after the certificate generation in order to avoid JWKS caching issues on the client side.

{% hint style="info" %}
See this [documentation page](../../getting-started/configuration/configure-am-api/) for details on how to configure notifications about certificate expiry.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-system-certificates.png" alt=""><figcaption><p>Certificate rotation</p></figcaption></figure>

#### How to configure the applications update

To adapt the duration of the applications update after a system certificate generation, update the `domains.certificates.default.refresh` section in the `gravitee.yaml` file of the Management API service.

{% code overflow="wrap" %}
```yaml
domains:
  certificates:
    default:
      keysize: 2048
      alias: default
      keypass: gravitee
      storepass: gravitee
      validity: 365             # Validity of the certificate
      algorithm: SHA256withRSA  # Algorithm used to sign certificate
      name: cn=Gravitee.io      # Certificate X.500 name
      # Refresh section is used to define the delay between a system certificate renewal and the applications update to use this new certificate
      refresh:
        delay: 10
        timeUnit: MINUTES
```
{% endcode %}

You can define these properties in the `values.yaml` file of the AM Helm Chart.

```yaml
api:
  domains:
    certificates:
      default:
        keysize: 2048
        alias: default
        keypass: gravitee
        storepass: gravitee
        validity: 365             # Validity of the certificate
        algorithm: SHA256withRSA  # Algorithm used to sign certificate
        name: cn=Gravitee.io      # Certificate X.500 name
        refresh:
          delay: 10
          timeUnit: MINUTES
```

### Certificate Fallback

Certificate fallback provides a resilience mechanism for JSON Web Token (JWT) signing operations in Gravitee Access Management (AM). When a client's configured certificate fails to load, the system can automatically fall back to a domain-level certificate before resorting to default Hash-based Message Authentication Code (HMAC) signing or failure. This feature improves service availability and gives administrators fine-grained control over certificate selection hierarchy.

#### Certificate Selection Hierarchy

AM follows a deterministic fallback chain when signing JWTs:

1. **Primary certificate**: The client's configured certificate
2. **Domain fallback certificate**: A domain-level certificate configured in certificate settings (if present)
3. **Default HMAC certificate**: Used only if `fallbackToHmacSignature` is enabled
4. **Failure**: Throws `TemporarilyUnavailableException` if all options are exhausted

The system skips the fallback certificate if its ID matches the primary certificate ID, preventing infinite loops.

#### Domain Scope Rules

Certificate access follows domain boundaries:

| Domain Type | Access Scope |
|:------------|:-------------|
| Master domain | All certificates across all domains (for cross-domain introspection) |
| Regular domain | Only certificates belonging to that domain |

#### Prerequisites

- AM domain with at least one non-system certificate configured
- `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization
- For fallback to activate: client certificate must be configured but unavailable (expired, deleted, or failed to load)

#### Configure Certificate Fallback via Console

1. Navigate to your domain's certificate settings.
2. Select a fallback certificate from the dropdown. The dropdown now includes system certificates (previously filtered out).
3. Click **Save** to activate the fallback.

Changes propagate immediately to all gateway nodes without requiring a domain restart.

#### Configure Certificate Fallback via Management API

Send a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body:

```json
{
  "fallbackCertificate": "certificate-id"
}
```

The endpoint returns the updated domain object (200 OK) or 500 on error.

#### JWT Signing Behavior

When signing a JWT, the system:

1. Attempts to use the client's configured certificate.
2. If that fails, retrieves the domain's fallback certificate (if configured).
3. Filters out the fallback certificate if its ID matches the primary certificate ID.
4. Logs a warning message including both certificate IDs: `"Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"`.
5. If the fallback certificate also fails, propagates the original error.
6. If no fallback is configured, checks whether HMAC fallback is allowed before throwing `TemporarilyUnavailableException`.

#### Restrictions

- Fallback certificate must belong to the same domain (except for master domains, which can access all certificates)
- Fallback certificate ID must not be null or empty string
- Fallback certificate must exist in the certificate manager at the time of use
- System does not validate that the fallback certificate is valid or non-expired at configuration time (validation occurs at signing time)
- If the fallback certificate ID matches the primary certificate ID, the fallback is skipped to prevent infinite loops
- HMAC fallback (if enabled) is only attempted after the domain fallback certificate fails or is unavailable
- Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission

### Gateway Configuration

#### Certificate Settings (Domain-Level)

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | `null` | Certificate ID to use when the primary certificate fails to load |

Certificate settings are stored at the domain level and managed independently of the domain configuration. Updates to certificate settings don't trigger a domain reload.

### Configuring Certificate Fallback

Navigate to your domain's certificate settings and select a fallback certificate from the dropdown. The dropdown now includes system certificates (previously filtered out). Save the settings to activate the fallback.

Alternatively, use the Management API (Application Programming Interface):

```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '{"fallbackCertificate": "certificate-id"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

The endpoint returns the updated domain object (200 OK) or 500 on error. Changes propagate immediately to all gateway nodes without requiring a domain restart.

### JWT Signing with Fallback

When signing a JWT (JSON Web Token), the system first attempts to use the client's configured certificate. If that fails, it retrieves the domain's fallback certificate (if configured) and filters it out if it matches the primary certificate ID. The system logs a warning message including both certificate IDs:

```
Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}
```

If the fallback certificate also fails, the system propagates the original error. If no fallback is configured, the system checks whether HMAC fallback is allowed before throwing `TemporarilyUnavailableException`.

### Client Configuration

### Architecture Notes

#### Thread-Safe State Management

Certificate settings are stored in an `AtomicReference<CertificateSettings>` for thread-safe updates. This ensures that concurrent requests see a consistent view of the fallback configuration even during updates.

#### Event-Driven Updates

The `DomainCertificateSettingsEvent` propagates certificate setting changes across all gateway nodes without requiring a full domain reload. This event-driven approach maintains consistency across distributed gateway instances while minimizing operational disruption.

#### Non-Disruptive Updates

The dedicated certificate settings API endpoint (`PUT /domains/{domain}/certificate-settings`) updates only the certificate fallback configuration. This avoids the overhead and risk of reloading the entire domain configuration, making fallback changes safe to perform during production traffic.

#### Logging Strategy

All fallback scenarios emit WARN-level log messages with certificate IDs. When a client certificate fails to load and a fallback is used, the log message is:

```
Certificate: {clientCert} not loaded, using: {fallbackCert} as fallback
```

When falling back to the default HMAC certificate, the message is:

```
Certificate: {clientCert} not loaded, using default certificate as fallback
```

These messages provide clear audit trails for troubleshooting certificate issues.

### Restrictions

See [Restrictions](#restrictions) above for details.
### Related Changes

Three new permission types were added to support protected resource management: `PROTECTED_RESOURCE_SETTINGS`, `PROTECTED_RESOURCE_OAUTH`, and `PROTECTED_RESOURCE_CERTIFICATE`. The domain settings UI (User Interface) now includes system certificates in the fallback certificate selection dropdown (previously filtered out). The Management API schema was extended with the new certificate settings endpoint, which returns the updated domain object on success. All certificate fallback events are logged at WARN level with certificate IDs for operational visibility.

