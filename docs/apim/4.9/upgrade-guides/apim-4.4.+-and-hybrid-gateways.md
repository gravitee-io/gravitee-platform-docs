---
description: Configuration guide for apim 4.4.+ & hybrid gateways.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/upgrade-guides/apim-4.4.+-and-hybrid-gateways
---

# APIM 4.4.+ & Hybrid Gateways

Starting with APIM 4.4.0, gateways need to explicitly disable certificate checks. The default "trust all" value was `true` it is now `false` for management of type "http".

You **need to** update `gravitee.yml` or your Helm's `values.yaml` if your configuration match **all of** the following:

* You were using a secured connection between Hybrid Gateway and Bridge Server (Gateway or Management API)
* You were using the default value (unset param)
* You were using a non-public CA to sign your certificate
* Your \`gateway.http.management.ssl configuration do not use a trust store to accept the server certificate.

The can explicitly disable certificate checks in the `gravitee.yaml`:

```yaml
management:
  http:
    ssl:
      trustAll: true
```

Or if you are using Helm charts, you can set it in your `values.yaml` file:

```yaml
gateway:
  management:
    http:
      ssl:
        trustAll: true
```

Or you can use an environment variable:

```
GRAVITEE_MANAGEMENT_HTTP_SSL_TRUSTALL="true"
```

{% hint style="warning" %}
The "trust all" configuration parameter was formerly named `trustall`, it is now named `trustAll` for consistency. To avoid a breaking change both names work, but the former has been deprecated.
{% endhint %}
