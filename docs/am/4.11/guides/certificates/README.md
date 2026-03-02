# Certificates

## Overview

Cryptographic algorithms such as KeyStore (private/public key) are used to sign using JSON-based data structures (JWT) tokens. Certificates are used as part of the OAuth 2.0 and OpenID Connect protocol to sign access, create and renew ID tokens and ensure the integrity of a token's payload.

Certificate definitions apply at the _security domain_ level.

By default AM is able to load certificate using JKS or PKCS12 format you can upload using the console or the REST API. An Enterprise plugin also exists to load PKCS12 certificate from [AWS Secret Manager](aws-certificate-plugin.md).

Domain-level certificate settings allow administrators to configure a fallback certificate that is automatically used when a client-specific certificate is unavailable or fails to load. This feature prevents service disruptions during certificate rotation or misconfiguration by providing a domain-wide safety net for JWT signing and client authentication operations.

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

### Certificate for Mutual TLS authentication

To mark a certificate as usable for mTLS, you just have to check the "mTLS" usage in the configuration form of your certificate.

{% hint style="info" %}
System certificates can't be used for mTLS authentication as they are self signed certificates generated internally by Access Management.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

### Custom certificates

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-custom-certificate.png" alt=""><figcaption><p>Custom certificate diagram</p></figcaption></figure>

AM is designed to be extended based on a pluggable modules architecture. You can develop your own certificate and provide a sign method for tokens.

## Troubleshooting

### TemporarilyUnavailableException: The certificate cannot be loaded

This exception occurs when the certificate manager cannot load any certificate through the three-tier resolution order:

1. Client-specific certificate (if configured and loadable)
2. Domain fallback certificate (if the client certificate fails)
3. Default HMAC certificate (if fallback is not configured and HMAC fallback is enabled)

**Conditions that trigger this exception:**

* The client-specific certificate is configured but cannot be loaded
* No fallback certificate is configured for the domain
* `fallbackToHmacSignature=false` is set, preventing HMAC fallback
* The fallback certificate is configured but cannot be loaded
* The fallback certificate ID matches the primary certificate ID (preventing retry loops)

**Resolution:**

1. Verify the client-specific certificate exists and is accessible
2. Configure a valid fallback certificate in the domain's certificate settings
3. Ensure the fallback certificate belongs to the domain (or use a master domain)
4. Check that `fallbackToHmacSignature` is enabled if no fallback certificate is configured
5. Review logs for WARN-level messages indicating fallback usage: "Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"

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

## Domain certificate settings

Domain-level certificate settings provide a fallback mechanism for JWT signing and client authentication operations. When a client-specific certificate is unavailable or fails to load, the system automatically uses the configured fallback certificate to prevent service disruptions during certificate rotation or misconfiguration.

### Key concepts

#### Fallback certificate

A domain-wide certificate that serves as a backup when client-specific certificates can't be loaded. The fallback certificate is referenced by ID in the domain's certificate settings and is automatically used by the certificate manager when primary certificates fail. The fallback certificate must belong to the same domain, except for master domains, which can access certificates across all domains.

#### Certificate resolution order

The certificate manager resolves certificates in a three-tier hierarchy:

1. Client-specific certificate if configured and loadable
2. Domain fallback certificate if the client certificate fails
3. Default HMAC certificate if fallback is not configured and HMAC fallback is enabled

If all three fail, the system throws a `TemporarilyUnavailableException` with the message "The certificate cannot be loaded."

#### Domain isolation

Regular domains can only access certificates where the certificate's domain ID matches the current domain ID. Master domains bypass this restriction and can access certificates from any domain for cross-domain introspection purposes. This isolation is enforced in the certificate manager's `belongsToCurrentDomain()` check.

### Prerequisites

Before configuring domain certificate settings, ensure the following:

* The domain exists and is accessible
* The fallback certificate (if configured) exists in the certificate repository
* The fallback certificate belongs to the target domain (unless the domain is a master domain)
* You have `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization to configure certificate settings
* You have `DOMAIN_SETTINGS[READ]` permission to view certificate settings in domain API responses

### Configuration properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificateSettings.fallbackCertificate` | The fallback certificate ID to use when no specific certificate is configured or when the configured certificate fails to load. Set to null or empty string to disable fallback. | `"cert-abc123"` |

### Configure domain certificate settings

Update the domain's certificate settings by sending a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body containing `{"fallbackCertificate": "certificate-id"}`.

The system processes the request as follows:

1. Validates that the certificate exists and belongs to the domain
2. Persists the certificate settings to the domain record if validation passes
3. Publishes a lightweight `DOMAIN_CERTIFICATE_SETTINGS` event to notify certificate managers across the cluster without triggering a full domain reload
4. Updates in-memory settings via the event listener in certificate managers

To disable fallback, set `fallbackCertificate` to null or an empty string.

### JWT signing with fallback

When signing JWTs, the system first attempts to use the primary certificate (client-specific or algorithm-specific).

1. If signing succeeds, the JWT is returned immediately
2. If signing fails and a fallback certificate is configured, the system checks whether the fallback certificate ID differs from the primary certificate ID
3. If the IDs differ, the system attempts to sign with the fallback certificate and logs a warning: "Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"
4. If the fallback succeeds, the JWT is returned
5. If the fallback fails or the fallback certificate ID matches the primary ID, the original error is propagated

This prevents infinite retry loops when the fallback certificate is the same as the failed primary certificate.

### Restrictions

* **Deletion prevention**: A fallback certificate can't be deleted while configured as the domain's fallback certificate. Attempting to delete returns `CertificateIsFallbackException` with HTTP 400 and message "You can't delete a certificate that is configured as the domain's fallback certificate"
* **Domain ownership**: The fallback certificate must belong to the same domain as the domain being configured (unless the domain is a master domain)
* **Non-existent certificate**: Setting a non-existent certificate ID as the fallback returns `InvalidParameterException` with message "Fallback certificate not found: {certificateId}"
* **Permission-based visibility**: Certificate settings are only visible in domain API responses to users with `DOMAIN_SETTINGS[READ]` permission
* **Fallback unavailability**: Certificate fallback doesn't apply if `fallbackToHmacSignature=false` and no fallback certificate is configured (system throws `TemporarilyUnavailableException`)
* **Retry loop prevention**: The fallback certificate isn't used if the primary certificate ID matches the fallback certificate ID
