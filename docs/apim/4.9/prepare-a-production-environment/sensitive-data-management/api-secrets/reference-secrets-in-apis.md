---
description: An overview about reference secrets in apis.
---

# Reference Secrets in APIs

## Overview

You can configure secret managers to work with your APIs. You can use secrets to hide information in any field that supports Gravitee Expression Language. For more information about Gravitee Expression Language, see [gravitee-expression-language.md](../../../gravitee-expression-language.md "mention").

Secret provider plugins extend the operable range of secret managers to resolve secrets both on startup and in APIs. For more information about secret provider plugins, see [integrations.md](../../../readme/integrations.md "mention").

This article explains the syntax that you can use to resolve secrets in v4 APIs and configure secret managers.

{% hint style="warning" %}
* This feature is available in Enterprise Edition only. To learn more about Gravitee Enterprise Edition, see [enterprise-edition.md](../../../readme/enterprise-edition.md "mention").
* Secrets work with only v4 APIs.
{% endhint %}

## Reference a secret with specialized syntax

Secrets can be resolved in fields that support [Gravitee Expression Language (EL)](./). Only some fields that support EL allow the resolution of secrets. In general, any field supporting EL that may contain sensitive information support secrets, such as URLs, header values, passwords, and SSL/TLS settings.

### General syntax

`{#secrets.get('<path to secret>')}`

Arguments can have the following formats:

* Static strings, surrounded by simple quotes: `'`
* EL (mix-in syntax)

{% hint style="info" %}
- The syntax must start with `{#secrets.get(`. No spaces are allowed anywhere between `{` and `(`.
- The syntax must end with `)}` . There must be no space between `)` and `}`.
{% endhint %}

Arguments can be embedded in a larger string, like in the following example:

`"My password is {#secrets.get('<path to secret>')} and should remain a secret"`

### Secret URI syntax

Secret URI syntax is a subset of URL syntax that you can use to [apply secrets to configurations ](../configure-secrets/configuration.md)(`secret://...`). Secret URI syntax allows you to specify the secret you want to resolve.

A URI is composed of the following components:

`/`<mark style="color:red;">`<provider>`</mark>`/`<mark style="color:green;">`<path>`</mark>`:`<mark style="color:yellow;">`<key>`</mark> `?`<mark style="color:orange;">`<query_paramter>`</mark>

* <mark style="color:red;">`provider`</mark>: The **id** or **plugin id** used to resolve secrets. It cannot contain `'/'`.
* <mark style="color:green;">`path`</mark>: The location of the secret in the secret manager. It can be a path, a name, or an ID. It is specific to each secret manager. It cannot contain `':'`.
* <mark style="color:yellow;">`key`</mark>: Secrets are returned as maps (key/value pairs). The key allows you to get one value of that map and is expected to be provided either as part of the URI, with `':'` separator, or as a separate argument.
* <mark style="color:orange;">`query_paramter`</mark>: This is an option to control secret resolution.
  * The syntax is similar to that of a URL: `key1=value&key2=value2`.

### Static secret reference

A static secret reference points directly to a secret value. It uses the following URI syntax:

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`')}`

Here is the URI syntax with query parameters:

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`?`<mark style="color:orange;">`query_paramter`</mark>`')}`

### Static URI with key in EL

A static URI with the key written in EL works the same way as a static reference, except the key is evaluated when the secret EL is evaluated. Here is an an example:

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`#expression_to_get_key`</mark>`')}`

Here is an example with query parameters:

`{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`#expression_to_get_key`</mark>`?`<mark style="color:orange;">`query_paramter`</mark>`')}`

### Dynamic URI

You can specific the secret using an EL. Here some example uses cases:

* Compute the secret path depending on the request information.
* Make the secret path different between environments using dictionaries.

Here is an example with a Dynamic URI:

`{#secrets.get('#expression_to_get_the_secret_path')}`

Here is an example with query parameters:

`{#secrets.get('#expression_to_get_the_secret_path?`<mark style="color:orange;">`query_paramter`</mark>`')}`

## Secret resolution and evaluation

### Resolution

Secret references are discovered when an API is deployed. When the EL is parsed, not evaluated, the URI is extracted, and then the secret can be resolved.

When the first resolution occurs, it blocks the deployment process for a short while. If retry on error is enabled and an error occurs, retry attempts occur in the background. This frees the deployment process for other APIs to be deployed.

Once a secret is resolved, whether it is found or in error, then other APIs do not attempt a new resolution on the same URI. The result is already cached.

### Evaluation

Although secrets are resolved at the time of deployment, the secret reference may not evaluate immediately. It may have an impact on the deployment and when errors are logged. The following sections explain the different cases.

#### Secrets evaluated during API deployment

