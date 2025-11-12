# Configuration-Level Secrets

## Overview

Gravitee offers an [integration](../../getting-started/integrations.md#secret-managers-integration) with secrets managers to obscure secrets in configuration files and environment variables.

{% hint style="info" %}
This page shows how to enable `secret-provider` plugins. Please refer to [Secret Provider Plugins Configuration](secret-provider-plugins-configuration.md) to learn how configure them in depth using `gravitee.yml` or environment variables, as well as how to set up hosts, authentication, SSL, retries, etc.
{% endhint %}

## Configuring access to secret managers <a href="#configuring-access-to-secret-managers" id="configuring-access-to-secret-managers"></a>

{% hint style="info" %}
For the sake of simplicity, only the `gravitee.yml` example will be shown here.
{% endhint %}

The following shows a `gravitee.yml` configuration, where plugins can run in parallel when enabled.

```yaml
secrets:
  loadFirst: kubernetes # to allow others SM credentials to be resolved from k8s
  kubernetes:
    enabled: true
  vault:
    enabled: true
```

## Resolving secrets in configuration files <a href="#resolving-secrets-in-configuration-files" id="resolving-secrets-in-configuration-files"></a>

Secret providers offer to resolve secrets once on startup or watch secrets for changes. See the [Integrations](../../getting-started/integrations.md#secret-managers-integration) section to learn about the various capabilities of those plugins.

To watch a secret requires support for hot reload. This use case is currently limited to TLS KeyStore, or PEM for HTTP, TCP, and Kafka servers.

This section covers the syntax for resolving secrets and how secrets are resolved for TLS.

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

The examples below show variations of this syntax as it applies to some of the plugins.

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

## Resolving secrets for TLS <a href="#resolving-secrets-for-tls" id="resolving-secrets-for-tls"></a>

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

For example:

```
secret://kubernetes/giotls?
  keymap=certificate:frontend-tls-cert&keymap=private_key:frontend-tls-priv-key
```

We expect the secret named `giotls` to contain two keys, `frontend-tls-cert` and `frontend-tls-key`, which are mapped to `certifcate` and `private_key`, respectively.
{% endtab %}

{% tab title="Key Store" %}
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

Note that the keystore content (key `content` of `garavitee-jks`) and password are sought separately. In addition, Gravitee does not perform any mapping because naming is Java-specific.
{% endtab %}
{% endtabs %}

## Using `secret providers` to configure secret managers <a href="#using-secret-providers-to-configure-secret-managers" id="using-secret-providers-to-configure-secret-managers"></a>

The example below uses the `kubernetes` plugin to configure the Vault KV engine. The Vault credentials are only visible to the user with higher privileges who set up the Secrets in Kubernetes.

```yaml
secrets:
  loadFirst: kubernetes  # this is mandatory to enable this feature
  kubernetes:
    enabled: true
    namespace: my-app
  vault:
    enabled: true
    # other mandatory configuration parameters
    auth:
      method: token
      config:
        token: secret://kubernetes/vault-creds:config_token
   
```

## Known limitations

Current limitations are summarized below:

* Only the `http.ssl.keystore.secret` x.509 pairs (whether format is PEM or KeyStore) can be watched and therefore hot-reloaded.
* Only environment variables and `gravitee.yml` properties can be resolved into secrets.\
  A secret URL cannot be set using JVM properties, for example:\
  `-Dsystem.proxy.password=secret://kubernetes/giosecrets:proxypass` **cannot be used**. JVM properties are passed directly to the platform without parsing and will not be detected by Gravitee as secret to resolve.
* The `vault` plugin watches via polling because Vault Events is an entreprise feature.
* The `aws`plugin does not support watch. Used in configuration secret will be resolved once.
