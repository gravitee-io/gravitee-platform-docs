# Secrets Managers

## Introduction

Gravitee offers a set of **secrets managers** in APIM in order to obscure secrets in configuration files and API definitions.

Functionally, secrets managers are `secret-provider` plugins that, when deployed, enable secrets managers to obscure database passwords and certificates in Gravitee Gateway, API Management, and Access Management configuration files and API definitions.

Secrets managers provide a secure and convenient way to encrypt, store, manage, and retrieve secrets and other sensitive data such as tokens, API keys, passwords, and certificates. Using secret managers, it's possible to enforce consistent security policies, ensure resources and digital credentials can only be accessed by authenticated and authorized users, and instantly connect systems to accomplish automated tasks.

## Configuring Secret Managers

You can enable secrets plugins by configuring them in `gravitee.yml`. The configurations for each secrets provider are mentioned below. As with all other configuration from gravitee.yml, you can set these as environment variables as well, in order to keep any information out of files on disk; the syntax is, for example, `GRAVITEE_SECRETS_KUBERNETES_ENABLED=true`.

{% tabs %}
{% tab title="Kubernetes" %}
The configuration in `gravitee.yml` is:

```yaml
secrets:
  kubernetes:
    enabled: true
    kubeConfigFile: /opt/gravitee/config/kube-config.json
    timeoutMs: 3000
    namespace: default
```

Some notes:

* No default assumptions are made regarding the location of `kubeConfigFile`. The absence of this file assumes that Gravitee is deployed in Kubernetes and the configuration is in-cluster.&#x20;
* Namespace can be overridden in URLs via `?namespace=<name>`. If no namespace is provided, the namespace is assumed to be that of the cluster in which the platform is deployed. To fetch from the default namespace, it must be set explicitly, unless Gravitee is deployed in that namespace.

{% hint style="info" %}
The legacy method of fetching configurations from Kubernetes ConfigMaps or Secrets using the syntax `kubernetes://...` remains available, but is discouraged and will be deprecated over future releases. Instead, secret providers retrieve sensitive information (passwords, x509 pairs, etc.) from secret managers (Kubernetes, HC Vault...) to ensure this information does not appear in clear text.
{% endhint %}
{% endtab %}

{% tab title="HashiCorp Vault" %}
The configuration in `gravitee.yml` is:

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

{% tab title="AWS" %}
The configuration in `gravitee.yml` is:

```yaml
secrets:
  aws:
    enabled: true
    region: eu-west-1
    # fipsEnabled: false
    # connectionTimeoutMs: 5000
    # endpointOverride: ...
    auth:
      provider: static # or "chain" 
      config:
        accessKeyId: ...
        secretAccessKey: ...
```

For `chain` auth provider see: [https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html)
{% endtab %}
{% endtabs %}

## Using Secrets in Configuration Files

The configuration in gravitee.yml may contain some sensitive information, e.g. the MongoDB password. In order to obscure this value from the configuration file, you can set the value of the property `MANAGEMENT_MONGODB_PASSWORD` to the name of the secret in the secret provider:

```
secret://vault/secret/gravitee/mongo/password
```

The syntax is `secret://{provider}/{name-of-secret}`. The name of the secret will vary by secret provider.

## Enabling API-Level Secrets

In order to use secrets managers in API configuration, you need to **enable** the secrets manager. This involves adding a new configuration entry in `gravitee.yml` as follows:

```yaml
api:
  secrets:
    providers:
      - plugin: vault
        environments: []
        configuration:
          enabled: true
```

You can then override the configuration of the provider from the top-level `secrets` configuration.

## Using Secrets in API Definitions

In order to use a secret in an API definition, you use the following expression:

```
{#secrets.get('/kubernetes/example', 'foo')}
```

The syntax is `{#secrets.get('<provider>', '<name-of-secret>')}`. The name of the secret will vary by provider.

This secret is stored off-heap and can only be resolved at runtime on the gateway. This value is never logged and cannot be retrieved via printing or any other mechanism.

As the expression is dynamic, it can be added and combined with other EL functions. For example, you can use the value:

```
{#secrets.get(api.properties['my-property'])}
```

You can use secrets in the following configurations in APIs:

### Endpoints

<table><thead><tr><th width="212">Endpoint</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Proxy</td><td>Target URL, header value fields, proxy fields for client connection, TLS configuration</td></tr><tr><td>Kafka</td><td>Bootstrap server list, JAAS config, TLS configuration</td></tr><tr><td>MQTT</td><td>Server host and port, username, password,  TLS configuration</td></tr><tr><td>RabbitMQ</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>Solace</td><td>URL and VPN name, username, password, truststore configuration</td></tr></tbody></table>

### Resources

<table><thead><tr><th width="213">Resource</th><th>Configuration Field</th></tr></thead><tbody><tr><td>OAuth2</td><td>Client ID, Client Secret</td></tr><tr><td>Redis Cache</td><td>Password</td></tr><tr><td>LDAP</td><td>LDAP URL, Base DN, Username, Password</td></tr><tr><td>Inline Authentication</td><td>Username, Password, Role</td></tr></tbody></table>

### Policies

<table><thead><tr><th width="216">Policy</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Callout</td><td>URL, Header Values</td></tr></tbody></table>
