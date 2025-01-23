---
description: Configuration and syntax to access secrets within v4 APIs.
---

# API-Level Secrets

## Overview

You can configure secrets managers to work with your APIs. You can use secrets to hide information in any field that supports Gravitee Expression Language. For more information about Gravitee Expression Language, see [gravitee-expression-language.md](../getting-started/gravitee-expression-language.md "mention").

Secret provider plugins extend the operable range of secret managers to resolve secrets on startup and resolve secrets in APIs. For more information about these plugins, see [integrations.md](../getting-started/integrations.md "mention").

This article explains the syntax for resolving secrets in v4 APIs and configuring secret managers with `secret-provider` plugins.

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](../overview/enterprise-edition.md) and what is included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Prerequisites to enable this feature

1. You must configure one of the following secret managers in your `gravitee.yml` file or using the equivalent [environment variable](../configure-apim/environment-properties.md): Kubernetes, Amazon Secret Manager, or Hashicorp Vault. For more information about these secret managers, see [Integrations](../getting-started/integrations.md#secret-managers-integration).
2. Reference those secrets in your API definitions with a specialized syntax.

## Configuring Gravitee to access secret managers

### Secret provider configuration for APIs

{% hint style="info" %}
Secrets work in only v4 APIs.
{% endhint %}

You can configure access to secret managers using `secret-provider`s plugins. Note that this section is different from [configuration-level-secrets.md](../configure-apim/sensitive-data-management/configuration-level-secrets.md "mention"), this means the plugin configuration, even if similar is not shared with the `secrets` section of the configuration.

Here are the configurations parameters to configure secret providers. To configure Secret Provider Plugins, see [secret-provider-plugins-configuration.md](../configure-apim/sensitive-data-management/secret-provider-plugins-configuration.md "mention").

#### gravitee.yml

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

#### Environment variable

You can add the following environment variables to your gravitee.yml file to configure secret providers:&#x20;

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

If you want to hide sensitive information in a Secret Manager, you must secure credentials. You can use [configuration-level-secrets.md](../configure-apim/sensitive-data-management/configuration-level-secrets.md "mention") to hide credentials in gravitee.yml.&#x20;

Here is an example with kubernetes:

```yaml
# this allows to resolve Kube secret into the configuration
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

By default, secrets providers are available for all environments the APIM Gateway manages. This availability means that all API deployed on that Gateway can access all secret providers.

You can specialize a secret-provider to a set of environments. If all providers are configured like this, an API deployed on another environments triggers a secret resolution error.

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
Beware environment are referenced using their UUIDs, "hrids" are not supported here.
{% endhint %}

#### Using a secret-provider plugin more than once

On multiple environments setup, it is possible to have the same secret manager with different credentials depending on the environment.

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

This syntax has an impact on how you reference secrets. For more information about Syntax references, see [#syntax-for-referring-to-a-secret](api-level-secrets.md#syntax-for-referring-to-a-secret "mention") to know more.

## Secret reference syntax

Secrets can be resolved in field supporting Expression Language (EL). Despite supporting EL, some fields may not allow resolution of secrets. Any field supporting EL that may contain sensitive information is likely to support secrets. For example, urls, header values, passwords, and SSL/TLS settings.

### General syntax

`{#secrets.get(<first arg>)}`

`{#secrets.get(<first arg>, <second arg>)}`

Arguments can be

* Static strings, surrounded by simple quotes:`'`&#x20;
* EL (mix-in syntax)

{% hint style="info" %}
It MUST start with `{#secrets.get(` - no space allowed anywhere between `{` and `(`

It MUST end with `)}` - no space allowed between `)` and `}`
{% endhint %}

Like any other EL, it can be embedded in a larger string such as :&#x20;

`"My password is {#secrets.get(<first arg>)} and should remain a secret"`

### Secret URI syntax

Secret URI syntax is a subset of secrets URLs you can use with [configuration-level-secrets.md](../configure-apim/sensitive-data-management/configuration-level-secrets.md "mention") (`secret://...`)  and allow you to specify the secret to resolve.

A URI is composed of the following components:

`/`<mark style="color:red;">`<provider>`</mark>`/`<mark style="color:green;">`<path>`</mark>`:`<mark style="color:yellow;">`<key>`</mark>

* <mark style="color:red;">`provider`</mark>: the **id** or **plugin id** used to resolve secrets, it cannot contains `'/'`&#x20;
* <mark style="color:green;">`path`</mark>: location of the secret in the secret manager, can be a path, a name, an ID: it is specific to each secret manager it cannot contain `':'`
* <mark style="color:yellow;">`key`</mark>: secret are returned as maps (key/value pairs) the key allows to get one value of that map. It is expected to be provided either as part of the URI (with ':' separator) or as a separate argument.

### Static secret references

Simplest way to access a secret as it points directly to a secret value.

They use the URI syntax and comes in two flavours:

* `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`')}`&#x20;
* `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`', '`<mark style="color:yellow;">`key`</mark>`')}`

### Static URI with key as EL

It works the same way as a static reference, except the key is evaluated when the secret EL is evaluated.

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`',`` `<mark style="color:blue;">`#expression_to_get_key`</mark>`)}`

## Secret resolution and evaluation

### Resolution

Secret references are discovered when an API is deployed. The EL is not evaluated but parse, URI is extracted, and then the secret can be resolved. This method this resolution does not require network I/O and therefore time to happen before the API is called.

A first resolution occurs, blocking the deployment process for a short while. If retry on error is enabled  and an error occurs, then retry attempts occur in the background freeing the deployment process for other API to be deployed.

Once a secret is resolved, whether it is found or in error, then other API won't attempt a new resolution on the same URI the result they are already cached.

### Evaluation

Although secret are resolved at deployment time, the secret reference is not evaluated immediately. Besides depending on the plugin you can access different context data depending on when the EL is evaluated.

For more detail about what you can access see [gravitee-expression-language.md](../getting-started/gravitee-expression-language.md "mention")

### Secrets evaluated during API deployment

Plugins that will evaluate EL just after the secret is resolved as part of there deployment process:

* HTTP Proxy endpoint
* Resources

When the key is an EL those plugin can access only access: dictionary and api properties, e.g. &#x20;

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`redis`</mark>`',`<mark style="color:yellow;">`#dictionary['redis']['password-key']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved when the API is deployed, the API will not be deployed. Errors will be shown in the logs and a caller will received a 404 error for HTTP APIs.
{% endhint %}

### Secrets evaluated within API traffic

Plugins that will evaluate EL strictly at runtime (when the API is called)

* all messages endpoints supporting secrets, on a new API call&#x20;
* policies supporting EL, on initialisation or on each call

&#x20;When the key is an EL those plugins can access: attributes, content, request/subscribe and response/publish data.

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`apis-tokens`</mark>`',`<mark style="color:yellow;">`#request.headers['PartnerId']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved, and retry is activated the API will be deployed, but executing the policy or endpoint will failed until retry resolves the secret.
{% endhint %}

## Uses cases

### Redis Cache example

Considering the following provider configuration (extract):

```yaml
api:
  secrets:
    providers:
      - plugin: vault
        configuration:
          enabled: true
          # ...
```

And a secret in HC Vault created as follow:

```
vault kv put -mount=secret gravitee/passwords -redis="[redacted]" ...
```

If you want to secure Redis password, you can configure the resource as follow (extract)

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

You can see here that the definition does not contain a clear text secret. This definition is saved as is, and resolution occur once deployed on APIM Gateway. When the API is actually started the resource is being initialised and the secret evaluated and used to connect to Redis.

### Native Kafka Endpoint API example

Considering the following provider configuration (extract):

```yaml
api:
  secrets:
    providers:
      - plugin: kubernetes
        configuration:
           enabled: true
```

And a secret in Kubernetes created as follow:

```
kubectl create secret generic kafka-auth --from-literal\
    scram-username=[redacted]\
    scram-password=[redacted]
```

If you want to use this token to configure SCRAM authentication, this how you can do it :&#x20;

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

You can see here that the definition does not contain a clear text secret. This definition will be saved as is, and resolution will occur once deployed on APIM Gateway. The `kafka-auth` secret will resolved once. Then, when the API is actually called and the backend Kafka client created, the secret evaluated to be used for authentication.

### Hiding secret provider plugin

When configuring secret providers, you can use "`id`" parameter to "hide" the secret provider implementation given by "`plugin`" parameter. This way the value of "id" is used instead of the plugin name.

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

Then a secret reference will look like this :&#x20;

`{#secrets.get('/`<mark style="color:red;">`secret-data`</mark>`/`<mark style="color:green;">`secret/gravitee/passwords`</mark>`', '`<mark style="color:yellow;">`redis`</mark>`')}`

## Resolved secrets stay secured

Credentials to access Secret Managers are set in Gravitee configuration allowing only system admin to manipulate them. Note that those credentials can also be hidden in Secret Managers, see configuration section. No user using any Gravitee UI can gain access to those.

Secrets are resolved in the Gateway, never when the API is saved. No user in Gravitee UI can see the value of a secret. Therefor as soon as the Gateway stops or the API un-deployed (see cache considerations below) those secrets are no longer accessible.

Secrets are resolved then stored in a cache. Cached data stay off-heap preventing admin users from dumping JVM memory using Gravitee admin endpoint.

## Consequence of caching secrets

Secret are resolved and cached when the API is deployed, then the cache is accessed when EL are evaluated. This has several consequences:

* The first API to use a given secret URI (e.g `/kubernetes/my-secret)`will resolve the secret, and all key/values in it. Thus, following APIs using a secret with the same URI (and maybe a different key) will not trigger a new resolution.
* For a given secret URI, a secret reference uses a key that is not present in the cache will trigger a resolution of the secret, and that key only will added.
* Fields not supporting secrets will fail being evaluated although the secret is present in the cache. That might counter intuitive, but when API is deployed and secrets are discovered, the Gateway does not know which field contains a secret, but at runtime with the EL is evaluated, the EL context contains information on the field and then accessing the secret can be denied.

### Know limitations

* If the value of a secret (e.g. a password) changes in the Secret Managers for a key that is already cached, then it will not be updated by the Gateway unless:
  * All APIs using that secret URI are undeployed, then one of the API using that secret URI is redeployed
  * This also is true if the secret was never resolved due to an error or because it does not exists. The cache is populated with an error or an empty secret that allow gravitee to report an error at runtime that is specific to each case.

Limitations will be addressed in future releases when secret lifecycle are managed by the Management API and their resolution not only depends on API being deployed. This will allow renewal applying restriction to where they are consumed.

## Plugin supporting secrets

### Native endpoints

| Endpoint | Configuration FIeld                                   |
| -------- | ----------------------------------------------------- |
| Kafka    | Bootstrap server list, JAAS config, TLS configuration |

### Endpoints

<table><thead><tr><th width="212">Endpoint</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Proxy</td><td>Target URL, header value fields, proxy fields for client connection, TLS configuration</td></tr><tr><td>Kafka</td><td>Bootstrap server list, JAAS config, TLS configuration</td></tr><tr><td>MQTT</td><td>Server host and port, username, password,  TLS configuration</td></tr><tr><td>RabbitMQ</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>Solace</td><td>URL and VPN name, username, password, truststore configuration</td></tr></tbody></table>

### Resources

<table><thead><tr><th width="213">Resource</th><th>Configuration Field</th></tr></thead><tbody><tr><td>OAuth2</td><td>Client ID, Client Secret</td></tr><tr><td>Redis Cache</td><td>Password</td></tr><tr><td>LDAP</td><td>LDAP URL, Base DN, Username, Password</td></tr></tbody></table>

### Policies

<table><thead><tr><th width="216">Policy</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Callout</td><td>URL, Header Values</td></tr><tr><td>Assign attribut</td><td>Attribute value</td></tr><tr><td>Transform headers</td><td>Header value</td></tr><tr><td>Transform query param</td><td>Param value</td></tr><tr><td>Traffic shadowing</td><td>URL, Header Values</td></tr><tr><td>Any other that supports EL</td><td></td></tr></tbody></table>

## Configuration reference

<table data-full-width="true"><thead><tr><th width="360">Property</th><th width="93" data-type="checkbox">Required</th><th width="326">Description</th><th width="103">Type</th><th>Default</th></tr></thead><tbody><tr><td><code>providers[]</code></td><td>true</td><td>Secret providers</td><td>array</td><td></td></tr><tr><td><code>providers[].id</code></td><td>false</td><td>alias id for the secret-provider plugin</td><td>string</td><td>providers[].plugin</td></tr><tr><td><code>providers[].plugin</code></td><td>true</td><td>secret-provider plugin id</td><td>string</td><td></td></tr><tr><td><code>providers[].configuration.enabled</code></td><td>false</td><td>Enables this secret-provider</td><td>boolean</td><td>true</td></tr><tr><td><code>providers[].configuration.*</code></td><td>true</td><td>Configuration of the plugin (see dedicated section)</td><td>multiple</td><td></td></tr><tr><td><code>providers[].environments[]</code></td><td>false</td><td>Environment IDs (not hrid) on which the provider can be used.</td><td>array</td><td>empty <br>means  <strong>all</strong> environments</td></tr><tr><td><code>retryOnError.enabled</code></td><td>false</td><td>Enable providers to retry fetching secret on errors except when a secret URI point to provider that is not configured.</td><td>boolean</td><td>true</td></tr><tr><td><code>retryOnError.delay</code></td><td>false</td><td>Initial delay between retries</td><td>integer</td><td>2</td></tr><tr><td><code>retryOnError.unit</code></td><td>false</td><td>Delay unit, values: MILLISECONDS, SECONDS, MINUTES</td><td>enum</td><td>SECONDS</td></tr><tr><td><code>retryOnError.backoffFactor</code></td><td>false</td><td>Backoff exponential factor between retries, 1=linear. 1.5 is considered "soft" backoff</td><td>float</td><td>1.5</td></tr><tr><td><code>retryOnError.maxDelay</code></td><td>false</td><td>Max delay between retries</td><td>integer</td><td>60</td></tr><tr><td><code>retryOnError.maxAttempt</code></td><td>false</td><td>Max attempt, after that the secret is marked in "error" in the cache</td><td>integer</td><td>10</td></tr></tbody></table>

