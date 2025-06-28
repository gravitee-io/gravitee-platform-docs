# Plugins

## Overview

Plugins can be installed to expand the capabilities of Gravitee APIM Gateway, APIM Management API (mAPI), AM, or Alert Engine (AE). They can customize the component’s behavior to satisfy needs and technical constraints.

{% hint style="info" %}
For more technical information about plugins, including details of their directory structure and how to create your own, see the [Custom Plugins Guide](customization.md).
{% endhint %}

## Types of plugins

The table below lists the different types of plugins you can use with APIM and the component(s) they can be plugged into, respectively:

<table><thead><tr><th width="133">Type</th><th width="102" data-type="checkbox">Gateway</th><th width="92" data-type="checkbox">mAPI</th><th width="101" data-type="checkbox">AM</th><th width="90" data-type="checkbox">AE</th><th>Examples</th></tr></thead><tbody><tr><td>Alert</td><td>true</td><td>true</td><td>false</td><td>false</td><td>Vertx</td></tr><tr><td>Connector</td><td>true</td><td>true</td><td>false</td><td>false</td><td>Kafka, MQTT, WebSocket</td></tr><tr><td>Fetcher</td><td>false</td><td>true</td><td>false</td><td>false</td><td>HTTP, GIT</td></tr><tr><td>Identity provider</td><td>false</td><td>true</td><td>false</td><td>false</td><td>LDAP, Oauth2, InMemory</td></tr><tr><td>Notifier</td><td>false</td><td>false</td><td>false</td><td>true</td><td>Email, Slack, Webhook</td></tr><tr><td>Policy</td><td>true</td><td>true</td><td>false</td><td>false</td><td>API Key, Rate-limiting, Cache</td></tr><tr><td>Reporter</td><td>true</td><td>false</td><td>false</td><td>false</td><td>Elasticsearch, Accesslog</td></tr><tr><td>Repository</td><td>true</td><td>true</td><td>false</td><td>false</td><td>MongoDB, Redis, Elasticsearch</td></tr><tr><td>Resource</td><td>true</td><td>true</td><td>false</td><td>false</td><td>Oauth2, Cache, LDAP</td></tr><tr><td>Secret provider</td><td>true</td><td>true</td><td>true</td><td>false</td><td>Kubernetes, HC Vault, AWS</td></tr><tr><td>Services</td><td>true</td><td>true</td><td>false</td><td>false</td><td>Sync, local-registry, health-check, monitor</td></tr></tbody></table>

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

See [Custom Policies ](../../policies/custom-policies.md)for how to create, use, and deploy a custom policy.

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

You can create, use and deploy custom reporters as described in the [Custom Plugins](customization.md) guide.

</details>

<details>

<summary>Repository</summary>

A repository is a pluggable storage component for API configuration, policy configuration, analytics, etc.

</details>

<details>

<summary>Resource</summary>

A resource can be added to an API for its whole lifecycle. APIM includes three default resources:

* Cache
* OAuth2 - Gravitee Access Management
* OAuth2 - Generic Authorization Server

</details>

<details>

<summary>Secret provider</summary>

A secret provider resolves secrets to avoid exposing plain text passwords and secrets keys in the `gravitee.yml` file or in V4 APIs. For example, users can store their MongoDB password in a secret manager like HashiCorp Vault and then resolve it when the platform starts. As well, user my want to secure a password in resource plugin, or a sensitive header in an API definition.&#x20;

</details>
