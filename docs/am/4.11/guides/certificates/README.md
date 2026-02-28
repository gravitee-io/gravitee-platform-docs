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

### Overview

The certificate fallback feature provides a configurable safety mechanism for JWT signing operations in Gravitee Access Management. When a client's primary certificate fails to load or sign a JWT, the system can automatically attempt a domain-level fallback certificate before resorting to the default HMAC certificate or failing completely. This improves service resilience while maintaining security controls for API authentication workflows.

### Certificate selection hierarchy

When signing JWTs or resolving client certificates, the system follows a three-tier hierarchy:

| Priority | Certificate Source | Condition |
|:---------|:-------------------|:----------|
| 1 | Client-specific certificate | `client.getCertificate()` is set and successfully loaded |
| 2 | Fallback certificate | Configured in `certificateSettings.fallbackCertificate` |
| 3 | Default HMAC certificate | Only if `fallbackToHmacSignature == true` |

If all three options fail or are unavailable, the system throws a `TemporarilyUnavailableException`.

### Fallback scope

Fallback certificates are configured at the domain level and apply to all clients within that domain. Master domains can access certificates from any domain for cross-domain introspection. Regular domains can only use certificates belonging to their own domain ID.

### Mutual exclusion

If the fallback certificate ID matches the primary certificate ID, the fallback step is skipped to prevent infinite loops.

### Prerequisites

- Access Management gateway version
- User account with `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization
- At least one valid certificate uploaded to the domain to serve as the fallback
-

### Configure the fallback certificate

Configure the fallback certificate using the Management API:

```http
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

**Request body:**

```json
{
  "fallbackCertificate": "cert-abc-123"
}
```

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificateSettings.fallbackCertificate` | ID of the certificate to use when primary certificate fails | `"cert-abc-123"` |

The endpoint updates only certificate settings without triggering a full domain reload. Changes propagate to gateway nodes via the `DOMAIN_CERTIFICATE_SETTINGS` event.

### Enable fallback behavior

To enable fallback behavior, send a PUT request to the certificate settings endpoint with the ID of an existing certificate. The certificate must belong to the current domain or be accessible if the domain is a master domain. Once configured, the gateway will automatically attempt the fallback certificate whenever a client's primary certificate fails to load or sign a JWT. No gateway restart is required—settings updates propagate via the event system.

### JWT signing with fallback

When encoding a JWT, the system first attempts to sign using the primary certificate provider. On error, it queries the certificate manager for a fallback provider, filters out cases where the fallback ID matches the primary ID, and logs a warning: `"Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"`. If the fallback certificate also fails or is unavailable, the original error is returned. This logic is implemented in `JWTServiceImpl.encodeJwtWithFallback()`.

### Client certificate resolution

When resolving a client certificate:

1. If `client.getCertificate()` is `null`, return the default certificate immediately.
2. Attempt to load the client certificate by ID.
3. On failure:
   - Try the fallback certificate.
   - Log warning: `"Certificate: {clientCertId} not loaded, using: {fallbackId} as fallback"`.
4. If the fallback is unavailable:
   - If `fallbackToHmacSignature == true`, use the default certificate.
   - Log warning: `"Certificate: {clientCertId} not loaded, using default certificate as fallback"`.
   - Otherwise, throw `TemporarilyUnavailableException`.

## Overview

The certificate fallback feature provides a configurable safety mechanism for JWT signing operations in Gravitee Access Management. When a client's primary certificate fails to load or sign a JWT, the system can automatically attempt a domain-level fallback certificate before resorting to the default HMAC certificate or failing completely. This improves service resilience while maintaining security controls for API authentication workflows.

### Event-driven settings updates

Certificate settings updates trigger a `DOMAIN_CERTIFICATE_SETTINGS` event with action `UPDATE`. Gateway nodes listen for this event and reload certificate settings from the repository without restarting the domain. Event listeners are registered in `CertificateManagerImpl.doStart()` and unregistered in `CertificateManagerImpl.doStop()`.

### Certificate visibility rules

Master domains can access all certificates in the system for cross-domain introspection. Regular domains can only access certificates where `certificate.domain.getId()` matches their own domain ID. This is enforced in `CertificateManagerImpl.belongsToCurrentDomain()`.

### Configuring a fallback certificate

To enable fallback behavior, send a PUT request to the certificate settings endpoint with the ID of an existing certificate. The certificate must belong to the current domain (or be accessible if the domain is a master domain). Once configured, the gateway automatically attempts the fallback certificate whenever a client's primary certificate fails to load or sign a JWT. No gateway restart is required—settings updates propagate via the event system.

### JWT signing with fallback

See [JWT signing with fallback](#jwt-signing-with-fallback) above for details.
### Client certificate resolution

See [Client certificate resolution](#client-certificate-resolution) above for details.
### Restrictions

- Fallback certificate must belong to the current domain (unless the domain is a master domain)
- If fallback certificate ID equals the primary certificate ID, fallback is skipped
- Fallback certificate must be successfully loaded; if it fails, the system proceeds to the default HMAC certificate (if enabled) or throws an error
- Requires `DOMAIN_SETTINGS[UPDATE]` permission to configure fallback settings
-
-

### Related changes

The Management API OpenAPI schema now includes `CertificateSettings` with a `fallbackCertificate` property and a new PUT endpoint for updating certificate settings. Three new permission types were added: `PROTECTED_RESOURCE_SETTINGS`, `PROTECTED_RESOURCE_OAUTH`, and `PROTECTED_RESOURCE_CERTIFICATE`. The UI certificate selection dialog was updated to include system certificates (previously filtered out). All fallback scenarios now emit warning-level logs with certificate IDs for troubleshooting.
