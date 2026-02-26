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

### Certificate Settings API

AM provides a dedicated endpoint for updating certificate settings independently of full domain updates:

```
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

This endpoint allows you to modify certificate fallback configuration without triggering a full domain reload. The response returns the updated domain object with the new certificate settings applied.

**Required permission**: `DOMAIN_SETTINGS[UPDATE]`

### Creating a Subscription with Certificate Fallback

When a client application is configured with a certificate, the system automatically applies fallback logic during JWT signing and certificate provider resolution. The fallback sequence operates as follows:

1. **Primary certificate attempt**: The system attempts to use the configured certificate.
2. **Fallback certificate attempt**: If the primary certificate fails, the system logs a warning (`"Certificate: {clientCert} not loaded, using: {fallbackId} as fallback"`) and attempts to use the fallback certificate.
3. **HMAC fallback** (if enabled): If the fallback certificate also fails and `fallbackToHmacSignature = true`, the system falls back to the default HMAC certificate with another warning log.
4. **Exception**: If all attempts fail, the system throws a `TemporarilyUnavailableException`.

### Architecture Notes

#### Atomic State Management

The system uses `AtomicReference<CertificateSettings>` to ensure thread-safe updates to certificate settings. When the domain repository fetches an updated domain, the certificate settings reference is updated atomically without requiring a domain restart.

#### JWT Signing Fallback

The `JWTServiceImpl` implements fallback logic for JWT encoding. When signing fails with the primary certificate, the service attempts to use the fallback certificate (if different from the original). If the fallback also fails or is the same as the original, the error is propagated. A warning is logged whenever the fallback is used.

### Restrictions

- Fallback certificate must belong to the same domain (except for master domains, which can access certificates from any domain)
- Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission
- System certificates are now selectable as fallback certificates in the UI (previously filtered out)
- If `fallbackToHmacSignature = false`, the system will throw an exception if both primary and fallback certificates fail
- Certificate loading failures trigger warning logs but don't prevent fallback attempts

### New Permission Types

The following permission types were added to support protected resource settings:

- `PROTECTED_RESOURCE_SETTINGS`
- `PROTECTED_RESOURCE_OAUTH`
- `PROTECTED_RESOURCE_CERTIFICATE`

Existing permission descriptions were updated to use more granular permission names. For example, `PROTECTED_RESOURCE[READ]` is now represented as `PROTECTED_RESOURCE_MEMBER[READ]`.

### Related Changes

The UI certificate selection filter was updated to include system certificates, aligning with backend capabilities. This change allows system certificates to be selected as fallback certificates in the certificate settings interface.

### Certificate fallback for domains

Certificate fallback allows domains to specify a backup certificate when the primary client certificate fails to load or is unavailable. This prevents service disruption during certificate rotation or temporary unavailability by providing a domain-level fallback before reverting to the default HMAC certificate.

#### Certificate selection hierarchy

When a client certificate is requested, the system follows this fallback chain:

1. The client's configured certificate
2. The domain's fallback certificate (if configured)
3. The domain's default HMAC certificate (only if `fallbackToHmacSignature = true`)
4. A `TemporarilyUnavailableException` if all options are exhausted

This hierarchy provides graceful degradation and prevents immediate failures during certificate issues.

#### Prerequisites

- Valid certificate IDs for both primary and fallback certificates
- `DOMAIN_SETTINGS[UPDATE]` permission on domain, environment, or organization level
- Fallback certificate must be loaded and available in the domain

#### Configure certificate fallback

To configure a fallback certificate, send a PUT request to the certificate settings endpoint:

```sh
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

Request body:

```json
{
  "fallbackCertificate": "backup-cert-id"
}
```

The system updates only certificate settings without triggering a full domain reload. The response returns the updated domain object with certificate settings.

#### Fallback behavior

When a client application is configured with a certificate, the system automatically applies the fallback logic during JWT signing and certificate provider resolution:

1. If the primary certificate fails, the system logs a warning (`"Certificate: {clientCert} not loaded, using: {fallbackId} as fallback"`) and attempts to use the fallback certificate.
2. If the fallback also fails and `fallbackToHmacSignature = true`, the system falls back to the default HMAC certificate with another warning log.
3. If all attempts fail, the system throws a `TemporarilyUnavailableException`.

#### Restrictions

See [Restrictions](#restrictions) above for details.
