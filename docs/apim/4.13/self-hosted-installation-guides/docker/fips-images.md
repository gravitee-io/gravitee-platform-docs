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

The images are based on JDK 25.

## Where to find them

FIPS images are published to the **private Gravitee registry only**. They are never pushed to
Docker Hub, so `docker pull graviteeio/apim-gateway:<version>-chainguard-fips` will not resolve.

```sh
docker login graviteeio.azurecr.io
docker pull graviteeio.azurecr.io/apim-gateway:4.13-chainguard-fips
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
| `pkcs12` | **Does not load.** There is no PKCS12 keystore implementation at all on this JDK once `SunJCE` is gone, and requesting one fails immediately. |
| `jks` | **Does not load.** BouncyCastle FIPS answers for JKS read-only, so APIM cannot open it. |
| `self-signed` | Not recommended: generating the certificate exercises the same non-approved paths. |

In practice, **configure your keystores and truststores as `pem`**. It is the only format that
works on this line.

{% hint style="warning" %}
This is stricter than the 4.12 FIPS images, which run on JDK 21 and still tolerate `pkcs12` and
`jks` in some paths. A deployment that upgrades from 4.12 to 4.13 while keeping a `jks` or
`pkcs12` keystore will fail to start its TLS listeners. Convert those keystores to PEM before
upgrading.
{% endhint %}

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
