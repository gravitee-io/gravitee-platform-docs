---
description: What the Gamma 4.13 release adds across API Management, Event Stream Management, and the other modules. Browse the new features and changes.
---

# Release Notes

Each Gamma version follows the support period of the API Management version it ships with. For release and end-of-life dates, see [Support Model](https://documentation.gravitee.io/apim/release-information/support-model).

## 4.13 new features

The 4.13 release adds the following capabilities.

### Agent Management

Agent Management adds AI Workspaces, which give a team governed access to chosen models with per-member budgets, spend tracking, and routing. LLM, MCP, and A2A Proxies gain API resources, broadcasts, metadata, property import, subscription export, and promotion to another environment. LLM Proxies gain Entrypoints, CORS, Failover, and **Models** pages, plus the **Cost Rate Limit** and **AI Token Compression** policies. They also read images, audio, video, and files in requests. LLM and A2A Proxies gain export, import, and duplicate, and A2A Proxies gain plans, subscriptions, and response templates. Agent Management also adds workflow tools, custom dashboards, and shadow AI agents from Edge Management, and runs on a JDBC management repository.

#### Gemini Enterprise Agent Platform provider

* The **Providers** page of the Catalog adds **Gemini Enterprise Agent Platform** as a provider. A provider is addressed by a **Project ID**, a **Region**, `global` by default, and a **Publisher**, **Google (Gemini)** or **Anthropic (Claude)**, rather than a URL.
* A service account key reaches Gemini and Claude models and requires a **Project ID**. An API key reaches Gemini models only, and without a **Project ID** it calls Google in express mode on the global host.
* The connection test and the save check the credential, the project, the region, the publisher, and every selected model against Google, and name what to fix. With a service account, the models Google lists for the publisher are offered for import, and **Add from registry** prices Gemini and Claude models from Google's public list.
* The models of these providers carry a **Gemini Enterprise Agent Platform** badge and a publisher badge in the **AI Models** list and in the **Add models from providers** panel. An LLM Proxy or an AI Workspace uses them by reference, and a service account key rotated in the vault applies to the gateway without a redeploy.
* See [Connect a Gemini Enterprise Agent Platform provider](../agent-management/import/connect-a-gemini-enterprise-agent-platform-provider.md).

#### AI Workspaces

* The **Secure** group of the Agent Management sidebar adds an **AI Workspaces** section that gives a team governed access to a chosen set of AI models. Each workspace holds the models its members can call, the budgets they're metered against, and the members themselves.
* A budget caps the dollars each member assigned to it may spend per hour, day, week, or month, charged at each model's real per-request cost, and optionally caps the requests each member sends per second, minute, hour, or day. A member who exhausts the budget is refused with `429`.
* Adding a user creates or reuses an application for them, subscribes it to the budget you pick, and issues an API key on that subscription.
* See [AI Workspaces](../agent-management/build/ai-workspaces/README.md).

#### Spend tracking for AI Workspaces

* The **Observability** group of each AI Workspace adds a **Spend** page that ranks the users, budgets, and models of the workspace by spend over a time range.
* **Export CSV** downloads the ranked users and models as one file named with the workspace ID and the dates of the time range.
* The AI Workspace Overview dashboard template charts requests, error rate, response time, tokens, and cost, with top-five breakdowns by model and by user.
* See [Track AI workspace spend](../agent-management/build/track-ai-workspace-spend.md) and [Monitor your AI workspaces](../agent-management/observe/monitor-your-ai-workspaces.md).

#### Router and AI Routing for AI Workspaces

* The **Router** page of each AI Workspace chains the policies every call of the workspace runs, whatever budget the member is on. Saving writes the router to every budget, and deploying the workspace applies it.
* The **AI Routing** policy picks the model that serves a request from the share of the member's budget already spent. Each band covers the share up to its limit and lists the models it routes to, and the last band catches everything left. The model it picks replaces the model the request names.
* See [Configure AI workspace routing](../agent-management/build/configure-ai-workspace-routing.md).

#### API Resources for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Resources** page that manages the resources the proxy's policies reference by name at runtime, such as caches, OAuth providers, and guardrail detectors.
* A resource change applies to the gateway when you deploy the proxy from the out-of-sync banner.
* See [Configure resources for your proxies](../agent-management/build/configure-resources-for-your-proxies.md).

#### Broadcasts for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Broadcasts** page under **Consumer Access** that sends a one-way announcement to the consumers of the proxy.
* Choose the **Portal Notifications**, **Email**, or **POST HTTP Message** channel.
* See [Broadcast messages to proxy consumers](../agent-management/build/broadcast-messages-to-proxy-consumers.md).

#### API metadata for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Metadata** page under **General** that lists the entries in effect for the proxy: the ones it holds a value for, together with the ones it inherits from its environment.
* The row menu offers **Override** on an entry the proxy only inherits, and **Edit** on one it owns.
* Metadata isn't part of the proxy definition, so a change takes effect without a deployment.
* See [Manage metadata for your proxies](../agent-management/build/manage-metadata-for-your-proxies.md).

#### Import and dynamic properties for LLM, MCP, and A2A Proxies

* The **Import** button on the **API Properties** page of each LLM Proxy, MCP Proxy, and A2A Proxy is now active. Paste one `KEY=value` pair per line to add new properties and replace the values of existing unencrypted properties.
* The **Manage dynamically** button is now active and opens the **Dynamic properties** page.
* A sync that changes the property list deploys the proxy automatically when the proxy was in sync.
* See [Configure properties for your proxies](../agent-management/build/configure-properties-for-your-proxies.md).

#### Plans and subscriptions for A2A Proxies

* The A2A Proxy detail view adds a **Consumer Access** group with a **Plans** page and a **Consumers** page.
* The **Plans** page lists the plans of the proxy by status, **Staging**, **Published**, **Deprecated**, or **Closed**, and creates plans of the five security types: **Keyless**, **API Key**, **JWT**, **OAuth2**, and **mTLS**.
* The **Consumers** page lists the subscriptions of the proxy, creates a subscription for an application, and approves, rejects, or closes each one.
* See [Manage A2A Proxy plans](../agent-management/build/configure-your-a2a-proxy/manage-a2a-proxy-plans.md) and [Manage subscriptions](../agent-management/publish/manage-subscriptions.md).

#### Subscription export for LLM, MCP, and A2A Proxies

* The **Consumers** page of each LLM Proxy, MCP Proxy, and A2A Proxy adds an **Export CSV** button that downloads the subscriptions matching the current **Status**, **Plan**, and **API Key** filters as a CSV file.
* The export holds every matching subscription, not only the current page of the table.
* See [Manage subscriptions](../agent-management/publish/manage-subscriptions.md).

#### Entrypoint configuration and navigation for LLM Proxies

* Each LLM Proxy detail view adds an **Entrypoints** page under **Design**. Add or remove context paths, switch the proxy to virtual hosts, and edit the options of the LLM Proxy entrypoint plugin after creation.
* The detail navigation is regrouped. **Models**, **Entrypoints**, **Endpoints**, **Policy Studio**, and **Resources** sit under **Design**, **Reporter Settings** and **Notifications** sit under **Monitoring**, **Security** follows **General**, and the **General** page is renamed **Configuration**. **LLM Studio** is renamed **Policy Studio**, and a link to the former page redirects to it.
* See [Configure LLM Proxy entrypoints](../agent-management/build/configure-llm-proxy-entrypoints.md).

#### Images, audio, video, and files in LLM Proxy requests

* LLM Proxies read images, audio, video, and files in requests sent in the OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, and Gemini formats.
* Four entrypoint options decide what happens to each content type: **Images sent by the client**, **Audio sent by the client**, **Video sent by the client**, and **Files sent by the client**. `ALLOW` forwards the content to the provider, `STRIP` removes it, and `REJECT` refuses the request with an HTTP `400` error and the code `modality_blocked`.
* Each option defaults to `STRIP`, because policies such as prompt guard rails inspect only text. An LLM Proxy created before 4.13 removes this content after the upgrade until you set its option to `ALLOW` and deploy it.
* See [Configure LLM Proxy entrypoints](../agent-management/build/configure-llm-proxy-entrypoints.md#edit-the-entrypoint-options).

#### Provider forms and the Models page for LLM Proxies

* The inline provider card of the creation wizard renders the configuration schema of the LLM Proxy endpoint plugin, with the labels, help text, and validation rules the plugin ships.
* The **Models** page of the LLM Proxy detail view, under **Design**, edits the providers after creation. Add an inline or catalog provider, edit a provider in place, remove one, and save every change at once.
* See [Create an LLM Proxy](../agent-management/build/create-an-llm-proxy.md) and [Configure an LLM Proxy](../agent-management/build/configure-an-llm-proxy.md#models).

#### CORS for LLM Proxies

* Each LLM Proxy detail view adds a **CORS** page under **General** that configures cross-origin access for browser-based clients: the allowed origins, methods, and request headers, the exposed response headers, credentials, the preflight cache duration, and whether policies run on preflight requests.
* CORS stays off until you enable it, so an existing LLM Proxy keeps its behavior after an upgrade.
* See [Configure LLM Proxy CORS](../agent-management/build/configure-llm-proxy-cors.md).

#### Failover for LLM Proxies

* The LLM Proxy detail view adds an **Endpoints** group under **Design**, with a **Failover** page. Every provider of the proxy is one endpoint, so failover retries a call on another provider when one is slow or failing.
* A model alias shared by several providers is what lets a request roll over between them. When every attempt fails, the gateway answers `502`.
* See [Configure LLM Proxy failover](../agent-management/build/configure-llm-proxy-failover.md).

#### Cost Rate Limit for LLM Proxies

* The **Cost Rate Limit** policy caps what a consumer spends on an LLM Proxy in dollars over a period, and a request is refused with `429` once the budget is exceeded.
* The budget belongs to the plan and subscription pair by default. Set **Key** to an Expression Language value, and turn on **Use key only**, to give each caller its own budget.
* See [Add the Cost Rate Limit policy](../agent-management/build/add-the-cost-rate-limit-policy.md).

#### AI Token Compression for LLM Proxies

* The **AI Token Compression** policy shrinks the tool output an LLM Proxy request carries, such as test runs, build logs, linter output, and directory listings, before the request reaches the model. It keeps what each run concluded and doesn't change the model's response.
* The policy runs in the request phase and acts only on requests whose conversation carries tool output. It passes every other request through unchanged, so no condition is needed.
* See [Add the AI Token Compression policy](../agent-management/build/add-the-ai-token-compression-policy.md).

#### Owner and sharding tags in the LLM Proxies list

* The **LLM Proxies** list adds an **Owner** column, showing the primary owner of each proxy, and a **Sharding Tags** column, showing the first tag alphabetically with a **more** badge that lists the remaining tags on hover.
* See [Browse the LLM Proxies list](../agent-management/build/browse-the-llm-proxies-list.md).

#### Pictures in the LLM Proxies list

* Each row of the **LLM Proxies** list now starts with the proxy's picture.
* Add, change, or remove the picture under **API Picture** on the proxy's **Configuration** page.
* See [Browse the LLM Proxies list](../agent-management/build/browse-the-llm-proxies-list.md) and [Configure an LLM Proxy](../agent-management/build/configure-an-llm-proxy.md#picture).

#### Negotiated pricing for AI models

* Record the price you negotiated with the provider on a cataloged model, in the **Input price ({currency} per 1M tokens)** and **Output price ({currency} per 1M tokens)** fields of the model edit form. The negotiated price replaces the suggested price wherever the price is shown and wherever cost is computed.
* Refreshing the catalog updates the provider-derived fields and keeps your negotiated price. Republish any LLM Proxy that consumes a repriced model so cost tracking picks up the negotiated rate.
* See [Add an AI model](../agent-management/import/add-an-ai-model.md).

#### Export, import, and duplicate for LLM Proxies

* The **Configuration** page of each LLM Proxy adds three actions. **Export** downloads the proxy as a Gravitee API definition or a Kubernetes CRD, and links to the Terraform tutorial. **Import** replaces the proxy from a Gravitee definition. **Duplicate** copies the proxy under a new context path and version.
* The **Create LLM proxy** button now opens a page offering **Create from scratch** and **Import**. Both import routes accept a local file or a remote URL, and only the Gravitee definition format.
* See [Export and import an LLM Proxy](../agent-management/build/export-and-import-an-llm-proxy.md) and [Duplicate an LLM Proxy](../agent-management/build/duplicate-an-llm-proxy.md).

#### Export, import, and duplicate for A2A Proxies

* The **Configuration** page of each A2A Proxy adds three actions. **Export** downloads the proxy as a Gravitee API definition or a Kubernetes CRD, and links to the Terraform tutorial. **Import** replaces the proxy from a Gravitee definition. **Duplicate** copies the proxy under a new context path and version.
* The **Create A2A proxy** button now opens a page offering **Create from scratch** and **Import**. Both import routes accept a local file or a remote URL, and only the Gravitee definition format.
* A create by import leaves the proxy stopped, for you to start from its **Configuration** page.
* See [Export and import an A2A Proxy](../agent-management/build/export-and-import-an-a2a-proxy.md) and [Duplicate an A2A Proxy](../agent-management/build/duplicate-an-a2a-proxy.md).

#### Promote LLM, MCP, and A2A Proxies

* **Promote** on the **Settings** page of an LLM, MCP, or A2A Proxy sends a copy of it to another environment through Gravitee Cloud. It's available once the installation is registered with Gravitee Cloud and accepted there.
* Someone in the target environment accepts or rejects the request from **Tasks & Approvals**. Accepting creates the proxy there as the same type of proxy, stopped.
* A promotion can't update a proxy that an earlier promotion created. Accepting such a request fails.
* See [Promote your proxies to another environment](../agent-management/build/promote-your-proxies-to-another-environment.md).

#### Response templates for A2A Proxies

* The **Design** group of each A2A Proxy adds a **Response Templates** page that replaces the AI Gateway's default error payload for one error and one kind of client. A template matches on a template key and an Accept header, and returns a status code, headers, and a body.
* Among the proxy types in Agent Management, response templates are offered on A2A Proxies only.
* See [Configure A2A Proxy response templates](../agent-management/build/configure-your-a2a-proxy/configure-a2a-proxy-response-templates.md).

#### Custom observability dashboards

* The **Dashboards** page of Agent Management builds dashboards alongside the templates Gravitee ships. **New dashboard** opens an empty draft, and **Duplicate as custom dashboard** turns a read-only template into an editable copy.
* The editor arranges widgets on a 12-column grid by dragging and resizing them, and edits the dashboard title and description in place.
* See [Build a custom dashboard](../agent-management/observe/dashboards/build-a-custom-dashboard.md).

#### Workflow tools

* The **Tools** page of the Catalog adds workflow tools. A workflow tool chains operations from your APIs in API Management into one MCP tool that the gateway runs as an Arazzo workflow.
* Build the workflow on a canvas from the operations of your APIs, or import an Arazzo 1.0 or 1.1 document. Then publish the tool to the Catalog and add it to an MCP Studio.
* Each step calls its API's backend directly, with the credentials the workflow tool sets for that backend.
* See [Create workflow tools](../agent-management/import/create-workflow-tools.md).

#### Shadow AI agents discovered from Edge Management

* The Catalog imports the AI provider domains Edge Management detects, so unsanctioned AI usage sits in the **Agents** list beside the agents you govern. Each entry is one intercepted domain, under a source named **Shadow AI** that the first synchronization pass creates in each environment, even when nothing has been detected.
* The **Agents** list reads the source under each agent's name, and the **Source** filter narrows the list to **Shadow AI**.
* See [Discover shadow AI agents from Edge Management](../agent-management/import/discover-shadow-ai-agents-from-edge-management.md).

#### Agent Management on a JDBC management repository

* Agent Management now runs on MongoDB or on a JDBC management repository. It keeps its data in the APIM management database and follows whichever of the two the platform runs on, so a JDBC installation doesn't need MongoDB for Agent Management.
* On JDBC, Agent Management creates and updates its own tables when the Management API starts. An installation that turns automatic migrations off applies them itself. See [Apply schema migrations manually](https://documentation.gravitee.io/apim/prepare-a-production-environment/repositories/apply-schema-migrations-manually).
* Agent Management doesn't copy its data between the two databases. An installation that moves from MongoDB to JDBC leaves its existing Agent Management data in MongoDB.

### API Management

API Management gains a file-based path for building and updating API proxies. Each API proxy also gains a Metadata page, a Response Templates page, and an API Score page, and the API detail workspace gains a redesigned out-of-sync banner. Its Policy Studio controls are also clearer, and an API proxy can be promoted to another environment through Gravitee Cloud. An API proxy can also be sent for review, and then waits for a reviewer before it starts.

#### Import an API proxy

* Create an API proxy from a Gravitee v4 API definition, an OpenAPI specification, or a WSDL document. The three formats are available from the **Import API** card on the **Create API Proxy** page.
* Replace the configuration of an existing API proxy from the same three formats, using **Import** on the **Settings** page of the API proxy.
* See [Import an API proxy](../api-management/build/import-an-api-proxy.md).

#### Metadata for API proxies

* The **General** group of the API proxy sidebar adds a **Metadata** page that manages the key and value entries the API carries.
* Editing an inherited entry creates an override on this API alone, **Reset** returns it to the environment default, and **Delete** removes an entry the API owns.
* See [Configure API metadata](../api-management/build/configure-your-api-proxy/configure-api-metadata.md).

#### Out-of-sync banner in the API detail workspace

* The **This API is out of sync** banner replaces the **This API has undeployed changes.** banner in the API detail workspace.
* The new banner carries an explanation: **Your latest changes are not live yet. Deploy to push them to the gateway.**
* See [API proxies](../api-management/manage/api-proxies/README.md).

#### Clearer controls in the Policy Studio

* An empty phase offers one **Add policy** control that opens the same searchable policy list as the plus button on a populated phase.
* In the **Add Policy** catalog, pointing to a row reveals an **Add** button that adds the policy directly, and the catalog header shows the phase you're adding to.
* The changes apply to the Policy Studio of API Management and Agent Management, and to the platform policies of Platform Management.

#### Response templates for API proxies

* The **Design** group of the API proxy sidebar adds a **Response Templates** page that overrides the error payloads the gateway returns by default. A template matches on a template key and an Accept header, and answers with the status code, headers, and body you set, so one proxy can answer a browser and a service differently for the same error.
* The page isn't offered on a TCP Proxy API, which forwards raw traffic and has no HTTP response to override, nor on an MCP or LLM Proxy API.
* See [Configure response templates](../api-management/build/configure-your-api-proxy/configure-response-templates.md).

#### API Score for API proxies

* The **General** group of the API proxy sidebar adds an **API Score** page when API Score is turned on for the environment, with **Enable API Score** on the **API Review** page of the **Environment** section in Platform Management.
* **Evaluate** checks the API definition and every OpenAPI or AsyncAPI documentation page of the API against the rulesets of the environment.
* An evaluation requires an installation connected to Gravitee Cloud.
* See [Review the API Score](../api-management/build/configure-your-api-proxy/review-the-api-score.md).

#### Promote an API proxy

* **Promote** on the **Settings** page of an API proxy sends a copy of it to another environment through Gravitee Cloud. It's available once the installation is registered with Gravitee Cloud and accepted there.
* Someone in the target environment accepts or rejects the request from **Tasks & Approvals**. Accepting creates the API there, or updates the API an earlier promotion created.
* See [Manage general settings](../api-management/build/configure-your-api-proxy/manage-general-settings.md#promote-the-api).

#### Review an API proxy

* While **Enable API Review** is on for the environment, an API proxy can't be started or published until a reviewer accepts it. A banner at the top of the API proxy's pages tracks the review.
* Authors ask for a review from the **API Events** card of the **Settings** page, or with the **Ask for a review** toggle in the last step of the creation wizard.
* See [Review an API proxy](../api-management/build/configure-your-api-proxy/review-an-api-proxy.md).

### Developer Portals

The Gamma console links to the settings of the New Developer Portal, which open in a separate tab.

#### Open the Developer Portal settings from the Gamma console

* The **Applications** section of the home page adds a **Developer Portals** card, and the menu at the top of every page lists **Developer Portals** with the other products.
* Both open the Developer Portal settings of the environment selected in the Gamma console, on the **Navigation** page, in a new browser tab.
* See [Open the Developer Portal settings](open-the-developer-portal-settings.md).

### Edge Management

Edge Management replaces the single configuration page and its flat lists of DNS domains and routes. A guided setup creates the configuration, and a page per concern edits it. Interception is configured per intercepted agent, and each route names the target API that receives its traffic. The console checks that API against the requirements of the route before you deploy. The analytics pages gain their content, and a Devices page shows the fleet.

#### Guided setup and one page per concern

* A new environment starts on a **Quick Start** page that opens a four-step guided setup: **Gateway**, **Intercepted agents**, **Shadow AI**, and **Deploy**. Nothing is deployed until the last step, which publishes an Edge API for the environment with a keyless plan.
* Once the environment is configured, the sidebar groups the pages into **General** with **Overview**, **Configuration** with **Gateway**, **Interception**, **Shadow AI**, and **Daemon deployment**, and **Analytics** with **Detected Shadow AI**, **Proxied Traffic**, and **Devices**.
* See [Set up Edge Management](../edge-management/connect/set-up-edge-management.md).

#### Interception per agent

* The **Interception** page configures interception per intercepted agent. An agent owns the domains it calls and the routes under those domains, and each route names the target API that receives it. **Claude Code** is a preset with a fixed domain, decoder format, vendor, and route. **Custom agent** lets you declare everything yourself.
* A configuration that still carries the legacy DNS domains and routes shows them read-only under **Legacy interception** and can't be saved until they're cleared with **Clear all**. Intercepted agents require Edge Daemon 2.0.0 or later.
* See [Configure interception](../edge-management/connect/configure-edge-management.md) and [Target API reference](../edge-management/connect/proxy-api-reference.md).

#### Analytics and devices

* **Detected Shadow AI** lists the direct connections of the devices to the watched provider domains, with the device, the provider, the process, and the number of detections.
* **Proxied Traffic** lists the intercepted requests that reached the gateway, with the device, the tool, the provider, the model, and the token counts.
* **Devices** lists the devices that run the daemon, with their status, their daemon version, and their heartbeats.
* See [Monitor detected shadow AI](../edge-management/observe/monitor-shadow-ai-traffic.md), [Monitor proxied traffic](../edge-management/observe/monitor-proxied-traffic.md), and [Monitor your devices](../edge-management/observe/monitor-devices.md).

### Event Stream Management

Event Stream Management regroups its sidebar by object and opens on a new Overview page. It adds Message APIs, the Kafka Explorer, and an Observability section, and brings Kafka Services to the same management depth as Message APIs: a Security step in the creation wizard, subscriptions, metadata, broadcasts, alerts, API Score, the review workflow, import, export, and duplication. Message APIs connect clients to message backends such as Kafka, MQTT 5.x, Solace, and RabbitMQ. The Kafka Explorer reads the live brokers, topics, consumer groups, and messages of a Kafka target through saved connections.

#### Sidebar groups and the Overview page

* The Event Stream Management sidebar groups its pages by object: **General** holds **Overview**, **APIs** holds **Kafka Services** and **Message APIs**, **Kafka Infrastructure** holds **Clusters**, **Virtual Clusters**, and **Explorer**, and **Observability** holds **Dashboards**, **Logs**, and **Tracing**. The **Manage** and **Build** groups are gone.
* The module opens on the **Overview** page. One card per area shows the total and the state breakdown of the Kafka Services, Message APIs, Clusters, Virtual Clusters, and Kafka Explorer connections of the environment, with **Create**, **Import** for the two API types, and **Manage** buttons that follow your role.
* A banner on the Overview page counts the clusters and Virtual Clusters with pending changes, and the **Observability** section links to the screens that your role can open.
* See [Use the Overview page](../event-stream-management/general/use-the-overview-page.md).

#### Kafka Service creation wizard

* The **Create Kafka Service** wizard has five steps: **Identity**, **Listener**, **Endpoint**, **Security**, and **Review**. Each forward button names the next step, for example **Next: Security**.
* The new **Security** step lines up the plans of the Kafka Service before it exists. It adds a Keyless plan by default, which is published at creation, so the Kafka Service can be consumed right away. Plans of the other security types are created in Staging, to finish and publish on the **Plans** page.
* The **Review** step offers **Deploy now** to start the Kafka Service right after creation, or **Ask for review** when the environment uses the API review workflow.
* The **Listener** step checks that the host prefix is free in the environment while you type.
* See [Create your first Kafka Service](../event-stream-management/get-started/create-your-first-kafka-service.md).

#### Kafka Service management

* Each Kafka Service opens on a sidebar with the groups **General**, **Design**, **Consumers**, **Monitoring**, **Observability**, and **Operations**. The **General** page is now **Settings**, the **Configuration** page splits into **Entrypoint** and **Endpoints**, and deployment splits into **Sharding Tags** and **Deployment History**.
* The **Overview** page tracks the setup in a five-item checklist, and shows the bootstrap server that the gateway resolved once the Kafka Service is deployed.
* New pages: **Metadata**, **Broadcasts**, a **Subscriptions** page that manages subscriptions and their API keys, **Alerts**, and **API Score** when the environment uses it.
* **Alerts** offers Kafka rules in five categories: **Connection**, **Topic traffic**, **Operations**, **Policy rejections**, and **Authentication**. A banner warns that most of them can't fire while **Aggregated metrics** are off on the Kafka Service.
* Publishing a secured plan while a Keyless plan is live opens a dialog that closes the conflicting plans and publishes the new one in one step.
* Saving in the **Policy Studio** no longer deploys the Kafka Service. Deploy the changes from the header of the Kafka Service.
* The **Settings** page imports a Gravitee API definition over the Kafka Service, as a local file or a remote URL, and exports the definition. **Import** on the **Kafka Services** list creates a Kafka Service the same way.
* Kafka Services follow the API review workflow, with a review badge and a banner to ask for or review changes.
* A Kafka Service published outside Event Stream Management shows **Unpublish** on its **Settings** page, so that you can then delete it.
* See [Kafka Services](../event-stream-management/apis/kafka-services/README.md).

#### Subscription metadata

* The detail page of a subscription, on a Kafka Service or a Message API, gains a **Metadata** card to add, edit, and delete the key and value entries of the subscription.

#### Clusters and Virtual Clusters

* The **Clusters** and **Virtual Clusters** lists gain a **Lifecycle** filter with **Deployed**, **Pending changes**, and **Undeployed**, and count each state above the list.
* Editing a deployed cluster or Virtual Cluster sets it to **Pending changes**. **Deploy changes**, in the row menu or at the top of its page, pushes the edits to the gateway.
* The sidebar of a cluster or Virtual Cluster holds **Overview**, **Settings**, **Configuration**, **User Permissions**, and **Used by Kafka Services**.
* The **Kafka Service** wizard and the **Virtual Cluster** wizard list only deployed clusters and Virtual Clusters.
* **Delete** is offered only once a cluster or Virtual Cluster is undeployed. The **Settings** and **Configuration** pages are editable only when your role on the cluster allows it.
* See [Register your Kafka clusters](../event-stream-management/kafka-infrastructure/clusters/register-your-kafka-clusters.md) and [Virtual Clusters](../event-stream-management/kafka-infrastructure/virtual-clusters/README.md).

#### Duplicate Kafka Services and Message APIs

* Create a copy of an existing Kafka Service or Message API with **Duplicate** on its **Settings** page. The copy reuses the source's configuration, including its endpoints.
* Provide a name and a version for the copy, and a new listener host prefix for a Kafka Service or a new context path for a Message API. The host prefix and the context path are unique per environment, the source's value counts as already in use, and the dialog checks availability while you type. A Message API whose only entrypoint is **Webhook** needs neither.
* The copy carries the plans, the documentation pages, and the members of the source.
* A copied Kafka Service is created in a stopped state, so you control when it starts accepting connections.
* See [Duplicate a Kafka Service](../event-stream-management/apis/kafka-services/duplicate-a-kafka-service.md) and [Manage general settings](../event-stream-management/apis/message-apis/manage-general-settings.md) for a Message API.

#### Deployment, rollback, and Kubernetes-managed APIs

* Deploying a Kafka Service or a Message API opens the **Deploy your API** dialog, with an optional **Deployment label** of 32 characters at most. The **Deployment History** page shows the label of each deployment.
* **Deployment History** restores the definition of a past deployment through the **Rollback API** dialog, for Kafka Services and Message APIs. Rolling back needs the definition update permission, and the version that the gateway runs isn't offered while the API is in sync with it.
* An API managed by the Kubernetes operator opens read-only: its design, plans, members, metadata, documentation, and start and stop actions can't be changed from the console. Its subscriptions, notifications, and alerts stay editable, and you can still deploy it and roll it back.
* On the **Settings** page of a Kubernetes-managed API, **Detach the Kafka Service** or **Detach the Message API** opens the **Detach API** dialog, which detaches the API from its automation source and makes it editable again.
* See [Manage deployments](../event-stream-management/apis/kafka-services/manage-deployments.md).

#### Plans, subscriptions, and broadcasts

* The plan form of Kafka Services and Message APIs gains **Characteristics**, a required subscription comment with a **Custom message to display to consumer** of 64 characters at most, and **Sharding tags**. A plan can use only the sharding tags that its API carries.
* The first plan of an API can be of any type, not only Keyless, and the plans list opens on **Published**.
* Subscribing an application to a Push plan asks for the delivery entrypoint, an optional channel, and the entrypoint's subscription configuration. The **Consumer subscription configuration** card of the subscription edits it while the subscription isn't closed.
* **Broadcasts** adds the **HTTP POST** channel, which posts the message to a URL with optional **HTTP headers** and **Use system proxy**.
* See [Manage plans](../event-stream-management/apis/message-apis/manage-plans.md), [Manage subscriptions](../event-stream-management/apis/message-apis/manage-subscriptions.md), and [Broadcast messages to consumers](../event-stream-management/apis/message-apis/broadcast-messages-to-consumers.md).

#### Message APIs

* The **APIs** group of the Event Stream Management sidebar adds **Message APIs**. A Message API is a v4 API that connects clients to a message backend.
* **Create Message API** opens a five-step wizard that picks the entrypoints, the endpoints, and the plans.
* The **Entrypoints** page manages several context paths, with optional virtual hosts. The **Endpoints** page manages endpoint groups with a **Load balancing algorithm**, and endpoints with a **Weight** and **Tenants**. The **Failover** page sets **Force next endpoint on failure**, **Max retries**, and a **Failure condition**.
* The **Webhooks** page lists the delivery attempts with the name of each application. **Settings** opens the **Webhook logs reporting settings** dialog, with **Enable webhook logs** and the request and response bodies and headers. When attempts aren't recorded, the **Delivery attempts are not recorded** banner names the setting to turn on.
* The creation wizard requires an enterprise license that includes the `apim-en-message-reactor` feature.
* See [Message APIs](../event-stream-management/apis/message-apis/README.md).

#### Kafka Explorer

* The **Kafka Infrastructure** group of the Event Stream Management sidebar adds **Explorer**, which opens the Kafka Explorer. The Kafka Explorer reads the live brokers, topics, consumer groups, and messages of a Kafka target through saved connections.
* Reaching the pages at all needs the new environment-scoped `EXPLORER` permission, which only the environment **ADMIN** role grants for create, update, and delete among the built-in roles: give a custom environment role the actions your other connection administrators need.
* Kafka Explorer requires an enterprise license that includes the `apim-native-kafka-explorer` feature.
* See [Kafka Explorer](../event-stream-management/kafka-infrastructure/kafka-explorer/README.md).

#### Observability for Kafka Services and Message APIs

* The Event Stream Management sidebar adds an **Observability** group holding **Dashboards**, **Logs**, and **Tracing**. All three read what the gateway already reported, and all three show only the Kafka Services and Message APIs of the environment.
* A failed Kafka connection shows its **Connection ID**, also available as an optional **Logs** column, to search the gateway logs for the same connection.
* Each Kafka Service and Message API gains **Dashboard**, **Logs**, and **Tracing** under **Observability** in its own sidebar.
* The **Reporter Settings** page of a Kafka Service turns **Aggregated metrics** and **Connection events** on or off, and picks which connection events the gateway records: **Connected**, **Disconnected**, and **Errors**.
* When the environment enables API Score, the **Observability** group also holds **API Score**, with a **Dashboard** tab and a **Rulesets** tab.
* See [Observability](../event-stream-management/observability/README.md) and [Configure reporter settings](../event-stream-management/observability/configure-reporter-settings.md).

### Platform Management

Platform Management adds environment-scoped dictionaries and metadata as reusable assets for APIs and API policies, gateway routing configuration for the organization, and organization-wide user administration. It also adds environment alerts on gateway nodes, API traffic, and endpoint health checks, with their notification channels and an activity board. It adds the organization-wide console settings too, covering console authentication, console behavior, cross-origin access to the Management API, and outbound email. Each environment also turns API Score on or off, and can require a review before an API is started or published.

#### Broadcast messages to environment members

* Send a one-way message to the members of the selected environment from the **Broadcasts** page under **APIs & Assets** in the **Environment** section. Choose the **Portal Notifications**, **Email**, or **POST HTTP Message** channel.
* See [Broadcast messages to environment members](broadcast-messages-to-environment-members.md).

#### Configure API logging

* The **API Logging** page of the **Environment** section caps how long APIs log full payloads, with **Max Duration (in ms)**. Its values belong to the organization and apply to every environment.
* The **Message Sampling** card sets a default and a limit for the probabilistic, count, temporal, and windowed count sampling of message APIs.
* See [Configure API logging](configure-api-logging.md).

#### Configure API Review

* Turn on **Enable API Score** and **Enable API Review** for an environment from the **API Review** page of the **Environment** section, each on its own.
* Add, edit, and delete the manual rules that reviewers check when they accept or reject an API.
* With API Score off, the **API Score** pages of the environment and of each API proxy are hidden. With API Review off, APIs start and publish without a reviewer.
* See [Configure API Review](configure-api-review.md).

#### Configure client registration

* Decide which application types the environment accepts from the **Client Registration** page under **System & Security** in the **Environment** section.
* **Enable Dynamic Client Registration** decides whether the environment offers the **Browser**, **Web**, **Native**, and **Backend-to-Backend** types at all.
* Add one OpenID Connect Dynamic Client Registration provider per environment, so that registering an application of one of those four types creates an OAuth client on the authorization server.
* Adding or opening a provider requires an enterprise license that includes the `apim-dcr-registration` feature.
* See [Configure client registration](configure-client-registration.md).

#### Configure console authentication

* Decide whether the Gamma console sign-in page shows the local username and password form, from the **Authentication** page of the **Organization** section.
* Add Gravitee Access Management, OpenID Connect, Google, and GitHub identity providers, edit them, and delete them. OpenID Connect requires an enterprise license.
* Map groups, organization roles, and environment roles to users from conditions on their profile, access token, or ID token, computed at first sign-in or at every sign-in.
* See [Configure console authentication](configure-console-authentication.md).

#### Configure console management and schedulers

* Name the APIM Console, set the URL Gravitee puts in the links it emails, and control support and self-registration from the **Management & Schedulers** page of the **Organization** section.
* Set how often the console polls for tasks and for notifications, in seconds.
* See [Configure console management and schedulers](configure-console-management-and-schedulers.md).

#### Configure CORS for the Developer Portal API

* The **CORS** page of the **Environment** section controls which browser origins may call the Developer Portal API of the environment, and which methods and headers a cross-origin request may use.
* Changes take effect without restarting the Management API.
* See [Configure CORS for the Developer Portal API](configure-developer-portal-cors.md).

#### Configure CORS for the Management API

* Set the origins, methods, allowed headers, exposed headers, and preflight cache duration for cross-origin calls to the organization's Management API from the **CORS** page.
* The console addresses resolved for the organization stay allowed on top of the list, so tightening the origins doesn't lock you out of the consoles.
* See [Configure CORS for the Management API](configure-console-cors.md).

#### Configure environment alerts

* Create, edit, enable, and delete the alerts of the selected environment from the **Alerts** page under **System & Security** in the **Environment** section.
* Send each alert by email, Slack, system email, or webhook, and limit repeated notifications with a dampening mode.
* The page requires an enterprise license that includes the Alert Engine feature.
* See [Configure environment alerts](configure-environment-alerts.md).

#### Configure environment notifications

* Subscribe to the user, support, federation, and group events of the selected environment from the **Notifications** page of the **Environment** section: in the console for yourself, and by email or webhook for your team.
* See [Configure environment notifications](configure-environment-notifications.md).

#### Configure primary owner mode

* Decide who can be the primary owner of an API or API Product from the **Primary Owner Mode** page under **System & Security** in the **Environment** section.
* With **Hybrid**, the default, a user or a group can be the primary owner. With **User**, only a person can be the primary owner, and the **PRIMARY_OWNER** role can't be selected for that kind of resource when you add or edit group members. In both modes, the person who creates the API or API Product becomes its primary owner.
* With **Group**, one of the creator's groups in which a member holds the **PRIMARY_OWNER** role for that kind of resource becomes the primary owner. A person without such a group can't create the API or API Product.
* See [Configure primary owner mode](configure-primary-owner-mode.md).

#### Configure the SMTP mail server

* Point the organization at its mail server from the **SMTP** page, with the host, port, credentials, protocol, sender address, and subject template.
* Add branded sender rules that replace the sender address and subject template for the recipients at a given domain.
* See [Configure the SMTP mail server](configure-smtp.md).

#### Configure the SMTP mail server for an environment

* The **SMTP** page of the **Environment** section sets the mail server the environment uses, with the same fields as the organization's **SMTP** page. For mail sent in the context of the environment, its values take precedence over the organization's.
* See [Configure the SMTP mail server for an environment](configure-environment-smtp.md).

#### Customize notification templates

* Reword the email and portal notifications the organization sends from the **Templates** page of the **Organization** section, where they're grouped by category and a **Custom** badge marks each overridden template.
* Turn on **Override default template** on a channel card, edit the title and the FreeMarker content, and save. Turn the override off to send the built-in default again without losing your wording.
* See [Customize notification templates](customize-notification-templates.md).

#### Let people request a console account

* While **Allow User Registration** is on, the Gamma console sign-in page offers a **Request an account** link, as long as the local login form is shown.
* The **Request an account** page asks for a first name, a last name, an email address, and the fields listed on the **User Fields** page.
* See [Configure console management and schedulers](configure-console-management-and-schedulers.md).

#### Manage API Score

* Review the latest score of every API in the selected environment from the **API Score** page under **APIs & Assets** in the **Environment** section.
* Import custom rulesets for OpenAPI, AsyncAPI, or one type of Gravitee API from YAML or JSON files, and import JavaScript functions that extend them, on the **Rulesets & Functions** tab.
* The page appears once **Enable API Score** is turned on for the environment on the **API Review** page, for people whose role can read the environment's integrations.
* See [Manage API Score](manage-api-score.md).

#### Manage dictionaries

* Create, edit, search, and delete the dictionaries of the selected environment from the **Dictionaries** page. Dictionaries hold key-value properties that API policies reference at runtime.
* Manual dictionaries hold properties that you maintain by hand and publish to the gateways with the **Deploy** action.
* Dynamic dictionaries poll an HTTP provider at a configured interval, transform the response with a JOLT specification, and publish the refreshed properties automatically while started.
* See [Manage dictionaries](manage-dictionaries.md).

#### Manage entrypoints and sharding tags

* Configure sharding tags, entrypoint mappings, and each environment's default entrypoint values from the **Entrypoints & Sharding Tags** page.
* Sharding tags route APIs to specific gateway groups.
* Entrypoint mappings define the entrypoint that the Developer Portal displays for APIs that carry a given tag, as an HTTP URL, a TCP port, or a Kafka bootstrap domain pattern, and apply to all environments or to a selection.
* See [Manage entrypoints and sharding tags](manage-entrypoints-and-sharding-tags.md).

#### Manage environment metadata

* Add, edit, search, and delete the key-value metadata entries of the selected environment from the **Metadata** page. Every API in the environment inherits each entry as a default value.
* Rename an entry or change its value without changing its key, so the APIs and Developer Portal pages that reference the key keep working.
* See [Manage environment metadata](manage-environment-metadata.md).

#### Manage groups

* Create, edit, search, and delete the groups of the selected environment from the **Groups** page of the **Team** section, and set the default API, API Product, and application roles their members hold, with a lock on each that keeps a group administrator from changing it.
* Attach a group to every existing API, API Product, or application of the environment in one action, or have the new ones join it automatically.
* See [Manage groups](manage-groups.md).

#### Manage platform policies

* Create, edit, reorder, disable, and delete the platform flows of the organization from the **Policy Studio** page of the **Organization** section. A platform flow applies request and response policies to every API in the organization, before and after each API's own flows, and native Kafka APIs and TCP proxy APIs are left untouched.
* Saving asks for confirmation, then deploys the flows to the gateways of the organization. The APIM Console edits the same flows.
* See [Manage platform policies](manage-platform-policies.md).

#### Manage roles

* List the roles of every scope from the **Roles** page of the **Team** section, with a **System** badge on the roles Gravitee defines and a **Default** badge on the one that new members of a scope receive.
* Create a custom role in any scope and set the **Create**, **Read**, **Update**, and **Delete** permissions it grants, one row per permission of that scope. Creating a role requires an enterprise license that includes the custom roles feature, and the **Explorer** and **AI Workspace** scopes carry no permissions to set.
* A role's name is fixed once it's created, system roles open read-only, and the `TAG`, `TENANT`, and `ENTRYPOINT` permissions of an **Environment** role now belong to the **Organization** scope.
* See [Manage roles](manage-roles.md).

#### Manage shared policy groups

* Create, edit, search, and delete the shared policy groups of the selected environment from the **Shared Policy Groups** page. A shared policy group bundles policy steps once for reuse across API flows, and is fixed to one API type and one flow phase at creation.
* Deploy the saved steps to the gateways of the environment. Each deployment raises the version by one and records an entry in the group's version history, and a group changed after deployment shows as **Pending** until you deploy again.
* See [Manage shared policy groups](manage-shared-policy-groups.md).

#### Manage tenants

* Create, edit, search, and delete the tenants of the organization from the **Tenants** page. A tenant pairs a gateway with the API endpoints that gateway loads, so one API can serve several regions without a second copy of it.
* A gateway loads an endpoint when the endpoint has no tenant or lists the gateway's own tenant.
* See [Manage tenants](manage-tenants.md).

#### Manage user fields

* Choose the extra questions people answer when they sign up, from the **User Fields** page of the **Environment** section. The Gamma console, APIM Console, and Developer Portal sign-up forms all ask them, and every environment of the organization shares the same list.
* Give each field a key, a label, and optionally a list of values that turns it into a choice. Turn on **Required** to make people answer a field to sign up.
* Deleting a field also deletes every person's answer to it.
* See [Manage user fields](manage-user-fields.md).

#### Manage users

* Add, review, and delete the users and service accounts of the organization from the **Users** page, and search the list by name, email, or ID.
* Grant organization roles and per-environment roles from the user's detail page, and manage the group memberships that carry the user's API, API Product, application, and integration roles in each environment.
* See [Manage users](manage-users.md).

#### Manage your account

* Open your own account from the account menu in the top-right corner of the console.
* Edit your first name, last name, and email address when Gravitee holds your account, fill in the custom user fields of the organization, and upload an avatar or return to the default one.
* Generate personal access tokens for the Management API, copy each one once together with a `curl` example, and revoke the tokens you no longer need.
* See [Manage your account](manage-your-account.md).

#### Monitor API health across an environment

* Review the health-check availability of the v4 HTTP proxy APIs of the selected environment from the **API Health Check** page under **System & Security** in the **Environment** section, over the last minute, hour, day, week, or month.
* The **API Health Check Report** banner counts the APIs in error, at 80% availability or less, and in warning, at 95% or less, across every API with health check enabled.
* See [Monitor API health across an environment](monitor-api-health-across-an-environment.md).

#### Monitor gateway instances

* Review the gateway instances registered with the selected environment from the **Gateways** page, with each instance's version, status, last heartbeat, address, tenant, and sharding tags.
* Open an instance to read what it reported about itself on the **Environment** tab: its information rows, the plugins it loaded, and its JVM system properties.
* Follow the instance's live resource use on the **Monitoring** tab, which refreshes every 5 seconds and reports CPU, heap, memory pools, uptime, file descriptors, threads, and garbage collection.
* See [Monitor gateway instances](monitor-gateway-instances.md).

#### Review organization and environment audit logs

* Trace who changed what, and when, from two **Audit** pages: one in the **Organization** section covering the whole organization, and one in the **Environment** section covering the selected environment.
* Export the filtered trail as CSV or JSON for a compliance archive, up to 10,000 events per export.
* See [Review organization and environment audit logs](review-audit-logs.md).

#### Save observability dashboards

* Save a custom observability dashboard in its environment over the Gamma API, so it survives a restart and reaches everyone with read access to that environment's dashboards. Each dashboard carries its title, its filters, its time range, and its widgets.
* Create, list, read, update, and delete dashboards under `/gamma/organizations/{orgId}/environments/{envId}/observability/dashboards`.
* Concurrent edits are caught with `ETag` and `If-Match`.
* See [Save observability dashboards with the Gamma API](save-observability-dashboards.md).

## Release Date: June 26, 2026

## Highlights

* **Agent Management**: Unified AI Gateway governing LLM, MCP, and A2A protocols with cost attribution, PII filtering, and end-to-end OpenTelemetry tracing across every agent hop.
* **API Management**: Create and govern REST, GraphQL, and gRPC API proxies with security plans, policy enforcement, and observability. Bridge existing APIs as AI tools in Agent Management.
* **Authorization Management**: Fine-grained, catalog-aware access control via GAPL policies enforced at microsecond latency inline in every gateway, across all Gamma traffic types.
* **Edge Management**: Lightweight device daemon that detects shadow AI usage and enforces pre-egress policies before AI traffic leaves employee devices.
* **Event Stream Management**: Register and govern Kafka clusters with virtual clusters for multi-tenant isolation, and bridge event streams as Kafka API tools in Agent Management.
* **Platform Management**: Shared platform foundations covering application management, reusable resources, Access Management integration, and OpenAPI viewer configuration.

## New features

### Agent Management

#### AI Gateway

* Provides a unified runtime for LLM, MCP, and A2A traffic. All three proxy types share a common authentication chain, policy chain, observability chain, and Authorization Management integration point.
* **LLM Proxy**: Routes model traffic to Anthropic, OpenAI, Bedrock, Gemini Enterprise Agent Platform (formerly Vertex AI), and Azure with guardrails, PII filtering, token-based rate limiting, and structured output enforcement.
* **MCP Proxy**: Governs tool invocations on upstream MCP servers (HubSpot, GitHub, Salesforce, Jira) with authentication, fine-grained policies, and protocol-native JSON-RPC 2.0. Supports both transparent proxy mode and Studio mode.
* **MCP Studio**: Compose tools, resources, prompts, and skills from multiple sources into a Composite MCP Server without writing code.
* **A2A Proxy**: Secures agent-to-agent delegations with skill discovery via `/.well-known/agent.json`, per-skill authorization, and agent identity verification across trust boundaries.

#### Catalog

* Authoritative registry of AI models, MCP servers, tools, prompts, agents, skills, and resources that policies are authored against.
* Syncs AI models from AWS Bedrock, Azure AI Foundry, and Gemini Enterprise Agent Platform (formerly Vertex AI), or accepts manual registration.
* Consumes from external MCP registries (GitHub, Smithery, and third-party) and operates as an MCP Registry itself, so other systems can discover and read from it.
* REST, GraphQL, and gRPC APIs from API Management become **API Tools**, and Kafka topics from Event Stream Management become **Kafka API Tools**, making existing enterprise infrastructure agent-accessible without redevelopment.

#### Agent Identity

* Registers agents as OAuth clients in Gravitee Access Management so gateways and authorization policies can authenticate, attribute, and audit every agent.
* Three personas: **Desktop Productivity Agent** (public PKCE client), **Hosted Agent** (confidential web client), and **Workload Agent** (service client with `client_credentials` or token exchange).
* Supports CIMD (Client ID Metadata Documents) and SPIFFE as credential options within the registration wizard.

#### Observability

* End-to-end OpenTelemetry tracing across every agent hop: agent to tool, agent to LLM, and agent to agent.
* Every span carries agent identity, tool name, inputs, outputs, latency, policy decision, cost, and timestamp.
* A lineage view stitches spans into a navigable trace of the full request graph.

### API Management

#### API Proxy Creation

* Define an API proxy with a context path, upstream target URL, and security plan via a step-by-step wizard or template-based flow.
* Templates preconfigure common patterns, reducing setup time for standard API topologies.

#### Security Plans

* Attach one or more plans to control who can call an API and how they authenticate.
* Supported plan types: Keyless, API Key, JWT, OAuth2, and mTLS.

#### Policy Enforcement

* Apply fine-grained policies at the request and response level: rate limiting, content transformation, and authorization checks powered by Authorization Management.
* Shared policy groups allow reusable policy sets to be applied across multiple API proxies.

#### Consumer Access

* Manage consumer applications, subscriptions, and API keys through controlled channels.
* API Products bundle proxies into a consumer-facing offering with its own subscription lifecycle.

#### Observability

* Monitor request volume, latency, error rates, and audit history for every deployed API via per-API dashboards and log search.
* Endpoint health monitoring surfaces backend availability without leaving the console.

#### API detail workspace

* Manage every aspect of an API proxy after creation from a single workspace: general settings, properties, resources, notifications, CORS, entrypoints, endpoints, failover, health checks, logging and tracing, plans, consumers, broadcasts, user permissions, audit logs, and deployment.
* Compare any two deployed versions of an API definition and roll back to an earlier one.
* See [API proxies](../api-management/manage/api-proxies/README.md).

### Authorization Management

#### GAPL Policy Language

* Policies are written in GAPL (Gravitee Authorization Policy Language), a Cedar-syntax subset optimized for the Gamma visual editor.
* Each policy declares an effect (`permit` or `forbid`), a principal, an action, a resource, and optional `when` conditions.
* Condition support includes time-of-day restrictions, IP range checks, token budgets, cost ceilings, scope checks, PII filter flags, and tenant attribute matching.

#### Policy Categories

* **MCP Policies**: Access to MCP servers, tools, prompts, and resources.
* **AI Model Policies**: Access to AI providers and specific models, with cost and token usage constraints.
* **API Policies**: Access to API proxies, endpoints, and data fields.
* **Custom Policies**: Policies for resources not routed as MCP, API, Agent, LLM, or Event (internal applications, data assets, and bespoke resources).

#### Inline Enforcement

* The Policy Decision Point (PDP) runs inside the AI Gateway, API Gateway, and Event Gateway at microsecond latency with no network hop.
* Principals can be synced from identity providers via SCIM or from Gravitee Access Management, with live sync progress surfaced via toast notifications.

#### Pre-built Condition Snippets

* Each policy category ships with reusable condition snippets for common scenarios: business hours, trusted device, corporate IP range, token budget, cost ceiling, rate limit, and tenant match.

### Edge Management

#### Shadow AI Detection

* Continuously scans device network connections to detect any process communicating with a known AI provider, regardless of whether traffic is routed through the Edge Daemon.
* Surfaces unmanaged AI usage across the device fleet with no per-tool configuration required.

#### Active Traffic Routing

* **Interception mode (default)**: Transparent local DNS resolver redirects configured AI provider domains to the daemon, which terminates TLS locally and forwards to the AI Gateway. No per-tool configuration needed. Automatically handles Node.js tools (Claude Code, Cursor) via `NODE_EXTRA_CA_CERTS`.
* **Proxy mode**: Tools can be pointed at the Edge Daemon explicitly via provider base URL environment variables for direct routing.

#### Local Pre-Egress Policy Enforcement

* Blocks sensitive data before it leaves the device: secrets, classified content, large prompt payloads, and disallowed models.
* Policies are evaluated locally so enforcement is not dependent on network connectivity to the gateway.

#### MDM Deployment

* Distributed via Kandji (Jamf and Intune planned) with automatic OS and Node.js trust store setup, with no manual certificate steps required.

### Event Stream Management

#### Kafka Cluster Registration

* Import existing Kafka clusters into Gamma so they can be governed, monitored, and composed into higher-level services.
* Registered clusters are available as the backing infrastructure for Kafka Services and Virtual Clusters.

#### Kafka Service Creation

* Define a governed Kafka Service with security plans, policies, and access controls backed by either a Registered Cluster or a Virtual Cluster.
* Analogous to an API proxy in API Management. The same plan types and policy model apply to event streams.

#### Virtual Clusters

* Provision logically isolated Kafka environments on shared infrastructure for multi-tenant workloads (Kafka Mesh).
* Prevents cross-tenant data access while allowing shared underlying broker infrastructure.

#### AI Bridging

* Kafka APIs and event streams can be exposed as **Kafka API Tools** in Agent Management, making existing event infrastructure accessible to AI agents without redevelopment.

### Platform Management

#### Application Management

* Manage consumer applications and their subscriptions to APIs, event streams, and agent services from a single location.

#### Shared Resources

* Define reusable components (OAuth2 token validation endpoints, cache stores, and authentication providers) that API proxies reference at runtime.

#### Access Management Integration

* Configure the connection to Gravitee Access Management, select an environment and domain, and verify OAuth capabilities required by agent identities and security plans.

#### OpenAPI Viewer Configuration

* Configure the OpenAPI viewer globally across both the management console and Portal Next for a consistent API documentation experience.
