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

1.  Create a directory structure in which to persist data and store plugins:\


    ```bash
    mkdir -p ./gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
    ```



    This command creates all necessary directories. The structure includes:&#x20;

    * `mongodb/data`: Stores API definitions, applications, and user data
    * `elasticsearch/data`: Contains analytics and monitoring data
    * `apim-gateway/plugins`: Stores custom gateway plugins
    * `apim-gateway/logs`: Gateway application logs
    * `apim-management-api/plugins`: Custom management API plugins
    * `apim-management-api/logs`: Management API application logs
    * `apim-management-ui/logs`: Management Console web server logs
    * `apim-portal-ui/logs`: Developer Portal web server logs
2.  Verify that the directory has the following structure:\


    {% code overflow="wrap" %}
    ```sh
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
3.  (**Enterprise Edition only**) Place your license key file in the current directory:\


    ```bash
    cp /path/to/your/license.key ./license.key
    ```



    {% hint style="info" %}
    Replace `/path/to/your/license.key` with the actual path to your Gravitee license file. You must name your license file  `license.key` and it must be located in the same directory as your `docker-compose-apim.yml` file.
    {% endhint %}
4. In your current root directory, create a file called `docker-compose-apim.yml`.&#x20;
5.  Add the following configuration to your `docker-compose-apim.yml` file, and then save the file:  \


    ```yaml
    #
    # Copyright (C) 2015 The Gravitee team (http://gravitee.io)
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #         http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    #
    version: '3.5'

    networks:
      frontend:
        name: frontend
      storage:
        name: storage

    services:
      mongodb:
        image: mongo:7.0
        container_name: gio_apim_mongodb
        restart: always
        volumes:
          - ./mongodb/data:/data/db
        # Access the MongoDB container logs with: docker logs gio_apim_mongodb
        networks:
          - storage

      elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:8.16.1
        container_name: gio_apim_elasticsearch
        restart: always
        volumes:
          - ./elasticsearch/data:/var/lib/elasticsearch/data
        # Access the Elasticsearch container logs with: docker logs gio_apim_elasticsearch
        environment:
          - http.host=0.0.0.0
          - transport.host=0.0.0.0
          - xpack.security.enabled=false
          - cluster.name=elasticsearch
          - bootstrap.memory_lock=true
          - discovery.type=single-node
          - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        ulimits:
          memlock:
            soft: -1
            hard: -1
          nofile: 65536
        networks:
          - storage

      gateway:
        image: graviteeio/apim-gateway:latest
        container_name: gio_apim_gateway
        restart: always
        ports:
          - "8082:8082"
        depends_on:
          - mongodb
          - elasticsearch
        volumes:
          - ./apim-gateway/logs:/opt/graviteeio-gateway/logs
          - ./apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext
          - ./license.key:/opt/graviteeio-gateway/license/license.key
        environment:
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_ratelimit_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
          - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
          - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
        networks:
          - storage
          - frontend

      management_api:
        image: graviteeio/apim-management-api:latest
        container_name: gio_apim_management_api
        restart: always
        ports:
          - "8083:8083"
        links:
          - mongodb
          - elasticsearch
        depends_on:
          - mongodb
          - elasticsearch
        volumes:
          - ./license.key:/opt/graviteeio-management-api/license/license.key
        environment:
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
          - gravitee_installation_standalone_portal_url=http://localhost:8085
        networks:
          - storage
          - frontend

      management_ui:
        image: graviteeio/apim-management-ui:latest
        container_name: gio_apim_management_ui
        restart: always
        ports:
          - "8084:8080"
        depends_on:
          - management_api
        volumes:
          - ./apim-management-ui/logs:/var/log/nginx
        environment:
          - MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/
        networks:
          - frontend

      portal_ui:
        image: graviteeio/apim-portal-ui:latest
        container_name: gio_apim_portal_ui
        restart: always
        ports:
          - "8085:8080"
        depends_on:
          - management_api
        volumes:
          - ./apim-portal-ui/logs:/var/log/nginx
        environment:
          - PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT
          - gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
          - gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
        networks:
          - frontend
    ```
6.  Run Docker Compose with the following command:\


    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```



    The `-d` flag runs containers in detached mode, which allows the containers to run in the background. When you run the command, Docker completes the following actions:

    * Create the frontend and storage networks.
    * Pull the required container images.
    * Start services in dependency order.
    * Configure inter-service communication.

