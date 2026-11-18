---
description: The API Management 4.13 Automation API manages APIM resources declaratively over HTTP. Browse the reference for the endpoints it exposes.
---

# Automation API Reference

## Overview

{% hint style="info" %}
Each version of APIM documents the Automation API it ships. For another version, go to the documentation of that version.
{% endhint %}

The Automation API is the declarative interface to APIM that the Gravitee Kubernetes Operator, the Gravitee Terraform provider, and CI/CD pipelines call. Each request carries the desired state of one resource, and APIM creates or updates the resource to match it.

* To authenticate, address resources, preview a change, and read the result of a call, see [Automation API guide](automation-api-guide.md).
* To browse the endpoints, open the [Automation API reference](https://apim-api-docs.gravitee.io/?v=4.13&api=automation). The viewer includes an option to download the OpenAPI specification.
* A running Management API serves the specification of its own installation at `GET /automation/open-api.yaml`, without authentication. That document includes only the Gamma module resources of the modules loaded on that installation.

## Gamma module resources

Gamma modules add their own resources to the Automation API, under a path segment named after the module. The reference includes the resources of every Gamma module that APIM 4.13 ships. A module resource answers only when the module is installed and the license includes the module's feature.

| Module        | Resources                                                                       | License feature    |
| ------------- | ------------------------------------------------------------------------------- | ------------------ |
| AI Management | `aim/catalog/mcp-servers` (AI Catalog) and `aim/mcp-proxies` (MCP Proxies) | `gamma-aim-module` |

For the error codes a module resource returns, see [Gamma module resources](automation-api-guide.md#gamma-module-resources).
