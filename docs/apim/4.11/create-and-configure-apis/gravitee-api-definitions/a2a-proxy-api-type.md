# A2A Proxy API Type Overview

## Overview

The A2A Proxy is a V4 API type that enables agent-to-agent communication through the Gravitee API Management platform. It replaces the earlier message-based implementation with a standalone reactor architecture aligned with LLM Proxy and MCP Proxy API types. This feature is available in Enterprise Edition under the AI Agent Management pack and requires Gravitee API Management 4.11 or later.

## A2A Proxy API Type

A2A Proxy APIs are defined with `"type": "A2A_PROXY"` and `"definitionVersion": "V4"`. They use HTTP selectors for flow routing and support REQUEST and RESPONSE flow phases. The management console displays A2A Proxy APIs with the label "A2A Proxy" and the `gio-literal:a2a-proxy` icon.

## Reactor Architecture

The A2A Proxy uses a dedicated reactor plugin (`gravitee-reactor-a2a-proxy`) that operates independently from the message API reactor. The architecture includes:

* **Reactor plugin**: `gravitee-reactor-a2a-proxy`
* **Entrypoint connector**: `gravitee-entrypoint-a2a-proxy`
* **Endpoint connector**: `gravitee-endpoint-a2a-proxy`

The endpoint connector extends the HTTP proxy connector and operates in REQUEST_RESPONSE mode.

## Endpoint Configuration

The A2A Proxy endpoint connector requires a target URL configuration:

| Property | Type | Description |
|:---------|:-----|:------------|
| `target` | String | Target URL for the A2A proxy endpoint. Required, cannot be null or empty. |

**Example:**

```json
{
  "target": "https://agent.example.com/api"
}
```

## Management Console Changes

The management console includes the following A2A Proxy-specific features:

* **API list filter**: "A2A Proxy" filter option available in the API list
* **API type display**: A2A Proxy APIs display with the `policies-a2a.svg` icon (418x255px)
* **Policy compatibility**: Policy plugin mapper recognizes A2A Proxy flow phase compatibility

## UI Library Updates

The following UI libraries were updated to version `17.4.0` to support A2A Proxy flow configuration:

* `@gravitee/ui-particles-angular`
* `@gravitee/ui-policy-studio-angular`
* `@gravitee/ui-analytics`
* `@gravitee/ui-schematics`

These updates include the `GioPolicyStudioFlowA2aFormDialogComponent` for A2A Proxy flow configuration.

## Documentation Generator Support

The documentation generator includes an A2A Proxy API example template (`v4-api-a2a-proxy.json.tmpl`) with the following structure:

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "A2A_PROXY",
    "name": "{{ .Title }} example API",
    "flows": [
      {
        "name": "All plans flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "methods": []
          }
        ],
        "{{ .Properties.phase }}": [
          {
            "name": "{{ .Title }}",
            "enabled": true,
            "policy": "{{ .ID }}",
            "configuration": {{ indent 14 .Node }}
          }
        ]
      }
    ]
  }
}
```
