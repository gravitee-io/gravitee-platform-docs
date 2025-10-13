# Configure and Deploy Kafka Console

## Overview

The Gravitee Kafka Console is a standalone application that integrates with APIM to provide a user interface for managing and monitoring Kafka clusters. It is based on Kafbat UI and communicates with the APIM Management API (mAPI) through JWT-based authentication.

The Kafka Console deployment requires coordination between the Management API, which must be configured to enable the Kafka Console integration, and the Kafka Console application, which runs as a separate service that connects to the mAPI.

This guide explains how to configure and deploy Kafka Console using either Docker Compose or the Gravitee Helm Chart.&#x20;

## Prerequisites

Before deploying Kafka Console, ensure the following criteria are met:

* Version **4.9.0-alpha.3** or later for APIM or the Gravitee Helm Chart, depending on your deployment method. The `4.9.0-alpha.3` tag is available in Azure Container Registry only. There is no `latest` tag for Kafka Console.
* An Enterprise license that includes the **apim-cluster** feature.
* Access to Gravitee's Azure Container Registry, `graviteeio.azurecr.io`, to use the Kafka Console image.
* The Kafka Console must be able to reach the Management API using the internal Docker network. Use service names, such as `mapi`, instead of `localhost`.
* A 32-character secret string for JWT token signing. The same secret must be used for the mAPI `gravitee_kafka_console_server_security_secret` and the Kafka Console `AUTH_JWT_SECRET`.
* If you are using SASL security protocols on ports 9095 and 9096, configure the cluster with:
  * **Security Protocol**: SASL\_PLAINTEXT or SASL\_SSL
  * **SASL Mechanism**: PLAIN
  * **Username**: As configured in your Kafka broker. For example, the reference setup uses `gravitee_user`.
  * **Password**: As configured in your Kafka broker. For example, the reference setup uses `gravitee_password`.

## Deploy Kafka Console

### Deploy with Docker Compose

To deploy the Kafka Console using Docker Compose, complete the following steps.

1.  Before pulling the Kafka Console image, run the following commands to authenticate with Azure Container Registry:

    ```bash
    az login
    az acr login -n graviteeio.azurecr.io
    ```
2.  Configure the mAPI service in your `docker-compose.yml` by adding the following environment variables:

    ```yaml
    management_api:
      image: graviteeio/apim-management-api:4.9.0-alpha.3
      environment:
        - gravitee_kafka_console_enabled=true
        - gravitee_kafka_console_server_host=kafkaConsole
        - gravitee_kafka_console_server_port=8080
        - gravitee_kafka_console_server_security_secret=YOUR_32_CHARACTER_SECRET
      networks:
        - kafkaConsole
    ```
3.  Add the Kafka Console service to your `docker-compose.yml` using the following configuration:

    ```yaml
    kafkaConsole:
      image: graviteeio.azurecr.io/apim-kafka-console:4.9.0-alpha.3
      container_name: gio_apim_kafka_console
      networks:
        - kafkaConsole
      depends_on:
        - management_api
      links:
        - management_api:mapi
      environment:
        - AUTH_JWT_SECRET=YOUR_32_CHARACTER_SECRET
        - KAFKA_GRAVITEE_MANAGEMENTAPIURL=http://mapi:8083/management/v2/organizations/DEFAULT/environments/DEFAULT
        - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINUSERNAME=admin
        - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINPASSWORD=admin
    ```



    {% hint style="info" %}
    You can authenticate the Kafka Console to the mAPI using either of the following options. The authenticating user must have Organization Admin privileges.

    *   Basic Authentication (shown above):

        ```yaml
        - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINUSERNAME=admin
        - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINPASSWORD=admin
        ```
    *   Personal Access Token:

        ```yaml
        - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINTOKEN=your_personal_access_token
        ```
    {% endhint %}
4.  Ensure your `docker-compose.yml`  configures the following dedicated network for Kafka Console communication:

    ```yaml
    networks:
      kafkaConsole:
        name: kafkaConsole
    ```
5.  Start your Docker Compose stack with the correct APIM version by running the following command:

    ```bash
    APIM_VERSION=4.9.0-alpha.3 docker compose up -d
    ```

<details>

<summary>Complete Docker Compose example</summary>

