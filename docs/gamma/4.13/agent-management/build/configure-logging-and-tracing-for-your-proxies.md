---
hidden: false
noIndex: false
description: Control which request and response data an LLM, MCP, or A2A Proxy reports to logs and analytics, and turn on OpenTelemetry tracing for it.
---

# Configure logging and tracing for your proxies

Each LLM Proxy, MCP Proxy, and A2A Proxy detail view includes a **Reporter Settings** page. The page controls how request and response data is reported for logs and analytics pipelines, and configures OpenTelemetry tracing for the proxy.

## Open the Reporter Settings page

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
3. Select the proxy you want to configure.
4. Under **Monitoring** for an LLM Proxy, or under **Gateway** for an MCP Proxy or an A2A Proxy, select **Reporter Settings**.

<!-- TODO: Screenshot of the Reporter Settings page of a proxy -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-reporter-settings.png" alt=""><figcaption><p>The Reporter Settings page</p></figcaption></figure>

When you change any setting, the **Discard** and **Save changes** buttons appear.

{% hint style="warning" %}
Detailed logging increases storage and can affect gateway performance. Use payload logging and verbose tracing only when needed.
{% endhint %}

## Configure the reporter

The **Settings** card adjusts reporter behavior for the proxy. The card header carries a switch that enables analytics. While that switch is off, every other setting on the page is disabled, and when you save with analytics turned off, tracing is turned off too.

The card groups the logging settings as follows:

| Group                  | Settings                     | Description                                                                                    |
| ---------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| **Logging mode**       | **Entrypoint**, **Endpoint** | Which connection leg to include in reported events: client to gateway, or gateway to upstream. |
| **Logging phase**      | **Request**, **Response**    | Which lifecycle phases to capture.                                                             |
| **Content data**       | **Headers**, **Payload**     | Optional inclusion of headers and bodies in log payloads.                                      |
| **Display conditions** | **Request phase condition**  | An optional Expression Language filter for the request phase. Leave it empty to log all requests. |

The phase, content, and condition settings stay disabled until at least one logging mode, **Entrypoint** or **Endpoint**, is enabled.

For example, the condition `{#request.headers['Content-Type'][0] == 'application/json'}` only logs JSON requests.

## Configure OpenTelemetry tracing

The **OpenTelemetry** card configures distributed tracing and OpenTelemetry log correlation through the following settings:

* **Trace enabled**. Enables OpenTelemetry tracing for the proxy. Tracing captures execution spans and conditions.
* **Verbose**. Adds detailed span events with headers, context attributes, and policy execution details. Requires **Trace enabled**. Enable it only for deep debugging, because it increases trace size significantly, and disable it after debugging is complete.
* **OTel Logs**. Emits request and response payloads as OpenTelemetry log records correlated to the active trace. This enables log-to-trace linking in Grafana and other OpenTelemetry-compatible backends. Requires **Trace enabled**.

When you save with **Trace enabled** off, **Verbose** is turned off too.

### Redact span attributes

With **Trace enabled** and **Verbose** both on, the **Span Attribute Redaction** section masks sensitive span attribute values before spans are exported. Without rules, span attributes are exported as-is. The rules defined here belong to this proxy.

To add a rule, follow these steps:

1. Click **Add rule**.
2. In the **New redaction rule** panel, enter an **Attribute Name Pattern**. The pattern is required, and each rule's pattern is unique within the proxy.
3. Select a **Masking Type**:
   * **Full Mask** replaces the entire attribute value. Optional: enter a **Replacement Text**. When it's left blank, the value is replaced with `[REDACTED]`.
   * **Partial Mask** keeps part of the value visible. Set **Prefix chars**, **Suffix chars**, and a single **Mask char**. The panel previews the result.
4. Optional: enter a **Value Filter**, a regular expression matched against the attribute value. The rule fires only when the value matches.
5. Click **Add**.

The rules table lists each rule's **Attribute Pattern**, **Masking**, and **Value Filter**. To change a rule, open it with its edit button, adjust it, and then click **Save**. To remove a rule, click its delete button. Like every other setting on the page, rule changes take effect when you save and deploy.

## Save and deploy

Saving doesn't deploy the change. Click **Save changes**, or click **Discard** to abandon the pending edits. After a save, the proxy shows the **This API is out of sync** banner until the change is deployed. Click **Deploy** on the banner, and then confirm to push the configuration to the gateway.

## Verification

To verify the reporter settings are configured as expected, follow these steps:

1. Enable analytics with the switch on the **Settings** card, turn on the **Entrypoint** logging mode and the **Request** phase, and then click **Save changes**.
2. Click **Deploy** on the **This API is out of sync** banner, and then confirm.
3. Return to the **Reporter Settings** page. The switches reflect the saved configuration, and the out-of-sync banner is gone.

<!-- TODO: Screenshot of the Reporter Settings page with analytics enabled and saved -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-reporter-settings-verification.png" alt=""><figcaption><p>The saved reporter settings</p></figcaption></figure>

## Next steps

* [Inspect your agent log](../observe/inspect-your-agent-log.md). Read the OpenTelemetry spans that trace each invocation through the AI Gateway.
* [Review audit logs](../observe/review-audit-logs.md). Trace configuration changes to the proxy.
