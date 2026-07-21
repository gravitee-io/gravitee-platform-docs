---
hidden: false
noIndex: false
---

# Create API tools

API tools bridge API Management and Agent Management. They expose REST APIs governed in API Management as agent-accessible tools in the Catalog, so agents can invoke your existing APIs through MCP without the APIs needing to learn MCP.

## How it works

The conversion path:

1. A REST API is created and governed in **API Management** (see [Create an API proxy](../../api-management/build/create-an-api-proxy.md))
2. The API is exposed as an **API Tool** in the Catalog
3. The API Tool becomes available as a building block in **MCP Studio** alongside MCP-native tools, resources, prompts, and skills

This bridge means that the enterprise APIs you've already built and governed — including their security plans, rate limits, and policies — become agent-accessible without redevelopment.

## Create an API tool

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Tools** list.
3. Select **Add Tool**, then choose **API Tool**.
4. **Step 1: Pick sources**
   - Search for one or more APIs with an OpenAPI documentation to shape the tool. Selected APIs display their version and active security plans.
   - Alternatively, use **Add from OAS** to paste an OpenAPI URL or upload a spec file.
5. **Step 2: Choose capabilities**
   - For each selected API source, review the available endpoints (capabilities) detected from its documentation.
   - Select the specific endpoints (e.g., `GET /pets`) you want to transform into tools.
   - You can review and adjust the generated **Tool name** and **Tool description** to ensure agents understand when and how to invoke the tool.
6. **Step 3: Review**
   - Confirm the selected capabilities and APIs.
7. Select **Save**.

The capabilities are extracted, analyzed, and added to the Catalog as individual tools. They become available in MCP Studio's tool palette.

## What an API Tool inherits

When you create an API Tool from an API proxy, the tool inherits:

* **Security plans** — The API Tool carries over the `planSecurityTypes` of the source API (e.g., `API_KEY`, `JWT`, `KEY_LESS`, `OAUTH2`). Agents invoking the tool must satisfy these requirements.
* **Endpoint configuration** — The API Tool routes through the API Gateway, preserving existing backend security and upstream configuration.
* **Policies** — Request/response policies applied to the source API continue to execute.

## Next steps

* **Compose into a Studio** — Include API Tools in a Composite MCP Server alongside MCP-native tools. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/tools/api-tools/Step1Sources.tsx -->
<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/tools/api-tools/Step2Capabilities.tsx -->