The following `docker-compose.yml` is a complete working example of the full APIM stack with Kafka Console integration. It includes all necessary services: MongoDB, Elasticsearch, APIM components, Kafka broker, and Kafka Console.

```yaml
#
# Copyright © 2015 The Gravitee team (http://gravitee.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

networks:
  frontend:
    name: frontend
  storage:
    name: storage
  kafka:
    name: kafka
  email:
    name: email
  gateway:
    name: gateway
  kafkaConsole:
    name: kafkaConsole

volumes:
  data-elasticsearch:
  data-mongo:
  data-kafka: null

services:
  mongodb:
    image: mongo:${MONGODB_VERSION:-6.0}
    container_name: gio_apim_mongodb
    restart: always
    volumes:
      - data-mongo:/data/db
      - ./.logs/apim-mongodb:/var/log/mongodb
    healthcheck:
      test: mongosh --eval 'db.runCommand({serverStatus:1}).ok' --quiet | grep 1
      interval: 5s
      timeout: 3s
      retries: 10
    networks:
      - storage

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION:-8.17.2}
    container_name: gio_apim_elasticsearch
    restart: always
    volumes:
      - data-elasticsearch:/usr/share/elasticsearch/data
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
    healthcheck:
      test:
        [
          "CMD",
          "curl",
          "-f",
          "http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s",
        ]
      interval: 5s
      timeout: 3s
      retries: 10
    networks:
      - storage

  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-latest}
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
      - "9092:9092"
    depends_on:
      mongodb:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    volumes:
      - ./.logs/apim-gateway:/opt/graviteeio-gateway/logs
      - ./.license:/opt/graviteeio-gateway/license
      - ./.ssl:/opt/graviteeio-gateway/ssl
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_ratelimit_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
    networks:
      storage:
      frontend:
      kafka:
      gateway:

  management_api:
    image: graviteeio/apim-management-api:${APIM_VERSION:-latest}
    container_name: gio_apim_management_api
    restart: always
    ports:
      - "8083:8083"
    links:
      - mongodb
      - elasticsearch
    depends_on:
      mongodb:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    volumes:
      - ./.logs/apim-management-api:/opt/graviteeio-management-api/logs
      - ./.license:/opt/graviteeio-management-api/license
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
      - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
      - gravitee_email_enabled=true
      - gravitee_email_host=mailhog
      - gravitee_email_port=1025
      - gravitee_email_subject="TEST"
      - gravitee_email_from="user@my.domain"
      - gravitee_kafka_console_enabled=true
      - gravitee_kafka_console_server_host=kafkaConsole
      - gravitee_kafka_console_server_port=8080
      - gravitee_kafka_console_server_security_secret=TCkyfrr8F6c75mAGKpRtKPaBHt9LyJ7P
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "code=$$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8083/management/health || echo 000); if [ \"$$code\" = \"200\" ] || [ \"$$code\" = \"401\" ]; then exit 0; else exit 1; fi",
        ]
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 45s
    networks:
      - storage
      - frontend
      - email
      - kafkaConsole

  management_ui:
    image: graviteeio/apim-management-ui:${APIM_VERSION:-latest}
    container_name: gio_apim_management_ui
    restart: always
    ports:
      - "8084:8080"
    depends_on:
      - management_api
    environment:
      - MGMT_API_URL=http://localhost:8083/management/
    volumes:
      - ./.logs/apim-management-ui:/var/log/nginx
    networks:
      - frontend

  portal_ui:
    image: graviteeio/apim-portal-ui:${APIM_VERSION:-latest}
    container_name: gio_apim_portal_ui
    restart: always
    ports:
      - "8085:8080"
    depends_on:
      - management_api
    environment:
      - PORTAL_API_URL=http://localhost:8083/portal
    volumes:
      - ./.logs/apim-portal-ui:/var/log/nginx
    networks:
      - frontend

  mailhog:
    image: mailhog/mailhog
    container_name: gio_apim_mailhog
    restart: always
    ports:
      - "8025:8025"
      - "1025:1025"
    networks:
      - email

  kafkaConsole:
    image: graviteeio.azurecr.io/apim-kafka-console:4.9.0-alpha.3
    container_name: gio_apim_kafka_console
    networks:
      - kafkaConsole
    depends_on:
      management_api:
        condition: service_healthy
    links:
      - management_api:mapi
    environment:
      - AUTH_JWT_SECRET=TCkyfrr8F6c75mAGKpRtKPaBHt9LyJ7P
      - KAFKA_GRAVITEE_MANAGEMENTAPIURL=http://mapi:8083/management/v2/organizations/DEFAULT/environments/DEFAULT
      - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINUSERNAME=admin
      - KAFKA_GRAVITEE_MANAGEMENTAPIORGADMINPASSWORD=admin

  kafka:
    image: docker.io/bitnamilegacy/kafka:3.9
    container_name: gio_apim_kafka
    volumes:
      - data-kafka:/bitnami/kafka
      - "./.ssl/server.keystore.jks:/bitnami/kafka/config/certs/kafka.keystore.jks:ro"
      - "./.ssl/server.truststore.jks:/bitnami/kafka/config/certs/kafka.truststore.jks:ro"
    ports:
      - "9091:9091"
      - "9093:9093"
      - "9094:9094"
      - "9095:9095"
      - "9096:9096"
      - "9097:9097"
    networks:
      - kafka
      - kafkaConsole
    environment:
      - BITNAMI_DEBUG=true
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@localhost:9093
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9091,CONTROLLER://:9093,SSL://:9094,SASL_PLAINTEXT://:9095,SASL_SSL://:9096,KAFDROP://:9097
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9091,SSL://kafka:9094,SASL_PLAINTEXT://kafka:9095,SASL_SSL://kafka:9096,KAFDROP://kafka:9097
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL,KAFDROP:PLAINTEXT,CONTROLLER:PLAINTEXT
      - KAFKA_CFG_SASL_MECHANISM_INTER_BROKER_PROTOCOL=PLAIN
      - KAFKA_NUM_PARTITIONS=1
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
      # SASL settings
      - KAFKA_CLIENT_USERS=gravitee_user
      - KAFKA_CLIENT_PASSWORDS=gravitee_password
      - KAFKA_CONTROLLER_USER=controller_user
      - KAFKA_CONTROLLER_PASSWORD=controller_password
      - KAFKA_INTER_BROKER_USER=inter_broker_user
      - KAFKA_INTER_BROKER_PASSWORD=inter_broker_password
      # Certificate credentials
      - KAFKA_CFG_SSL_KEYSTORE_LOCATION=/opt/bitnami/kafka/config/certs/kafka.keystore.jks
      - KAFKA_CFG_SSL_KEYSTORE_PASSWORD=gravitee
      - KAFKA_CFG_SSL_TRUSTSTORE_LOCATION=/opt/bitnami/kafka/config/certs/kafka.truststore.jks
      - KAFKA_CFG_SSL_TRUSTSTORE_PASSWORD=gravitee
      - KAFKA_TLS_CLIENT_AUTH=requested
      - KAFKA_CERTIFICATE_PASSWORD=gravitee
      - KAFKA_TLS_TYPE=JKS
      - KAFKA_CFG_SSL_ENDPOINT_IDENTIFICATION_ALGORITHM=
    healthcheck:
      test: ["CMD", "bash", "-c", "echo > /dev/tcp/localhost/9097"]
      interval: 5s
      timeout: 10s
      retries: 5
      start_period: 10s
```

