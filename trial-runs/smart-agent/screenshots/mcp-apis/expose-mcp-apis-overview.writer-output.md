# expose mcp apis overview.writer output

## Overview

This guide explains how to expose your APIs as Model Context Protocol (MCP) servers using Gravitee. By transforming your APIs into MCP tools, you enable Large Language Models (LLMs) and AI agents to discover and invoke your API operations without requiring complex connectors.

MCP is an emerging standard that enables AI agents to understand and interact with external tools and data. Exposing your MCP servers through Gravitee API Management (APIM) allows you to maintain governance, observability, and security over interactions between AI agents and your backend services.

## Use cases

Gravitee supports the following MCP integration scenarios:

| Scenario                           | Description                                                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| Proxy an unsecured MCP server      | Add governance, observability, and control to an MCP server that doesn't require authentication |
| Proxy a secured MCP server         | Route traffic to an MCP server that implements its own OAuth authentication flow                |
| Secure an MCP server with Gravitee | Add OAuth2 security to an unsecured MCP server using Gravitee Access Management                 |

## Next steps

* [Proxy an unsecured MCP server](/broken/pages/8434bebb1879c83f676bfa796a53f109d58593d0)
* [Proxy a secured MCP server](/broken/pages/1e99c37904639592705ea456a0d4e16aa74c0c01)
* [Secure an MCP server with Access Management](/broken/pages/34e029d160ee033a8f9950ebde0f7edd19c12eec)
* [Configure MCP access control](/broken/pages/da691a21aeae4af95403dab81a9b3707dec466ca)
