---
hidden: false
noIndex: false
description: Configure an A2A Proxy's behavior, security, and observability from the Gamma console. Follow the steps to apply policies in the Policy Studio.
---

# Configure your A2A Proxy

After creating an Agent-to-Agent (A2A) Proxy, you can configure its behavior, manage security, and establish access controls using the Policy Studio.

The Gamma console provides a visual builder to apply policies and manage flows on your A2A Proxy.

* **[Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md)**. Learn how to use the Policy Studio to attach security, transformation, and logic policies to your A2A communications.
* **[Configure logging and tracing](configure-logging-and-tracing.md)**. Control the reported request and response data, and enable OpenTelemetry tracing.

## A2A Proxy navigation

When you open an A2A Proxy from the dashboard, you can configure it using the following sidebar navigation groups:

* **General**:
  * **Overview**. View proxy status and deployment history.
  * **General**. Manage the proxy's name, description, and status.
  * **Endpoint**. Configure the target URL of the upstream agent.
  * **API Properties**. Manage the key/value properties that policies read at runtime, import them in bulk, or sync them from an HTTP endpoint. See [Configure properties for your proxies](../configure-properties-for-your-proxies.md).
  * **Resources**. Manage the resources that the proxy's policies reference at runtime. See [Configure resources for your proxies](../configure-resources-for-your-proxies.md).
* **Design**:
  * **Policy Studio**. Design your flows and apply policies to agent-to-agent communication.
* **Consumer Access**:
  * **Broadcasts**. Send a one-way announcement to the consumers of the proxy. See [Broadcast messages to proxy consumers](../broadcast-messages-to-proxy-consumers.md).
* **Observability**. Monitor the proxy with **Dashboard**, **Logs**, and **Tracing**.
