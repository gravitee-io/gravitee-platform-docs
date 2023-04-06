# installation-guide-docker-images

## Setup

Before you can get into the actual installation, a couple of things need to be set up

1.  **Docker**

    Is assumed to be installed.
2.  **Persistence**

    Containers are great, but you do want persistence in case they need to be restarted. You are going to persist the MongoDB data, the Elasticsearch data and provide locations for additional plugins (both for the Gateway and the REST API). It is assumed in this page that these will live under a filesystem mounted at `/gravitee` on the host system.

    ```
    mkdir /gravitee/mongodb
    mkdir /gravitee/mongodb/data
    mkdir /gravitee/elasticsearch
    mkdir /gravitee/elasticsearch/data
    mkdir /gravitee/apim-gateway
    mkdir /gravitee/apim-gateway/plugins
    mkdir /gravitee/apim-gateway/logs
    mkdir /gravitee/apim-management-api
    mkdir /gravitee/apim-management-api/plugins
    mkdir /gravitee/apim-management-api/logs
    mkdir /gravitee/apim-management-ui
    mkdir /gravitee/apim-management-ui/logs
    mkdir /gravitee/apim-portal-ui
    mkdir /gravitee/apim-portal-ui/logs
    ```
3.  **Network**

    To provide an easy way for the containers to **talk** in this setup, create two docker networks. One for **storage** communication, one for **frontend** communication. The combination of this network and giving names to the containers will allow you to specify connections easily.

    ```
    docker network create graviteestorage
    docker network create graviteefrontend
    ```

As was indicated before, your architecture may differ and thus require a different setup.

## Install MongoDB

| container   | [MongoDB^](https://hub.docker.com/\_/mongo) |
| ----------- | ------------------------------------------- |
| network     | **graviteestorage**                         |
| persistence | **/gravitee/mongodb/data**                  |

Assumptions

**Instructions**

```
docker pull mongo:3.6
docker run --name gravitee-mongo \
  --net graviteestorage \
  --volume /gravitee/mongodb/data:/data/db \
  --detach mongo:3.6
```

## Install Elasticsearch

| container   | [Elasticsearch^](https://hub.docker.com/\_/elasticsearch) |
| ----------- | --------------------------------------------------------- |
| network     | **graviteestorage**                                       |
| persistence | **/gravitee/elasticsearch/data**                          |

Assumptions

**Instructions**

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.0
docker run --name gravitee-elasticsearch \
  --net graviteestorage \
  --env http.host=0.0.0.0 \
  --env transport.host=0.0.0.0 \
  --env xpack.security.enabled=false \
  --env xpack.monitoring.enabled=false \
  --env cluster.name=gravitee-elasticsearch \
  --env bootstrap.memory_lock=true \
  --env discovery.type=single-node \
  --env "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  --volume /gravitee/elasticsearch/data:/usr/share/elasticsearch/data \
  --detach docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```

## Install API Management Gateway

| container   | [Gateway^](https://hub.docker.com/r/graviteeio/apim-gateway) |
| ----------- | ------------------------------------------------------------ |
| network     | **graviteestorage**                                          |
| network     | **graviteefrontend**                                         |
| persistence | **/gravitee/apim-gateway/plugins**                           |
| persistence | **/gravitee/apim-gateway/logs**                              |

Assumptions

**Instructions**

```
docker pull graviteeio/apim-gateway:latest

docker run --publish 8082:8082 \
  --volume /gravitee/apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext \
  --volume /gravitee/apim-gateway/logs:/opt/graviteeio-gateway/logs \
  --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
  --env gravitee_ratelimit_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
  --env gravitee_reporters_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
  --env gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins \
  --env gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext \
  --net graviteestorage \
  --name gravitee-apim-gateway \
  --detach graviteeio/apim-gateway:latest

docker network connect graviteefrontend gravitee-apim-gateway
```

## Install API Management REST API

| container   | [REST API^](https://hub.docker.com/r/graviteeio/apim-management-api) |
| ----------- | -------------------------------------------------------------------- |
| network     | **graviteestorage**                                                  |
| network     | **graviteefrontend**                                                 |
| persistence | **/gravitee/apim-management-api/plugins**                            |
| persistence | **/gravitee/apim-management-api/logs**                               |

Assumptions

**Instructions**

```
docker pull graviteeio/apim-management-api:latest

docker run --publish 8083:8083 \
  --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
  --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
  --env gravitee_management_mongodb_uri="mongodb://gravitee-mongo:27017/gravitee-apim?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
  --env gravitee_analytics_elasticsearch_endpoints_0="http://gravitee-elasticsearch:9200" \
  --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
  --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
  --net graviteestorage \
  --name gravitee-apim-management-api \
  --detach graviteeio/apim-management-api:latest

docker network connect graviteefrontend gravitee-apim-management-api
```

## Install API Management Management UI

| container   | [Management UI^](https://hub.docker.com/r/graviteeio/apim-management-ui) |
| ----------- | ------------------------------------------------------------------------ |
| network     | **graviteefrontend**                                                     |
| persistence | **/gravitee/apim-management-ui/logs**                                    |

Assumptions

**Instructions**

```
docker pull graviteeio/apim-management-ui:latest
docker run --publish 8084:8080 \
  --volume /gravitee/apim-management-ui/logs:/var/log/nginx \
  --net graviteefrontend \
  --name gravitee-apim-management-ui \
  --env MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT \
  --detach graviteeio/apim-management-ui:latest
```

## Install API Management Portal UI

| container   | [Portal UI^](https://hub.docker.com/r/graviteeio/apim-portal-ui) |
| ----------- | ---------------------------------------------------------------- |
| network     | **graviteefrontend**                                             |
| persistence | **/gravitee/apim-portal-ui/logs**                                |

Assumptions

**Instructions**

```
docker pull graviteeio/apim-portal-ui:latest
docker run --publish 8085:8080 \
  --volume /gravitee/apim-portal-ui/logs:/var/log/nginx \
  --net graviteefrontend \
  --name gravitee-apim-portal-ui \
  --env PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT \
  --detach graviteeio/apim-portal-ui:latest
```
