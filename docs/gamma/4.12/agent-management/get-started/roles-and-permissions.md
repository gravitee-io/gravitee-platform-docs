---
hidden: false
noIndex: false
---

# Roles and permissions

Gravitee Agent Management uses a Role-Based Access Control (RBAC) system to govern who can view, create, edit, and delete AI resources. Permissions are scoped at the Environment level and applied to specific roles (like Environment Admin, API Publisher, or custom roles).

## Agent Management permissions

<!-- Source: gravitee-gamma/gravitee-gamma-module-platform/src/main/ui/features/access-management/utils/amConfig.ts @ 6f18c36855 -->
The following core permissions govern access to Agent Management capabilities within a given environment:

| Permission | Description |
| :--- | :--- |
| **ENVIRONMENT_AM_CONFIGURATION** | Controls access to the Access Management integration settings. Users with this permission can configure the connection between the Agent Management module and Gravitee Access Management (AM) for features like Identity Provider synchronization. |
| **ENVIRONMENT_AGENT_IDENTITY** | Controls the ability to define and manage Agent Identities. Users with this permission can create, update, or delete the identity profiles that determine how agents authenticate and authorize against MCP tools. |
| **API_SUBSCRIPTION** | Controls the ability to manage consumer subscriptions for LLM Proxies and MCP Proxies (Accept, Reject, Close). |
| **ENVIRONMENT_API** | Controls the ability to create new APIs, including LLM Proxies and MCP Proxies. |
| **API_DEFINITION** | Controls the ability to update the configuration of existing proxies, including modifying the tool composition of an MCP Studio or overriding parameters. |

To manage roles and assign these permissions to users, navigate to the **Settings > Roles** section of the console.
