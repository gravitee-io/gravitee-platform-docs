---
description: An overview about policies.
metaLinks:
  alternates:
    - policies.md
---

# Policies

## Overview

Gravitee policies are customizable rules or logic the Gateway executes during an API transaction. They modify the behavior of the request or response handled by the APIM Gateway to fulfill business rules during request/response processing. Policies are used to secure APIs, transform data, route traffic, restrict access, customize performance, or monitor transactions.

Gravitee supports the following Kafka policies, which can be applied to Kafka APIs.

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-acl.md">Kafka ACL</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-message-filtering.md">Kafka Message Filtering</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-offloading.md">Kafka Offloading</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-quota.md">Kafka Quota</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md">Kafka Topic Mapping</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-transform-key.md">Kafka Transform Key</a></td><td></td><td></td></tr></tbody></table>

## Policy phases

The request and response of a Kafka API transaction are broken up into the following phases:

* **Entrypoint Connect:** Policies are executed when clients establish TCP connections to Native Kafka entrypoints, before authentication occurs. This allows connection-level filtering (IP allowlists, rate limiting, TLS validation) to reject unauthorized clients before SASL handshake. Available in APIM 4.11.x with Native Kafka reactor 6.x and Agent-to-Agent connectors 2.0.0-alpha.1.
* **Connect:** Policies are executed after plan selection and authentication on the Gateway, but before the client connects to the upstream broker.
* **Interact:** Policies with a global scope (e.g., topic mapping) are executed on all interactions between the client and the Gateway.
* **Publish:** Specific policies acting at the message level are applied to each produced record.
* **Subscribe:** Specific policies acting at the message level are applied to each fetched record.

Which Kafka policies can be applied to each phase is summarized below:

<table><thead><tr><th>Policy</th><th data-type="checkbox">Entrypoint Connect</th><th data-type="checkbox">Connect</th><th data-type="checkbox">Interact</th><th data-type="checkbox">Publish</th><th data-type="checkbox">Subscribe</th></tr></thead><tbody><tr><td>Kafka ACL</td><td>false</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Message Filtering</td><td>false</td><td>false</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Kafka Offloading</td><td>false</td><td>false</td><td>false</td><td>true</td><td>true</td></tr><tr><td>Kafka Quota</td><td>false</td><td>false</td><td>false</td><td>true</td><td>true</td></tr><tr><td>Kafka Topic Mapping</td><td>false</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Transform Key</td><td>false</td><td>false</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>

Kafka policies can be applied to these phases in policy chains of arbitrary length.

### Connector mode support

Only entrypoint connectors support the Entrypoint Connect phase. Endpoint connectors do not.

<table><thead><tr><th>Connector</th><th>Supported Modes</th></tr></thead><tbody><tr><td><code>native-kafka</code> (entrypoint)</td><td><code>ENTRYPOINT_CONNECT</code>, <code>INTERACT</code>, <code>PUBLISH</code>, <code>SUBSCRIBE</code></td></tr><tr><td><code>native-kafka</code> (endpoint)</td><td><code>INTERACT</code>, <code>PUBLISH</code>, <code>SUBSCRIBE</code></td></tr><tr><td><code>agent-to-agent</code> (entrypoint)</td><td><code>ENTRYPOINT_CONNECT</code>, <code>SUBSCRIBE</code>, <code>PUBLISH</code></td></tr><tr><td><code>agent-to-agent</code> (endpoint)</td><td><code>SUBSCRIBE</code>, <code>PUBLISH</code></td></tr></tbody></table>

### Connection interruption

Policies in the Entrypoint Connect phase can reject connections by calling `ctx.interrupt(reason)`, which throws an `InterruptConnectionException`. The reactor catches this exception and closes the socket immediately. This mechanism prevents unauthorized clients from reaching the authentication layer.

### Context limitations

The Entrypoint Connect context provides connection metadata (remote address, local address, TLS session, API attributes) but does not include authentication data, request/response objects, or message payloads. Policies must operate solely on connection-level information.

Available context attributes:

<table><thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>connection.id</code></td><td>String</td><td>Unique identifier for this connection</td></tr><tr><td><code>connection.remoteAddress</code></td><td>String</td><td>Client IP address and port</td></tr><tr><td><code>connection.localAddress</code></td><td>String</td><td>Gateway IP address and port</td></tr><tr><td><code>ssl</code></td><td>EvaluableSSLSession</td><td>TLS session data (cipher suite, peer certificates) if connection uses TLS</td></tr><tr><td><code>context.attributes</code></td><td>Map&lt;String, Object&gt;</td><td>API-level attributes set in configuration</td></tr></tbody></table>

### Policy execution order

When a client connects to a Native Kafka entrypoint, the gateway executes phases in strict order:

