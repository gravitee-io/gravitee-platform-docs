# Deploy in Kubernetes

## Overview

This guide explains how to deploy Gravitee Access Management (AM) on Kubernetes using Helm. It is assumed that you are already familiar with Kubernetes terms.

## AM Helm Chart

The Helm Chart supports versions 2.10.x and higher.

### Components

This chart will deploy the following:

* Gravitee AM Console
* Gravitee AM API
* Gravitee AM Gateway
* MongoDB replica-set (optional dependency)

### Add the Helm Chart repo

Add the Gravitee Helm Chart repo using the command below:

```sh
helm repo add graviteeio https://helm.gravitee.io
```

### Install the Helm Chart

Now, install the chart from the Helm repo with the release name `graviteeio-am`.

To prevent potential issues in the future, it is best practice to create a separate namespace for your installation in order to prevent the use of the default Kubernetes namespace. The installation command provided immediately below assumes that such best practice is followed, however this is not a mandatory requirement.

To install the Helm Chart using a dedicated namespace (we use `gravitee-am` as an example), run the following command:

{% code overflow="wrap" %}
```sh
helm install graviteeio-am graviteeio/am --create-namespace --namespace gravitee-am
```
{% endcode %}

To install the Helm Chart using the default namespace (not recommended), run the following command:

```sh
helm install graviteeio-am graviteeio/am
```

To install the chart using the chart archive, run:

```sh
helm install am-1.0.0.tgz
```

### Create a Helm Chart archive

To package this chart directory into a chart archive, run:

```sh
helm package .
```

### License

An enterprise plugin requires a license in AM. You can define it by:

* Fill the `license.key` field in the `values.yml` file
* Add Helm arg: `--set license.key=<license.key in base64>`

To get the license.key value, encode your file `license.key` in `base64`:

* Linux: `base64 -w 0 license.key`
* macOS: `base64 license.key`

Example:

<pre class="language-sh"><code class="lang-sh">$ export GRAVITEESOURCE_LICENSE_B64="$(base64 -w 0 license.key)"

<strong>$ helm install \
</strong>  --set license.key=${GRAVITEESOURCE_LICENSE_B64} \
  graviteeio-am \
  graviteeio/am
</code></pre>

### Configuration

The following tables list the configurable parameters of the Gravitee chart and their default values.

You can rely on Kubernetes _ConfigMaps_ and _Secrets_ to initialize Gravitee settings since AM 3.15.0. To use this feature, you have to create the ServiceAccount that allows AM to connect to the Kubernetes API (the helm chart should do it by default) and then you simply have to define your application settings like this:

* Secret settings: `secrets://kubernetes/mysecret:key?namespace=ns`, with the kube plugin enabled via `secrets.kubernetes.enabled=true`

{% hint style="warning" %}
The above syntax only applies to Gravitee versions 4.2 and later
{% endhint %}

* ConfigMap settings: `kubernetes://<namespace>/configmaps/<my-configmap-name>/<my-configmap-key>`

Here is an example for the mongodb uri initialized from the `mongo` secret deployed in the `default` namespace:

```yaml
mongo:
  uri: kubernetes://default/secrets/mongo/mongouri
```

{% hint style="info" %}
If you need to access a secret, you have to create a role within your namespace.

If you are deploying in another namespace and you need to access a secret there, you have to create a separate role in that namespace. The two roles can have the same name, but they are completely separate objects - each role only gives access to the namespace it is created in.

