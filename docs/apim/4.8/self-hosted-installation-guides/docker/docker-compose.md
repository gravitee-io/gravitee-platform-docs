---
hidden: true
---

# Docker Compose

## Overview

This guide explains how to install Gravitee API Management (APIM) with Docker Compose. When you install APIM with Docker Compose, you can install custom plugins and control the location of the persistent data.

## Prerequisites

Before you install APIM, complete the following steps:

* Install Docker. For more information about installing Docker, go to [Install Docker Engine](https://docs.docker.com/engine/install/).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Install Gravitee APIM&#x20;

1.  Create the directory structure, and then download the `docker compose` file. Once you create the directory, verify that the directory has the following structure:

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
2.  &#x20;To ensure that the `docker-compose-apim.yml` uses the `/gravitee`directory structure, follow the following sub-steps:

    a. in a text editor, open `docker-compose-apim.yml`

    b. Remove the following lines of code:

{% code overflow="wrap" %}
```bash
volumes:
  data-elasticsearch:
  data-mongo:
```
{% endcode %}

&#x20;       c. Change `$services.mongodb.volumes` to the following code:

{% code overflow="wrap" %}
```bash
volumes:
  - ./mongodb/data:/data/db
# Access the MongoDB container logs with: docker logs gio_apim_mongodb
```
{% endcode %}

&#x20;        d. Change `$services.gateway.volumes` to the following code:

{% code overflow="wrap" %}
```bash
volumes:
  - ./elasticsearch/data:/var/lib/elasticsearch/data
# Access the Elasticsearch container logs with: docker logs gio_apim_elasticsearch
```
{% endcode %}

&#x20;      e. Navigate to `$services.gateway.volumes`, and then add the following lines of code:

{% code overflow="wrap" %}
```yaml
volumes:
  - ./apim-gateway/logs:/opt/graviteeio-gateway/logs
  - ./apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext
```
{% endcode %}

&#x20;      f. Add the following environment variables:

```yaml
environment:
            - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
            - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
```

&#x20;    h. Remove `$services.management_api.links`.

&#x20;    i. Change `$services.management_ui.volumes` to the following lines of code:

```bash
volumes:
  - ./apim-management-api/logs:/opt/graviteeio-management-api/logs
  - ./apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext
```

&#x20;   j.  Add the following lines to `$services.management_api.environment`:

{% code overflow="wrap" %}
```bash
- gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
- gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
```
{% endcode %}

&#x20;   k. Change `$services.management_ui.volumes`to the following lines of code:

```bash
volumes:
  - ./apim-management-ui/logs:/var/log/nginx
```

&#x20;   l. Change `$services.portal_ui.volumes` to the following lines of code:

```bash
volumes:
  - ./apim-portal-ui/logs:/var/log/nginx
```

3. (Optional) If you are using the Enterprise Edition (EE) of Gravitee APIM, add your license key by following the following steps:

&#x20;       a. Copy your license key to `/gravitee/license.key.`

&#x20;       b. In a text editor, open the `docker-compose-apim.yml` file.

&#x20;       c. Navigate to `$services.gateway.volumes`, and then add the following line of code:

```bash
- ./license.key:/opt/graviteeio-gateway/license/license.key
```

&#x20;      d. Navigate to `$services.management_api.volumes`, and then add the following line of code:

```bash
- ./license.key:/opt/graviteeio-management-api/license/license.key
```

4. Run `docker compose`using the following command:

```bash
docker compose -f docker-compose-apim.yml up -d
```

5. To open the Console and the Developer portal, complete the following steps:

* To open the console, go to `http://localhost:8084`.
* To open the Developer Portal, go to `http://localhost:8085.`

{% hint style="info" %}
- The default username for the Console and the Developer Portal is admin.
- The default password for the Developer Portal is admin.
{% endhint %}

## Enable Federation

[Federation](broken-reference) is a new capability that was released with Gravitee 4.4. Federation is disabled by default and must be explicitly activated for it to work.&#x20;

To enable federation, follow the first guide below to [enable federation with Docker Compose](docker-compose.md#enable-federation-with-docker-compose). If in addition you are running multiple replicas of APIM for high availability, you'll also need to ensure that [cluster mode is set up](docker-compose.md#set-up-cluster-mode).&#x20;

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
