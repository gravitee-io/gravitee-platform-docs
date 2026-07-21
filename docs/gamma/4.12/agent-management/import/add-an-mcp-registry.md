---
hidden: false
noIndex: false
---

# Add an MCP Registry
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 52 · Confirmable · Confirm the full list of supported registries in the June release. Needs: Engineering input -->
<!-- GAP: 53 · Documentable · Document the exact UI steps for adding an MCP Registry. Needs: Demo session, Source code -->

{% hint style="warning" %}
**Coming soon.** Connecting to an external MCP registry and browsing or importing its servers is planned for a future release. To add an MCP server today, register it individually by URL. See [Register an MCP server](register-an-mcp-server.md).
{% endhint %}

An MCP Registry is an external catalog of MCP servers. Connecting a registry will let you browse and import MCP servers — along with their tools, resources, and prompts — directly into the Gamma Catalog.

Gamma will work in both directions in the MCP ecosystem: consuming from external registries, and operating as an MCP Registry that other systems can discover and read from. For the publisher side, see [Expose an MCP Registry](../publish/expose-an-mcp-registry.md).

## Supported registries (coming soon)

The registries below are planned for registry-based import. None are connectable yet.

| Registry                         | Description                                     |
| -------------------------------- | ----------------------------------------------- |
| **Gravitee MCP Server Registry** | Gravitee's own registry of curated MCP servers. |
| **GitHub MCP Server Registry**   | MCP servers published to the GitHub ecosystem.  |
| **Smithery**                     | A third-party MCP server registry.              |

## Connect and import (coming soon)

Connecting a registry and browsing it to import servers in bulk is planned for a future release.

Today, add MCP servers **one at a time, by URL**. The guided setup discovers the server's tools, resources, and prompts and walks you through upstream authentication. See [Register an MCP server](register-an-mcp-server.md).

## Next steps

* **Register an MCP server (available now)** — Add a server by URL, including upstream authentication. See [Register an MCP server](register-an-mcp-server.md).
* **Expose your Catalog as a registry (coming soon)** — Publish your Catalog so other systems can discover and consume your MCP servers. See [Expose an MCP Registry](../publish/expose-an-mcp-registry.md).
