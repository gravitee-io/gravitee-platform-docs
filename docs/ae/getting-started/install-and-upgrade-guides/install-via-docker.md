---
description: This article covers how to install Alert Engine via Docker
---

# Install via Docker

## Introduction and prerequisites

This section explains how to run AE images in Docker. These procedures are intended for users who are already familiar with Docker.

### Prerequisites

To run our official images, you must first install [Docker](https://docs.docker.com/installation/).

## Images

You can find the complete set of AE images [on Docker Hub](https://hub.docker.com/u/graviteeio/).

| Image name                                                             | Version | Base                                                             |
| ---------------------------------------------------------------------- | ------- | ---------------------------------------------------------------- |
| [graviteeio/ae-engine](https://hub.docker.com/r/graviteeio/ae-engine/) | latest  | [openjdk:11-jre-slim-buster](https://hub.docker.com/_/openjdk/) |

### graviteeio/ae-engine

The AE image provides a set of environment variables you can use tune your container.

### **Run the image**

```
$ docker run  \
        --publish 72:8072  \
        --name alert-engine  \
        --detach  \
        graviteeio/ae-engine:2.1.2
```

### **Configure the container**

If you want to override the default configuration and any properties included in the `gravitee.yml` file, you need to use environment variables. For more information, see the [Configuration](../configuration/README.md) section.

The following example changes the Hazelcast configuration file:

```
$ docker run  \
        --publish 72:8072  \
        --name alert-engine  \
        --volume /host/path/to/hazelcast.xml:/container/path/to/hazelcast.xml:ro \
        --env GRAVITEE_CLUSTER_HAZELCAST_CONFIG_PATH=/path/to/hazelcast.xml
        --detach  \
        graviteeio/ae-engine:2.1.2
```

\\
