# ReleaseNotes

### Release Date:

### Highlights

* The new Developer Portal supports Gravitee Markdown, which extends standard Markdown with dynamic UI components such as blocks, buttons, cards, and grids.
* The new Developer Portal (tech preview) lets administrators customize top-level navigation by creating pages, folders, and links in portal settings.
* APIM 4.10 introduces an AI Token Rate Limit policy for LLM proxy APIs that enforces a maximum total of inbound and outbound tokens over a configurable time window.
* Running the prompt guard rails capability requires ONNX runtime support in the gateway container.
* APIM can enforce prompt guard rails on LLM Proxy APIs using an AI text-classification model to evaluate incoming prompts for policy violations.
* With Redis distributed sync enabled, a new Gateway instance can bootstrap and continue serving APIs even when the management database is down and the original primary gateway is stopped.
* In a Bridge-based deployment, gateways can continue synchronizing through Redis distributed sync even if the Bridge component crashes.
* MCP Proxy APIs can be secured end-to-end with OAuth 2.0 by combining APIM OAuth2 plans (token verification and access control) with Gravitee Access Management as the authorization server.
* The new Developer Portal supports configurable authentication to control access.
* APIM 4.10+ new Developer Portal can require users to authenticate before accessing any portal content.
* Consumers can create applications in the new Developer Portal to subscribe to API plans and obtain credentials unless an API uses a keyless plan.
* API publishers can enable and tune runtime logging for v4 Proxy APIs and v4 Message APIs, and separately enable webhook logging for webhook-based v4 Message APIs.

### Breaking Changes

### New Features

**Add new GMD customization to New Dev Portal docs**

{% hint style="warning" %}
The new Developer Portal (tech preview) lets administrators customize top-level navigation by creating pages, folders, and links in portal settings.
{% endhint %}

* The new Developer Portal supports Gravitee Markdown, which extends standard Markdown with dynamic UI components such as blocks, buttons, cards, and grids. Buttons support multiple appearances and can link to internal portal routes or external URLs with configurable targets, and cards support structured content with theming and custom styling inputs. This enables richer documentation layouts and interactive content without custom front-end work.
* The new Developer Portal (tech preview) lets administrators customize top-level navigation by creating pages, folders, and links in portal settings. Pages and folders can optionally require authentication, allowing you to restrict documentation sections to signed-in users while keeping other items public. This enables a more tailored portal structure and access control without custom development.

**Add token rate limit policy to the docs**

* APIM 4.10 introduces an AI Token Rate Limit policy for LLM proxy APIs that enforces a maximum total of inbound and outbound tokens over a configurable time window. Because token usage is only known after a response is generated, enforcement operates with a one-request latency. The policy supports strict blocking, availability-first pass-through, or asynchronous enforcement, and limits can be applied by subscription/plan or a custom key (optionally key-only) with optional rate-limit response headers.

**Proxy your LLMs doc**

* Running the prompt guard rails capability requires ONNX runtime support in the gateway container. Alpine-based gateway images are not compatible, so a Debian-based APIM gateway image is required to use the text-classification model at runtime.
* APIM can enforce prompt guard rails on LLM Proxy APIs using an AI text-classification model to evaluate incoming prompts for policy violations. The guard rails checks can detect content such as profanity, sexually explicit language, harmful intent, and jailbreak/prompt-injection attempts before requests are forwarded.
* APIM 4.10 introduces an LLM Proxy API that exposes an OpenAI-compatible interface to clients while automatically adapting requests to supported LLM providers such as OpenAI, Gemini, and Bedrock. This enables you to apply APIM capabilities like subscriptions, policies, and analytics to LLM traffic, with additional token-aware statistics and rate limiting for LLM usage.
* APIM 4.10 adds an LLM proxy that exposes an OpenAI-compatible API and routes requests to supported LLM providers. It translates OpenAI-format requests into provider-specific formats and maps responses back, so clients can call one API surface while targeting OpenAI, Gemini, AWS Bedrock Converse, or other OpenAI-compatible providers. Supported endpoints include /chat/completions, /responses, and /embeddings for text-only use cases.
* LLM proxy feature support varies by provider: Bedrock does not support streaming and has strict embeddings constraints (single-string input and limited dimensions), while Gemini supports streaming and array embeddings with different token-usage behavior. OpenAI features such as tool/function calling, multimodal inputs, multiple completion choices, and logit bias/logprobs are not supported across providers. Unsupported optional parameters may be ignored, and incompatible requests return explicit errors to help clients implement fallbacks.
* When using streaming responses with the LLM Proxy, token tracking can be disabled for stream mode. Disabling token tracking can reduce visibility into token usage and may prevent token-based usage statistics and rate limiting from working correctly.
* LLM proxies can enforce token budgets by applying the AI Token Rate Limit policy to request flows, returning a rate-limit error when the configured token threshold is exceeded within the time window. The policy may fail on Alpine-based APIM Gateway Docker images due to missing ONNX runtime support; use a Debian-based gateway image variant (for example, graviteeio/apim-gateway:4.8.0-debian) when enabling this policy.
* OpenAI Python SDK clients can call the Gravitee LLM Proxy by pointing the SDK base URL to the gateway and LLM proxy context path. Requests must include the Gravitee API key via the x-gravitee-api-key header so the gateway can authenticate and authorize calls through the proxy.

**Redis distributed sync**

