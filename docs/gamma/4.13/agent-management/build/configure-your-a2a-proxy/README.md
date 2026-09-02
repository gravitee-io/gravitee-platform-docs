---
hidden: false
noIndex: false
description: Configure an A2A Proxy's behavior, security, and observability from the Gamma console. Follow the steps to apply policies in the Policy Studio.
---

# Configure your A2A Proxy

After creating an Agent-to-Agent (A2A) Proxy, you can configure its behavior, manage security, and establish access controls using the Policy Studio.

The Gamma console provides a visual builder to apply policies and manage flows on your A2A Proxy.

* **[Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md)**. Learn how to use the Policy Studio to attach security, transformation, and logic policies to your A2A communications.
* **[Manage A2A Proxy plans](manage-a2a-proxy-plans.md)**. Create, publish, and close the plans that control how consumers authenticate to the proxy.
* **[Configure logging and tracing](configure-logging-and-tracing.md)**. Control the reported request and response data, and enable OpenTelemetry tracing.

## A2A Proxy navigation

When you open an A2A Proxy from the list, the sidebar offers the following groups:

* **General**:
  * **Overview**. View the owner, version, context path, and dates of the proxy, and copy its gateway URL and upstream agent URL.
  * **Configuration**. Manage the general settings of the proxy.
  * **API Properties**. Manage the key/value properties that policies read at runtime, import them in bulk, or sync them from an HTTP endpoint. See [Configure properties for your proxies](../configure-properties-for-your-proxies.md).
* **Security**:
  * **User Permissions**. Manage who can view and manage the proxy.
* **Design**:
  * **Endpoint**. Configure the target URL of the upstream agent and the upstream authentication.
  * **Policy Studio**. Design your flows and apply policies to agent-to-agent communication. See [Add policies to your A2A Proxy](add-policies-to-a2a-proxy.md).
  * **Resources**. Manage the resources that the policies and the OAuth2 plans of the proxy reference by name. See [Configure resources for your proxies](../configure-resources-for-your-proxies.md).
* **Consumer Access**:
  * **Plans**. Create, publish, and close the plans that control how consumers authenticate. See [Manage A2A Proxy plans](manage-a2a-proxy-plans.md).
  * **Consumers**. Create, approve, reject, and close the subscriptions to the plans. See [Manage subscriptions](../../publish/manage-subscriptions.md).
  * **Broadcasts**. Send a one-way announcement to the consumers of the proxy. See [Broadcast messages to proxy consumers](../broadcast-messages-to-proxy-consumers.md).
* **Monitoring**:
  * **Audit Logs**. Review the audit trail of the proxy. See [Review audit logs](../../observe/review-audit-logs.md).
  * **Reporter Settings**. Configure the reported request and response data and OpenTelemetry tracing. See [Configure logging and tracing](configure-logging-and-tracing.md).
  * **Notifications**. Choose which API events send notifications and where they're delivered. See [Configure A2A Proxy notifications](../configure-a2a-proxy-notifications.md).
* **Observability**. Open the **Dashboard**, **Logs**, and **Tracing** views of the proxy in a new tab.
* **Operations**:
  * **Deployment**. Configure the deployment of the proxy under **Configuration**, and review its deployments under **History**. See [Configure A2A Proxy deployment](../configure-a2a-proxy-deployment.md) and [Review A2A Proxy deployment history](../review-a2a-proxy-deployment-history.md).

The **Broadcasts**, **Audit Logs**, and **Notifications** items appear only when your role can read them.
