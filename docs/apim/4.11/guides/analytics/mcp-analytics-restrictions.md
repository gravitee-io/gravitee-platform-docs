# MCP Analytics Restrictions and Limitations

## Restrictions

MCP analytics features have the following limitations:

- **Protocol scope**: MCP filters and facets apply only to HTTP-based analytics metrics. They are not available for non-HTTP protocols.
- **Method-dependent filters**: Tool, resource, and prompt filters require the corresponding MCP method to be invoked. For example, `MCP_PROXY_TOOL` is only populated when `keyword_mcp-proxy_method` is `tools/call`.
- **Widget ID generation**: Dashboard widget IDs are generated at creation time using `crypto.randomUUID()` and cannot be manually specified.
- **Template preview image**: The MCP dashboard template preview image is located at `assets/images/templates/mcp-preview.png`.
