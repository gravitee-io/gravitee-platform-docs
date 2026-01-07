---
description: Documentation about docker cli in the context of APIs.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/self-hosted-installation-guides/docker/docker-cli
---

# Docker CLI

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

* You must install Docker. For more information about installing Docker, go to [Install Docker Engine](https://docs.docker.com/engine/install/).
* If you are using the Enterprise Edition (EE) of Gravitee, ensure that you have a licensing key. If you do not know your licensing key, see the [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

### Install Gravitee APIM <a href="#install-gravitee-apim" id="install-gravitee-apim"></a>

1. Create a directory structure in which to persist data and store plugins:
   1.  Create a directory structure using the following command:

       ```shellscript
       mkdir -p /gravitee/{mongodb/data,elasticsearch/data,apim-gateway/plugins,apim-gateway/logs,apim-management-api/plugins,apim-management-api/logs,apim-management-ui/logs,apim-portal-ui/logs}
       ```
   2.  Once you create the directory, verify that the directory has the following structure:

       ```shellscript
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
2. (Optional) If you are installing the Enterprise Edition (EE) of Gravitee APIM, copy your license key to `/gravitee/license.key`.
3.  Create two Docker bridge networks using the following commands:

    ```shellscript
    docker network create storage
    docker network create frontend
    ```
4.  Install MongoDB using the following commands:

    ```shellscript
    docker pull mongo:7.0
    docker run --name gio_apim_mongodb \
      --net storage \
      --volume /gravitee/mongodb/data:/data/db \
      --detach mongo:7.0
    ```
5.  Install Elasticsearch using the following commands:

    ```shellscript
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.16.1

    docker run --name gio_apim_elasticsearch \
      --net storage \
      --hostname elasticsearch \
      --env http.host=0.0.0.0 \
      --env transport.host=0.0.0.0 \
      --env xpack.security.enabled=false \
      --env cluster.name=elasticsearch \
      --env bootstrap.memory_lock=true \
      --env discovery.type=single-node \
      --env "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
      --ulimit memlock=-1:-1 \
      --ulimit nofile=65536:65536 \
      --volume /gravitee/elasticsearch/data:/var/lib/elasticsearch/data \
      --detach docker.elastic.co/elasticsearch/elasticsearch:8.16.1
    ```
6.  Install the API Gateway using the following commands. If you use the Community Edition (CE) of Gravitee APIM, remove the following line: `--volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key`.

    ```shellscript
    docker pull graviteeio/apim-gateway:latest

    docker run --publish 8082:8082 \
      --volume /gravitee/apim-gateway/plugins:/opt/graviteeio-gateway/plugins-ext \
      --volume /gravitee/apim-gateway/logs:/opt/graviteeio-gateway/logs \
      --volume /gravitee/license.key:/opt/graviteeio-gateway/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_ratelimit_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_reporters_elasticsearch_endpoints_0="http://gio_apim_elasticsearch:9200" \
      --env gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext \
      --net storage \
      --name gio_apim_gateway \
      --detach graviteeio/apim-gateway:latest

    docker network connect frontend gio_apim_gateway
    ```
7.  Install the Management API using the following commands. If you are installing the CE of Gravitee, remove the following line: `--volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key` .

    ```shellscript
    docker pull graviteeio/apim-management-api:latest

    docker run --publish 8083:8083 \
      --publish 8072:8072 \
      --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
      --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
      --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://gio_apim_elasticsearch:9200" \
      --env gravitee_installation_standalone_portal_url="http://localhost:8085" \
      --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
      --net storage \
      --name mgmtapi \
      --detach graviteeio/apim-management-api:latest

    docker network connect frontend mgmtapi
    ```

{% hint style="success" %}
Port 8072 is exposed for federation agent WebSocket connections. This port is required if you plan to use Federation features with agents.
{% endhint %}

8.  Install the Console using the following commands:

    ```shellscript
    docker pull graviteeio/apim-management-ui:latest

    docker run --publish 8084:8080 \
      --volume /gravitee/apim-management-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_management_ui \
      --env MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/ \
      --detach graviteeio/apim-management-ui:latest
    ```
9.  Install the Developer portal using the following commands:

    ```shellscript
    docker pull graviteeio/apim-portal-ui:latest

    docker run --publish 8085:8080 \
      --volume /gravitee/apim-portal-ui/logs:/var/log/nginx \
      --net frontend \
      --name gio_apim_portal_ui \
      --env PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT \
      --detach graviteeio/apim-portal-ui:latest
    ```

{% hint style="info" %}
* MongoDB is on the `storage` network and uses `/gravitee/mongodb` for persistent storage.
* Elasticsearch is on the `storage` network and uses `/gravitee/elasticsearch` for persistent storage.
* The API Gateway is on both the `storage` and `frontend` networks and uses `/gravitee/apim-gateway` for persistent storage.
* The Management API is on both the `storage` and `frontend`networks, and uses the `/gravitee/apim-api` for persistent storage.
* The Console is on the `frontend` network and uses `/graviee/apim-management-ui` for persistent storage.
* The Developer Portal is on the `frontend` network and uses `/gravitee/apim-portal-ui` for persistent storage.
{% endhint %}

### Verification <a href="#verification" id="verification"></a>

* To open the APIM Console, go to `http://localhost:8084`. The default username and password are both `admin`.
* To open the Developer Portal, go to `http://localhost:8085`. The default username and password are both `admin`.

### Enable Federation <a href="#enable-federation" id="enable-federation"></a>

Federation is disabled by default for security and performance reasons. You can enable Federation by adding environment variables to your existing Docker CLI configuration. If you plan to run multiple APIM instances for high availability, configure cluster mode using Hazelcast to ensure data synchronization across all instances.

To enable Federation, complete the following steps:

* [#enable-federation-with-docker-cli](docker-cli.md#enable-federation-with-docker-cli "mention")
* If you are running multiple replicas of APIM for high availability, [#set-up-cluster-mode](docker-cli.md#set-up-cluster-mode "mention")

#### Enable Federation with Docker CLI <a href="#enable-federation-with-docker-cli" id="enable-federation-with-docker-cli"></a>

To use Federation, you need to add an environment variable to the Management API section in your Docker CLI command, and then restart the service.

To enable Federation, complete the following steps:

1.  Stop and Remove Existing Management API Container with the following command:

    ```bash
    docker stop mgmtapi

    docker rm mgmtapi
    ```
2.  Restart management API with Federation enabled with the following command:

    ```bash
    docker run --publish 8083:8083 \
      --publish 8072:8072 \
      --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
      --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
      --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://gio_apim_elasticsearch:9200" \
      --env gravitee_installation_standalone_portal_url="http://localhost:8085" \
      --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
      --env gravitee_integration_enabled=true \ # activates federation
      --net storage \
      --name mgmtapi \
      --detach graviteeio/apim-management-api:latest
    ```
3.  Reconnect to the frontend network using the following command:

    ```bash
    docker network connect frontend mgmtapi
    ```

**Configure Federation Agent**

When running federation agents in Docker alongside your APIM deployment, you need to configure the agent to connect to your Management API. To configure the agent environment, create a `.env` file for your federation agent with the appropriate configuration for your integration type. For example, this configuration below is for Confluent Platform integration:

```bash
## GRAVITEE PARAMETERS ##
WS_ENDPOINTS=http://<container_name>:8072
WS_AUTH_TOKEN=your-auth-token-here
INTEGRATION_ID=your-integration-id-here
WS_ORG_ID=DEFAULT

# Additional configuration may be required based on your integration type
# Example for Confluent Platform integration:
CLUSTER_API_ENDPOINT=http://rest-proxy:8082
SCHEMA_REGISTRY_ENDPOINT=http://schema-registry:8081
BASIC_AUTH_LOGIN=superUser
BASIC_AUTH_PASSWORD=superUser
TRUST_ALL=true
```

Make the following modificatinos to your `.env` file above:

* `WS_ENDPOINTS`: Uses `mgmtapi:8072` (the container name without underscores and port 8072)
* `WS_AUTH_TOKEN`: Obtain from Gravitee Console when creating a service account for the federation agent
* `INTEGRATION_ID`: Generated when you create an integration in the Gravitee Console
* Container networking: Ensure your federation agent containers are on the same Docker network as your Management API

**Verify Federation Agent**

1. Run the federation agent using the following command:

```bash
docker pull graviteeio/federation-agent-confluent-platform:latest
docker run --name gravitee_federation_agent \
  --env-file .env \
  --net frontend \
  --detach graviteeio/federation-agent-confluent-platform:latest
```

#### Set up cluster mode <a href="#set-up-cluster-mode" id="set-up-cluster-mode"></a>

If APIM is running with high availability, you need to set up cluster mode. To set up cluster mode, complete the following steps:

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
              xsi:schemaLocation="http://www.haze\lcast.com/schema/config
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
    ?xml version="1.0" encoding="UTF-8"?>
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
                    <tcp-ip enabled="true">       </join>
            </network>
        </hazelcast>
    ```
4.  Apply the settings using the `docker run` command:

    ```shellscript
    # For Management API with cluster mode:
    docker run --publish 8083:8083 \
      --publish 8072:8072 \
      --volume /gravitee/apim-management-api/plugins:/opt/graviteeio-management-api/plugins-ext \
      --volume /gravitee/apim-management-api/logs:/opt/graviteeio-management-api/logs \
      --volume /gravitee/license.key:/opt/graviteeio-management-api/license/license.key \
      --volume /path/to/hazelcast-cluster.xml:/opt/graviteeio-management-api/config/hazelcast-cluster.xml \
      --volume /path/to/hazelcast-cache.xml:/opt/graviteeio-management-api/config/hazelcast-cache.xml \
      --env gravitee_management_mongodb_uri="mongodb://gio_apim_mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000" \
      --env gravitee_analytics_elasticsearch_endpoints_0="http://gio_apim_elasticsearch:9200" \
      --env gravitee_installation_standalone_portal_url="http://localhost:8085" \
      --env gravitee_plugins_path_0=/opt/graviteeio-management-api/plugins \
      --env gravitee_plugins_path_1=/opt/graviteeio-management-api/plugins-ext \
      --env gravitee_integration_enabled=true \
      --env GRAVITEE_CLUSTER_TYPE=hazelcast \
      --env GRAVITEE_CLUSTER_HAZELCAST_CONFIGPATH=/opt/graviteeio-management-api/config/hazelcast-cluster.xml \
      --env GRAVITEE_CACHE_TYPE=hazelcast \
      --env GRAVITEE_CACHE_HAZELCAST_CONFIGPATH=/opt/graviteeio-management-api/config/hazelcast-cache.xml \
      --net storage \
      --name mgmtapi \
      --detach graviteeio/apim-management-api:latest
    ```
5. Add the following plugins to APIM:
   * https://download.gravitee.io/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-5.18.1.zip
   * https://download.gravitee.io/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-5.18.1.zip
