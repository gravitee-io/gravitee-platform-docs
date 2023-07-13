# Hybrid

## Introduction

This documentation page relates to the installation of the client (On-Prem / Private Cloud) part of the API Management platform in a Hybrid architecture (SaaS + On-prem / Private cloud).

![Hybrid Architecture](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture.svg)

### SaaS Components <a href="#saas-components" id="saas-components"></a>

|                        Component                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :-----------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|        <p>APIM Console<br>(for API producers)</p>       | <p>This web UI gives easy access to some key APIM Management API services. API publishers can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</p>                                                                                                                                                                                                                                                                                                                                                  |
| <p>APIM API Developer Portal<br>(for API consumers)</p> | <p>This web UI gives easy access to some key <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-rest-api">APIM API</a> services. <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-consumer">API Consumers</a> can use it to search for, view, try out and subscribe to a published API.<br>They can also use it to manage their <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-application">applications</a>.</p>                          |
|                   APIM Management API                   | <p>This RESTful API exposes services to manage and configure the <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-mgmt-ui">APIM Console</a> and <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-portal-ui">APIM Portal</a> web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the <a href="https://docs.gravitee.io/apim/3.x/apim_installguide_rest_apis_documentation.html">API Reference</a> section.</p> |
|                  APIM SaaS API Gateways                 | <p>APIM Gateway is the core component of the APIM platform. You can think of it like a smart proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="https://docs.gravitee.io/apim/3.x/apim_overview_plugins.html#gravitee-plugins-policies">policies</a> (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.</p>                                          |
|                     Bridge Gateways                     | A _bridge_ API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC and so on)                                                                                                                                                                                                                                                                                                                                                                                      |
|                     Config Database                     | All the API Management platform management data, such as API definitions, users, applications and plans.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|              S3 Bucket + Analytics Database             | Analytics and logs data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|               <p>[Optional]<br>Cockpit</p>              | Gravitee Cloud is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.                                                                                                                                                                                                                                                                                                                                                                                                 |
|            <p>[Optional]<br>API Designer</p>            | Drag-and-Drop graphical (MindMap based) API designer to quickly and intuitively design your APIs (Swagger / OAS) and even deploy mocked APIs for quick testing.                                                                                                                                                                                                                                                                                                                                                                                                        |
|            <p>[Optional]<br>Alert Engine</p>            | <p>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</p>                                                                                                |

### On-prem / Private cloud components[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#on-prem-private-cloud-components) <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

