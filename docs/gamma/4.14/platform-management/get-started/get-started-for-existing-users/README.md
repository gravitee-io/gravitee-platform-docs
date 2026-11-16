---
hidden: false
noIndex: false
description: Already running Gravitee? Activate Gamma on your existing installation instead of installing from scratch. Choose the path for how you run it.
---
# Get started for existing users

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

If you already run Gravitee, you turn Gamma on rather than installing from scratch. Activating Gamma means moving to the Gamma build (the `4.14` images), enabling Gamma on the Management API, and adding the Gamma console. Choose the page for how you run Gravitee today.

## Choose your path

* **Self-hosted with Docker:** [Activate Gamma with Docker Compose](activate-gamma-with-docker-compose.md).
* **Self-hosted with Kubernetes:** [Activate Gamma with Kubernetes (Helm)](activate-gamma-with-kubernetes-helm.md).
* **Next-Gen Cloud:** Activate Gamma on a Gravitee Cloud account and connect a self-hosted Gateway. For more information, see the [hybrid installation guides](../../install/hybrid-installation-guides/README.md).

## Before you start

Gamma is available from APIM 4.12. Agent Management needs an enterprise license that includes the `agent-management` pack. Some features in the other modules also need an enterprise license:

* API Products, in API Management.
* Federation, which you manage from **Integrations** in Platform Management.
* **Alerts**, **Audit**, and **Client Registration**, in Platform Management.

To get a license, contact your Technical Account Manager.

## Next steps

* Once Gamma is running, create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