The following plugins evaluate EL after the secret is resolved as part of their deployment process:

* HTTP Proxy endpoint
* Resources

When the key is written in EL, those plugins can only access dictionaries and API properties. Here is an example:

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`redis`</mark>`',`<mark style="color:yellow;">`#dictionary['redis']['password-key']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved when the API is deployed, the API is not deployed. Errors are shown in the logs, and a caller receives a 404 error for HTTP APIs.
{% endhint %}

#### Secrets evaluated within API traffic

The following are plugins that evaluate EL strictly at runtime when the API is called:

* All message endpoints supporting secrets, on a new API call.
* Policies supporting EL, on initialization or on each call.

When the key is an EL, those plugins can access: dictionaries, API properties, attributes, content, request/subscribe data, and response/publish data. Here is an example:

`{#secrets.get('/`<mark style="color:red;">`kubernetes`</mark>`/`<mark style="color:green;">`apis-tokens`</mark>`',`<mark style="color:yellow;">`#request.headers['PartnerId']`</mark>`)}`

{% hint style="warning" %}
If the secret cannot be resolved and retry is activated, the API is deployed, but executing the policy or endpoint fails until retry resolves the secret.
{% endhint %}

## Secret renewal

If some secrets may change in the secret manager, renew their values regularly to avoid missing new values.

You can do this by using the following two query parameters:

*   `renewable=true`. This parameter enables automatic renewal of a secret. When added to a secret reference, it activates a renewal mechanism that checks the secret’s TTL, and then refreshes its value when necessary. Here is an example URI with this query parameter:

    `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`?`<mark style="color:orange;">`renewable=true`</mark>`')}`
* `reloadOnChange=true`. If this query parameter is set with the `renewable=true` parameter, the API is reloaded to use the new secret value. This ensures that the API operates with the most current value. Here is an example URI with this query parameter:\
  \
  `{#secrets.get('/`<mark style="color:red;">`provider`</mark>`/`<mark style="color:green;">`path`</mark>`:`<mark style="color:yellow;">`key`</mark>`?`<mark style="color:orange;">`renewable=true&reloadOnChange=true`</mark>`')}`

Secret TTL is global to all secrets that have the `renewable` option enabled. For more information about TTL renewal, see [configuration.md](configuration.md "mention") .

## Multi-environment secret references

### Configuration

The following extract from a `gravitee.yml` file defines two instances of HashiCorp Vault:

```yaml
api:
  secrets:
    providers:
      - id: dev
        plugin: vault
        configuration:
           enabled: true
           host: dev.vault.my.company.com
           ...
        environments: ["db0d7ed4-387f-43c9-91b8-f479c9d1956b"]
     - id: test
        plugin: vault
        configuration:
           enabled: true
           host: prod.vault.my.company.com
           ...
        environments: ["bb204730-9e07-45c1-8ca1-ad351d4391a1"]
```

You must use `id` . It creates an alias of the secret provider plugin. This lets you use the same plugin multiple times for a given Gateway without a naming collision. Also, it hides which secret manager is used. For example, API Publisher might not need to know the underlying technology.

### Aliased secret reference

The consequence of using `id` is that instead of using the plugin name in secret references, you use an alias. A secret reference looks like the following examples:

`{#secrets.get('/`<mark style="color:red;">`dev`</mark>`/`<mark style="color:green;">`secret/gravitee/passwords`</mark>`:`<mark style="color:yellow;">`redis`</mark>`')}`

or

`{#secrets.get('/`<mark style="color:red;">`test`</mark>`/`<mark style="color:green;">`secret/gravitee/passwords`</mark>`:`<mark style="color:yellow;">`redis`</mark>`')}`

### Cross-environment invariant using dictionaries

The following dictionary is for a development environment:

* The dictionary name is `api-secrets` and has the following properties:
  * Name: `redis-password` .
  * Value: `{#secrets.get('/`<mark style="color:red;">`dev`</mark>`/`<mark style="color:green;">`secret/gravitee/passwords`</mark>`:`<mark style="color:yellow;">`redis`</mark>`')}`

If you reproduce this in the production environment, but with the '`/`<mark style="color:red;">`test`</mark>`/...`' secret reference, you now have the following invariant `#dictionaries['api-secrets']['redis-password']` that exists in both environments.

You can create an API with the following secret reference. Redis is also managed with dictionaries:

```json
{
  "name": "My API v4",
  "gravitee": "4.0.0",
  "type": "proxy",
  // ...
  "resources":[{
      "enabled" : true,
      "configuration" : {
          "password" : "{#secrets.get(#dictionaries['api-secrets']['redis-password'])}",
          "standalone": {
              "host" : "{#dictionaries['redis']['host']}",
              "port" : 6379
          }
      }
  }]
}
```

When this API promoted from "dev" to "test" environment, it can resolve a secret without any change to its definition.

## Secret cache

### Resolved secrets stay secured

Credentials to access secret managers are set in the Gravitee configuration and only system admins can manipulate them. Also, these credentials can be hidden in secret managers. No user of any Gravitee UI can gain access to them.

Secrets are resolved in only the Gateway and not when the API is saved. No user of any Gravitee UI can see the value of a secret. When the Gateway stops or the API is undeployed, those secrets are no longer accessible. For more information about caching secrets, see [#consequence-of-caching-secrets](reference-secrets-in-apis.md#consequence-of-caching-secrets "mention").

Secrets are resolved and stored in a cache. Cached data stays off-heap, preventing admin users from dumping JVM memory using a Gravitee admin endpoint.

### Consequence of caching secrets

Secrets are resolved and cached when the API is deployed. The cache is accessed when the EL is evaluated. Here are the following consequences:

* The first API to use a given secret URI. For example, `/kubernetes/my-secret` resolves the secret and all key/values in it. Subsequent APIs that use a secret with the same URI does not trigger a new resolution. This means that if the value changes in the secret manager the new value is ignored. In that case, use [#secret-renewal](reference-secrets-in-apis.md#secret-renewal "mention") to overcome this situation.
* For a given secret URI, a secret reference that uses a key that is not present in the cache triggers a resolution of the secret, and only that key is added.
* Fields not supporting secrets fail evaluation although the secret is present in the cache. When an API is deployed and secrets are discovered, the Gateway does not know which field contains a secret. At runtime, when the EL is evaluated, the EL context contains information about the field, and then access to the secret can be denied.

## Gravitee Kubernetes Operator

API-level secrets apply to GKO v4 API CRDs seamlessly. Here is an example of what this looks like:

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "example API"
spec:
  name: "api-v4"
  version: "1.0"
  type: PROXY
  listeners:
    - type: HTTP
      paths:
        - path: "/echo-v4"
      entrypoints:
        - type: http-proxy
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          configuration:
            target: https://api.gravitee.io/echo
          sharedConfigurationOverride:
           headers:
             - name: "Authorization"
               value": "ApiKey {#secrets.get('/aws/gravitee/apikeys', 'echo')}"
```

## Examples

### Redis Cache example

Here is an extract of a provider configuration:

```yaml
api:
  secrets:
    providers:
      - plugin: vault
        configuration:
          enabled: true
          # ...
```

Here is an example of a secret in HashiCorp Vault:

```
vault kv put -mount=secret gravitee/passwords -redis="[redacted]" ...
```

If you want to secure the Redis password, you can configure the resource like the following example:

```json
{
    "name": "My API v4",
    "gravitee": "4.0.0",
    "type": "proxy",
    // ...
    "resources":[{
        "enabled" : true,
        "configuration" : {
            "password" : "{#secrets.get('/vault/secret/gravitee/passwords:redis')}",
            "standalone": {
                "host" : "{#dictionaries['redis']['host']}",
                "port" : 6379
            }
        }
    }]
}
```

The definition does not contain a clear text secret. This definition is saved, and then resolution occurs once it is deployed on APIM Gateway. When the API is started, the resource is initialized, and then the secret is evaluated and used to connect to Redis.

Here is an example of how to reference a secret when you configure a Redis Cache resource:

<figure><img src="../../../../4.7/.gitbook/assets/image%20(143).png" alt=""><figcaption></figcaption></figure>

### Native Kafka endpoint API example

Here is an extract of a provider configuration:

```yaml
api:
  secrets:
    providers:
      - plugin: kubernetes
        configuration:
           enabled: true
```

Here is a secret in Kubernetes:

```
kubectl create secret generic kafka-auth --from-literal\
    scram-username=[redacted]\
    scram-password=[redacted]
```

If you want to use this token to configure SCRAM authentication, you can use the following example:

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
              "username": "{#secrets.get('/kubernetes/kafka-auth:scram-username')}",
              "password": "{#secrets.get('/kubernetes/kafka-auth:scram-password')}"
            }
          }
        }
      }
    }
  ]
  // ...
}
```

The definition does not contain a clear text secret. This definition is saved as it is, and the resolution occurs once it is deployed on APIM Gateway. The `kafka-auth` secret is resolved once. When the API is actually called and the backend Kafka client is created, the secret is evaluated and used for authentication.

Here is an example of how to reference a secret during a SASL configuration:

<figure><img src="../../../../4.7/.gitbook/assets/Screenshot%202025-01-23%20at%2013.54.01.png" alt=""><figcaption></figcaption></figure>
