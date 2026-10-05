---
description: Every API Management 4.12 component ships a FIPS image variant alongside its ordinary image. Learn what the FIPS builds provide.
---

# FIPS images

From APIM 4.12.11, each APIM backend and frontend component has a FIPS image variant next to its ordinary image. The FIPS images are built on a FIPS-validated base image. They're intended for deployments that require FIPS 140-3 validated cryptography end to end.

They aren't a drop-in swap. The JVM inside them accepts a narrower set of algorithms and keystore formats than the ordinary images, so a configuration that works elsewhere doesn't always load. This page describes what changes.

{% hint style="info" %}
These images aren't public. They're published to the private Gravitee registry only, so you need credentials before any command on this page works. Contact [Gravitee support](https://www.gravitee.io/contact-us) to have access granted for your organization.
{% endhint %}

## What is different inside

The FIPS images replace the JVM's cryptographic providers:

* BouncyCastle FIPS (`BCFIPS`) is registered as provider 1, and the BouncyCastle JSSE provider (`BCJSSE`) as provider 2.
* `SunJCE` and `SunJSSE` are **absent** from the provider list.
* The JVM runs in BouncyCastle's *approved only* mode (`org.bouncycastle.fips.approved_only=true`), which rejects algorithms outside the validated set, including several that the ordinary images accept without complaint.

The images are based on JDK 21.

For the provider's own documentation, see the [BouncyCastle FIPS Java documentation](https://www.bouncycastle.org/download/bouncy-castle-java-fips/). For the FIPS base images, see the [Chainguard FIPS documentation](https://edu.chainguard.dev/platform/fips/fips-images/).

## Where to find them

FIPS images are published to the **private Gravitee registry only**. They're never pushed to Docker Hub, so `docker pull graviteeio/apim-gateway:<version>-chainguard-fips` won't resolve.

```sh
docker login graviteeio.azurecr.io
docker pull graviteeio.azurecr.io/apim-gateway:4.12-chainguard-fips
```

The tag is the ordinary version tag with the `-chainguard-fips` suffix. It's available for:

| Component | Image |
| --- | --- |
| API Gateway | `graviteeio.azurecr.io/apim-gateway:<version>-chainguard-fips` |
| Management API | `graviteeio.azurecr.io/apim-management-api:<version>-chainguard-fips` |
| Console | `graviteeio.azurecr.io/apim-management-ui:<version>-chainguard-fips` |
| Developer Portal | `graviteeio.azurecr.io/apim-portal-ui:<version>-chainguard-fips` |
| Gamma Console | `graviteeio.azurecr.io/gamma-ui:<version>-chainguard-fips` |

**Contact [Gravitee support](https://www.gravitee.io/contact-us) if you need access to the registry.**

The three UI images are built on a FIPS-validated nginx base rather than a JVM one. They serve static content over plain HTTP, with TLS terminated upstream, so the keystore constraints below concern the Gateway and the Management API only.

## Gateway TLS on the FIPS images

From APIM 4.12.19, the keystores the Gateway builds itself on the FIPS images are BouncyCastle FIPS keystores rather than PKCS12 ones.

So the HTTPS listeners, client certificate authentication, mTLS plans, and the Kafka Gateway listener no longer depend on PKCS12 on these images. The formats that load from a file are listed in the next section.

## Keystore and truststore formats

This is the constraint that most often surprises. Under *approved only* mode, the formats APIM accepts don't all load:

| Format | On the FIPS images |
| --- | --- |
| `pem` | **Works.** The recommended format. |
| `pem-folder` | **Works**, truststores only. It reads the certificates directly rather than opening a keystore file, like `pem`, and `watch` picks up files added, updated, and removed in the directory. |
| `pkcs12` | Loads in memory, but writing a keystore fails on the integrity MAC, which needs `HmacPBESHA256`. That algorithm has no provider once `SunJCE` is gone, and the failure surfaces as `calculateMac failed: Algorithm HmacPBESHA256 not available`. |
| `jks` | Loads, but relies on SUN's SHA-1 based password encryption, which isn't FIPS-approved. Using it defeats the purpose of running the FIPS image. |
| `bcfks` | **Works from APIM 4.12.19.** The BouncyCastle FIPS keystore, designed for approved-only mode. Unlike PKCS12 it's also writable, so it's the option to reach for when you need a single password-protected container rather than separate certificate and key files. |
| `self-signed` | From APIM 4.12.19, the certificate is kept in a BouncyCastle FIPS keystore, so it doesn't go through PKCS12. |

In practice, **configure your keystores and truststores as `pem`**. It needs no password and no conversion tooling. On 4.12.19 and later, `bcfks` is the alternative when you'd rather ship one container file. Earlier 4.12 patches don't accept the type.

The table describes the Gateway's listeners. The Management API's own HTTPS listener reads a `jks` or `pkcs12` keystore only.

The JVM-level trust store is a separate matter: `javax.net.ssl.trustStore` doesn't accept PEM. The FIPS base image carries `-Djavax.net.ssl.trustStoreType=FIPS` in `JDK_JAVA_OPTIONS`, which reads the bundled `cacerts` in compatibility mode. APIM doesn't set it, so this follows the base image rather than a Gravitee decision. It applies to the TLS connections APIM opens to JDBC, Redis, and Elasticsearch or OpenSearch.

### Configure a PEM keystore

Use an unencrypted private key file. An encrypted key fails with `No private key found for the specified pem content.` With Docker, point the listener at the certificate and key files:

```yaml
environment:
  - gravitee_http_secured=true
  - gravitee_http_ssl_keystore_type=pem
  - gravitee_http_ssl_keystore_certificates_0_cert=/certificates/server.crt
  - gravitee_http_ssl_keystore_certificates_0_key=/certificates/server.key
```

With the Helm chart, from chart 4.12.19, use `certificates`, a list of `cert` and `key` pairs:

```yaml
gateway:
  ssl:
    enabled: true
    keystore:
      type: pem
      certificates:
        - cert: /certificates/server.crt
          key: /certificates/server.key
```

The same key exists per listener under `gateway.servers[].ssl.keystore`, from chart 4.12.19 as well, for the Kafka listener under `gateway.kafka.ssl.keystore`, for the rate limit repository under `gateway.ratelimit.redis.keystore`, and for distributed sync under `gateway.distributedSync.redis.keystore`.

### Configure a BCFKS keystore

From APIM 4.12.19, `bcfks` is accepted for a keystore or truststore read from a file `path`, on the HTTP and TCP listeners and the Kafka Gateway listener. Point the store at the file and give its password. The keys inside are read with that same password. With Docker:

```yaml
environment:
  - gravitee_http_secured=true
  - gravitee_http_ssl_keystore_type=bcfks
  - gravitee_http_ssl_keystore_path=/certificates/server.bcfks
  - gravitee_http_ssl_keystore_password=secret
```

With the Helm chart:

```yaml
gateway:
  ssl:
    enabled: true
    keystore:
      type: bcfks
      path: /certificates/server.bcfks
      password: secret
```

The type isn't accepted from a Kubernetes secret or configmap location, or from a secret-provider reference. A `bcfks` store configured that way isn't loaded: the Gateway logs `No loader accepted the store configuration, no certificate will be loaded` and the store stays empty. The Redis stores for rate limiting and distributed sync don't accept it either: they take `jks`, `pkcs12`, and `pem`.

## Known limitations

Because the non-FIPS BouncyCastle provider isn't present, a few capabilities that ship inside third-party libraries lose their cryptographic backing on the FIPS images. None of them affect Gravitee's own code, and none are enabled by default:

* **Microsoft SQL Server**: client certificate authentication from a PEM file, and Always Encrypted, both go through the non-FIPS provider.
* **MariaDB**: the `parsec` authentication plugin, which uses Ed25519 (not a FIPS-approved algorithm in any case).
* **PDF handling in the Management API**: encrypted or digitally signed PDFs.
* **Argon2 and SCrypt password encoders**: present in the Spring Security library but not used by APIM, so only relevant to a plugin that calls them directly.

If your deployment depends on one of these, the FIPS images aren't a suitable target for it.

## Reproduce an issue

The APIM repository ships a reproduction stack at `docker/quick-setup/fips-mtls`. It brings up the FIPS images with a PEM keystore and an mTLS plan configured end to end, which is a faster starting point than assembling a stack by hand when investigating FIPS-specific behavior.
