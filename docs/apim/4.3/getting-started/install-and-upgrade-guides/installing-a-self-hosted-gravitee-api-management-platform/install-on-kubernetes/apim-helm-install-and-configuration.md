---
description: >-
  This article covers how to install and configure APIM with Gravitee's official
  Helm chart
---

# APIM Helm Install and Configuration

## Introduction

This page describes how to install APIM on any Kubernetes environment using our official Helm Chart:

* [Installation](apim-helm-install-and-configuration.md#installation)

The Helm Chart is designed to be flexible and can be deployed on various Kubernetes distributions, including but not limited to AKS and OpenShift.

Additionally, the Helm Chart supports a variety of configuration types and database options. Gravitee Helm Chart parameters, default values, and other configuration details are summarized in the following sections:

* [Application settings](apim-helm-install-and-configuration.md#application-settings)
* [Configuration types](apim-helm-install-and-configuration.md#configuration-types)
* [Database options](apim-helm-install-and-configuration.md#database-options)
* [Gravitee parameters](apim-helm-install-and-configuration.md#gravitee-parameters)
* [OpenShift](apim-helm-install-and-configuration.md#openshift)
* [Licenses](apim-helm-install-and-configuration.md#licences)

## Installation

### Prerequisites

The following command line tools must be installed:

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [Helm v3](https://helm.sh/docs/intro/install/)

### Installation steps

1.  Add the Gravitee Helm Chart repo:

    ```sh
    helm repo add graviteeio https://helm.gravitee.io
    ```
2.  Install the chart from the Helm repo specifying the desired release, e.g., `graviteeio-apim4x` in the example below. The chart can be installed into either the default namespace or a dedicated namespace.

    {% hint style="warning" %}
    **Dedicated namespace**

    To prevent potential issues, it is best practice to create a separate namespace for your installation and avoid using the default Kubernetes namespace. This is not mandatory, but the installation command below follows this recommendation.
    {% endhint %}

    *   **Dedicated namespace:** To install the Helm Chart using a dedicated namespace (e.g., `gravitee-apim`), run the following command:

        {% code overflow="wrap" %}
        ```sh
        helm install graviteeio-apim4x graviteeio/apim --create-namespace --namespace gravitee-apim
        ```
        {% endcode %}
    *   **Default namespace:** To install the Helm Chart using the default namespace (not recommended), run the following command:

        ```sh
        helm install graviteeio-apim4x graviteeio/apim
        ```

    {% hint style="info" %}
    **Installation tips**

    Specify each parameter using `helm install` and the `--set key=value[,key=value]`.

    Alternatively, provide a YAML file that specifies the values for the parameters when installing the chart. For example:

    ```sh
    helm install my-release -f values.yaml gravitee
    ```

    By default, APIM uses the values in the `values.yml` config file during installation. These can be modified via the parameters in the [configuration](apim-helm-install-and-configuration.md) tables.
    {% endhint %}
3.  (Optional) Alternatively, you can package this chart directory into a chart archive:

    ```sh
    helm package .
    ```

    To install the chart using the chart archive, run:

    ```sh
    helm install apim-4.0.0.tgz
    ```

## Application settings

By default, the Helm Chart creates a ServiceAccount that enables Gravitee API Management (APIM) to connect to the Kubernetes API. This allows Kubernetes ConfigMaps and Secrets to initialize Gravitee settings.

[Roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole) enable use of the service account:

* By default, the service account created does not have a cluster role.
* The Helm Chart includes an option to configure the service account to use a cluster role.
* To access a Secret, create a role within your namespace.
* To deploy in another namespace from which you will access a Secret, create a another role in that namespace. The two roles can have the same name but are completely separate objects. Each role only provides access to the namespace in which it is created.

Application settings must be defined as follows:

*   Secret settings: `secrets://kubernetes/mysecret:key?namespace=ns`, with the kube plugin enabled via `secrets.kubernetes.enabled=true`

    {% hint style="warning" %}
    The above syntax applies to Gravitee versions 4.2 and later
    {% endhint %}
* ConfigMap settings: `kubernetes://<namespace>/configmaps/<my-configmap-name>/<my-configmap-key>`

For example, the MongoDB URI initialized from the `mongo` Secret deployed in the `default` namespace is defined as:

```
mongo:
  uri: kubernetes://default/secrets/mongo/mongouri
```

## **Configuration types**

DB-less mode, development deployment, external, and shared configuration types are described in detail below.

{% tabs %}
{% tab title="DB-less mode" %}
DB-less mode allows a Gateway to be deployed with no dependencies, assuming only that there is an operator running in the same cluster or namespace. Although the setup does not include Elasticsearch or MongoDB, analytics can still be configured using a custom reporter such as Datadog, TCP with Logstash, etc.

Below is the minimum `value-dbless.yml` APIM configuration required by a DB-less deployment. Change the `domain` value and run the following command:

<pre><code><strong>helm install gravitee-apim graviteeio/apim -f values-dbless.yml
</strong></code></pre>

{% code title="values-dbless.yaml" %}
```yaml
api:
  enabled: false

portal:
  enabled: false

ui:
  enabled: false

es:
  enabled: false

ratelimit:
  type: none

gateway:
  replicaCount: 1
  autoscaling:
    enabled: false
  ingress:
    enabled: false
  image:
    repository: graviteeio/apim-gateway
    tag: 4.1
    pullPolicy: Always
  services:
    sync:
      kubernetes:
        enabled: true
  dbLess: true
  reporters:
    elasticsearch:
      enabled: false
```
{% endcode %}

{% hint style="info" %}
The above is just one example of a DB-less mode configuration. Note that if DB-less mode is configured without a running APIM instance to sync with, the `management-context`resource serves no purpose.
{% endhint %}
{% endtab %}

{% tab title="Dev deployment" %}
Below is the minimum `value-light.yml` configuration required by a development deployment. Change the `domain` value and run the following command:

{% hint style="warning" %}
Do not use `value-light.yml` in production.
{% endhint %}

<pre><code><strong>helm install gravitee-apim graviteeio/apim -f value-light.yml
</strong></code></pre>

```yaml
# Deploy an elasticsearch cluster.
elasticsearch:
  enabled: true

# Elasticsearch uri, do not change.
es:
  endpoints:
    - http://graviteeio-apim-elasticsearch-ingest-hl:9200

# Deploy a mongoDB cluster.
mongodb:
  enabled: true

# MongoDB uri, do not change.
mongo:
  uri: mongodb://graviteeio-apim-mongodb-replicaset-headless:27017/gravitee?replicaset=rs0&connectTimeoutMS=30000

# Change the ingress host with your host domain.
# no TLS provided here. Check the documentation if needed.
api:
  ingress:
    management:
      hosts:
        - management-api.mydomain.com
    portal:
      hosts:
        - management-api.mydomain.com

# Change the ingress host with your host domain.
# no TLS provided here. Check the documentation if needed.
gateway:
  ingress:
    hosts:
      - gateway.mydomain.com

# Change the ingress host with your host domain.
# no TLS provided here. Check the documentation if needed.
portal:
  ingress:
    hosts:
      - portal.mydomain.com

# Change the ingress host with your host domain.
# no TLS provided here. Check the documentation if needed.
ui:
  ingress:
    hosts:
      - management-ui.mydomain.com
```
{% endtab %}

{% tab title="External configuration" %}
To use an external configuration file, such as `gravitee.yaml` for the Gateway or API management, or `constant.json` for the UI, add the following to the Helm Chart (`gravitee-config-configmap-name` is the name of the ConfigMap that contains the external configuration file):

```yaml
extraVolumes: |
    - name: config
      configMap:
        name: gravitee-config-configmap-name
```

{% hint style="warning" %}
External configuration files are only available for:

* AE Helm Charts 1.1.42 and later
* AM Helm Charts 1.0.53 and later
* APIM Helm Charts 3.1.60 and later
{% endhint %}
{% endtab %}

{% tab title="Shared configuration" %}
To configure common features such as:

* Chaos testing: See [chaoskube](https://github.com/kubernetes/charts/tree/master/stable/chaoskube) chart
* Configuration database: See [mongodb](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) chart
* Logs database: See [elasticsearch](https://github.com/bitnami/charts/tree/master/bitnami/elasticsearch) chart

<table><thead><tr><th width="255">Parameter</th><th width="190">Description</th><th>Default</th></tr></thead><tbody><tr><td><code>chaos.enabled</code></td><td>Enable Chaos test</td><td>false</td></tr><tr><td><code>inMemoryAuth.enabled</code></td><td>Enable oauth login</td><td>true</td></tr><tr><td><code>ldap.enabled</code></td><td>Enable LDAP login</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## **Database options**

Gravitee supports MongoDB, PostgreSQL, Elasticsearch, and Redis configurations. Installation instructions and parameters are detailed below.

{% tabs %}
{% tab title="MongoDB" %}
To install MongoDB with Helm:

```
helm install mongodb bitnami/mongodb --set auth.rootPassword=r00t
```

**MongoDB connections**

There are three ways to configure MongoDB connections.

1. The simplest way is to provide the [MongoDB URI](https://docs.mongodb.com/manual/reference/connection-string/).

| Parameter   | Description | Default |
| ----------- | ----------- | ------- |
| `mongo.uri` | Mongo URI   | `null`  |

2. If no `mongo.uri` is provided, you can provide a `mongo.servers` raw definition in combination with `mongo.dbname` and an authentication configuration:

```yaml
mongo:
  servers: |
    - host: mongo1
      port: 27017
    - host: mongo2
      port: 27017
  dbname: gravitee
  auth:
    enabled: false
    username:
    password:
```

3. If neither `mongo.uri` nor `mongo.servers` is provided, you must define the following configuration options:

<table><thead><tr><th width="247.66666666666666">Parameter</th><th width="190">Description</th><th>Default</th></tr></thead><tbody><tr><td><code>mongo.rsEnabled</code></td><td>Whether Mongo replicaset is enabled or not</td><td><code>true</code></td></tr><tr><td><code>mongo.rs</code></td><td>Mongo replicaset name</td><td><code>rs0</code></td></tr><tr><td><code>mongo.dbhost</code></td><td>Mongo host address</td><td><code>mongo-mongodb-replicaset</code></td></tr><tr><td><code>mongo.dbport</code></td><td>Mongo host port</td><td><code>27017</code></td></tr><tr><td><code>mongo.dbname</code></td><td>Mongo DB name</td><td><code>gravitee</code></td></tr><tr><td><code>mongo.auth.enabled</code></td><td>Enable Mongo DB authentication</td><td><code>false</code></td></tr><tr><td><code>mongo.auth.username</code></td><td>Mongo DB username</td><td><code>null</code></td></tr><tr><td><code>mongo.auth.password</code></td><td>Mongo DB password</td><td><code>null</code></td></tr></tbody></table>

**Other keys**

| Parameter               | Description                      | Default |
| ----------------------- | -------------------------------- | ------- |
| `mongo.sslEnabled`      | Enable SSL connection to MongoDB | `false` |
| `mongo.socketKeepAlive` | Enable keep alive for socket     | `false` |

**Mongo replica set**

{% hint style="warning" %}
The mongodb-replicaset installed by Gravitee is NOT recommended in production. It should be used for testing purpose and running APIM locally.
{% endhint %}

<table><thead><tr><th width="233.66666666666666">Parameter</th><th>Description</th><th>Default</th></tr></thead><tbody><tr><td><code>mongodb-replicaset.enabled</code></td><td>Enable deployment of Mongo replicaset</td><td><code>false</code></td></tr></tbody></table>

See [MongoDB](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) for detailed Helm Chart documentation.

{% hint style="warning" %}
You may encounter issues while [running this Helm Chart on Apple Silicon M1](https://github.com/bitnami/charts/issues/7305). If you want to deploy MongoDB on M1, we encourage you to use another Helm Chart.
{% endhint %}
{% endtab %}

{% tab title="PostgreSQL" %}
To install a new PostgresSQL database via JDBC, first run the command below after updating the `username`, `password`, and `databasename` parameters:

```sh
helm install --set postgresqlUsername=postgres --set postgresqlPassword=P@ssw0rd
--set postgresqlDatabase=graviteeapim postgres-apim bitnami/postgresql
```

Verify that the PostgreSQL pod is up and running via `kubectl get pods`:

```sh
kubectl get pods
```

{% code title="Expected output" %}
```
NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
postgres-apim-postgresql-0                1/1     Running      0           98s
```
{% endcode %}

Modify the `values.yml` content below to use the `username`, `password`, `URL`, and `database name` specific to your instance:

```yaml
jdbc:
  driver: https://jdbc.postgresql.org/download/postgresql-42.2.23.jar
  url: jdbc:postgresql://postgres-apim-postgresql:5432/graviteeapim
  username: postgres
  password: P@ssw0rd
management:
  type: jdbc
```
{% endtab %}

{% tab title="Elasticsearch" %}
<table><thead><tr><th width="201">Parameter</th><th>Description</th><th>Default</th></tr></thead><tbody><tr><td><code>es.security.enabled</code></td><td>Elasticsearch username and password enabled</td><td>false</td></tr><tr><td><code>es.security.username</code></td><td>Elasticsearch username</td><td><code>example</code></td></tr><tr><td><code>es.security.password</code></td><td>Elasticsearch password</td><td><code>example</code></td></tr><tr><td><code>es.tls.enabled</code></td><td>Elasticsearch TLS enabled</td><td>false</td></tr><tr><td><code>es.tls.keystore.type</code></td><td>Elasticsearch TLS keystore type (jks, pem or pfx)</td><td><code>null</code></td></tr><tr><td><code>es.tls.keystore.path</code></td><td>Elasticsearch TLS keystore path (jks, pfx)</td><td><code>null</code></td></tr><tr><td><code>es.tls.keystore.password</code></td><td>Elasticsearch TLS keystore password (jks, pfx)</td><td><code>null</code></td></tr><tr><td><code>es.tls.keystore.certs</code></td><td>Elasticsearch TLS certs (only pems)</td><td><code>null</code></td></tr><tr><td><code>es.tls.keystore.keys</code></td><td>Elasticsearch TLS keys (only pems)</td><td><code>null</code></td></tr><tr><td><code>es.index</code></td><td>Elasticsearch index</td><td><code>gravitee</code></td></tr><tr><td><code>es.endpoints</code></td><td>Elasticsearch endpoint array</td><td><code>[http://elastic-elasticsearch-client.default.svc.cluster.local:9200]</code></td></tr></tbody></table>

**Elasticsearch Cluster**

| Parameter               | Description                                | Default |
| ----------------------- | ------------------------------------------ | ------- |
| `elasticsearch.enabled` | Enable deployment of Elasticsearch cluster | `false` |

See [Elasticsearch](https://artifacthub.io/packages/helm/bitnami/elasticsearch) for detailed documentation on optional Helm Chart requirements.

{% hint style="warning" %}
The Elasticsearch installed by Gravitee is NOT recommended in production. It is for testing purposes and running APIM locally.
{% endhint %}
{% endtab %}

{% tab title="Redis" %}
To install Redis, use the command below:

```sh
helm install --set auth.password=p@ssw0rd redis-apim bitnami/redis
```

See [Redis](https://github.com/bitnami/charts/tree/main/bitnami/redis) for detailed documentation on this Helm Chart (like how to use Sentinel).

Check that Redis pod is up and running before proceeding by running `kubectl get pods` as indicated below.

```
kubectl get pods
```

{% code title="Expected output" %}
```
NAME                    READY   STATUS    RESTARTS   AGE
redis-apim-master-0     1/1     Running   0          105s
redis-apim-replicas-0   1/1     Running   0          105s
redis-apim-replicas-1   1/1     Running   0          68s
redis-apim-replicas-2   1/1     Running   0          40s
```
{% endcode %}

To use Redis for rate limit policy, use the information below in `values.yml` and replace the `host`, `port` and `password` with details for your specific instance. You can enable ssl by setting `ssl` to true.

```yaml
ratelimit:
  type: redis
gateway:
  ratelimit:
    redis:
      host: redis-apim-master
      port: 6379
      password: p@ssw0rd
      ssl: false
```

If you want to connect to a Sentinel cluster, you need to specify the `master` and the `nodes`.

```yaml
gateway:
  ratelimit:
      password: p@ssw0rd
      ssl: false
      sentinel:
        master: redis-master
        nodes:
          - host: sentinel1
            port: 26379
          - host: sentinel2
            port: 26379
```

**Other Keys**

| Parameter                          | Description                    | Default |
| ---------------------------------- | ------------------------------ | ------- |
| `gateway.ratelimit.redis.ssl`      | Enable SSL connection to Redis | `false` |
| `gateway.ratelimit.redis.password` | Redis password                 | `false` |
{% endtab %}
{% endtabs %}

### **Gravitee parameters**

The following tables list the available configuration parameters for the Gravitee UI, Gravitee API, Gravitee Gateway, and Alert Engine.

{% tabs %}
{% tab title="Gravitee UI" %}
| Parameter                                 | Description                                                                                                                                                                       | Default                                                                                                                                                                                                    |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ui.name`                                 | UI service name                                                                                                                                                                   | `ui`                                                                                                                                                                                                       |
| `ui.baseURL`                              | Base URL to access to the Management API _(if set to `null`, defaults to Management API ingress value)_                                                                           | `[apim.example.com]/management`                                                                                                                                                                            |
| `ui.title`                                | UI Portal title _(if set to `null`, retrieved from the management repository)_                                                                                                    | `API Portal`                                                                                                                                                                                               |
| `ui.managementTitle`                      | UI Management title _(if set to `null`, retrieved from the management repository)_                                                                                                | `API Management`                                                                                                                                                                                           |
| `ui.documentationLink`                    | UI link to documentation _(if set to `null`, retrieved from the management repository)_                                                                                           | `http://docs.gravitee.io/`                                                                                                                                                                                 |
| `ui.portal.apikeyHeader`                  | API key header name _(if set to `null`, retrieved from the management repository)_                                                                                                | `X-Gravitee-Api-Key`                                                                                                                                                                                       |
| `ui.portal.devMode.enabled`               | Whether to enable developer mode _(if set to `null`, retrieved from the management repository)_                                                                                   | `false`                                                                                                                                                                                                    |
| `ui.portal.userCreation.enabled`          | Whether to enable user creation _(if set to `null`, retrieved from the management repository)_                                                                                    | `false`                                                                                                                                                                                                    |
| `ui.portal.support.enabled`               | Whether to enable support features _(if set to `null`, retrieved from the management repository)_                                                                                 | `true`                                                                                                                                                                                                     |
| `ui.portal.rating.enabled`                | Whether to enable API rating _(if set to `null`, retrieved from the management repository)_                                                                                       | `false`                                                                                                                                                                                                    |
| `ui.portal.analytics.enabled`             | Whether to enable analytics features _(if set to `null`, retrieved from the management repository)_                                                                               | `false`                                                                                                                                                                                                    |
| `ui.portal.analytics.trackingId`          | Tracking ID used for analytics _(if set to `null`, retrieved from the management repository)_                                                                                     | `""`                                                                                                                                                                                                       |
| `ui.replicaCount`                         | How many replicas of the UI pod                                                                                                                                                   | `1`                                                                                                                                                                                                        |
| `ui.image.repository`                     | Gravitee UI image repository                                                                                                                                                      | `graviteeio/management-ui`                                                                                                                                                                                 |
| `ui.image.tag`                            | Gravitee UI image tag                                                                                                                                                             | `1.29.5`                                                                                                                                                                                                   |
| `ui.image.pullPolicy`                     | K8s image pull policy                                                                                                                                                             | `Always`                                                                                                                                                                                                   |
| `ui.image.pullSecrets`                    | K8s image pull Secrets, used to pull both Gravitee UI image and `extraInitContainers`                                                                                             | `null`                                                                                                                                                                                                     |
| `ui.autoscaling.enabled`                  | Whether auto-scaling is enabled or not                                                                                                                                            | `true`                                                                                                                                                                                                     |
| `ui.autoscaling.minReplicas`              | If `ui.autoscaling.enabled` is `true`, what’s the minimum number of replicas                                                                                                      | `2`                                                                                                                                                                                                        |
| `ui.autoscaling.maxReplicas`              | If `ui.autoscaling.enabled` is `true`, what’s the maximum number of replicas                                                                                                      | `3`                                                                                                                                                                                                        |
| `ui.autoscaling.targetAverageUtilization` | If `ui.autoscaling.enabled` what’s the average target utilization (in %) before it auto-scale                                                                                     | `50`                                                                                                                                                                                                       |
| `ui.service.name`                         | UI service name                                                                                                                                                                   | `nginx`                                                                                                                                                                                                    |
| `ui.service.type`                         | K8s publishing [service type](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)                                                 | `ClusterIP`                                                                                                                                                                                                |
| `ui.service.externalPort`                 | K8s UI service external port                                                                                                                                                      | `8082`                                                                                                                                                                                                     |
| `ui.service.internalPort`                 | K8s UI service internal port (container)                                                                                                                                          | `80`                                                                                                                                                                                                       |
| `ui.service.internalPortName`             | K8s UI service internal port name (container)                                                                                                                                     | `http`                                                                                                                                                                                                     |
| `ui.ingress.enabled`                      | Whether Ingress is enabled or not                                                                                                                                                 | `true`                                                                                                                                                                                                     |
| `ui.ingress.hosts`                        | If `ui.ingress.enabled` is enabled, set possible ingress hosts                                                                                                                    | `[apim.example.com]`                                                                                                                                                                                       |
| `ui.ingress.annotations`                  | Supported Ingress annotations to configure ingress controller                                                                                                                     | `[kubernetes.io/ingress.class: nginx, kubernetes.io/app-root: /management, kubernetes.io/rewrite-target: /management, ingress.kubernetes.io/configuration-snippet: "etag on;\nproxy_pass_header ETag;\n"]` |
| `ui.ingress.tls.hosts`                    | [Ingress TLS termination](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)                                                                                   | `[apim.example.com]`                                                                                                                                                                                       |
| `ui.ingress.tls.secretName`               | Ingress TLS K8s Secret name containing the TLS private key and certificate                                                                                                        | `api-custom-cert`                                                                                                                                                                                          |
| `ui.resources.limits.cpu`                 | K8s pod deployment [limits definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)                                                     | `100m`                                                                                                                                                                                                     |
| `ui.resources.limits.memory`              | K8s pod deployment limits definition for memory                                                                                                                                   | `128Mi`                                                                                                                                                                                                    |
| `ui.resources.requests.cpu`               | K8s pod deployment [requests definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/#specify-a-cpu-request-and-a-cpu-limit)             | `50m`                                                                                                                                                                                                      |
| `ui.resources.requests.memory`            | K8s pod deployment requests definition for memory                                                                                                                                 | `64Mi`                                                                                                                                                                                                     |
| `ui.lifecycle.postStart`                  | K8s pod deployment [postStart](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition | `null`                                                                                                                                                                                                     |
| `ui.lifecycle.preStop`                    | K8s pod deployment [preStop](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition   | `null`                                                                                                                                                                                                     |
{% endtab %}

{% tab title="Gravitee API" %}
| Parameter                                             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Default                                                                                                                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.name`                                            | API service name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `api`                                                                                                                                                       |
| `api.logging.debug`                                   | Whether to enable API debug logging or not                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                                                     |
| `api.logging.graviteeLevel`                           | Logging level for Gravitee classes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `DEBUG`                                                                                                                                                     |
| `api.logging.jettyLevel`                              | Logging level for Jetty classes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `INFO`                                                                                                                                                      |
| `api.logging.stdout.encoderPattern`                   | Logback standard output encoder pattern                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n`                                                                                                  |
| `api.logging.file.enabled`                            | Whether to enable file logging or not                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                                                      |
| `api.logging.file.rollingPolicy`                      | Logback file rolling policy configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `TimeBasedRollingPolicy` for 30 days                                                                                                                        |
| `api.logging.file.encoderPattern`                     | Logback file encoder pattern                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n`                                                                                                  |
| `api.logging.additionalLoggers`                       | List of additional logback loggers. Each logger is defined by a `name` and `level` (TRACE, DEBUG, INFO, WARN, or ERROR)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `empty`                                                                                                                                                     |
| `api.ssl.enabled`                                     | API exposition through HTTPS protocol activation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `false`                                                                                                                                                     |
| `api.ssl.keystore.type`                               | Keystore type for API exposition through HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `jks`                                                                                                                                                       |
| `api.ssl.keystore.path`                               | Keystore path for API exposition through HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `null`                                                                                                                                                      |
| `api.ssl.keystore.password`                           | Keystore password for API exposition through HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `null`                                                                                                                                                      |
| `api.ssl.truststore.type`                             | Truststore type for client authentication through 2 way TLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `jks`                                                                                                                                                       |
| `api.ssl.truststore.path`                             | Truststore path for client authentication through 2 way TLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `null`                                                                                                                                                      |
| `api.ssl.truststore.password`                         | Truststore password for client authentication through 2 way TLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `null`                                                                                                                                                      |
| `api.http.services.core.http.authentication.password` | HTTP core service authentication password                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `adminadmin`                                                                                                                                                |
| `api.http.services.core.http.port`                    | HTTP core service port exposed in container                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `18083`                                                                                                                                                     |
| `api.http.services.core.http.host`                    | HTTP core service bind IP or host inside container (0.0.0.0 for exposure on every interfaces)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `localhost`                                                                                                                                                 |
| `api.http.services.core.http.authentication.password` | HTTP core service authentication password                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `adminadmin`                                                                                                                                                |
| `api.http.services.core.http.ingress.enabled`         | Ingress for HTTP core service authentication (requires `api.http.services.core.service.enabled` to be true)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `false`                                                                                                                                                     |
| `api.http.services.core.http.ingress.path`            | The ingress path which should match for incoming requests to the management technical API.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `/management/_(.*)`                                                                                                                                         |
| `api.http.services.core.http.ingress.hosts`           | If `api.ingress.enabled` is enabled, set possible ingress hosts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `[apim.example.com]`                                                                                                                                        |
| `api.http.services.core.http.ingress.annotations`     | Supported Ingress annotations to configure ingress controller                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `[kubernetes.io/ingress.class: nginx, nginx.ingress.kubernetes.io/rewrite-target: /_$1]`                                                                    |
| `api.http.services.core.http.ingress.tls.hosts`       | [Ingress TLS termination](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `[apim.example.com]`                                                                                                                                        |
| `api.http.services.core.http.ingress.tls.secretName`  | Ingress TLS K8s Secret name containing the TLS private key and certificate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `api-custom-cert`                                                                                                                                           |
| `api.http.services.core.http.service.enabled`         | Whether a service is added or not for technical API                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `false`                                                                                                                                                     |
| `api.http.services.core.http.service.externalPort`    | K8s service external port (internal port is defined by `api.http.services.core.http.port` )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `18083`                                                                                                                                                     |
| `api.http.api.entrypoint`                             | Listening path for the API                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `/management`                                                                                                                                               |
| `api.http.client.timeout`                             | HTTP client global timeout                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `10000`                                                                                                                                                     |
| `api.http.client.proxy.type`                          | HTTP client proxy type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `HTTP`                                                                                                                                                      |
| `api.http.client.proxy.http.host`                     | HTTP client proxy host for HTTP protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `localhost`                                                                                                                                                 |
| `api.http.client.proxy.http.port`                     | HTTP client proxy port for HTTP protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `3128`                                                                                                                                                      |
| `api.http.client.proxy.http.username`                 | HTTP client proxy username for HTTP protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `null`                                                                                                                                                      |
| `api.http.client.proxy.http.password`                 | HTTP client proxy password for HTTP protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `null`                                                                                                                                                      |
| `api.http.client.proxy.https.host`                    | HTTP client proxy host for HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `localhost`                                                                                                                                                 |
| `api.http.client.proxy.https.port`                    | HTTP client proxy port for HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `3128`                                                                                                                                                      |
| `api.http.client.proxy.https.username`                | HTTP client proxy username for HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `null`                                                                                                                                                      |
| `api.http.client.proxy.https.password`                | HTTP client proxy password for HTTPS protocol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `null`                                                                                                                                                      |
| `api.user.login.defaultApplication`                   | Whether to enable default application creation on first user authentication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                                                      |
| `api.user.anonymizeOnDelete`                          | Whether to enable user anonymization on deletion                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `false`                                                                                                                                                     |
| `api.supportEnabled`                                  | Whether to enable support feature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `true`                                                                                                                                                      |
| `api.ratingEnabled`                                   | Whether to enable API rating feature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                                                      |
| `smtp.enabled`                                        | Email sending activation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `true`                                                                                                                                                      |
| `smtp.host`                                           | SMTP server host                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `smtp.example.com`                                                                                                                                          |
| `smtp.port`                                           | SMTP server port                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `25`                                                                                                                                                        |
| `smtp.from`                                           | Email sending address                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `info@example.com`                                                                                                                                          |
| `smtp.username`                                       | SMTP server username                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `info@example.com`                                                                                                                                          |
| `smtp.password`                                       | SMTP server password                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `example.com`                                                                                                                                               |
| `smtp.subject`                                        | Email subjects template                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `[gravitee] %s`                                                                                                                                             |
| `smtp.auth`                                           | SMTP server authentication activation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                                                      |
| `smtp.starttlsEnable`                                 | SMTP server TLS activation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                                                     |
| `smtp.localhost`                                      | Hostname that is resolvable by the SMTP server                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `null`                                                                                                                                                      |
| `api.portalURL`                                       | The portal URL used in emails                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `https://{{ index .Values.ui.ingress.hosts 0 }}`                                                                                                            |
| `api.restartPolicy`                                   | Policy to [restart K8 pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-and-container-status)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `OnFailure`                                                                                                                                                 |
| `api.updateStrategy.type`                             | [K8s deployment strategy type](https://kubernetes.io/zh/docs/concepts/workloads/controllers/deployment/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `RollingUpdate`                                                                                                                                             |
| `api.updateStrategy.rollingUpdate.maxUnavailable`     | <p>If api.updateStrategy.type is set to <code>RollingUpdate</code>, <strong>you must set a value here or your deployment can default to 100% unavailability.</strong></p><p>The deployment controller will stop the bad rollout automatically and will stop scaling up the new replica set. This depends on the <code>rollingUpdate</code> parameters (specifically on <code>maxUnavailable</code>) that you have specified. By default, Kubernetes sets the value to 1 and sets spec.replicas to 1, <strong>so if you don’t set those parameters, your deployment can have 100% unavailability by default!</strong></p> | `1`                                                                                                                                                         |
| `api.replicaCount`                                    | How many replicas for the API pod                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `1`                                                                                                                                                         |
| `api.image.repository`                                | Gravitee API image repository                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `graviteeio/management-api`                                                                                                                                 |
| `api.image.tag`                                       | Gravitee API image tag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `1.29.5`                                                                                                                                                    |
| `api.image.pullPolicy`                                | K8s image pull policy                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `Always`                                                                                                                                                    |
| `api.image.pullSecrets`                               | K8s image pull Secrets, used to pull both Gravitee Management API image and `extraInitContainers`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `null`                                                                                                                                                      |
| `api.env`                                             | Environment variables, defined as a list of `name` and `value` as specified in [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)                                                                                                                                                                                                                                                                                                                                                                                                               | `null`                                                                                                                                                      |
| `api.service.type`                                    | K8s publishing [service type](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `ClusterIP`                                                                                                                                                 |
| `api.service.externalPort`                            | K8s service external port                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `83`                                                                                                                                                        |
| `api.service.internalPort`                            | K8s service internal port (container)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `8083`                                                                                                                                                      |
| `api.service.internalPortName`                        | K8s service internal port name (container)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `http`                                                                                                                                                      |
| `api.autoscaling.enabled`                             | Whether auto-scaling is enabled or not                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `true`                                                                                                                                                      |
| `api.autoscaling.minReplicas`                         | If `api.autoscaling.enabled` is `true`, what’s the minimum number of replicas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `2`                                                                                                                                                         |
| `api.autoscaling.maxReplicas`                         | If `api.autoscaling.enabled` is `true`, what’s the maximum number of replicas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `3`                                                                                                                                                         |
| `api.autoscaling.targetAverageUtilization`            | If `api.autoscaling.enabled` what’s the average target utilization (in %) before it auto-scale                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `50`                                                                                                                                                        |
| `api.ingress.enabled`                                 | Whether Ingress is enabled or not                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `true`                                                                                                                                                      |
| `api.ingress.path`                                    | The ingress path which should match for incoming requests to the Management API.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `/management`                                                                                                                                               |
| `api.ingress.hosts`                                   | If `api.ingress.enabled` is enabled, set possible ingress hosts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `[apim.example.com]`                                                                                                                                        |
| `api.ingress.annotations`                             | Supported Ingress annotations to configure ingress controller                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `[kubernetes.io/ingress.class: nginx, ingress.kubernetes.io/configuration-snippet: "etag on;\nproxy_pass_header ETag;\nproxy_set_header if-match \"\";\n"]` |
| `api.ingress.tls.hosts`                               | [Ingress TLS termination](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `[apim.example.com]`                                                                                                                                        |
| `api.ingress.tls.secretName`                          | Ingress TLS K8s Secret name containing the TLS private key and certificate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `api-custom-cert`                                                                                                                                           |
| `api.ingress.management.scheme`                       | Whether to use HTTP or HTTPS to communicate with Management API, defaults to https                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `https`                                                                                                                                                     |
| `api.ingress.portal.scheme`                           | Whether to use HTTP or HTTPS to communicate with Management API, defaults to https                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `https`                                                                                                                                                     |
| `api.resources.limits.cpu`                            | K8s pod deployment [limits definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `500m`                                                                                                                                                      |
| `api.resources.limits.memory`                         | K8s pod deployment limits definition for memory                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `1024Mi`                                                                                                                                                    |
| `api.resources.requests.cpu`                          | K8s pod deployment [requests definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/#specify-a-cpu-request-and-a-cpu-limit)                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `200m`                                                                                                                                                      |
| `api.resources.requests.memory`                       | K8s pod deployment requests definition for memory                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `512Mi`                                                                                                                                                     |
| `api.lifecycle.postStart`                             | K8s pod deployment [postStart](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition                                                                                                                                                                                                                                                                                                                                                                                                                                        | `null`                                                                                                                                                      |
| `api.lifecycle.preStop`                               | K8s pod deployment [preStop](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition                                                                                                                                                                                                                                                                                                                                                                                                                                          | `null`                                                                                                                                                      |
{% endtab %}

{% tab title="Gravitee Gateway" %}
| Parameter                                      | Description                                                                                                                                                                                                | Default                                                                                                                                                                                                                     |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway.name`                                 | Gateway service name                                                                                                                                                                                       | `gateway`                                                                                                                                                                                                                   |
| `gateway.logging.debug`                        | Whether to enable Gateway debug logging or not                                                                                                                                                             | `false`                                                                                                                                                                                                                     |
| `api.logging.additionalLoggers`                | List of additional logback loggers. Each logger is defined by a `name` and `level` (TRACE, DEBUG, INFO, WARN, or ERROR)                                                                                    | `empty`                                                                                                                                                                                                                     |
| `gateway.ssl.enabled`                          | API exposition through HTTPS protocol activation                                                                                                                                                           | `false`                                                                                                                                                                                                                     |
| `gateway.ssl.keystore.type`                    | Keystore type for API exposition through HTTPS protocol                                                                                                                                                    | `jks`                                                                                                                                                                                                                       |
| `gateway.ssl.keystore.path`                    | Keystore path for API exposition through HTTPS protocol                                                                                                                                                    | `null`                                                                                                                                                                                                                      |
| `gateway.ssl.keystore.password`                | Keystore password for API exposition through HTTPS protocol                                                                                                                                                | `null`                                                                                                                                                                                                                      |
| `gateway.ssl.clientAuth`                       | Client authentication through 2 way TLS activation                                                                                                                                                         | `false`                                                                                                                                                                                                                     |
| `gateway.ssl.truststore.type`                  | Truststore type for client authentication through 2 way TLS                                                                                                                                                | `jks`                                                                                                                                                                                                                       |
| `gateway.ssl.truststore.path`                  | Truststore path for client authentication through 2 way TLS                                                                                                                                                | `null`                                                                                                                                                                                                                      |
| `gateway.ssl.truststore.password`              | Truststore password for client authentication through 2 way TLS                                                                                                                                            | `null`                                                                                                                                                                                                                      |
| `gateway.logging.graviteeLevel`                | Logging level for Gravitee classes                                                                                                                                                                         | `DEBUG`                                                                                                                                                                                                                     |
| `gateway.logging.jettyLevel`                   | Logging level for Jetty classes                                                                                                                                                                            | `INFO`                                                                                                                                                                                                                      |
| `gateway.logging.stdout.encoderPattern`        | Logback standard output encoder pattern                                                                                                                                                                    | `%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n`                                                                                                                                                        |
| `gateway.logging.file.enabled`                 | Whether to enable file logging or not                                                                                                                                                                      | `true`                                                                                                                                                                                                                      |
| `gateway.logging.file.rollingPolicy`           | Logback file rolling policy configuration                                                                                                                                                                  | `TimeBasedRollingPolicy` for 30 days                                                                                                                                                                                        |
| `gateway.logging.file.encoderPattern`          | Logback file encoder pattern                                                                                                                                                                               | `%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n`                                                                                                                                                        |
| `gateway.type`                                 | Gateway deployment type: `deployment` or `statefulSet`                                                                                                                                                     | `deployment`                                                                                                                                                                                                                |
| `gateway.replicaCount`                         | How many replicas of the Gateway pod                                                                                                                                                                       | `2`                                                                                                                                                                                                                         |
| `gateway.image.repository`                     | Gravitee Gateway image repository                                                                                                                                                                          | `graviteeio/gateway`                                                                                                                                                                                                        |
| `gateway.image.tag`                            | Gravitee Gateway image tag                                                                                                                                                                                 | `1.29.5`                                                                                                                                                                                                                    |
| `gateway.image.pullPolicy`                     | K8s image pull policy                                                                                                                                                                                      | `Always`                                                                                                                                                                                                                    |
| `gateway.image.pullSecrets`                    | K8s image pull Secrets, used to pull both Gravitee Gateway image and `extraInitContainers`                                                                                                                 | `null`                                                                                                                                                                                                                      |
| `gateway.env`                                  | Environment variables, defined as a list of `name` and `value` as specified in [Kubernetes documentation](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) | `null`                                                                                                                                                                                                                      |
| `gateway.service.type`                         | K8s publishing [service type](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)                                                                          | `ClusterIP`                                                                                                                                                                                                                 |
| `gateway.service.externalPort`                 | K8s Gateway service external port                                                                                                                                                                          | `82`                                                                                                                                                                                                                        |
| `gateway.service.internalPort`                 | K8s Gateway service internal port (container)                                                                                                                                                              | `8082`                                                                                                                                                                                                                      |
| `gateway.service.internalPortName`             | K8s Gateway service internal port name (container)                                                                                                                                                         | `http`                                                                                                                                                                                                                      |
| `gateway.autoscaling.enabled`                  | Whether auto-scaling is enabled or not                                                                                                                                                                     | `true`                                                                                                                                                                                                                      |
| `gateway.autoscaling.minReplicas`              | If `gateway.autoscaling.enabled` is `true`, what’s the minimum number of replicas                                                                                                                          | `2`                                                                                                                                                                                                                         |
| `gateway.autoscaling.maxReplicas`              | If `gateway.autoscaling.enabled` is `true`, what’s the maximum number of replicas                                                                                                                          | `3`                                                                                                                                                                                                                         |
| `gateway.autoscaling.targetAverageUtilization` | If `gateway.autoscaling.enabled` what’s the average target utilization (in %) before it auto-scale                                                                                                         | `50`                                                                                                                                                                                                                        |
| `gateway.websocket`                            | Whether websocket protocol is enabled or not                                                                                                                                                               | `false`                                                                                                                                                                                                                     |
| `gateway.apiKey.header`                        | Header used for the API Key. Set an empty value to prohibit its use.                                                                                                                                       | `X-Gravitee-Api-Key`                                                                                                                                                                                                        |
| `gateway.apiKey.param`                         | Query parameter used for the API Key. Set an empty value to prohibit its use.                                                                                                                              | `api-key`                                                                                                                                                                                                                   |
| `gateway.sharding_tags`                        | Sharding tags (comma separated list)                                                                                                                                                                       | \`\`                                                                                                                                                                                                                        |
| `gateway.ingress.enabled`                      | Whether Ingress is enabled or not                                                                                                                                                                          | `true`                                                                                                                                                                                                                      |
| `gateway.ingress.path`                         | The ingress path which should match for incoming requests to the Gateway.                                                                                                                                  | `/gateway`                                                                                                                                                                                                                  |
| `gateway.ingress.hosts`                        | If `gateway.ingress.enabled` is enabled, set possible ingress hosts                                                                                                                                        | `[apim.example.com]`                                                                                                                                                                                                        |
| `gateway.ingress.annotations`                  | Supported Ingress annotations to configure ingress controller                                                                                                                                              | `[kubernetes.io/ingress.class: nginx, nginx.ingress.kubernetes.io/ssl-redirect: "false", nginx.ingress.kubernetes.io/enable-rewrite-log: "true", kubernetes.io/app-root: /gateway, kubernetes.io/rewrite-target: /gateway]` |
| `gateway.ingress.tls.hosts`                    | [Ingress TLS termination](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)                                                                                                            | `[apim.example.com]`                                                                                                                                                                                                        |
| `gateway.ingress.tls.secretName`               | Ingress TLS K8s Secret name containing the TLS private key and certificate                                                                                                                                 | `api-custom-cert`                                                                                                                                                                                                           |
| `gateway.resources.limits.cpu`                 | K8s pod deployment [limits definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)                                                                              | `500m`                                                                                                                                                                                                                      |
| `gateway.resources.limits.memory`              | K8s pod deployment limits definition for memory                                                                                                                                                            | `512Mi`                                                                                                                                                                                                                     |
| `gateway.resources.requests.cpu`               | K8s pod deployment [requests definition for CPU](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/#specify-a-cpu-request-and-a-cpu-limit)                                      | `200m`                                                                                                                                                                                                                      |
| `gateway.resources.requests.memory`            | K8s pod deployment requests definition for memory                                                                                                                                                          | `256Mi`                                                                                                                                                                                                                     |
| `gateway.lifecycle.postStart`                  | K8s pod deployment [postStart](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition                          | `null`                                                                                                                                                                                                                      |
| `gateway.lifecycle.preStop`                    | K8s pod deployment [preStop](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers) command definition                            | `null`                                                                                                                                                                                                                      |
{% endtab %}

{% tab title="Alert Engine" %}
| Parameter                                               | Description                                                              | Default                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------- |
| `alerts.enabled`                                        | Enables AE connectivity                                                  | `true`                     |
| `alerts.endpoints`                                      | Defines AE endpoints                                                     | `- http://localhost:8072/` |
| `alerts.security.enabled`                               | Enables AE secure connectivity                                           | `false`                    |
| `alerts.security.username`                              | The AE username                                                          | `"admin"`                  |
| `alerts.security.password`                              | The AE password                                                          | `"password"`               |
| `alerts.options.sendEventsOnHttp`                       | Send event on http to AE (websocket otherwise)                           | `true`                     |
| `alerts.options.useSystemProxy`                         | Use system proxy to connect to AE                                        | `false`                    |
| `alerts.options.connectTimeout`                         | AE connection timeout                                                    | `2000`                     |
| `alerts.options.idleTimeout`                            | AE idleTimeout timeout                                                   | `120000`                   |
| `alerts.options.keepAlive`                              | Keep the connection alive                                                | `true`                     |
| `alerts.options.pipelining`                             | Enables event pipelining                                                 | `true`                     |
| `alerts.options.tryCompression`                         | Enables event compression                                                | `true`                     |
| `alerts.options.maxPoolSize`                            | Set the maximum numner of connection                                     | `50`                       |
| `alerts.options.bulkEventsSize`                         | Send events by packets                                                   | `100`                      |
| `alerts.options.bulkEventsWait`                         | Duration for events to be ready to be sent                               | `100`                      |
| `alerts.options.ssl.trustall`                           | Ssl trust all                                                            | `false`                    |
| `alerts.options.ssl.keystore.type`                      | Type of the keystore (jks, pkcs12, pem)                                  | `null`                     |
| `alerts.options.ssl.keystore.path`                      | Path to the keystore                                                     | `null`                     |
| `alerts.options.ssl.keystore.password`                  | Path to the keystore                                                     | `null`                     |
| `alerts.options.ssl.keystore.certs`                     | Keystore cert paths (array, only for pem)                                | `null`                     |
| `alerts.options.ssl.keystore.keys`                      | Keystore key paths (array, only for pem)                                 | `null`                     |
| `alerts.options.ssl.truststore.type`                    | Type of the truststore                                                   | `null`                     |
| `alerts.options.ssl.truststore.path`                    | Path to the truststore                                                   | `null`                     |
| `alerts.options.ssl.truststore.password`                | Password of the truststore                                               | `null`                     |
| `alerts.engines.<cluster-name>.endpoints`               | Defines AE endpoints on the cluster \<cluster-name>                      | `- http://localhost:8072/` |
| `alerts.engines.<cluster-name>.security.username`       | The AE username on the cluster \<cluster-name>                           | `"admin"`                  |
| `alerts.engines.<cluster-name>.security.password`       | The AE password on the cluster \<cluster-name>                           | `"password"`               |
| `alerts.engines.<cluster-name>.ssl.trustall`            | Ssl trust all on the cluster \<cluster-name>                             | `false`                    |
| `alerts.engines.<cluster-name>.ssl.keystore.type`       | Type of the keystore (jks, pkcs12, pem) on the cluster \<cluster-name>   | `null`                     |
| `alerts.engines.<cluster-name>.ssl.keystore.path`       | Path to the keystore (jks, pkcs12, pem) on the cluster \<cluster-name>   | `null`                     |
| `alerts.engines.<cluster-name>.ssl.keystore.password`   | Path to the keystore on the cluster \<cluster-name>                      | `null`                     |
| `alerts.engines.<cluster-name>.ssl.keystore.certs`      | Keystore cert paths (array, only for pem) on the cluster \<cluster-name> | `null`                     |
| `alerts.engines.<cluster-name>.ssl.keystore.keys`       | Keystore key paths (array, only for pem) on the cluster \<cluster-name>  | `null`                     |
| `alerts.engines.<cluster-name>.ssl.truststore.type`     | Type of the truststore on the cluster \<cluster-name>                    | `null`                     |
| `alerts.engines.<cluster-name>.ssl.truststore.path`     | Path to the truststore on the cluster \<cluster-name>                    | `null`                     |
| `alerts.engines.<cluster-name>.ssl.truststore.password` | Password of the truststore on the cluster \<cluster-name>                | `null`                     |
{% endtab %}
{% endtabs %}

## OpenShift

The Gravitee API Management Helm Chart supports Ingress standard objects and does not support specific OpenShift Routes. It is therefore compatible with OpenShift versions 3.10 and later. When deploying APIM within OpenShift:

* Use the full host domain instead of paths for all components (ingress paths are not supported well by OpenShift)
* Override the security context to let OpenShift automatically define the `user-id` and `group-id` used to run the containers

For Openshift to automatically create Routes from the Ingress, you must define the `ingressClassName` as `none`. Here is a standard `values.yaml` used to deploy APIM into OpenShift:

{% code title="values.yml" %}
```yaml
api:
  ingress:
    management:
      ingressClassName: none
      path: /management
      hosts:
        - api-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
      annotations:
        route.openshift.io/termination: edge
    portal:
      ingressClassName: none
      path: /portal
      hosts:
        - api-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
      annotations:
        route.openshift.io/termination: edge
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: 1000
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

gateway:
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - gw-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
    annotations:
      route.openshift.io/termination: edge
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: 1000
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

portal:
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - portal-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
    annotations:
      route.openshift.io/termination: edge
  securityContext: null
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: null
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

ui:
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - console-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
    annotations:
      route.openshift.io/termination: edge
  securityContext: null
  deployment:
    securityContext:
      runAsUser: null
      runAsGroup: null
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault
```
{% endcode %}

By setting `runAsUser` to `null`, OpenShift is forced to define the correct values when deploying the Helm Chart.

## Licences

Enterprise plugins require a license in APIM. To define a license, enter the `license.key` value in the `values.yml` file and add the Helm argument `--set license.key=<license.key in base64>`.

{% hint style="info" %}
The `license.key` value you enter must be encoded in `base64`:

* Linux: `base64 -w 0 license.key`
* macOS: `base64 license.key`
{% endhint %}

Example:

```sh
$ export GRAVITEESOURCE_LICENSE_B64="$(base64 -w 0 license.key)"
$ helm install \
  --set license.key=${GRAVITEESOURCE_LICENSE_B64} \
  --create-namespace --namespace gravitee-apim \
  graviteeio-apim3x \
  graviteeio/apim3
```

| Parameter     | Description | Default                            |
| ------------- | ----------- | ---------------------------------- |
| `license.key` | string      | license.key file encoded in base64 |
