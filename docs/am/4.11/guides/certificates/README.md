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

Certificate fallback enables Access Management domains to specify a backup certificate for JWT signing operations. When the primary certificate fails to load or sign a token, the gateway automatically attempts the fallback certificate before resorting to the default HMAC certificate. This improves resilience during certificate rotation or temporary availability issues.

#### Fallback Hierarchy

The gateway evaluates certificates in three tiers:

1. The client's configured certificate
2. The domain-level fallback certificate
3. The default HMAC certificate (if `fallbackToHmacSignature` is enabled)

The fallback certificate is only used when it differs from the primary certificate. If all options are exhausted and HMAC fallback is disabled, the gateway throws a `TemporarilyUnavailableException`.

#### Runtime Configuration

Certificate settings can be updated via the Management API without triggering a full domain reload. The gateway subscribes to `DomainCertificateSettingsEvent.UPDATE` events and reloads settings from the database when changes occur. This allows administrators to adjust fallback behavior during certificate rotation without downtime.

#### Master Domain Access

Master domains can reference certificates from any domain in the organization (for cross-domain introspection). Non-master domains can only access certificates within their own domain scope.

#### Prerequisites

* Access Management gateway running with certificate management enabled
* At least one certificate configured in the domain (beyond the default HMAC certificate)
* `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization
*

#### Gateway Configuration

Configure the fallback certificate at the domain level. This setting is stored in the `Domain` model and can be updated independently of other domain properties.

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificateSettings.fallbackCertificate` | ID of the certificate to use when the primary certificate fails | `"cert-abc123"` |

The fallback certificate must exist in the domain's certificate store. For master domains, the certificate can belong to any domain in the organization.

#### Configure Certificate Fallback

To enable fallback behavior, update the domain's certificate settings via the Management API or Console UI.

**Using AM Console:**

1. Navigate to **Domain Settings → Certificates**.
2. Select a fallback certificate from the dropdown.
3. Click **Save** to activate the fallback.

**Using AM API:**

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '{"fallbackCertificate": "<certificate-id>"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```
{% endcode %}

The gateway immediately subscribes to the change and reloads settings without restarting the domain.

#### JWT Signing with Fallback

When the gateway encodes a JWT, it first attempts to sign with the client's configured certificate. If that certificate is null, the gateway uses the default certificate immediately. If the primary certificate fails to load, the gateway retrieves the domain-level fallback certificate and logs a warning:

```
Certificate: {id} not loaded, using: {fallbackId} as fallback
```

If the fallback certificate also fails and HMAC fallback is disabled, the gateway throws a `TemporarilyUnavailableException`.

### JWT Signing with Fallback

When the gateway encodes a JWT, it follows a deterministic fallback sequence to ensure token signing succeeds even when the primary certificate is unavailable.

#### Fallback Logic

The gateway attempts to sign JWTs using the following sequence:

1. **Primary certificate**: The certificate configured for the client application.
2. **Fallback certificate**: The domain-level fallback certificate (if configured and different from the primary).
3. **Default HMAC certificate**: The system-generated HMAC certificate (if `fallbackToHmacSignature` is enabled).

#### Fallback Triggers

The gateway invokes fallback logic under the following conditions:

**Null primary certificate**
If the client's configured certificate is null, the gateway immediately uses the default HMAC certificate without attempting fallback.

**Certificate load failure**
If the primary certificate fails to load from the certificate store, the gateway retrieves the domain-level fallback certificate and logs:

```
Certificate: {id} not loaded, using: {fallbackId} as fallback
```

If the fallback certificate also fails to load:
- When `fallbackToHmacSignature` is `true`: The gateway falls back to the default HMAC certificate and logs:
  ```
  Certificate: {id} not loaded, using default certificate as fallback
  ```
- When `fallbackToHmacSignature` is `false`: The gateway throws a `TemporarilyUnavailableException` and the signing operation fails.

**Signing operation failure**
If the primary certificate loads successfully but fails during the signing operation, the gateway attempts to use the fallback certificate and logs:

```
Failed to sign JWT with certificate: {id}, attempting fallback using: {fallbackId}
```

The same HMAC fallback logic applies if the fallback certificate also fails during signing.

#### Mutual Exclusion Logic

The gateway only invokes the fallback certificate when it differs from the primary certificate. Certificate IDs are compared using `Objects.equals(fallback.getCertificateInfo().certificateId(), certificateProvider.getCertificateInfo().certificateId())`. If the IDs match, the gateway skips the fallback tier and progresses directly to the default HMAC certificate (when enabled).

