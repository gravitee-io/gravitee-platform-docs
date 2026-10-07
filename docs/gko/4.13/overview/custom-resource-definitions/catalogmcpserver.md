---
description: The CatalogMcpServer custom resource registers an MCP server in the Agent Management Catalog for the Gravitee Kubernetes Operator 4.13. See the key fields.
---

# CatalogMcpServer

The `CatalogMcpServer` custom resource registers an upstream MCP server in the Catalog of Agent Management. Gravitee discovers the tools, prompts, and resources the server exposes, and the resource's status lists them with the entity IDs that authorization policies reference.

## Overview

A `CatalogMcpServer` declares how Gravitee reaches an MCP server and the identity the server has in the Catalog. GKO checks the resource against the platform before it's admitted, then applies it through the Automation API. Deleting the resource removes the server from the Catalog.

The status reports when the server was last synced, the name and version the server reports, and the negotiated MCP protocol version. It also lists the server's tools, prompts, and resources. Run `kubectl get catalogmcpservers` to see each server's entity ID, endpoint, and last sync.

An [`McpProxy`](mcpproxy.md) in `STUDIO` mode picks its tools from `CatalogMcpServer` resources.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: docs-search-mcp
stringData:
  token: "Bearer <token>"
---
apiVersion: gravitee.io/v1alpha1
kind: CatalogMcpServer
metadata:
  name: docs-search
spec:
  contextRef:
    name: "apim-context"
  entityId: mcp-server.docs-search
  description: Search tools for the product documentation
  connection:
    endpoint: https://mcp.example.com/mcp
    transport: HTTP
    auth:
      type: HEADER
      header:
        name: Authorization
        value: "[[ secret `docs-search-mcp/token` ]]"
```

The `[[ secret ... ]]` expression reads the credential from a Kubernetes Secret. For the syntax, see [Templating](../../guides/templating.md).

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.entityId` | Identity of the server in the Catalog, which authorization policies reference. Starts with `mcp-server.` |
| `spec.description` | Description shown in the Catalog (optional) |
| `spec.connection.endpoint` | URL of the MCP server |
| `spec.connection.transport` | `HTTP`, the Streamable HTTP transport |
| `spec.connection.auth.type` | `NONE`, `HEADER`, or `OAUTH2` |
| `spec.connection.auth.header` | `name` and full `value` of the header sent on every request, for `HEADER` |
| `spec.connection.auth.oauth2` | `clientId`, `clientSecret`, `tokenUrl`, and optional `scope` for OAuth 2.0 client credentials, for `OAUTH2` |

## Validation

* `spec.contextRef` is required.
* `spec.entityId` can't change after the resource is created.
* `spec.connection.auth.header` is set only when `type` is `HEADER`, and `spec.connection.auth.oauth2` only when `type` is `OAUTH2`.
* Deleting a `CatalogMcpServer` that an `McpProxy` still uses is allowed, with a warning that names those `McpProxy` resources.

{% hint style="info" %}
For the full description of each field and of what Gravitee checks when it registers the server, see [Register MCP servers with the Automation API](https://documentation.gravitee.io/agent-management/import/register-mcp-servers-with-the-automation-api).
{% endhint %}
