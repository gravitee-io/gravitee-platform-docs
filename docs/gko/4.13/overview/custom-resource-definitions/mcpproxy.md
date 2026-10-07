---
description: The McpProxy custom resource declares an Agent Management MCP proxy, its plans, and its policy flows for the Gravitee Kubernetes Operator 4.13. See the key fields.
---

# McpProxy

The `McpProxy` custom resource declares an Agent Management MCP proxy: the upstream it exposes, the plans consumers subscribe to, the identity providers those plans authenticate against, its policy flows, and whether it runs.

## Overview

An `McpProxy` has one of two modes:

* `PROXY` exposes one upstream MCP server at the proxy's context path.
* `STUDIO` exposes tools picked from [`CatalogMcpServer`](catalogmcpserver.md) resources, named through `serverRef`.

GKO checks the resource against the platform before it's admitted, then applies it through the Automation API. A `STUDIO` proxy isn't applied until its `CatalogMcpServer` resources have synced. Until then, its `ResolvedRefs` condition is `False`, and GKO tries again later. Deleting the resource deletes the MCP proxy.

The status reports the proxy's state on the Gateway and, for a Studio, the entity ID of each tool. Run `kubectl get mcpproxies` to see each proxy's entity ID, mode, context path, and state.

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: docs-search-upstream
stringData:
  token: "<token>"
---
apiVersion: gravitee.io/v1alpha1
kind: McpProxy
metadata:
  name: docs-search
spec:
  contextRef:
    name: "apim-context"
  entityId: mcp-proxy.docs-search
  name: Docs search
  contextPath: /mcp/docs-search
  mode: PROXY
  proxy:
    serverUrl: https://mcp.example.com/mcp
    upstreamAuth:
      type: BEARER
      bearer:
        token: "[[ secret `docs-search-upstream/token` ]]"
  plans:
    - name: API key
      security:
        type: API_KEY
        apiKey:
          source: HEADER
```

A `STUDIO` proxy names its tools by `CatalogMcpServer`, and gives each server an upstream credential:

```yaml
  mode: STUDIO
  studio:
    tools:
      - serverRef:
          name: docs-search
        tool: search
    upstreamAuth:
      - serverRef:
          name: docs-search
        auth:
          type: NONE
```

## Key fields

| Field | Description |
|:------|:------------|
| `spec.contextRef` | Reference to a `ManagementContext` resource |
| `spec.entityId` | Identity of the proxy, which authorization policies reference. Starts with `mcp-proxy.` |
| `spec.name` | Display name of the proxy |
| `spec.contextPath` | Path the Gateway serves the proxy on |
| `spec.mode` | `PROXY` or `STUDIO` |
| `spec.proxy` | `serverUrl` and `upstreamAuth`, for `PROXY` |
| `spec.studio` | `tools`, `upstreamAuth`, and `enableFGA`, for `STUDIO`. Each tool and credential names a `CatalogMcpServer` in `serverRef`, whose namespace defaults to the proxy's |
| `spec.state` | `STARTED`, the default, or `STOPPED` |
| `spec.flows` | Policy flows of the proxy |
| `spec.identityProviders` | Authorization servers that `OAUTH2` plans reference, with an `oauth2Generic` or `auth0` block for those types |
| `spec.plans` | Plans consumers subscribe to, each with a `name`, a `security` block, and optional `flows` |

The upstream authentication and plan security blocks follow their `type`: `apiKey`, `bearer`, `basic`, or `oauth2` for upstream authentication, and `apiKey` or `oauth2` for plan security.

## Validation

* `spec.contextRef` is required.
* `spec.proxy` is set only when `mode` is `PROXY`, and `spec.studio` only when `mode` is `STUDIO`.
* `spec.mode` and `spec.entityId` can't change after the resource is created.
* Each `serverRef` names a `CatalogMcpServer`.

{% hint style="info" %}
For the full description of each field, and of how plans, flows, and identity providers change when you apply the resource again, see [Manage MCP proxies with the Automation API](https://documentation.gravitee.io/agent-management/build/mcp-proxies/manage-mcp-proxies-with-the-automation-api).
{% endhint %}
