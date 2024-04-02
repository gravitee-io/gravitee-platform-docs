# Plugins

## Overview

Plugins can be installed to expand the capabilities of Gravitee APIM Gateway, APIM Management API (mAPI), AM, or Alert Engine (AE). They can customize the component’s behavior to satisfy needs and technical constraints.

{% hint style="info" %}
For more technical information about plugins, including details of their directory structure and how to create your own, see the [Custom Plugins Guide](../guides/developer-contributions/custom-plugins.md).
{% endhint %}

## Types of plugins

The table below lists the different types of plugins you can use with APIM and the component(s) they can be plugged into, respectively:

<table><thead><tr><th width="133">Type</th><th width="102" data-type="checkbox">Gateway</th><th width="92" data-type="checkbox">mAPI</th><th width="101" data-type="checkbox">AM</th><th width="90" data-type="checkbox">AE</th><th>Examples</th></tr></thead><tbody><tr><td><a href="plugins.md#alert">Alert</a></td><td>true</td><td>true</td><td>false</td><td>false</td><td>Vertx</td></tr><tr><td><a href="plugins.md#connector">Connector</a></td><td>true</td><td>true</td><td>false</td><td>false</td><td>Kafka, MQTT, WebSocket</td></tr><tr><td>Fetcher</td><td>false</td><td>true</td><td>false</td><td>false</td><td>HTTP, GIT</td></tr><tr><td><a href="plugins.md#identity-provider">Identity provider</a></td><td>false</td><td>true</td><td>false</td><td>false</td><td>LDAP, Oauth2, InMemory</td></tr><tr><td><a href="plugins.md#notifier">Notifier</a></td><td>false</td><td>false</td><td>false</td><td>true</td><td>Email, Slack, Webhook</td></tr><tr><td><a href="plugins.md#policy">Policy</a></td><td>true</td><td>true</td><td>false</td><td>false</td><td>API Key, Rate-limiting, Cache</td></tr><tr><td><a href="plugins.md#reporter">Reporter</a></td><td>true</td><td>false</td><td>false</td><td>false</td><td>Elasticsearch, Accesslog</td></tr><tr><td><a href="plugins.md#repository">Repository</a></td><td>true</td><td>true</td><td>false</td><td>false</td><td>MongoDB, Redis, Elasticsearch</td></tr><tr><td><a href="plugins.md#resource">Resource</a></td><td>true</td><td>true</td><td>false</td><td>false</td><td>Oauth2, Cache, LDAP</td></tr><tr><td><a href="plugins.md#secret-provider">Secret provider</a></td><td>true</td><td>true</td><td>true</td><td>false</td><td>Kubernetes, HC Vault</td></tr><tr><td>Services</td><td>true</td><td>true</td><td>false</td><td>false</td><td>Sync, local-registry, health-check, monitor</td></tr></tbody></table>

<details>

<summary>Alert</summary>

An alert is used to send triggers or events to the Alert Engine. These can be processed to send a notification via the configured plugin notifier. Configuring the notifier is the responsibility of the trigger.

</details>

<details>

<summary>Connector</summary>

A connector is used to add support for specific protocols, API styles, event brokers, and/or message queue services. For example, the Websocket and Kafka connector plugins allow you to front a Kafka topic with a Websocket API, making that Kafka topic consumable over a WebSocket connection.

</details>

<details>

<summary>Identity provider</summary>

An identity provider brokers trust with external user providers to authenticate and obtain information about end users. Out-of-the-box identity providers are:

* MongoDB
* In-memory
* LDAP / Active Directory
* OpenID Connect IdP (Azure AD, Google)

</details>

<details>

<summary>Notifier</summary>

A notifier is used to send notifications. The notifiers offered by Gravitee are:

* Email
* Slack
* Webhook

</details>

<details>

<summary>Policy</summary>

