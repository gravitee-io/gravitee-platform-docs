# Docker CLI

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to run a self-hosted Gravitee Gamma platform with the Docker CLI, one container at a time.

You run the standard APIM containers, turn on Gamma in the Management API with `gravitee_gamma_enabled=true`, and add the Gamma console (`graviteeio/gamma-ui`). The Gamma console isn't a separate backend. It talks to the Management API, which runs with Gamma enabled.

Every component is published on `localhost` on its own port. On a single host, `localhost:8084`, `localhost:8086`, and `localhost:8083` are the **same site**, so the login session cookie is sent across ports and the consoles log in. For the detail, see [Why this works on one host](docker-cli.md#why-this-works-on-one-host).

This guide uses the `4.12.0` images, which include the Agent Management module. For more information, see [Add your license key](docker-cli.md#enterprise-edition-only-add-your-license-key).

## Prerequisites

Before you start, complete the following steps:

* Install Docker. For more information, see [Install Docker Engine](https://docs.docker.com/engine/install/).
* **(Enterprise Edition only)** To enable Agent Management, you need an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. For more information, see [Add your license key](docker-cli.md#enterprise-edition-only-add-your-license-key).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Run Gamma

To run Gamma, complete the following steps:

1. [#create-the-networks](docker-cli.md#create-the-networks "mention")
2. [#run-mongodb-and-elasticsearch](docker-cli.md#run-mongodb-and-elasticsearch "mention")
3. [#enterprise-edition-only-add-your-license-key](docker-cli.md#enterprise-edition-only-add-your-license-key "mention")
4. [#run-the-management-api-and-gateway](docker-cli.md#run-the-management-api-and-gateway "mention")
5. [#run-the-consoles](docker-cli.md#run-the-consoles "mention")

### Create the networks

Create two Docker bridge networks. The datastores stay on `storage`, and the backends join both networks:

```bash
docker network create storage
docker network create frontend
```

### Run MongoDB and Elasticsearch

1.  Run MongoDB on the `storage` network:

    ```bash
    docker run --detach --name gamma-mongodb \
      --net storage \
      mongo:7.0
    ```
2.  Run Elasticsearch on the `storage` network:

    ```bash
    docker run --detach --name gamma-elasticsearch \
      --net storage \
      --env discovery.type=single-node \
      --env xpack.security.enabled=false \
      --env "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
      docker.elastic.co/elasticsearch/elasticsearch:8.17.2
    ```

### (Enterprise Edition only) Add your license key

Agent Management is an enterprise feature. It only activates with an enterprise license that includes the `agent-management` pack. Without a license, the module loads but stays inactive and doesn't appear in the console. The other modules (API Management, Authorization Management, and Platform Management) work without a license.

To get a license, contact your Technical Account Manager. Your account manager sends you the license as a `license.key` file.

{% hint style="info" %}
If your license is a base64-encoded text file (for example, `license.base64.txt`), decode it into `license.key` first:

```bash
base64 -d < license.base64.txt > license.key
```

On macOS, use `base64 -D` (capital `D`) if `base64 -d` returns an error.
{% endhint %}

1. Place the `license.key` file in the directory where you run the `docker run` commands.
2. In the [Run the Management API and Gateway](docker-cli.md#run-the-management-api-and-gateway) step, keep the `--volume` line that mounts `license.key`. For the community edition, remove that line.

### Run the Management API and Gateway

1.  Run the Management API with Gamma enabled. **(Enterprise Edition only)** keep the `--volume "$(pwd)/license.key:..."` line. For the community edition, remove it:

    ```bash
    docker run --detach --name gamma-management-api \
      --net storage \
      --publish 8083:8083 \
      --volume "$(pwd)/license.key:/opt/graviteeio-management-api/license/license.key:ro" \
      --env gravitee_gamma_enabled=true \
      --env gravitee_management_mongodb_uri="mongodb://gamma-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://gamma-elasticsearch:9200" \
      --env gravitee_installation_standalone_console_url="http://localhost:8084" \
      --env gravitee_installation_standalone_portal_url="http://localhost:8085" \
      --env gravitee_http_cors_enabled=true \
      --env gravitee_http_cors_allow-origin_0="http://localhost:8084" \
      --env gravitee_http_cors_allow-origin_1="http://localhost:8085" \
      --env gravitee_http_cors_allow-origin_2="http://localhost:8086" \
      --env gravitee_http_cors_allow-headers="Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie" \
      --env gravitee_http_cors_allow-methods="GET,POST,PUT,DELETE,OPTIONS" \
      --env gravitee_http_cors_exposed-headers="X-Total-Count,Set-Cookie" \
      --env gravitee_http_cors_allow-credentials=true \
      --env gravitee_http_cookie_sameSite=Lax \
      --env gravitee_http_cookie_secure=false \
      graviteeio/apim-management-api:4.12.0

    docker network connect frontend gamma-management-api
    ```
2.  Run the Gateway:

    ```bash
    docker run --detach --name gamma-gateway \
      --net storage \
      --publish 8082:8082 \
      --env gravitee_management_mongodb_uri="mongodb://gamma-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_ratelimit_mongodb_uri="mongodb://gamma-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_reporters_elasticsearch_endpoints_0="http://gamma-elasticsearch:9200" \
      graviteeio/apim-gateway:4.12.0

    docker network connect frontend gamma-gateway
    ```

{% hint style="info" %}
The Management API takes a few minutes to initialize. Confirm it's ready with `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8083/management/v2/ui/bootstrap` (returns `200`).
{% endhint %}

### Run the consoles

1.  Run the APIM Console:

    ```bash
    docker run --detach --name gamma-apim-console \
      --net frontend \
      --publish 8084:8080 \
      --env MGMT_API_URL="http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/" \
      graviteeio/apim-management-ui:4.12.0
    ```
2.  Run the Developer Portal:

    ```bash
    docker run --detach --name gamma-developer-portal \
      --net frontend \
      --publish 8085:8080 \
      --env PORTAL_API_URL="http://localhost:8083/portal/environments/DEFAULT" \
      graviteeio/apim-portal-ui:4.12.0
    ```
3.  Run the Gamma console:

    ```bash
    docker run --detach --name gamma-console \
      --net frontend \
      --publish 8086:8080 \
      --env GAMMA_API_URL="http://localhost:8083/gamma" \
      --env GAMMA_CONSOLE_BASE_HREF=/ \
      --env HTTP_PORT=8080 \
      --env SERVER_NAME=localhost \
      graviteeio/gamma-ui:4.12.0
    ```

## Access the consoles

Open the consoles in your browser. The default username and password for the Gamma console, the APIM Console, and the Developer Portal are both `admin`.

| Component        | URL                     | Default credentials |
| ---------------- | ----------------------- | ------------------- |
| Gamma console    | `http://localhost:8086` | `admin` / `admin`   |
| APIM Console     | `http://localhost:8084` | `admin` / `admin`   |
| Developer Portal | `http://localhost:8085` | `admin` / `admin`   |
| API Gateway      | `http://localhost:8082` | Not applicable      |

## Verification

*   Confirm the Management API is ready and the Gamma console signs in:

    ```bash
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8083/management/v2/ui/bootstrap
    ```

    \
    The command returns `200` once the platform is up. You can then sign in to the Gamma console at `http://localhost:8086` with `admin` / `admin`.

## Why this works on one host

The cross-origin cookie problem that breaks Gamma login on separate hostnames doesn't apply here. For cookies, a "site" is the registrable domain, and the port is ignored. So `localhost:8086` (the Gamma console) and `localhost:8083` (the Management API) are the **same site**. The session cookie set by the Management API is sent on the console's requests across ports, and the `gravitee_http_cors_*` settings allow the cross-origin calls. That's why every console logs in without a reverse proxy.

## Stop and clean up

*   To stop and remove every container and both networks:

    ```bash
    docker rm -f gamma-console gamma-developer-portal gamma-apim-console gamma-gateway gamma-management-api gamma-elasticsearch gamma-mongodb
    docker network rm frontend storage
    ```

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