For more information about roles, see [Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole) in the [Kubernetes documentation](https://kubernetes.io/docs/).
{% endhint %}

#### **Shared configuration**

To configure common features such as:

* chaos testing (see [chaoskube](https://github.com/kubernetes/charts/tree/master/stable/chaoskube) chart)
* configuration database (see [mongodb](https://github.com/bitnami/charts/tree/master/bitnami/mongodb)

| Parameter       | Description       | Default |
| --------------- | ----------------- | ------- |
| `chaos.enabled` | Enable Chaos test | false   |

#### **Mongo**

**MongoDB connections**

There are three ways to configure MongoDB connections.

The most simple is to provide the [MongoDB URI](https://docs.mongodb.com/manual/reference/connection-string/).

| Parameter   | Description | Default |
| ----------- | ----------- | ------- |
| `mongo.uri` | Mongo URI   | `null`  |

If no `mongo.uri` is provided, you can provide a `mongo.servers` raw definition in combination with `mongo.dbname`, plus eventual authentication configuration:

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

If neither `mongo.uri` or `mongo.servers` are provided, you have to define the following configuration options:

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

#### **Mongo ReplicaSet**

| Parameter                    | Description                           | Default |
| ---------------------------- | ------------------------------------- | ------- |
| `mongodb-replicaset.enabled` | Enable deployment of Mongo replicaset | `false` |

See [MongoDB replicaset](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) for detailed documentation on helm chart.

Please be aware that the mongodb-replicaset installed by Gravitee is NOT recommended in production and it is just for testing purpose and running AM locally.

{% hint style="info" %}
You may encounter issues while running this Helm Charts on Apple Silicon M1 (see [https://github.com/bitnami/charts/issues/7305](https://github.com/bitnami/charts/issues/7305)). If you want to deploy MongoDB on M1 we encourage you to switch to an other Helm Charts for deploying MongoDB.
{% endhint %}

#### **Proxy configuration for HTTP clients**

To define the proxy settings for HTTP clients used by the Management API and the Gateway, the `httpClient` section needs to be defined into the `values.yaml`. This section will be applied on both Gateway and Management API configuration files.

{% code title="values.yaml" overflow="wrap" %}
```yaml
httpClient:
  timeout: 10000 # in milliseconds
  proxy:
    enabled: false
    exclude-hosts: # list of hosts to exclude from proxy (wildcard hosts are supported)
      - '*.internal.com'
      - internal.mycompany.com
    type: HTTP #HTTP, SOCK4, SOCK5
    http:
      host: localhost
      port: 3128
      username: user
      password: secret
    https:
      host: localhost
      port: 3128
      username: user
      password: secret
```
{% endcode %}

#### **Gravitee.io Configuration**

| Key                                                                          | Type                                  | Default                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| alerts.enabled                                                               | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.endpoints                                                             | string\[]                             | `- http://localhost:8072/`                                                                                                                                                                                                                                                                                                                                                             |
| alerts.security.enabled                                                      | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| alerts.security.username                                                     | string                                | `"admin"`                                                                                                                                                                                                                                                                                                                                                                              |
| alerts.security.password                                                     | string                                | `"password"`                                                                                                                                                                                                                                                                                                                                                                           |
| alerts.options.sendEventsOnHttp                                              | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.useSystemProxy                                                | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| alerts.options.connectTimeout                                                | int                                   | `2000`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.idleTimeout                                                   | int                                   | `120000`                                                                                                                                                                                                                                                                                                                                                                               |
| alerts.options.keepAlive                                                     | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.pipelining                                                    | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.tryCompression                                                | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.maxPoolSize                                                   | int                                   | `50`                                                                                                                                                                                                                                                                                                                                                                                   |
| alerts.options.bulkEventsSize                                                | int                                   | `100`                                                                                                                                                                                                                                                                                                                                                                                  |
| alerts.options.bulkEventsWait                                                | int                                   | `100`                                                                                                                                                                                                                                                                                                                                                                                  |
| alerts.options.ssl.trustall                                                  | boolean                               | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| alerts.options.ssl.keystore.type                                             | enum(jks, pkcs12, pem)                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.keystore.path                                             | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.keystore.password                                         | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.keystore.certs                                            | array\<string>                        | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.keystore.keys                                             | array\<string>                        | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.truststore.type                                           | enum(jks, pkcs12, pem)                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.truststore.path                                           | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.options.ssl.truststore.password                                       | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.endpoints                                     | array\<string>                        | `- http://localhost:8072/`                                                                                                                                                                                                                                                                                                                                                             |
| alerts.engines.\<cluster-name>.security.username                             | string                                | `"null"`                                                                                                                                                                                                                                                                                                                                                                               |
| alerts.engines.\<cluster-name>.security.password                             | string                                | `"null"`                                                                                                                                                                                                                                                                                                                                                                               |
| alerts.engines.\<cluster-name>.ssl.trustall                                  | boolean                               | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| alerts.engines.\<cluster-name>.ssl.keystore.type                             | enum(jks, pkcs12, pem)                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.keystore.path                             | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.keystore.password                         | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.keystore.certs                            | array\<string>                        | \`null                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.keystore.keys                             | array\<string>                        | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.truststore.type                           | enum(jks, pkcs12, pem)                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.truststore.path                           | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| alerts.engines.\<cluster-name>.ssl.truststore.password                       | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.autoscaling.enabled                                                      | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.autoscaling.maxReplicas                                                  | int                                   | `3`                                                                                                                                                                                                                                                                                                                                                                                    |
| api.autoscaling.minReplicas                                                  | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| api.autoscaling.targetAverageUtilization                                     | int                                   | `50`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.autoscaling.targetMemoryAverageUtilization                               | int                                   | `80`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.enabled                                                                  | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.services.core.http.authentication.password                          | string                                | `"adminadmin"`                                                                                                                                                                                                                                                                                                                                                                         |
| api.http.services.core.http.host                                             | string                                | `"localhost"`                                                                                                                                                                                                                                                                                                                                                                          |
| api.http.services.core.http.port                                             | int                                   | `18093`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.services.core.ingress.enabled                                       | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.services.core.service.enabled                                       | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.host                                                                | string                                | `"0.0.0.0"`                                                                                                                                                                                                                                                                                                                                                                            |
| api.http.port                                                                | bool                                  | `8093`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.idleTimeout                                                         | int                                   | `30000`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.acceptors                                                           | int                                   | `-1`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.http.selectors                                                           | int                                   | `-1`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.http.outputBufferSize                                                    | int                                   | `32768`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.requestHeaderSize                                                   | int                                   | `8192`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.responseHeaderSize                                                  | int                                   | `8192`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.pool.minThreads                                                     | int                                   | `10`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.http.pool.maxThreads                                                     | int                                   | `200`                                                                                                                                                                                                                                                                                                                                                                                  |
| api.http.pool.idleTimeout                                                    | int                                   | `60000`                                                                                                                                                                                                                                                                                                                                                                                |
| api.http.pool.queueSize                                                      | int                                   | `6000`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.pool.accesslog.enabled                                              | boolean                               | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.http.pool.accesslog.path                                                 | string                                | `${gravitee.home}/logs/gravitee_accesslog_yyyy_mm_dd.log}`                                                                                                                                                                                                                                                                                                                             |
| api.image.pullPolicy                                                         | string                                | `"Always"`                                                                                                                                                                                                                                                                                                                                                                             |
| api.image.repository                                                         | string                                | `"graviteeio/am-management-api"`                                                                                                                                                                                                                                                                                                                                                       |
| api.ingress.annotations."ingress.kubernetes.io/configuration-snippet"        | string                                | `"etag on;\nproxy_pass_header ETag;\nproxy_set_header if-match \"\";\n"`                                                                                                                                                                                                                                                                                                               |
| api.ingress.annotations."kubernetes.io/ingress.class"                        | string                                | `"nginx"`                                                                                                                                                                                                                                                                                                                                                                              |
| api.ingress.enabled                                                          | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.ingress.hosts\[0].host                                                   | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| api.ingress.path                                                             | string                                | `"/management"`                                                                                                                                                                                                                                                                                                                                                                        |
| api.ingress.tls\[0].hosts\[0]                                                | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| api.ingress.tls\[0].secretName                                               | string                                | `"api-custom-cert"`                                                                                                                                                                                                                                                                                                                                                                    |
| api.jwt.secret                                                               | string                                | `"s3cR3t4grAv1t3310AMS1g1ingDftK3y"`                                                                                                                                                                                                                                                                                                                                                   |
| api.logging.debug                                                            | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.logging.file.enabled                                                     | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.logging.file.encoderPattern                                              | string                                | `"%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n%n"`                                                                                                                                                                                                                                                                                                                         |
| api.logging.file.rollingPolicy                                               | string                                | `"\u003crollingPolicy class=\"ch.qos.logback.core.rolling.TimeBasedRollingPolicy\"\u003e\n \u003c!-- daily rollover --\u003e\n \u003cfileNamePattern\u003e${gravitee.management.log.dir}/gravitee_%d{yyyy-MM-dd}.log\u003c/fileNamePattern\u003e\n \u003c!-- keep 30 days' worth of history --\u003e\n \u003cmaxHistory\u003e30\u003c/maxHistory\u003e\n\u003c/rollingPolicy\u003e\n"` |
| api.logging.graviteeLevel                                                    | string                                | `"DEBUG"`                                                                                                                                                                                                                                                                                                                                                                              |
| api.logging.jettyLevel                                                       | string                                | `"INFO"`                                                                                                                                                                                                                                                                                                                                                                               |
| api.logging.stdout.encoderPattern                                            | string                                | `"%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"`                                                                                                                                                                                                                                                                                                                           |
| api.logging.stdout.json                                                      | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.name                                                                     | string                                | `"management-api"`                                                                                                                                                                                                                                                                                                                                                                     |
| api.reloadOnConfigChange                                                     | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.replicaCount                                                             | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| api.resources.limits.cpu                                                     | string                                | `"500m"`                                                                                                                                                                                                                                                                                                                                                                               |
| api.resources.limits.memory                                                  | string                                | `"1024Mi"`                                                                                                                                                                                                                                                                                                                                                                             |
| api.resources.requests.cpu                                                   | string                                | `"200m"`                                                                                                                                                                                                                                                                                                                                                                               |
| api.resources.requests.memory                                                | string                                | `"512Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| api.restartPolicy                                                            | string                                | `"OnFailure"`                                                                                                                                                                                                                                                                                                                                                                          |
| api.service.externalPort                                                     | int                                   | `83`                                                                                                                                                                                                                                                                                                                                                                                   |
| api.service.internalPort                                                     | int                                   | `8093`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.service.internalPortName                                                 | string                                | `http`                                                                                                                                                                                                                                                                                                                                                                                 |
| api.service.type                                                             | string                                | `"ClusterIP"`                                                                                                                                                                                                                                                                                                                                                                          |
| api.ssl.clientAuth                                                           | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.ssl.enabled                                                              | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| api.updateStrategy.rollingUpdate.maxUnavailable                              | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| api.updateStrategy.type                                                      | string                                | `"RollingUpdate"`                                                                                                                                                                                                                                                                                                                                                                      |
| chaos.enabled                                                                | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.autoscaling.enabled                                                  | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.autoscaling.maxReplicas                                              | int                                   | `3`                                                                                                                                                                                                                                                                                                                                                                                    |
| gateway.autoscaling.minReplicas                                              | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| gateway.autoscaling.targetAverageUtilization                                 | int                                   | `50`                                                                                                                                                                                                                                                                                                                                                                                   |
| gateway.autoscaling.targetMemoryAverageUtilization                           | int                                   | `80`                                                                                                                                                                                                                                                                                                                                                                                   |
| gateway.enabled                                                              | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.image.pullPolicy                                                     | string                                | `"Always"`                                                                                                                                                                                                                                                                                                                                                                             |
| gateway.image.repository                                                     | string                                | `"graviteeio/am-gateway"`                                                                                                                                                                                                                                                                                                                                                              |
| gateway.http.cookie.secure                                                   | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.http.cookie.sameSite                                                 | string                                | `"Lax"`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.http.cookie.session.name                                             | string                                | `"GRAVITEE_IO_AM_SESSION"`                                                                                                                                                                                                                                                                                                                                                             |
| gateway.http.cookie.session.timeout                                          | int                                   | `1800000`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.annotations."kubernetes.io/app-root"                         | string                                | `"/auth"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.annotations."kubernetes.io/ingress.class"                    | string                                | `"nginx"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.annotations."kubernetes.io/rewrite-target"                   | string                                | `"/auth"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.annotations."nginx.ingress.kubernetes.io/enable-rewrite-log" | string                                | `"true"`                                                                                                                                                                                                                                                                                                                                                                               |
| gateway.ingress.annotations."nginx.ingress.kubernetes.io/ssl-redirect"       | string                                | `"false"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.enabled                                                      | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.ingress.hosts\[0]                                                    | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| gateway.ingress.path                                                         | string                                | `"/auth"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.ingress.tls\[0].hosts\[0]                                            | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| gateway.ingress.tls\[0].secretName                                           | string                                | `"api-custom-cert"`                                                                                                                                                                                                                                                                                                                                                                    |
| gateway.jwt.secret                                                           | string                                | `"s3cR3t4grAv1t3310AMS1g1ingDftK3y"`                                                                                                                                                                                                                                                                                                                                                   |
| gateway.logging.debug                                                        | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.logging.file.enabled                                                 | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.logging.file.encoderPattern                                          | string                                | `"%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n"`                                                                                                                                                                                                                                                                                                                 |
| gateway.logging.file.rollingPolicy                                           | string                                | `"\u003crollingPolicy class=\"ch.qos.logback.core.rolling.TimeBasedRollingPolicy\"\u003e\n \u003c!-- daily rollover --\u003e\n \u003cfileNamePattern\u003e${gravitee.home}/logs/gravitee_%d{yyyy-MM-dd}.log\u003c/fileNamePattern\u003e\n \u003c!-- keep 30 days' worth of history --\u003e\n \u003cmaxHistory\u003e30\u003c/maxHistory\u003e\n\u003c/rollingPolicy\u003e\n"`          |
| gateway.logging.graviteeLevel                                                | string                                | `"DEBUG"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.logging.jettyLevel                                                   | string                                | `"WARN"`                                                                                                                                                                                                                                                                                                                                                                               |
| gateway.logging.stdout.encoderPattern                                        | string                                | `"%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n"`                                                                                                                                                                                                                                                                                                                 |
| gateway.logging.stdout.json                                                  | string                                | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.name                                                                 | string                                | `"gateway"`                                                                                                                                                                                                                                                                                                                                                                            |
| gateway.reloadOnConfigChange                                                 | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.replicaCount                                                         | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| gateway.resources.limits.cpu                                                 | string                                | `"500m"`                                                                                                                                                                                                                                                                                                                                                                               |
| gateway.resources.limits.memory                                              | string                                | `"512Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.resources.requests.cpu                                               | string                                | `"200m"`                                                                                                                                                                                                                                                                                                                                                                               |
| gateway.resources.requests.memory                                            | string                                | `"256Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| gateway.service.externalPort                                                 | int                                   | `82`                                                                                                                                                                                                                                                                                                                                                                                   |
| gateway.service.internalPort                                                 | int                                   | `8092`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.service.internalPortName                                             | string                                | `http`                                                                                                                                                                                                                                                                                                                                                                                 |
| gateway.service.type                                                         | string                                | `"ClusterIP"`                                                                                                                                                                                                                                                                                                                                                                          |
| gateway.ssl.clientAuth                                                       | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.ssl.enabled                                                          | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| gateway.type                                                                 | string                                | `"Deployment"`                                                                                                                                                                                                                                                                                                                                                                         |
| license.key                                                                  | string                                | license.key file encoded in base64                                                                                                                                                                                                                                                                                                                                                     |
| mongo.auth.enabled                                                           | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| mongo.auth.password                                                          | string                                | `nil`                                                                                                                                                                                                                                                                                                                                                                                  |
| mongo.auth.source                                                            | string                                | `"admin"`                                                                                                                                                                                                                                                                                                                                                                              |
| mongo.auth.username                                                          | string                                | `nil`                                                                                                                                                                                                                                                                                                                                                                                  |
| mongo.connectTimeoutMS                                                       | int                                   | `30000`                                                                                                                                                                                                                                                                                                                                                                                |
| mongo.dbhost                                                                 | string                                | `"mongo-mongodb-replicaset"`                                                                                                                                                                                                                                                                                                                                                           |
| mongo.dbname                                                                 | string                                | `"gravitee"`                                                                                                                                                                                                                                                                                                                                                                           |
| mongo.dbport                                                                 | int                                   | `27017`                                                                                                                                                                                                                                                                                                                                                                                |
| mongo.rs                                                                     | string                                | `"rs0"`                                                                                                                                                                                                                                                                                                                                                                                |
| mongo.rsEnabled                                                              | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| mongo.socketKeepAlive                                                        | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| mongo.sslEnabled                                                             | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| mongodb-replicaset.auth.adminPassword                                        | string                                | `"password"`                                                                                                                                                                                                                                                                                                                                                                           |
| mongodb-replicaset.auth.adminUser                                            | string                                | `"username"`                                                                                                                                                                                                                                                                                                                                                                           |
| mongodb-replicaset.auth.enabled                                              | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| mongodb-replicaset.auth.key                                                  | string                                | `"keycontent"`                                                                                                                                                                                                                                                                                                                                                                         |
| mongodb-replicaset.auth.metricsPassword                                      | string                                | `"password"`                                                                                                                                                                                                                                                                                                                                                                           |
| mongodb-replicaset.auth.metricsUser                                          | string                                | `"metrics"`                                                                                                                                                                                                                                                                                                                                                                            |
| mongodb-replicaset.configmap                                                 | object                                | `{}`                                                                                                                                                                                                                                                                                                                                                                                   |
| mongodb-replicaset.enabled                                                   | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| mongodb-replicaset.image.repository                                          | string                                | `"mongo"`                                                                                                                                                                                                                                                                                                                                                                              |
| mongodb-replicaset.image.tag                                                 | float                                 | `3.6`                                                                                                                                                                                                                                                                                                                                                                                  |
| mongodb-replicaset.persistentVolume.accessModes\[0]                          | string                                | `"ReadWriteOnce"`                                                                                                                                                                                                                                                                                                                                                                      |
| mongodb-replicaset.persistentVolume.enabled                                  | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| mongodb-replicaset.persistentVolume.size                                     | string                                | `"1Gi"`                                                                                                                                                                                                                                                                                                                                                                                |
| mongodb-replicaset.replicaSetName                                            | string                                | `"rs0"`                                                                                                                                                                                                                                                                                                                                                                                |
| mongodb-replicaset.replicas                                                  | int                                   | `3`                                                                                                                                                                                                                                                                                                                                                                                    |
| mongodb-replicaset.resources.limits.cpu                                      | string                                | `"500m"`                                                                                                                                                                                                                                                                                                                                                                               |
| mongodb-replicaset.resources.limits.memory                                   | string                                | `"512Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| mongodb-replicaset.resources.requests.cpu                                    | string                                | `"100m"`                                                                                                                                                                                                                                                                                                                                                                               |
| mongodb-replicaset.resources.requests.memory                                 | string                                | `"256Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| smtp.enabled                                                                 | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| smtp.from                                                                    | string                                | `"info@example.com"`                                                                                                                                                                                                                                                                                                                                                                   |
| smtp.host                                                                    | string                                | `"smtp.example.com"`                                                                                                                                                                                                                                                                                                                                                                   |
| smtp.password                                                                | string                                | `"example.com"`                                                                                                                                                                                                                                                                                                                                                                        |
| smtp.port                                                                    | int                                   | `25`                                                                                                                                                                                                                                                                                                                                                                                   |
| smtp.properties.auth                                                         | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| smtp.properties.starttlsEnable                                               | bool                                  | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| smtp.subject                                                                 | string                                | `"[gravitee] %s"`                                                                                                                                                                                                                                                                                                                                                                      |
| smtp.username                                                                | string                                | `"info@example.com"`                                                                                                                                                                                                                                                                                                                                                                   |
| ui.autoscaling.enabled                                                       | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| ui.autoscaling.maxReplicas                                                   | int                                   | `3`                                                                                                                                                                                                                                                                                                                                                                                    |
| ui.autoscaling.minReplicas                                                   | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| ui.autoscaling.targetAverageUtilization                                      | int                                   | `50`                                                                                                                                                                                                                                                                                                                                                                                   |
| ui.autoscaling.targetMemoryAverageUtilization                                | int                                   | `80`                                                                                                                                                                                                                                                                                                                                                                                   |
| ui.enabled                                                                   | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| ui.image.pullPolicy                                                          | string                                | `"Always"`                                                                                                                                                                                                                                                                                                                                                                             |
| ui.image.repository                                                          | string                                | `"graviteeio/am-management-ui"`                                                                                                                                                                                                                                                                                                                                                        |
| ui.ingress.annotations."ingress.kubernetes.io/configuration-snippet"         | string                                | `"etag on;\nproxy_pass_header ETag;\n"`                                                                                                                                                                                                                                                                                                                                                |
| ui.ingress.annotations."kubernetes.io/app-root"                              | string                                | `"/"`                                                                                                                                                                                                                                                                                                                                                                                  |
| ui.ingress.annotations."kubernetes.io/ingress.class"                         | string                                | `"nginx"`                                                                                                                                                                                                                                                                                                                                                                              |
| ui.ingress.annotations."kubernetes.io/rewrite-target"                        | string                                | `"/"`                                                                                                                                                                                                                                                                                                                                                                                  |
| ui.ingress.enabled                                                           | bool                                  | `true`                                                                                                                                                                                                                                                                                                                                                                                 |
| ui.ingress.hosts\[0]                                                         | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| ui.ingress.path                                                              | string                                | `"/"`                                                                                                                                                                                                                                                                                                                                                                                  |
| ui.ingress.tls\[0].hosts\[0]                                                 | string                                | `"am.example.com"`                                                                                                                                                                                                                                                                                                                                                                     |
| ui.ingress.tls\[0].secretName                                                | string                                | `"api-custom-cert"`                                                                                                                                                                                                                                                                                                                                                                    |
| ui.name                                                                      | string                                | `"management-ui"`                                                                                                                                                                                                                                                                                                                                                                      |
| ui.replicaCount                                                              | int                                   | `1`                                                                                                                                                                                                                                                                                                                                                                                    |
| ui.resources.limits.cpu                                                      | string                                | `"100m"`                                                                                                                                                                                                                                                                                                                                                                               |
| ui.resources.limits.memory                                                   | string                                | `"128Mi"`                                                                                                                                                                                                                                                                                                                                                                              |
| ui.resources.requests.cpu                                                    | string                                | `"50m"`                                                                                                                                                                                                                                                                                                                                                                                |
| ui.resources.requests.memory                                                 | string                                | `"64Mi"`                                                                                                                                                                                                                                                                                                                                                                               |
| ui.service.externalPort                                                      | int                                   | `8002`                                                                                                                                                                                                                                                                                                                                                                                 |
| ui.service.internalPort                                                      | int                                   | `80`                                                                                                                                                                                                                                                                                                                                                                                   |
| ui.service.internalPortName                                                  | string                                | `http`                                                                                                                                                                                                                                                                                                                                                                                 |
| ui.service.name                                                              | string                                | `"nginx"`                                                                                                                                                                                                                                                                                                                                                                              |
| ui.service.type                                                              | string                                | `"ClusterIP"`                                                                                                                                                                                                                                                                                                                                                                          |
| userManagement.activity.enabled                                              | boolean                               | `false`                                                                                                                                                                                                                                                                                                                                                                                |
| userManagement.activity.anon.algorithm                                       | enum(`SHA256`, `SHA512`, `NONE`)      | `SHA256`                                                                                                                                                                                                                                                                                                                                                                               |
| userManagement.activity.anon.salt                                            | string                                | `null`                                                                                                                                                                                                                                                                                                                                                                                 |
| userManagement.activity.retention.time                                       | int                                   | `3`                                                                                                                                                                                                                                                                                                                                                                                    |
| userManagement.activity.retention.unit                                       | `enum(java.time.temporal.ChronoUnit)` | `MONTHS`                                                                                                                                                                                                                                                                                                                                                                               |
| userManagement.activity.geolocation.variation.latitude                       | double                                | `0.07`                                                                                                                                                                                                                                                                                                                                                                                 |
| userManagement.activity.geolocation.variation.longitude:                     | double                                | `0.07`                                                                                                                                                                                                                                                                                                                                                                                 |

### Gravitee Alert trigger & settings

When alerts are enabled, you may want to define your own settings the alert triggers and for the risk\_assessment settings. To do so, you wan define triggers and settings under the alerts section of the `values.yaml`.

\{% code title="values.yaml" %\} \`

\`\`yaml alerts: enabled: true endpoints: - http://localhost:8072/ security: enabled: true username: admin password: adminadmin triggers: risk\_assessment: # You need the Risk Assessment Service plugin for these alerts geoVelocity: name: Geo velocity alert description: A geo velocity risk-based alert has been triggered assessments: LOW # Default is LOW severity: WARNING ipReputation: name: IP reputation alert description: An IP reputation risk-based alert has been triggered assessments: LOW # Default is LOW severity: WARNING unknownDevices: name: Unknown Device alert description: An unknown device risk-based alert has been triggered assessments: HIGH # Default is HIGH severity: WARNING too\_many\_login\_failures: name: "Too many login failures detected" description: "More than {threshold}% of logins are in failure over the last {window} second(s)" # the threshold rate in % to reach before notify. Default 10% of login failures. threshold: 10 # the minimum sample size. Default 1000 login attempts. sampleSize: 1000 # window time in seconds. Default 600s (10 minutes). window: 600 # severity of the alert (INFO, WARNING, CRITICAL). Default WARNING. severity: WARNING settings: risk\_assessment: settings: enabled: true # default is false devices: enabled: true # default is true thresholds: HIGH: 1 # Arbitrary value ipReputation: enabled: true # default is true thresholds: #Default is only LOW, but you can add more thresholds #percentage LOW: 1 #MEDIUM: 30 #HIGH: 70 geoVelocity: enabled: true # default is true thresholds: # meter per second, default is 0.2777778 (1km/h) LOW: 0.2777778 #MEDIUM: 6.9444445 # (25km/h) #HIGH: 69.444445 # (250km/h)

````

</div>

### OpenShift

The Gravitee Access Management Helm Chart supports OpenShift > 3.10 This chart is only supporting Ingress standard objects and not the specific OpenShift Routes, reason why OpenShift is supported started from 3.10.

There are two major considerations to have in mind when deploying Gravitee Access Management within OpenShift: 1\_ Use full host domain instead of paths for all the components (ingress paths are not well supported by OpenShift) 2\_ Override the security context to let OpenShift to define automatically the user-id and the group-id to run the containers.

Also, for Openshift to automatically create Routes from Ingress, you must define the ingressClassName to "none".

Here is a standard `values.yaml` used to deploy Gravitee APIM into OpenShift:

<div data-gb-custom-block data-tag="code" data-title='values.yaml'>

```yaml
api:
  ingress:
    ingressClassName: none
    path: /management
    hosts:
      - api-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
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

gateway:
  ingress:
    ingressClassName: none
    path: /
    hosts:
      - gw-graviteeio.apps.openshift-test.l8e4.p1.openshiftapps.com
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
````

By setting the value to `null` for `runAsUser` and `runAsGroup` it forces OpenShift to define the correct values for you while deploying the Helm Chart.

## Configure backend

AM can rely on different backends to prersist data. By default AM comes with MongoDB configuration but RDMS such as Postgres, MySQL, MariaDB and SQLServer are also supported. This section will provide samples to configure the AM backend using the AM Helm Chart.

### MongoDB

If you are using a managed MongoDB like MongoDB Atlas, you can simply define the mongo uri.

{% code title="MongoDB Altas" overflow="wrap" %}
```yaml
mongo:
  uri: mongodb+srv://<username>:<password>@<instance>.mongodb.net/<dbname>?retryWrites=true&w=majority&connectTimeoutMS=10000&maxIdleTimeMS=30000

management:
  type: mongodb

oauth2:
  type: mongodb
```
{% endcode %}

If you want to deploy a MongoDB ReplicaSet using the Helm Chart dependency, you simply have to enable it. The **dbhost** has to be defined using the name of the helm installation (in this example **am**) followed by **-mongodb-replicaset**.

{% hint style="danger" %}
This is not recommended for production environments.
{% endhint %}

{% code title="MongoDB ReplicaSet" %}
```yaml
mongodb-replicaset:
  enabled: true
  startupProbe:
    successThreshold	: 1

mongo:
  dbhost: am-mongodb-replicaset
  dbname: gravitee-am
```
{% endcode %}

### RDBMS: Postgres

{% code title="PostgreSQL configuration" overflow="wrap" %}
```yaml
jdbc:
  driver: postgresql
  host: <host>
  port: <port>
  database: <dbname>
  username: <username>
  password: <password>
  # URLs to download the drivers
  drivers:
    - https://jdbc.postgresql.org/download/postgresql-42.2.20.jar
    - https://repo1.maven.org/maven2/org/postgresql/r2dbc-postgresql/1.0.7.RELEASE/r2dbc-postgresql-1.0.7.RELEASE.jar
  pool:
    acquireRetry:  1
    initialSize: 0
    maxSize: 10
    maxIdleTime: 30000
    maxLifeTime: 30000
    maxAcquireTime: 0
    maxCreateConnectionTime: 0

management:
  type: jdbc

oauth2:
  type: jdbc
  
gateway:
  type: jdbc
```
{% endcode %}

### RDBMS: MySQL

{% code title="MySQL configuration" overflow="wrap" %}
```yaml
jdbc:
  driver: mysql
  host: <host>
  port: <port>
  database: <dbname>
  username: <username>
  password: <password>
  # URLs to download the drivers
  drivers:
    - https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.21/mysql-connector-java-8.0.21.jar
    - https://repo1.maven.org/maven2/io/asyncer/r2dbc-mysql/1.0.2/r2dbc-mysql-1.0.2.jar
  pool:
    acquireRetry:  1
    initialSize: 0
    maxSize: 10
    maxIdleTime: 30000
    maxLifeTime: 30000
    maxAcquireTime: 0
    maxCreateConnectionTime: 0

management:
  type: jdbc

oauth2:
  type: jdbc
  
gateway:
  type: jdbc
```
{% endcode %}

### RDBMS: MariaDB

{% code title="MariaDB configuration" overflow="wrap" %}
```sh
jdbc:
  driver: mariadb
  host: <host>
  port: <port>
  database: <dbname>
  username: <username>
  password: <password>
  # URLs to download the drivers
  drivers:
    - https://downloads.mariadb.com/Connectors/java/connector-java-2.7.3/mariadb-java-client-2.7.3.jar
    - https://repo1.maven.org/maven2/org/mariadb/r2dbc-mariadb/1.0.3/r2dbc-mariadb-1.0.3.jar
  pool:
    acquireRetry:  1
    initialSize: 0
    maxSize: 10
    maxIdleTime: 30000
    maxLifeTime: 30000
    maxAcquireTime: 0
    maxCreateConnectionTime: 0

management:
  type: jdbc

oauth2:
  type: jdbc
  
gateway:
  type: jdbc
```
{% endcode %}

### RDBMS: SQLServer

{% code title="SQLServer configuration" overflow="wrap" %}
```sh
jdbc:
  driver: sqlserver
  host: <host>
  port: <port>
  database: <dbname>
  username: <username>
  password: <password>
  # URLs to download the drivers
  drivers:
    - https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/8.4.1.jre11/mssql-jdbc-8.4.1.jre11.jar
    - https://repo1.maven.org/maven2/io/r2dbc/r2dbc-mssql/1.0.0.RELEASE/r2dbc-mssql-1.0.0.RELEASE.jar
  pool:
    acquireRetry:  1
    initialSize: 0
    maxSize: 10
    maxIdleTime: 30000
    maxLifeTime: 30000
    maxAcquireTime: 0
    maxCreateConnectionTime: 0

management:
  type: jdbc

oauth2:
  type: jdbc
  
gateway:
  type: jdbc
```
{% endcode %}

## Install AM Enterprise Edition

To enable the Enterprise Edition (EE) mode of Access Management, you have to mount the license file using a secret and specify which EE plugin to download in the `additionalPlugins` section for the Gateway and the API. This has to be done for the Management API and the Gateway services.

```yaml
gateway:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-saml2-generic/gravitee-am-identityprovider-saml2-generic-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-gateway/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license

api:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/am/plugins/idps/gravitee-am-identityprovider-saml2-generic/gravitee-am-identityprovider-saml2-generic-<version>.zip
  extraVolumeMounts: |
    - name: graviteeio-license
      mountPath: /opt/graviteeio-am-management-api/license
      readOnly: true
  extraVolumes: |
    - name: graviteeio-license
      secret:
        secretName: graviteeio-license
```

## Production Ready Configuration

In this section, you will find an example `values.yaml` file based on the [**Configure a Production-ready AM Environment**](configure-a-production-ready-am-environment.md) page.

### Disable the internal APIs

If not used, the recommendation is to disable the internal APIs on the AM API and AM Gateway components. This can be done by defining environment variables for both components.

{% code title="Disable AM API internal APIs" %}
```yaml
api:
  env:
    - name: gravitee_services_core_http_enabled
      value: "false"
```
{% endcode %}

{% code title="Disable AM Gateway internal APIs" %}
```yaml
gateway:
  env:
    - name: gravitee_services_core_http_enabled
      value: "false"
```
{% endcode %}

The AM Gateway provides a readiness probe that takes into account the number of domains synced at startup. If you want to use this probe, then you shouldn’t disable the internal APIs. Instead, we use the following configuration on the gateway:

{% code title="AM Gateway readiness probe" %}
```yaml
gateway:
  services:
    core:
      http:
        host: 0.0.0.0
  readinessProbe:
    domainSync: true
```
{% endcode %}

### Update the default users

By default, the Management API creates an admin user during the first service start-up. For security reasons, it is strongly recommended to disable this user definition and define your own users.

Disable the default inline provider with user admin and create your own admin user:

```yaml
api:
  env:
		# Disable the default inline provider
    - name: gravitee_security_defaultAdmin
      value: "false"
		# Create your own admin user
    - name: gravitee_security_providers_0_type
      value: memory
    - name: gravitee_security_providers_0_enabled
      value: "true"
    - name: gravitee_security_providers_0_passwordencodingalgo
      value: "BCrypt"
    - name: gravitee_security_providers_0_users_0_username
      value: "admin"
    - name: gravitee_security_providers_0_users_0_firstname
      value: "Administrator"
    - name: gravitee_security_providers_0_users_0_lastname
      value: "Administrator"
    - name: gravitee_security_providers_0_users_0_role
      value: "ORGANIZATION_OWNER"
    - name: gravitee_security_providers_0_users_0_password
      value: "$2a$..." #(BCrypt encoded password)
```

### Update the JWT secret & enable secured cookies

The "Secure" flag instructs a user’s browser to only send the cookie along with requests over HTTPS to in-scope addresses. The recommendation is to set the "Secure" flag to true on AM API and AM Gateway components. In addition, the default JWT secret for both AM API and AM Gateway components needs to be updated to guarantee the integrity of JWT signed by AM for some actions (ex: reset password link).

Update the JWT secret on AM API:

```yaml
api:
  jwt:
    secret: super_secret_JWT_string
    cookie:
      domain: .yourdomain.com
      secure: true
```

Update the JWT secret on AM Gateway:

```yaml
gateway:
  jwt:
    secret: super_secret_JWT_string
    cookie:
      domain: .yourdomain.com
      secure: true
  http:
    cookie:
      secure: true
```

### Update CORS policies & URL Redirects on AM Management API

Only selected and trusted domains should access AM (e.g. the AM console).

CORS and allowed redirections:

```yaml
api:
  env:
    - name: GRAVITEE_HTTP_CORS_ALLOWORIGIN
      value: https://am.console.yourdomain.com
    - name: gravitee_http_login_allowredirecturls
      value: https://am.console.yourdomain.com/login/callback
    - name: gravitee_http_logout_allowredirecturls
      value: https://am.console.yourdomain.com/logout/callback
```

### Mitigate Cross-Site Scripting (XSS) and Cross Site Framing

The AM Gateway implements Content-Security-Policy and X-Frame-Options. It is recommended to use these two mechanisms to have better control over the resources the user agent is allowed to load for a given page and the CSRF secret must be updated.

```yaml
gateway:
  http:
    csrf:
      secret: super_secret_CSRF_string
    xframe:
      action: DENY
    csp:
      script-inline-nonce: true
      directives:
        - "default-src 'self';"
        - "script-src *.yourdomain.com https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs@3/dist/fp.min.js https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs-pro@3/dist/fp.min.js *.gstatic.com *.google.com;"
        - "img-src *.yourdomain.com data: 'unsafe-inline';"
        - "style-src *.yourdomain.com 'unsafe-inline';"
        - "frame-ancestors 'none';"
        - "frame-src 'self' https://www.google.com;"
```

### Values

This section regroups in a single place all the settings previously described on this page.

```yaml
api:
  env:
    - name: gravitee_services_core_http_enabled
      value: "false"
    - name: GRAVITEE_HTTP_CORS_ALLOWORIGIN
      value: https://am.console.yourdomain.com
    - name: gravitee_security_defaultAdmin
      value: "false"
    - name: gravitee_security_providers_0_type
      value: memory
    - name: gravitee_security_providers_0_enabled
      value: "true"
    - name: gravitee_security_providers_0_passwordencodingalgo
      value: "BCrypt"
    - name: gravitee_security_providers_0_users_0_username
      value: "admin"
    - name: gravitee_security_providers_0_users_0_firstname
      value: "Administrator"
    - name: gravitee_security_providers_0_users_0_lastname
      value: "Administrator"
    - name: gravitee_security_providers_0_users_0_role
      value: "ORGANIZATION_OWNER"
    - name: gravitee_security_providers_0_users_0_password
      value: "$2a$..."
    - name: gravitee_http_login_allowredirecturls
      value: https://am.console.yourdomain.com/login/callback
    - name: gravitee_http_logout_allowredirecturls
      value: https://am.console.yourdomain.com/logout/callback
  jwt:
    secret: super_secret_JWT_string
    cookie:
      domain: .yourdomain.com
      secure: true
  image:
    tag: 3.18.0
  autoscaling:
    enabled: false
  replicaCount: 1
  deployment:
    strategy:
      rollingUpdate:
        maxUnavailable: 0
  ingress:
    path: /management
    hosts:
      - am.api.yourdomain.com
    tls:
      - hosts:
          - am.api.yourdomain.com
        secretName: am-api-cert
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
  extraVolumeMounts: |
    - name: gravitee-license
      mountPath: /opt/graviteeio-am-management-api/license
      readOnly: true
  extraVolumes: |
    - name: gravitee-license
      secret:
        secretName: gravitee-license

gateway:
  enabled: true
  env:
    - name: gravitee_services_core_http_enabled
      value: "false"
  http:
    cookie:
      secure: true
    csrf:
      secret: super_secret_CSRF_string
    xframe:
      action: DENY
    csp:
      script-inline-nonce: true
      directives:
        - "default-src 'self';"
        - "script-src *.yourdomain.com https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs@3/dist/fp.min.js https://cdn.jsdelivr.net/npm/@fingerprintjs/fingerprintjs-pro@3/dist/fp.min.js *.gstatic.com *.google.com;"
        - "img-src *.yourdomain.com data: 'unsafe-inline';"
        - "style-src *.yourdomain.com 'unsafe-inline';"
        - "frame-ancestors 'none';"
        - "frame-src 'self' https://www.google.com;"
  jwt:
    secret: super_secret_JWT_string
    cookie:
      domain: .yourdomain.com
      secure: true
  image:
    tag: 3.18.0
  autoscaling:
    enabled: false
  replicaCount: 1
  deployment:
    strategy:
      rollingUpdate:
        maxUnavailable: 0
  resources:
    limits:
      memory: 1024Mi
    requests:
      memory: 768Mi
  ingress:
    path: /
    hosts:
      - am.gateway.yourdomain.com
    tls:
      - hosts:
          - am.gateway.yourdomain.com
        secretName: am-gateway-cert
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
      nginx.ingress.kubernetes.io/proxy-buffer-size: "64k"
      nginx.ingress.kubernetes.io/proxy-buffers-number: "8"
      nginx.ingress.kubernetes.io/proxy-body-size: "5m"
  extraVolumeMounts: |
    - name: gravitee-license
      mountPath: /opt/graviteeio-am-gateway/license
      readOnly: true
  extraVolumes: |
    - name: gravitee-license
      secret:
        secretName: gravitee-license

ui:
  image:
    tag: 3.18.0
  autoscaling:
    enabled: false
  replicaCount: 1
  ingress:
    path: /
    hosts:
      - am.console.yourdomain.com
    tls:
      - hosts:
          - am.console.yourdomain.com
        secretName: am-console-cert
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
```
