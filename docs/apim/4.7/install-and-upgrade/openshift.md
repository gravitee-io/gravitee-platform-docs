# OpenShift

## Prerequisites

* Gravitee API Management (APIM) Helm chart is compatible with OpenShift versions 3.10 and later.
* You must install the following command line tools:
  * [Kubectl or OC](https://docs.openshift.com/container-platform/4.9/cli_reference/openshift_cli/getting-started-cli.html#cli-installing-cli_cli-developer-commands)
  * [Helm](https://docs.openshift.com/container-platform/4.10/applications/working_with_helm_charts/installing-helm.html)

{% include "../.gitbook/includes/installation-guide-note.md" %}

## Procedure

To install APIM within OpenShift, complete the following steps:

* [#optional-configure-the-serviceaccount-using-roles](openshift.md#optional-configure-the-serviceaccount-using-roles "mention")
* [#optional-configure-the-configuration-types](openshift.md#optional-configure-the-configuration-types "mention")
* [#configure-the-databases](openshift.md#configure-the-databases "mention")
* [#configure-the-gravitee-parameters](openshift.md#configure-the-gravitee-parameters "mention")
* [#install-the-gravitee-helm-chart](openshift.md#install-the-gravitee-helm-chart "mention")

### (Optional) Configure the ServiceAccount using roles

If you want to configure the ServiceAccount with more advanced settings, you must use Roles. For more information about using roles, go to go to [Using RBAC to define and apply permissions RBAC overview](https://docs.openshift.com/container-platform/4.8/authentication/using-rbac.html).

### (Optional) Configure the configuration types

You can configure your deployment for the following configuration types:

* Development deployment
* External configuration
* Shared configuration

The configuration types for OpenShift are the same configuration types for Kubernetes. For more information about the configuration types, see [#configuration-types](kubernetes.md#configuration-types "mention").

### Configure the databases

To deploy OpenShift, you must configure the MongoDB database. Also, you can configure other databases if you need them.

{% tabs %}
{% tab title="MongoDB" %}
**(Optional) Install MongoDB**

{% hint style="info" %}
If you have already installed MongoDB, you do not need to install MongoDB again.
{% endhint %}

* To install MongoDB with Helm, use the following command:

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm install mongodb bitnami/mongodb \
  --set image.repository=bitnamilegacy/mongodb \
  --set auth.rootPassword=r00t
```

**Configure the connection MongoDB**

**Step 1:** To configure the connection to MongoDB, complete either of the following steps:

* **Option 1:** Provide the MongoDB URI. For more information about the MongoDB URI, go to [Connection Strings](https://www.mongodb.com/docs/manual/reference/connection-string/).

| Parameter   | Description | Default |
| ----------- | ----------- | ------- |
| `mongo.uri` | Mongo URI   | `null`  |

* **Option 2:** Provide a `mongo.servers` raw definition with `mongo.dbname` and an authentication configuration:

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

**Step 2:** Define the following configuration options:

| Parameter             | Description                                | Default                    |
| --------------------- | ------------------------------------------ | -------------------------- |
| `mongo.rsEnabled`     | Whether Mongo replicaset is enabled or not | `true`                     |
| `mongo.rs`            | Mongo replicaset name                      | `rs0`                      |
| `mongo.dbhost`        | Mongo host address                         | `mongo-mongodb-replicaset` |
| `mongo.dbport`        | Mongo host port                            | `27017`                    |
| `mongo.dbname`        | Mongo DB name                              | `gravitee`                 |
| `mongo.auth.enabled`  | Enable Mongo DB authentication             | `false`                    |
| `mongo.auth.username` | Mongo DB username                          | `null`                     |
| `mongo.auth.password` | Mongo DB password                          | `null`                     |

**Other keys**

| Parameter               | Description                      | Default |
| ----------------------- | -------------------------------- | ------- |
| `mongo.sslEnabled`      | Enable SSL connection to MongoDB | `false` |
| `mongo.socketKeepAlive` | Enable keep alive for socket     | `false` |

**Mongo replica set**

Use the mongodb-replicaset for only testing purposes and running locally.

| Parameter                        | Description                           | Default |
| -------------------------------- | ------------------------------------- | ------- |
| **`mongodb-replicaset.enabled`** | Enable deployment of Mongo replicaset | `false` |

{% hint style="info" %}
You might encounter issues while running this Helm chart on Apple Silicon M1. If you want to deploy MongoDB on M1, use another Helm chart. For more information, go to [Support for ARM64 architecture in Bitnami container images](https://github.com/bitnami/charts/issues/7305).
{% endhint %}
{% endtab %}

{% tab title="PostgresSQL" %}
**(Optional) Install PostgreSQL**

{% hint style="info" %}
If you have already installed PostgreSQL, you do not need to install PostgreSQL again.
{% endhint %}

To install a new PostgreSQL database, complete the following steps:

1. Update the `username`, `password`, and `databasename` parameters.
2. Run the following commands:

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm install postgres-apim bitnami/postgresql \
  --set image.repository=bitnamilegacy/postgresql \
  --set postgresqlUsername=postgres \
  --set postgresqlPassword=P@ssw0rd \
  --set postgresqlDatabase=graviteeapim
```

**Verification**

Verify that the PostgreSQL pod works using the following command:

```
kubectl get pods
```

If the PostgreSQL is running correctly, you see an output similar to the following expected output:

```
NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
postgres-apim-postgresql-0                1/1     Running      0           98s
```

**Configure PostgreSQL**

* Modify the `values.yml` the following content to use the `username`, `password`, `URL`, and `database name` that is specific to your instance:

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

{% tab title="ElasticSearch" %}
{% hint style="info" %}
* If you have already installed ElasticSearch, you do not need to install ElasticSearch again.
* For information about customizations, see [Elastic Stack Helm Chart](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html).
{% endhint %}

**(Optional) Install ElasticSearch**

To install ElasticSearch, run the following commands:

```sh
helm repo add elastic https://helm.elastic.co

helm repo update

helm install es-kb-quickstart elastic/eck-stack -n elastic-stack --create-namespace
```

**Configure ElasticSearch**

| Parameter                  | Description                                       | Default                                                                |
| -------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------- |
| `es.security.enabled`      | Elasticsearch username and password enabled       | false                                                                  |
| `es.security.username`     | Elasticsearch username                            | `example`                                                              |
| `es.security.password`     | Elasticsearch password                            | `example`                                                              |
| `es.tls.enabled`           | Elasticsearch TLS enabled                         | false                                                                  |
| `es.tls.keystore.type`     | Elasticsearch TLS keystore type (jks, pem or pfx) | `null`                                                                 |
| `es.tls.keystore.path`     | Elasticsearch TLS keystore path (jks, pfx)        | `null`                                                                 |
| `es.tls.keystore.password` | Elasticsearch TLS keystore password (jks, pfx)    | `null`                                                                 |
| `es.tls.keystore.certs`    | Elasticsearch TLS certs (only pems)               | `null`                                                                 |
| `es.tls.keystore.keys`     | Elasticsearch TLS keys (only pems)                | `null`                                                                 |
| `es.index`                 | Elasticsearch index                               | `gravitee`                                                             |
| `es.endpoints`             | Elasticsearch endpoint array                      | `[http://elastic-elasticsearch-client.default.svc.cluster.local:9200]` |
{% endtab %}

{% tab title="Redis" %}
**(Optional) Install Redis**

{% hint style="info" %}
If you have already installed Redis, you do not need to install Redis again.
{% endhint %}

To install Redis using the following commands:

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm install redis-apim bitnami/redis \
  --version 19.6.4 \
  --set image.repository=bitnamilegacy/redis \
  --set auth.password=p@ssw0rd
```

For more information about Redis, go to [Redis](https://github.com/bitnami/charts/tree/main/bitnami/redis).

**Verification**

Check that Redis pod works using the following command:

```bash
kubectl get pods
```

If the Redis pod is working correctly, you see an output similar to the following expected output:

```sh
NAME                    READY   STATUS    RESTARTS   AGE
redis-apim-master-0     1/1     Running   0          105s
redis-apim-replicas-0   1/1     Running   0          105s
redis-apim-replicas-1   1/1     Running   0          68s
redis-apim-replicas-2   1/1     Running   0          40s
```

**Configure Redis**

To use Redis for rate limit policy, add the following information to the `values.yml` file:

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

* Replace `host`, `port`, and `password` with details specific to your instance.
* (optional) Enable `ssl` by setting `ssl` to `true`.
* (optional) To connect to a Sentinel cluster, specify the `master` and the `nodes`.

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

### Configure the Gravitee Parameters and values.yml file

#### Configure the Gravitee Parameters

You can configure the following Gravitee components:

* Gravitee UI
* Gravitee API
* Gravitee Gateway
* Alert Engine

The process for configuring the Gravitee components on OpenShift is the same process as configuring the Gravitee components on Kubernetes with some adjustments. To configure the Gravitee components, see [#gravitee-parameters](kubernetes.md#gravitee-parameters "mention").

#### Adjustments needed for OpenShift

When you configure your `values.yml` file for OpenShift deployment, you must complete the following actions:

* Use the full host domain instead of paths for all components.
* Override the security context to let OpenShift automatically define the `user-id` and `group-id` you use to run the containers. Here is an example of the security context that has been overridden:

```yaml
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

* For OpenShift to automatically create Routes from the Ingress, define the `ingressClassName` as `none`. Here is an example of an `ingressClassName` defined as `none`:

```yaml
 api:
  ingress:
    management:
      ingressClassName: none
      path: /management
      hosts:
        - api-graviteeio.apps.openshift-test.xxxx.p1.openshiftapps.com
      annotations:
        route.openshift.io/termination: edge
```

**Example**

Here is an example of a typical `values.yml` file used to deploy APIM on OpenShift:

{% hint style="info" %}
By setting `runAsUser` to `null`, OpenShift is forced to define the correct values when deploying the Helm chart.
{% endhint %}

{% code title="values.yml" %}
```yaml
openshift:
  enabled: true
  
# Configure access to your Config Database (e.g.: MongoDB)
#mongo:
#  uri: mongodb+srv://${gravitee_apim_mongodb_user}:${gravitee_apim_mongodb_pass}@${gravitee_apim_mongodb_host}/${gravitee_apim_mongodb_name}?retryWrites=true&w=majority&connectTimeoutMS=10000&socketTimeoutMS=10000&maxIdleTimeMS=30000

# Configure access to your Analytics Database (e.g.: Elasticsearch)
#es:
#  enabled: true
#  index: ${gravitee_apim_index_name}
#  index_mode: ilm
#  lifecycle:
#    enabled: true
#    policies:
#      monitor: gravitee_monitor_default_1_days
#      request: gravitee_request_default_90_days
#      health: gravitee_health_default_30_days
#      log: gravitee_log_default_7_days
#  endpoints:
#    - ${elastic_endpoint}
#  security:
#    enabled: true
#    username: ${elastic_gravitee_user}
#    password: ${elastic_gravitee_pass}

api:
  ingress:
    management:
      ingressClassName: none
      path: /management
      hosts:
        - api-graviteeio.apps.openshift-test.xxxx.xx.openshiftapps.com
      annotations:
        route.openshift.io/termination: edge
    portal:
      ingressClassName: none
      path: /portal
      hosts:
        - api-graviteeio.apps.openshift-test.xxxx.xx.openshiftapps.com
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
      - gw-graviteeio.apps.openshift-test.xxxx.xx.openshiftapps.com
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
      - portal-graviteeio.apps.openshift-test.xxxx.xx.openshiftapps.com
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
      - console-graviteeio.apps.openshift-test.xxxx.xx.openshiftapps.com
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

### Install the Gravitee Helm Chart

To install the Gravitee Helm Chart, complete the following steps:

1. Add the Gravitee Helm chart repo using the following command:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

2. Install the Helm chart to a dedicated namespace using the following command:

```sh
helm install -f values.yaml graviteeio-apim4x graviteeio/apim --create-namespace --namespace gravitee-apim
```

{% hint style="info" %}
`values.yaml` file refers to the values.yaml file that you prepared in the [#configure-the-gravitee-parameters-and-values.yml-file](openshift.md#configure-the-gravitee-parameters-and-values.yml-file "mention") section.
{% endhint %}
