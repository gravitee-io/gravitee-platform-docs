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

### Certificate Fallback for JWT Signing

Certificate fallback enables AM domains to automatically switch to a backup certificate when the primary certificate fails to load or sign JWTs. Administrators configure fallback certificates at the domain level via the Management API or Console, improving service resilience without requiring domain restarts.

#### Certificate Selection Hierarchy

When a client application or API requests JWT signing, the gateway attempts certificate resolution in this order:

1. Client-configured certificate
2. Domain fallback certificate
3. Default HMAC certificate (if `fallbackToHmacSignature=true`)
4. Fail with `TemporarilyUnavailableException`

The fallback certificate must differ from the original to prevent infinite loops.

#### Master Domain Privileges

Master domains can access certificates from any domain in the organization, enabling cross-domain introspection and centralized certificate management. Regular domains can only access certificates within their own scope.

#### Event-Driven Configuration

Certificate settings updates propagate via `DomainCertificateSettingsEvent` without triggering a full domain reload, allowing runtime configuration changes with minimal service disruption.

#### Prerequisites

* AM domain with at least one non-system certificate configured
* `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization
* Certificate IDs for both primary and fallback certificates

#### Gateway Configuration

Configure fallback behavior at the domain level using the Management API or Console.

**Domain Certificate Settings**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | `null` | Certificate ID to use when primary certificate fails |

**Management API Endpoint:**

```http
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

**Request Body:**

```json
{
  "fallbackCertificate": "cert-backup-2024"
}
```

**Response (200):**

```json
{
  "certificateSettings": {
    "fallbackCertificate": "cert-backup-2024"
  }
}
```

#### Creating a Certificate Fallback Configuration

1. In AM Console, navigate to the domain's certificate settings.
2. Open the certificate selection dialog.
3. Choose a fallback certificate from the dropdown (system certificates are included).
4. Click **SAVE**.

The change takes effect immediately without restarting the domain. The gateway logs fallback usage at WARN level:

```
Failed to sign JWT with certificate: {original}, attempting fallback using: {fallback}
```

#### Architecture Notes

**JWT Signing Flow**

When `JWTServiceImpl.encodeWithFallback()` encounters a signing error, it retrieves the fallback certificate from `CertificateManager.fallbackCertificateProvider()`, filters out matches to the original certificate, and attempts signing. If the fallback fails or is unavailable, the original error is returned.

**Certificate Provider Resolution**

`CertificateManager.getClientCertificateProvider()` implements the selection hierarchy. If a client has no configured certificate, the default provider is used. If the client certificate fails to load, the system attempts the fallback certificate before falling back to HMAC (if enabled) or throwing `TemporarilyUnavailableException`.

**Validation and Filtering**

Fallback certificate IDs must be non-empty and exist in the certificate manager. The system returns an empty `Maybe` if validation fails, allowing graceful degradation. Master domains bypass domain-scoped filtering when accessing certificates.

#### Restrictions

* Fallback certificate must differ from the primary certificate (prevents infinite loops)
* Regular domains can only access certificates within their own domain scope
* Master domains can access certificates from all domains
* Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission
*
*
*

#### Related Changes

The Management Console certificate selection UI now includes system certificates in the fallback dropdown (previously filtered out). Certificate settings updates emit `DomainCertificateSettingsEvent` with action `UPDATE` and scope `DOMAIN_CERTIFICATE_SETTINGS`, enabling event-driven configuration propagation across gateway nodes.

Fallback usage generates WARN-level logs for operational visibility:

```
Certificate: {original} not loaded, using: {fallback} as fallback
Certificate: {original} not loaded, using default certificate as fallback
```

### Validation and filtering

Fallback certificate IDs must be non-empty and exist in the certificate manager. The system returns an empty `Maybe` if validation fails, allowing graceful degradation. Master domains bypass domain-scoped filtering when accessing certificates.

#### Restrictions

See [Restrictions](#restrictions) above for details.
#### Related changes

See [Related changes](#related-changes) above for details.
### Event-driven configuration

See [Event-driven configuration](#event-driven-configuration) above for details.
#### Prerequisites

See [Prerequisites](#prerequisites) above for details.
#### Gateway configuration

### Master domain privileges

See [Master domain privileges](#master-domain-privileges) above for details.
### Architecture notes

#### JWT signing flow

When `JWTServiceImpl.encodeWithFallback()` encounters a signing error, it:

1. Retrieves the fallback certificate from `CertificateManager.fallbackCertificateProvider()`
2. Filters out matches to the original certificate
3. Attempts signing with the fallback certificate

If the fallback signing fails or no fallback certificate is available, the original error is returned.

#### Certificate provider resolution

`CertificateManager.getClientCertificateProvider()` implements the certificate selection hierarchy:

1. If a client has a configured certificate, that certificate is used
2. If no client certificate is configured, the default provider is used
3. If the client certificate fails to load, the system attempts the fallback certificate
4. If the fallback certificate is unavailable or fails, the system falls back to HMAC (if enabled)
5. If HMAC is not enabled, a `TemporarilyUnavailableException` is thrown

#### Validation and filtering

See [Validation and filtering](#validation-and-filtering) above for details.
### Overview

Certificate fallback enables AM domains to automatically switch to a backup certificate when the primary certificate fails to load or sign JWTs. Configure fallback certificates at the domain level using the Management API to improve service resilience without requiring domain restarts.

### Related changes

See [Related changes](#related-changes) above for details.
### Restrictions

See [Restrictions](#restrictions) above for details.
### Domain Certificate Settings

Configure fallback behavior at the domain level using the Management API or AM Console.

#### Configuration Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | `null` | Certificate ID to use when primary certificate fails |

#### Management API Configuration

Use the following endpoint to configure domain certificate settings:

```http
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

**Request Body:**

```json
{
  "fallbackCertificate": "cert-backup-2024"
}
```

**Response (200):**

```json
{
  "certificateSettings": {
    "fallbackCertificate": "cert-backup-2024"
  }
}
```

### Key concepts

#### Certificate selection hierarchy

See [Certificate selection hierarchy](#certificate-selection-hierarchy) above for details.
#### Master domain privileges

See [Master domain privileges](#master-domain-privileges) above for details.
#### Event-driven configuration

See [Event-driven configuration](#event-driven-configuration) above for details.
### Prerequisites

See [Prerequisites](#prerequisites) above for details.
