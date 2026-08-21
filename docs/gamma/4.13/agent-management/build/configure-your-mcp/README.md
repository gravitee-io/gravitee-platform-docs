---
hidden: false
noIndex: false
description: Configure upstream authentication on an MCP Proxy so the Gateway injects the credentials a third-party MCP server needs. Follow the steps to set it up.
---

# Configure your MCP proxy

After you create an MCP Proxy, configure how it handles upstream authentication. These settings control how the proxy authenticates with upstream MCP servers on behalf of your users and agents.

## Upstream Authentication

One of the most important problems the MCP Proxy solves is securing third-party MCP servers such as HubSpot, Salesforce, GitHub, Slack, and Jira. The MCP Proxy handles authentication by injecting the necessary credentials before forwarding the request to the upstream server.

The MCP Proxy currently supports injecting static credentials into the request headers.

## Configure Upstream Authentication

1. In the Gravitee console, navigate to **MCP Proxies**, and then open your MCP Proxy.
2. In the menu under **General**, select **Endpoint**. This page contains the **Upstream authentication** section.
3. Select one of the following authentication methods:
    * **Static credential**. Inject a static credential into a request header on every call.
    * **No upstream auth**. Call the upstream without injecting credentials.
4. If you chose **Static credential**, open the **Credential type** list, and then select one of the following:
    * **API key**. Select an **Injection location** of **Authorization header**, **x-api-key header**, or **Custom header**. If you select **Custom header**, enter the **Header name**. Enter the key in the **Credential** field.
    * **Bearer token**. Enter the token in the **Credential** field. The Gateway injects it as `Authorization: Bearer <token>`.
    * **Basic auth**. Enter the **Username** and **Password / token**. The Gateway injects them as `Authorization: Basic <base64>`.
    * **Custom secret**. Select an **Injection location** of **Authorization header**, **x-api-key header**, or **Custom header**. If you select **Custom header**, enter the **Header name**. Enter the secret in the **Credential** field.
5. Click **Save changes**.

## Next steps

* [Add policies to your MCP server](add-policies-to-mcp-server.md). Apply fine-grained authorization at the tool level.
* [Layered governance for MCP tools](govern-mcp-tool-access.md). Combine authorization, rate limits, and response redaction on one server.
* [Configure deployment](configure-deployment.md). Choose which gateway instances load the MCP proxy.
* [Configure logging and tracing](configure-logging-and-tracing.md). Control the reported request and response data, and enable OpenTelemetry tracing.
* [Review deployment history](review-deployment-history.md). Compare deployed versions and roll back to an earlier one.