|   Component  | Description                                                                                                                                                                                                                                          |
| :----------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Gateway | APIM Gateway is the core component of the APIM platform, smartly proxing trafic applying policies.                                                                                                                                                   |
|   Logstash   | Collect and send local Gateways logs and metrics to the Gravitee APIM SaaS Control Plane.                                                                                                                                                         |
|     Redis    | Database use locally for rate limits synchronized counters (RateLimit, Quota, Spike Arrest) and optionnaly as an external cache for the [Cache policy](https://docs.gravitee.io/apim/3.x/apim\_resources\_cache\_redis.html#redis\_cache\_resource). |

![Hybrid Architecture Connections](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture-connections.svg)

## Self-hosted hybrid gateway[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#self-hosted-hybrid-gateway) <a href="#self-hosted-hybrid-gateway" id="self-hosted-hybrid-gateway"></a>

#### Installation[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#installation) <a href="#installation" id="installation"></a>

Kubernetes (Helm)DockerBinaries

Online documentation and assets

* [Install APIM on Kubernetes with the Helm Chart](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html)
* [Deploy a Hybrid architecture in Kubernetes](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_kubernetes.html)
* [Gravitee.io Helm Charts](https://artifacthub.io/packages/helm/graviteeio/apim3)

Prerequisites

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [Helm v3](https://helm.sh/docs/intro/install)

Steps :

1.  Add the Gravitee Helm charts repository.

    ```
    helm repo add graviteeio https://helm.gravitee.io
    ```
2.  Install using the `values.yaml` file.\
    [Here is the full `values.yaml` example](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values), please customize it following the [Configuration sections](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration).

    ```
    helm install graviteeio-apim3x graviteeio/apim3 -f values.yaml
    ```

#### Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration) <a href="#configuration" id="configuration"></a>

There is at least 3 connections to configure :

* The connection to the SaaS Management plane with the Bridge Gateway.
* The connection to push Analytics and Logs with file or tcp reporter pushing data for logstash to send them to the SaaS storage.
* The connection the local rate limits database.
* \[Optional] The connection to the SaaS Alert Engine.

**Management**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#management)

Kubernetes (Helm with `values.yaml` file)DockerGateway with `gravitee.yml` file

Into the `values.yaml` configuration file :

| values.yaml                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>
























</code></pre> | <pre><code>management:  type: httpgateway:  management:    http:      url: https://bridge-gateway-url:bridge-gateway-port      username: kubernetes://&#x3C;namespace>/secrets/&#x3C;my-secret-name>/&#x3C;my-secret-key>      password: kubernetes://&#x3C;namespace>/secrets/&#x3C;my-secret-name>/&#x3C;my-secret-key>      # ssl:      #   trustall: true      #   verifyHostname: true      #   keystore:      #     type: jks # Supports jks, pem, pkcs12      #     path: ${gravitee.home}/security/keystore.jks      #     password: secret      #   truststore:      #     type: jks # Supports jks, pem, pkcs12      #     path: ${gravitee.home}/security/truststore.jks      #     password: secret      # proxy:      #   host:      #   port:      #   type: http      #   username:      #   password:
</code></pre> |

Online documentation

* [Install APIM on Kubernetes with the Helm Chart](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html)
* [Deploy a Hybrid architecture in Kubernetes](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_kubernetes.html)
* [Gravitee.io Helm Charts](https://artifacthub.io/packages/helm/graviteeio/apim3)

**Analytics and Logs**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#analytics-and-logs)

Kubernetes (Helm)DockerGateway with `gravitee.yml` file

**FILES**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#files)

Into the `values.yaml` configuration file :

| values.yaml                     |                                                                                                                                         |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>






</code></pre> | <pre><code>gateway:  reporters:    tcp:      enabled: true      host: logstash      port: 8379      output: elasticsearch
</code></pre> |

**DIRECT (TCP)**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#direct-tcp)

Warning

Choosing the direct connection may result in a loss of data. If the connection between the gateway and logstash is broken the newly generated analytics and logs data will be lost.

Into the `values.yaml` configuration file :

| values.yaml                     |                                                                                                                                         |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>






</code></pre> | <pre><code>gateway:  reporters:    tcp:      enabled: true      host: logstash      port: 8379      output: elasticsearch
</code></pre> |

Online documentation

* [APIM hybrid deployment](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_deployment.html#configuration)
* [Full `values.yaml` example](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values)

**Rate limits**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#rate-limits)

Kubernetes (Helm)DockerGateway with `gravitee.yml` file

| values.yaml                     |                                                                                                                                    |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>






</code></pre> | <pre><code>ratelimit:  type: redisredis:  host: 'redis-host'  port: 6379  password: 'redis-password'  download: true
</code></pre> |

Online documentation

* [APIM hybrid deployment](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_deployment.html#configuration)
* [Full `values.yaml` example](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values)

**Alert Engine**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#alert-engine)

Kubernetes (Helm)DockerGateway with `gravitee.yml` file

Into the `values.yaml` configuration file :

| values.yaml                      |                                                                                                                                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>







</code></pre> | <pre><code>alerts:  enabled: true  endpoints:    - https://alert-engine-url:alert-engine-port  security:    enabled: true    username: alert-engine-username    password: alert-engine-password
</code></pre> |

Online documentation

* [Integrate AE with API Management](https://docs.gravitee.io/ae/apim\_installation.html#configuration)
* [Install APIM on Kubernetes with the Helm Chart](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html)
* [Deploy a Hybrid architecture in Kubernetes](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_kubernetes.html)
* [Gravitee.io Helm Charts](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values\&path=alerts)

**Cockpit**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#cockpit)

Follow Gravitee Cloud instructions

Please follow directly the instruction you have on cockpit. `https://cockpit.gravitee.io/accounts/YOUR-ACCOUNT-HRID/installations/how-to`

**Full example**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#full-example)

Kubernetes (Helm)Docker(VMs) Gateway with `gravitee.yml` file

Into the `values.yaml` configuration file :

| values.yaml                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <pre><code>





















</code></pre> | <pre><code>management:  type: httpgateway:  management:    http:      url: https://bridge-gateway-url:bridge-gateway-port      username: kubernetes://&#x3C;namespace>/secrets/&#x3C;my-secret-name>/&#x3C;my-secret-key>      password: kubernetes://&#x3C;namespace>/secrets/&#x3C;my-secret-name>/&#x3C;my-secret-key>  reporters:    tcp:      enabled: true      host: logstash      port: 8379      output: elasticsearchalerts:  enabled: true  endpoints:    - https://alert-engine-url:alert-engine-port  security:    enabled: true    username: alert-engine-username    password: alert-engine-password
</code></pre> |

Online documentation

* [Install APIM on Kubernetes with the Helm Chart](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html)
* [Deploy a Hybrid architecture in Kubernetes](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_kubernetes.html)
* [Gravitee.io Helm Charts - Values Template](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values)

### Redis[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#redis) <a href="#redis" id="redis"></a>

#### Installation[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#installation\_1) <a href="#installation_1" id="installation_1"></a>

Kubernetes (Helm)DockerVM

* [Bitnami helm charts](https://artifacthub.io/packages/helm/bitnami/redis)

#### Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration\_1) <a href="#configuration_1" id="configuration_1"></a>

Easy peasy

No specific configuration is needed.

### Logstash[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#logstash) <a href="#logstash" id="logstash"></a>

#### Installation[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#installation\_2) <a href="#installation_2" id="installation_2"></a>

Kubernetes (Helm)DockerVM

* [Official helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash)
* [Bitnami helm charts](https://bitnami.com/stack/logstash/helm)

#### Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration\_2) <a href="#configuration_2" id="configuration_2"></a>

Input TCP - Output S3 bucket

| logstash.conf                                   |                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <pre><code>






















</code></pre> | <pre><code>input {  tcp {      port => 8379      codec => "json"  }}filter {    if [type] != "request" {        mutate { remove_field => ["path", "host"] }    }}output {  s3 {    access_key_id => "${S3_ACEESS_KEY_ID}"    secret_access_key => "${S3_SECRET_ACCESS_KEY}"    region => "${S3_REGION}"    bucket => "${S3_BUCKET_NAME}"    size_file => 10485760    codec => "json_lines"  }}
</code></pre> |

Online documentation

* [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html)
