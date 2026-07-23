---
hidden: false
noIndex: false
---
# Run a hybrid Gamma Gateway with Docker Compose
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You run the Gravitee Gateway and Redis with Docker Compose, and the Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. Redis provides rate limiting at the edge, because the data-plane Gateway doesn't reach the control-plane datastore.

By the end of this guide, your Gateway is registered with Gravitee Cloud and ready to serve the APIs, Kafka services, and MCP servers you design in the Gamma console.

## Prerequisites

Before you start, complete the following steps:

* Install Docker. For more information, see [Install Docker Engine](https://docs.docker.com/engine/install/). You need access to [Docker Hub](https://hub.docker.com/) to pull the Gravitee images.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Run the Gateway

To run the Gateway, complete the following steps:

1. [#create-the-compose-file](#create-the-compose-file "mention")
2. [#create-the-env-file](#create-the-env-file "mention")
3. [#start-the-gateway](#start-the-gateway "mention")

### Create the compose file

1. Create a file named `docker-compose-gamma-hybrid.yml`, and then copy the following configuration into it. Redis is used for rate limiting.

   ```yaml
   volumes:
     data-redis:

   services:
     gio-gamma-hybrid-gateway:
       image: graviteeio/apim-gateway:${GATEWAY_VERSION:-4.12}
       container_name: gio_gamma_hybrid_gateway
       hostname: gamma-gateway
       ports:
         - "8082:8082"
       depends_on:
         gio-gamma-hybrid-redis:
           condition: service_healthy
       environment:
         # Turn on Gamma in the Gateway (required for AuthZ policy/PDP sync)
         - gravitee_gamma_enabled=true
         # Rate limit store - Redis
         - gravitee_ratelimit_type=redis
         - gravitee_ratelimit_redis_host=redis
         - gravitee_ratelimit_redis_port=6379
         - gravitee_ratelimit_redis_password=${REDIS_PASSWORD}
         # Gravitee Cloud control plane
         - gravitee_cloud_token=${CLOUD_TOKEN}
         - gravitee_license_key=${LICENSE_KEY}
       restart: unless-stopped

     gio-gamma-hybrid-redis:
       image: redis:${REDIS_VERSION:-7.2-alpine}
       container_name: gio_gamma_hybrid_redis
       hostname: redis
       restart: always
       ports:
         - "6379:6379"
       command: redis-server --requirepass ${REDIS_PASSWORD}
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 1s
         timeout: 3s
         retries: 30
       volumes:
         - data-redis:/data
   ```

2. Save the `docker-compose-gamma-hybrid.yml` file.

### Create the env file

1. Place the following `.env` file in the same directory as `docker-compose-gamma-hybrid.yml` to centralize the configuration values:

   ```bash
   # We recommend running the same Gateway version as your Gamma control plane, shown in Gravitee Cloud.
   GATEWAY_VERSION=4.12

   # Use a Redis version that is supported by Gravitee.
   REDIS_VERSION=7.2-alpine

   # Change this default password before running in any non-local environment.
   REDIS_PASSWORD=<my-default-redis-password>

   # Replace with your actual values from Gravitee Cloud.
   CLOUD_TOKEN=<cloud-token>
   LICENSE_KEY=<license-key>
   ```

   * Replace `<my-default-redis-password>` with your Redis password.
   * Replace `<cloud-token>` with your Cloud Token.
   * Replace `<license-key>` with your License Key.

2. Save the `.env` file.

<details>

<summary>Explanations of key settings</summary>

**Gravitee Cloud connection**

`gravitee_cloud_token` registers the Gateway with your Gravitee Cloud control plane, and `gravitee_license_key` activates the Gateway. The Gateway pulls its API definitions from the control plane, so you don't run the Management API, the consoles, or a database locally.

**Gateway version**

`GATEWAY_VERSION` sets the Gateway image. We recommend running the same version as your Gamma control plane for compatibility. You can find your control plane version in the Gravitee Cloud dashboard.

**Redis**

Redis is the rate-limit store for the data plane. The self-hosted Gateway doesn't reach the control-plane datastore, so it keeps rate-limit counters in a local Redis.

</details>

### Start the Gateway

1. From the directory that contains `docker-compose-gamma-hybrid.yml` and the `.env` file, start the Gateway using the following command. This command uses the values from `.env` to launch the Gateway and Redis in detached mode.

   ```sh
   docker compose -f docker-compose-gamma-hybrid.yml up -d
   ```

## Verification

To confirm that your hybrid installation works, complete the following checks:

1. [#ensure-the-gateway-registers-in-gravitee-cloud](#ensure-the-gateway-registers-in-gravitee-cloud "mention")
2. [#ensure-the-gateway-is-listening-locally](#ensure-the-gateway-is-listening-locally "mention")

### Ensure the Gateway registers in Gravitee Cloud

1. Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).
2. From the **Dashboard**, open the **Gateways** section. Your new hybrid Gateway appears here.

   
If the Gateway doesn't appear or shows an error state, complete the following checks:

* Ensure that your `.env` file includes a valid `CLOUD_TOKEN` and a valid `LICENSE_KEY`.
* Ensure that the Gateway container has Internet access to reach Gravitee Cloud.

### Ensure the Gateway is listening locally

1. Open a terminal, and then run the following `curl` command to call the Gateway on its default exposed port:

   ```bash
   curl -i http://localhost:8082/
   ```

2. Verify that the command output is similar to the following response:

   ```http
   HTTP/1.1 404 Not Found
   Content-Length: 40
   Content-Type: text/plain

   No context-path matches the request URI.
   ```

   {% hint style="info" %}
   This response confirms that the Gateway has initialized, but no APIs are deployed yet. Once you publish APIs through the Gamma control plane, this message is replaced by valid responses routed through the configured context paths.
   {% endhint %}

## View the logs

* To check the Gateway logs, use the following command:

  ```sh
  docker logs -f gio_gamma_hybrid_gateway
  ```

## Stop the Gateway

To shut down the Gateway, choose one of the following options.

* To stop and remove the containers but preserve the Redis volume (`data-redis`), use the following command:

  ```sh
  docker compose -f docker-compose-gamma-hybrid.yml down
  ```

* To stop the containers and remove both the containers and the Redis volume (`data-redis`), use the following command:

  ```sh
  docker compose -f docker-compose-gamma-hybrid.yml down -v
  ```

## Proxy configuration

To route Gateway traffic through a corporate proxy (for example, for backend API calls or JWKS retrieval from external identity providers like Microsoft Entra ID), add the following `gravitee_system_proxy_*` environment variables to the Gateway container:

```
gravitee_system_proxy_enabled=true
gravitee_system_proxy_type=HTTP
gravitee_system_proxy_host=<proxy-host>
gravitee_system_proxy_port=<proxy-port>
gravitee_system_proxy_https_host=<proxy-host>
gravitee_system_proxy_https_port=<proxy-port>
```

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../../agent-management/get-started/create-your-first-mcp-server.md).
* Create your first API. For more information, see [Create your first API](../../../../api-management/get-started/create-your-first-api.md).
