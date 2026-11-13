---
description: The breaking changes and deprecations in Gamma 4.13 and 4.14 that can affect an existing configuration, script, or integration. Review them before you upgrade.
---

# Breaking Changes and Deprecations

## Breaking changes

Here are the breaking changes for versions 4.X of Gamma, grouped by module. Gamma runs on API Management, so the changes to the Gateway, the Management API, the Automation API, the Developer Portal, and the Helm chart also apply to Gamma. For those changes, see the API Management [Breaking Changes and Deprecations](https://documentation.gravitee.io/apim/release-information/breaking-changes-and-deprecations) page.

### 4.14.0

The following breaking change applies from Gamma 4.14.0.

#### Agent Management

**New JWT plans of MCP Proxies and MCP Studios remove the `Authorization` header**

From 4.14.0, a JWT plan that you create in Gamma for an MCP Proxy or MCP Studio starts with **Propagate Authorization header** off. This applies to the plan that a creation wizard makes for the **JWT** method and to a plan that you create on the **Plans** page. After the gateway validates the token, it removes the `Authorization` header from the request, so the policies that follow and the upstream don't receive it. In 4.13, a new JWT plan had no such setting and kept the header.

Plans created before the upgrade keep their behavior. When you edit a plan that kept the header, **Propagate Authorization header** is on.

After you upgrade, turn on **Propagate Authorization header** in the **Advanced settings** of a new JWT plan when the upstream or a policy reads the consumer's token from the `Authorization` header. The token exchange in [Exchange tokens for upstream MCP servers](../agent-management/build/configure-your-mcp/exchange-tokens-for-upstream-mcp-servers.md) reads it there. For more information, see [Configure a JWT plan](../agent-management/build/configure-your-mcp/manage-mcp-proxy-plans.md#configure-a-jwt-plan).

### 4.13.0

#### API Management

**API notifications no longer list review, support, and rating events**

From 4.13.0, the API notification settings in Gamma no longer show the review, support, and rating events, because they serve only the Classic Developer Portal. These events still fire, and the notification settings that already select them keep them. To change them, use the API's notification settings in the Console.

#### Event Stream Management

**Connection events are selected one by one**

From 4.13.0, the **Reporter Settings** page of a Kafka Service replaces **Enable connection-metrics reporting** with **Connection events**, and **Enable event-metrics reporting** with **Aggregated metrics**. Under **Connection events**, you select **Connected**, **Disconnected**, and **Errors**. **Connected** and **Errors** are selected by default, which matches the 4.12 behavior. **Disconnected** writes a record when a connection closes cleanly, and roughly doubles the records a healthy Kafka Service writes.

In the log detail of a Kafka Service, the record that closes a connection shows when the connection opened and closed and how long it lasted, and **This connection** shows the requests it served for each operation. The request counts are written only when a connection closes cleanly, so select **Disconnected** to see them. If you select **Disconnected** without **Errors**, a connection that fails gets no closing record and appears open.

#### Agent Management

**LLM, MCP, and A2A Proxies no longer export as CRD or Terraform**

From 4.13.0, Gamma exports an LLM Proxy, MCP Proxy, or A2A Proxy only as a Gravitee API definition. The CRD and Terraform export options are removed for these proxies. The Console's export of these APIs is unchanged. Before you upgrade, update any process that exports these proxies from Gamma as CRD or Terraform.

**The Token Exchange Endpoint field is removed from MCP Proxies**

From 4.12.14 and 4.13.0, the OAuth2 generic identity provider form of the MCP Proxy creation flow no longer has a **Token Exchange Endpoint** field, and the plan security configuration of an MCP Proxy no longer has `tokenEndpoint`.

**LLM Routers are named LLM Proxies**

From 4.12.0, LLM Routers are named LLM Proxies in Gamma, and the Agent Management API serves them at `/llm-proxies`.

**Credentials no longer have usage surfaces**

The usage surfaces that credentials had in the 4.13 pre-releases are removed, from the credential forms and from the credential API. An upgrade from 4.12 isn't affected, because 4.12 has no usage surfaces.

#### Authorization Management

**Policy `kind` is optional and deprecated**

From 4.13.0, `kind` is optional when you create a policy with `POST /organizations/{organizationId}/environments/{environmentId}/modules/authz/policies`, and defaults to `GLOBAL`. In 4.12, it was required. `kind` has no effect on evaluation, and it's deprecated in the request, in the response, and as the `kind` filter of `GET /policies`. A policy created without a kind is stored as `GLOBAL`, so `GET /policies?kind=RESOURCE` doesn't return it. The kind of a policy is fixed when the policy is created.

Before you upgrade, update the scripts that create policies or list them by kind.

**The AuthZEN PDP policy follows the AuthZEN Authorization API 1.0**

From 4.13.0, the AuthZEN PDP policy follows the AuthZEN Authorization API 1.0. Its responses change as follows:

* A `400` or `503` response holds only an error object, `{"error":{"status":<code>,"message":"..."}}`, without a decision, context, results, or page.
* When the PDP is unreachable, times out, fails, or isn't ready, a single evaluation returns `503` with an error object, where it previously returned `200` with a deny decision. The new **PDP unavailable HTTP status** setting chooses `200` or `503`, and defaults to `503`. **Cold-start HTTP status** now also defaults to `503`, where it defaulted to `200`. To keep the 4.12 behavior, set both to `200`.
* With `deny_on_first_deny` or `permit_on_first_permit`, a batch evaluation returns fewer results than items when it stops early.
* An item that carries its own `context` no longer inherits the top-level context.
* An invalid item in a batch evaluation returns `{"decision": false, "context": {"reason": "invalid_request", ...}}` within a `200` response, where the whole batch previously returned `400`.
* Responses are always `application/json`, echo the `X-Request-ID` header, and always return `page.next_token`.

Before you upgrade, review how your AuthZEN clients handle errors, unavailable PDPs, and batch evaluations.

**Authorization decisions are written to the `gravitee-decisions` indices**

From 4.13.0, the Elasticsearch reporter writes authorization decisions to `gravitee-decisions-YYYY.MM.DD`, or to `gravitee-decisions` with ILM-managed indices. The `gravitee` prefix follows the reporter's index name. The `authz-decisions` index, template, and ILM policy of the 4.13 pre-releases are removed. The File, TCP, and Gravitee Cloud reporters label each decision with `"type": "decisions"`. To apply an ILM policy, set `reporters.elasticsearch.lifecycle.policies.decisions`, or `es.lifecycle.policies.decisions` in the Helm chart. It applies to the indices created after you set it.

#### Edge Management

**The Edge Reactor keeps its 4.12 behavior**

4.13.0 ships the same Edge Reactor as 4.12. Its endpoints aren't secured by API plans, and a listener that fails to start, for example because its port is in use or its keystore can't be read, is logged and skipped without stopping the node. The reactor reads its port only from `edge.server.port`, which defaults to `18093`. The `edge.port`, `edge.host`, `edge.secured`, and `edge.ssl` settings, and the `gateway.edge.port` and `gateway.edge.ssl` values of the Helm chart, have no effect in 4.13.

A later release secures Edge APIs with API plans, so an Edge API with no plan becomes unreachable and returns `401`. In that release, a listener that fails to start stops the node, and `edge.server.port` is deprecated in favor of `edge.port`. Before you upgrade to that release, provision a plan for each Edge API.

#### Observability

**Custom dashboards belong to a module**

From 4.13.0, each custom dashboard belongs to a module. The dashboard lists of API Management, Agent Management, and Authorization Management show only the dashboards of their own module. A dashboard created without a module in a 4.13 pre-release doesn't appear in any of these lists. The observability API still returns it when you list dashboards with no `module` parameter, at `GET /gamma/organizations/{orgId}/environments/{envId}/observability/dashboards`. An upgrade from 4.12 isn't affected, because 4.12 has no custom dashboards to move.

**The Request URI log filter matches by prefix**

From 4.13.0, the **Request URI** log filter offers only the starts with operator, and matches the start of the request URI. It accepts the `*`, `?`, and `\` wildcards. In 4.12, the filter was named **HTTP Path** and offered only the equals operator. The observability logs search still accepts `EQ` on `URI`, as a deprecated alias of `STARTS_WITH`. Before you upgrade, check the scripts that search logs with an exact URI, because the search now also returns the requests whose URI starts with it.

**`facetSize` is replaced by `limit`, which counts across the whole time range**

From 4.13.0, the analytics time series request, `POST /gamma/organizations/{orgId}/environments/{envId}/observability/analytics/time-series`, takes `limit` to set how many values to return. `facetSize` is a deprecated alias of `limit`, and `limit` wins when a request sends both. The meaning also changes. In 4.12, `facetSize` capped the values in each time bucket. In 4.13, `limit` picks the top values over the whole time range, so every bucket shows the same values. A `limit` above `100` returns `400`.

Before you upgrade, update the scripts that send `facetSize`, and check the charts that rely on each bucket showing its own top values.

## Deprecated functionality

Here is the deprecated functionality for versions 4.X of Gamma, grouped by module.

### 4.14.0

#### API Management

**Alpine Linux images of the Gateway and the Management API are deprecated**

From 4.14.0, the `graviteeio/apim-gateway` and `graviteeio/apim-management-api` images are also published with an `-alpine` suffix: `<version>-alpine`, `<major>.<minor>-alpine`, and, for the latest release, `<major>-alpine` and `latest-alpine`. Each `-alpine` tag points to the same image as the matching tag without a suffix.

The March 2027 release of APIM moves the tags without a suffix, including `<major>` and `latest`, to the Debian image that the `-debian` tags already publish. The June 2027 release stops publishing Alpine Linux images of the Gateway and the Management API. The APIM Console and Developer Portal images aren't affected and stay on Alpine Linux.

To stay on Alpine Linux until then, replace each tag without a suffix with its `-alpine` tag, for example `graviteeio/apim-gateway:4.14-alpine`. To move to Debian, use the `-debian` tags, which the APIM Helm chart already uses by default. Before you switch, check how the Debian image differs:

* `JAVA_HOME` isn't set. The JRE is in `/usr/lib/jvm/temurin-25-jre-<arch>`, for example `/usr/lib/jvm/temurin-25-jre-amd64`, instead of `/opt/java/openjdk`.
* The Java truststore is `/etc/ssl/certs/adoptium/cacerts`. It's regenerated from the system certificates by `update-ca-certificates`.
* `jattach`, `ps`, `wget`, and fonts aren't installed. `curl` is.
* The image is about 40 MB larger to download and about 185 MB larger on disk.

For more information about the image variants, see [Self-host with Docker](https://documentation.gravitee.io/apim/self-hosted-installation-guides/docker#image-variants) in the API Management documentation.

### 4.13.0

#### API Management

**v2 APIs are deprecated**

From 4.13.0, v2 APIs are deprecated. The October 2027 release of APIM removes them. Migrate your v2 APIs to v4 before you upgrade to that release. For more information, see [v2 API Deprecation and Migration to v4](https://documentation.gravitee.io/apim/release-information/v2-api-deprecation) and [Migrate APIs](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis/migrate-apis).
