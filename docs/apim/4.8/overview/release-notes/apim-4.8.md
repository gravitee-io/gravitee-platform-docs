# APIM 4.8

## Release Date: 2025/06/19

## Highlights

* **Agent Mesh:** Introduced Gravitee Agent Mesh, which has the following features:
  * Agent Catalog. A centralized catalog of all the AI agents built across your organization.
  * LLM Proxy. The LLM Proxy sits on top of LLM models models to provide a layer of abstraction between AI agents and LLMs.
  * A2A Proxy. A v4 Message API that communicates using the Agent-to-Agent (A2A) protocol, which allows you to apply API management principles to the interactions between AI agents.&#x20;
  * Agent Tool Server. You can convert v4 proxy APIs to MCP Tools and expose them.
* **AccessPoint for the Kafka Gateway:** Introduced support for AccessPoint in the Kafka Gateway, enabling multi-tenant routing based on API definition listener's host and routing mode.
* **Ability to expose metrics for the Kafka Gateway to Prometheus:** Introduced the ability to expose metrics for your Kafka Gateway with Prometheus.
* **Developer Portal upgrade:** Upgraded the Developer Portal to Angular 19.

## Breaking Changes and Deprecations

* **Support for the Classic Developer Portal reduced:** Gravitee continues to implement fixes for the Classic Developer Portal; but there are no new features planned for the Classic Developer Portal.
* **Deprecated APIM Standalone components:** The APIM standalone components that were available to download from [Gravitee.io downloads - apim/components](https://download.gravitee.io/#graviteeio-apim/components/) are no longer available or supported. You can use the full distribution .ZIP file instead. To download the full distribution .ZIP file, go to [Gravitee.io downloads - apim/distributions](https://download.gravitee.io/#graviteeio-apim/distributions/).
* **Removal of v1 APIs:** Starting from 4.9, v1 APIs are not supported by APIM.
* **Lucene update 10:** Lucene has been upgraded to 10. Before starting the Management API (mAPI), you must clean the `/data` directory in your `GRAVITEE_HOME` containing Lucene working files. Otherwise, the mAPI does not start. When mAPI restarts, it re-indexes.&#x20;
* **Custom plugin development:** If a plugin is referencing `io.gravitee.gateway.reactor.ReactableApi`, it needs to be recompiled with APIM 4.8 dependencies because `ReactableApi` it is now an interface rather than an abstract class. Without recompilation, the plugin throws a `java.lang.IncompatibleClassChangeError` .

## Product

### New Features

#### Agent Mesh

* Introduced Gravitee's new Agent Mesh, which has the following features:
  * Agent Catalog. A centralized catalog of all the AI agents built across your organization.
  * LLM Proxy. The LLM Proxy sits on top of LLM models models to provide a layer of abstraction between AI agents and LLMs.
  * A2A Proxy. A v4 Message API that communicates using the Agent-to-Agent (A2A) protocol, which allows you to apply API management principles to the interactions between AI agents.&#x20;
  * Agent Tool Server. You can convert v4 proxy APIs to MCP Tools and expose them.

#### AI policies

* Added two new policies for your AI agent:
  * Guard rails policy. This policy uses an AI-powered text classification model to evaluate user prompts for potentially inappropriate or malicious content.
  * Token tracking policy. This policy allows you to track of the number of tokens sent and received by an AI API.

#### **Kafka Gateway**

* Added three new policies for your Native API:
  * Transform Key policy. This policy adds a custom Kafka message key to your messages so that you can customize partitioning and perform general actions. For example, ordering the transactions.
  * Offloading policy. This Policy lets you configure the delegation of Kafka message content to storage.&#x20;
  * Message filtering policy (subscribe phase only). This policy allows fine-grained control over which Kafka messages should be delivered to consumers based on configurable filter expressions.

### Updates

#### New Docker images

*   We have introduced new Docker images based on Debian instead of Alpine. For 4.8 release, the usual tag (`4.8`, `4.8.0`, `4`) will remain the Alpine based images, and the Debian based images can be found with `-debian` suffix: `4-debian`, `4.8-debian` and `4.8.0-debian` .

    ⚠️ Debian based images are required to use the new Guard Rails policy introduced in APIM 4.8.\


    {% hint style="warning" %}
    Debian based images are required to use the new Guard Rails policy introduced in APIM 4.8.
    {% endhint %}

#### Debug mode is now compatible with V4 Proxy APIs

* Before APIM 4.8, Debug mode worked only with V2 APIs. Starting with 4.8, Debug mode now works with V2 APIs and V4 Proxy APIs. For more information about how to use Debug mode, see [debug-mode.md](../../policies/debug-mode.md "mention").

#### Webhook Improvements

* **Retry policy:** You can configure a retry policy for subscriptions to your Push plan. This updates ensures that push plans are restarted automatically.
* **Configure subscriptions through the New Developer Portal:** You can configure Webhook subscriptions through the New Developer Portal.

#### Kafka Gateway

* **AccessPoint:** Introduced support for AccessPoint in the Kafka Gateway, which enables multi-tenant routing based on API definition listener's host and routing mode. This update has the following benefits:
  * Allows for more granular control over API routing and message handling.
  * Supports routing based on host, path, or a combination of both.
  * Enables seamless integration with Kafka clusters for efficient message processing.
*   **Expose metrics to Prometheus:** From APIM 4.8, you can expose metrics for your Kafka Gateway to Prometheus. Here is a list of metrics that you can view for your Kafka Gateway:\


    | Metric                                            | What it measures                                                      |
    | ------------------------------------------------- | --------------------------------------------------------------------- |
    | net\_server\_active\_connections                  | Count of active Kafka connections opened by clients to the Gateway    |
    | net\_client\_active\_connections                  | Count of active connections from the Gateway to the Kafka brokers     |
    | kafka\_downstream\_produce\_topic\_records\_total | Total number of produced records received by the Gateway from clients |
    | kafka\_downstream\_produce\_topic\_record\_bytes  | Total bytes of produced records received by the Gateway from clients  |
    | kafka\_upstream\_produce\_topic\_records\_total   | Total number of produced records the Gateway sends to brokers         |
    | kafka\_upstream\_produce\_topic\_record\_bytes    | Total bytes of produced records the Gateway sends to brokers          |
    | kafka\_downstream\_fetch\_topic\_records\_total   | Total number of fetched records the Gateway sends to clients          |
    | kafka\_downstream\_fetch\_topic\_record\_bytes    | Total bytes of fetched records the Gateway sends to clients           |
    | kafka\_upstream\_fetch\_topic\_records\_total     | Total number of fetched records the Gateway receives from brokers     |
    | kafka\_upstream\_fetch\_topic\_record\_bytes      | Total bytes of fetched records the Gateway receives from brokers      |

#### Policy updates:

* **Retry:** The Retry policy now is compatible with V4 Proxy APIs.
* **Javascript:** The Javascript policy is now compatible with V4 Proxy APIs.
* **Rate Limit:** The Rate Limit policy is now compatible with V4 Message APIs.
* **Quota:** The Quota policy is now compatible with V4 message APIs.
* **Spike Arrest:** The Spike arrest policy is now compatible with V4 Message APIs.
* **Assign Attributes:** the assign attributes policy is now compatible with Native Kafka APIs.
* **Transform header:** the Transform header policy is now compatible with Native Kafka APIs.
* **Transform Protobuf <> JSON:** the Transform Protobuf <> JSON policy is now compatible with Native Kafka APIs.&#x20;

#### Developer Portal

* **Upgrade to Angular 19:** Upgraded the Developer Portal to Angular 19.
* **Custom CSS Support**: Introduced new Gravitee CSS tokens to facilitate customizing elements in the New Developer Portal.
* **New fonts:** Added the DM Mono and DM Sans as fonts that you can select for your portal customization.

#### Audit & Event Retention

* Audits data are cleaned based on a duration of retention. The clean is enabled by default and configured to keep 1 year of update. This can be configured in `gravitee.yaml` with
  * `services.audit.enabled` enable/disable this task
  * `services.audit.cron` when the task should be scheduled in [Spring cron format](https://spring.io/blog/2020/11/10/new-in-spring-5-3-improved-cron-expressions)
  * `services.audit.retention.days` retention duration in days
* Events are cleaned based on number of events by APIs. The clean is enabled by default and configured to keep the last 5 events of a specific type. This can be configured in `gravitee.yaml` with
  * &#x20;`services.events.enabled` enable/disable this task
  * `services.events.cron` when the task should be scheduled in [Spring cron format](https://spring.io/blog/2020/11/10/new-in-spring-5-3-improved-cron-expressions)
  * `services.events.keep` number of events kept by API
  * &#x20;`services.events.timeToLive` max duration of the task in minutes

#### API Management Console

* **Improved analytics page:** Improved the API analytics page within the API Management Console. This update provides the following benefits:&#x20;
  * Provides detailed insights into API usage, performance, and consumer behavior.
  * Includes advanced visualizations and filtering capabilities.
  * Supports data-driven decision-making for API lifecycle management.

### Fixes

* Resolved an issue where custom API keys were not applied correctly when creating subscriptions API plans.&#x20;
* Fixed a bug where APIs were not properly undeployed and disabled during updates.
* Addressed an error that occurred when attempting to extract the context path for Native APIs.
* Resolved an issue where updating a plan with an excluded group that does not exist would not throw a bad request exception.
* Fixed a bug where the validation process for excluded groups on v4 APIs did not throw a "Group Not Found" exception if no matching group was found.
* Resolved an issue where the export functionality for members, metadata, and plans of APIs v4 was not working correctly.
* Fixed a bug where the group selection logic did not display only the groups the user is a member of when the setting to add at least one group is enabled.
* Addressed an issue where searching users in the add members dialog was not disabled when the maximum allowed invitation limit was reached for a group.
* Fixed a bug where the default API and application roles were not initialized correctly for group members when adding them.
* Resolved an issue where the use of CORS methods in the API v2 debug mode was not disabled.
* Addressed an issue where the threshold value disappeared when switching the threshold type on the alert screen.
* Fixed a bug where the admin could not change API and application roles in the group when permitted.
* Resolved an issue where APIs federation versions were not displayed correctly in the federation pages.
* Fixed a bug where empty application pictures were ignored.
* Addressed an issue where 502 errors occurred when keepalive was activated with the v4 emulation engine.
* Fixed a bug where the calculation of the classic portal preview URL was incorrect when not in classic mode.
* Fixed a bug where the end-to-end test 9334 was not working as expected.
