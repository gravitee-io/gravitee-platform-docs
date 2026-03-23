# Certificates

## Overview

Cryptographic algorithms such as KeyStore (private/public key) are used to sign using JSON-based data structures (JWT) tokens. Certificates are used as part of the OAuth 2.0 and OpenID Connect protocol to sign access, create and renew ID tokens and ensure the integrity of a token's payload.

Certificate definitions apply at the _security domain_ level.

By default AM is able to load certificate using JKS or PKCS12 format you can upload using the console or the REST API. An Enterprise plugin also exists to load PKCS12 certificate from [AWS Secret Manager](aws-certificate-plugin.md).

Certificate fallback enables administrators to configure a domain-level fallback certificate that is used when an application's primary signing certificate fails to load. This feature prevents authentication failures when external certificate providers (such as AWS CloudHSM) become unavailable.

Administrators can configure fallback certificates per security domain and optionally enable HMAC signing as a final fallback.

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
6. Click **Create**.

<figure><img src="../../../4.10/.gitbook/assets/image (132).png" alt=""><figcaption></figcaption></figure>

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
2. Next to your certificate, click the key icon.

<figure><img src="../../../4.10/.gitbook/assets/image (134).png" alt=""><figcaption></figcaption></figure>

3. You can copy/paste the public key to use with third-party libraries to verify your tokens.

<figure><img src="../../../4.10/.gitbook/assets/image (135).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Gravitee API Management (APIM) comes with a JWT Policy to verify and decode tokens that can be used for your APIs.
{% endhint %}

### Apply the certificate to your application

1. In AM Console, click and choose your **Application**.
2. In the **Settings** tab, click **Secrets & Certificates** tab.
3. Choose your certificate and click **SAVE**.

<figure><img src="../../../4.10/.gitbook/assets/image (136).png" alt=""><figcaption></figcaption></figure>

### Certificate for Mutual TLS authentication <a href="#certificate-for-mutual-tls-authentication" id="certificate-for-mutual-tls-authentication"></a>

To mark a certificate as usable for mTLS, you just have to check the "mTLS" usage in the configuration form of your certificate.

{% hint style="info" %}
System certificates can't be used for mTLS authentication as they are self signed certificates generated internally by Access Management.
{% endhint %}

<figure><img src="../../../4.10/.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

### Fallback certificates
A fallback certificate provides a safety net for JWT signing within a security domain. When configured, AM will automatically use the fallback certificate if the primary certificate (selected at the application level or the domain default) fails to sign a token or fails to load entirely.

This is particularly useful in environments that rely on external signing infrastructure, such as AWS CloudHSM, where transient connectivity or availability issues could otherwise cause token generation to fail entirely.

#### How the resolution chain works
When AM needs to sign a JWT token for an application, it follows this resolution chain:
1. **Application-level certificate** - The certificate explicitly assigned to the application is used first.
2. **Domain fallback certificate** - If signing with the application certificate fails (signing error or certificate loading error) AM attempts to sign with the domain's configured fallback certificate.
3. **Legacy HMAC fallback** - If no fallback certificate if configured and the Legacy HMAC flag is enabled, AM falls back to the default HMAC-based certificate provider.
4. **Failure** - If none of the above succeed, the signing operation fails and the token request returns an error.

#### Configure a fallback cerificate using the Access Management Console

**Prerequisites** 

* At least two certificates must already exist within the domain.
* You must have the **DOMAIN_SETTINGS[UPDATE]** permission.

**Configure a fallback certificate**

1. Navigate to **Settings > Certificates** in your security domain.
2. Click **Settings**. The **Certificate Settings** dialog box appears.
3. From the **Fallback Certificate** dropdown menu, select a certificate.
4. Click **Confirm**.

{% hint style="info" %}
When configuring a fallback certificate the security domain does not require a full domain reload. The change is applied to the gateway via a lightweight event, so there is no downtime or route redeployment.
{% endhint %}

#### Deletion protection
A certificate that is currently configured as the domain's fallback cannot be deleted. The delete button will be disabled, and hovering over it will show a tooltip with the following text: Cannot delete: certificate is configured as fallback.

To delete a certificate that is marked as fallback, you must comnplete either of the following steps:
* Reassign the fallback to a different certificate
* Clear the fallback certificate selection entirely.

#### Legacy HMAC fallback

AM includes a gateway-level setting that controls whether to fall back to the default HMAC-based certificate provider when no other certificate is available to sign a token. This acts as the last resort in the signing resolution chain, before an outright failure.

{% tabs %}
{% tab title="gravitee.yml" %}
Apply the following configuration to the Gateway gravitee.yml to enable HMAC fallback:

```yml
applications:
  signing:
    fallback-to-hmac-signature: true  # default: false
```

{% endtab %}

{% tab title="Environment Variable" %}
Add the following environment variable to enable HMAC fallback:

```
gravitee_applications_signining_fallbacktohmacsignature=true
```

{% endtab %}
{% endtabs %}

| Property                                          | Default | Description                                                                                                                                                                                                                                 |
| ------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `applications.signing.fallback-to-hmac-signature` | `false`  | When `true`, the gateway falls back to the default HMAC certificate provider if both the application certificate and the domain fallback certificate are unavailable. Set to `false` to disable this behavior and fail immediately instead. |

This setting is enabled by default. The property is commented out in the default gravitee.yml, meaning the default value of true applies unless explicitly overridden.

### Custom certificates

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-custom-certificate.png" alt=""><figcaption><p>Custom certificate diagram</p></figcaption></figure>

AM is designed to be extended based on a pluggable modules architecture. You can develop your own certificate and provide a sign method for tokens.

## Certificate resolution order

When signing OAuth tokens or ID tokens, AM attempts to load certificates in the following order:

1. The application's assigned certificate
2. The domain's fallback certificate (if configured)
3. The default HMAC certificate (if legacy fallback is enabled)

If all options are exhausted, AM returns a `TemporarilyUnavailableException` and logs a warning. When fallback certificates are used, warning-level logs are emitted that include the original certificate ID and the fallback certificate ID being substituted.

## System certificates

When a new domain is created, a certificate is generated for use by the domain applications to sign the tokens. Such certificates are marked as "system" certificates.

System certificates (including default certificates) are visible in the fallback certificate selection dialog, allowing administrators to designate built-in certificates as fallback options.

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

<figure><img src="../../../4.10/.gitbook/assets/image (137).png" alt=""><figcaption></figcaption></figure>

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
