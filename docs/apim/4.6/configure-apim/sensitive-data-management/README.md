---
description: >-
  Gravitee provides several options to protect sensitive information. This page
  lists them and provide guidance for when to apply them.
---

# Sensitive Data Management

## Secret managers integration

Gravitee offers integrations with various secret managers. If you are storing sensitive data into 3rd-party software, such as usernames, passwords, tokens, keys, and certificates, Gravitee allows you to use those secrets.&#x20;

We provide the follow integrations:&#x20;

* Kubernetes&#x20;
* HashiCorp Vault ([Enterprise Edition](../../overview/enterprise-edition.md))
* AWS Secrets Manager ([Enterprise Edition](../../overview/enterprise-edition.md))

For more information about secret manager integrations, see the [Integrations](../../getting-started/integrations.md).

When you use secret managers, you use Gravitee's `secret-provider` plugins to configure access, and then you can reference the secrets in different locations.&#x20;

See the [secret provider plugins configuration](secret-provider-plugins-configuration.md) for more information.

### Referencing a secret at the configuration level

{% hint style="info" %}
If you use the Community Edition of Gravitee, this feature is available with only the Kubernetes secret provider.
{% endhint %}

You can set up Gravitee with secret managers and fetch secrets for Gravitee product configurations. This allows you to protect database passwords, tokens, encryption keys, and TLS such as PEM or KeyStore with renewal, depending on the plugin.

Configuration-level secrets are compatible with all Gravitee products:&#x20;

* APIM&#x20;
  * Management API
  * Gateway
* Access Management
  * Management API
  * Gateway

For more information, see [Configuration-Level Secrets](configuration-level-secrets.md).

### Referencing a secret at the API level (v4 APIs only)

You can configure Gravitee to get secrets from a secret manager, and then use secrets in a v4 API. Secrets obscure sensitive information in v4 API definitions for endpoint authentication and TLS, resources requiring passwords, sensitive headers values, and URLs that may contain sensitive data. Secrets also ensure that sensitive data is not stored in the Gravitee database. All plugins compatible with [Gravitee Expression Language](../../getting-started/gravitee-expression-language.md) can use secrets.

See [API-Level Secrets](../../configure-v4-apis/api-level-secrets.md) for more information.

## API encrypted properties&#x20;

If you wish to protect sensitive information, you can encrypt [API properties](../../policies/v4-api-policy-studio.md#api-properties). Both v2 and v4 APIs allow you to encrypt data in the database. This data is automatically decrypted when used by the Gateway.&#x20;

{% hint style="info" %}
Although the data is encrypted, secret managers are better suited to store secrets. However, they remain a viable and secure option for many use cases.
{% endhint %}

## GKO templating

If you are a GKO user, you can use CRD templating. This allows you to include secrets within your CRDs. Although it is included in the Community Edition, there are two limitations with this approach:

* Secrets included in the API definition are stored in ConfigMaps or the database, depending on your GKO setup
* This is limited to Kubernetes Secrets

{% embed url="https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/templating" %}

## GKO and API-level secrets

API-level secrets apply to GKO v4 API CRDs seamlessly, removing the two pain points mentioned above. Here is an example of what this looks like:

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