* This example uses `bitnamilegacy/kafka:3.9`. Standard `bitnami/kafka` has moved to the legacy repository.
* Replace the JWT secret `TCkyfrr8F6c75mAGKpRtKPaBHt9LyJ7P` with your own 32-character secret.
* Replace the included SSL certificates mounted from `./.ssl/` directory with your own.
* The OAuth/OIDC configuration points to an internal Gravitee test environment. Adjust this for your setup.
* Launch with `APIM_VERSION=4.9.0-alpha.3 docker compose up -d`.

</details>

### Deploy with the Gravitee Helm Chart

To deploy the Kafka Console using the Gravitee Helm Chart, complete the following steps.

{% hint style="warning" %}
There is a bug in `4.9.0-alpha.3` that requires adding the JWT secret to both the `api` section and the `kafkaConsole` section. This redundancy will be fixed in future releases.
{% endhint %}

1.  Add the following Kafka Console configuration to your Helm `values.yml` file:

    ```yaml
    api:
      env:
        - name: gravitee_kafka_console_server_security_secret
          value: YOUR_32_CHARACTER_SECRET

    kafkaConsole:
      name: kafka-console
      image:
        repository: graviteeio.azurecr.io/apim-kafka-console
        tag: 4.9.0-alpha.3
      enabled: true
      jwt:
        secret: YOUR_32_CHARACTER_SECRET
      apim:
        security:
          token: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```



    {% hint style="info" %}
    Instead of using a Personal Access Token, you can use basic authentication like in the following example:

    ```yaml
    kafkaConsole:
      # ... other configuration ...
      apim:
        security:
          username: admin
          password: your_password
    ```
    {% endhint %}
