# APIM 4.10

## Release Date: January 8, 2025

## Highlights

* AI Token Rate Limit policy enforces inbound and outbound token budgets for LLM Proxy APIs.
* LLM Proxy exposes OpenAI-compatible endpoints and routes requests to providers like OpenAI, Gemini, and Bedrock.
* Redis distributed sync improves Gateway availability and enables faster clustering failover during database or Bridge outages.
* MCP Proxy APIs can be secured end-to-end with OAuth 2.0 using APIM OAuth2 plans and Gravitee Access Management.
* New Developer Portal supports Gravitee Markdown and customizable navigation.
* New Developer Portal authentication can be enforced with local login or SSO providers such as AM, Entra ID, and OIDC.
* Consumers can create portal applications to subscribe to plans and obtain credentials, except for keyless plans.
* v4 runtime and webhook logging supports sampling, filterable log views, and optional OpenTelemetry correlation.
* Elasticsearch connector now supports Elasticsearch 9.2.x and OpenSearch 3.x.
* AWS Lambda policy supports asynchronous invocation and secret-provider credentials via Gravitee Expression Language.
* Kafka Gateway supports SASL Delegate to Broker authentication, including AWS MSK IAM when hosted on AWS.

## Breaking Changes

#### Kafka Native APIs Analytics

* In APIM 4.10.0, Elasticsearch indices used by Kafka Native APIs have been modified for better compatibility with OpenSearch and better accuracy.
* You might have to do a roll-over of your `gravitee-event-metrics` index.
* Previous indexed document is deleted. However they are no longer be taken into account in Gravitee Dashboards.

## New Features

#### **AI Token Rate Limit policy**

* APIM 4.10 introduces an AI Token Rate Limit policy for LLM proxy APIs that caps total inbound and outbound tokens per time window; enforcement is one-request delayed and supports blocking, pass-through, or asynchronous modes with subscription/plan or custom keys.

#### **LLM Proxy**

* APIM 4.10 introduces an LLM Proxy that exposes an OpenAI-compatible interface and adapts requests to supported providers such as OpenAI, Gemini, and Bedrock, enabling subscriptions, policies, analytics, and token-aware usage statistics for LLM traffic.
* APIM 4.10 supports the following LLM providers: Bedrock, Gemini, OpenAI API, and OpenAI compatible LLM. Each provider has different capabilities: Bedrock does not support streaming and has stricter embeddings constraints, while Gemini supports streaming array embeddings, and tool calling; unsupported OpenAI options, for example tool calling or multimodal inputs, may be ignored or rejected with explicit errors.
* The Prompt Guard Rails policy can evaluate prompts with an AI text-classification model to block content such as profanity, sexually explicit language, harmful intent, and jailbreak/prompt-injection attempts, but require ONNX runtime support and a Debian-based Gateway image (Alpine images are not compatible).
* With the Toke Rate Limit policy, you can configure your LLM proxy to limit the number of total inbound tokens and the number of total outbound tokens allowed over a limited period of time in minutes and seconds.&#x20;

#### **Gateway cluster sync with Redis**

* Gateways can bootstrap and continue serving APIs from Redis distributed sync even when the management database is unavailable, improving availability during outages.
* In Bridge deployments, Gateways can keep synchronizing through Redis distributed sync and new nodes can join using state stored in Redis even if the Bridge component crashes.
* Gateway clusters can elect a new primary node and resume coordination from Redis state without a full resynchronization cycle for faster failover.

#### **OAuth2 security for MCP Proxy**

* MCP Proxy APIs can be secured end-to-end with OAuth 2.0 by combining APIM OAuth2 plans with Gravitee Access Management as the authorization server; clients can use dynamic client registration and must present access tokens to access MCP tools and resources.

#### **New Developer Portal enhancements**

{% hint style="warning" %}
The New Developer Portal is in tech preview.
{% endhint %}

**Navigation customization**

* You can customize the navigation of your New Developer Portal. You can customize the top-level navigation items to include individual pages, folders, and links to other pages or content. Also, you can customize navigations for each section by adding pages, links, or sub-folders to a section.
* You can customize the individual pages with the editor using Gravitee Markdown, which is standard Markdown enriched with Gravitee Markdown components.

**Authentication**

* The New Developer Portal supports configurable authentication and can enforce sign-in so only authenticated users can access portal content; unauthenticated visitors are redirected to the login screen when force authentication is enabled.
* Local username and password authentication can use in-memory users, LDAP, or APIM as the identity source; using APIM enables self-registration and is required when OAuth2 is used for portal sign-in.
* Single sign-on is supported with the following providers: Gravitee Access Management, social providers, Microsoft Entra ID, and OpenID Connect, and. Also, you can disable login with username and password so users must use single sign-on to access your New Developer Portal.

**Applications**

* Consumers can create applications in the New Developer Portal to subscribe to plans and obtain credentials unless an API uses a keyless plan, with multiple application types, and OAuth/OIDC DCR options plus optional client certificate and client metadata settings.

#### **v4 runtime and webhook logs**

* API publishers can enable runtime logging for v4 Proxy and v4 Message APIs and enable webhook logging for webhook-based v4 Message APIs, with sampling modes (including windowed count) to control volume and overhead.
* Platform administrators can enforce Gateway-wide logging defaults and limits (for example full-logging duration, audit tracking, and end-user capture for OAuth2/JWT plans) so publishers can't exceed safe logging rates in high-throughput environments.
* Runtime and webhook logs are viewable and filterable (runtime: time, entrypoint, HTTP method, plan; webhooks: time, HTTP status, application, and optional callback URL) and can be correlated with OpenTelemetry tracing, including optional verbose tracing.

#### Environment-level analytics dashboard for v4 Proxy APIs

* Users can view analytics for their v4 Proxy APIs at the environment level in the analytics section of their APIM Console.&#x20;
* The V4 API analytics dashboard provides you with clear visibility into the API performance and traffic patterns for all of your V4 Proxy APIs at the environment level.&#x20;
* The dashboard shows the following key metrics:
  * **Requests**.
  * **Error Rate**.
  * **Average latency**.
  * **Average response time of the Gateway**.&#x20;

## Updated features

#### **Elasticsearch and OpenSearch support**

* APIM's Elasticsearch connector now supports Elasticsearch 9.2.x and OpenSearch 3.x for analytics and reporting without requiring a different repository type.

#### **Policy updates for Lambda and rate limits**

* The AWS Lambda policy now supports asynchronous invocation for proxy and message API requests, returning a standard response without waiting for Lambda execution to complete.
* AWS Lambda policy credentials (access key and secret key) can be retrieved from a secret provider such as Vault using Gravitee Expression Language instead of being stored directly in policy configuration.
* Quota, Rate Limit, and Spike Arrest policies support a dynamic period duration (dynamicPeriodTime) that is resolved at runtime (including via a secret provider); it is used when the static periodTime is omitted or set to 0.

#### **Kafka broker delegation authentication**

* Kafka Gateway endpoint configuration supports delegating SASL authentication to the broker (for example PLAIN or AWS MSK IAM); AWS MSK IAM delegation requires hosting the Kafka Gateway on AWS, and OAuthBearer tokens can be fixed or resolved with Gravitee Expression Language.

#### **Portal authentication configuration model**

* Developer Portal authentication is configured through the new portal authentication model (enforced access and authentication method selection) rather than the legacy force-login configuration snippet.

#### **OpenTelemetry tracing verbosity**

* OpenTelemetry tracing is documented as always-on standard tracing plus an optional verbose mode that adds detailed per-policy span events (including headers and context attributes), increasing trace volume and potential performance overhead.
