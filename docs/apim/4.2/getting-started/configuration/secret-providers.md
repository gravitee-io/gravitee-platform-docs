---
description: Tutorial on Secret Providers.
---

# Secret Providers

## Introduction

Gravitee 4.2 offers a set of `secret-provider` plugins that, when deployed, enable secret managers to obscure database passwords and certificates in Gravitee Gateway, API Management, and Access Management configuration files.

{% hint style="info" %}
A future release will enable secret providers to obscure API endpoint credentials in the Management Console.
{% endhint %}

Secret managers provide a secure and convenient way to encrypt, store, manage, and retrieve secrets and other sensitive data such as tokens, API keys, passwords, certificates, etc. Using secret managers, it's possible to enforce consistent security policies, ensure resources and digital credentials can only be accessed by authenticated and authorized users, and instantly connect systems to accomplish automated tasks.

While a secret manager refers to any third party software that is able to store and manage secrets securely, secret providers refer to a category of Gravitee plugin. Secret provider plugins can gain access to secret managers via credentials and a secured connection to provide secrets to Gravitee configurations.

{% hint style="info" %}
The legacy method of fetching configurations from Kubernetes ConfigMaps or Secrets using the syntax `kubernetes://...` remains available, but is discouraged and will be deprecated over future releases. Instead, secret providers retrieve sensitive information (passwords, x509 pairs, etc.) from secret managers (Kubernetes, HC Vault...) to ensure this information does not appear in clear text.
{% endhint %}

The sections below focus on the details of `secret-provider` plugins, how to configure access to secret managers, and how to resolve secrets.

## Secret provider plugins

Secret providers are generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to secret managers. The following `secret-provider` plugins are available for Gravitee Gateway, Management API, and Access Management:

* `kubernetes`: A Community Edition plugin that fetches secret and TLS pairs from Kubernetes.io
* `vault`: An Enterprise Edition plugin that uses the Key/Value engine of HashiCorp Vault

{% hint style="warning" %}
To learn more about Gravitee Enterprise and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/gravitee-apim-enterprise-edition/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

The following table shows which features have been implemented for each of these plugins:

<table><thead><tr><th width="173">Feature</th><th>kubernetes</th><th>vault</th></tr></thead><tbody><tr><td>Resolve a secret</td><td>Yes</td><td>Yes</td></tr><tr><td>Watch a secret</td><td>Yes</td><td>Yes (via polling)</td></tr><tr><td>Secret format</td><td>All K8s types (TLS, generic, etc.)</td><td><p>Key/Value engine v1 or v2</p><p>(no mixing)</p></td></tr><tr><td>TLS</td><td>Yes</td><td>Yes, but not with PKI engine</td></tr><tr><td>Client</td><td>in-house</td><td>Lean and community- based, but flawed. To be replace by in-house.</td></tr><tr><td>Zip size</td><td>11KB</td><td>161KB</td></tr></tbody></table>

## Configuring access to secret managers

To configure access to secret managers, you can use `gravitee.yml`, environment variables, or JVM properties.

The following shows a `gravitee.yml` configuration, where plugins can run in parallel when enabled:

```yaml
secrets:
  loadFirst: kubernetes # to allow others SM credentials to be resolved from k8s
  kubernetes:
    enabled: true
  vault:
    enabled: true
```

Alternatively, a `secret-provider` plugin can be enabled and configured by setting environment variables, e.g., `GRAVITEE_SECRETS_KUBERNETES_ENABLED=true`.

Configuration details are discussed below:

{% tabs %}
{% tab title="Kubernetes" %}
* No default assumptions are made regarding the location of `kubeConfigFile`. The absence of this file assumes that Gravitee is deployed in Kubernetes and the configuration is in-cluster.
* Namespace can be overridden in URLs via `?namespace=<name>`. If no namespace is provided, the namespace is assumed to be that of the cluster in which the platform is deployed. To fetch from the default namespace, it must be set explicitly, unless Gravitee is deployed in that namespace.

```yaml
secrets:
  kubernetes:
    enabled: true
    kubeConfigFile: /opt/gravitee/config/kube-config.json
    timeoutMs: 3000
    namespace: default
```
{% endtab %}

{% tab title="HashiCorp Vault" %}
Explanations inline:

