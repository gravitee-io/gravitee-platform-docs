# Environment Properties

## Overview

Gravitee's configuration is controlled via the `gravitee.yml` file located in the `/config` directory of every component. The configuration for the gateway and the management API are different. This page documents what the environment properties of each component are.

## Using Environment Variables in Different Installation Methods

{% tabs %}
{% tab title="Linux Server" %}
If you are installing Gravitee APIM on a regular Linux server, the gateway will use environment variables accessible to the JVM to override the configuration in `gravitee.yml`. You name the variables in **uppercase**, with an **underscore** to represent the position in the hierarchy in the `gravitee.yml` file, prefixed with `GRAVITEE`.&#x20;

For example, the variable in `gravitee.yml` referred to as:

```yaml
system:
  proxy:
    enabled: true
```

This can be referred to in your shell by setting:

```sh
export GRAVITEE_SYSTEM_PROXY_ENABLED=true
```
{% endtab %}

{% tab title="Docker" %}
If you are installing Gravitee APIM in Docker, you can reference environment variables in the `environment` section of your `Dockerfile` or `docker-compose.yml`. You name the variables with an **underscore** to represent the position in the hierarchy in the `gravitee.yml` file, prefixed with `gravitee`.

For example, the variable in `gravitee.yml` referred to as:

```yaml
system:
  proxy:
    enabled: true
```

This can be referred to in the `Dockerfile` for the gateway by adding the environment variable:

```properties
gravitee_system_proxy_enabled=true
```
{% endtab %}
{% endtabs %}

## Gateway Properties

The properties are listed in the order they appear in the YAML file. The dots in each name represents the level of the property in the YAML configuration.

<table><thead><tr><th width="320">Property</th><th>Use</th></tr></thead><tbody><tr><td>secrets.loadFirst</td><td>Determines the order to load secrets from providers if there is more than one provider in use.</td></tr><tr><td>secrets.kubernetes.enabled</td><td>Determines whether the Kubernetes provider is enabled.</td></tr><tr><td>secrets.kubernetes.namespace</td><td>Namespace where the secrets reside in Kubernetes. When enabled, default is <code>default</code>.</td></tr><tr><td>secrets.kubernetes.kubeConfigFile</td><td>Path to the configuration for the plugin. When enabled, default is <code>/opt/gravitee/conpfig/kube-config.json</code>.</td></tr><tr><td>secrets.kubernetes.timeoutMs</td><td>Timeout for the Kubernetes client in milliseconds.</td></tr><tr><td>secrets.vault.enabled</td><td>Determines whether the Vault provider is enabled.</td></tr><tr><td>secrets.vault.host</td><td>Host IP address for the Vault instance. When enabled, default is <code>127.0.0.1</code>.</td></tr><tr><td>... <em>(many more to add before going live)</em></td><td></td></tr></tbody></table>

## Management API Properties
