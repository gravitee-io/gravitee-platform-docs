# Plugins

## Overview

Plugins are additional components that can be _plugged into_ [APIM Gateway](broken-reference) or [APIM API](broken-reference). They can customize the component’s behavior to exactly fit your needs and technical constraints.

For more information about plugins, including how to deploy them and details of their directory structure, see the [Plugins Developer Guide](../../dev-guide/dev-guide-plugins.md).

## Types of Plugins

The table below lists the different types of plugins you can use with APIM, with the component(s) they can be plugged into and some examples. For more details of what each plugin type does, see the sections below.

| Type                                                     | Component                       | Examples                                    |
| -------------------------------------------------------- | ------------------------------- | ------------------------------------------- |
| [Identity Providers](plugins.md#gravitee-plugins-idp)    | APIM API                        | LDAP, Oauth2, InMemory                      |
| Fetchers                                                 | APIM API                        | HTTP, GIT                                   |
| [Policies](plugins.md#gravitee-plugins-policies)         | <p>APIM API<br>APIM Gateway</p> | API Key, Rate-limiting, Cache               |
| [Reporters](plugins.md#gravitee-plugins-reporters)       | APIM Gateway                    | Elasticsearch, Accesslog                    |
| [Repositories](plugins.md#gravitee-plugins-repositories) | <p>APIM API<br>APIM Gateway</p> | MongoDB, Redis, Elasticsearch               |
| [Resources](plugins.md#gravitee-plugins-resources)       | <p>APIM API<br>APIM Gateway</p> | Oauth2, Cache, LDAP                         |
| Services                                                 | <p>APIM API<br>APIM Gateway</p> | Sync, local-registry, health-check, monitor |
| [Notifiers](plugins.md#gravitee-plugins-notifiers)       | Alert Engine                    | Email                                       |
| [Alerts](plugins.md#gravitee-plugins-alerts)             | <p>APIM API<br>APIM Gateway</p> | Vertx                                       |
| Connectors                                               | <p>APIM API<br>APIM Gateway</p> | Kafka, MQTT, Websocket                      |

### Identity Providers

An **identity provider** brokers trust with external user providers, to authenticate and obtain information about your end users.

Out-of-the-box identity providers are:

* MongoDB
* In-memory
* LDAP / Active Directory
* OpenID Connect IdP (Azure AD, Google)

### Policies

A **policy** modifies the behavior of the request or response handled by APIM Gateway. It can be chained by a request policy chain or a response policy chain using a logical order. Policies can be considered like a _proxy controller_, guaranteeing that a given business rule is fulfilled during request/response processing.

Examples of a policy are:

* Authorization using an API key (see the [api-key policy documentation](../../policy-reference/policy-apikey.md))
* Applying header or query parameter transformations
* Applying rate limiting or quotas to avoid API flooding

Want to know how to create, use, and deploy a custom policy? Check out the [Policies Developer Guide](../../dev-guide/dev-guide-policies.md).

### Reporters

A **reporter** is used by an APIM Gateway instance to report many types of event:

* Request/response metrics — for example, response-time, content-length, api-key
* Monitoring metrics — for example, CPU, Heap usage
* Health-check metrics — for example, status, response code

_Out-of-the-box_ reporters are :

* Elasticsearch Reporter
* File Reporter

As with all plugins, you can create, use and deploy custom reporters as described in the [Plugins Developer Guide](../../dev-guide/dev-guide-plugins.md).

### Repositories

A **repository** is a pluggable storage component for API configuration, policy configuration, analytics and so on. You can find more information in the [Repositories](../../getting-started/configuration/configuration/repositories/installation-guide-repositories.md) section of the Installation Guide.

### Resources

A **resource** can be added to an API for its whole lifecycle. APIM comes with three default resources:

* Cache
* OAuth2 - Gravitee Access Management
* OAuth2 - Generic Authorization Server

You can find more information in the [Resources](../../user-guide/publisher/resources/resources-overview.md) section of the API Publisher Guide.

### Notifiers

A **notifier** is used to send notifications. Currently, the only notifier available is the **email notifier**, but others including **slack** and **portal** are planned soon.

### Alerts

An **alert** is used to send triggers or events to the Alert Engine which can be processed to send a notification using the configured plugin notifier. Configuring the notifier is the responsibility of the trigger.

### Connectors

A connector is used to "Add" support for specific protocols, API styles, event brokers, and/or message queue services. For example, if you have the "Websocket" and "Kafka" connector plugins, you are able to "front" a Kafka topic with a Websocket API, making that Kafka topic consumable over a Websocket connection.&#x20;
