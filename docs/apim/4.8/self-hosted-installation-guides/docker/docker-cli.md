# Docker CLI

## Prerequisites

* You must install Docker. For more information about installing Docker, go to [Install Docker Engine](https://docs.docker.com/engine/install/).
* If you are using the Enterprise Edition (EE) of Gravitee, ensure that you have a licensing key. If you do not know your licensing key, see the [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Install Gravitee APIM

1. Create a directory structure in which to persist data and store plugins:
   1.  Create a directory structure using the following command:

       {% code overflow="wrap" %}
       ```bash
       mkdir -p /gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
       ```
       {% endcode %}
   2.  Once you create the directory, verify that the directory has the following structure:

       {% code overflow="wrap" %}
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
       {% endcode %}
2. (Optional) If you are installing the Enterprise Edition (EE) of Gravitee APIM, copy your license key to `/gravitee/license.key`.
3.  Create two Docker bridge networks using the following commands:

    {% code overflow="wrap" %}
    ```bash
    $ docker network create storage
    $ docker network create frontend
    ```
    {% endcode %}
4.  Install MongoDB using the following commands:

    {% code overflow="wrap" %}
    ```bash
    $ docker pull mongo:6
    $ docker run --name gio_apim_mongodb \
      --net storage \
      --volume /gravitee/mongodb/data:/data/db \
      --detach mongo:6
    ```
    {% endcode %}
5.  Install Elasticsearch using the following commands:

    {% code overflow="wrap" %}
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
    {% endcode %}
6.  Install the API Gateway using the following commands. If you use the Community Edition (CE) of Gravitee APIM, remove the following line:  `--volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key`.

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
7.  Install the Management API using the following commands. If you are installing the CE of Gravitee, remove the following line: `--volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key` .

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
8.  Install the Console using the following commands:

    ```bash
    $ docker pull graviteeio/apim-management-ui:4.0
    $ docker run --publish 8084:8080 \
      --volume /gravitee/apim-management-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_management_ui \
      --env MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT \
      --detach graviteeio/apim-management-ui:4.0
    ```
9.  Install the Developer using the following commands:

    ```bash
    $ docker pull graviteeio/apim-portal-ui:4.0
    $ docker run --publish 8085:8080 \
      --volume /gravitee/apim-portal-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_portal_ui \
      --env PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT \
      --detach graviteeio/apim-portal-ui:4.0
    ```

{% hint style="info" %}
* MongoDB is on the `storage` network and uses `/gravitee/mongodb` for persistent storage.
* Elasticsearch is on the `storage` network and uses `/gravitee/elasticsearch` for persistent storage.
* The API Gateway is on both the `storage` and `frontend` networks and uses `/gravitee/apim-gateway` for persistent storage.
* The Management API is on both the `storage` and `frontend`networks, and uses the `/gravitee/apim-api` for persistent storage.
* The Console is on the `frontend` network and uses `/graviee/apim-management-ui` for persistent storage.
* The Developer Portal is on the `frontend` network and uses `/gravitee/apim-portal-ui` for persistent storage.
{% endhint %}

## Verification

* To open the APIM Console, go to `http://localhost:8084`. The default username and password are both `admin`.
* To open the Developer Portal, go to `http://localhost:8085`. The default username and password are both `admin`.