{% hint style="info" %}
Gravitee API Management may take a few minutes to initialize.
{% endhint %}

## Verification

* To open the APIM Console, go to `http://localhost:8084`. The default username and password are both `admin`.
* To open the Developer Portal, go to `http://localhost:8085`. The default username and password are both `admin`.

## Enable Federation

[Federation](../../govern-apis/federation/) is disabled by default for security and performance reasons. You will enable it by adding environment variables to your existing Docker Compose configuration. If you plan to run multiple APIM instances for high availability, you will also configure cluster mode using Hazelcast to ensure data synchronization across all instances.

To enable Federation, complete the following steps:

* [#enable-federation-with-docker-compose](docker-compose.md#enable-federation-with-docker-compose "mention")
* If you are running multiple replicas of APIM for high availability, [#set-up-cluster-mode](docker-compose.md#set-up-cluster-mode "mention")

### Enable Federation with Docker Compose

Enable Federation by adding the `GRAVITEE_INTEGRATION_ENABLED` environment variable to both the gateway and management API services in your existing `docker-compose-apim.yml` file.

Open your existing `docker-compose-apim.yml` file and locate both the `gateway` and `management_api` service sections and add the Federation environment variable to each. Add `GRAVITEE_INTEGRATION_ENABLED=true` to the `environment` section of both services:

The `GRAVITEE_INTEGRATION_ENABLED=true` setting activates the Federation endpoints in the gateway and management API services.&#x20;

```yaml
  gateway:
    image: graviteeio/apim-gateway:latest
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    depends_on:
      - mongodb
      - elasticsearch
    volumes:
      - ./gravitee/apim-gateway/logs:/opt/graviteeio-gateway/logs
      - ./gravitee/apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext
      - ./license.key:/opt/graviteeio-gateway/license/license.key
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_ratelimit_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
      - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
      - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugin
      - GRAVITEE_INTEGRATION_ENABLED=true # activates federation 

  management_api:
    image: graviteeio/apim-management-api:latest
    container_name: gio_apim_management_api
    restart: always
    ports:
      - "8083:8083"
    links:
      - mongodb
      - elasticsearch
    depends_on:
      - mongodb
      - elasticsearch
    volumes:
      - ./license.key:/opt/graviteeio-management-api/license/license.key
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
      - gravitee_installation_standalone_portal_url=http://localhost:8085
      - GRAVITEE_INTEGRATION_ENABLED=true # activates federation 
```

Restart your APIM services because Docker containers read environment variables only during container startup. The running containers cannot detect the new `GRAVITEE_INTEGRATION_ENABLED` setting without a restart.

```bash
docker compose -f docker-compose-apim.yml down
```

Start the services with the updated Federation configuration:

```
docker compose -f docker-compose-apim.yml up -d
```

### Set up cluster mode

If APIM is running with high availability, you need to set up cluster mode. To set up cluster mode, complete the following steps:

1.  Add the following parameter values to the root of your `gravitee.yaml` configuration file:\


    ```yaml
    GRAVITEE_CLUSTER_TYPE = hazelcast
    GRAVITEE_CLUSTER_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast.xml
    GRAVITEE_CACHE_TYPE = hazelcast
    GRAVITEE_CACHE_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast.xml
    ```
2.  Open the example `hazelcast.xml` configuration file that is included in the distribution, and then modify the following sections as needed:\


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
3. Mount a volume with the `hazelcast.xml` configuration file. This is used to configure Hazelcast, which can then run as a library inside the APIM container.
4. Add the following plugins to APIM. They are not included by default.
   * [https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip ](https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip)
   * [https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip](https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip)
