---
description: An overview about configuration.
---

# Configuration

## Overview

This section explains how to configure secret managers to reference secrets in Gravitee.

Secrets manager integrations are handled by `secret-provider` plugins. These plugins allow you to access 3rd-party secret managers to resolve secrets.

{% hint style="info" %}
To learn more about Gravitee [Enterprise Edition](../../../readme/enterprise-edition.md) and what's included in various enterprise packages:

* [Book a demo](https://documentation.gravitee.io/platform-overview/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

### Known limitations

Current limitations are summarized below:

* Only the `http.ssl.keystore.secret` x.509 pairs, in either PEM or KeyStore format, can be watched, and therefore hot-reloaded.
* Only environment variables and `gravitee.yml` properties can be resolved into secrets.\
  A secret URL cannot be set using JVM properties, For example:\
  `-Dsystem.proxy.password=secret://kubernetes/giosecrets:proxypass` **cannot be used**. JVM properties are passed directly to the platform without parsing, and are not detected by Gravitee as secrets to resolve.
* The `vault` plugin watches via polling because Vault Events is an enterprise feature.
* The `aws` plugin does not support watch. When used in a configuration, the secret is resolved once.

## Configuration for each secret manager <a href="#per-manager-configuration" id="per-manager-configuration"></a>

A `secret provider` plugin must be either bundled or added to the plugin directory.

You can enable a `secret-provider` plugin by configuring it in `gravitee.yml`. The configurations for each secret provider plugin are discussed in the following sections.

### Kubernetes

The following example is a typical configuration for running Gravitee in Kubernetes. With this configuration, secrets are **resolved in the same namespace**.

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
The Gravitee deployment must be configured to access the additional namespace.
{% endhint %}

Here are more options for configuring secrets in Kubernetes:

* `timeoutMs`: This attribute controls the Kubernetes client request timeout.
* `kubeConfigFile`: This attribute sets the path to a local Kubernetes configuration when a local instance of Gravitee runs outside of Kubernetes.

### HashiCorp Vault

This plugin enables all possible options to access Vault's K/V engine. It can manage the following authentication methods:

* Token
* Userpass
* App Role
* Github
* Certificate (mTLS)
* Kubernetes (short and long lived tokens)

Here is an example configuration:

```yaml
secrets:
  vault:
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
        token: a_vault_token
    retry:
      attempts: 2          # set '0' to disable
      intervalMs: 1000
    watch:
      enabled: true
      pollIntervalSec: 30
```

With this configuration, Gravitee authenticates using a secure connection a Vault token, watches secrets via polling, and has 2 retry attempts to fetch a secret.

{% hint style="info" %}
By default, `retry` and `watch` are disabled.
{% endhint %}

#### Alternative SSL configuration

*   To use an inline PEM, add the following configuration:

    ```yaml
    secrets:
      vault:
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
*   To use a Java TrustStore, add the following configuration:

    ```yaml
    secrets:
      vault:
        enabled: true
        host: 127.0.0.1      
        port: 8200
        ssl:
          enabled: true
          format: truststore
          file: /opt/gravitee/vault.jks
        auth: ...
    ```

#### Other authentication methods

{% hint style="info" %}
To ensure that examples remain concise, full configurations are not shown.
{% endhint %}

Each of these authentication methods can be configured in Vault using a non-default path. Use `path` under `config` to specify the path. See GitHub for an example.

*   GitHub

    ```yaml
    secrets:
      vault:
        enabled: true
        ...
        auth:
          method: github
          config:
            token: a_github_token
            path: dev-acme-gh-org   # non default auth path (application to all methods)
    ```
*   Username/password

    ```yaml
    secrets:
      vault:
        enabled: true
        ...
        auth:
          method: github
          config:
            username: admin
            password: password
    ```
*   App role

    ```yaml
    secrets:
      vault:
        enabled: true
        ...
        auth:
          method: github
          config:
            roleId: fda63f0a-36ab-4681-9a64-eee51c77088e
            secretId: 6f688ba0-dc09-4d6c-aa20-95d12de8f9d0
    ```
* mTLS
  *   With PEM files

      ```yaml
      secrets:
        vault:
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
  *   With a Java KeyStore

      ```yaml
      secrets:
        vault:
          enabled: true
          ...
          auth:
            method: cert
            config:
               format: keystore
               keyStore: /opt/gravitee/vault/client.jks
               password: verysecret
      ```
* Kubernetes
  *   With short-lived tokens (recommended)

      ```yaml
      secrets:
        vault:
          enabled: true
          ...
          auth:
            method: kubernetes
            config:
              role: vault-role
      ```

      * (Optional) If your pod does not make the token available in `/var/run/secrets/kubernetes.io/serviceaccount/token` , you can add `tokenFile` .
  *   With long-lived tokens

      ```yaml
      secrets:
        vault:
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

### AWS secret manager

Here is a standard configuration when Gravitee runs in AWS EC2 or EKS. For more information about using `"chain"`, go to [Default credentials provider chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html).

```yaml
secrets:
  aws:
    enabled: true
    region: "eu-west-1"
    auth:
      provider: chain
```

Here is an example when Gravitee runs outside of AWS:

```yaml
secrets:
  aws:
    enabled: true
    region: "eu-west-1"
    auth:
      provider: static
      config:
        accessKeyId: my_aws_access_key_id
        secretAccessKey: my_ aws_secret_access_key
```

Here are more options that can be used to configure your AWS secret manager:

* `fipsEnabled` to enable FIPS (`false` by default)
* `connectionTimeoutMs` to control the connection timeout (`5000` by default)
* `endpointOverride` to use a non-default AWS endpoint

## Combine several secret managers

You can use several secret managers at once.

The following example shows a typical use case, where the `kubernetes` plugin configures the Vault K/V engine. The Vault credentials are only visible to users with higher privileges who set up secrets in Kubernetes. No credentials appear in the configuration.

```yaml
secrets:
  loadFirst: kubernetes  # tell Gravitee to load kubernetes first
  kubernetes:
    enabled: true
  vault:
    enabled: true
    # ... other mandatory configuration parameters
    auth:
      method: token
      config:
        token: secret://kubernetes/vault-creds:config_token
```

## Helm chart specifics

All of the configurations can be set using `gravitee.yml`. For APIM Helm charts, you must apply those configurations in the relevant sections.

Here is an example for the APIM Gateway with Kubernetes:

```yaml
gateway:
  secrets:
    kubernetes:
      enabled: true
```

Here is an example for APIM Management API with Kubernetes:

```yaml
api:  
  secrets:
    kubernetes:
      enabled: true
```

## Environments specifics <a href="#per-manager-configuration" id="per-manager-configuration"></a>

All `gravitee.yml` properties can be set using environment variables.

For secrets, it can be useful to redact the secret manager's credentials.

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

In this example, the token is missing. It can be set using an environment variable:

```bash
GRAVITEE_SECRETS_VAULT_AUTH_CONFIG_TOKEN="my_vault_token_for_gravitee_secrets"
```
