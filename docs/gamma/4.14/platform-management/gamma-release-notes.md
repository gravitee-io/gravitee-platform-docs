---
description: What the Gamma 4.14 release adds to Agent Management, API Management, Authorization Management, Edge Management, Event Stream Management, and Platform Management. Browse the new features and changes.
---

# Release Notes

For release and end-of-life dates, see [Support Model](https://documentation.gravitee.io/apim/release-information/support-model).

## Release Date: TBD

## Highlights

* **Agent Management**: Add the **AWS Lambda** and **Data Cache Policy** policies to LLM Proxies, set up alerts for MCP Proxies, import MCP servers that the control plane can't reach, and encrypt the dynamic properties of LLM, MCP, and A2A Proxies. A2A Proxies gain a **CORS** page, and MCP Proxies an **API Score** page. Human In the Lead holds MCP tool calls until a person approves or rejects them.
* **API Management**: Encrypt the dynamic properties of API proxies, group their analytics with path mappings, design flows on API Products in a Policy Studio, configure the resources of API Products, and secure API Products with OAuth2 plans.
* **Authorization Management**: Manage PDP gateways, schema documents, entities, and policies as code, through the Automation API, as Kubernetes resources, and with Terraform.
* **Edge Management**: Choose how Edge Daemons authenticate to the Edge Reactor, apply OAuth2 plans to intercepted routes, edit gateway addresses after the guided setup, and install the Edge Daemon on Windows devices.
* **Event Stream Management**: Use registered Clusters in Message APIs, bound the metadata requests that the gateway sends to its brokers, disable broker hostname verification over SSL, and encrypt the dynamic properties of Kafka Services and Message APIs.
* **Platform Management**: Encrypt the sensitive values of environment dictionaries, renew the shared API key of an application with a value you choose, and label, describe, and hide the additional and custom metrics of an environment.

## Breaking changes and deprecations

#### **Alpine Linux images of the Gateway and the Management API are deprecated**

From 4.14.0, the `graviteeio/apim-gateway` and `graviteeio/apim-management-api` images are also published with `-alpine` tags, which point to the same images as the tags without a suffix. The March 2027 release of APIM moves the tags without a suffix, including `latest`, to the Debian image. The June 2027 release stops publishing Alpine Linux images of these two components. To stay on Alpine Linux until then, switch to the `-alpine` tags. To move to Debian, use the `-debian` tags, and check how the Debian image differs before you switch. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md#alpine-linux-images-of-the-gateway-and-the-management-api-are-deprecated).

#### **The Gateway and the Management API verify the Elasticsearch certificate**

From 4.14.0, the Gateway reporter and the Management API verify the certificate of an Elasticsearch cluster that they reach over `https`. A cluster whose certificate is self-signed or signed by an internal authority needs a truststore in `ssl.truststore`, or `ssl.trustAll: true` to keep the previous behavior. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md#the-gateway-and-the-management-api-verify-the-elasticsearch-certificate).

#### **Event Stream Management guards the Clusters that APIs use**

From 4.14.0, only the members of a Cluster bind a Kafka Service or a Message API to it. A Cluster that started APIs use can't be undeployed, deleted, or lose a connection that they use. Starting a Kafka Service and deploying a Virtual Cluster are refused while a Cluster that they use isn't deployed, or doesn't have their connection. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md).

#### **COUNT on the LLM token and cost metrics counts requests**

From 4.14.0, **COUNT** on the six token and cost metrics of LLM traffic gives the number of requests that carry the value, and **SUM** gives the total. In 4.13, **COUNT** gave the total. A custom dashboard widget that reads **COUNT** on one of these metrics shows a number of requests after the upgrade, so select **SUM** under **Measure** to keep the total. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md#count-on-the-llm-token-and-cost-metrics-counts-requests).

#### **AVG, MIN, MAX, and the percentiles leave out the requests without a value**

From 4.14.0, **AVG**, **MIN**, **MAX**, and the percentiles of a built-in metric leave out the requests that don't carry its value. In 4.13, they counted those requests as `0`. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md#avg-min-max-and-the-percentiles-leave-out-the-requests-without-a-value).

#### **HTTP Errors and Edge Heartbeat Count now count only their own events**

From 4.14.0, **COUNT** on **HTTP Errors** counts the requests whose status is from 400 to 599, and **COUNT** on **Edge Heartbeat Count** counts heartbeat events only. In 4.13, they counted every request and every Edge Management event. For more information, see [Breaking Changes and Deprecations](gamma-breaking-changes.md#http-errors-and-edge-heartbeat-count-now-count-only-their-own-events).

## New features

The 4.14 release adds the following capabilities.

### Agent Management

Agent Management adds the following in 4.14:

* **LLM Proxies**: the **AWS Lambda** and **Data Cache Policy** policies.
* **MCP Proxies**: alerts, an **API Score** page, and HTTP/2 fields, which Catalog MCP servers also gain.
* **A2A Proxies**: a **CORS** page for calls from web pages on other origins.
* **All proxy types**: the pages of LLM Proxies, MCP Proxies, and A2A Proxies name the type of proxy instead of the API, and their **Properties** pages encrypt dynamic properties.
* **MCP Proxies and MCP Studios**: JWT plans gain two settings, for the claims of the token and for the `Authorization` header, and OAuth2 plans can require a subscription.
* **Catalog**: the Catalog imports an MCP server that the control plane can't reach, from the list responses you supply.
* **Human In the Lead**: approval rules hold the tool calls of MCP Proxies and MCP Studios until a person approves or rejects them, with an inbox, notifications, and a decision history.

#### AWS Lambda and Data Cache for LLM Proxies

* In the **Policy Studio** of an LLM Proxy, you can add the **AWS Lambda** and **Data Cache Policy** policies to the request and response phases.
* **AWS Lambda** invokes an AWS Lambda function. It isn't included in the default distribution, so [download](https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-aws-lambda/) version 3.5.0 or later of its plugin and [deploy it](https://documentation.gravitee.io/apim/plugins/deployment) first.
* **Data Cache Policy** reads, writes, and removes values in a cache resource of the LLM Proxy, so add a cache resource on the **Resources** page first. See [Resources](../agent-management/build/configure-an-llm-proxy.md#resources).

#### Alerts for MCP Proxies

* A new **Alerts** page in the **Monitoring** group of an MCP Proxy lists its alerts, and adds, edits, enables, disables, and deletes them. Each alert notifies you when the traffic of the proxy matches its rule.
* Four rules watch the requests of the proxy: a condition on a request metric, no request for a period of time, the aggregated value of a request metric, and the rate of requests that meet a condition. Filters narrow the events that a rule evaluates, and the **Error Key** values include the error keys of the MCP Proxy.
* Alerts notify through **System email** and the notifiers installed on the platform, such as **Email**, **Slack**, and **Webhook**. Dampening limits how many notifications an alert sends when it fires several times for the same condition, and timeframes limit when it sends them. When you open a saved alert, the secrets of its channels stay masked.
* The **History** tab of an alert lists its events.
* Alerts require Alert Engine.
* See [Configure MCP Proxy alerts](../agent-management/build/configure-mcp-proxy-alerts.md).

#### API Score for MCP Proxies

* A new **API Score** page in the **General** group of an MCP Proxy rates the proxy against the rulesets of its environment, and lists the findings of each asset by severity. The page appears when API Score is turned on for the environment.
* **Evaluate** starts an evaluation, and the page shows that it's running until it ends. A successful evaluation replaces the previous result. An evaluation requires an installation connected to Gravitee Cloud.
* On the **API Score** page of Platform Management, the name of an MCP Proxy and **View API-level Score Details** open the **API Score** page of the MCP Proxy in Agent Management.
* See [Review the MCP Proxy API Score](../agent-management/build/review-the-mcp-proxy-api-score.md).

#### HTTP/2 fields and the API key header of MCP Proxies

* When the **HTTP version** is **HTTP/2**, the **HTTP configuration** section of the **Advanced settings** on the **Endpoint** page of an MCP Proxy shows four new fields: **HTTP/2 multiplexing limit**, **HTTP/2 max frame size (bytes)**, **HTTP/2 connection window size (bytes)**, and **HTTP/2 stream window size (bytes)**. The **Advanced settings** that **Configure** opens for an MCP server of the Catalog show the same fields.
* When the API key of an MCP Proxy was saved without a header, the **Endpoint** page shows the **Injection location** as **x-api-key header**, the header the gateway sends the key in, and saving a new key keeps it there. Before 4.14, the page showed **Authorization header**, and saving a new key moved the key to the `Authorization` header.
* See [Configure the MCP Proxy endpoint](../agent-management/build/configure-mcp-proxy-endpoint.md#adjust-the-advanced-settings) and [Configure Upstream Authentication](../agent-management/build/configure-your-mcp/README.md#configure-upstream-authentication).

#### Proxy pages name the proxy instead of the API

* The pages of an LLM Proxy, MCP Proxy, or A2A Proxy now name the type of proxy where they named an API. The out-of-sync banner reads **This LLM proxy is out of sync**, **This MCP proxy is out of sync**, or **This A2A proxy is out of sync**, and its dialog reads **Deploy your LLM proxy**, **Deploy your MCP proxy**, or **Deploy your A2A proxy**. AI workspaces share the banner and read **This AI workspace is out of sync** and **Deploy your AI workspace**.
* In the **Design** group of the proxy sidebar, **API Properties** is now **Properties**. On the **Settings** page, **API Picture** and **API Background** are now **Picture** and **Background**, and the **API Events** card is now **Runtime**.
* The read-only notices, empty states, confirmations, and permission messages of those pages name the type of proxy in the same way, for example the **Select LLM proxy member** field when you transfer ownership.

#### Manual import of MCP servers

* The **Add MCP server** wizard of the Catalog now offers two ways to add a server. **Import from discovery** is selected when the wizard opens. **Import manually** adds a server in a private network that the control plane can't reach, from the `tools/list`, `prompts/list`, and `resources/list` responses that you collect and then paste or upload.
* When **Verify URL** ends with **Connection failed.**, the wizard offers **Import capabilities manually instead** and keeps the URL.
* The **MCP Servers**, **Tools**, **Prompts**, and **MCP Resources** lists have a new **Import** column, which reads **Remote** or **Manual**. The **Overview** card of a server, tool, prompt, or resource shows the same value.
* A manual import has **Update capabilities** in place of **Re-sync**. It replaces the tools, prompts, and resources of the server with the list responses you supply.
* The module's REST API validates list responses, imports a catalog entry, and exports one. An exported entry imports into another environment.
* See [Import an MCP server manually](../agent-management/import/import-an-mcp-server-manually.md).

#### JWT plan settings for MCP Proxies and MCP Studios

* The **Advanced settings** of a JWT plan on an MCP Proxy or MCP Studio have two new switches. They appear in the **Secure** step of the MCP Proxy and MCP Studio creation wizards, and in the **Security** step of a plan.
* **Extract JWT claims** puts the claims of the token on the `jwt.claims` context attribute, for the policies that follow. It's off by default.
* **Propagate Authorization header** keeps the `Authorization` header on the request after the gateway validates the token. A new plan starts with it off.
* See [Configure a JWT plan](../agent-management/build/configure-your-mcp/manage-mcp-proxy-plans.md#configure-a-jwt-plan).

#### Require a subscription on OAuth2 plans of MCP Proxies and MCP Studios

* OAuth2 plans of MCP Proxies and MCP Studios have a new **Require a subscription** switch, off by default. With it on, the gateway accepts a token only when its client ID belongs to an application subscribed to the plan. With it off, the plan accepts a valid token without a subscription, as before 4.14.
* The switch is in the **Subscriptions** card of the plan's **Security** step, and in the **Secure** step of the MCP Proxy and MCP Studio wizards for **Gravitee as Authorization Server** and **External Authorization Server**. Turning it on for a published or deprecated plan asks for confirmation. The plan list shows a **Subscription required** badge on a plan that has it on.
* See [Require a subscription](../agent-management/build/configure-your-mcp/manage-mcp-proxy-plans.md#require-a-subscription).

#### Encryption of dynamic properties for LLM, MCP, and A2A Proxies

* On the **Properties** page of an LLM Proxy, MCP Proxy, or A2A Proxy, the actions menu of a dynamic property now offers **Encrypt value**, while the property is unencrypted, and **Remove (re-added on next sync)**. It no longer offers **Edit**.
* An encrypted dynamic property carries the `Encrypted` and `Dynamic` badges, and a sync keeps it encrypted. A dynamic property that you remove comes back at the next sync, unencrypted unless **Encrypt on fetch** is on.
* The **Dynamic properties** page has a new **Encrypt on fetch** switch, off by default, which stores every synced value encrypted.
* An import now skips a key that matches a dynamic property, and lists it under **Skipped (synced by the dynamic provider):**.
* When the proxy is managed by the Kubernetes operator, the **Properties** page is now read-only.
* See [Encrypt or remove a dynamic property](../agent-management/build/configure-properties-for-your-proxies.md#encrypt-or-remove-a-dynamic-property).

#### CORS for A2A Proxies

* A new **CORS** page in the **Design** group of an A2A Proxy lets web pages served from other origins call the agent directly from the browser.
* The page sets the allowed origins, methods, and headers, the exposed headers, credentials, private network access, and the preflight cache duration, and whether policies run on preflight requests. On a new A2A Proxy, CORS is off until you enable it.
* The **Request validation** card of the page has a **Reject null byte** switch. It applies to every request to the proxy, whether or not CORS is enabled, and an A2A Proxy that you create starts with it on.
* On the **CORS** pages of LLM Proxies, MCP Proxies, and A2A Proxies, the page now checks an origin when you add it. A save that changes the CORS settings while CORS is enabled is now refused when it has no allowed origin, no allowed method, a method other than `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, `TRACE`, `CONNECT`, or `*`, or **Access-Control-Allow-Credentials** on while `*` is an allowed origin.
* See [Configure A2A Proxy CORS](../agent-management/build/configure-a2a-proxy-cors.md).

#### Human In the Lead

* A new **Human In the Lead** group in the Agent Management sidebar holds the **Inbox**, **Rules**, **Notifications**, and **History** pages. It requires a license that includes Human In the Lead.
* An approval rule names the tool calls that wait for a person: catalog tools or a name pattern, narrowed by argument conditions. It also names the users and groups who decide, and how long they have. A call that nobody decides in time is denied.
* The **Human approval** card on the **Overview** page of an MCP Proxy or MCP Studio turns human approval on for that proxy.
* From the **Inbox**, a call is approved for that call only or for a set time, or rejected with a reason that's returned to the agent.
* Notifications send approval notices by email or webhook, with optional reminders. Their email templates are listed under **Human in the lead** on the **Templates** page of Platform Management.
* The **History** page lists past decisions and what became of each call, and exports them as CSV or JSON files.
* See [Human In the Lead](../agent-management/human-in-the-lead/README.md).

### API Management

API Management adds the following in 4.14:

* **API proxies**: encryption of dynamic properties, and path mappings that group their analytics.
* **API Products**: their own flows, designed in a Policy Studio, a banner that deploys them, their own resources, and OAuth2 plans.

#### Flows on API Products

* The sidebar of an API Product has a **Policy Studio** item in its **Consumers** group. Its **Plan Flows** apply to the requests of one of the product's plans, and its **Common Flows** to the requests of any of them, in the **Request Phase** and the **Response Phase**.
* The flows of an API Product run on every API of the product, only for the requests that come through one of its plans. The flows of the product's plan run first, then the product's common flows, then the API's common flows.
* A rate limit or quota in a flow of an API Product counts the requests of a subscription to every API of the product together.
* An API Product has its own **Mode** and **Match required** settings for its flows. With **Match required** on, a request that comes through one of its plans and matches none of its flows gets a `404` response.
* Saving the flows doesn't deploy them. When an API Product is **Out of sync**, its pages show a banner with a **Deploy API Product** button.
* On every deployment of an API Product, the Gateway also checks the license of the policies in its flows. A Gateway that refuses a version keeps serving the version it already had, while the API Product shows **Synced**.
* A Gateway earlier than 4.14 runs the plan flows of an API Product but not its common flows, and ignores its **Mode** and **Match required** settings.
* See [Design API Product flows](../api-management/build/configure-your-api-product/design-api-product-flows.md).

#### Encryption of dynamic API properties

* On the **API Properties** page of an API proxy, a dynamic property now has an actions menu. It offers **Encrypt value**, while the property is unencrypted, and **Remove (re-added on next sync)**.
* An encrypted dynamic property carries the **Encrypted** and **Dynamic** badges, and a sync keeps it encrypted. A dynamic property that you remove comes back at the next sync, unencrypted unless **Encrypt on fetch** is on.
* The **Dynamic properties** screen has a new **Encrypt on fetch** switch, off by default, which encrypts every fetched value before it's stored.
* The **Dynamic properties** screen now saves the settings of an HTTP Proxy or TCP Proxy API in the form that the sync reads. Before 4.14, the sync didn't apply the schedule, the JOLT specification, or the HTTP client, proxy, and SSL settings saved from this screen. Settings saved before 4.14 keep the earlier form until you save them again from this screen. To apply them, change a field on the screen, click **Save changes**, and then deploy the API.
* When the API proxy is managed by the Kubernetes operator, the **API Properties** page is now read-only.
* See [Configure API properties](../api-management/build/configure-your-api-proxy/configure-api-properties.md#manage-existing-properties).

#### Path mappings on API proxies

* A new **Path Mappings** page, in the **Monitoring** group of an API proxy with an HTTP listener, adds, edits, and deletes the path mappings that group the analytics of the API proxy by path, such as `/orders/:orderId`.
* **Import from Swagger** adds the paths of an OpenAPI page of the API proxy's documentation in the next-gen Developer Portal. **Replace existing path mappings** replaces the list with them.
* The import of an OpenAPI specification gains a **Create the path mapping for analytics** option. On an update, it replaces the existing path mappings. Turned off, an update keeps them.
* The path mappings apply the next time you deploy the API proxy.
* The dashboard of an API proxy adds **Top 5 Path mappings**, which counts the requests that matched a path mapping and passed security. **Top 5 Paths** now ranks the paths of the requests, after the API's context path.
* A new **Path mapping** filter narrows a dashboard to the requests of the path mappings you pick.
* See [Configure path mappings](../api-management/build/configure-your-api-proxy/configure-path-mappings.md).

#### Resources on API Products

* A new **Resources** page, in the new **Design** group of an API Product, adds, edits, enables, disables, and removes the resources that the policies of the product use.
* An API Product supports 11 resource types: **Cache**, **Cache Redis**, five OAuth2 providers, three authentication providers, and **Content Provider Inline Resource**.
* A policy in the **Policy Studio** of an API Product uses the product's resources on every API in the product, and the policies of each API keep using that API's resources.
* Known limitation: the Cache policy can't use a Cache resource of the API Product yet. The Data Cache policy can.
* Changes to the resources take effect after you deploy the API Product. Deploying a change to the resources restarts them, so a **Cache** resource starts empty.
* On every deployment of an API Product, the Gateway also checks the license of its enabled resource types. A Gateway that refuses a version keeps serving the version it already had, while the API Product shows **Synced**.
* A Gateway earlier than 4.14 ignores the resources of an API Product. A policy in a plan flow of the product then uses the API's resource with the same name if the API has one, and otherwise fails as if the resource didn't exist.
* The Management API saves the resources of an API Product with an update of the product.
* See [Configure API Product resources](../api-management/build/configure-your-api-product/configure-api-product-resources.md).

#### OAuth2 plans on API Products

* On the **Plans** page of an API Product, **Create plan** now offers **OAuth2**, next to **API Key**, **JWT**, and **mTLS**.
* The **OAuth2 resource** and the **Cache resource** of the plan name resources on the product's **Resources** page. The plan validates tokens with those resources, never with the resources of the product's APIs. Neither field takes an expression.
* Publishing the plan, and saving a published or deprecated plan, fails when a resource it names is an expression, isn't on the product's **Resources** page, isn't of the right type, or is disabled.
* See [OAuth2 plans on an API Product](../api-management/build/configure-your-api-product/api-product-configuration-reference.md#oauth2-plans-on-an-api-product).

### Authorization Management

Authorization Management adds the following in 4.14:

* **As code**: PDP gateways, schema documents, entities, and policies are managed through the Automation API, as Kubernetes resources, and with Terraform.

#### PDP gateways, schema documents, entities, and policies as code

* The Automation API creates or updates a PDP gateway, a schema document, an entity, or a policy from a specification, and reads or deletes it. A dry run validates a specification and reports its findings without saving anything.
* The Gravitee Kubernetes Operator declares them with `AuthzPdp`, `AuthzSchema`, `AuthzEntity`, and `AuthzPolicy` resources.
* The Gravitee Terraform provider declares them with `apim_authz_pdp`, `apim_authz_schema`, `apim_authz_entity`, and `apim_authz_policy` resources.
* See [Custom Resource Definitions](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/overview/custom-resource-definitions) and [Gravitee Resources](https://documentation.gravitee.io/apim/terraform/example-resource-configurations).

### Edge Management

Edge Management adds the following in 4.14:

* **Daemon authentication**: Edge Daemons identify themselves to the Edge Reactor keyless, with mTLS and the certificates of your fleet, or both.
* **OAuth2 plans**: the routes of an intercepted agent take an OAuth2 plan of their target API, so that each developer signs in with your identity provider.
* **Gateway addresses**: the guided setup fills in the gateway addresses that your installation proposes, the addresses stay editable after the setup, and one gateway serves the Edge Management configuration of several environments.
* **Windows devices**: the **Daemon deployment** page has a **Windows** tab, with the download of the Edge Daemon for Windows and its install command.

#### Daemon authentication

* The new **Daemon authentication** page, in the **Configuration** group, and the new **Authentication** step of the guided setup decide how the daemons of an environment identify themselves to the Edge Reactor.
* **Keyless** serves daemons that present no certificate, and every daemon while mTLS is off. It's on by default. **mTLS** serves daemons that present one of the active certificates enrolled on the page, issued by your own PKI. Gravitee never sees a private key. Both can be on at the same time, and at least one always stays on.
* Turning keyless off makes authentication mandatory. Keyless can be turned off once mTLS is on and an enrolled certificate is active.
* The Edge Reactor listener runs over TLS and asks the daemons for a client certificate once you configure it to. By default, it stays plain HTTP. When the listener requires a certificate, a certificate that it doesn't trust fails at the TLS handshake. It trusts the enrolled certificates, and mTLS only accepts a certificate in the environment that enrolled it. See [Secure the Edge Reactor listener](../edge-management/connect/secure-the-edge-reactor-listener.md).
* After the upgrade, the Edge Reactor refuses every call from the daemons of an environment configured before 4.14, until its Edge API is deployed again. Any change that you save in Edge Management for that environment deploys it, for example enrolling a certificate. The redeployed Edge API has keyless on, as by default.
* See [Configure daemon authentication](../edge-management/connect/configure-daemon-authentication.md).

#### OAuth2 plans on intercepted routes

* On the **Interception** page, each route of an intercepted agent takes a **Keyless** or **OAuth2** plan of its target API. For an OAuth2 plan, choose the application subscribed to it.
* The daemons receive the authorization server of the plan's OAuth2 resource and the client of the application, so that each developer signs in with your identity provider.
* **What this route needs** adds four requirements for the plan of a route. A route of the **Claude Code** preset that isn't secured by an OAuth2 plan reports **Check** rather than **Ready**, even when its target API meets every other requirement.
* A target API created from the picker sends the agent's own key to the AI provider through the API key authentication of its endpoint.
* See [Secure a route with an OAuth2 plan](../edge-management/connect/configure-edge-management.md#secure-a-route-with-an-oauth2-plan).

#### Gateway addresses

* The guided setup fills in the **Gateway URL** and the **Reactor URL** with the addresses that your installation proposes, when it proposes them.
* The **Gateway** page now saves a change to either address with **Save & Deploy**. A change only applies to the daemons installed after it, and a warning under the changed field says so. Daemons already installed keep the addresses they were installed with.
* When the installation proposes an address other than the one in the field, the **Gateway** page shows it under the field, with where it comes from.
* The **Reactor URL** that the installation proposes is the address that you set for the environment, or else the address that you set for every environment, which the Helm chart takes from its Edge ingress. See [Propose the Reactor URL to Edge Management](../edge-management/connect/configure-edge-ingress.md#propose-the-reactor-url-to-edge-management).
* The install command of the **Daemon deployment** page passes the ID of the environment, so that each daemon gets the configuration of its own environment.
* See [Change the gateway addresses](../edge-management/connect/set-up-edge-management.md#change-the-gateway-addresses).

#### Edge Daemon on Windows

* The **Daemon deployment** page has a **macOS** tab and a **Windows** tab. Each tab has the download of the daemon for each architecture of its platform, the install command, and the diagnostic and uninstall commands. The Windows download comes in **x64 (amd64)** and **Arm (arm64)**.
* On Windows, the install command runs from PowerShell as Administrator, or as a post-install script that your MDM runs as SYSTEM. The installer registers the daemon as a Windows service that starts at boot.
* The page no longer names Kandji. Run the install command by hand, or as the post-install script of your MDM.
* See [Install the Edge Daemon on Windows](../edge-management/connect/install-edge-daemon-on-windows.md).

#### Changes to the Edge Reactor

* If the Edge Reactor listener can't start, the gateway doesn't start either, for example when the port of the listener is already in use, or when its keystore or truststore can't be read. Before 4.14, the gateway started without the listener.
* The setting for the port of the Edge Reactor listener has a new name. The previous name still works, and the gateway logs a warning at startup. See [Rename the port setting](../edge-management/connect/secure-the-edge-reactor-listener.md#rename-the-port-setting).
* One gateway serves the Edge API of every environment that it deploys, and keeps the configuration of each environment apart. A new gateway setting decides which environment serves the daemons installed without an environment ID. See [Serve several environments from one gateway](../edge-management/connect/secure-the-edge-reactor-listener.md#serve-several-environments-from-one-gateway).
* The Edge API of each environment carries the `gravitee-edge-configuration` sharding tag. An Edge API deployed before the upgrade to 4.14 carries it only once the Edge configuration of its environment is deployed again, for example when you save a change with **Save & Deploy**. A gateway that deploys only the APIs of some sharding tags deploys the Edge API when `gravitee-edge-configuration` is one of them. See [Deploy the Edge API on gateways with sharding tags](../edge-management/connect/secure-the-edge-reactor-listener.md#deploy-the-edge-api-on-gateways-with-sharding-tags).

### Event Stream Management

Event Stream Management adds the following in 4.14:

* **Backend metadata max age**: a Standalone endpoint group, a Cluster, or a Virtual Cluster bounds the metadata requests that the gateway sends to its brokers on its own.
* **Kafka connections**: you can disable the broker hostname verification of a Kafka connection over SSL.
* **Registered Clusters**: Message APIs can use the connections of registered Clusters, and each Cluster lists the APIs that use it.
* **Dynamic properties**: the **API Properties** page of Kafka Services and Message APIs encrypts dynamic properties.

#### Registered Clusters for Message APIs

* The Kafka endpoint group of a Message API now offers **Registered cluster** next to **Direct**, in the creation wizard and on the **Endpoints** page. The group uses a **Cluster** and a **Default connection**, and each endpoint uses one connection of the Cluster, which holds the bootstrap servers and the security.
* A connection that Message APIs can't use shows **(not supported)** after its name, with the reason in its tooltip.
* A Message API follows the changes that you deploy on its Cluster, such as new credentials, without a new deployment of the Message API.
* The **Used by Kafka Services** page of a Cluster and of a Virtual Cluster is now **APIs**. It lists the Kafka Services and the Message APIs that use the Cluster, started or not, with their type, state, and connection, and a search by name. The **APIs** item of the sidebar shows how many APIs use the Cluster.
* When you undeploy a Cluster, or save a **Configuration** that removes a connection, the console lists the started APIs that block the change, each with a link.
* The values of the security settings of a Cluster connection accept a reference to a secret in your secret manager. The Cluster stores only the reference. With the `renewable=true` and `reloadOnChange=true` options, the gateway uses a rotated secret without a new deployment of the Cluster.
* Cluster connections authenticate with every SASL mechanism that the form offers, including `OAUTHBEARER`, `OAUTHBEARER_TOKEN`, `GSSAPI`, and `AWS_MSK_IAM`, and with JKS, PKCS12, and PEM stores given by path or by content, for Kafka Services, Message APIs, and Virtual Clusters.
* The requests and connections that go through a Cluster carry the ID of the Cluster and of the connection in their analytics.
* Only the members of a Cluster bind an API to it, and the Cluster lists of Kafka Services and Message APIs offer those Clusters, plus the Cluster that the API already uses.
* See [Connect a Kafka group to a registered cluster](../event-stream-management/apis/message-apis/configure-endpoints-and-failover.md#connect-a-kafka-group-to-a-registered-cluster), [Manage clusters](../event-stream-management/kafka-infrastructure/clusters/manage-a-cluster.md#see-which-apis-use-a-cluster), and [Bind APIs to a cluster](../event-stream-management/kafka-infrastructure/clusters/manage-cluster-permissions.md#bind-apis-to-a-cluster).

#### Backend metadata max age

* **Backend metadata max age (seconds)** is a new field of the form that the **Edit** button of a **Standalone** endpoint group opens, of the **Configuration** step and page of a Cluster, and of the **Configuration** page of a Virtual Cluster. Empty, the field applies the gateway default. `0` keeps one request per new client connection, as before. A value from `1` to `3600` lets each gateway instance send that request at most about once per that many seconds, whatever the number of clients.
* A Standalone group with a value shows a **Metadata max age** badge in the **Endpoints** list. The read-only **Configuration** card of a Cluster or a Virtual Cluster shows a **Backend metadata max age** row.
* The value of a Cluster or a Virtual Cluster applies to every Kafka Service bound to it once the changes are deployed, without a new deployment of the Kafka Services. The value of a Virtual Cluster applies to every backend, whatever their own Clusters set.
* The feature also ships in APIM 4.13.2.
* See [Set the backend metadata max age of a Standalone group](../event-stream-management/apis/kafka-services/configure-endpoints.md#set-the-backend-metadata-max-age-of-a-standalone-group), [Manage clusters](../event-stream-management/kafka-infrastructure/clusters/manage-a-cluster.md#set-the-backend-metadata-max-age), and [Manage a Virtual Cluster](../event-stream-management/kafka-infrastructure/virtual-clusters/manage-a-virtual-cluster.md#set-the-backend-metadata-max-age).

#### Kafka connections can disable broker hostname verification over SSL

* When the security protocol of a Kafka connection is **Protocol SSL** or **Protocol SASL_SSL**, the gateway checks that the broker hostname matches its certificate. This verification stays on by default.
* **SSL configuration** now includes **Verify Host**, the switch that turns the verification off. Disable it only if you trust the network.
* See [Configure endpoints and failover](../event-stream-management/apis/message-apis/configure-endpoints-and-failover.md).

#### Encryption of dynamic API properties for Kafka Services and Message APIs

* On the **API Properties** page of a Kafka Service or a Message API, a dynamic property now has an actions menu where it showed **Managed**. It offers **Encrypt value**, while the property is unencrypted, and **Remove (re-added on next sync)**.
* An encrypted dynamic property shows **Encrypted** next to **Dynamic**, and later polls keep it encrypted. A dynamic property that you remove comes back at the next poll, unencrypted unless **Encrypt on fetch** is on.
* The **Dynamic properties** form has a new **Encrypt on fetch** switch, off by default, which stores every fetched value encrypted.
* See Configure API properties for [Kafka Services](../event-stream-management/apis/kafka-services/configure-api-properties.md#change-a-property) and for [Message APIs](../event-stream-management/apis/message-apis/configure-api-properties.md#change-a-property).

### Platform Management

Platform Management adds the following in 4.14:

* **Dictionaries**: encryption of the sensitive values of environment dictionaries.
* **Applications**: a **Shared API Keys** page, which renews the shared API key of an application with a value you choose.
* **Additional metrics**: a **Metrics configuration** page for the values that a policy or the gateway attaches to requests and for the values that the Assign metrics policy writes, which the logs and dashboards of API Management and Agent Management now show.

#### Encrypted dictionary properties

* On the detail page of a dictionary, turn on **Encrypt on save** when you add a property, or select **Encrypt** in the actions menu of an existing property, and then select **Save**. A dictionary holds encrypted and unencrypted properties side by side.
* The console masks an encrypted value and never shows it again, while policies still read the original value at runtime. To change an encrypted value in a manual dictionary, select **Replace value**.
* A dynamic dictionary encrypts every value that it fetches from its provider when you select **Encrypt fetched values** while you create or edit it.
* See [Encrypt property values](manage-dictionaries.md#encrypt-property-values).

#### Shared API keys of applications

* A new **Shared API Keys** page, in the **Access** group of an application that uses a shared API key, lists the keys that every subscription of the application shares. **Renew** gives every subscription a new key, and the previous key stays valid for two hours.
* When **Allow custom API Key** is turned on, the **Renew API Key** dialog has a **Custom API Key** field for the value of the new key. A value of an earlier key of the application, even a revoked or expired one, makes that key valid again.
* The feature also ships in APIM 4.13.8 and 4.12.30.
* See [Renew the shared API key](manage-applications.md#renew-the-shared-api-key).

#### Additional metrics

* A new **Metrics configuration** page, in the **System & Security** group of the **Environment** section, lists the additional metrics of the environment, the values that a policy or the gateway attaches to requests. It sets the label, description, and unit of each one, and whether the filter, column, and widget-editor lists offer it. It also declares a metric before any request carries it.
* API Management and Agent Management have a new **Settings** page in their **Observability** group, which shows the same list, read-only, for the API types of the module and for the metrics that belong to no API type.
* On the **Logs** pages of API Management and Agent Management, the detail of a log has an **Additional metrics** section, **View** adds an additional metric as a column of the table, and **Filter by** offers additional metrics, including one that it doesn't list, by its key.
* In the widget editor of a custom dashboard, **Metric** and **Group by** offer additional metrics, including one that they don't list, by its key.
* Custom metrics, the values that the Assign metrics policy writes, are listed on the same page with a **Personal data** badge, and take a label, a description, and a visibility setting. The **Logs** pages show them in a **Custom** section of the log detail and under **Custom** in **View** and **Filter by**, and **Group by** of the widget editor offers them.
* The value suggestions of a filter on a text additional or custom metric list the values that start with what you type, whatever the case.
* See [Configure additional metrics](configure-additional-metrics.md), [Read additional and custom metrics](../api-management/observe/view-api-logs.md#read-additional-and-custom-metrics), and [Select the data on the Data tab](../agent-management/observe/dashboards/build-a-custom-dashboard.md#select-the-data-on-the-data-tab).
