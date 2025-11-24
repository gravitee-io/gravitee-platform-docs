---
description: Configuration guide for quick start.
---

# Quick Start

{% hint style="info" %}
This quick start uses configuration examples for HashiCorp Vault and Gravitee APIM Gateway. For other secret managers and use cases, refer to [configuration.md](configuration.md "mention")to view a complete reference.
{% endhint %}

## Prerequisites

* A Gravitee APIM instance in a local or development environment.
* Credentials for your secret manager.

## Configure and reference configuration-level secrets

To configure configuration-level secrets, complete the following steps:

1. [#configure-gravitee-to-access-a-secret-manager](quick-start.md#configure-gravitee-to-access-a-secret-manager "mention")
2. [#reference-secrets-in-the-configuration](quick-start.md#reference-secrets-in-the-configuration "mention")
3. [#restart-and-test](quick-start.md#restart-and-test "mention")

### Configure Gravitee to access a secret manager

After you configure your HashiCrorp Vault, you can configure your environment using a `gravitee.yml` file, the Helm chart, or environment variables.

#### Configure access to a secret manager with a `gravitee.yml` file

*   In your `gravitee.yml` file, add the following configuration:

    ```yaml
    secrets:
      vault:
        enabled: true
        host: 127.0.0.1      
        port: 8200
        ssl:
          enabled: false
        auth:
          method: token 
          config:
            token: root
    ```

#### Configure access to a secret manager with a Helm chart

*   In your Helm chart, add the following configuration:

    ```yaml
    gateway:
      secrets:
        vault:
          enabled: true
          ## other properties as listed above
    ```

#### Configure access to a secret manager with environment variables

*   In your `docker-compose.yml` file, add the following configuration:

    ```bash
    GRAVITEE_SECRETS_VAULT_ENABLED="true"
    GRAVITEE_SECRETS_VAULT_HOST="127.0.0.1"
    GRAVITEE_SECRETS_VAULT_PORT="8200"
    GRAVITEE_SECRETS_VAULT_SSL_ENABLED="true"
    GRAVITEE_SECRETS_VAULT_AUTH_METHOD="token"
    GRAVITEE_SECRETS_VAULT_AUTH_CONFIG_TOKEN="root"
    ```

{% hint style="info" %}
For more information about configuring access to your secret manager, see [configuration.md](configuration.md "mention").
{% endhint %}

### Reference secrets in the configuration

#### Example 1

The following example shows how to protect your database username and password.

* It uses a secret named `gravitee/mongo` .
* It uses a secret mount with two entries:
  * A `username` that has the value `admin`.
  * A `password` that has the value `password`.

```bash
vault kv put -mount=secret gravitee/mongo username=admin password=password
```

#### Example 2

The following example shows what your `gravitee.yml` contains before you use secrets:

```yaml
ds:
  mongodb:
    username: admin
    password: password
```

#### Example 3

The following example shows that with the `secret://` syntax, you can instruct Gravitee to resolve the secret from the configured secret manager:

```yaml
ds:
  mongodb:
    username: secret://vault/secret/gravitee/mongo:username
    password: secret://vault/secret/gravitee/mongo:password
```

### Restart and test

1. Restart your Gateway.
2. Check the logs and ensure that there are no errors.

## Next steps

* For more information about configurations for other secret managers and a complete list of available options, see [configuration.md](configuration.md "mention").
* For more information about the the `secret://` syntax, see [reference-secrets-in-configurations.md](reference-secrets-in-configurations.md "mention").
