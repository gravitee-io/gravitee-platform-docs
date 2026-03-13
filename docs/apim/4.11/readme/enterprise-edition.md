---
description: An overview about enterprise edition.
metaLinks:
  alternates:
    - enterprise-edition.md
---

# Enterprise Edition

## Overview

The Enterprise Edition (EE) version of API Management (APIM) distribution can include API Management, Event Management, and AI Agent Management features andcapabilities.

The Gravitee APIM Enterprise Edition requires a [license](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing). Licenses are available as different packages, each offering a different level of access to enterprise features and capabilities. For more information, go to the [pricing page](https://www.gravitee.io/pricing).

## Global Enterprise Features

These capabilities provide foundational security, observability, and administrative control across your entire Gravitee deployment, regardless of the specific APIs or events you manage.

| Category   | Feature                                                                                                                                      | Description                                                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Core       | [Audit Trail](../analyze-and-monitor-apis/audit-trail.md)                                                                                    | Monitor platform and API behavior by auditing API consumption and activity per event type.                                                                          |
| Core       | [Custom Roles](../configure-and-manage-the-platform/manage-organizations-and-environments/authentication/roles-and-groups-mapping.md)        | Create specialized user roles by grouping permissions at the organization, environment, API, or application levels.                                                 |
| Core       | [Debug Mode](../create-and-configure-apis/apply-policies/debug-mode.md)                                                                      | Test, troubleshoot, and debug your policy execution and enforcement in real time.                                                                                   |
| Core       | [Dynamic Client Registration (DCR)](../how-to-guides/use-case-tutorials/configure-dcr.md)                                                    | Allow OAuth client applications to register seamlessly with an OAuth server through the OpenID Connect (OIDC) endpoint.                                             |
| Core       | [Enterprise OpenID Connect SSO](../configure-and-manage-the-platform/manage-organizations-and-environments/authentication/openid-connect.md) | Centralize user authentication using OpenID Connect Single Sign-On across your API Management platform.                                                             |
| Core       | [Sharding Tags](../configure-and-manage-the-platform/gravitee-gateway/sharding-tags.md)                                                      | Control exactly where an API is deployed. Tag specific Gateways with keywords and select the corresponding tag in the API's proxy settings to route the deployment. |
| Reporter   | [Cloud Reporter](../analyze-and-monitor-apis/reporters/)                                                                                     | Expose a secure endpoint for analytics propagated from a Gravitee Gateway to Elastic storage.                                                                       |
| Reporter   | [Datadog Reporter](../analyze-and-monitor-apis/reporters/datadog-reporter.md)                                                                | Send Gravitee API metrics directly to your Datadog instance for advanced dashboarding and observability.                                                            |
| Reporter   | [TCP Reporter](../analyze-and-monitor-apis/reporters/tcp-reporter.md)                                                                        | Stream Gateway events and metrics to a dedicated TCP listening server for custom monitoring integrations.                                                           |
| Repository | Bridge Gateway / HTTP Client                                                                                                                 | Deploy a repository proxy to synchronize data over HTTP, securing your database by avoiding direct external connections.                                            |
| Resource   | [Cache Redis](../create-and-configure-apis/configure-v2-apis/service-discovery.md)                                                           | Enterprise-grade distributed caching utilizing Redis for high availability. Supports standalone or Sentinel modes.                                                  |
| Resource   | GeoIP Service                                                                                                                                | Load GeoIP databases into memory, functioning as a prerequisite resource for the GeoIP Filtering policy.                                                            |

## API Management

Secure, optimize, and manage enterprise REST API traffic using advanced policies and standard HTTP protocols.

| Category    | Feature                                                                                                      | Description                                                                                                                         |
| ----------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Reactor     | Proxy Reactor                                                                                                | Handles traditional, synchronous HTTP request and response flows natively within the Gateway.                                       |
| Entrypoint  | [HTTP GET](../create-and-configure-apis/configure-v4-apis/entrypoints/http-get.md)                           | Front a backend or data source with a REST API supporting HTTP GET requests.                                                        |
| Entrypoint  | [HTTP POST](../create-and-configure-apis/configure-v4-apis/entrypoints/http-post.md)                         | Front a backend or data source with a REST API supporting HTTP POST requests.                                                       |
| Policy      | [Assign Metrics](../create-and-configure-apis/apply-policies/policy-reference/assign-metrics.md)             | Push custom metrics alongside natively provided request metrics to populate analytics dashboards or generate monetization invoices. |
| Policy      | [Data Logging Masking](../create-and-configure-apis/apply-policies/policy-reference/data-logging-masking.md) | Protect sensitive user data by configuring rules to conceal strings and variables in API logs.                                      |
| Policy      | [GeoIP Filtering](../create-and-configure-apis/apply-policies/policy-reference/geoip-filtering.md)           | Control access to your APIs by allowing or blocking IP addresses based on their physical distance or country of origin.             |
| Plugin Pack | Enterprise Policy Pack                                                                                       | A bundled pack of enterprise-grade policies necessary for strict, production API Management deployments.                            |

## Event Management

Mediate, expose, and secure asynchronous event streams by connecting to advanced messaging brokers and exposing APIs via event-driven entrypoints.

| Category   | Feature                                                                                                      | Description                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Reactor    | Message Reactor                                                                                              | Handles asynchronous, event-driven traffic and message streams natively within the Gateway.                        |
| Entrypoint | [Server-Sent Events (SSE)](../create-and-configure-apis/configure-v4-apis/entrypoints/server-sent-events.md) | Enable unidirectional, real-time communication from the server to the client.                                      |
| Entrypoint | [Webhook](../create-and-configure-apis/configure-v4-apis/entrypoints/webhook.md)                             | Allow consumers to subscribe to the Gravitee Gateway and retrieve streamed data in real time via a callback URL.   |
| Entrypoint | [WebSocket](../create-and-configure-apis/configure-v4-apis/entrypoints/websocket.md)                         | Send and retrieve streamed events and messages in real time using the WebSocket protocol.                          |
| Endpoint   | [Azure Service Bus](../create-and-configure-apis/configure-v4-apis/endpoints/azure-service-bus.md)           | Publish and subscribe to events in Azure Service Bus via HTTP and WebSocket mediation.                             |
| Endpoint   | [Kafka](../create-and-configure-apis/configure-v4-apis/endpoints/kafka.md)                                   | Publish and subscribe to Kafka events using HTTP and WebSocket mediation.                                          |
| Endpoint   | [MQTT5](../create-and-configure-apis/configure-v4-apis/endpoints/mqtt5.md)                                   | Publish and subscribe to messages on an MQTT 5.x broker (e.g., HiveMQ, Mosquitto).                                 |
| Endpoint   | [RabbitMQ](../create-and-configure-apis/configure-v4-apis/endpoints/rabbitmq.md)                             | Communicate seamlessly with a RabbitMQ resource using the AMQP 0-9-1 protocol.                                     |
| Endpoint   | [Solace](../create-and-configure-apis/configure-v4-apis/endpoints/solace.md)                                 | Publish and subscribe to messages on a Solace broker using the SMF protocol.                                       |
| Resource   | Confluent Schema Registry                                                                                    | Enterprise resource that fetches serialization and deserialization data directly from a Confluent schema registry. |

## AI Agent Management

Govern and manage the communication protocols required for building and securing AI agents.

| Category   | Feature        | Description                                                                                                        |
| ---------- | -------------- | ------------------------------------------------------------------------------------------------------------------ |
| Reactor    | A2A Proxy      | Dedicated V4 API type that enables agent-to-agent communication through the Gravitee API Management platform.      |
| Entrypoint | Agent to Agent | Support Google's Agent-to-Agent (A2A) protocol using SSE, HTTP GET, or HTTP POST methods for client consumption.   |
| Endpoint   | Agent to Agent | Support Google's Agent-to-Agent (A2A) protocol using SSE, HTTP GET, or HTTP POST methods for backend connectivity. |

## Alert Engine

Configure and manage proactive alerts across your entire API Management platform. Alert Engine is an enterprise **Plugin Pack** that allows you to monitor API traffic, health checks, and platform events, automatically triggering notifications to your preferred channels (e.g., Email, Slack, Webhooks) whenever specific conditions, anomalies, or thresholds are met.

## Hosting Options

Gravitee EE is an investment in deployment flexibility. Choose the deployment model that best aligns with your internal infrastructure, security, and operational constraints:

| Category   | Feature                                                                                                                | Description                                                                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deployment | [SaaS deployments](https://app.gitbook.com/s/QiHAMRWybFsowkRWSjCc/getting-started/getting-started-with-gravitee-cloud) | Let Gravitee fully host, manage, scale, and maintain all APIM components within its own enterprise-grade cloud environment, minimizing your operational overhead.       |
| Deployment | [Hybrid deployments](../hybrid-installation-and-configuration-guides/)                                                 | Gravitee hosts and manages the Control Plane within its cloud environment, while you securely host and manage the Gateway (data plane) within your own private network. |
| Deployment | [Fully self-hosted deployments](../self-hosted-installation-guides/)                                                   | Install and host APIM within your own private cloud/environment.                                                                                                        |
