# Docker Images Install

This section explains how to run AM images in Docker. These procedures are intended for users who are already familiar with Docker.

## Prerequisites

To run our official images, you must first install [Docker](https://docs.docker.com/installation/).

## Images

You can find the complete set of AM images on [Docker Hub](https://hub.docker.com/u/graviteeio/).

{% hint style="info" %}
You can also find all the [Docker files on GitHub](https://github.com/gravitee-io/graviteeio-access-management/tree/master/docker/). Starting from the version 3.18.0, Gravitee will provide a single bundle for AM Community and Enterprise Edition (EE).
{% endhint %}

| Image name                                                                             | Source                                                                                                                     | Version | Base                                                                                                   |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------ |
| [graviteeio/am-gateway](https://hub.docker.com/r/graviteeio/am-gateway/)               | [images/am-gateway](https://github.com/gravitee-io/graviteeio-access-management/tree/master/docker/gateway/)               | latest  | [eclipse-temurin:17-jre-alpine](https://hub.docker.com/_/eclipse-temurin?tab=tags\&name=17-jre-alpine) |
| [graviteeio/am-management-api](https://hub.docker.com/r/graviteeio/am-management-api/) | [images/am-management-api](https://github.com/gravitee-io/graviteeio-access-management/tree/master/docker/management-api/) | latest  | [eclipse-temurin:17-jre-alpine](https://hub.docker.com/_/eclipse-temurin?tab=tags\&name=17-jre-alpine) |
| [graviteeio/am-management-ui](https://hub.docker.com/r/graviteeio/am-management-ui/)   | [images/am-webui](https://github.com/gravitee-io/graviteeio-access-management/tree/master/docker/management-ui/)           | latest  | [nginx:1.21-alpine](https://hub.docker.com/_/nginx?tab=tags\&name=1.21-alpine)                         |

### graviteeio/am-gateway

The AM Gateway image provides a set of environment variables that you can use to tune your container.

You can replace the address of the default MongoDB repository (`localhost:27017`) with your own (`GRAVITEE_MONGODB_HOST:GRAVITEE_MONGODB_PORT`).

#### **Run the image**

```sh
docker run  \
        --publish 8092:8092  \
        --name am-sgateway  \
        --detach  \
        graviteeio/am-gateway:latest
```

#### **Configure the container**

If you want to override the default configuration for MongoDB and any other properties included in the `gravitee.yml` file, you need to use environment variables. For more information, see the [AM Gateway configuration section.](../../configuration/configure-am-gateway/README.md)

The following example changes the MongoDB connection:

```sh
docker run  \
        --publish 8092:8092  \
        --name am-gateway  \
        --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname
        --detach  \
        graviteeio/am-gateway:latest
```

#### **Configure EE feature**

If you want to start AM EE distribution, you will have to deploy a license key and install the [EE plugins](https://download.gravitee.io/#graviteeio-ee/am/plugins/) attached to your license key.

The following example show how to provide a license key to the container and additional plugins:

```sh
docker run  \
        --publish 8092:8092  \
        --name am-gateway  \
        --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname
        --env GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-gateway/plugins
        --env GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-gateway/plugins-ee
        -v license.key:/opt/graviteeio-gateway/license
        -v plugins-dir-ee:/opt/graviteeio-gateway/plugins-ee
        --detach  \
        graviteeio/am-gateway:latest
```

### graviteeio/am-management-api

The AM API image provides a set of environment variables which you can use to tune your container. You can replace the address of the default MongoDB repository (`localhost:27017`) with your own (`GRAVITEE_MONGODB_HOST:GRAVITEE_MONGODB_PORT`).

#### **Run the image**

```sh
docker run \
          --publish 8093:8093 \
          --name am-management-api \
          --detach  \
          graviteeio/am-management-api:latest
```

#### **Configure the container**

If you want to override the default configuration for MongoDB and any other properties included in the `gravitee.yml` file, you need to use environment variables. For more information, see the [AM API configuration section.](../../configuration/configure-am-api/README.md)

The following example changes the MongoDB connection:

```sh
docker run \
          --publish 8093:8093 \
          --name am-management-api \
          --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname
          --detach  \
          graviteeio/am-management-api:latest
```

#### **Configure EE feature**

If you want to start AM EE distribution, you will have to deploy a license key and install the [EE plugins](https://download.gravitee.io/#graviteeio-ee/am/plugins/) attached to your license key.

The following example shows how to provide a license key to the container and additional plugins:

```sh
docker run  \
        --publish 8093:8093 \
        --name am-management-api \
        --env GRAVITEE_MANAGEMENT_MONGODB_URI=mongodb://username:password@mongohost:27017/dbname
        --env GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-management-api/plugins
        --env GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-management-api/plugins-ee
        -v license.key:/opt/graviteeio-am-management-api/license
        -v plugins-dir-ee:/opt/graviteeio-am-management-api/plugins-ee
        --detach  \
        graviteeio/am-management-api:latest
```

### graviteeio/am-management-ui

The AM Console image provides a set of environment variables that you can use to tune your container. AM Console needs AM API to run, so you need to update `MGMT_API_URL` to specify where `management-api` is running.

#### **Run the image**

```sh
docker run \
        --publish 80:8080 \
        --env MGMT_API_URL=http://localhost:8093/management/ \
        --name am-management-ui \
        --detach  \
        graviteeio/am-management-ui:latest
```
