# Apply Secrets to APIs

## Overview

You can configure secrets managers to work with your APIs. You can use secrets to hide information in any field that supports Gravitee Expression Language. For more information about Gravitee Expression Language, see [gravitee-expression-language.md](../../gravitee-expression-language.md "mention").

Secret provider plugins extend the operable range of secret managers to resolve secrets on startup and resolve secrets in APIs. For more information about secret provider plugins, see [integrations.md](../../readme/integrations.md "mention").

This article explains the syntax used to resolve secrets in v4 APIs and configure secret managers.

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](../../readme/enterprise-edition.md) and what is included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Prerequisites to enable this feature

1. You must configure one of the following secret managers in your `gravitee.yml` file or using the equivalent [environment variable](./): Kubernetes, Amazon Secret Manager, or Hashicorp Vault. For more information about these secret managers, see [Integrations](../../readme/integrations.md#secret-managers-integration).
2. Reference those secrets in your API definitions with a specialized syntax.

## Configuring Gravitee to access secret managers

### Secret provider configuration for APIs

{% hint style="info" %}
Secrets work in only v4 APIs.
{% endhint %}

You can configure access to secret managers using `secret-provider` plugins.

{% hint style="warning" %}
Configuring access to plugins is not the same as [configuring access to secrets](apply-secrets-to-configurations.md). This section discusses the plugin configuration, which is different from the `secrets` section of the configuration.
{% endhint %}

Below are examples of setting the configuration parameters for secret providers. To configure secret provider plugins, see [Secret Provider Plugins Configuration](configure-secret-provider-plugins.md).

#### `gravitee.yml`

```yaml
api:
  secrets:
    providers:
      - plugin: <plugin_id>      # mandatory: e.g. vault
        configuration:           # plugin configuration, see dedicated section
          enabled: true          # mantadory to enable the plugin
          # here lay the rest of the config
      - plugin: <another>
        configuration: 
        # ...
    retryOnError:                # when error occurs while resolving
      enabled: true
      delay: 2                   
      unit: SECONDS
      backoffFactor: 1.5
      maxDelay: 60
      maxAttempt: 10
```

#### Environment variables

You can add the following environment variables to your `gravitee.yml` file to configure secret providers:

```sh
GRAVITEE_API_SECRETS_PROVIDERS_0_PLUGIN="<plugin id>"
GRAVITEE_API_SECRETS_PROVIDERS_0_CONFIGURATION_ENABLED="true"
GRAVITEE_API_SECRETS_PROVIDERS_0_CONFIGURATION_SOME_PARAM="some value" # etc.
GRAVITEE_API_SECRETS_RETRY_ON_ERROR_ENABLED="true"
GRAVITEE_API_SECRETS_RETRY_ON_ERROR_DELAY="2"
# etc.
```

#### Helm Charts

```yaml
# values.yml
gateway:
  # starting from here it is identical to gravitee.yml
  api:
    secrets:
      providers:
        - plugin: 
      retryOnError:
        enabled: true

```

### Advanced configuration

#### Use configuration-level secrets to configuration API-level secrets

If you want to hide sensitive information in a secret manager, you must secure credentials. You can use [apply-secrets-to-configurations.md](apply-secrets-to-configurations.md "mention") to hide credentials in `gravitee.yml`.

Here is an example with Kubernetes:

```yaml
# this allows resolving the Kube secret into the configuration
secrets:
 kubernetes:
   enabled: true

# as an example
db:
  mongo:
    password: secret://kubernetes/mongo:password

# now use Kube to configure API-level secrets
api:
  secrets:
    providers:
      - plugin: <plugin_id>      
        configuration:           
          enabled: true          
          auth:
            method: token
            token: secret://kubernetes/secret-provider:token
```

#### Restrict to selected environments

By default, secret providers are available for all environments the APIM Gateway manages. This availability means that all APIs deployed on that Gateway can access all secret providers.

You can specialize a secret provider to a set of environments. If all providers are configured like this, an API deployed on another environment triggers a secret resolution error.

```yaml
api:
  secrets:
    providers:
      - plugin: <plugin_id>      
        environments:
          - b5c8c703-fc12-404d-bf61-22fa19998435
          - 2b4db0b1-8eeb-4410-a50b-dbf83fb55b2c
        configuration:           
          enabled: true          
          # ...
      - plugin: <another>
        environments:
          - 4787fa8b-5e45-41ec-9df8-a3f3061d0412
        configuration: 
          # ...
```

{% hint style="warning" %}
Environments are referenced using their UUIDs. "hrids" are not supported here.
{% endhint %}

#### Using a secret provider plugin more than once

For a setup with multiple environments, it is possible to use the same secret manager with different credentials, depending on the environment.

```yaml
api:
  secrets:
    providers:
      - id: dev
        plugin: <plugin_id_1>      
        environments:
          - b5c8c703-fc12-404d-bf61-22fa19998435
        configuration:           
          enabled: true          
          auth:
            method: token
            token: 9887DSKflkjdf53EZzhkjchs
      - id: test
        plugin: <plugin_id_1>
        environments:
          - 4787fa8b-5e45-41ec-9df8-a3f3061d0412
        configuration: 
          enabled: true          
            auth:
              method: token
              token: fjdhfj765756dksjhds587
```

This syntax has an impact on how you reference secrets. For more information about syntax references, see[#secret-reference-syntax](apply-secrets-to-apis.md#secret-reference-syntax "mention").

## Secret reference syntax

Secrets can be resolved in fields that support [Gravitee Expression Language (EL)](../../gravitee-expression-language.md). However, not all fields that support EL allow the resolution of secrets. In general, any field supporting EL that may contain sensitive information is likely to support secrets, such as URLs, header values, passwords, and SSL/TLS settings.

### General syntax

`{#secrets.get(<first arg>)}`

`{#secrets.get(<first arg>, <second arg>)}`

Arguments can be:

* Static strings, surrounded by simple quotes:`'`
* EL (mix-in syntax)

{% hint style="info" %}
The syntax MUST start with `{#secrets.get(` - no space allowed anywhere between `{` and `(`

The syntax MUST end with `)}` - no space allowed between `)` and `}`
{% endhint %}

Like any other EL, it can be embedded in a larger string, such as:

`"My password is {#secrets.get(<first arg>)} and should remain a secret"`

### Secret URI syntax

Secret URI syntax is a subset of secret URLs you can use with [apply-secrets-to-configurations.md](apply-secrets-to-configurations.md "mention") (`secret://...`). Secret URI syntax allows you to specify the secret you want to resolve.

A URI is composed of the following components:

`/`<mark style="color:red;">`<provider>`</mark>`/`<mark style="color:green;">`<path>`</mark>`:`<mark style="color:yellow;">`<key>`</mark>

* <mark style="color:red;">`provider`</mark>: The **id** or **plugin id** used to resolve secrets. It cannot contains `'/'`.
* <mark style="color:green;">`path`</mark>: The location of the secret in the secret manager. It can be a path, a name, or an ID. It is specific to each secret manager it cannot contain `':'`.
* <mark style="color:yellow;">`key`</mark>: Secrets are returned as maps (key/value pairs). The key allows you to get one value of that map and is expected to be provided either as part of the URI (with ':' separator) or as a separate argument.

### Static secret reference

A static secret reference is the simplest way to access a secret because it points directly to a secret value. It uses the URI syntax and comes in two flavors:

* `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`')}`
* `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`', '`<mark style="color:yellow;">`key`</mark>`')}`

### Static URI with key in EL

A static URI with the key written in EL works the same way as a static reference, except the key is evaluated when the secret EL is evaluated.

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>` ',`` `` `<mark style="color:blue;">`#expression_to_get_key`</mark>`)}`

## Secret resolution and evaluation

### Resolution

Secret references are discovered when an API is deployed. The EL is parsed (not evaluated), the URI is extracted, and then the secret can be resolved.

{% hint style="info" %}
This resolution does not require network I/O, so does not need time to happen before the API is called.
{% endhint %}

A first resolution occurs, blocking the deployment process for a short while. If retry on error is enabled and an error occurs, retry attempts occur in the background. This frees the deployment process for other APIs to be deployed.

Once a secret is resolved, whether it is found or in error, then other APIs won't attempt a new resolution on the same URI. The result is already cached.

### Evaluation

Although secrets are resolved at the time of deployment, the secret reference is not evaluated immediately. You can access different context data both depending on the plugin and when the EL is evaluated.

For more information on what you can access, see [gravitee-expression-language.md](../../gravitee-expression-language.md "mention").

### Secrets evaluated during API deployment

The following plugins evaluate EL just after the secret is resolved as part of their deployment process:

* HTTP Proxy endpoint
* Resources

When the key is an EL, those plugins can only access dictionaries and API properties. For example:

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`redis`</mark>`',`<mark style="color:yellow;">`#dictionary['redis']['password-key']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved when the API is deployed, the API will not be deployed. Errors will be shown in the logs, and a caller will received a 404 error for HTTP APIs.
{% endhint %}

### Secrets evaluated within API traffic

The following are plugins that evaluate EL strictly at runtime (when the API is called):

* All message endpoints supporting secrets, on a new API call.
* Policies supporting EL, on initialization or on each call.

When the key is an EL, those plugins can access attributes, content, request/subscribe data, and response/publish data.

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`apis-tokens`</mark>`',`<mark style="color:yellow;">`#request.headers['PartnerId']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved and retry is activated, the API will be deployed, but executing the policy or endpoint will fail until retry resolves the secret.
{% endhint %}

## Use cases

### Redis Cache example

Consider the following provider configuration (extract):

```yaml
api:
  secrets:
    providers:
      - plugin: vault
        configuration:
          enabled: true
          # ...
```

And a secret in HC Vault created as follows:

```
vault kv put -mount=secret gravitee/passwords -redis="[redacted]" ...
```

If you want to secure the Redis password, you can configure the resource as follows (extract):

<pre class="language-json"><code class="lang-json"><strong>{
</strong><strong>    "name": "My API v4",
</strong>    "gravitee": "4.0.0",
    "type": "proxy",
    // ...
    "resources":[{
        "enabled" : true,
        "configuration" : {
            "password" : "{#secrets.get('/vault/secret/gravitee/passwords', 'redis')}",
            "standalone": {
                "host" : "{#dictionaries['redis']['host']}",
                "port" : 6379
            }
        }
    }]
}
</code></pre>

You can see here that the definition does not contain a clear text secret. This definition is saved as is, and resolution occurs once it is deployed on APIM Gateway. When the API is actually started, the resource is initialized and the secret is evaluated and used to connect to Redis.

Here is an example of referencing a secret when you configure a Redis Cache resource:

<figure><img src="../../../4.6/.gitbook/assets/image (142) (1).png" alt=""><figcaption></figcaption></figure>

### Native Kafka endpoint API example

Consider the following provider configuration (extract):

```yaml
api:
  secrets:
    providers:
      - plugin: kubernetes
        configuration:
           enabled: true
```

And a Secret in Kubernetes created as follows:

```
kubectl create secret generic kafka-auth --from-literal\
    scram-username=[redacted]\
    scram-password=[redacted]
```

If you want to use this token to configure SCRAM authentication, this how you can do it:

```json
{
  "name": "My Native API",
  "gravitee": "4.0.0",
  "type": "native",
  "endpointGroups": [
    {
      "name": "default-native",
      "type": "native-kafka",
      "loadBalancer": {
        "type": "round-robin"
      },
      "endpoints": [
        {
          "name": "default-native",
          "type": "native-kafka",
          "weight": 1,
          "configuration": {
            "bootstrapServers": "localhost:9099"
          }
        }
      ],
      "sharedConfiguration": {
        "security": {
          "protocol": "SASL_PLAINTEXT",
          "sasl": {
            "mechanism": {
              "type": "SCRAM-SHA-256",
              "username": "{#secrets.get('/kubernetes/kafka-auth', 'scram-username')}",
              "password": "{#secrets.get('/kubernetes/kafka-auth', 'scram-password')}"
            }
          }
        }
      }
    }
  ]
  // ...
}
```

You can see here that the definition does not contain a clear text secret. This definition will be saved as is, and the resolution occurs once it is deployed on APIM Gateway. The `kafka-auth` secret is resolved once. Then, when the API is actually called and the backend Kafka client is created, the secret is evaluated to be used for authentication.

Here is an example of referencing a secret during a SASL configuration:

<figure><img src="../../../4.6/.gitbook/assets/Screenshot 2025-01-23 at 13.54.01 (1).png" alt=""><figcaption></figcaption></figure>

### Hiding secret provider plugin

When configuring secret providers, you can use the "`id`" parameter to "hide" the secret provider implementation shown by the "`plugin`" parameter. This way, the value of "`id`" is used instead of the plugin name.

Considering the following provider configuration (extract):

```yaml
api:
  secrets:
    providers:
      - id: secret-data
        plugin: vault
        configuration:
           enabled: true
           
```

Then a secret reference will look like this :

`{#secrets.get('/`<mark style="color:red;">`secret-data`</mark>`/`<mark style="color:green;">`secret/gravitee/passwords`</mark>`', '`<mark style="color:yellow;">`redis`</mark>`')}`

## Resolved secrets stay secured

Credentials to access secret managers are set in the Gravitee configuration, and only system admins are allowed to manipulate them. These credentials can also be hidden in secret managers. No user of any Gravitee UI can gain access to them.

Secrets are resolved in the Gateway, never when the API is saved. No user of any Gravitee UI can see the value of a secret. Therefore, as soon as the Gateway stops or the API is undeployed (see cache considerations below) those secrets are no longer accessible.

Secrets are resolved ,then stored in a cache. Cached data stays off-heap, preventing admin users from dumping JVM memory using a Gravitee admin endpoint.

## Consequence of caching secrets

Secrets are resolved and cached when the API is deployed, then the cache is accessed when EL are evaluated. This has several consequences:

* The first API to use a given secret URI (e.g., `/kubernetes/my-secret)`will resolve the secret, and all key/values in it. Subsequent APIs using a secret with the same URI (and maybe a different key) will not trigger a new resolution.
* For a given secret URI, a secret reference using a key that is not present in the cache will trigger a resolution of the secret, and only that key will be added.
* Fields not supporting secrets will fail evaluation although the secret is present in the cache. That might seem counterintuitive, but when an API is deployed and secrets are discovered, the Gateway does not know which field contains a secret. At runtime, when the EL is evaluated, the EL context contains information about the field, and then access to the secret can be denied.

### Known limitations

* If the value of a secret (e.g., a password) changes in the secret manager for a key that is already cached, then it will not be updated by the Gateway, unless:
  * All APIs using that secret URI are undeployed. Then, one of the APIs using that secret URI is redeployed.
  * This also is true if the secret was never resolved due to an error or because it does not exist. The cache is populated with an error or an empty secret that allows Gravitee to report an error at runtime that is specific to each case.

Limitations will be addressed in future releases when the secret lifecycle is managed by the Management API and secret resolution does not only depend on the API being deployed. This will allow renewal, applying restrictions to where they are consumed.

## Plugin supporting secrets

### Native endpoints

| Endpoint | Configuration FIeld                                   |
| -------- | ----------------------------------------------------- |
| Kafka    | Bootstrap server list, JAAS config, TLS configuration |

### Endpoints

<table><thead><tr><th width="212">Endpoint</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Proxy</td><td>Target URL, header value fields, proxy fields for client connection, TLS configuration</td></tr><tr><td>Kafka</td><td>Bootstrap server list, JAAS config, TLS configuration</td></tr><tr><td>MQTT</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>RabbitMQ</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>Solace</td><td>URL and VPN name, username, password, truststore configuration</td></tr></tbody></table>

### Resources

<table><thead><tr><th width="213">Resource</th><th>Configuration Field</th></tr></thead><tbody><tr><td>OAuth2</td><td>Client ID, Client Secret</td></tr><tr><td>Redis Cache</td><td>Password</td></tr><tr><td>LDAP</td><td>LDAP URL, Base DN, Username, Password</td></tr></tbody></table>

### Policies

<table><thead><tr><th width="216">Policy</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Callout</td><td>URL, Header Values</td></tr><tr><td>Assign attribute</td><td>Attribute value</td></tr><tr><td>Transform headers</td><td>Header value</td></tr><tr><td>Transform query param</td><td>Param value</td></tr><tr><td>Traffic shadowing</td><td>URL, Header Values</td></tr><tr><td>Any other that supports EL</td><td></td></tr></tbody></table>

## Configuration reference

<table data-full-width="true"><thead><tr><th width="360">Property</th><th width="93" data-type="checkbox">Required</th><th width="326">Description</th><th width="103">Type</th><th>Default</th></tr></thead><tbody><tr><td><code>providers[]</code></td><td>true</td><td>Secret providers</td><td>array</td><td></td></tr><tr><td><code>providers[].id</code></td><td>false</td><td>alias id for the secret-provider plugin</td><td>string</td><td>providers[].plugin</td></tr><tr><td><code>providers[].plugin</code></td><td>true</td><td>secret-provider plugin id</td><td>string</td><td></td></tr><tr><td><code>providers[].configuration.enabled</code></td><td>false</td><td>Enables this secret-provider</td><td>boolean</td><td>true</td></tr><tr><td><code>providers[].configuration.*</code></td><td>true</td><td>Configuration of the plugin (see dedicated section)</td><td>multiple</td><td></td></tr><tr><td><code>providers[].environments[]</code></td><td>false</td><td>Environment IDs (not hrid) on which the provider can be used.</td><td>array</td><td>empty<br>means <strong>all</strong> environments</td></tr><tr><td><code>retryOnError.enabled</code></td><td>false</td><td>Enable providers to retry fetching secret on errors except when a secret URI point to provider that is not configured.</td><td>boolean</td><td>true</td></tr><tr><td><code>retryOnError.delay</code></td><td>false</td><td>Initial delay between retries</td><td>integer</td><td>2</td></tr><tr><td><code>retryOnError.unit</code></td><td>false</td><td>Delay unit, values: MILLISECONDS, SECONDS, MINUTES</td><td>enum</td><td>SECONDS</td></tr><tr><td><code>retryOnError.backoffFactor</code></td><td>false</td><td>Backoff exponential factor between retries, 1=linear. 1.5 is considered "soft" backoff</td><td>float</td><td>1.5</td></tr><tr><td><code>retryOnError.maxDelay</code></td><td>false</td><td>Max delay between retries</td><td>integer</td><td>60</td></tr><tr><td><code>retryOnError.maxAttempt</code></td><td>false</td><td>Max attempt, after that the secret is marked in "error" in the cache</td><td>integer</td><td>10</td></tr></tbody></table>
