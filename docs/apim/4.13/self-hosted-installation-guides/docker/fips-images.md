---
description: >-
  What the FIPS variants of the APIM Docker images are, where to pull them, and
  what they constrain.
---

# FIPS images

Each APIM backend and frontend component has a FIPS image variant next to its ordinary image. The FIPS images are built on a FIPS-validated base image. They're intended for deployments that require FIPS 140-3 validated cryptography end to end.

They aren't a drop-in swap. The JVM inside them accepts a narrower set of algorithms and keystore formats than the ordinary images, so a configuration that works elsewhere doesn't always load. This page describes what changes.

{% hint style="info" %}
These images aren't public. They're published to the private Gravitee registry only, so you need credentials before any command on this page works. Contact [Gravitee support](https://www.gravitee.io/contact-us) to have access granted for your organization.
{% endhint %}

## What is different inside

The FIPS images replace the JVM's cryptographic providers:

* BouncyCastle FIPS (`BCFIPS`) is registered as provider 1, and the BouncyCastle JSSE provider (`BCJSSE`) as provider 2.
* `SunJCE` and `SunJSSE` are **absent** from the provider list.
* The JVM runs in BouncyCastle's *approved only* mode (`org.bouncycastle.fips.approved_only=true`), which rejects algorithms outside the validated set, including several that the ordinary images accept without complaint.

The images are based on JDK 25.

For the provider's own documentation, see the [BouncyCastle FIPS Java documentation](https://www.bouncycastle.org/download/bouncy-castle-java-fips/). For the FIPS base images, see the [Chainguard FIPS documentation](https://edu.chainguard.dev/platform/fips/fips-images/).

## Where to find them

FIPS images are published to the **private Gravitee registry only**. They're never pushed to Docker Hub, so `docker pull graviteeio/apim-gateway:<version>-chainguard-fips` won't resolve.

```sh
docker login graviteeio.azurecr.io
docker pull graviteeio.azurecr.io/apim-gateway:4.13-chainguard-fips
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

## Keystore and truststore formats

This is the constraint that most often surprises. Under *approved only* mode, the formats APIM accepts don't all load:

| Format | On the FIPS images |
| --- | --- |
| `pem` | **Works.** The recommended format. |
| `pem-folder` | **Works**, truststores only. It reads the certificates directly rather than opening a keystore file, like `pem`, and `watch` picks up files added, updated, and removed in the directory. |
| `pkcs12` | **Doesn't load.** There's no PKCS12 keystore implementation at all on this JDK once `SunJCE` is gone, and requesting one fails immediately. |
| `jks` | **Doesn't load.** BouncyCastle FIPS answers for JKS read-only, so APIM can't open it. |
| `bcfks` | **Works.** The BouncyCastle FIPS keystore, designed for approved-only mode. Unlike PKCS12 it's also writable, so it's the option to reach for when you need a single password-protected container rather than separate certificate and key files. |
| `self-signed` | Not recommended: generating the certificate exercises the same non-approved paths. |

In practice, **configure your keystores and truststores as `pem`**: it needs no password and no conversion tooling. Where you'd rather ship one password-protected container file, `bcfks` is the other format that loads. Those two are the only ones on this line.

{% hint style="warning" %}
This is stricter than the 4.12 FIPS images, which run on JDK 21 and still tolerate `pkcs12` and `jks` in some paths. A deployment that upgrades from 4.12 to 4.13 while keeping a `jks` or `pkcs12` keystore fails to start its TLS listeners. Convert those keystores before upgrading, to PEM or to `bcfks` if you'd rather keep a single password-protected container, which is the closer equivalent of the JKS you're leaving behind.
{% endhint %}

The JVM-level trust store is a separate matter: `javax.net.ssl.trustStore` doesn't accept PEM. The FIPS base image carries `-Djavax.net.ssl.trustStoreType=FIPS` in `JDK_JAVA_OPTIONS`, which reads the bundled `cacerts` in compatibility mode. APIM doesn't set it, so this follows the base image rather than a Gravitee decision. It applies to the TLS connections APIM opens to JDBC, Redis, and Elasticsearch or OpenSearch.

### Configure a PEM keystore

With Docker, point the listener at the certificate and key files:

```yaml
environment:
  - gravitee_http_secured=true
  - gravitee_http_ssl_keystore_type=pem
  - gravitee_http_ssl_keystore_certificates_0_cert=/certificates/server.crt
  - gravitee_http_ssl_keystore_certificates_0_key=/certificates/server.key
```

With the Helm chart, use `certificates`, a list of `cert` and `key` pairs:

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

The same key exists per listener under `gateway.servers[].ssl.keystore`, for the Kafka listener under `gateway.kafka.ssl.keystore`, for the rate limit repository under `gateway.ratelimit.redis.keystore`, and for distributed sync under `gateway.distributedSync.redis.keystore`.

## Known limitations

Because the non-FIPS BouncyCastle provider isn't present, a few capabilities that ship inside third-party libraries lose their cryptographic backing on the FIPS images. None of them affect Gravitee's own code, and none are enabled by default:

* **Microsoft SQL Server**: client certificate authentication from a PEM file, and Always Encrypted, both go through the non-FIPS provider.
* **MariaDB**: the `parsec` authentication plugin, which uses Ed25519 (not a FIPS-approved algorithm in any case).
* **PDF handling in the Management API**: encrypted or digitally signed PDFs.
* **Argon2 and SCrypt password encoders**: present in the Spring Security library but not used by APIM, so only relevant to a plugin that calls them directly.

If your deployment depends on one of these, the FIPS images aren't a suitable target for it.

## Reproduce an issue

The APIM repository ships a reproduction stack at `docker/quick-setup/fips-mtls`. It brings up the FIPS images with a PEM keystore and an mTLS plan configured end to end, which is a faster starting point than assembling a stack by hand when investigating FIPS-specific behavior.
