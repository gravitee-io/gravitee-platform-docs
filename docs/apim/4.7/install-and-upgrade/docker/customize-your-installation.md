---
description: This page explains how to customize your Gravitee API Management on Docker
---

# Customize your Installation

## Install additional plugins

* To add an additional plugin, copy the plugin archive that is contained in a `.zip` folder into the `plugins-ext` folder.

{% hint style="info" %}
- For the API Gateway, `the plugin-ext` folder is located at `/gravitee/apim-gateway/plugins`.
- For the Management API, the `plugin-ext` is located at `/gravitee/apim-management-api/plugins.`
{% endhint %}

You can download additional plugins from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/).

For more information about plugin deployment, see [Deployment](../../getting-started/plugins/deployment.md#deployment).

{% hint style="warning" %}
Some plugins need to be installed on both the API Gateway and the Management API. Installation details are provided in a specific plugin’s documentation.
{% endhint %}

## Use Redis as the datastore for rate-limiting counters

{% tabs %}
{% tab title="Use Redis with docker-compose" %}
To use Redis with `docker compose`, complete the following steps:

1. In the `$services.gateway.environment` section of the Docker compose file, add the following lines of code:

```yaml
      - gravitee_ratelimit_type=redis
      - gravitee_ratelimit_redis_host=gravitee-redis
      - gravitee_ratelimit_redis_port=6379
```

2. Remove the line that contains the following code: `gravitee_ratelimit_mongodb_uri`.

{% hint style="info" %}
Your Redis host and port may be different
{% endhint %}
{% endtab %}

{% tab title="Use Redis with Docker images" %}
To use Redis with Docker images, complete the following steps:

1. In the command that you use to start the API Gateway, add the following environment variables:

```bash
  --env gravitee_ratelimit_type=redis \
  --env gravitee_ratelimit_redis_host=gravitee-redis \
  --env gravitee_ratelimit_redis_port=6379 \
```

2. Remove the following line of code: `gravitee_ratelimit_mongodb_uri` `env`

{% hint style="info" %}
Your Redis host and port may be different.
{% endhint %}
{% endtab %}
{% endtabs %}

## Use the JDBC connection as the datastore for management

### Prerequisites

* The correct JDBC driver must be installed on the API Gateway and the Management API.
* The containers must be started using additional environment variables.

### 1. Download the driver

To download the driver, complete the following sub-steps:

1. Download the correct driver for your database. For more information about downloading the correct drive, go to [Supported databases.](../../configure-apim/repositories/README.md#supported-databases)
2. Place the driver in the `plugins-ext` folder.

{% hint style="info" %}
* For the API Gateway, the `plugin-ext` folder is located at `/gravitee/apim-gateway/plugins`.
* For the Management API, the `plugin-ext`folder is located at the `/gravitee/apim-management-api/plugins`.
{% endhint %}

### 2. Use JDBC

To use the JDBC driver, complete the following sub-steps based on if you installed Gravitee APIM using docker-compose or if you installed Gravitee APIM using Docker images.

{% tabs %}
{% tab title="Use JDBC with docker-compose" %}
To use JDBC with `docker compose`, complete the following steps:

1. In the `$services.gateway.environment` section, add the following lines of code:

```yaml
 - gravitee_management_type=jdbc
 - gravitee_management_jdbc_url=jdbc:mysql://gravitee-mysql:3306/gravitee?useSSL=false&user=mysql_users&password=mysql_password
```

2. Remove the following line of code: `gravitee_management_mongodb_uri.`

{% hint style="danger" %}
* Ensure that your `gravitee_management_jdbc_url` is appropriate for your environment.
* Use `useSSL=false` with caution in production.
* Your host, port, username, and password may be different.
{% endhint %}
{% endtab %}

{% tab title="Use JDBC with Docker images" %}
To use JDBC with Docker images, complete the following steps:

1. In the command that you use to start the Gateway, add the following environment variables:

```bash
--env gravitee_management_type=jdbc \
  --env gravitee_management_jdbc_url=jdbc:mysql://gravitee-mysql:3306/gravitee?useSSL=false&user=mysql_users&password=mysql_password \
```

2. Remove the `gravitee_management_mongodb_uri` `env`.

{% hint style="danger" %}
* Ensure that your`gravitee_management_jdbc_url` is appropriate for your environment.
* Use caution`useSSL=false`if you use in production.
* Your host, port, username, and password may be different.
{% endhint %}
{% endtab %}
{% endtabs %}
