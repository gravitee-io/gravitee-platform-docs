---
description: >-
  What the FIPS variants of the APIM Docker images are, where to pull them, and
  what they constrain.
---

# FIPS images

Alongside the ordinary images, APIM publishes a FIPS variant of each backend and frontend
component, built on a FIPS-validated base image. They exist for deployments that must run
FIPS 140-3 validated cryptography end to end.

They are not a drop-in swap: the JVM inside them accepts a narrower set of algorithms and
keystore formats than the ordinary images, so a configuration that works elsewhere may not load.
This page describes what changes.

## What is different inside

The FIPS images replace the JVM's cryptographic providers:

* BouncyCastle FIPS (`BCFIPS`) is registered as provider 1, and the BouncyCastle JSSE provider
  (`BCJSSE`) as provider 2.
* `SunJCE` and `SunJSSE` are **absent** from the provider list.
* The JVM runs in BouncyCastle's *approved only* mode (`org.bouncycastle.fips.approved_only=true`),
  which rejects algorithms outside the validated set — including several that the ordinary images
  accept without complaint.

The images are based on JDK 21.

## Where to find them

FIPS images are published to the **private Gravitee registry only**. They are never pushed to
Docker Hub, so `docker pull graviteeio/apim-gateway:<version>-chainguard-fips` will not resolve.

```sh
docker login graviteeio.azurecr.io
docker pull graviteeio.azurecr.io/apim-gateway:4.12-chainguard-fips
```

The tag is the ordinary version tag with the `-chainguard-fips` suffix. It is available for:

| Component | Image |
| --- | --- |
| API Gateway | `graviteeio.azurecr.io/apim-gateway:<version>-chainguard-fips` |
| Management API | `graviteeio.azurecr.io/apim-management-api:<version>-chainguard-fips` |
| Console | `graviteeio.azurecr.io/apim-management-ui:<version>-chainguard-fips` |
| Developer Portal | `graviteeio.azurecr.io/apim-portal-ui:<version>-chainguard-fips` |

Contact Gravitee support if you need access to the registry.

## Keystore and truststore formats

This is the constraint that most often surprises. Under *approved only* mode, the formats APIM
accepts do not all load:

| Format | On the FIPS images |
| --- | --- |
| `pem` | **Works.** The recommended format. |
| `pkcs12` | Loads in memory, but writing a keystore fails: the PKCS12 key derivation function (`PBEWithHmacSHA256AndAES_256`) has no provider once `SunJCE` is gone. |
| `jks` | Loads, but relies on SUN's SHA-1 based password encryption, which is not FIPS-approved — using it defeats the purpose of running the FIPS image. |
| `bcfks` | **Works from APIM 4.12.19.** The BouncyCastle FIPS keystore, designed for approved-only mode: unlike PKCS12 it can also be written, so it is the option to reach for when you need a single password-protected container rather than separate certificate and key files. |
| `self-signed` | Not recommended: generating the certificate exercises the same non-approved paths. |

In practice, **configure your keystores and truststores as `pem`**. It needs no password and
no conversion tooling. On 4.12.19 and later, `bcfks` is the alternative when you would rather
ship one container file; earlier 4.12 patches do not accept the type.

The JVM-level trust store is a separate matter: `javax.net.ssl.trustStore` does not accept PEM,
so the images set `-Djavax.net.ssl.trustStoreType=FIPS` to read the bundled `cacerts` in
compatibility mode. This applies to the TLS connections APIM opens to JDBC, Redis and
Elasticsearch or OpenSearch.

### Configuring a PEM keystore

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

The same key exists per listener under `gateway.servers[].ssl.keystore`, for the Kafka listener
under `gateway.kafka.ssl.keystore`, and for the rate limit repository under
`gateway.ratelimit.redis.keystore`.

## Known limitations

Because the non-FIPS BouncyCastle provider is not present, a few capabilities that ship inside
third-party libraries lose their cryptographic backing on the FIPS images. None of them affect
Gravitee's own code, and none are enabled by default:

* **Microsoft SQL Server** — client certificate authentication from a PEM file, and Always
  Encrypted, both go through the non-FIPS provider.
* **MariaDB** — the `parsec` authentication plugin, which uses Ed25519 (not a FIPS-approved
  algorithm in any case).
* **PDF handling in the Management API** — encrypted or digitally signed PDFs.
* **Argon2 and SCrypt password encoders** — present in the Spring Security library but not used
  by APIM, so only relevant to a plugin that calls them directly.

If your deployment depends on one of these, the FIPS images are not a suitable target for it.

## Reproducing an issue

The APIM repository ships a reproduction stack at `docker/quick-setup/fips-mtls`. It brings up
the FIPS images with a PEM keystore and an mTLS plan configured end to end, which is a faster
starting point than assembling a stack by hand when investigating FIPS-specific behaviour.
