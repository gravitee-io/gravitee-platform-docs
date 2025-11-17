# Plugins

## Overview

Plugins are additional components that can be _plugged into_ Gravitee API Management (APIM) Gateway or APIM Management API. They can customize the component’s behavior to exactly fit your needs and technical constraints.

{% hint style="info" %}
For more technical information about plugins, including details of their directory structure and how to create your own, see the [Custom Plugins Guide](../guides/developer-contributions/dev-guide-plugins.md).
{% endhint %}

## Types of Plugins

The table below lists the different types of plugins you can use with APIM, the component(s) they can be plugged into, and some examples. For more details of what each plugin type does, see the sections below.

| Type                                                                     | Component                       | Examples                                    |
| ------------------------------------------------------------------------ | ------------------------------- | ------------------------------------------- |
| [Identity Providers](plugins.md#identity-providers)                      | APIM API                        | LDAP, Oauth2, InMemory                      |
| Fetchers                                                                 | APIM API                        | HTTP, GIT                                   |
| [Policies](plugins.md#policies)                                          | <p>APIM API<br>APIM Gateway</p> | API Key, Rate-limiting, Cache               |
| [Reporters](plugins.md#reporters)                                        | APIM Gateway                    | Elasticsearch, Accesslog                    |
| [Repositories](../getting-started/configuration/configure-repositories/README.md) | <p>APIM API<br>APIM Gateway</p> | MongoDB, Redis, Elasticsearch               |
| [Resources](plugins.md#resources)                                        | <p>APIM API<br>APIM Gateway</p> | Oauth2, Cache, LDAP                         |
| Services                                                                 | <p>APIM API<br>APIM Gateway</p> | Sync, local-registry, health-check, monitor |
| [Notifiers](plugins.md#notifiers)                                        | Alert Engine                    | Email, Slack, Webhook                       |
| [Alerts](plugins.md#alerts)                                              | <p>APIM API<br>APIM Gateway</p> | Vertx                                       |
| Connectors                                                               | <p>APIM API<br>APIM Gateway</p> | Kafka, MQTT, Websocket                      |

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

* Authorization using an API key&#x20;
* Applying header or query parameter transformations
* Applying rate limiting or quotas to avoid API flooding

Want to know how to create, use, and deploy a custom policy? Check out the [Custom Policies Developer Guide](../guides/developer-contributions/dev-guide-policies.md).

### Reporters

A **reporter** is used by an APIM Gateway instance to report many types of event:

* Request/response metrics — for example, response-time, content-length, api-key
* Monitoring metrics — for example, CPU, Heap usage
* Health-check metrics — for example, status, response code

_Out-of-the-box_ reporters are :

* Elasticsearch Reporter
* Metrics Reporter
* File Reporter
* TCP reporter

As with all plugins, you can create, use and deploy custom reporters as described in the [Custom Plugins Developer Guide](../guides/developer-contributions/dev-guide-plugins.md).

### Repositories

A **repository** is a pluggable storage component for API configuration, policy configuration, analytics and so on. You can find more information in the [Repositories](../getting-started/configuration/configure-repositories/README.md) section of the Configuration Guide.

### Resources

A **resource** can be added to an API for its whole lifecycle. APIM comes with three default resources:

* Cache
* OAuth2 - Gravitee Access Management
* OAuth2 - Generic Authorization Server

You can find more information in the [Resources](../guides/api-configuration/resources.md) section of the documentation.

### Notifiers

A **notifier** is used to send notifications. Currently, Gravitee offers the following notifiers:

* Email
* Slack
* Webhook

### Alerts

An **alert** is used to send triggers or events to the Alert Engine which can be processed to send a notification using the configured plugin notifier. Configuring the notifier is the responsibility of the trigger.

### Connectors

A connector is used to "Add" support for specific protocols, API styles, event brokers, and/or message queue services. For example, if you have the "Websocket" and "Kafka" connector plugins, you are able to "front" a Kafka topic with a Websocket API, making that Kafka topic consumable over a WebSocket connection.

## Deployment

Deploying a plugin is as easy as copying the plugin archive (zip) into the dedicated directory. By default, you need to deploy the archives in `${GRAVITEE_HOME/plugins}`. Refer to the [APIM Gateway Configuration Documentation](../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-directory) for more information on modifying the directory structure.

{% hint style="warning" %}
You must restart APIM nodes when applying new or updated plugins.
{% endhint %}

## Discovery and Loading

Plugin discovery and loading is completed regardless of the APIM license you are using. If a plugin is not included with your license, then it will be loaded but it will not be functional.

### Phase 1: discover plugins

When APIM starts, all plugin zip files are read from the list of plugin directories set in the `gravitee.yaml` configuration file.&#x20;

{% hint style="info" %}
Note, that this operation is completed asynchronously for performance benefits.
{% endhint %}

If duplicates are found (same type and id), **the most recent file is kept regardless of the plugin's version.** This allows for easily overriding plugins.

Plugin override circumvents the need to remove plugins to use a newer version which is a huge benefit for Kubernetes deployments with Gravitee's Helm chart. This also benefits plugin developers as they can pack and copy an updated plugin without having to script the removal of the old version.

### Phase 2: load plugins

After APIM finishes traversing the plugin directories, the plugins are loaded.&#x20;

Plugins are immediately initialized by a specialized handler. If an error occurs while unpacking a plugin zip file, then the faulty plugin is ignored. An error will be reported in the logs and the loading of the remaining plugins will resume.

The loading process is sequential and adheres to the following order based on plugin type:

1. cluster
2. cache
3. repository
4. alert
5. cockpit
6. any other types

The rest of the plugins are loaded in no particular order, except if they have dependencies. If a plugin depends on another plugin, then that takes precedence over the type ordering.

For example, if `plugin1 (type:cluster)` depends on `plugin2 (type:cache)` which depends on `plugin3(type:alert)`, then the following will occur:

* `plugin3` (because plugin 2 depends on it,  even if this one is #4 in the type priority list)
* `plugin2` (because plugin 1 depends on it, even if this one is #2 in the type priority list)
* `plugin1`