This prevents redundant fallback attempts and ensures the gateway does not retry the same certificate twice.

#### HMAC Fallback Control

The `fallbackToHmacSignature` flag controls whether the gateway can fall back to the default HMAC certificate when both the primary and fallback certificates fail. When this flag is disabled, the gateway throws a `TemporarilyUnavailableException` instead of using HMAC, forcing administrators to resolve certificate issues before JWT signing can succeed.

### Event-Driven Settings Updates

The gateway uses an event-driven architecture to propagate certificate settings changes across distributed deployments. When an administrator updates the fallback certificate via the Management API, the system publishes a `DomainCertificateSettingsEvent.UPDATE` event. All gateway nodes subscribed to this event reload the settings from the database without requiring a full domain restart.

This ensures zero-downtime configuration changes and allows administrators to adjust fallback behavior during certificate rotation without service interruption.

### Master Domain Access

Master domains can reference certificates from any domain in the organization, enabling cross-domain introspection scenarios. Non-master domains can only access certificates within their own domain scope. This restriction applies to both primary and fallback certificate configurations.

### Troubleshooting certificate fallback

When the gateway encounters certificate failures during JWT signing, it logs detailed warnings to help you diagnose and resolve issues. Understanding these log messages and the fallback behavior enables you to maintain token signing reliability during certificate rotation or availability problems.

#### Interpreting fallback warnings

The gateway emits two types of warnings when fallback logic is triggered:

**Certificate load failure**
When the primary certificate fails to load, the gateway logs:

```
Certificate: {id} not loaded, using: {fallbackId} as fallback
```

This indicates the gateway could not retrieve or initialize the primary certificate and has switched to the configured fallback certificate.

**Certificate signing failure**
When the primary certificate loads successfully but fails during the signing operation, the gateway logs:

```
Failed to sign JWT with certificate: {id}, attempting fallback using: {fallbackId}
```

This indicates the primary certificate is accessible but encountered an error while signing the token payload.

Both warnings include the certificate IDs involved, allowing you to correlate log entries with your certificate configuration.

#### Handling exhausted fallback options

If all fallback options are exhausted and `fallbackToHmacSignature` is disabled, the gateway throws a `TemporarilyUnavailableException` and the JWT signing operation fails. This exception indicates:

- The primary certificate failed to load or sign.
- The fallback certificate (if configured) also failed.
- HMAC fallback is disabled, preventing the gateway from using the default certificate.

To resolve this:

1. Verify the primary and fallback certificates exist in the domain's certificate store.
2. Check certificate validity periods and ensure they have not expired.
3. Review gateway logs for specific error details about why each certificate failed.
4. If certificate rotation is in progress, enable `fallbackToHmacSignature` temporarily to maintain availability while updating certificates.
5. Confirm the fallback certificate ID matches an existing certificate in the domain (or organization, for master domains).

#### Common failure scenarios

**Mismatched certificate IDs**
If the fallback certificate ID does not exist in the domain's certificate store, the gateway skips the fallback and proceeds directly to the default HMAC certificate (if enabled). Verify the fallback certificate ID in **Domain Settings → Certificates** matches an available certificate.

**Identical primary and fallback certificates**
The gateway skips the fallback if the primary and fallback certificate IDs are identical. This prevents redundant fallback attempts. Ensure the fallback certificate differs from the primary certificate.

**Master domain scope issues**
Non-master domains can only reference certificates within their own domain. If a non-master domain attempts to use a fallback certificate from another domain, the gateway ignores the fallback. Master domains can reference certificates from any domain in the organization.

### Event-driven settings updates

The gateway uses an event-driven architecture to propagate certificate settings changes across distributed nodes. When an administrator updates the fallback certificate via the Management API, the system publishes a `DomainCertificateSettingsEvent.UPDATE` event. All gateway nodes subscribed to this event reload the settings from the database without requiring a full domain restart. This ensures zero-downtime configuration changes across distributed deployments.

The event subscription mechanism allows the gateway to respond immediately to certificate settings updates. When the Management API processes a certificate settings change, it persists the new configuration to the database and broadcasts the `UPDATE` event. Each gateway node receives the event, queries the updated settings, and applies them to the in-memory domain configuration. This approach eliminates the need for manual domain restarts or configuration file updates when adjusting fallback behavior during certificate rotation.
