---
hidden: false
noIndex: false
description: Configure an A2A Proxy's behavior, security, and observability from the Gamma console. Follow the steps to apply policies in the Policy Studio.
---

# Configure your A2A Proxy

After creating an Agent-to-Agent (A2A) Proxy, you can configure its behavior, manage security, and establish access controls using the Policy Studio.

The Gamma console provides a visual builder to apply policies and manage flows on your A2A Proxy.

* **[Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md)**. Learn how to use the Policy Studio to attach security, transformation, and logic policies to your A2A communications.
* **[Configure deployment](configure-deployment.md)**. Choose which gateway instances load the A2A Proxy.
* **[Configure logging and tracing](configure-logging-and-tracing.md)**. Control the reported request and response data, and enable OpenTelemetry tracing.
* **[Review deployment history](review-deployment-history.md)**. Compare deployed versions and roll back to an earlier one.

## A2A Proxy navigation

When you open an A2A Proxy from the dashboard, you can configure it using the following sidebar navigation groups:

* **General**:
  * **Overview**. View proxy status and deployment history.
  * **General**. Manage the proxy's name, description, and status.
  * **Endpoint**. Configure the target URL of the upstream agent.
  * **API Properties**. Manage dynamic properties that can be evaluated at runtime.
* **Design**:
  * **Policy Studio**. Design your flows and apply policies to agent-to-agent communication.
* **Observability**. Monitor the proxy with **Dashboard**, **Logs**, and **Tracing**.
