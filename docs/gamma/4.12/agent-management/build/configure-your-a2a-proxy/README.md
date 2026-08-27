---
hidden: false
noIndex: false
description: Configure an A2A Proxy's behavior, security, and observability from the Gamma console. Follow the steps to apply policies in the Policy Studio.
---

# Configure your A2A Proxy

After creating an Agent-to-Agent (A2A) Proxy, you can configure its behavior, manage security, and establish access controls using the Policy Studio.

The Gamma console provides a visual builder for applying policies and managing flows on your A2A Proxy.

* **[Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md)**: Learn how to use the Policy Studio to attach security, transformation, and logic policies to your A2A communications.
* **[Configure logging and tracing](configure-logging-and-tracing.md)**: Control the reported request and response data, and enable OpenTelemetry tracing.

## A2A Proxy Navigation

When you open an A2A Proxy from the dashboard, you can configure it using the sidebar navigation groups:

* **General**:
  * **Overview**: View proxy status and deployment history.
  * **General**: Manage the proxy's name, description, and status.
  * **Endpoint**: Configure the target URL of the upstream agent.
  * **API Properties**: Manage dynamic properties that can be evaluated at runtime.
  * **Notifications**: Choose which API events send notifications, and where they are delivered. See [Configure A2A Proxy notifications](../configure-a2a-proxy-notifications.md).
* **Gateway**:
  * **Reporter Settings**: Control the reported request and response data, and configure OpenTelemetry tracing. See [Configure logging and tracing](configure-logging-and-tracing.md).
* **Design**:
  * **Policy Studio**: Design your flows and apply policies to agent-to-agent communication.
* **Monitoring**:
  * **Audit Logs**: Review the changes made to the proxy.
* **Observability**: Monitor the proxy with **Dashboard**, **Logs**, and **Tracing**.
* **Operations**:
  * **Deployment**: Choose which gateway instances load the proxy, and review past deployments. See [Configure A2A Proxy deployment](../configure-a2a-proxy-deployment.md) and [Review A2A Proxy deployment history](../review-a2a-proxy-deployment-history.md).
