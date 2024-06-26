# Custom Install with Docker Compose

## Overview

This page describes how to install and run APIM Community Edition or APIM Enterprise Edition in Docker containers on `localhost` using the `docker compose` command and a specified filesystem for persistence and plugins.

## Prerequisites

* Docker is installed and running
* The Enterprise Edition requires a [license key](https://www.gravitee.io/pricing)

## Install APIM

### 1. Create the filesystem and download the `docker compose` file

1.  Use the following command to create a directory structure in which to persist data, store plugins, and save a copy of the Docker Compose file:

    {% code overflow="wrap" %}
    ```bash
    mkdir -p ./gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
    ```
    {% endcode %}
2.  Verify the directory has the following structure:

    {% code overflow="wrap" %}
    ```bash
    /gravitee
     ├── docker-compose-apim.yaml
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
3. Enter the `/gravitee` directory
4.  Download the `docker-compose.yml` file as `docker-compose-apim.yml`:

    {% code overflow="wrap" %}
    ```bash
    curl -L https://bit.ly/docker-apim-4x -o docker-compose-apim.yml
    ```
    {% endcode %}

### 2. Edit `docker-compose-apim.yml`

Edit `docker-compose-apim.yml` so the installation uses the `/gravitee` filesystem.

1. Open `docker-compose-apim.yml` in a text editor.
2.  Remove the following lines:

    {% code overflow="wrap" %}
    ```bash
    volumes:
      data-elasticsearch:
      data-mongo:
    ```
    {% endcode %}
3.  Change `$services.mongodb.volumes` to:

    {% code overflow="wrap" %}
    ```bash
    volumes:
      - ./mongodb/data:/data/db
    # Access the MongoDB container logs with: docker logs gio_apim_mongodb
    ```
    {% endcode %}
4.  Change `$services.elasticsearch.volumes` to:

    {% code overflow="wrap" %}
    ```bash
    volumes:
      - ./elasticsearch/data:/var/lib/elasticsearch/data
    # Access the Elasticsearch container logs with: docker logs gio_apim_elasticsearch
    ```
    {% endcode %}
5.  Change `$services.gateway.volumes` to:

    {% code overflow="wrap" %}
    ```bash
    volumes:
      - ./apim-gateway/logs:/opt/graviteeio-gateway/logs
      - ./apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext
    ```
    {% endcode %}
6.  Add the following lines to `$services.gateway.environment`:

    {% code overflow="wrap" %}
    ```bash
    - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
    - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
    ```
    {% endcode %}
7. Remove `$services.management_api.links`
8.  Change `$services.management_api.volumes` to:

    ```bash
    volumes:
      - ./apim-management-api/logs:/opt/graviteeio-management-api/logs
      - ./apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext
    ```
9.  Add the following lines to `$services.management_api.environment`:

    {% code overflow="wrap" %}
    ```bash
    - gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
    - gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
    ```
    {% endcode %}
10. Change `$services.management_ui.volumes` to:

    ```bash
    volumes:
      - ./apim-management-ui/logs:/var/log/nginx
    ```
11. Change `$services.portal_ui.volumes` section to:

    ```bash
    volumes:
      - ./apim-portal-ui/logs:/var/log/nginx
    ```

### 3. Add the license key

If you are installing the Enterprise Edition, you need to add the license key. If you are installing the Community Edition, skip these steps.

1. Copy your license key to `/gravitee/license.key`
2. Open `docker-compose-apim.yml` in a text editor
3.  Under `$services.gateway.volumes`, add the following line:

    ```bash
    - ./license.key:/opt/graviteeio-gateway/license/license.key
    ```
4.  Under `$services.management_api.volumes`, add the following line:

    ```bash
    - ./license.key:/opt/graviteeio-management-api/license/license.key
    ```

### 4. Run `docker compose`

1.  Run `docker compose` to download and start all of the components:

    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```
2.  In your browser:

    1. Go to `http://localhost:8084` to open the Console
    2. Go to `http://localhost:8085` to open the Developer Portal

    You can log in to both with username `admin` and password `admin`.

{% hint style="info" %}
**Container initialization**

APIM can take up to a minute to fully initialize with Docker. If you get an error when going to `http://localhost:8084` or `http://localhost:8085`, wait, then try again.
{% endhint %}

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/) for your next steps.
{% endhint %}

## Enable Federation

[Federation](../../../guides/federation/) is a new capability that was released with Gravitee 4.4.

Federation is disabled by default and must be explicitly activated for it to work.&#x20;

To enable federation, follow the first guide below to [enable federation with Docker Compose](custom-install-with-docker-compose.md#enable-federation-with-docker-compose).&#x20;

If in addition you are running multiple replicas of APIM for high availability, you'll also need to ensure that [cluster mode is set up](custom-install-with-docker-compose.md#set-up-cluster-mode).&#x20;

### Enable Federation with Docker Compose

To enable federation, define the following environment variable and set its value to `true` (default is `false`):

`GRAVITEE_INTEGRATION_ENABLED = true`

### Set up cluster mode

For cases where APIM is running with high availability, you'll need to setup cluster mode.

The following parameters and values need to be added to the root of the gravitee.yaml configuration file:

```bash
GRAVITEE_CLUSTER_TYPE = hazelcast
GRAVITEE_CLUSTER_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast.xml
GRAVITEE_CACHE_TYPE = hazelcast
GRAVITEE_CACHE_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast.xml
```

In addition, you'll need to mount a volume with the hazelcast.xml configuration file. This is used to configure Hazelcast that will run as a library inside the APIM container.

An example hazelcast.xml configuration file will be included in the distribution, but you may need to change certain parts (those emphasized below):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hazelcast xmlns="http://www.hazelcast.com/schema/config"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.hazelcast.com/schema/config
          http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">
   <cluster-name>graviteeio-api-cluster</cluster-name>
   <properties>
       <property name="hazelcast.discovery.enabled">true</property>
       <property name="hazelcast.max.wait.seconds.before.join">3</property>
       <property name="hazelcast.member.list.publish.interval.seconds">5</property>
       <property name="hazelcast.socket.client.bind.any">false</property>
       <property name="hazelcast.logging.type">slf4j</property>
   </properties>


   <queue name="integration-cluster-command-*">
       <backup-count>0</backup-count>
       <async-backup-count>1</async-backup-count>
   </queue>


   <map name="integration-controller-primary-channel-candidate">
       <backup-count>0</backup-count>
       <async-backup-count>1</async-backup-count>
   </map>


   <cp-subsystem>
       <cp-member-count>0</cp-member-count>
   </cp-subsystem>


   <network>
       <!-- CUSTOMIZE THIS JOIN SECTION --> 
       <join>
            <auto-detection/>
            <multicast enabled="false"/>
            <tcp-ip enabled="true">
                <interface>127.0.0.1</interface>
            </tcp-ip>
       </join>
   </network>
</hazelcast>
```

You will also need to add two new plugins to APIM that aren’t included by default:

* [https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip ](https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip)
* [https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip](https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip)

\
