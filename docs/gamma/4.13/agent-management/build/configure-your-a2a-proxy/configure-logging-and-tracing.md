---
hidden: false
noIndex: false
description: Control which request and response data an A2A Proxy reports to logs and analytics, and turn on OpenTelemetry tracing. Follow the steps to configure it.
---

# Configure logging and tracing

The **Reporter Settings** page controls how request and response data is reported for logs and analytics pipelines, and configures OpenTelemetry tracing for this A2A Proxy.

To open the page, follow these steps:

1. Click **A2A Proxies** in the module sidebar.
2. Select your A2A Proxy.
3. Click **Reporter Settings** in the A2A Proxy sidebar.

When you change any setting, the **Discard** and **Save changes** buttons appear.

After you save, a confirmation notification appears and both buttons disappear until you edit the form again.

<figure><img src="../../.gitbook/assets/gamma-aim-a2a-proxy-reporter-settings.png" alt="The Reporter Settings page for an A2A Proxy, showing the Settings card with the analytics switch on and the logging mode and logging phase groups"><figcaption><p>The Reporter Settings page</p></figcaption></figure>

{% hint style="warning" %}
Detailed logging increases storage and can affect gateway performance. Use payload logging and verbose tracing only when needed.
{% endhint %}

## Configure the reporter

The **Settings** card adjusts reporter behavior for this A2A Proxy. The card's own switch enables analytics. While it's off, every other setting on the card is disabled.

The card groups the logging settings as follows:

| Group                  | Settings                     | Description                                                                                    |
| ---------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| **Logging mode**       | **Entrypoint**, **Endpoint** | Which connection leg to include in reported events: client to gateway, or gateway to upstream. |
| **Logging phase**      | **Request**, **Response**    | Which lifecycle phases to capture.                                                             |
| **Content data**       | **Headers**, **Payload**     | Optional inclusion of headers and bodies in log payloads.                                      |
| **Display conditions** | **Request phase condition**  | An optional Expression Language filter for the request phase. Leave empty to log all requests.  |

The phase, content, and condition settings stay disabled until at least one logging mode, **Entrypoint** or **Endpoint**, is enabled.

For example, the condition `{#request.headers['Content-Type'][0] == 'application/json'}` only logs JSON requests.

## Configure OpenTelemetry tracing

The **OpenTelemetry** card configures distributed tracing and OpenTelemetry log correlation with the following settings:

* **Trace enabled**. Enable OpenTelemetry tracing for this A2A Proxy. Captures execution spans and conditions.
* **Verbose**. Adds detailed span events with headers, context attributes, and policy execution details. Requires **Trace enabled**. Enable only for deep debugging, because it increases trace size significantly, and disable it after debugging is complete.
* **OTel Logs**. Emit request and response payloads as OpenTelemetry log records correlated to the active trace, which enables log-to-trace linking in Grafana and other OpenTelemetry-compatible backends. Requires **Trace enabled**.

<figure><img src="../../.gitbook/assets/gamma-aim-a2a-otel-card.png" alt="The OpenTelemetry card on an A2A Proxy's Reporter Settings page, with the Trace enabled, Verbose, and OTel Logs switches"><figcaption><p>The <strong>OpenTelemetry</strong> card of an A2A Proxy. All three switches are off until you turn them on.</p></figcaption></figure>

### What an A2A trace contains

With **Trace enabled** on, the proxy records one span for each call it forwards to the upstream agent. The span sits under the gateway's invoker span, and the HTTP client span nested below it reports the transport.

The span is named after the JSON-RPC method of the call, such as `message/send`. When the request carries no readable JSON-RPC method, the span is named `a2a` instead.

<!-- TODO: Screenshot of a trace timeline in the Trace Explorer showing the A2A span named after its JSON-RPC method -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-a2a-trace-timeline.png" alt=""><figcaption><p>An A2A span in the trace timeline, named after its JSON-RPC method.</p></figcaption></figure>

The span carries the following attributes:

| Attribute | Value |
| --- | --- |
| `rpc.system.name` | Always `jsonrpc`. |
| `gen_ai.operation.name` | Always `invoke_agent`. |
| `rpc.method` | The JSON-RPC method of the call. Absent when the request carries none. |
| `jsonrpc.request.id` | The JSON-RPC request id. Absent when the request carries none. |
| `server.address` | The upstream agent's host, without scheme, port, or path. |
| `server.port` | The upstream agent's port, filled in from the scheme when the target leaves it implicit. |

<!-- TODO: Screenshot of the span details panel listing the A2A span attributes -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-a2a-span-attributes.png" alt=""><figcaption><p>The attributes of an A2A span.</p></figcaption></figure>

The span records the host and the port, never the full target address. A target can resolve a secret, so it can carry credentials.

Each of the following leaves the rest of the trace intact, and none of them changes the outcome of the request:

* A request that isn't a `POST` is forwarded without its JSON-RPC attributes being read, so the span is named `a2a`.
* A request body that's absent, or isn't JSON-RPC, leaves `rpc.method` and `jsonrpc.request.id` unset, and the span is named `a2a`.
* A target that isn't a valid URI omits both `server.address` and `server.port`.
* A target with no scheme or authority omits both `server.address` and `server.port`.
* A target whose authority carries no host omits both `server.address` and `server.port`.
* A target naming a non-numeric port omits `server.port` and keeps `server.address`.

### Redact span attributes

With **Trace enabled** and **Verbose** both on, the **Span Attribute Redaction** section masks sensitive attribute values before spans are exported. Without rules, span attributes are exported as-is. Global redaction rules are applied first, and the rules defined here are specific to this A2A Proxy and appended after them.

Each rule carries an **Attribute Name Pattern**, a **Masking Type**, and type-specific fields such as **Replacement Text**, **Prefix chars**, **Suffix chars**, and **Mask char**. A rule can also match on the attribute value with a partial-match regular expression.

Adding a rule updates the list on the page only. Click **Save changes** to persist the rule list.

## Verification

To verify the reporter settings are working as expected, follow these steps:

1. Enable analytics, turn on the **Entrypoint** logging mode and the **Request** phase, and click **Save changes**.
2. Deploy the A2A Proxy and send a request to it.
3. Open the logs. The request appears with the captured data. See [Inspect your agent log](../../observe/inspect-your-agent-log.md).
