# Certificates

## Overview

Cryptographic algorithms such as KeyStore (private/public key) are used to sign using JSON-based data structures (JWT) tokens. Certificates are used as part of the OAuth 2.0 and OpenID Connect protocol to sign access, create and renew ID tokens and ensure the integrity of a token's payload.

Certificate definitions apply at the _security domain_ level.

By default AM is able to load certificate using JKS or PKCS12 format you can upload using the console or the REST API. An Enterprise plugin also exists to load PKCS12 certificate from [AWS Secret Manager](aws-certificate-plugin.md).

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

You can use public keys to verify a token payload's integrity. To obtain the public key for your certificate:

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

## Certificate fallback

The certificate fallback feature provides a domain-level safety mechanism for JWT signing operations. When a client's primary certificate fails or is unavailable, the system automatically falls back to a configured domain certificate. This improves service resilience without requiring manual intervention.

### Certificate resolution hierarchy

When signing a JWT, the system attempts certificate resolution in the following order:

1. Client-specific certificate
2. Domain fallback certificate (if configured)
3. Default HMAC certificate (if `fallbackToHmacSignature` is enabled)
4. Error (`TemporarilyUnavailableException`)

Each fallback attempt is logged at WARN level with certificate IDs for operational visibility.

### Domain certificate settings

Certificate settings are managed independently from other domain configuration. Updates use a dedicated event type (`DOMAIN_CERTIFICATE_SETTINGS`) and apply immediately without triggering a full domain reload. Settings are stored in an `AtomicReference` for thread-safe concurrent access.

### Cross-domain certificate access

Master domains can access certificates from any domain in the organization, enabling cross-domain introspection and centralized certificate management. Regular domains can only access certificates belonging to that domain.

### Thread-safe state management

The certificate settings object is wrapped in an `AtomicReference` to ensure thread-safe reads and updates during concurrent JWT signing operations. This prevents race conditions when fallback certificates are updated while active signing requests are in flight.

{% hint style="info" %}
Thread safety is critical in high-concurrency environments where multiple JWT signing operations may occur simultaneously.
{% endhint %}

### Configure certificate fallback

Use the Management API to enable, update, or disable certificate fallback for a domain. Changes apply immediately without requiring a domain restart.

#### Prerequisites

Before configuring certificate fallback, ensure you have:

- An active Access Management domain
- At least one certificate configured in the domain (or accessible from a master domain)
- `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization

#### API endpoint

```
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

#### Request body schema

| Property | Type | Description |
|:---------|:-----|:------------|
| `fallbackCertificate` | String | Certificate ID to use when primary certificate fails or is unavailable. Set to `null` or empty string to disable fallback. |

#### Enable certificate fallback

To enable fallback, send a PUT request with the fallback certificate ID:

```json
{
  "fallbackCertificate": "cert-abc123"
}
```

**Example:**

```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type: application/json" \
     -X PUT \
     -d '{"fallbackCertificate": "cert-backup-001"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/org1/environments/prod/domains/api-domain/certificate-settings
```

The certificate must exist in the domain. Master domains can use certificates from any domain in the organization.

#### Disable certificate fallback

To disable fallback, set `fallbackCertificate` to `null` or an empty string:

```json
{
  "fallbackCertificate": null
}
```

or

```json
{
  "fallbackCertificate": ""
}
```

#### Behavior notes

- Changes take effect immediately without restarting the domain
- The fallback certificate must belong to the same domain unless the domain is a master domain
- Certificate settings updates emit `DOMAIN_CERTIFICATE_SETTINGS` events for monitoring
- System certificates are now visible in the UI certificate selector and can be selected as fallback certificates

### JWT signing with fallback

When signing a JWT, the system follows this flow:

1. Attempt to sign JWT with the primary certificate provider.
2. On error:
   - Retrieve the fallback certificate from `CertificateManager.fallbackCertificateProvider()`.
   - Filter out the fallback if it matches the failed certificate (prevents infinite loop).
   - Log warning: `"Failed to sign JWT with certificate: {originalId}, attempting fallback using: {fallbackId}"`.
   - Attempt signing with the fallback certificate.
3. If the fallback also fails, return the original error.

### Fallback loop prevention

When a primary certificate fails, the fallback mechanism filters out the fallback certificate if it matches the failed certificate ID. This prevents infinite retry loops when the fallback certificate itself is unavailable.

{% hint style="info" %}
The system automatically excludes a fallback certificate from the retry sequence if its ID matches the ID of the certificate that triggered the fallback. This ensures that unavailable certificates do not cause repeated failures.
{% endhint %}

### Certificate loading warnings

The system logs warnings when fallback certificates are used:

| Scenario | Log Level | Message Template |
|:---------|:----------|:-----------------|
| Primary certificate missing, using fallback | WARN | `"Certificate: {clientCertId} not loaded, using: {fallbackCertId} as fallback"` |
| Primary and fallback missing, using default | WARN | `"Certificate: {clientCertId} not loaded, using default certificate as fallback"` |

### Event-driven settings updates

Certificate settings changes propagate through the system using a dedicated `DOMAIN_CERTIFICATE_SETTINGS` event type. This decouples certificate configuration from full domain lifecycle events, reducing reload overhead and improving update latency.

{% hint style="info" %}
The `DOMAIN_CERTIFICATE_SETTINGS` event type ensures certificate configuration changes are processed independently of broader domain updates, minimizing system impact during certificate management operations.
{% endhint %}

### Restrictions

- The fallback certificate must belong to the same domain unless the domain is a master domain.
- System certificates are now visible and selectable in the fallback certificate dropdown.
- All certificate resolution attempts that fail throw a `TemporarilyUnavailableException`.
- Certificate settings updates propagate through the system using the `DOMAIN_CERTIFICATE_SETTINGS` event type.

