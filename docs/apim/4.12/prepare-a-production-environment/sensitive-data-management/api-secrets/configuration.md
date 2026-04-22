---
description: An overview about configuration.
metaLinks:
  alternates:
    - configuration.md
---

# Configuration

## Overview

{% hint style="warning" %}
This feature work for only V4 APIs.
{% endhint %}

You can configure secret managers to work with your APIs. You can use secrets to hide information in any field that supports Gravitee Expression Language. For more information about Gravitee Expression Language, see [Gravitee Expression Language](../../../gravitee-expression-language.md).

Secret provider plugins extend the operable range of secret managers to resolve secrets on startup and in APIs. For more information about secret provider plugins, see [Integrations](../../../readme/integrations.md).

This article explains the syntax Gravitee uses to resolve secrets in v4 APIs and configure secret managers.

{% hint style="info" %}
To learn more about Gravitee [Enterprise Edition](../../../readme/enterprise-edition.md) and what's included in various enterprise packages, please:

* [Book a demo](https://documentation.gravitee.io/platform-overview/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

### Known limitations

* Only environment variables and `gravitee.yml` properties can be resolved into secrets.\
  A secret URL cannot be set using JVM properties, for example:\
  `-Dsystem.proxy.password=secret://kubernetes/giosecrets:proxypass` **cannot be used**. JVM properties are passed directly to the platform without parsing and will not be detected by Gravitee as secret to resolve.
* The `vault` plugin watches with polling because Vault Events is an enterprise feature.
* The `aws` plugin does not support the `watch` feature.

### Prerequisites to enable this feature <a href="#prerequisites-to-enable-this-feature" id="prerequisites-to-enable-this-feature"></a>

* Configure one of the following secret managers in your `gravitee.yml` file, Helm Chart, or using the equivalent environment variable: Kubernetes, Amazon Secret Manager, or Hashicorp Vault. For more information about these secret managers, see [Integrations](../../../readme/integrations.md#secret-managers-integration).
* Reference those secrets in your API definitions with a specialized syntax. For more information about referencing secrets in API definitions, see [reference-secrets-in-apis.md](reference-secrets-in-apis.md "mention").

## Configuration for each secret manager <a href="#per-manager-configuration" id="per-manager-configuration"></a>

A `secret provider` plugin must be either bundled or added to the plugin directory.

You can enable `secret-provider` plugins by configuring them in `gravitee.yml`. The configurations for each secret provider plugin are discussed in the following sections.

The following examples are for both `gravitee.yml` and Helm `values.yml`.

### Kubernetes

The following example is a typical configuration for running Gravitee in Kubernetes. With this configuration, secrets are **resolved in the same namespace:**

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
secrets:
  kubernetes:
    enabled: true
```
{% endcode %}

The following example shows how to add another namespace:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
secrets:
  kubernetes:
    enabled: true
    namespace: another-namespace
```
{% endcode %}

{% hint style="info" %}
The deployment of Gravitee must be configured to access the additional namespace.
{% endhint %}

Here are more options for configuring secrets in Kubernetes:

* `timeoutMs`. With this attribute, you control Kubernetes client request timeout.
* `kubeConfigFile` . With this attribute, you set a file path to a local Kubernetes configuration when you run Gravitee locally outside of Kubernetes.

### HashiCorp Vault

This plugin enables all possible option to access KV engine of Vault. It can manage the following authentication methods:

* Token
* Userpass
* App Role
* Github
* Certificate (mTLS)
* Kubernetes (short-lived and long-lived tokens)

Here is an example configuration:

With this configuration, Gravitee uses a **secured** connection, a **Vault token** to authenticate, and then **watches** secrets by polling and 2 **retry** attempt to fetch a secret.

{% tabs %}
{% tab title="gravitee.yml/Helm values.yml" %}
<pre class="language-yaml" data-title="gravitee.yml/Helm values.yml"><code class="lang-yaml"><strong>api:
</strong><strong>  secrets:
</strong><strong>    providers:
</strong><strong>      - id: vault
</strong><strong>        plugin: vault
</strong><strong>        configuration:
</strong>          enabled: true
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
</code></pre>
{% endtab %}

{% tab title="Environment variables" %}
```bash
gravitee_api_secrets_providers_0_plugin=vault
gravitee_api_secrets_providers_0_configuration_enabled=true
gravitee_api_secrets_providers_0_configuration_host=127.0.0.1
gravitee_api_secrets_providers_0_configuration_port=8200
gravitee_api_secrets_providers_0_configuration_ssl_enabled=true
gravitee_api_secrets_providers_0_configuration_ssl_format=pemfile
gravitee_api_secrets_providers_0_configuration_ssl_file=/opt/gravitee/vault/server.pem
gravitee_api_secrets_providers_0_configuration_auth_method=token
gravitee_api_secrets_providers_0_configuration_auth_config_token=your_vault_token
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
By default, `retry` and `watch` are disabled.
{% endhint %}

#### Alternative SSL configuration

* To use an inline PEM, add the following configuration:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

* To use a java TrustStore, add the following configuration:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

#### Other authentication methods

{% hint style="info" %}
Some of the configuration is not shown here to ensure that examples remain concise.
{% endhint %}

Each of these authentication method can be configured in Vault in a non-default path. Use `path` under `config` to specify it. See, the following GitHub configuration for an example.

* GitHub

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

* Username and Password

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
              username: admin
              password: password
```
{% endcode %}

* App role

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

* mTLS
  * With PEM files

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

* With a Java Keystore

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

* Kubernetes
  *   (recommended) Here is an example with short lived tokens:

      <pre class="language-yaml" data-title="gravitee.yml/Helm values.yml"><code class="lang-yaml">api:
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
      </code></pre>

      * (Optional) If your pod does not make the token available in `/var/run/secrets/kubernetes.io/serviceaccount/token` , you can add `tokenFile` .
  *   Here is an example with long-lived tokens:

      <pre class="language-yaml" data-title="gravitee.yml/Helm values.yml"><code class="lang-yaml">api:
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
      </code></pre>

### AWS Secret manager

Here is a standard configuration when Gravitee runs in AWS EC2 or EKS. For more information about using `"chain"`, go to [Default credentials provider chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html).

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

Here is an example when Gravitee runs outside AWS:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
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
{% endcode %}

Here are more options that can be used to configure your AWS secret manager:

* `fipsEnabled` to enable FIPS. The default value is `false` .
* `connectionTimeoutMs` to control connection the timeout. The default value is `5000` .
* `endpointOverride` to use a non default AWS endpoint.

## Advanced configuration <a href="#advanced-configuration" id="advanced-configuration"></a>

### **Use 'configuration-level secrets' for 'API-level secrets configuration'**

If you want to hide sensitive information in a secret manager, you must secure credentials. When configuring your secret provider credentials, you can use [configuration-level secrets](../configure-secrets/reference-secrets-in-configurations.md) to hide these credentials in `gravitee.yml`.

Here is an example with Kubernetes configured to HashiCorp Vault:

{% code title="gravitee.yml/Helm values.yml" %}
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
{% endcode %}

### **Restrict to selected environments**

By default, secret providers are available for all environments that the APIM Gateway manages. This availability means that all APIs deployed on that Gateway can access all secret providers.

You can specialize a secret provider to a set of environments. If all providers are configured like this, an API deployed on another environment triggers a secret resolution error.

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
  secrets:
    providers:
      - id: kubernetes
        plugin: kubernetes     
        environments:
          - b5c8c703-fc12-404d-bf61-22fa19998435
          - 2b4db0b1-8eeb-4410-a50b-dbf83fb55b2c
        configuration:           
          enabled: true
      - id: vault
        plugin: vault
        environments:
          - 4787fa8b-5e45-41ec-9df8-a3f3061d0412
        configuration: 
          enabled: true
          ...
```
{% endcode %}

Environments are referenced using their UUIDs. Hrids are not supported.

### **Using a secret provider plugin more than once**

{% hint style="warning" %}
This syntax has a **critical** impact on how you reference secrets. For more information about syntax references, see [reference-secrets-in-apis.md](reference-secrets-in-apis.md "mention").
{% endhint %}

For a setup with multiple environments, it is possible to use the same secret manager with different credentials, depending on the environment. Here is an example of a configuration with multiple environments:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
  secrets:
    providers:
      - id: dev
        plugin: vault      
        environments:
          - b5c8c703-fc12-404d-bf61-22fa19998435
        configuration:           
          enabled: true
          ...      
          auth:
            method: token
            config:
              token: 9887DSKflkjdf53EZzhkjchs
      - id: test
        plugin: vault
        environments:
          - 4787fa8b-5e45-41ec-9df8-a3f3061d0412
        configuration: 
          enabled: true
          ...          
          auth:
            method: token
            config:
              token: fjdhfj765756dksjhds587
```
{% endcode %}

## Helm Charts specifics

All of the configurations can be used as is if you edit `gravitee.yml.` For APIM Helm Charts, you must apply those configurations in the relevant sections:

Here is an example for configuration-level secrets in the APIM Gateway with Kubernetes:

{% code title="Helm values.yaml" %}
```yaml
gateway:
  secrets:
    kubernetes:
      enabled: true
```
{% endcode %}

Here is an example for api-level secrets in the APIM Gateway with Kubernetes:

{% code title="Helm values.yaml" %}
```yaml
api:  
  secrets:
    kubernetes:
      enabled: true
```
{% endcode %}

## Environments specifics <a href="#per-manager-configuration" id="per-manager-configuration"></a>

All `gravitee.yml` properties can be set using environment variables.

For secrets, it can be useful to redact the secret manager's credentials.

{% code title="gravitee.yml" %}
```yaml
secrets:
  vault:
    enabled: true
    host: 127.0.0.1      
    port: 8200
    ssl:
      ...
    auth:
      method: token
```
{% endcode %}

In this example the token is missing. It can be set using an environment variable:

```bash
GRAVITEE_SECRETS_VAULT_AUTH_CONFIG_TOKEN="my_vault_token_for_gravitee_secrets"
```

## Retry options

Retry options are applicable to all secret provider plugins. They are triggered in the background when a secret cannot be resolved. They are enabled by default.

Here is an example to that shows the defaults:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
  secrets:
    providers:
      - plugin: vault
        configuration:
          enabled: true
          host: 127.0.0.1
          port: 8200
          ssl:
            ...
          auth:
            method: token
          # better to disable internal vault plugin retry
          retry:
            attempts: 0
    retryOnError:
      enabled: true
      delay: 2                   
      unit: SECONDS
      backoffFactor: 1.5
      maxDelay: 60
      maxAttempt: 10
```
{% endcode %}

## Renewal

If a secret reference has the ?`renewable=true` option, you can control the following actions:

* How frequently a secret's TTL is checked to trigger the renewal.
* The default TTL is set for secrets with the ?`renewable=true` option.

Here is an example that shows the defaults. With this configuration, a check is completed every 15 minutes where secrets older than one day are resolved again:

{% code title="gravitee.yml/Helm values.yml" %}
```yaml
api:
  secrets:
    providers:
      - plugin: vault
        configuration:
          enabled: true
          host: 127.0.0.1
          port: 8200
          ssl:
            ...
          auth:
            method: token
            config:
              token: your_token
    renewal:
      enabled: true
      check:
        delay: 15                   
        unit: MINUTES
      defaultSecretTtl:
        delay: 1
        unit: DAYS
```
{% endcode %}
