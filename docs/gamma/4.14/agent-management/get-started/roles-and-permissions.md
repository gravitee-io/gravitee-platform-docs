---
hidden: false
noIndex: false
description: The environment-scoped permissions that govern who can view, create, edit, and delete Agent Management resources. Find the permission you need.
---

# Roles and permissions

Gravitee Agent Management uses a Role-Based Access Control (RBAC) system to govern who can view, create, edit, and delete AI resources. Permissions are scoped at the Environment level and applied to specific roles (like Environment Admin, API Publisher, or custom roles).

## Agent Management permissions

The following core permissions govern access to Agent Management capabilities within a given environment:

| Permission | Description |
| :--- | :--- |
| **ENVIRONMENT_AM_CONFIGURATION** | Controls access to the Access Management integration settings. Users with this permission can configure the connection between the Agent Management module and Gravitee Access Management (AM) for features like Identity Provider synchronization. |
| **ENVIRONMENT_AGENT_IDENTITY** | Controls the ability to define and manage Agent Identities. Users with this permission can create, update, or delete the identity profiles that determine how agents authenticate and authorize against MCP tools. |
| **API_SUBSCRIPTION** | Controls the ability to view and manage the consumer subscriptions of LLM Proxies, MCP Proxies, and A2A Proxies: create, accept, reject, and close them, and manage their API keys. |
| **API_PLAN** | Controls the ability to list, create, publish, and close the plans of LLM Proxies, MCP Proxies, and A2A Proxies. |
| **ENVIRONMENT_API** | Controls the ability to create new APIs, including LLM Proxies, MCP Proxies, and A2A Proxies. |
| **API_DEFINITION** | Controls the ability to update the configuration of existing proxies, including modifying the tool composition of an MCP Studio or overriding parameters. |
| **HITL_RULES** | Controls the ability to view, create, edit, and delete the approval rules of Human In the Lead, on the **Rules** page. Users see only the rules that name them in **Rule access**. |
| **HITL_DECISIONS** | Read opens the **Inbox** and **History** pages. Update approves, rejects, and ends time-based approvals. Approving or rejecting a call also requires being in the **Approval ownership** of its rule. The default USER role has read and update. |
| **HITL_NOTIFICATIONS** | Controls the ability to view, create, edit, and delete the saved notifications of Human In the Lead, on the **Notifications** page. |

To manage roles and assign these permissions to users, navigate to the **Settings > Roles** section of the console.
