---
description: Everything in the Gravitee Gamma 4.13 release, across Agent, API, Event Stream, and Platform Management. Browse the highlights.
---

# Gamma Release Notes

## Release Date: TBD

## Highlights

* **Agent Management**: Dollar-denominated spend caps on LLM Proxies with the Cost Rate Limit policy, and a configuration audit trail on every LLM, MCP, and A2A Proxy.
* **API Management**: Build or replace an API proxy from a Gravitee v4 definition, an OpenAPI specification, or a WSDL document, and a clearer out-of-sync banner in the API detail workspace.
* **Event Stream Management**: Duplicate an existing Kafka Service to reuse its listener and endpoint configuration under a new name and host prefix.
* **Platform Management**: Environment-scoped dictionaries, gateway routing configuration through sharding tags and entrypoints, organization-wide user administration, and a live view of the gateway instances behind an environment.

## New features

### Agent Management

#### Cost Rate Limit Policy

* Caps what a consumer spends on an LLM Proxy in dollars over a period, and returns `429` once the budget is exceeded. Budgets accept decimals, so `0.05` is five cents and `50` is fifty dollars.
* Charges each request against the budget using the cost the LLM Proxy computes from the prices configured on the models it serves. A **Missing price policy** setting decides what happens to a model with no price.
* Runs in the request phase and coexists with the Token Rate Limit policy on the same flow.
* See [Add the Cost Rate Limit policy](../agent-management/build/add-the-cost-rate-limit-policy.md).

#### Audit Logs for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds an **Audit Logs** page under **Monitoring** that lists the audit events recorded for the proxy.
* Each entry shows the date, the actor, the event type, and the target of the change. Entries that carry a JSON Patch open the exact change in a side panel.
* Filter the trail by event type and date range, and page through entries 10, 25, 50, or 100 at a time.
* See [Review audit logs](../agent-management/observe/review-audit-logs.md).

### API Management

#### Import an API Proxy

* Create an API proxy from a Gravitee v4 API definition, an OpenAPI specification, or a WSDL document. The three formats are available from the **Import API** card on the **Create API Proxy** page.
* Replace the configuration of an existing API proxy from the same three formats, using **Import** on the **General** page of the API proxy.
* Supply each format as a local file or as a remote `http` or `https` URL that the Management API fetches server-side.
* For OpenAPI and WSDL imports, choose whether to create a documentation page from the specification and whether to add an OpenAPI Specification Validation policy. WSDL imports also offer the REST to SOAP Transformer policy.
* See [Import an API proxy](../api-management/build/import-an-api-proxy.md).

#### Out-of-Sync Banner in the API Detail Workspace

* The **This API is out of sync** banner replaces the **This API has undeployed changes.** banner in the API detail workspace.
* The new banner carries an explanation: **Your latest changes are not live yet. Deploy to push them to the gateway.**
* The **Deploy API** button on the banner and the **Out of sync** state badge in the sidebar header are unchanged.
* See [Configure your API proxy](../api-management/build/configure-your-api-proxy/README.md).

### Event Stream Management

#### Kafka Service Duplication

* Create a copy of an existing Kafka Service with **Duplicate** on the service's **General** page. The copy reuses the source service's listener and endpoint configuration.
* Provide a name, a version, and a new listener host prefix for the copy. The host prefix is unique per environment, and the source service's prefix counts as already in use.
* The new service is created in a stopped state and without plans, so you control when it starts accepting connections.
* See [Duplicate a Kafka service](../event-stream-management/build/duplicate-a-kafka-service.md).

### Platform Management

#### Dictionary Management

* Create, edit, search, and delete the dictionaries of the selected environment from the **Dictionaries** page. Dictionaries hold key-value properties that API policies reference at runtime.
* Manual dictionaries hold properties that you maintain by hand and publish to the gateways with the **Deploy** action.
* Dynamic dictionaries poll an HTTP provider at a configured interval, transform the response with a JOLT specification, and publish the refreshed properties automatically while started.
* See [Manage dictionaries](manage-dictionaries.md).

#### Entrypoints and Sharding Tags

* Configure sharding tags, entrypoint mappings, and each environment's default entrypoint values from the **Entrypoints & Sharding Tags** page.
* Sharding tags route APIs to specific gateway groups. Create a tag with an immutable key, restrict it to selected groups, and add the key to the gateway's configuration file.
* Entrypoint mappings define the entrypoint that the Developer Portal displays for APIs that carry a given tag, as an HTTP URL, a TCP port, or a Kafka bootstrap domain pattern, and apply to all environments or to a selection.
* See [Manage entrypoints and sharding tags](manage-entrypoints-and-sharding-tags.md).

#### User Management

* Add, review, and delete the users and service accounts of the organization from the **Users** page, and search the list by name, email, or ID.
* Grant organization roles and per-environment roles from the user's detail page, and manage the group memberships that carry the user's API, API Product, application, and integration roles in each environment.
* Accept or reject a pending registration, convert a user to a service account, and send an Active user a password reset email that opens the reset page of the Gamma console.
* Generate and revoke personal access tokens for a user, and review the APIs, API Products, and applications the user is a member of.
* See [Manage users](manage-users.md).

#### Gateway Instance Monitoring

* Review the gateway instances registered with the selected environment from the **Gateways** page, with each instance's version, status, last heartbeat, address, tenant, and sharding tags.
* Open an instance to read what it reported about itself on the **Environment** tab: its information rows, the plugins it loaded, and its JVM system properties.
* Follow the instance's live resource use on the **Monitoring** tab, which refreshes every 5 seconds and reports CPU, heap, memory pools, uptime, file descriptors, threads, and garbage collection.
* See [Monitor gateway instances](monitor-gateway-instances.md).
