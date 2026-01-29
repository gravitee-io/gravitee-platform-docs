# Configure Secret Providers

## Overview <a href="#overview" id="overview"></a>

You can configure secret managers to work with your Domains. You can use secrets to hide information in any plugin field that supports Gravitee Secret Expression Language.

Secret provider plugins extend the operable range of secret managers to resolve secrets on startup and in APIs. For more information about secret provider plugins, see [Integrations](../secret-providers.md).

This article explains the syntax Gravitee uses to resolve secrets in domains and configure secret managers.

#### Known limitations <a href="#known-limitations" id="known-limitations"></a>

* The `vault` plugin watches with polling because Vault Events is an enterprise feature.
* The `aws` plugin does not support the `watch` feature.
* Domain Secrets are currently manage only by a subset of plugins, it is currently not possible to use a secret in a form which is not a plugin configuration. To see the list of plugins, please refer to [Plugins support](plugins-support.md).
* Secret are resolved when the plugin is instantiated. if a secret is updated in the secret manager the plugin needs to be restarted with either with a plugin configuration update or with a service restart. By default, Secrets are cached for one hour. So a simple plugin update may not refresh the secret.
* Secret providers defined at domain level can not restricted to a specific environment.

## Prerequisities <a href="#prerequisites-to-enable-this-feature" id="prerequisites-to-enable-this-feature"></a>

* Configure one of the following secret managers in your `gravitee.yml` file, Helm Chart, or using the equivalent environment variable: Kubernetes, Amazon Secret Manager, or Hashicorp Vault. For more information about Secret Managers, see [secret-providers.md](../secret-providers.md "mention").
* Reference those secrets in your plugin definitions with a specialized syntax. For more information about referencing secrets in Domain definitions, see [Apply Secret to Domains](apply-secret-to-domains.md).

### Configuration for each secret manager <a href="#per-manager-configuration" id="per-manager-configuration"></a>

A `secret provider` plugin must be either bundled or added to the plugin directory.

You can enable `secret-provider` plugins by configuring them in `gravitee.yml`  or in the `values.yaml`. The configurations for each secret provider plugin are discussed in the following sections.

The following examples are for both `gravitee.yml` and Helm `values.yml`.

#### Kubernetes <a href="#kubernetes" id="kubernetes"></a>

The following example show to resolve secrets in the same namespace.&#x20;

{% tabs %}
{% tab title="Resolving secrets in the same namespace" %}
{% hint style="info" %}
This configuration works with both the `gravitee.yml` file and the `values.yaml` file.
{% endhint %}

* Navigate to the the domains section of your `gravitee.yml` file or. your `values.yaml` file, and then add the following configuration:

```yml
domains:
  secrets:
    providers:
      - id: kubernetes
        plugin: kubernetes
        configuration:
          enabled: true
```
{% endtab %}

{% tab title="Resolving secrets in a different namespace" %}
{% hint style="info" %}
The deployment of Gravitee must be configured to access the additional namespace.
{% endhint %}

* Navigate to the `domains` section of your `gravitee.yml` file or your `values.yaml` file, and then add the following configuration:&#x20;

```yml
domains:
  secrets:
    providers:
      - id: kubernetes
        plugin: kubernetes
        configuration:
          enabled: true
          namespace: <another-namespace>
```

* Replace `<another-namespace>` with the namespace where the secret is stored.
{% endtab %}
{% endtabs %}

Here are additional options for configuring secrets in Kubernetes:

* `timeoutMs`. With this attribute, you control Kubernetes client request timeout.
* `kubeConfigFile` . With this attribute, you set a file path to a local Kubernetes configuration when you run Gravitee locally outside of Kubernetes.

#### HashiCorp Vault <a href="#hashicorp-vault" id="hashicorp-vault"></a>

This plugin enables all possible option to access KV engine of Vault. It can manage the following authentication methods:

* Token
* Userpass
* App Role
* Github
* Certificate (mTLS)
* Kubernetes (short-lived and long-lived tokens)

With the following configuration, Gravitee uses a **secured** connection, a **Vault token** to authenticate, and then **watches** secrets by polling and 2 **retry** attempt to fetch a secret. By default, `retry` and `watch` are disabled.

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          host: 127.0.0.1      
          port: 8200
          ssl:
            enabled: true
            format: pemfile
            file: /opt/gravitee/vault/server.pem
          auth:
            method: token
            config:
              token: your_vault_token
          retry:
            attempts: 2 # set '0' to disable
            intervalMs: 1000
          watch:
            enabled: true
            pollIntervalSec: 30
```
{% endtab %}
{% endtabs %}

**Alternative SSL configuration**

* To use an inline PEM, add the following configuration:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          host: 127.0.0.1      
          port: 8200
          ssl:
            enabled: true
            format: pem
            pem: |
              ---BEGIN CERTIFICATION---
              ...
          auth: ...
```
{% endtab %}
{% endtabs %}

* To use a java TrustStore, add the following configuration:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          host: 127.0.0.1      
          port: 8200
          ssl:
            enabled: true
            format: truststore
            file: /opt/gravitee/vault.jks
          auth: ...
```
{% endtab %}
{% endtabs %}

**Other authentication methods**

{% hint style="info" %}
To ensure that examples remain concise, some of the configuration is not shown here t.
{% endhint %}

Each of these authentication method can be configured in Vault in a non-default path. Use `path` under `config` to specify it. Here is an example using a GitHub configuration:

{% tabs %}
{% tab title="gravitee.yml/Helm values.yml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          ...
          auth:
            method: github
            config:
              token: a_github_token
              path: dev-acme-gh-org   # non default auth path (application to all methods)
```
{% endtab %}
{% endtabs %}

