# MCP Servers

{% hint style="danger" %}
**Preview Feature**: MCP Server support is currently in preview. Features and APIs may change in future releases. **This functionality is not production-ready and should be used with caution.**
{% endhint %}

## Overview

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/) Servers in Gravitee Access Management (AM) provide a standardized way to secure and manage access to AI-integrated services and tools.

An MCP Server represents a protected resource that exposes one or more MCP Tools to MCP client applications. Access to these tools is protected by OAuth 2.1 and can be further refined using [Authorization Engines](../authorization-engines/README.md) such as OpenFGA for fine-grained, attribute-based, and relationship-based authorization.

This page provides a high-level overview of MCP Servers and points to the detailed pages for configuration and integration.

## **MCP Servers in AM**

In Gravitee Access Management, an MCP Server represents the configuration of a protected resource, not the actual implementation of the MCP Server.

An MCP Server involves two components: The MCP Server implementation and the MCP Server configuration.

### **MCP Server implementation**

This is the real MCP Server running in the customer’s infrastructure, outside of Gravitee AM. It is responsible for:

* Exposing tools defined by the MCP specification.
* Handling requests from MCP clients.
* Performing the business logic behind each tool.
* Using Gravitee AM for token validation and authorization.

This is a representation of the external MCP Server as a protected resource as defined in Gravitee AM. The MCP Server entry defines:

* **Resource identifiers:** URL corresponding to the external MCP Server endpoint.
* **OAuth 2.1 credentials:** Client ID and Client Secret that identify the MCP Server as a protected resource.
* **MCP Tools:** The list of tools exposed by the MCP Server, each with required OAuth 2.1 scopes.

The MCP Server configuration in AM does not execute tools. Instead, it secures access to them.

## Key capabilities and benefits

MCP Servers in Gravitee AM let you do the following:

* **Secure AI tool access:** Control which client applications can access specific AI tools and operations.
* **Use delegated consent (scopes):** Define OAuth 2.1 scopes per tool so that users can explicitly approve what an application may do on their behalf.
* **Apply fine-grained permissions:** Integrate with Authorization Engines (e.g., OpenFGA) to decide what a user is actually allowed to access, beyond the scopes they have consented to.
* **Centralize authentication and authorization:** Use Gravitee AM as the single place to manage MCP credentials, scopes, policies, and access flows.
* **Audit and monitor:** Leverage Gravitee’s audit logging to track MCP Server usage.
* **Stay standards-based:** MCP Servers are built on OAuth 2.1, resource indicators, token introspection, and AuthZen-compatible authorization evaluation.

## When to use MCP Servers

MCP Servers are designed for scenarios where AI agents or applications need controlled access to backend tools and data, such as:

* **AI agent platforms.** These secure access to tools used by AI agents and assistants.
* **API Gateways for AI services.** These centralize authentication and authorization for multiple AI service providers.
* **Enterprise AI integrations.**&#x54;hese control which internal applications can call AI tools and what they’re allowed to do.
* **Multi-tenant AI applications.** These isolate and secure AI tool access per tenant, customer, or business unit.

## **Using MCP Servers with OpenFGA**

MCP Servers support two complementary layers of access control:

* OAuth 2.1 scopes
* OpenFGA permissions

Both layers must succeed for a tool to be executed securely.

This section explains how they work together, why they must remain separate, and how the MCP Server enforces them at runtime.

### **OAuth 2.1 scopes**

[OAuth](../auth-protocols/oauth-2.0/README.md) 2.1 scopes represent what the user allows a client application to do on their behalf. Scopes are requested by the client and explicitly approved by the user during the authorization flow.

OAuth 2.1 scopes have the following characteristics:

* They are granted at runtime through a consent screen.
* They apply only to the delegated application, not to the user globally.
* They do not define the actual user permissions.

Examples of OAuth 2.1 scopes include the following:

* `files:read`
* `files:write`
* `tools:get_weather`

### **OpenFGA permissions**

[OpenFGA](../authorization-engines/openfga.md) defines the user’s permissions, independent of any client application. These are intrinsic, system-defined permissions describing what the user is actually allowed to access. Permissions determine if a user is allowed to perform an action on a resource.

OpenFGA permissions have the following characteristics:

* They represent the access rights in the domain.
* They are long-lived until explicitly changed.
* They are validated by the Authorization Engine (PDP) through AuthZen.

Examples of OpenFGA permissions include the following:

* `user:alice reader tool:get_weather`
* `user:bob admin tool:invoice_generator`
