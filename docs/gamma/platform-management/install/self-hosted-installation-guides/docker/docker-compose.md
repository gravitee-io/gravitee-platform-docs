# Docker Compose

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to run a self-hosted Gravitee Gamma platform on your own machine with Docker Compose, from a single self-contained file.

You run the standard APIM containers, turn on Gamma in both the Management API and the Gateway with `gravitee_gamma_enabled=true`, and add the Gamma console (`graviteeio/gamma-ui`). The Gamma console isn't a separate backend. It talks to the Management API, which runs with Gamma enabled. Enabling Gamma on the Gateway is required to sync AuthZ policies (PDP) for Authorization Management.

Every component is published on `localhost` on its own port. On a single host, `localhost:8084`, `localhost:8086`, and `localhost:8083` are the **same site**, so the login session cookie is sent across ports and the consoles log in. For the detail, see [Why this works on one host](docker-compose.md#why-this-works-on-one-host).

## Prerequisites

Before you start, complete the following steps:

* Install Docker. For more information, see [Install Docker Engine](https://docs.docker.com/engine/install/).
* **(Enterprise Edition only)** To enable Agent Management, you need an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. For more information, see [Add your license key](docker-compose.md#enterprise-edition-only-add-your-license-key).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Run Gamma

To run Gamma, complete the following steps:

1. [#create-the-compose-file](docker-compose.md#create-the-compose-file "mention")
2. [#enterprise-edition-only-add-your-license-key](docker-compose.md#enterprise-edition-only-add-your-license-key "mention")
3. [#start-the-stack](docker-compose.md#start-the-stack "mention")

### Create the compose file

1.  Create a file named `docker-compose-gamma.yml`, and then copy the following configuration into it:

    ```yaml
    networks:
      gamma:
        name: gamma

    volumes:
      mongo-data:
      es-data:

    services:
      mongodb:
        image: mongo:7.0
        container_name: gamma_mongodb
        restart: unless-stopped
        volumes:
          - mongo-data:/data/db
        networks: [gamma]

      elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:8.17.2
        container_name: gamma_elasticsearch
        restart: unless-stopped
        environment:
          - discovery.type=single-node
          - xpack.security.enabled=false
          - ES_JAVA_OPTS=-Xms512m -Xmx512m
        volumes:
          - es-data:/usr/share/elasticsearch/data
        networks: [gamma]

      gateway:
        image: graviteeio/apim-gateway:4.12.0
        container_name: gamma_gateway
        restart: unless-stopped
        depends_on: [mongodb, elasticsearch]
        ports:
          - "8082:8082"
        environment:
          # Turn on Gamma in the Gateway (required for AuthZ policy/PDP sync)
          - gravitee_gamma_enabled=true
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_ratelimit_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
        networks: [gamma]

      management_api:
        image: graviteeio/apim-management-api:4.12.0
        container_name: gamma_management_api
        restart: unless-stopped
        depends_on: [mongodb, elasticsearch]
        ports:
          - "8083:8083"
        environment:
          # Turn on Gamma in the Management API
          - gravitee_gamma_enabled=true
          # Datastores
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
          # Console and portal URLs
          - gravitee_installation_standalone_console_url=http://localhost:8084
          - gravitee_installation_standalone_portal_url=http://localhost:8085
          # CORS - allow the console origins with credentials
          - gravitee_http_cors_enabled=true
          - gravitee_http_cors_allow-origin_0=http://localhost:8084
          - gravitee_http_cors_allow-origin_1=http://localhost:8085
          - gravitee_http_cors_allow-origin_2=http://localhost:8086
          - gravitee_http_cors_allow-headers=Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie
          - gravitee_http_cors_allow-methods=GET,POST,PUT,DELETE,OPTIONS
          - gravitee_http_cors_exposed-headers=X-Total-Count,Set-Cookie
          - gravitee_http_cors_allow-credentials=true
          # Cookie - same-site localhost over HTTP
          - gravitee_http_cookie_sameSite=Lax
          - gravitee_http_cookie_secure=false
        # (Enterprise Edition) Agent Management needs a license. Once you have your
        # license, uncomment the two lines below and place your license file as
        # license.key next to this compose file, then redeploy. See
        # "(Enterprise Edition only) Add your license key".
        # volumes:
        #   - ./license.key:/opt/graviteeio-management-api/license/license.key:ro
        networks: [gamma]

      management_ui:
        image: graviteeio/apim-management-ui:4.12.0
        container_name: gamma_apim_console
        restart: unless-stopped
        depends_on: [management_api]
        ports:
          - "8084:8080"
        environment:
          - MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/
        networks: [gamma]

      portal_ui:
        image: graviteeio/apim-portal-ui:4.12.0
        container_name: gamma_portal
        restart: unless-stopped
        depends_on: [management_api]
        ports:
          - "8085:8080"
        environment:
          - PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT
        networks: [gamma]

      gamma_console:
        image: graviteeio/gamma-ui:4.12.0
        container_name: gamma_console
        restart: unless-stopped
        depends_on: [management_api]
        ports:
          - "8086:8080"
        environment:
          - GAMMA_API_URL=http://localhost:8083/gamma
          - GAMMA_CONSOLE_BASE_HREF=/
          - HTTP_PORT=8080
          - SERVER_NAME=localhost
        networks: [gamma]
    ```
2. Save the `docker-compose-gamma.yml` file.

<details>

<summary>Explanations of key settings</summary>

**Turn on Gamma**

`gravitee_gamma_enabled=true` activates Gamma and must be set on both the `management_api` and `gateway` services. On `management_api`, it mounts the Gamma API at `/gamma` on port `8083`. On `gateway`, it enables AuthZ policy (PDP) synchronization, which is required for Authorization Management. The `gamma_console` service (`graviteeio/gamma-ui`) is the Gamma user interface.

**Gamma console wiring**

* `GAMMA_API_URL=http://localhost:8083/gamma` is the URL the Gamma console uses to reach the Gamma API. The console writes it into its `constants.json`.
* `GAMMA_CONSOLE_BASE_HREF=/` serves the Gamma console at the root path on its port.

**CORS and cookies**

Each console is on a different port from the Management API, so the browser requests are cross-origin. The `gravitee_http_cors_*` settings allow the three console origins with credentials, and `gravitee_http_cookie_sameSite=Lax` with `secure=false` lets the session cookie ride along over HTTP between same-site `localhost` ports.

</details>

### (Enterprise Edition only) Add your license key

Agent Management is an enterprise feature. It only activates with an enterprise license that includes the `agent-management` pack. Without a license, the module loads but stays inactive and doesn't appear in the console. The other modules (API Management, Authorization Management, and Platform Management) work without a license.

To get a license, contact your Technical Account Manager. Your account manager sends you the license as a `license.key` file.

{% hint style="info" %}
If your license is a base64-encoded text file (for example, `license.base64.txt`), the Management API can't read that text. Decode it into the `license.key` file the container expects. Run the command in the same directory as `docker-compose-gamma.yml`, and replace `license.base64.txt` with the name of your file:

```bash
base64 -d < license.base64.txt > license.key
```

On macOS, use `base64 -D` (capital `D`) if `base64 -d` returns an error.
{% endhint %}

Once you have your `license.key`, complete the following steps:

1. Place the `license.key` file in the same directory as `docker-compose-gamma.yml`.
2.  In the `management_api` service of `docker-compose-gamma.yml`, uncomment the two license lines so the `license.key` file is mounted into the container:

    ```yaml
        volumes:
          - ./license.key:/opt/graviteeio-management-api/license/license.key:ro
    ```
3.  Redeploy the stack:

    ```bash
    docker compose -f docker-compose-gamma.yml up -d
    ```

    \
    After the Management API restarts, Agent Management appears in the console module switcher.

### Start the stack

1.  Start the services from the directory that contains `docker-compose-gamma.yml`:

    ```bash
    docker compose -f docker-compose-gamma.yml up -d
    ```

    Docker pulls the images, creates the network and volumes, and starts the services. The Management API takes a few minutes to initialize.

{% hint style="info" %}
Elasticsearch and the Management API are memory-heavy. If a container exits or keeps restarting, give Docker a few gigabytes of memory, then run the command again.
{% endhint %}

#### Verification

*   Confirm the Management API is ready using the following command:

    ```bash
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8083/management/v2/ui/bootstrap
    ```

    \
    The command returns `200` once the platform is up.

## Access the consoles

Open the consoles in your browser. The default username and password for the Gamma console, the APIM Console, and the Developer Portal are both `admin`.

| Component        | URL                     | Default credentials |
| ---------------- | ----------------------- | ------------------- |
| Gamma console    | `http://localhost:8086` | `admin` / `admin`   |
| APIM Console     | `http://localhost:8084` | `admin` / `admin`   |
| Developer Portal | `http://localhost:8085` | `admin` / `admin`   |
| API Gateway      | `http://localhost:8082` | Not applicable      |

## Why this works on one host

The cross-origin cookie problem that breaks Gamma login on separate hostnames doesn't apply here. For cookies, a "site" is the registrable domain, and the port is ignored. So `localhost:8086` (the Gamma console) and `localhost:8083` (the Management API) are the **same site**. The session cookie set by the Management API is sent on the console's requests across ports, and the `gravitee_http_cors_*` settings allow the cross-origin calls. That's why every console logs in without a reverse proxy.

## Stop and clean up

*   To stop and remove the containers while keeping the database data:

    ```bash
    docker compose -f docker-compose-gamma.yml down
    ```
*   To stop the containers and delete all data:

    ```bash
    docker compose -f docker-compose-gamma.yml down -v
    ```

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../../agent-management/get-started/create-your-first-mcp-server.md).
