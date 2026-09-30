---
hidden: false
noIndex: false
description: The Design group of an API proxy's sidebar holds the Entrypoints, Policy Studio, Endpoints, Failover, Response Templates, Resources, API Properties, and CORS pages. Choose the page you need.
---

# Design

The **Design** group of an API proxy's sidebar holds the **Entrypoints**, **Policy Studio**, **Endpoints**, **Failover**, **Response Templates**, **Resources**, **API Properties**, and **CORS** pages.

* [**Configure entrypoints**](../../../build/configure-your-api-proxy/configure-entrypoints.md). Change the context paths consumers use to reach an API proxy, or switch to virtual hosts.
* [**Apply security policies**](../../../build/configure-your-api-proxy/apply-security-policies.md). Policies are rules the API Gateway evaluates on every request and response, on top of security plans.
* [**Control how policy flows are matched to requests**](../../../build/configure-your-api-proxy/configure-flow-execution.md). Choose whether the API Gateway runs every matching policy flow or only the closest match.
* [**Reuse policies with shared policy groups**](../../../build/shared-policy-groups.md). A shared policy group configures a set of policies once and reuses them across APIs and flows.
* [**Configure endpoints**](../../../build/configure-your-api-proxy/configure-backend-security.md). Endpoint groups define where the API Gateway routes requests, with load balancing, timeouts, and TLS.
* [**Configure failover**](../../../build/configure-your-api-proxy/configure-failover.md). Turn on automatic retries with a circuit breaker so a slow or failing backend doesn't take your API down.
* [**Configure response templates**](../../../build/configure-your-api-proxy/configure-response-templates.md). Override the gateway's default error payloads on an API proxy.
* [**Configure API resources**](../../../build/configure-your-api-proxy/configure-api-resources.md). Create API-level resources such as caches and OAuth providers that this API's policies reference at runtime.
* [**Configure API properties**](../../../build/configure-your-api-proxy/configure-api-properties.md). Define static or dynamic key/value properties that policies read at runtime through the Expression Language.
* [**Configure CORS**](../../../build/configure-your-api-proxy/configure-cors.md). Let browsers on other origins call your API by enabling cross-origin resource sharing and setting the allowed origins.
