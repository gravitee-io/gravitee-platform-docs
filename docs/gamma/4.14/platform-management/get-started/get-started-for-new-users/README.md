---
hidden: false
noIndex: false
description: New to Gravitee and want to run Gamma? Choose between Gravitee Next-Gen Cloud and installing it yourself. Compare the two paths and pick one.
---
# Get started for new users

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

If you're new to Gravitee and want to run Gamma, choose the path that fits how you want to host it. You can try Gamma on Gravitee Next-Gen Cloud, where Gravitee hosts the platform for you, or install it yourself in your own infrastructure.

## Choose your path

* **Next-Gen Cloud:** Gravitee hosts the Gamma control plane, and you connect your own self-hosted Gateway. To create an account, go to [Gravitee Cloud](https://cloud.gravitee.io). To connect your Gateway, see the [hybrid installation guides](../../install/hybrid-installation-guides/README.md).
* **Run it yourself with Docker:** [Fully self-hosted installation with Docker](fully-self-hosted-with-docker.md) is best for a single host or a local trial.
* **Run it yourself on Kubernetes:** [Fully self-hosted installation with Vanilla Kubernetes](fully-self-hosted-with-vanilla-kubernetes.md) is best for a cluster.

## Before you start

Gamma is available from APIM 4.12. The self-hosted guides use the `4.14` images. Agent Management needs an enterprise license that includes the `agent-management` pack. Some features in the other modules also need an enterprise license:

* API Products, in API Management.
* Federation, which you manage from **Integrations** in Platform Management.
* **Alerts**, **Audit**, and **Client Registration**, in Platform Management.

To get a license, contact your Technical Account Manager.

## Next steps

* Once Gamma is running, create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