2.  (Optional) Specify your custom `organization` and `environment` IDs to override the default Kafka Console connections to the `DEFAULT` organization and `DEFAULT` environment:

    ```yaml
    kafkaConsole:
      # ... other configuration ...
      apim:
        organization: YOUR_ORG_ID
        environment: YOUR_ENV_ID
    ```
3.  Deploy or upgrade your Helm release:

    ```bash
    helm upgrade --install gravitee-apim gravitee/apim \
      --version 4.9.0-alpha.3 \
      -f values.yml
    ```

## Enable Kafka Console

The Kafka Console feature must be explicitly enabled. Use one of the following options to enable Kafka Console:

*   Environment variable:

    ```bash
    GRAVITEE_KAFKA_CONSOLE_ENABLED=true
    ```
*   `gravitee.yml` configuration:

    ```yaml
    kafka:
      console:
        enabled: true
    ```
*   Helm values:

    ```yaml
    kafkaConsole:
      enabled: true
    ```

## Access Kafka Console

To Access Kafka Console, complete the following steps:

1. Sign in to the APIM Console.
2. Navigate to **Kafka Clusters** in the left menu.
3. Click the **Open Kafka Console** button at the top of the page.

The Console opens in a new tab. JWT-based authentication is handled automatically.

## Known Limitations

Kafka Console is subject to the following known limitations:

* **Cluster list refresh**: The Kafka Console fetches the list of available clusters only at startup. After you create a new cluster in APIM Console, you must restart the Kafka Console pod or container for it to appear. Use the restart method appropriate to your deployment:
  * Docker Compose: `docker compose restart kafkaConsole`
  * Helm/Kubernetes: `kubectl rollout restart deployment/kafka-console`
  * Production/hybrid deployments: Contact your platform team or submit a support ticket
* **File-based user bug**: There is a known issue when adding file-based users from `gravitee.yml` to cluster permissions. This does not affect deployments that use external user management systems such as LDAP or OAuth.
* **Read-only mode**: The alpha version provides read-only access to Kafka clusters. Message publishing and topic management capabilities are not included in this release.

## Troubleshooting

<details>

<summary>JWT signature validation error</summary>

**Symptom**: Error message `JWT signature does not match locally computed signature`.

**Solution**: Verify that the mAPI and Kafka Console JWT secrets are an exact match.

* Management API: `gravitee_kafka_console_server_security_secret`
* Kafka Console: `AUTH_JWT_SECRET`

</details>

<details>

<summary>Cannot connect to Kafka cluster</summary>

**Symptom**: Connection timeout or "node -1 could not be established" errors.

**Solution**:

1. Verify you are using Docker service names, such as `kafka:9091`, instead of `localhost`.
2. Ensure the Kafka Console service is connected to the same Docker network as your Kafka broker.
3. Check that the Kafka broker is healthy and accepting connections.

</details>

<details>

<summary>"Open Kafka Console" button not visible</summary>

**Symptom**: The button does not appear in the APIM Console.

**Solution**:

1. Verify `gravitee_kafka_console_enabled=true` is set in Management API environment variables.
2. Restart the Management API container/pod.
3. Clear your browser cache and reload the APIM Console.

</details>

## Additional resources

* For detailed information about using the Kafka Console UI features, refer to the official [Kafbat UI Documentation](https://ui.docs.kafbat.io/).
* For information about creating and configuring Kafka clusters in APIM Console, see [Create and Configure Kafka Clusters](create-and-configure-kafka-clusters.md).