1. **TCP/TLS handshake** completes.
2. **Entrypoint Connect phase** policies execute with connection metadata only. If any policy calls `ctx.interrupt()`, the socket closes immediately.
3. **SASL authentication** occurs (username/password or certificate validation).
4. **Interact phase** policies execute for request/response operations.
5. **Publish/Subscribe phase** policies execute during message flow.

This sequence ensures connection-level filtering happens before authentication overhead.

## Gravitee Policy Studio

The **Policies** section takes you to the Gravitee Policy Studio.

<figure><img src="../../../.gitbook/assets/A 11 policy 1.png" alt=""><figcaption></figcaption></figure>

You can use the Policy Studio to create and manage flows. Flows are policy enforcement sequences that protect or transform how APIs are consumed. They control where, and under what conditions, one or more policies act on an API transaction.

Policies are scoped to different API consumers through flows. You can create a flow for an existing plan that applies to only the subscribers of that plan, or a Common flow that applies to all users of the API. For a native Kafka API, only one Common flow is allowed, and only one flow is allowed per plan.

Policies are added to flows to enforce security, reliability, and proper data transfer. Policies can be added to the different request/response phases of a Kafka API transaction in policy chains of arbitrary length.

## Create a policy

1. Click the **+** next to a plan's name to create a flow for that individual plan, or next to **Common** to create a Common flow.
2. Give your flow a name.
3.  Click **Create**.

    <figure><img src="../../../.gitbook/assets/A 11 policy 0.png" alt=""><figcaption></figcaption></figure>
4.  (Optional) In the Flow details panel, select the **Entrypoint Connect** header to add a policy to the **Entrypoint Connect** phase of the Kafka API transaction.

    {% hint style="info" %}
    The Entrypoint Connect phase is available in APIM 4.11.x with Native Kafka reactor 6.x and Agent-to-Agent connectors 2.0.0-alpha.1.
    {% endhint %}

    Select a policy compatible with connection-level context (e.g., IP Filtering, Rate Limiting).

    Configure the policy using available attributes: `connection.remoteAddress`, `connection.localAddress`, `ssl` session data, or `context.attributes`.

    To reject connections, configure the policy to call `ctx.interrupt("reason")` when conditions are not met.

    Fill out the policy configuration details and click **Add policy**.
5.  In the Flow details panel, select the **Global** header to add a policy to the **Interact** phase of the Kafka API transaction.

    <figure><img src="../../../.gitbook/assets/A 11 policy 2.png" alt=""><figcaption></figcaption></figure>

    Choose either the Kafka ACL or [Kafka Topic Mapping](../../../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md) policy.

    <figure><img src="../../../.gitbook/assets/A 11 policy 3.png" alt=""><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.

    <figure><img src="../../../.gitbook/assets/AAA policy.png" alt=""><figcaption></figcaption></figure>
6.  In the Flow details panel, select the **Event messages** header to add a policy to the **Publish** and/or **Subscribe** phase of the Kafka API transaction.

    <figure><img src="../../../.gitbook/assets/A 11 policy 4.png" alt=""><figcaption></figcaption></figure>

    Select the [Kafka Quota](../../../create-and-configure-apis/apply-policies/policy-reference/kafka-quota.md) policy.

    <figure><img src="../../../.gitbook/assets/A 11 policy 5.png" alt=""><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.

    <figure><img src="../../../.gitbook/assets/AAB policy.png" alt=""><figcaption></figcaption></figure>
7. Click **Save** and redeploy your API for changes to take effect.

## Flow schema

The `FlowV4` schema for Native APIs includes an `entrypointConnect` array field. Each element is a `StepV4` object containing policy name, configuration, and execution conditions. The deprecated `connect` field has been removed.

```json
{
  "name": "Connection Filter Flow",
  "enabled": true,
  "entrypointConnect": [
    {
      "name": "ip_allowlist",
      "policy": "ip-filtering",
      "configuration": "{\"whitelist\": [\"10.0.0.0/8\"]}"
    }
  ],
  "interact": [],
  "publish": [],
  "subscribe": []
}
```

## Prerequisites

* Gravitee APIM 4.11.x or later
* Native Kafka reactor 6.x or Agent-to-Agent connectors 2.0.0-alpha.1
* Java 21 runtime
* Native API type (not Proxy or Message APIs)

## Restrictions

* Entrypoint Connect phase is supported only by entrypoint connectors (Native Kafka, Agent-to-Agent). Endpoint connectors do not support this mode.
* Requires APIM 4.11.x or later. Native Kafka reactor 6.x is incompatible with APIM 4.10.x and earlier.
* Policies in this phase cannot access authentication data, request/response headers, or message payloads.
* The `ctx.interrupt()` method throws `InterruptConnectionException`. Policies must handle this or allow it to propagate.
* The deprecated `connect` flow field is removed. Existing APIs using `connect` must migrate to `entrypointConnect`.
* Java 21 runtime is required for Native Kafka reactor 6.x.
