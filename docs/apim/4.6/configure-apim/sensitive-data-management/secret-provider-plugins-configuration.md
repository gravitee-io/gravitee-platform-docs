---
description: >-
  Gravitee's secret managers integrations rely on the secret-provider plugin
  type. This page lets you know how to configure these plugins for all use
  cases.
---

# Secret Provider Plugins Configuration

## Introduction

Secrets managers provide a secure and convenient way to encrypt, store, manage, and retrieve secrets and other sensitive data such as tokens, API keys, passwords, and certificates. Using secret managers, it's possible to enforce consistent security policies, ensure resources and digital credentials can only be accessed by authenticated and authorized users, and instantly connect systems to accomplish automated tasks.

Gravitee offers an [integration](../../getting-started/integrations.md#secret-managers-integration) with secrets managers to obscure secrets and avoid clear text credentials stored in files or databases.

[Configuration-level secrets](configuration-level-secrets.md) allow you to obscure secrets in `gravitee.yml`, Helm Charts, and environment variables.

[API-level secrets](../../configure-v4-apis/api-level-secrets.md) (starting from APIM 4.6) allow v4 APIs to obscure secrets in many plugins, as long as they support [Gravitee Expression Language](../../getting-started/gravitee-expression-language.md). &#x20;

Functionally, the secrets managers integrations are handled by`secret-provider` plugins that, when deployed, configured and enabled, allow you to access those third parties to resolve secrets.&#x20;

This capability is available in Gravitee Gateway and API Management for both Access Management and APIM.

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](../../overview/enterprise-edition.md) and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Per manager configuration

As with any other plugin, a secret provider plugin must be either bundled or added to the plugin directory.

You can enable `secret-provider` plugins by configuring them in `gravitee.yml`. The configurations for each secret provider plugin are discussed below. As with all other `gravitee.yaml` configurations, you can also set these as [environment variables](../environment-properties.md#using-environment-variables-in-different-installation-methods).

### Use cases

Using a secrets manager integration to obscure sensitive data in a configuration and using a secrets manager integration to obscure sensitive data in an API are two different use cases that are performed independently. For more information on each use case, see:

[#example-for-configuration](secret-provider-plugins-configuration.md#example-for-configuration "mention")

&#x20;[#example-for-v4-apis](secret-provider-plugins-configuration.md#example-for-v4-apis "mention")&#x20;

### Enable a `secret-provider` plugin

All secret providers share the `enabled` property, and this is disabled by default.

```yaml
enabled: true
```

### Kubernetes (plugin id: `kubernetes`)

```yaml
enabled: true
kubeConfigFile: /opt/gravitee/config/kube-config.json
timeoutMs: 3000
namespace: default
```

* No default assumptions are made regarding the location of `kubeConfigFile`. The absence of this file assumes that Gravitee is deployed in Kubernetes and the configuration is in-cluster.&#x20;
* Namespace can be overridden in Secrets URLs via `?namespace=<name>`. If no namespace is provided, the namespace is assumed to be that of the cluster in which the platform is deployed. To fetch from the default namespace, it must be set explicitly, unless Gravitee is deployed in that namespace.

{% hint style="warning" %}
The legacy method of fetching data from Kubernetes Secrets in a Gravitee configuration with syntax `kubernetes://secrets/...` remains available, but is deprecated and should be replaced by `secret://kubenetes/...` .
{% endhint %}

### Hashicorp Vault (plugin id: `vault`)

```yaml
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
    token: [redacted]
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
# for both watch and read
retry:
  attempts: 2          # set '0' to disable
  intervalMs: 1000
# if disabled an error will be displayed at load time if http.ssl.keystore.secret is used with watch enabled
watch:
  enabled: true
  pollIntervalSec: 30
```

### AWS Secret Manager (plugin id: `aws`)

```yaml
enabled: true
region: eu-west-1
# fipsEnabled: false
# connectionTimeoutMs: 5000
# endpointOverride: ...
auth:
  provider: static # or "chain" 
  config:
    accessKeyId: [redacted]
    secretAccessKey: [redacted]
```

If you are running Gravitee in EKS or EC2, you can use`"chain"`as the provider for authentication. See [https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html) for more details.

## Example for configuration&#x20;

A specific location needs to be added to the configuration above to enable secrets. Here is an example:

{% tabs %}
{% tab title="gravitee.yml" %}
```yaml
# configuration-level secret configuration
secrets:
  # plugin id, hence no duplicates
  kubernetes:        
    # configuration
    enabled: true
    kubeConfigFile: /opt/gravitee/config/kube-config.json
    timeoutMs: 3000
    namespace: default
```
{% endtab %}

{% tab title="Helm Charts" %}
```yaml
# for Management API
api:
  secrets:
    kubernetes:
      enabled: true
      # ...
      
# for Gateway
gateway:
  secrets:
    kubernetes:
      enabled: true
      # ...
```
{% endtab %}
{% endtabs %}

Learn more about [configuration-level secrets](configuration-level-secrets.md).

## Example for v4 APIs

{% tabs %}
{% tab title="gravitee.yml" %}
```yaml
# api level secrets
api:
  secrets:
    providers:
      # list allow duplication, see dedicated section
      - plugin: kubernetes
        configuration:
          enabled: true
          kubeConfigFile: /opt/gravitee/config/kube-config.json
          timeoutMs: 3000
          namespace: default
```
{% endtab %}

{% tab title="Helm Charts" %}
```yaml
# api-level secret configuration
api:
  secrets:
    providers:
      # list allow duplication, see dedicated section
      - plugin: kubernetes
        configuration:
          enabled: true
          kubeConfigFile: /opt/gravitee/config/kube-config.json
          timeoutMs: 3000
          namespace: default
```
{% endtab %}
{% endtabs %}

Learn more about [API-level secrets](../../configure-v4-apis/api-level-secrets.md).
