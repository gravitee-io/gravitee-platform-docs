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

## Certificate fallback mechanism

When signing a JWT or providing a client certificate, the system follows a strict priority order to ensure resilience during certificate failures. The fallback mechanism automatically switches to backup certificates when the primary certificate fails to load or sign.

### Prerequisites

Before configuring certificate fallback, ensure you have:

- At least one valid certificate configured in the domain
- `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization
- Understanding of JWT signing algorithms and certificate formats

### Certificate selection hierarchy

The system attempts certificate selection in the following order:

| Priority | Certificate source | Condition |
|:---------|:------------------|:----------|
| 1 | Client-specific certificate | `client.getCertificate()` is set and loaded |
| 2 | Fallback certificate | Configured in `CertificateSettings.fallbackCertificate` |
| 3 | Default HMAC certificate | Only if `fallbackToHmacSignature == true` |
| 4 | Error | Throws `TemporarilyUnavailableException` |

If the client-specific certificate is unavailable, the system falls back to the domain-wide fallback certificate specified in certificate settings. If no fallback is configured and `fallbackToHmacSignature` is enabled, the system uses the default HMAC certificate. If all options are exhausted, the operation fails with a `TemporarilyUnavailableException`.

### Configure certificate fallback

To enable certificate fallback, send a PUT request to the certificate settings endpoint with the ID of your chosen fallback certificate:

```sh
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

Request body:

```json
{
  "fallbackCertificate": "backup-cert-2024"
}
```

The system validates that the certificate exists and is accessible to the domain. Master domains can reference certificates from any domain, while regular domains can only use their own certificates. Once configured, the fallback certificate is stored in an atomic reference and propagated to all gateway nodes via domain events. The configuration takes effect immediately without requiring a domain restart.

To remove the fallback, send an empty or null value for `fallbackCertificate`.

{% hint style="info" %}
Requires `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization.
{% endhint %}

### Gateway configuration

Certificate settings are managed separately from the main domain configuration to allow atomic updates without domain reload.

| Property | Description | Example |
|:---------|:------------|:--------|
| `fallbackCertificate` | ID of the certificate to use when primary certificate fails | `"backup-cert-2024"` |

### Fallback behavior during JWT signing

When a JWT signing operation fails with the primary certificate:

1. The system retrieves the fallback certificate from `CertificateSettings.fallbackCertificate`.
2. The system filters out the fallback certificate if it matches the failed certificate ID to prevent infinite loops.
3. The system logs a warning: `"Failed to sign JWT with certificate: {originalCertId}, attempting fallback using: {fallbackCertId}"`.
4. The system retries signing with the fallback certificate.
5. If the fallback fails, the system propagates the original error.

### Client creation with fallback

When creating or updating a client application, specify the primary certificate ID in the client configuration. If the primary certificate becomes unavailable during JWT signing or certificate provider retrieval, the system automatically attempts to use the domain's fallback certificate.

The fallback is logged at WARN level:

```
Certificate: {clientCertId} not loaded, using: {fallbackCertId} as fallback
```

If the fallback certificate also fails and `fallbackToHmacSignature` is enabled, the system uses the default HMAC certificate as a final fallback:

```
Certificate: {clientCertId} not loaded, using default certificate as fallback
```

If all fallback options are exhausted, the operation fails with `TemporarilyUnavailableException`.

### Master domain privilege

Master domains have special access rights to certificates across all domains, enabling cross-domain introspection and centralized certificate management. Regular domains can only access certificates within their own domain boundary. This distinction is enforced during certificate retrieval and fallback resolution.

### Event-driven configuration updates

Certificate settings changes are propagated to all gateway nodes via `DomainCertificateSettingsEvent` without requiring a domain restart. The event system ensures that fallback certificate configuration updates take effect immediately across the cluster, maintaining consistency and minimizing downtime during configuration changes.

Certificate settings event listeners are registered when a domain starts and unregistered when the domain stops. The listener is scoped to the specific domain ID, ensuring that certificate settings updates only affect the intended domain.

### Atomic configuration updates

Certificate settings are stored in an `AtomicReference<CertificateSettings>` to ensure thread-safe updates without locking. When a certificate settings update event is received, the manager atomically swaps the reference to the new settings object. This design eliminates race conditions during concurrent JWT signing operations while a configuration update is in progress.

### Logging behavior

The system logs fallback usage at WARN level for operational visibility:

- `"Certificate: {clientCertId} not loaded, using: {fallbackCertId} as fallback"` — when falling back from client certificate to fallback certificate
- `"Certificate: {clientCertId} not loaded, using default certificate as fallback"` — when falling back to default HMAC certificate
- `"Failed to sign JWT with certificate: {originalCertId}, attempting fallback using: {fallbackCertId}"` — when retrying JWT signing with fallback certificate

### Restrictions

- Fallback certificate must exist and be accessible to the domain (regular domains cannot reference certificates from other domains unless they are master domains)
- Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission
- System certificates are now included in the UI certificate selection dropdown
- If both primary and fallback certificates fail, and `fallbackToHmacSignature` is disabled, the operation fails with `TemporarilyUnavailableException`
- Fallback certificate cannot be the same as the primary certificate (filtered during fallback resolution)
- Certificate settings updates do not trigger a full domain reload
