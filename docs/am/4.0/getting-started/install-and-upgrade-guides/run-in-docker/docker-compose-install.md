---
description: Step‑by‑step tutorial for Prerequisites.
---

# Docker Compose Install

This section explains how to run AM images in Docker. It is intended for users who are already familiar with Docker.

{% hint style="info" %}
If you want to change the default configuration for any of the component images, see the relevant component section in the [AM Configuration Guide.](../../configuration/README.md)
{% endhint %}

## Prerequisites

To run our images, you must start by installing [Docker](https://docs.docker.com/installation/).

## Images

The AM Docker images are [available on Docker Hub](https://hub.docker.com/u/graviteeio/). You can find all the [Dockerfiles on GitHub](https://github.com/gravitee-io/graviteeio-access-management/tree/master/docker/).

## Run AM

You can run a complete AM environment using our `docker-compose` file. It includes all the AM components and MongoDB.

```sh
# Download required Docker Compose files
$ mkdir -p config
$ curl -L -O https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/compose/docker-compose.yml
$ curl -O https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/compose/.env
$ cd config && { curl -O https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/compose/config/nginx.conf ; cd -; }

# (Optional step: pull to ensure that you are running latest images)
$ docker-compose pull

# And run...
$ docker-compose up
```

## EE deployment

To turn on the enterprise edition mode of Access Management, you must provide a license key to the containers and additional plugins.

You can find below a docker-compose configuration snippet that mounts two volumes for both AM Management API and AM Gateway :

* to deploy enterprise plugins in an additional plugin directory
* to deploy the license file

```sh
  management:
    image: graviteeio/am-management-api:latest
    container_name: gio_am_management
    volumes:
      - /path/to/plugins-dir:/opt/graviteeio-am-management-api/plugins-ee
      - /path/to/license-dir/license.key:/opt/graviteeio-am-management-api/license/license.key
    environment:
      - GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-management-api/plugins
      - GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-management-api/plugins-ee

  gateway:
    image: graviteeio/am-gateway:3.18.0
    container_name: gio_am_gateway
    restart: always
    volumes:
      - /path/to/plugins-dir:/opt/graviteeio-am-gateway/plugins-ee
      - /path/to/license/license.key:/opt/graviteeio-am-gateway/license/license.key
    environment:
      - GRAVITEE_PLUGINS_PATH_0=/opt/graviteeio-am-gateway/plugins
      - GRAVITEE_PLUGINS_PATH_1=/opt/graviteeio-am-gateway/plugins-ee
```

## Check AM is running

When all components are started, you can run a quick test by checking these URLs:

| Image                                                                                  | URL                            |
| -------------------------------------------------------------------------------------- | ------------------------------ |
| [graviteeio/am-gateway](https://hub.docker.com/r/graviteeio/am-gateway/)               | http://localhost/am/           |
| [graviteeio/am-management-api](https://hub.docker.com/r/graviteeio/am-management-api/) | http://localhost/am/management |
| [graviteeio/am-management-ui](https://hub.docker.com/r/graviteeio/am-webui/)           | http://localhost/am/ui/        |

## Run AM with a different version or port

If you want to run a different version of AM or change the default port, you can run `docker-compose` as follows:

```sh
GIO_AM_VERSION=3 NGINX_PORT=18000 docker-compose up
```

## Run AM with a single command

If you want to get up and running quickly with AM 4.x, you can also run the following command line:

{% code overflow="wrap" %}
```sh
curl -L https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/launch.sh | bash
```
{% endcode %}

{% hint style="info" %}
You can change default http port (80), by passing `-s <port>` argument to the curl command.
{% endhint %}

{% code overflow="wrap" %}
```sh
curl -L https://raw.githubusercontent.com/gravitee-io/graviteeio-access-management/master/docker/launch.sh | bash -s 8080
```
{% endcode %}

The validation steps are the same as in the previous section.
