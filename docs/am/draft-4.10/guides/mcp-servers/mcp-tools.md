# MCP Tools

## Overview

MCP Tools are the individual operations that an MCP Server registered in Gravitee Access Management (AM) can expose to AI clients. Each tool describes a single capability, such as "get user profile," "list invoices," or "trigger workflow."

## MCP Tools in Gravitee Access Management

### MCP Tool definition

For each MCP Server, administrators can define one or more tools. A tool typically contains the following information:

* **Name:** A unique identifier for the tool, used by MCP clients. For example `get_weather` or `list_invoices`.
* **Description:** A short, natural-language description that helps LLMs understand when and how to use the tool.
*   **Required scopes:** One or more OAuth 2.1 scopes that must be present on the access token in order to call this tool. For example, `weather:read`, `invoices:read`, or `invoices:write`.

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Scopes must be defined before using the MCP Tool. To define scopes, go to <strong>Settings > Scopes</strong> and create a new scope.</p></div>

### Manage MCP Tools in the UI

To manage MCP Tools, go to **MCP Servers** in the AM Console. Select the MCP Server whose tool(s) you want to manage, and then select **Tools.** From this window, you can perform the following actions:

* Add a new tool.
* Remove a tool.
* Edit the tool name and description.
* Add or remove scopes for the tool.

### Example: Tools on an MCP Server

A billing MCP Server might define tools such as:

* `list_invoices`
  * **Description:** "List invoices for a given customer and date range."
  * **Input schema:** Customer ID, optional date range.
  * **Required scopes:** `invoices:read`.
* `get_invoice_pdf`
  * **Description:** "Retrieve a PDF version of a specific invoic&#x65;_."_
  * **Input schema:** Invoice ID.
  * **Required scopes:** `invoices:read`.
* `cancel_invoice`
  * **Description:** "Cancel an invoice if it is still open."
  * **Input schema:** Invoice ID, optional reason.
  * **Required scopes:** `invoices:write`, `invoices:cancel`.

During the OAuth 2.1 Authorization, client applications request the scopes they need. At runtime, the MCP Server only allows a tool invocation if the following conditions are met:

* The access token contains the required scopes for that tool.
* (Optionally) The configured Authorization Engine (e.g., OpenFGA) returns an `allow` decision for the user and resource.

{% hint style="info" %}
A deeper explanation of how scopes and OpenFGA permissions work together is covered in the dedicated section [#using-mcp-servers-with-openfga](./#using-mcp-servers-with-openfga "mention")
{% endhint %}