A policy modifies the behavior of the request or response handled by the Gateway. It can be considered a proxy controller, guaranteeing that a given business rule is fulfilled during request/response processing. Policies can be chained by a request or response policy chain using a logical order.&#x20;

Examples:

* Authorization using an API key&#x20;
* Applying header or query parameter transformations
* Applying rate limiting or quotas to avoid API flooding

See [Custom Policies ](../guides/developer-contributions/custom-policies.md)for how to create, use, and deploy a custom policy.

</details>

<details>

<summary>Reporter</summary>

A reporter is used by an APIM Gateway instance to report events such as:

* Request/response metrics (e.g., response-time, content-length, api-key)
* Monitoring metrics (e.g., CPU, Heap usage)
* Health-check metrics  (e.g., status, response code)

Out-of-the-box reporters:

* Elasticsearch Reporter
* File Reporter
* Metrics Reporter
* TCP reporter

You can create, use and deploy custom reporters as described in the [Custom Plugins](../guides/developer-contributions/custom-plugins.md) guide.

</details>

<details>

<summary>Repository</summary>

A repository is a pluggable storage component for API configuration, policy configuration, analytics, etc. See the [Repositories](../getting-started/configuration/repositories/) documentation for more information.

</details>

<details>

<summary>Resource</summary>

A resource can be added to an API for its whole lifecycle. APIM includes three default resources:

* Cache
* OAuth2 - Gravitee Access Management
* OAuth2 - Generic Authorization Server

See [Resources](../guides/api-configuration/resources.md) for more information.

</details>

<details>

<summary>Secret provider</summary>

A secret provider resolves secrets to avoid exposing plain text passwords and secrets keys in the `gravitee.yml` file. For example, users can store their MongoDB password in a secret manager like HashiCorp Vault and then resolve it when the platform starts.&#x20;

</details>

## Deployment

Deploying a plugin is as easy as copying the plugin archive (zip) into the dedicated directory. By default, you need to deploy the archives in `${GRAVITEE_HOME/plugins}`. Refer to [APIM Gateway Configuration ](../getting-started/configuration/apim-gateway/general-configuration.md#configure-the-plugins-directory)for more information on modifying the directory structure.

{% hint style="warning" %}
You must restart APIM nodes when applying new or updated plugins.
{% endhint %}

## Discovery and loading

Plugin discovery and loading occurs regardless of APIM license type. If a plugin is not included with your license, then it will be loaded but it will not be functional.

### Phase 1: Discover plugins

When APIM starts, all plugin zip files are read from the list of plugin directories set in the `gravitee.yaml` configuration file.&#x20;

{% hint style="info" %}
This operation is completed asynchronously for performance benefits.
{% endhint %}

If duplicates are found (same type and ID), the most recent file is kept regardless of the plugin's version. This allows for easily overriding plugins.

Plugin override circumvents the need to remove plugins to use a newer version, which is a huge benefit for Kubernetes deployments via Gravitee's Helm Chart. This also benefits plugin developers, as they can pack and copy an updated plugin without having to script the removal of the old version.

### Phase 2: Load plugins

After APIM finishes traversing the plugin directories, the plugins are loaded.&#x20;

Plugins are immediately initialized by a specialized handler. If an error occurs while unpacking a plugin zip file, the faulty plugin is ignored. An error will be reported in the logs and the loading of the remaining plugins will resume.

The loading process is sequential and adheres to the following order based on plugin type:

1. Cluster
2. Cache
3. Repository
4. Alert
5. Cockpit
6. Any other types

The rest of the plugins are loaded in no particular order, except if they have dependencies. If a plugin depends on another plugin, that takes precedence over type ordering.

For example, if `plugin1 (type:cluster)` depends on `plugin2 (type:cache)` which depends on `plugin3(type:alert)`, then the plugins are loaded in the following order:

* `plugin3` (because plugin 2 depends on it,  even if it is #4 in the type priority list)
* `plugin2` (because plugin 1 depends on it, even if it is #2 in the type priority list)
* `plugin1`