Here is an example configuration that uses App role:

{% tabs %}
{% tab title="gravitee.yml / Helm values.yml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          ...
          auth:
            method: approle
            config:
              roleId: fda63f0a-36ab-4681-9a64-eee51c77088e
              secretId: 6f688ba0-dc09-4d6c-aa20-95d12de8f9d0
```
{% endtab %}
{% endtabs %}

Here is an example configuration that uses mTLS with PEM files:

{% tabs %}
{% tab title="gravitee.yml / Helm values.yml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          ...
          auth:
            method: cert
            config:
               format: pemfile                        # "pemfile" or "pem" 
               ## for 'pem' and 'pemfile' format
               cert: /opt/gravitee/vault/client.crt   # file path or inline cert
               key: /opt/gravitee/vault/client.key    # file path or inline private key
               ## for 'keystore' format
               # keyStore:      # file path
               # password:      # keystore password
```
{% endtab %}
{% endtabs %}

Here is an example configuration that uses a Java Keystore:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          ...
          auth:
            method: cert
            config:
              format: keystore
              keyStore: /opt/gravitee/vault/client.jks
              password: verysecret
```
{% endtab %}
{% endtabs %}

Here is an example configuration that uses Kubernetes:

* (Recommended) The example uses short lived tokens:
* (Optional) If your pod does not make the token available in `/var/run/secrets/kubernetes.io/serviceaccount/token` , you can add `tokenFile` .

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:  
          enabled: true
          ...
          auth:
            method: kubernetes
            config:
              role: vault-role
```
{% endtab %}
{% endtabs %}

Here is an example configuration with long-lived tokens:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: vault
        plugin: vault
        configuration:
          enabled: true
          ...
          auth:
            method: kubernetes
            config:
              role: vault-role
              tokenSecret:
                name: auth-sa-token
                namespace: gravitee  # same namespace as Gravitee if unset       
```
{% endtab %}
{% endtabs %}

#### AWS Secret manager <a href="#aws-secret-manager" id="aws-secret-manager"></a>

Here is a standard configuration when Gravitee runs in AWS EC2 or EKS. For more information about using `"chain"`, go to [Default credentials provider chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html).

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: aws
        plugin: aws
        configuration:
          enabled: true
          region: "eu-west-1"
          auth:
            provider: chain
```
{% endtab %}
{% endtabs %}

Here is an example configuration when Gravitee runs outside AWS:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
domains:
  secrets:
    providers:
      - id: aws
        plugin: aws
        configuration:
          enabled: true
          region: "eu-west-1"
          auth:
            provider: static
            config:
              accessKeyId: my_aws_access_key_id
              secretAccessKey: my_ aws_secret_access_key
```
{% endtab %}
{% endtabs %}

Here are more options that you can use  to configure your AWS secret manager:

* `fipsEnabled` to enable FIPS. The default value is `false` .
* `connectionTimeoutMs` to control connection the timeout. The default value is `5000` .
* `endpointOverride` to use a non default AWS endpoint.

### Advanced configuration <a href="#advanced-configuration" id="advanced-configuration"></a>

#### **Use 'configuration-level secrets' for 'Domain-level secrets configuration'** <a href="#use-configuration-level-secrets-for-api-level-secrets-configuration" id="use-configuration-level-secrets-for-api-level-secrets-configuration"></a>

If you want to hide sensitive information in a secret manager, you must secure credentials. When configuring your secret provider credentials, you can use [configuration-level secrets](../secret-providers.md) to hide these credentials in `gravitee.yml`.

Here is an example with Kubernetes configured to HashiCorp Vault:

{% tabs %}
{% tab title="gravitee.yaml / Helm values.yaml" %}
```yaml
secrets:
 kubernetes:
   enabled: true

api:
  secrets:
    providers:
      - id: vault
        plugin: vault     
        configuration:           
          enabled: true          
          auth:
            method: token
            config:
              token: secret://kubernetes/secret-provider:token
```
{% endtab %}
{% endtabs %}

### Secret cache <a href="#secret-cache" id="secret-cache"></a>

#### Resolved secrets stay secured <a href="#resolved-secrets-stay-secured" id="resolved-secrets-stay-secured"></a>

Credentials to access secret managers are set in the Gravitee configuration and only system admins can manipulate them. Also, these credentials can be hidden in secret managers. No user of any Gravitee UI can gain access to them.

Secrets are resolved and stored in a cache. Cached data stays off-heap, preventing admin users from dumping JVM memory using a Gravitee admin endpoint.

#### Consequence of caching secrets <a href="#consequence-of-caching-secrets" id="consequence-of-caching-secrets"></a>

When the plugin is initialized, secrets are resolved and cached . The cache is accessed when the secret expression language is evaluated. Here is the following consequence:

* The first domain to use a given secret URI. For example, `/kubernetes/my-secret` resolves the secret and all key/values in it. Subsequent domains that use a secret with the same URI does not trigger a new resolution. This means that if the value changes in the secret manager, the new value is ignored.&#x20;

#### Cache configuration

The cache is enable by default with a TTL set to 1 hours (duration in millisecond) without cache size limit.&#x20;

* To configure the cache, Navigate to the `domains.secrets`, and then add the `cache` section.

{% tabs %}
{% tab title="First Tab" %}
```yaml
domains:
  secrets:
    cache:
      ttl: 3600000
      maxSize: 100
```
{% endtab %}
{% endtabs %}