```yaml
secrets:
  vault:
    enabled: true
    host: 127.0.0.1      
    port: 8200
# optional
    namespace: myapphcvns      # default: "default"
    kvEngine: V2               # defaults to v2 can be "v1", no mixing supported
    readTimeoutSec: 2
    connectTimeoutSec: 3
# required although can be disabled
    ssl:
      enabled: false                        # not for production
      # format: "pemfile"                   # one of "pem", "pemfile", "truststore"
      # pem:                                # (only for "pem")
                                            # value is base64 with headers
      # file: /opt/gravitee/vault.pem       # for pemfile truststore files
    auth:
      method: token # one of "token", "github", "userpass", "approle", "cert" (mTLS)
    ### github config
      config:
        token: hvc.KksuhsLShi8d8s7/sLius==
    ### github config
        # token:
        # path: <non standard github path>
    ### userpass config
        # username:
        # password:
        # path: <non standard github path>
    ### approle
        # roleId:
        # secretId:
    ### cert
        # format: pemfile                    # one of "pem","pemfile","keystore"
        ## for 'pem' and 'pemfile' format
        # cert:                              # file path or inline cert
        # key:                               # file path or inline private key
        ## for 'keystore' format
        # keyStore:      # file path
        # password:      # keystore password
    # RECOMMENDED but works without
    # for both watch and read
    retry:
      attempts: 2          # set '0' to disable
      intervalMs: 1000
    # if disabled an error will be displayed at load time if http.ssl.keystore.secret is used with watch enabled
    watch:
      enabled: true
      pollIntervalSec: 30
```
{% endtab %}
{% endtabs %}

## Resolving secrets in configuration files

Secret providers extend the operable range of secret managers to both resolve secrets on startup and watch secrets.

{% hint style="warning" %}
To watch a secret requires support for hot reload. This use case is currently limited to TLS KeyStore.
{% endhint %}

This section covers the syntax for resolving secrets, how secrets are resolved for TLS, and how `secret-provider` plugins are used to configure secret managers.

### Syntax

A consistent URL-like syntax can be used to specify the location of the secret (single value or pairs):

**`secret://`**`<plugin id>/<secret path or name>[:<data key>][?option=value1&option=value2]`

This is a custom syntax that doesn't follow RFC for query parameters but adheres to the following:

* `&` splits the string into key/value pairs
* `=` (first occurrence) splits key and value. If absent, the default value is `true`
* The `data key` is used for single values
* A key can be repeated for options with multiple values
* No other characters are interpreted

The examples below show variations of this syntax as it applies to each of the plugins.

{% tabs %}
{% tab title="Kubernetes" %}
```yaml
ds:
  mongodb:
    password: secret://kubernetes/gravitee-mongo:password?namespace=gravitee
```

* `gravitee-mongo`: The secret holding key/value pairs
* `password`: The desired key (optional)
* `?namespace`: Overrides the configuration namespace (`secrets.kubernetes.namespace`)
{% endtab %}

{% tab title="HashiCorp Vault" %}
```yaml
ds:
  mongodb:
    password: secret://vault/secret/gravitee/mongo:password?namespace=gravitee
```

`secret`: The mount point for Vault's Key-Value engine (required)

`gravitee/mongo`: The secret holding key/value pairs (required)

`password`: The desired key (optional)

`?namespace`: Overrides the configuration namespace (`secrets.vault.namespace`)
{% endtab %}
{% endtabs %}

### Resolving secrets for TLS

#### For PEM

The following shows the TLS configuration in `gravitee.yml`, which replaces the `ssl.keystore.kubernetes` parameter:

```yaml
http:
  secured: true
  ssl:
    keystore:
      type: pem
      watch: true
      secret: secret://kubernetes/gravitee-tls
```

When the secret is fetched, both the `certificate` and `private_key` must be read. Gravitee points to the whole secret instead of specifying a `data key` because the names of the keys are unknown.

The default mapping of the `kubernetes` plugin matches the "tls" secret type:

* `certificate` → `tls.crt`
* `private_key` → `tls.key`

By default, the data keys for other secret managers are assumed to be "certificate" and "private\_key." However, users may want to follow other naming conventions or store several cert/key pairs in a single secret. For example, in Kubernetes, users may store TLS secrets in "generic" secrets.

To extract the certificate and private key and create a keystore to secure Gravitee in a way that works with any secret manager, we use the query parameter `keymap`. For example:

```xml
secret://kubernetes/giotls?
  keymap=certificate:frontend-tls-cert&keymap=private_key:frontend-tls-priv-key
```

Here, we expect the secret named `giotls` to contain two keys, `frontend-tls-cert` and `frontend-tls-key`, which are mapped to `certifcate` and `private_key`, respectively.

#### For Java KeyStore

Instead of using PEM, you can use a base64 encoded Java KeyStore with the following configuration:

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

### Using `secret providers` to configure Secret Managers

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
* Only system environment variables and `gravitee.yml` properties can be resolved into secrets. A secret URL cannot be set via JVM properties, e.g., `-Dsystem.proxy.password=secret://kubernetes/giosecrets:proxypass` cannot be used. The parameters are passed directly to the platform without parsing and will not be detected by a `secret provider` plugin.
* The `vault` plugin watches via polling because Vault events is an unstable feature.
