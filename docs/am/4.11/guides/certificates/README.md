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

### Certificate Fallback Overview

Certificate fallback provides a configurable safety net when primary client certificates fail or become unavailable during JWT signing operations. Administrators can designate a domain-level fallback certificate that the system automatically uses when the primary certificate can't be loaded, improving resilience during certificate rotation or temporary outages without requiring domain restarts.

#### Certificate Selection Hierarchy

When a client requests JWT signing, the system follows a three-tier fallback chain:

1. The client's configured certificate
2. The domain's fallback certificate (if configured)
3. The domain's default HMAC certificate (if `fallbackToHmacSignature` is enabled)

If all options are exhausted, the system throws a `TemporarilyUnavailableException`. Fallback is skipped if the fallback certificate ID matches the primary certificate ID to prevent infinite loops.

| Tier | Source | Condition |
|:-----|:-------|:----------|
| Primary | Client configuration | Always attempted first |
| Fallback | Domain certificate settings | Used when primary fails and fallback is configured |
| Default | Domain HMAC certificate | Used only if `fallbackToHmacSignature = true` |

{% hint style="info" %}
Fallback triggers only on certificate load failure, not signing errors.
{% endhint %}

#### Certificate Visibility Rules

Master domains can access certificates from all domains to support cross-domain introspection scenarios. Regular domains can only access certificates belonging to their own domain. This isolation ensures proper security boundaries while allowing master domains to perform administrative operations across the platform.

#### Hot-Reload Architecture

Certificate settings updates trigger a `DOMAIN_CERTIFICATE_SETTINGS` event that notifies all gateway nodes in real time. Each node reloads its in-memory certificate settings from the repository without requiring a domain restart, enabling zero-downtime certificate configuration changes.

The system uses `AtomicReference` and event manager subscriptions to handle event-driven configuration updates. When a certificate settings change occurs, the event propagates to all gateway nodes, which update their local configuration atomically.

#### JWT Signing Fallback Flow

During JWT signing operations, the gateway uses reactive error handling to implement the fallback chain. When the primary certificate fails to load, the system automatically attempts the fallback certificate. If both fail and HMAC fallback is disabled, the client receives a `temporarily_unavailable` OAuth 2.0 error response.

Gateway logs include `"Certificate: {id} not loaded, using: {fallbackId} as fallback"` warnings to provide operational visibility into fallback activation.

#### Prerequisites

- Domain administrator access with `DOMAIN_SETTINGS[UPDATE]` permission
- At least one certificate loaded and available in the target domain
- Understanding of the domain's certificate rotation schedule and failure scenarios

#### Configuring Certificate Fallback

Configure fallback behavior at the domain level using the Management API. The fallback certificate must exist in the same domain (or be accessible if the domain is a master domain).

**API Endpoint**: `PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`

**Request Body**:
```json
{
  "fallbackCertificate": "cert-backup-2024"
}
```

| Property | Description | Example |
|:---------|:------------|:--------|
| `fallbackCertificate` | ID of certificate to use when primary certificate fails | `"cert-backup-2024"` |

To enable fallback:

1. Send a PUT request to the certificate settings endpoint with the ID of your fallback certificate.
2. The system validates that the certificate exists and is accessible to the domain.
3. The configuration change broadcasts to all gateway nodes via the event system.
4. Monitor gateway logs for fallback activation warnings during certificate failures.

To disable fallback, send the same request with `"fallbackCertificate": null`.

#### Creating a Client with Fallback Protection

When creating or updating a client that requires JWT signing, configure the primary certificate as usual through the client configuration. The fallback mechanism activates automatically when the primary certificate fails to load—no client-side configuration is required. The client continues to receive signed JWTs transparently, with fallback usage logged on the gateway for operational visibility.

### Certificate Visibility in UI Selectors

The certificate selector dialog in the AM Console now displays system certificates alongside user-created certificates. Previously, system certificates were filtered out of the selector interface.

This change supports certificate fallback configuration scenarios where administrators may need to reference system certificates as fallback options. System certificates remain restricted from use in Mutual TLS authentication contexts, as documented in the [Certificate for Mutual TLS authentication](#certificate-for-mutual-tls-authentication) section.

{% hint style="info" %}
System certificates are automatically generated when a domain is created and are marked with a "system" designation in the certificate list.
{% endhint %}