* With Redis distributed sync enabled, a new Gateway instance can bootstrap and continue serving APIs even when the management database is down and the original primary gateway is stopped. The deployed state stored in Redis allows API calls to keep succeeding during database outages, improving availability for consumers.
* In a Bridge-based deployment, gateways can continue synchronizing through Redis distributed sync even if the Bridge component crashes. A newly added gateway can join the cluster and pull the deployed state from Redis to serve API traffic without requiring the Bridge to be available.
* Gateway clustering can automatically elect a new primary (master) node when the current master goes offline. The new master uses the synchronization state stored in Redis to resume coordination without requiring a full resynchronization cycle, helping clusters fail over quickly while continuing to serve API traffic.

**Secure MCP Proxy with OAuth2**

* MCP Proxy APIs can be secured end-to-end with OAuth 2.0 by combining APIM OAuth2 plans (token verification and access control) with Gravitee Access Management as the authorization server. MCP clients can use dynamic client registration to onboard automatically, then authenticate to obtain access tokens that are required for gateway access to MCP server tools and resources.

**Update New dev portal docs for AM integration**

* The new Developer Portal supports configurable authentication to control access. You can authenticate users with local login/password or with single sign-on (SSO), and you can enforce authentication so only authenticated users can access the portal.
* APIM 4.10+ new Developer Portal can require users to authenticate before accessing any portal content. When force authentication is enabled, unauthenticated visitors are redirected to the login screen, limiting portal access to verified users and improving security for private APIs and assets.
* APIM 4.10+ new Developer Portal can authenticate users with a username and password. You can back this authentication with in-memory users, LDAP, or APIM itself as the identity source, enabling controlled access and role-based permissions. Using APIM as a data source also enables user self-registration and is required when OAuth2 is used for portal sign-in.
* APIM 4.10+ new Developer Portal can use SSO to authenticate users via supported identity providers, including Gravitee Access Management, social providers, Microsoft Entra ID, and OpenID Connect. Identity providers can be activated per organization/environment, and you can optionally disable local login so users can sign in only through SSO.

**Update portal documentation to reflect changes**

* Consumers can create applications in the new Developer Portal to subscribe to API plans and obtain credentials unless an API uses a keyless plan. The portal supports multiple application types (Simple, SPA, Web, Native, and Backend-to-Backend), including Dynamic Client Registration (DCR) options for OAuth/OIDC-based apps and optional client certificate and client metadata settings.

**Webhook logs/analytics**

* API publishers can enable and tune runtime logging for v4 Proxy APIs and v4 Message APIs, and separately enable webhook logging for webhook-based v4 Message APIs. Message API logging supports multiple sampling modes, including windowed count, to capture representative traffic without excessive overhead. Logging configuration can also enable OpenTelemetry tracing (with optional verbose tracing) to correlate log records with trace spans during troubleshooting.
* Platform administrators can configure gateway-wide API logging controls, including maximum full-logging duration, audit tracking, and whether end-user details are captured for OAuth2/JWT plans. For v4 Message APIs, the gateway supports multiple message sampling strategies—probabilistic, count, temporal, and windowed count—to limit log volume and resource usage. System-level defaults and limits can be enforced so API publishers can't exceed safe logging rates in high-throughput environments.
* APIM can display runtime logs for v4 Proxy APIs and v4 Message APIs, and it can also display webhook logs for v4 Message APIs that use a webhook entrypoint. Runtime logs can be filtered by time period, entrypoint, HTTP method, and plan, while webhook logs can be filtered by time period, HTTP status, application, and (optionally) callback URL. This makes it easier to troubleshoot both API traffic and webhook callback behavior from operational history.

### Updated features

**Update database support in the docs-GKO 1492**

* APIM's Elasticsearch connector support has been expanded to include Elasticsearch 9.2.x and OpenSearch 3.x, in addition to previously supported versions. This allows analytics and reporting to run against newer Elasticsearch/OpenSearch clusters without requiring a different repository type.

**Update documentation show new EL support : APIM 11412**

* The AWS Lambda policy now supports asynchronous invocation for proxy and message API requests, returning a standard API response to the consumer without waiting for the Lambda execution to complete. This enables background processing patterns where Lambda work continues after the client request finishes.
* AWS credentials used by the AWS Lambda policy (access key and secret key) can now be retrieved securely from a secret provider such as Vault using Gravitee Expression Language. This reduces the need to store long-lived credentials directly in policy configuration.
* Quota, Rate Limit, and Spike Arrest policies now support a dynamic period duration (dynamicPeriodTime) that can be resolved at runtime, including secure retrieval from a secret provider such as Vault via Gravitee Expression Language. When set, this dynamic value is used when the static periodTime is omitted or set to 0, enabling per-request or environment-driven period sizing.

**Update Kafka Gateway doc for broker delegation**

* Kafka Gateway endpoint configuration adds support for delegating SASL authentication to the Kafka broker via the Delegate to Broker mechanism, allowing clients to authenticate using supported broker-side mechanisms such as PLAIN or AWS MSK IAM. AWS MSK IAM delegation requires hosting the Kafka Gateway on AWS; otherwise authentication fails. OAuthBearer token authentication can also use fixed tokens or dynamically resolve tokens using Gravitee Expression Language.

**Update New dev portal docs for AM integration**

* Developer Portal authentication is now configured through the new Developer Portal authentication model (including enforcing authenticated access and selecting the authentication method) rather than relying on the legacy portal force-login configuration snippet. This aligns portal access control with the new portal's authentication mechanisms.

**Update-OpenTelemetry-documentation**

* OpenTelemetry tracing is described as two levels: standard tracing is always active and captures request/response flow, policy execution timing, errors, and conditional policy trigger recording. Optional verbose mode adds detailed events on each policy span, including headers and context attributes before and after policy execution, which increases trace volume and may affect performance. This helps you choose the right balance between troubleshooting detail and overhead.
