---
hidden: false
noIndex: false
---
# Fully self-hosted installation with Docker

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

To run a full Gamma platform yourself with Docker, use one of the Docker installation guides. Both bring up the whole stack (the Management API with Gamma enabled, the Gateway, the consoles, and the datastores) on a single host, and both finish with the Gamma console, the APIM Console, the Developer Portal, and the Gateway running locally.

## Choose a Docker guide

* [Run Gamma with Docker Compose](../self-hosted-installation-guides/docker/docker-compose.md): one Compose file that brings up every component together. Use this for the simplest path.
* [Run Gamma with Docker CLI](../self-hosted-installation-guides/docker/docker-cli.md): start each container yourself with `docker run`. Use this when you want to see each component or fit Gamma into an existing setup.
* **Hybrid with Docker:** run a self-hosted Docker Gateway against a Gravitee Cloud (Next-Gen Cloud) control plane. See [Run a hybrid Gateway with Docker Compose](../hybrid-installation-guides/docker/docker-compose.md) or [with the Docker CLI](../hybrid-installation-guides/docker/docker-cli.md).

## What to expect

Both guides serve every console and the Management API on one host so the Gamma console can sign in. The default username and password for the consoles are both `admin`.

## Next steps

* Once Gamma is running, create your first MCP server. For more information, see [Create your first MCP server](../../agent-management/get-started/create-your-first-mcp-server.md).
