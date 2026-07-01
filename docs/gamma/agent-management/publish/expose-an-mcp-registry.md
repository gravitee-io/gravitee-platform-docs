---
hidden: false
noIndex: false
---

# Expose an MCP Registry
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 75 · Documentable · Document the exact UI steps for exposing the Catalog as an MCP Registry. Needs: Demo session, Source code, UI verification -->

{% hint style="warning" %}
**Coming soon.** Exposing the Catalog as a discoverable MCP Registry (outbound federation) is part of the platform vision and is planned for a future release. This page describes the intended capability, not a shipped flow.
{% endhint %}

Gamma will work in both directions in the MCP ecosystem: consuming from external registries (see [Add an MCP Registry](../import/add-an-mcp-registry.md)) and operating as an **MCP Registry** that other systems can discover and consume from. Exposing an MCP Registry will make your Catalog's MCP servers — both Native and Composite — available to external MCP clients.

## What exposing a registry will do

When you expose the Gamma Catalog as an MCP Registry:

1. Gamma publishes a discovery endpoint that external systems can query
2. External MCP clients can browse available MCP servers, tools, resources, and prompts
3. Consumers connect to the published MCP servers through the AI Gateway, inheriting all governance (authentication, authorization, observability)

This makes Gravitee a **platform node** in the emerging MCP ecosystem — not just a consumer of MCP servers, but a publisher that other platforms and tools can discover and connect to.

## Configure the registry endpoint (coming soon)

This flow is planned for a future release. It will let you publish a discovery endpoint, choose which Catalog entities to include, and set access control, with all traffic still flowing through the AI Gateway.

The registry endpoint will become available at a discoverable URL that external MCP clients can query to browse available servers.

## What external clients see

External MCP clients querying the registry endpoint can discover:

* Available MCP servers (both Native and Composite)
* Each server's tools, resources, and prompts
* Connection instructions for accessing each server through the AI Gateway

All connections to published MCP servers pass through the AI Gateway, so your governance policies remain in effect even when external clients connect through the registry.

## Next steps

* [Add an MCP Registry](../import/add-an-mcp-registry.md) — Import MCP servers from external registries into the Catalog.
* [Create an MCP Studio](../build/create-an-mcp-studio.md) — Author Composite MCP Servers to publish through the registry.
