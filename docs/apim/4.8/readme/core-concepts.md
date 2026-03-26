---
description: An overview about core concepts.
---

# Core Concepts

## Overview

The implementation of Gravitee's API management capabilities hinge on the following core concepts.

* An **API** is the proxy that sits between clients and the backend.
* An **endpoint** is the backend service that can be exposed to the client. Endpoints are part of the configuration for an API.
* A **Gateway** is the runtime that takes in requests from a client, processes the request, talks to the endpoint, transforms the response, and returns it to the client. APIs are deployed to a Gateway.
* **Plans** define what kind of authentication a service requires before talking to an API, and other rules that clients must respect when connecting. Plans can require that API keys, OAuth tokens, JWT tokens, or client TLS certificates (mTLS) are used for authentication.
* **Policies** are actions that the Gateway takes when processing requests and responses. Policies do things like transform HTTP headers, enforce that TLS is used, change the content of the request body, run scripts, or call out to another HTTP service.
* **Subscriptions** are made by clients to get access to plans. Subscriptions may require validation, or may be automatically accepted. Accepted subscriptions yield a credential that can be used by the client to access the API proxy.
* **Applications** are an intermediate layer between end users and their software clients. Subscriptions are done on behalf of an application, not a specific user or client. This is particularly useful when a client is not a person, but a program running in an automated software system, which is common. An application can have a client ID that is set up with OAuth to use dynamic credentials instead of a static API key.
* The **Management Console** is the control plane UI where APIs are configured. The Management Console has a Management API, which provides a standard model for creating resources in Gravitee. Gateways are registered to a Management API instance.
* The **Developer Portal** is a UI where subscribers of applications can view documentation, understand how to call an API, and get a credential to use a plan. A service publishes APIs to the Portal, and a client subscribes to the API plan in the Portal.

## Architecture

