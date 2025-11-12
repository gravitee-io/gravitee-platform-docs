---
description: >-
  Gravitee's secret managers integrations rely on the secret-provider plugin
  type. This page lets you know how to configure these plugins for all use
  cases.
---

# Secret Provider Plugins Configuration

## Introduction

Secrets managers provide a secure and convenient way to encrypt, store, manage, and retrieve secrets and other sensitive data such as tokens, API keys, passwords, and certificates. Using secret managers, it's possible to enforce consistent security policies, ensure resources and digital credentials can only be accessed by authenticated and authorized users, and instantly connect systems to accomplish automated tasks.

Gravitee offers an [integration](docs/apim/4.6/getting-started/integrations.md#secret-managers-integration) with secrets managers to obscure secrets and avoid clear text credentials stored in files or databases.

[Configuration-level secrets](configuration-level-secrets.md) allow you to obscure secrets in `gravitee.yml`, Helm Charts, and environment variables.

[API-level secrets](docs/apim/4.6/configure-v4-apis/api-level-secrets.md) (starting from APIM 4.6) allow v4 APIs to obscure secrets in many plugins, as long as they support [Gravitee Expression Language](docs/apim/4.6/getting-started/gravitee-expression-language.md). &#x20;

Functionally, the secrets managers integrations are handled by`secret-provider` plugins that, when deployed, configured and enabled, allow you to access those third parties to resolve secrets.&#x20;

This capability is available in Gravitee Gateway and API Management for both Access Management and APIM.

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](docs/apim/4.6/overview/enterprise-edition.md) and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Per manager configuration

As with any other plugin, a secret provider plugin must be either bundled or added to the plugin directory.

You can enable `secret-provider` plugins by configuring them in `gravitee.yml`. The configurations for each secret provider plugin are discussed below. As with all other `gravitee.yaml` configurations, you can also set these as [environment variables](docs/apim/4.6/configure-apim/environment-properties.md#using-environment-variables-in-different-installation-methods).

### Use cases

Using a secrets manager integration to obscure sensitive data in a configuration and using a secrets manager integration to obscure sensitive data in an API are two different use cases that are performed independently. \
\
For more information on each use case, check the following sections below:

[#example-for-configuration](secret-provider-plugins-configuration.md#example-for-configuration "mention")

&#x20;[#example-for-v4-apis](secret-provider-plugins-configuration.md#example-for-v4-apis "mention")&#x20;

### Kubernetes (plugin id: `kubernetes`)

<pre class="language-yaml"><code class="lang-yaml">enabled: true
<strong># kubeConfigFile: /opt/gravitee/config/kube-config.json
</strong># timeoutMs: 3000
# namespace: default
</code></pre>

* No default assumptions are made regarding the location of `kubeConfigFile`. The absence of this file assumes that Gravitee is deployed in Kubernetes and the configuration is in-cluster.&#x20;
* Namespace can be overridden in Secrets URLs via `?namespace=<name>`. If no namespace is provided, the namespace is assumed to be that of the cluster in which the platform is deployed. To fetch from the default namespace, it must be set explicitly, unless Gravitee is deployed in that namespace.

{% hint style="warning" %}
The legacy method of fetching data from Kubernetes Secrets in a Gravitee configuration with syntax `kubernetes://secrets/...` remains available, but is deprecated and should be replaced by `secret://kubenetes/...` .
{% endhint %}

### Hashicorp Vault (plugin id: `vault`)

This plugin enables all possible option to access K/V engine of Vault. It can manage the following authentication methods:

* Token
* Userpass
* App Role
* Github
* Certificate (mTLS)
* Kubernetes (short and long lived tokens)

Here is an example configuration:

```yaml
# mandatory
enabled: true
host: 127.0.0.1      
port: 8200
# optional
namespace: default.        # default: "default"
kvEngine: V2               # defaults to v2 can be "v1", no mixing supported
readTimeoutSec: 2
connectTimeoutSec: 3
# required although can be disabled in Vault's dev mode
ssl:
  enabled: false                        # not for production
  # format: "pemfile"                   # one of "pem", "pemfile", "truststore"
  # pem:                                # (only for "pem")
                                        # value is base64 with headers
  # file: /opt/gravitee/vault.pem       # for pemfile truststore files
# mandatory
auth:
  method: token # can also be "github", "userpass", "approle", "cert", "kubenetes"
### token config
  config:
    token: [redacted]
### github config
    # token:
    # path: <optional non standard github auth path>
### userpass config
    # username:
    # password:
    # path: <optional non standard userpass auth path>
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
    # path: <optional non standard cert auth path>
### kubernetes
    # role:
    ## short-lived tokens (default)
    # tokenFile:     # default: "/var/run/secrets/kubernetes.io/serviceaccount/token"
    ## Gravitee service account secret for long-lived tokens
    ## Will supersedes short-lived when set
    # tokenSecret:
    #   name:
    #   namespace:   # current Gravitee namespace if unset
    # path: <optional non standard kubernetes auth path>
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

Here is an example configuration:

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

If you run Gravitee in EKS or EC2, you can use`"chain"`as the provider for authentication. For more information about using `"chain"`, see [Default credentials provider chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html).

## Example configurations to enable secrets

A specific location needs to be added to the configuration above to enable secrets. Here are examples for the following:

* gravitee.yml (all products)
* Helm Charts (APIM)

For more information about configuration-level secrets, see [configuration-level-secrets.md](configuration-level-secrets.md "mention").&#x20;

### gravitee.yml (all products)

Here is an example configuration for enabling secrets in your `gravitee.yml`file:

```yaml
# configuration-level secret configuration
secrets:
  # plugin id, hence no duplicates
  kubernetes:        
    # configuration
    enabled: true
    # ...
```

### Helm Charts (APIM)

Here is an example configuration for enabling secrets in your `values.yml` file:

```yaml
# Works for both APIs and Gateway
secrets:
  kubernetes:
    enabled: true
    # ...
```

## Example configuration for v4 APIs (APIM Gateway)

Here are examples for configuring secrets the following:

* gravitee.yml (all products)
* Helm Charts (APIM)

For more information about API-level secrets, see [api-level-secrets.md](docs/apim/4.6/configure-v4-apis/api-level-secrets.md "mention").

### gravitee.yml

Here is an example configuration for v4 APIs for a `gravitee.yml`file:

```yaml
# api level secrets
api:
  secrets:
    providers:
      # list allow duplication, see dedicated section
      - plugin: kubernetes
        configuration:
          enabled: true
          # ...
```

### Helm Charts

Here is an example configuration for v4 APIs for your `values.yml` file:

```yaml
# api-level secret configuration
gateway:
  api:
    secrets:
      providers:
        # list allow plugin duplication, see dedicated section
        - plugin: kubernetes
          configuration:
            enabled: true
            # ...
```
