# Docker CLI

## Overview

This guide explains how to install the Data Plane using Docker CLI commands. The Data Plane includes core components like the Gateway and Redis for rate limiting.

{% include "../../../../4.6/.gitbook/includes/installation-guide-note (1).md" %}

## Prerequisites

* Install [Docker](https://docs.docker.com/engine/install/).
* Ensure you have access to [Gravitee Cloud](https://cloud.gravitee.io/), with permissions to install new Gateways.
* Complete the steps in [#prepare-your-installation](../#prepare-your-installation "mention").

## Install Gateway and Configure Redis

To enable API rate-limiting, configure your Gateway to use a rate-limiting repository, such as Redis with the following steps:

1.  Create a Docker network with the following command:

    ```sh
    docker network create gravitee-network
    ```
2.  Run the command below to start Redis. 

    ```sh
    docker run -d \
      --name gio-apim-hybrid-redis \
      --hostname redis \
      --network gravitee-network \
      -p 6379:6379 \
      redis:7.2-alpine redis-server --requirepass <redis_password>
    ```

    * Replace `<redis_password>` with your own secure password.
3.  Run the Gateway with Redis rate limiting enabled with the following command:

    ```bash
    docker run -d \
      --name gio-apim-hybrid-gateway \
      --hostname apim-gateway \
      --network gravitee-network \
      -p 8082:8082 \
      -e gravitee_ratelimit_type=redis \
      -e gravitee_ratelimit_redis_host=redis \
      -e gravitee_ratelimit_redis_port=6379 \
      -e gravitee_ratelimit_redis_password=<redis_password> \
      -e gravitee_ratelimit_redis_ssl=false \
      -e gravitee_cloud_token=<cloud_token> \
      -e gravitee_license_key=<license_key> \
      graviteeio/apim-gateway:<CONTROL_PLANE_VERSION>
    ```

    * Replace `<cloud_token>` with your Cloud Token from Gravitee Cloud.
    * Replace `<license_key>` with your License Key from Gravitee Cloud.
    * Set `redis_password` environment variable: `export redis_password=your_redis_password` or replace `${redis_password}` with your actual Redis password.
    *   Replace `<CONTROL_PLANE_VERSION>` with the version that matches your Gravitee Cloud Control Plane. For example. 4.8.2.

        <figure><img src="../../../.gitbook/assets/image (324) (1).png" alt=""><figcaption></figcaption></figure>

## Verification

To confirm that your Hybrid installation is working, complete the following steps:

* [#check-container-status](docker-cli.md#check-container-status "mention")
* [#check-port-mapping](docker-cli.md#check-port-mapping "mention")
* [#ensure-the-gateway-is-listening-in-your-local-environment](docker-cli.md#ensure-the-gateway-is-listening-in-your-local-environment "mention")
* [#verify-the-redis-connection](docker-cli.md#verify-the-redis-connection "mention")
* [#view-the-logs](docker-cli.md#view-the-logs "mention")
* [#stop-the-gateway](docker-cli.md#stop-the-gateway "mention")

### Check container status

*   Check the container status using the following command:

    ```sh
    docker ps
    ```

    \
    The command generates the following output. 

    ```sh
    CONTAINER ID   IMAGE                         COMMAND                  CREATED             STATUS             PORTS                    NAMES
    50016b90785e   graviteeio/apim-gateway:4.8.2   "./bin/gravitee"         About an hour ago   Up About an hour   0.0.0.0:8082->8082/tcp   gio-apim-hybrid-gateway
    a8d3e6f1c2b4   redis:7.2-alpine              "redis-server --requ..." About an hour ago   Up About an hour   0.0.0.0:6379->6379/tcp   gio-apim-hybrid-redis
    ```

### Check port mapping

*   To verify the container's port is correctly mapped run the following command:

    ```sh
    docker port gio-apim-hybrid-gateway
    ```

    \
    The command generates the following output:

    ```sh
    8082/tcp -> 0.0.0.0:8082
    ```

### **Ensure the Gateway is listening in your local environment**

1.  Open a terminal, and then run the following `curl` command to call the Gateway on its default exposed port:

    ```bash
    curl -i http://localhost:8082/
    ```

The command generates the following output:

```http
HTTP/1.1 404 Not Found
Content-Length: 40
Content-Type: text/plain

No context-path matches the request URI.
```

{% hint style="info" %}
This response confirms that the Gateway has initialized, but no APIs have been deployed. Once APIs are published through the Control Plane, this message is replaced by valid responses routed through the configured context paths.
{% endhint %}

### Verify the Redis Connection

*   Test the Redis connection with the following command:

    ```bash
    docker exec -it gio-apim-hybrid-redis redis-cli -a <redis_password> ping
    ```

    \
    The command generates the following output:

    ```bash
    PONG
    ```

### View the logs

*   To check the Gateway logs, use the following command:

    ```sh
    docker logs -f gio-apim-hybrid-gateway
    ```

    \
    The command generates the following output: 

    ```bash
    [gio-apim-hybrid-gateway] INFO  i.g.p.c.internal.PluginRegistryImpl - Loading plugins from /opt/graviteeio-gateway/plugins
    [gio-apim-hybrid-gateway] INFO  i.g.p.c.internal.PluginRegistryImpl - List of available policy: 
    [gio-apim-hybrid-gateway] INFO  i.g.p.c.internal.PluginRegistryImpl -         > rate-limit [3.0.0] has been loaded
    [gio-apim-hybrid-gateway] INFO  i.g.p.c.internal.PluginRegistryImpl -         > jwt [6.1.2] has been loaded
    [gio-apim-hybrid-gateway] INFO  i.g.p.c.internal.PluginRegistryImpl -         > key-less [4.0.0] has been loaded
    [gio-apim-hybrid-gateway] INFO  i.g.p.r.i.RepositoryPluginHandler - Repository [RATE_LIMIT] loaded by redis
    [gio-apim-hybrid-gateway] INFO  i.g.r.redis.vertx.RedisClient - Redis is now ready to be used.
    [gio-apim-hybrid-gateway] INFO  i.g.node.container.AbstractContainer - Starting Gravitee.io - API Gateway...
    [gio-apim-hybrid-gateway] INFO  i.g.g.r.s.vertx.HttpProtocolVerticle - HTTP server [http] ready to accept requests on port 8082
    [gio-apim-hybrid-gateway] INFO  i.g.node.container.AbstractNode - Gravitee.io - API Gateway id[05dbfca1-3102-4cbb-9bfc-a13102acbbdd] version[4.8.2] started in 866 ms.
    [gio-apim-hybrid-gateway] INFO  i.g.g.s.s.p.r.s.n.NodeMetadataSynchronizer - Node metadata synchronized in 285ms
    [gio-apim-hybrid-gateway] INFO  i.g.g.s.s.p.r.s.l.LicenseSynchronizer - 1 licenses synchronized in 46ms
    [gio-apim-hybrid-gateway] INFO  i.g.g.s.s.p.r.s.api.ApiSynchronizer - 0 apis synchronized in 26ms
    [gio-apim-hybrid-gateway] INFO  i.g.g.s.s.p.r.DefaultSyncManager - Sync service has been scheduled with delay [10000 MILLISECONDS]
    ```
*   To check the Redis logs, use the following command:

    ```bash
    docker logs -f gio-apim-hybrid-redis
    ```

    \
    The command generates the following output:

    ```bash
    1:C 19 Aug 2025 10:30:15.123 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
    1:C 19 Aug 2025 10:30:15.123 # Redis version=7.2.4, bits=64, commit=00000000, modified=0, pid=1, just started
    1:C 19 Aug 2025 10:30:15.123 # Configuration loaded
    1:M 19 Aug 2025 10:30:15.124 * monotonic clock: POSIX clock_gettime
    1:M 19 Aug 2025 10:30:15.124 * Running mode=standalone, port=6379.
    1:M 19 Aug 2025 10:30:15.124 * Server initialized
    1:M 19 Aug 2025 10:30:15.125 * Ready to accept connections tcp
    ```

### (Optional) Stop the Gateway

To shut down the Gateway, choose one of the following options.

*   This command stops the containers but keeps them available to restart. The Redis data is preserved.

    ```sh
    docker stop gio-apim-hybrid-gateway gio-apim-hybrid-redis
    ```
*   These commands remove the containers, their data, and the network, and all Redis data is lost.

    ```sh
    docker stop gio-apim-hybrid-gateway gio-apim-hybrid-redis
    docker rm gio-apim-hybrid-gateway gio-apim-hybrid-redis
    # Remove the network
    docker network rm gravitee-network
    ```

## Next steps

* Access your API Management Console. To access your Console, complete the following steps:
  1. Log in to your [Gravitee Cloud](https://cloud.gravitee.io/).
  2. From the Dashboard, navigate to the Environment where you created your Gateway.
  3. Click on **APIM Console** to open the user interface where you can create and manage your APIs.
* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](../../../how-to-guides/create-and-publish-your-first-api/ "mention").
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [configure-the-kafka-client-and-gateway.md](../../../kafka-gateway/configure-the-kafka-client-and-gateway.md "mention").