Gravitee offers three different API Management architecture schemes: [self-hosted](core-concepts.md#self-hosted-architecture), [hybrid](core-concepts.md#hybrid-architecture), and [Gravitee-managed](core-concepts.md#gravitee-managed-architecture). Each architecture relies on a specific set of Gravitee components. Some components are common to all architectures while others are architecture-specific.

Gravitee-managed architecture refers to a scheme where all Gravitee API Management components are Gravitee-managed SaaS components. Gravitee Cloud and API Designer are optional and can be connected to a Gravitee-managed API Management installation.

The following table compares the component types and management of self-hosted and hybrid architectures.

<table><thead><tr><th width="326">Component</th><th data-type="checkbox">Self-hosted</th><th data-type="checkbox">Hybrid</th></tr></thead><tbody><tr><td>API Management Console</td><td>true</td><td>true</td></tr><tr><td>Management API</td><td>true</td><td>true</td></tr><tr><td>Developer Portal</td><td>true</td><td>true</td></tr><tr><td>APIM Gateway</td><td>true</td><td>true</td></tr><tr><td>Bridge Gateway</td><td>false</td><td>true</td></tr><tr><td>Config Database</td><td>true</td><td>true</td></tr><tr><td>Analytics Database</td><td>true</td><td>true</td></tr><tr><td>Logstash</td><td>false</td><td>true</td></tr><tr><td>Redis</td><td>false</td><td>true</td></tr><tr><td>Rate Limits Database</td><td>true</td><td>false</td></tr><tr><td>[Enterprise] Gravitee Cloud</td><td>true</td><td>true</td></tr><tr><td>[Enterprise] API Designer</td><td>true</td><td>true</td></tr><tr><td>[Enterprise] Alert Engine</td><td>true</td><td>true</td></tr></tbody></table>

### Component Descriptions

Component descriptions for the full catalog of Gravitee architecture components are summarized in the following table:

<table><thead><tr><th width="212.5213913690476">Component</th><th>Description</th></tr></thead><tbody><tr><td>APIM Console<br>(for API producers)</td><td>A web UI that provides easy access to several key APIM Management API services. API publishers can use it to publish APIs. Admins can configure global platform settings and specific Portal settings.</td></tr><tr><td>APIM Management API</td><td>A REST API to manage and configure the APIM Console and APIM Developer Portal. All exposed services are restricted by authentication and authorization rules.</td></tr><tr><td>APIM Developer Portal<br>(for API consumers)</td><td>A web UI that provides easy access to several key APIM API services. API consumers can manage their applications and discover/subscribe to published APIs.</td></tr><tr><td>APIM Gateway</td><td>The core component of the APIM platform. Unlike a traditional HTTP proxy, it can apply policies to transform, secure, or monitor APIs at the request and/or response phase of an API transaction.</td></tr><tr><td>Bridge Gateway</td><td>In a hybrid architecture using Gravitee Classic Cloud, this gateway exposes extra HTTP services to bridge HTTP calls to the underlying repository.</td></tr><tr><td>Config Database</td><td>A database that stores API Management data such as API definitions, users, applications, and plans.</td></tr><tr><td>Analytics Database</td><td>A database that stores Gateway events and logs. In a hybrid architecture using Gravitee Classic Cloud, the Analytics Database is supplemented by an "S3 Bucket."</td></tr><tr><td>Logstash</td><td>Collects and sends local Gateway logs/metrics to the Gravitee APIM SaaS Control Plane. Exclusive to a Classic Cloud hybrid architecture and hosted by users on-prem or in a private cloud.</td></tr><tr><td>Redis</td><td>A database for rate limit synchronized counters. Optionally acts as an external cache in accordance with the Cache policy. Exclusive to hybrid architectures and hosted by users on-prem or in a private cloud.</td></tr><tr><td>[Enterprise]<br>Gravitee Cloud</td><td>A tool for centralized, multi-environment/organization management of APIM and AM installations. Two versions are offered: Gravitee Next-Gen Cloud and Gravitee Classic Cloud.</td></tr><tr><td>[Enterprise]<br>API Designer</td><td>A drag-and-drop MindMap-based tool to quickly and intuitively design Swagger/OAS APIs and deploy mocked APIs for testing.</td></tr><tr><td>[Enterprise]<br>Alert Engine</td><td>Provides APIM/AM users with API platform monitoring via flexible alerting configurations and notification mechanisms.<br>It is triggered by pre-configured upstream conditions and does not require external components or a database.</td></tr></tbody></table>

## Configuration

Gravitee APIM consists of four components: Gateway, Management API, APIM Console, and Developer Portal. APIM components can be configured using:

1. Environment variables
2. System properties
3. The `gravitee.yaml` file

{% hint style="warning" %}
The order in which they are listed corresponds to their order of precedence. System properties override the `gravitee.yml` configuration and environment variables override all other configuration methods.
{% endhint %}

### Environment variables

You can override the default APIM configuration (`gravitee.yml`) and system properties by defining environment variables. Any property in the `yaml` file can be translated to an environment variable by prefixing the property with "gravitee" and using `camel_case` or dot notation.

{% hint style="warning" %}
Certain properties are case-sensitive and cannot use uppercase characters. We recommend using lowercase characters to define all Gravitee environment variables. To ensure compatibility and avoid or confusion, refer to your system documentation for environment variable naming best practices.
{% endhint %}

<details>

<summary>Environment variable override examples</summary>

**Example 1**

To override this property:

```yaml
management:
  mongodb:
    dbname: myDatabase
```

Define one of the following variables:

```
gravitee_management_mongodb_dbname=myDatabase
gravitee.management.mongodb.dbname=myDatabase
```

**Example 2**

Some properties are arrays:

```yaml
analytics:
  elasticsearch:
    endpoints:
      - https://my.first.endpoint.com
      - https://my.second.endpoint.com

security:
  providers:
    - type: ldap
      context-source-username: "cn=Directory Manager"
      context-source-password: "password"
```

To translate and override, define one of the following variables:

**`camel_case`**

```
gravitee_analytics_elasticsearch_endpoints_0=https://my.first.endpoint.com
gravitee_analytics_elasticsearch_endpoints_1=https://my.second.endpoint.com

gravitee_security_providers_0_type=ldap
gravitee_security_providers_0_contextsourceusername=cn=Directory Manager
gravitee_security_providers_0_contextsourcepassword=password
```

**Dot notation**

```
gravitee.analytics.elasticsearch.endpoints[0]=https://my.first.endpoint.com
gravitee.analytics.elasticsearch.endpoints[1]=https://my.second.endpoint.com

gravitee.security.providers[0]type=ldap
gravitee.security.providers[0]context-source-username=cn=Directory Manager
gravitee.security.providers[0]context-source-password=password
gravitee.security.providers[0].users[1].password=password
```

</details>

### System properties

You can override the default APIM configuration (`gravitee.yml`) by defining system properties.

<details>

<summary>System property override example</summary>

To override this property:

```yaml
management:
  mongodb:
    dbname: myDatabase
```

Add this property to the JVM:

```
-Dmanagement.mongodb.dbname=myDatabase
```

</details>

### The `gravitee.yaml` file

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
YAML format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}
