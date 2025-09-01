# Docker Compose

### Overview <a href="#overview" id="overview"></a>

This guide explains how to install Gravitee API Management (APIM) with Docker Compose. When you install APIM with Docker Compose, you can install custom plugins and control the location of the persistent data.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

Before you install APIM, complete the following steps:

* Install Docker. For more information about installing Docker, go to Install [Docker Engine](https://docs.docker.com/engine/install/).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see Gravitee Platform [Pricing](https://www.gravitee.io/pricing).

### Install Gravitee APIM <a href="#install-gravitee-apim" id="install-gravitee-apim"></a>

1.  Create a directory structure in which to persist data and store plugins:\


    ```bash
    mkdir -p ./gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
    ```

    This command creates all necessary directories. The structure includes:

    * `mongodb/data`: Stores API definitions, applications, and user data
    * `elasticsearch/data`: Contains analytics and monitoring data
    * `apim-gateway/plugins`: Stores custom gateway plugins
    * `apim-gateway/logs`: Gateway application logs
    * `apim-management-api/plugins`: Custom management API plugins
    * `apim-management-api/logs`: Management API application logs
    * `apim-management-ui/logs`: Management Console web server logs
    * `apim-portal-ui/logs`: Developer Portal web server logs
2.  Verify that the directory has the following structure:



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
3.  (**Enterprise Edition only**) Place your license key file in the current root directory:



    ```bash
    cp /path/to/your/license.key ./license.key
    ```

    Replace `/path/to/your/license.key` with the actual path to your Gravitee license file. You must name your license file `license.key` and it must be located in the same directory as your `docker-compose-apim.yml` file.
4. In your current root directory, create a file called `docker-compose-apim.yml`.
5.  Add the following configuration to your `docker-compose-apim.yml` file, and then save the file:



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
        container_name: mgmtapi
        restart: always
        ports:
          - "8083:8083"
          - "8072:8072"  # Federation WebSocket port for agents
        links:
          - mongodb
          - elasticsearch
        depends_on:
          - mongodb
          - elasticsearch
        volumes:
          - ./license.key:/opt/graviteeio-management-api/license/license.key
          - ./apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext
        environment:
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
          - gravitee_installation_standalone_portal_url=http://localhost:8085
          - gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
          - gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
          - gravitee_integration_enabled=true
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
        networks:
          - frontend
    ```
6.  Run Docker Compose with the following command:



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

### Verification <a href="#verification" id="verification"></a>

* To open the APIM Console, go to `http://localhost:8084`. The default username and password are both `admin`.
* To open the Developer Portal, go to `http://localhost:8085`. The default username and password are both `admin`.

## Enable Federation <a href="#enable-federation" id="enable-federation"></a>

Federation is disabled by default for security and performance reasons. You can enable Federation by adding environment variables to your existing Docker Compose configuration. If you plan to run multiple APIM instances for high availability, configure cluster mode using Hazelcast to ensure data synchronization across all instances.

To enable Federation, complete the following steps:

* [Enable Federation with Docker Compose](https://documentation.gravitee.io/apim/~/changes/324/self-hosted-installation-guides/docker/docker-compose#enable-federation-with-docker-compose)
* If you are running multiple replicas of APIM for high availability, [Set up cluster mode](https://documentation.gravitee.io/apim/~/changes/324/self-hosted-installation-guides/docker/docker-compose#set-up-cluster-mode)

### Enable Federation with Docker Compose <a href="#enable-federation-with-docker-compose" id="enable-federation-with-docker-compose"></a>

To use Federation, you need to add an environment variable to the Management API section of your `docker-compose-apim.yml` file, and then restart the service.

{% hint style="warning" %}
**Docker-specific requirements for Federation:**

* **Container naming**: Do NOT use underscores (\_) in container names for the Management API. For example, use `managementapi` or `mgmtapi` instead of `mgmt_api`. Underscores in container names can cause connectivity issues with federation agents.
* **Port exposure**: The Management API exposes port 8072 for federation agent WebSocket connections. This port must be accessible to federation agents running in the same Docker network.
{% endhint %}

To enable Federation, complete the following steps:

1. Open your existing `docker-compose-apim.yml` file and locate the `management_api` service section.
2.  Add the Federation environment variable `GRAVITEE_INTEGRATION_ENABLED=true` to the environment section of the Management API service. This activates the Federation endpoints in the Management API.



    ```yaml
    management_api:
        image: graviteeio/apim-management-api:4.8.0-debian
        container_name: mgmtapi
        restart: always
        ports:
          - "8083:8083"
          - "8072:8072"  # Federation WebSocket port for agents
        depends_on:
          mongodb:
            condition: service_healthy
          elasticsearch:
            condition: service_started
        environment:
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
          - gravitee_installation_standalone_portal_url=http://localhost:8085
          - gravitee_license=/opt/graviteeio-management-api/license/license.key
          - gravitee_plugins_path_0=$${gravitee.home}/plugins
          - gravitee_plugins_path_1=$${gravitee.home}/plugins-ext
          ## Federation is enabled
          - gravitee_integration_enabled=true 
        networks:
          - storage
          - frontend
        volumes:
          - ./.logs/apim-management:/opt/graviteeio-management-api/logs
          - ./.license/license.key:/opt/graviteeio-management-api/license/license.key
          - ./.plugins:/opt/graviteeio-management-api/plugins-ext
    ```
3.  Restart your APIM services. \


    ```bash
    docker compose -f docker-compose-apim.yml down
    ```

{% hint style="success" %}
Docker containers read environment variables only during container startup. The running containers cannot detect the new `GRAVITEE_INTEGRATION_ENABLED` setting without a restart.
{% endhint %}

4.  Start the services with the updated Federation configuration.\


    ```bash
    docker compose -f docker-compose-apim.yml up -d
    ```

### Configure Federation Agent <a href="#configure-federation-agent" id="configure-federation-agent"></a>

1. When running federation agents in Docker alongside your APIM deployment,configure the agent to connect to your Management API. To configure the agent environment, create a `.env` file for your federation agent with the following configuration. The following configuration example is for Confluent Platform integration:&#x20;

```bash
## GRAVITEE PARAMETERS ##
WS_ENDPOINTS=http://<container_name>:8072
WS_AUTH_TOKEN=your-auth-token-here
INTEGRATION_ID=your-integration-id-here
WS_ORG_ID=DEFAULT

## AWS API GATEWAY PARAMETERS ##
AWS_REGION=<your-aws-region>
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>

## LOGGING ##
LOG_LEVEL=DEBUG

## For Confluent Platform integration (uncomment if using Confluent):
# CLUSTER_API_ENDPOINT=http://rest-proxy:8082
# SCHEMA_REGISTRY_ENDPOINT=http://schema-registry:8081
# BASIC_AUTH_LOGIN=superUser
# BASIC_AUTH_PASSWORD=superUser
# TRUST_ALL=true

## For Solace integration (uncomment if using Solace):
# SOLACE_HOST=tcp://solace:55555
# SOLACE_USERNAME=admin
# SOLACE_PASSWORD=admin
# SOLACE_VPN=default
```

* WS\_ENDPOINTS: Replace `<container_name>` with your Management API container name. The port `8072` is used for WebSocket communication between the agent and the Management API.
* WS\_AUTH\_TOKEN: Obtain this token from the Gravitee Console when creating a service account for the federation agent.
* INTEGRATION\_ID: This is generated when you create an integration in the Gravitee Console.
* Container networking: Ensure your federation agent containers are on the same Docker network as your Management API to allow communication via container name resolution.

{% hint style="info" %}
This example shows configuration for Confluent Platform integration. For Solace or AWS API Gateway integrations, the core Gravitee parameters remain the same, but additional integration-specific parameters will differ.
{% endhint %}



2.  To enable federation, add the federation agent service to your `docker-compose-apim.yml` file. You can see a sample configuration example in the complete Docker Compose file above with all available agent options. \


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
        container_name: mgmtapi
        restart: always
        ports:
          - "8083:8083"
          - "8072:8072"  # Federation WebSocket port
        links:
          - mongodb
          - elasticsearch
        depends_on:
          - mongodb
          - elasticsearch
        volumes:
          - ./license.key:/opt/graviteeio-management-api/license/license.key
          - ./apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext
        environment:
          - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
          - gravitee_installation_standalone_portal_url=http://localhost:8085
          - gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins
          - gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext
          
          # FEDERATION CONFIGURATION - REQUIRED FOR FEDERATION TO WORK
          - gravitee_integration_enabled=true
          - gravitee_exchange_controller_enabled=true
          - gravitee_exchange_controller_ws_enabled=true
          - gravitee_exchange_controller_ws_port=8072
          - gravitee_exchange_controller_ws_host=0.0.0.0
          
          # Enable federation agent support
          - gravitee_federation_agent_enabled=true
          
        networks:
          - storage
          - frontend

      # Federation Agent Configuration
      # Select the correct agent image for your integration type:
      # * AWS API Gateway: graviteeio/federation-agent-aws-api-gateway:latest
      # * Confluent Platform: graviteeio/federation-agent-confluent-platform:latest
      # * Solace: graviteeio/federation-agent-solace:latest
      federation_agent:
        image: graviteeio/federation-agent-aws-api-gateway:latest
        container_name: gravitee_federation_agent
        restart: always
        environment:
          # WebSocket connection configuration
          - gravitee_integration_connector_ws_endpoints_0=${WS_ENDPOINTS}
          - gravitee_integration_connector_ws_headers_0_name=Authorization
          - gravitee_integration_connector_ws_headers_0_value=bearer ${WS_AUTH_TOKEN}
          
          # Provider configuration
          - gravitee_integration_providers_0_type=aws-api-gateway
          - gravitee_integration_providers_0_integrationId=${INTEGRATION_ID}
          - gravitee_integration_providers_0_configuration_accessKeyId=${AWS_ACCESS_KEY_ID}
          - gravitee_integration_providers_0_configuration_secretAccessKey=${AWS_SECRET_ACCESS_KEY}
          - gravitee_integration_providers_0_configuration_region=${AWS_REGION}
          - gravitee_integration_providers_0_configuration_acceptApiWithoutUsagePlan=true
          
          # Logging
          - GRAVITEE_LOG_LEVEL=${LOG_LEVEL}
        depends_on:
          - management_api
        networks:
          - frontend
          - storage

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
        networks:
          - frontend
    ```



3. Make the following modifications to your `docker-compose-apim.yml` file:

* Select the correct agent image for your integration type:
  * Confluent Platform: `graviteeio/federation-agent-confluent-platform:latest`
  * Solace: `graviteeio/federation-agent-solace:latest`
  * AWS API Gateway: `graviteeio/federation-agent-aws-api-gateway:latest`

### Set up cluster mode <a href="#set-up-cluster-mode" id="set-up-cluster-mode"></a>

If APIM is running with high availability, you need to set up cluster mode. To set up cluster mode, complete the following steps::

1.  Add the following parameter values to the root of your `gravitee.yaml` configuration file:



    ```bash
    GRAVITEE_CLUSTER_TYPE = hazelcast
    GRAVITEE_CLUSTER_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast-cluster.xml
    GRAVITEE_CACHE_TYPE = hazelcast
    GRAVITEE_CACHE_HAZELCAST_CONFIGPATH = ${gravitee.home}/config/hazelcast-cache.xml
    ```
2.  Mount a volume with the `hazelcast-cluster.xml` configuration file. This configures Hazelcast to support APIM cluster mode. Here is an example `hazelcast-cluster.xml` configuration file. You may need to customize the values for `join` in the `network` section:



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

       <queue name="integration-*">
            <backup-count>0</backup-count>
            <async-backup-count>1</async-backup-count>
            <empty-queue-ttl>300</empty-queue-ttl>
        </queue>

       <cp-subsystem>
           <cp-member-count>0</cp-member-count>
       </cp-subsystem>

       <network>
           <!-- CUSTOMIZE THIS JOIN SECTION --> 
           <port>5701</port>
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
3.  Mount a volume with the `hazelcast-cache.xml` configuration file. This configures the Hazelcast cluster that is used by APIM's caching system. Here is an example `hazelcast-cache.xml` configuration file. You may need to customize the values for `join` in the `network` section:



    ```xml
      <?xml version="1.0" encoding="UTF-8"?>
      <hazelcast xmlns="http://www.hazelcast.com/schema/config"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.hazelcast.com/schema/config
                 http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">
          <cluster-name>graviteeio-apim-cache</cluster-name>
          <properties>
              <property name="hazelcast.discovery.enabled">true</property>
              <property name="hazelcast.max.wait.seconds.before.join">3</property>
              <property name="hazelcast.member.list.publish.interval.seconds">5</property>
              <property name="hazelcast.socket.client.bind.any">false</property>
              <property name="hazelcast.logging.type">slf4j</property>
          </properties>

          <map name="integration-*">
              <backup-count>0</backup-count>
              <async-backup-count>1</async-backup-count>
          </map>

          <cp-subsystem>
              <cp-member-count>0</cp-member-count>
          </cp-subsystem>

          <network>
              <port>5702</port>
              <join>
                  <multicast enabled="false"/>
                  <tcp-ip enabled="true">
                      <interface>127.0.0.1</interface>
                  </tcp-ip>
              </join>
          </network>
      </hazelcast>
    ```
4. Add the following plugins to APIM:
   * https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip
   * https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip

[\
](https://documentation.gravitee.io/apim/~/changes/324/self-hosted-installation-guides/docker)
