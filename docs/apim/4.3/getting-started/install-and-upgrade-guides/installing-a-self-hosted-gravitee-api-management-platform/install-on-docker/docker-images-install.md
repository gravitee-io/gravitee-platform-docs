---
description: >-
  An overview about Installing Gravitee API Management with Docker Images
  Install.
---

# Installing Gravitee API Management with Docker Images Install

## Overview

This page describes how to install and run APIM Community Edition or APIM Enterprise Edition in Docker containers on `localhost` using the `docker` command and a specified filesystem for persistence and plugins.

## Prerequisites

* Docker is installed and running
* The Enterprise Edition requires a [license key](https://www.gravitee.io/pricing)

## Install APIM

1.  Use the following command to create a directory structure in which to persist data and store plugins:

    \{% code overflow="wrap" %\}

    ```bash
    mkdir -p /gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
    ```

    \{% endcode %\}
2.  Verify the directory has the following structure:

    \{% code overflow="wrap" %\}

    ```bash
    /gravitee
     ├── apim-gateway
     │    ├── logs
     │    └── plugins
     ├── apim-management-api
     │    ├── logs
     │    └── plugins
     ├── apim-management-ui
     │    └── logs
     ├── apim-portal-ui
     │    └── logs
     ├── elasticsearch
     │    └── data
     └── mongodb
         └── data
    ```

    \{% endcode %\}
3. If you are installing the Enterprise Edition, copy your license key to `/gravitee/license.key`
4.  Create two Docker bridge networks using the following commands:

    \{% code overflow="wrap" %\}

    ```bash
    $ docker network create storage
    $ docker network create frontend
    ```

    \{% endcode %\}
5.  Install MongoDB using the following commands. Note that MongoDB is on the `storage` network and uses `/gravitee/mongodb` for persistent storage.

    \{% code overflow="wrap" %\}

    ```bash
    $ docker pull mongo:6
    $ docker run --name gio_apim_mongodb \
      --net storage \
      --volume /gravitee/mongodb/data:/data/db \
      --detach mongo:6
    ```

    \{% endcode %\}
6.  Install Elasticsearch using the following commands. Note that Elasticsearch is on the `storage` network and uses `/gravitee/elasticsearch` for persistent storage.

    \{% code overflow="wrap" %\}

    ```bash
    $ docker pull docker.elastic.co/elasticsearch/elasticsearch:8.8.1
    $ docker run --name gio_apim_elasticsearch \
      --net storage \
      --hostname elasticsearch \
      --env http.host=0.0.0.0 \
      --env transport.host=0.0.0.0 \
      --env xpack.security.enabled=false \
      --env xpack.monitoring.enabled=false \
      --env cluster.name=elasticsearch \
      --env bootstrap.memory_lock=true \
      --env discovery.type=single-node \
      --env "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
      --volume /gravitee/elasticsearch/data:/var/lib/elasticsearch/data \
      --detach docker.elastic.co/elasticsearch/elasticsearch:8.8.1
    ```

    \{% endcode %\}
7.  Install the API Gateway using the following commands.

    *   If you are installing the Community Edition, remove the following line:

        ```bash
        --volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key \
        ```

    Note that the API Gateway is on both the `storage` and `frontend` networks and it uses `/gravitee/apim-gateway` for persistent storage.

    ```bash
    $ docker pull graviteeio/apim-gateway:4.0
    $ docker run --publish 8082:8082 \
      --volume /gravitee/apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext \
      --volume /gravitee/apim-gateway/logs:/opt/graviteeio-gateway/logs \
      --volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_ratelimit_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_reporters_elasticsearch_endpoints_0="http://elasticsearch:9200" \
      --env gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext \
      --net storage \
      --name gio_apim_gateway \
      --detach graviteeio/apim-gateway:4.0
    $ docker network connect frontend gio_apim_gateway
    ```
8.  Install the Management API using the following commands.

    *   If you are installing the Community Edition, remove the following line:

        ```bash
        --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
        ```

    Note that the Management API is on both the `storage` and `frontend` networks and it uses `/gravitee/apim-api` for persistent storage.

    ```bash
    $ docker pull graviteeio/apim-management-api:4.0
    $ docker run --publish 8083:8083 \
      --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
      --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
      --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://elasticsearch:9200" \
      --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
      --net storage \
      --name gio_apim_management_api \
      --detach graviteeio/apim-management-api:4.0
    $ docker network connect frontend gio_apim_management_api
    ```
9.  Install the Console using the following commands. Note that the Console is on the `frontend` network and it uses `/gravitee/apim-management-ui` for persistent storage.

    ```bash
    $ docker pull graviteeio/apim-management-ui:4.0
    $ docker run --publish 8084:8080 \
      --volume /gravitee/apim-management-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_management_ui \
      --env MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT \
      --detach graviteeio/apim-management-ui:4.0
    ```
10. Install the Developer Portal using the following commands. Note that the Developer Portal is on the `frontend` network and it uses `/gravitee/apim-portal-ui` for persistent storage.

    ```bash
    $ docker pull graviteeio/apim-portal-ui:4.0
    $ docker run --publish 8085:8080 \
      --volume /gravitee/apim-portal-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_portal_ui \
      --env PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT \
      --detach graviteeio/apim-portal-ui:4.0
    ```
11. In your browser:

    1. Go to `http://localhost:8084` to open the APIM Console
    2. Go to `http://localhost:8085` to open the APIM Developer Portal

    You can log in to both with the username `admin` and password `admin`.

{% hint style="info" %}
**Container initialization**

APIM can take up to a minute to fully initialize with Docker. If you get an error when going to `http://localhost:8084` or `http://localhost:8085`, wait, then try again.
{% endhint %}

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../../quickstart-guide/) for your next steps.
{% endhint %}
