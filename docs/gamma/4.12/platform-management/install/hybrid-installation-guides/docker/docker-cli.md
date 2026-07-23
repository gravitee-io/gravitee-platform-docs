---
hidden: false
noIndex: false
---
# Run a hybrid Gamma Gateway with Docker CLI
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You run the Gravitee Gateway and Redis with Docker CLI commands, one container at a time, and the Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. Redis provides rate limiting at the edge, because the data-plane Gateway doesn't reach the control-plane datastore.

## Prerequisites

Before you start, complete the following steps:

* Install Docker. For more information, see [Install Docker Engine](https://docs.docker.com/engine/install/). You need access to [Docker Hub](https://hub.docker.com/) to pull the Gravitee images.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Run the Gateway

To run the Gateway, complete the following steps:

1. [#create-the-network](#create-the-network "mention")
2. [#run-redis](#run-redis "mention")
3. [#run-the-gateway](#run-the-gateway "mention")

### Create the network

* Create a Docker network so the Gateway can reach Redis by name:

  ```sh
  docker network create gravitee-network
  ```

### Run Redis

1. Run Redis on the network. Redis is the rate-limit store for the data plane:

   ```sh
   docker run -d \
     --name gio-gamma-hybrid-redis \
     --hostname redis \
     --network gravitee-network \
     -p 6379:6379 \
     redis:7.2-alpine redis-server --requirepass <redis-password>
   ```

   * Replace `<redis-password>` with your own secure password.

### Run the Gateway

1. Run the Gateway with Redis rate limiting enabled, and connect it to your Gravitee Cloud control plane:

   ```bash
   docker run -d \
     --name gio-gamma-hybrid-gateway \
     --hostname gamma-gateway \
     --network gravitee-network \
     -p 8082:8082 \
     -e gravitee_gamma_enabled=true \
     -e gravitee_ratelimit_type=redis \
     -e gravitee_ratelimit_redis_host=redis \
     -e gravitee_ratelimit_redis_port=6379 \
     -e gravitee_ratelimit_redis_password=<redis-password> \
     -e gravitee_ratelimit_redis_ssl=false \
     -e gravitee_cloud_token=<cloud-token> \
     -e gravitee_license_key=<license-key> \
     graviteeio/apim-gateway:4.12
   ```

   * Replace `<redis-password>` with the password you set for Redis.
   * Replace `<cloud-token>` with your Cloud Token from Gravitee Cloud.
   * Replace `<license-key>` with your License Key from Gravitee Cloud.

   {% hint style="info" %}
   The tag sets the Gateway version. We recommend running the same version as your Gamma control plane for compatibility. You can find your control plane version in the Gravitee Cloud dashboard.
   {% endhint %}

## Verification

To confirm that your hybrid installation works, complete the following checks:

1. [#check-the-container-status](#check-the-container-status "mention")
2. [#ensure-the-gateway-registers-in-gravitee-cloud](#ensure-the-gateway-registers-in-gravitee-cloud "mention")
3. [#ensure-the-gateway-is-listening-locally](#ensure-the-gateway-is-listening-locally "mention")

### Check the container status

* Check the container status using the following command:

  ```sh
  docker ps
  ```

  \
  The Gateway and Redis containers report an `Up` status:

  ```sh
  CONTAINER ID   IMAGE                                   COMMAND                  STATUS         PORTS                      NAMES
  50016b90785e   graviteeio/apim-gateway:4.12   "./bin/gravitee"    Up 2 minutes   0.0.0.0:8082->8082/tcp     gio-gamma-hybrid-gateway
  a8d3e6f1c2b4   redis:7.2-alpine                        "redis-server --requ..." Up 2 minutes   0.0.0.0:6379->6379/tcp     gio-gamma-hybrid-redis
  ```

### Ensure the Gateway registers in Gravitee Cloud

1. Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).
2. From the **Dashboard**, open the **Gateways** section. Your new hybrid Gateway appears here.

   
If the Gateway doesn't appear or shows an error state, complete the following checks:

* Ensure that your `gravitee_cloud_token` and `gravitee_license_key` values are valid.
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
  docker logs -f gio-gamma-hybrid-gateway
  ```

## Stop the Gateway

To shut down the Gateway, choose one of the following options.

* To stop the containers but keep them available to restart, use the following command:

  ```sh
  docker stop gio-gamma-hybrid-gateway gio-gamma-hybrid-redis
  ```

* To remove the containers and the network, use the following commands:

  ```sh
  docker rm -f gio-gamma-hybrid-gateway gio-gamma-hybrid-redis
  docker network rm gravitee-network
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
