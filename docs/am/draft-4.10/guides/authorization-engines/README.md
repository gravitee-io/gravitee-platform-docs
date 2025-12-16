# Authorization Engines

{% hint style="danger" %}
**Preview Feature:** Authorization Engines are currently in preview. Features and APIs may change in future releases. **This functionality is not production-ready and should be used with caution.**
{% endhint %}

## Overview

Gravitee Access Management (AM) provides a powerful framework for implementing fine-grained authorization. This allows applications and services to apply highly specific access-control rules based on resources, actions, context, attributes, and policies defined centrally in AM.

Instead of relying solely on coarse role-based checks (e.g., "is user an admin?"), fine-grained authorization enables decisions such as:

* Can user X perform operation Y on resource Z?
* Is this action allowed only under certain conditions (time, device, context)?
* Does this client application have permission to access a specific domain, entity, or data partition?

These dynamic authorization decisions are driven by Authorization Engines configured within Gravitee AM. Authorization Engines control access to MCP Servers at a granular level to let you define:

* Which users can access which MCP Servers.
* What operations users can perform on MCP resources.

## Authorization Engines in Gravitee AM

Authorization Engines act as Policy Decision Points (PDP). They evaluate incoming authorization queries sent by MCP Servers or any registered application and return a decision: `allow` or `deny`.

Authorization Engines provide:

* **Centralized policy management:** All authorization logic is maintained in AM.
* **Real-time policy evaluation:** Each authorization request triggers a fresh decision.
* **Plug-and-play integration:** MCP Servers and custom clients can send [AuthZen](authzen.md)-compatible authorization queries using AM’s [APIs](authzen.md#request-format).

In this architecture, the MCP Server acts as the Policy Enforcement Point (PEP). The PEP is responsible for:

* Sending authorization queries (via AuthZen) to the PDP.
* Enforcing the decision returned by the Authorization Engine.

### Supported Authorization Engines

Gravitee supports the [OpenFGA](openfga.md) Authorization Engine. OpenFGA provides relationship-based access control for MCP Servers using:

* Authorization models that define resource types and relationships.
* Relationship tuples that map users to MCP Server resources.
* Permission checks based on relationships and computed permissions.

### Required permissions

To manage Authorization Engines in a domain, the following permissions are required:

* `DOMAIN_AUTHORIZATION_ENGINE[LIST]`: View authorization engines.
* `DOMAIN_AUTHORIZATION_ENGINE[READ]`: View details.
* `DOMAIN_AUTHORIZATION_ENGINE[CREATE]`: Create engines.
* `DOMAIN_AUTHORIZATION_ENGINE[UPDATE]`: Update engines.
* `DOMAIN_AUTHORIZATION_ENGINE[DELETE]`: Delete engines.

### Limitations

* Each domain can have its own authorization engine configuration.
* Only one Authorization Engine per domain can be configured.

## Example workflow with MCP

### Actors

* **User:** The end user of the system.
* **MCP Client:** For example, an AI chatbot.
* **MCP Server:** Server hosting MCP models, contexts, and operations.
* **AM:** Gravitee Access Management.
* **Authorization Engine:** Fine-grained PDP implementation. For example, [the OpenFGA plugin](openfga.md).

### Workflow

1. The client triggers an operation. For example, "execute X."
2. The MCP Server (acting as PEP) sends an authorization query to AM’s Authorization Engine using an [AuthZen](authzen.md) request.
3. AM evaluates policies using the PDP:
   1. AM returns a decision (`allow` or `deny`).
   2. The MCP Server enforces the decision before executing the operation.

<figure><img src="../../.gitbook/assets/auth-eng.jpg" alt=""><figcaption></figcaption></figure>
