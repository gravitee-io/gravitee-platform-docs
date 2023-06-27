---
description: A detailed guide for installing and configuring a hybrid APIM deployment
---

# Advanced Hybrid Deployment

## Introduction

This documentation page relates to the installation of the client (On-Prem / Private Cloud) part of the API Management platform in a Hybrid architecture (SaaS + On-prem / Private cloud).

![Hybrid Architecture](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture.svg)

### SaaS Components <a href="#saas-components" id="saas-components"></a>

|                                             Component                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| :----------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                            <p>APIM Console<br>(for API producers)</p>                            | <p>This web UI gives easy access to some key APIM Management API services. <a href="../../#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</p>                                                                                                                                                                                                                |
|                                        APIM Management API                                       | <p>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../../reference/management-api-reference/"> Management API Reference</a> section.</p>                                                                                                                                          |
| <p><a href="../../guides/developer-portal/">APIM Developer Portal</a><br>(for API consumers)</p> | This web UI gives easy access to some key APIM API services. Allows [API Consumers](../../#api-consumer) to [manage their applications](../../guides/api-exposure-plans-applications-and-subscriptions/#applications) and search for, view, try out, and subscribe to a published API.                                                                                                                                                                                  |
|                                      APIM SaaS API Gateways                                      | <p>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../reference/policy-reference/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</p>                                               |
|                                          Bridge Gateways                                         | A _bridge_ API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)                                                                                                                                                                                                                                                                                           |
|                                          Config Database                                         | All the API Management platform management data, such as API definitions, users, applications, and plans.                                                                                                                                                                                                                                                                                                                                                               |
|                                  S3 Bucket + Analytics Database                                  | Analytics and logs data                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|                                <p>[Optional]<br>Gravitee Cloud</p>                               | Gravitee Cloud is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.                                                                                                                                                                                                                                                                                           |
|                                 <p>[Optional]<br>API Designer</p>                                | Drag-and-Drop graphical (MindMap) API designer to quickly and intuitively design your APIs (Swagger / OAS) and deploy mocked APIs for quick testing.                                                                                                                                                                                                                                                                                                                    |
|                                 <p>[Optional]<br>Alert Engine</p>                                | <p>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</p> |

### On-prem / Private cloud components[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#on-prem-private-cloud-components) <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

|   Component  | Description                                                                                                                                                                                                                                                                                                                                                                                                               |
| :----------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Gateway | <p>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../reference/policy-reference/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</p> |
|   Logstash   | Collect and send local Gateways logs and metrics to the Gravitee APIM SaaS Control Plane.                                                                                                                                                                                                                                                                                                                                 |
|     Redis    | The database used locally for rate limits synchronized counters (RateLimit, Quota, Spike Arrest) and optionally, as an external cache for the Cache policy.                                                                                                                                                                                                                                                               |

![Hybrid Architecture Connections](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture-connections.svg)

## Self-hosted hybrid gateway installation[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#installation) <a href="#installation" id="installation"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}






{% hint style="info" %}
**Additional assets**

* [Hybrid Deployment on Kubernetes](hybrid-deployment-on-kubernetes.md)
* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
Please follow the APIM install instructions laid out in the [Install on Docker](../install-guides/install-on-docker/) guide.

#### **Local file structure**

```
.
├── config
│   ├── gateway
│   │   └── gravitee.yml 

│   └── logstash
│       └── logstash.conf

├── docker-compose.yml
├── logs
│   └── apim-gateway-dev
└── plugins
    ├── gravitee-apim-repository-hazelcast-3.18.3.zip
    └── gravitee-apim-repository-redis-3.18.3.zip
```

#### **Download**&#x20;

**Download plugins**

* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

#### **plugins**

**Download plugins**

*   [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

    **Download plugins**

    *   [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

        **Download plugins**

        * [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
        *
* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
* [gravitee-apim-repository-hazelcast-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-hazelcast/gravitee-apim-repository-hazelcast-3.18.3.zip)
{% endtab %}

{% tab title="ZIP" %}
Please follow the APIM install instructions laid out in the [Install with `.ZIP`](../install-guides/install-with-.zip.md) guide.

**Download plugins**

* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
{% endtab %}
{% endtabs %}



## Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration) <a href="#configuration" id="configuration"></a>

There is at least 3 connections to configure :

* The connection to the SaaS Management plane with the Bridge Gateway.
* The connection to push Analytics and Logs with file or tcp reporter pushing data for logstash to send them to the SaaS storage.
* The connection the local rate limits database.
* \[Optional] The connection to the SaaS Alert Engine.

### **Management**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#management)

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

### **Analytics and Logs**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#analytics-and-logs)

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

### **Rate limits**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

### **Alert Engine**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

### **Gravite Cloud**

Follow cockpit instructions

Please follow directly the instruction you have on cockpit. `https://cockpit.gravitee.io/accounts/YOUR-ACCOUNT-HRID/installations/how-to`

### **Full example**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

## Redis Installation <a href="#redis" id="redis"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

## Logstash <a href="#logstash" id="logstash"></a>

### Installation <a href="#installation_2" id="installation_2"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}

{% endtab %}

{% tab title="Docker" %}

{% endtab %}

{% tab title="ZIP" %}

{% endtab %}
{% endtabs %}

### Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration\_2) <a href="#configuration_2" id="configuration_2"></a>

