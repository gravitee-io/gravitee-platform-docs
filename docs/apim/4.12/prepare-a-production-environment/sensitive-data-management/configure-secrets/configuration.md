---
description: An overview about configuration.
metaLinks:
  alternates:
    - configuration.md
---

# Configuration

## Overview

This section explains how to configure secret managers to reference secrets in Gravitee.

Secrets manager integrations are handled by `secret-provider` plugins. These plugins allow you to access 3rd-party secret managers to resolve secrets.

{% hint style="info" %}
To learn more about Gravitee [Enterprise Edition](../../../introduction/enterprise-edition.md) and what's included in various enterprise packages:

* [Book a demo](https://documentation.gravitee.io/apim/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

### Known limitations

Current limitations are summarized below:

* Only the `http.ssl.keystore.secret` x.509 pairs, in either PEM or keystore format, can be watched, and therefore hot-reloaded.
* Only environment variables and `gravitee.yml` properties can be resolved into secrets. A secret URL can't be set using JVM properties. For example: `Dsystem.proxy.password=secret://kubernetes/giosecrets:proxypass` **can't be used**. JVM properties are passed directly to the platform without parsing, and are not detected by Gravitee as secrets to resolve.
* The `vault` plugin watches via polling because Vault Events is an enterprise feature.
* The `aws` plugin doesn't support watch. When used in a configuration, the secret is resolved once.

### Configuration for each secret manager <a href="#per-manager-configuration" id="per-manager-configuration"></a>

A `secret provider` plugin must be either bundled or added to the plugin directory.

You can enable a `secret-provider` plugin by configuring it in `gravitee.yml`. The configurations for each secret provider plugin are discussed in the following sections.

{% hint style="info" %}
The examples in this section show `gravitee.yml` syntax. For APIM Helm chart deployments, the same blocks must be nested under `api:` or `gateway:` in your `values.yaml` file, depending on which component reads the secret. See Helm chart specifics below for the equivalent Helm chart configuration.
{% endhint %}

### Kubernetes

The following example is a typical configuration for running Gravitee in Kubernetes. With this configuration, secrets are **resolved in the same namespace**.

{% code title="gravitee.yml" %}
```yaml
secrets:
  kubernetes:
    enabled: true
```
{% endcode %}

The following example shows how to add another namespace:

{% code title="gravitee.yml" %}
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
* GitHub
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

{% hint style="info" %}
The `secret://aws/<path>:<key>` URI syntax shown on this page applies to `gravitee.yml`, Helm `values.yaml`, and environment variables only. To reference an AWS Secrets Manager value from inside a v4 API definition, for example, in an endpoint's SSL or mTLS configuration, request headers, URL, or authentication credentials, use the `{#secrets.get('/aws/<path>:<key>')}` Gravitee Expression Language syntax instead. For details, see reference-secrets-in-apis.md.
{% endhint %}

### Azure Key Vault

The Azure Key Vault secret provider plugin enables integration with Azure Key Vault for secret management. The plugin supports multiple authentication providers to accommodate different deployment scenarios.

{% hint style="info" %}
The Azure Key Vault Secret Provider is a paid plugin available in Gravitee API Management and Access Management 4.11.x or later. Plugin version 1.0.0 or later is required.
{% endhint %}

#### Prerequisites

Before configuring the Azure Key Vault Secret Provider, ensure the following requirements are met:

* Azure Key Vault instance with secrets configured
* Azure AD tenant and appropriate credentials based on the selected authentication provider:
  * **Client Secret**: Azure AD app registration with client secret
  * **Certificate**: Azure AD app registration with client certificate in PEM format
  * **Managed Identity**: Azure VM, App Service, or AKS with system-assigned or user-assigned managed identity
  * **Workload Identity**: Kubernetes cluster with workload identity federation configured and federated token file mounted
  * **Environment**: `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` environment variables set on the Gravitee host

#### Global secret provider configuration

Configure the Azure Key Vault secret provider in `gravitee.yml` to make secrets available across all APIs and applications. The configuration requires the Key Vault URL and authentication provider details.

| Property | Description | Example |
|----------|-------------|---------|
| `secrets.azure-keyvault.enabled` | Enable or disable the plugin | `true` |
| `secrets.azure-keyvault.vaultUrl` | Azure Key Vault URL (required when enabled) | `https://my-vault.vault.azure.net` |
| `secrets.azure-keyvault.auth.provider` | Authentication provider | `CLIENT_SECRET`, `CERTIFICATE`, `DEFAULT_AZURE_CREDENTIAL`, `MANAGED_IDENTITY`, `ENVIRONMENT`, `WORKLOAD_IDENTITY` |
| `secrets.azure-keyvault.auth.tenantId` | Azure AD tenant ID (required for `CLIENT_SECRET` and `CERTIFICATE`; optional for `WORKLOAD_IDENTITY`) | `my-tenant-id` |
| `secrets.azure-keyvault.auth.clientId` | App registration client ID (required for `CLIENT_SECRET` and `CERTIFICATE`; user-assigned managed identity client ID for `MANAGED_IDENTITY` and `DEFAULT_AZURE_CREDENTIAL` when `auth.managedIdentityClientId` is unset; optional for `WORKLOAD_IDENTITY`) | `my-client-id` |
| `secrets.azure-keyvault.auth.clientSecret` | Client secret (required for `CLIENT_SECRET`) | `my-client-secret` |
| `secrets.azure-keyvault.auth.certificateFile` | Path to PEM certificate (required for `CERTIFICATE`) | `/path/to/cert.pem` |
| `secrets.azure-keyvault.auth.managedIdentityClientId` | User-assigned managed identity client ID | `mi-client-id` |
| `secrets.azure-keyvault.auth.managedIdentityResourceId` | User-assigned managed identity ARM resource ID (mutually exclusive with client ID and object ID at runtime) | `/subscriptions/.../resourceGroups/.../providers/Microsoft.ManagedIdentity/userAssignedIdentities/...` |
| `secrets.azure-keyvault.auth.managedIdentityObjectId` | User-assigned managed identity object ID (used when resource ID and client ID are unset) | `mi-object-id` |
| `secrets.azure-keyvault.auth.workloadIdentityTokenFile` | Federated token file path (defaults to `AZURE_FEDERATED_TOKEN_FILE` environment variable when unset) | `/var/run/secrets/azure/tokens/azure-identity-token` |
| `secrets.azure-keyvault.ssl.verify` | Verify TLS server certificates (set `false` only for local test doubles) | `true` |
| `secrets.azure-keyvault.ssl.pemFile` | PEM file with custom CA certificate(s) for TLS trust | `/path/to/ca-bundle.pem` |

**Example configuration (Client Secret):**

```yaml
secrets:
  azure-keyvault:
    enabled: true
    vaultUrl: https://my-vault.vault.azure.net
    auth:
      provider: CLIENT_SECRET
      tenantId: my-tenant-id
      clientId: my-client-id
      clientSecret: my-client-secret
```

**Example configuration (Managed Identity):**

```yaml
secrets:
  azure-keyvault:
    enabled: true
    vaultUrl: https://my-vault.vault.azure.net
    auth:
      provider: MANAGED_IDENTITY
      managedIdentityClientId: mi-client-id
```

#### API-level secret provider configuration

APIs can override the global secret provider configuration or define their own Azure Key Vault connection. API-level configuration follows the same property structure as global configuration.

```yaml
api:
  secrets:
    providers:
      - plugin: azure-keyvault
        configuration:
          enabled: true
          vaultUrl: https://api-specific-vault.vault.azure.net
          auth:
            provider: DEFAULT_AZURE_CREDENTIAL
            tenantId: my-tenant-id
            managedIdentityClientId: mi-client-id
```

#### Managed identity identifier selection

When using the **Managed Identity** provider, the Azure SDK accepts only one identifier: `auth.managedIdentityResourceId`, `auth.managedIdentityObjectId`, or `auth.managedIdentityClientId` / `auth.clientId` (in that priority order). Omit all identifiers to use the system-assigned managed identity. Specifying multiple identifiers will cause the SDK to use only the highest-priority value.

#### Environment variables for environment provider

The **Environment** provider reads credentials from the following environment variables on the Gravitee host:

| Variable | Purpose |
|----------|---------|
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_CLIENT_ID` | App registration client ID |
| `AZURE_CLIENT_SECRET` | Client secret |

The **Workload Identity** provider reads the federated token file path from `AZURE_FEDERATED_TOKEN_FILE` when `auth.workloadIdentityTokenFile` is not set.

#### SSL trust store behavior

When `ssl.pemFile` is set, the plugin builds a custom trust store from that file and does **not** merge it with the JVM default trust store. Include the full certificate chain needed to validate the Azure Key Vault endpoint or any intermediate proxies. When `ssl.verify` is `false`, the plugin trusts all certificates regardless of the `ssl.pemFile` setting. Use this only for local test environments.

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
