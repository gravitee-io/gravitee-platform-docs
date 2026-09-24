---
hidden: false
noIndex: false
description: Choose what a Message API reports in Event Stream Management, from runtime logs and message sampling to OpenTelemetry traces. Follow the steps to configure its reporter settings.
---

# Configure reporter settings

The reporter settings of a Message API decide what it reports: the runtime logs of its connections and messages, how many messages those logs keep, and its OpenTelemetry traces. What the Message API reports is what Observability shows for it.

Every option costs storage and gateway throughput. Recommended: Turn on message content and verbose tracing for an investigation, then turn them off.

## Open the reporter settings

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Operations** group of the Message API sidebar, click **Reporter Settings**.

Without permission to change the Message API's definition, the page is read-only.

## Turn on runtime logs

1. Turn on the switch next to the **Settings** title. The **Logging mode**, **Message sampling**, **Display conditions**, and **OpenTelemetry tracing** options become available.
2. Under **Logging mode**, select what to capture:
    * **Entrypoint**. The exchange between the client and the gateway.
    * **Endpoint**. The exchange between the gateway and the backend broker.
3. Under **Logging phase**, select **Request**, **Response**, or both.
4. Under **Content data**, select what to store with each logged event: **Message content**, **Message headers**, **Message metadata**, or **Headers**, the transport headers of the request itself.

With no logging mode, the connections of the Message API still appear in **Logs**, but no message content is captured. A logging mode without a logging phase captures no content either.

**Message content** writes the body of each logged message to the log store as-is, including any personal or secret data it carries.

## Choose the message sampling

Message sampling decides how many messages of the stream the logs keep.

1. Under **Message sampling**, select a strategy:
    * **Probabilistic**. Keeps a share of the messages, as a probability.
    * **Count**. Keeps one message out of every N.
    * **Temporal**. Keeps at most one message per duration, in ISO-8601 format, for example `PT1S`.
    * **Windowed Count**. Keeps at most a number of messages per duration, in the form `COUNT/DURATION`, for example `1/PT10S`.
2. Enter the value.

Your installation's logging settings set the default value and the limit of each strategy. A value past the limit shows an error that names the limit. A valid value shows the sampling in plain words under the field, for example the share of messages kept.

## Filter the logs

Under **Display conditions**, both conditions are optional and accept Gravitee Expression Language:

* **Request phase condition**. Logs only the requests that meet the condition. Leave it empty to log every request.
* **Message condition**. Logs only the messages that meet the condition. Leave it empty to log every message.

When your organization caps how long runtime logging stays on, the page shows **Logging stops on its own** with the date when logging stops. Saving again pushes the date back.

## Turn on OpenTelemetry

1. In the **OpenTelemetry** section, turn on **OpenTelemetry tracing**.
2. Optional: Turn on **Verbose tracing** to add detailed span events, with headers, context attributes, and policy execution details. Verbose mode makes traces much larger.
3. Optional: Under **Span Attribute Redaction**, click **Add rule** to mask span attributes. Enter an **Attribute Name Pattern**, then choose a **Masking Type**: a full mask that replaces the whole value, or a partial mask that keeps a prefix and a suffix visible.

Redaction rules apply to span attributes only. They don't redact the message payloads written to the runtime logs.

## Save the reporter settings

1. Click **Save changes**.

The console confirms with **Runtime logs settings saved**. The settings reach the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

## Verification

To verify the reporter settings, follow these steps:

1. Deploy the Message API.
2. Open its **Overview** page, and check that no reporting banner is shown.
3. Send traffic to the Message API, then open **Logs** in the **Observability** group of the Message API sidebar, and check that its connections appear.
