---
description: An overview about reference secrets in configurations.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/prepare-a-production-environment/sensitive-data-management/configure-secrets/reference-secrets-in-configurations
---

# Reference Secrets in Configurations

## Overview

Gravitee offers an [integration](../../../readme/integrations.md#secret-managers-integration) with secrets managers to obscure secrets in configuration files and environment variables. This page shows how to enable `secret-provider` plugins.

{% hint style="info" %}
Please refer to [Secret Provider Plugins Configuration](./) to learn how configure them in depth using `gravitee.yml` or environment variables, as well as how to set up hosts, authentication, SSL, retries, and other configurations.
{% endhint %}

## Prerequisites <a href="#resolving-secrets-in-configuration-files" id="resolving-secrets-in-configuration-files"></a>

* Required secret provider plugins are either bundled or have been added.
* Complete the steps in [quick-start.md](quick-start.md "mention").

## Resolve secrets in configuration files <a href="#resolving-secrets-in-configuration-files" id="resolving-secrets-in-configuration-files"></a>

Secret providers offer to resolve secrets once on startup or watch secrets for changes. For more information about the capabilities of those plugins, see [Integrations](../../../readme/integrations.md#secret-managers-integration) .

To watch a secret requires support for hot reload. This use case is currently limited to TLS KeyStore, or PEM for HTTP, TCP, and Kafka servers.

### Syntax <a href="#syntax" id="syntax"></a>

A consistent URL-like syntax can be used to specify the location of the secret (single value or pairs):

`secret://`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`[:`<mark style="color:yellow;">`key`</mark>`][?option=value1&option=value2]`

* <mark style="color:red;">`provider`</mark>: ID of the secret provider plugin.
* <mark style="color:green;">`path`</mark>: Path or name of the secret. It is specific to the secret manager.
* <mark style="color:yellow;">`key`</mark>: The key within the secret key/value pair that the secret manager returns.

This is custom syntax that does not follow RFC for **query parameters** but adheres to the following:

* `&` splits the string into key/value pairs.
* `=` (first occurrence) splits key and value. If absent, the default value is `true`.
* The <mark style="color:yellow;">`key`</mark> is used for single values.
* A key can be repeated for options with multiple values.
* No other characters are interpreted.

The examples below show variations of this syntax as it applies to the plugins:

{% tabs %}
{% tab title="Kubenetes" %}
```yaml
ds:
  mongodb:
    password: secret://kubernetes/gravitee-mongo:password?namespace=gravitee
```

<mark style="color:green;">`gravitee-mongo`</mark>: The path of secret holding key/value pairs.

<mark style="color:yellow;">`password`</mark>: The desired `key` (optional in some cases, but not here).

`?namespace`: Overrides the configuration namespace (`secrets.kubernetes.namespace`).
{% endtab %}

{% tab title="Vault" %}
```yaml
ds:
  mongodb:
    password: secret://vault/secret/gravitee/mongo:password?namespace=gravitee
```

<mark style="color:green;">`secret`</mark>: The mount point for Vault's Key-Value engine (required).

<mark style="color:green;">`gravitee/mongo`</mark>: The secret holding key/value pairs (required).

<mark style="color:yellow;">`password`</mark>: The desired `key` (optional in some cases, but not here).

`?namespace`: Overrides the configuration namespace (`secrets.vault.namespace`).
{% endtab %}

{% tab title="AWS" %}
```yaml
ds:
  mongodb:
    password: secret://aws/gravitee/mongo:password
```

<mark style="color:green;">`gravitee/mongo`</mark>: The secret holding key/value pairs (required).

<mark style="color:yellow;">`password`</mark>: The desired `key` (optional in some cases, but not here).
{% endtab %}
{% endtabs %}

## Resolve secrets for TLS <a href="#resolving-secrets-for-tls" id="resolving-secrets-for-tls"></a>

{% tabs %}
{% tab title="PEM" %}
Below is the TLS configuration in `gravitee.yml`, which replaces the `ssl.keystore.kubernetes` parameter:

```yaml
http:
  secured: true
  ssl:
    keystore:
      type: pem
      watch: true
      secret: secret://kubernetes/gravitee-tls
```

When the secret is fetched, both the `certificate` and `private_key` must be read. Gravitee points to the whole secret instead of specifying a <mark style="color:yellow;">`key`</mark> because the names of the keys are unknown.

The default mapping of the `kubernetes` plugin matches the "tls" secret type:

* `certificate` → `tls.crt`
* `private_key` → `tls.key`

By default, the keys for other secret managers are assumed to be "certificate" and "private\_key." However, users may want to follow other naming conventions or store several cert/key pairs in a single secret. For example, in Kubernetes, users may store TLS secrets in "generic" secrets.

To extract the certificate and private key and create a keystore to secure Gravitee in a way that works with any secret manager, we use the query parameter `keymap`.

Here is an example:

```
secret://kubernetes/giotls?
  keymap=certificate:frontend-tls-cert&keymap=private_key:frontend-tls-priv-key
```

We expect the secret named `giotls` to contain two keys, `frontend-tls-cert` and `frontend-tls-key`, which are mapped to `certifcate` and `private_key`, respectively.
{% endtab %}

{% tab title="KeyStore" %}
Instead of using PEM, you can use a base64-encoded Java KeyStore with the following configuration:

```yaml
http:
  secured: true
  ssl:
    keystore:
      type: PKCS12  # JKS format supported despite not recommended for production
      watch: true
      secret: secret://kubernetes/gravitee-jks/content
      password: secret://kubernetes/gravitee-jks/password
```

Note that the KeyStore content (key `content` of `garavitee-jks`) and password are sought separately. In addition, Gravitee does not perform any mapping because naming is Java-specific.
{% endtab %}
{% endtabs %}
