---
description: Expose REST APIs governed in API Management as agent-accessible API tools in the Agent Management Catalog.
hidden: false
noIndex: false
---

# Create API tools

API tools bridge API Management and Agent Management. They expose REST APIs governed in API Management as agent-accessible tools in the Catalog. Agents can then invoke your existing APIs through MCP without the APIs needing to learn MCP.

## How it works

The conversion path includes the following stages:

1. A REST API is created and governed in **API Management**. See [Create an API proxy](../../api-management/build/create-an-api-proxy.md).
2. The API is exposed as an **API tool** in the Catalog.
3. The API tool becomes available as a building block in **MCP Studio** alongside MCP-native tools, resources, prompts, and skills.

This bridge means that the enterprise APIs you've already built and governed—including their security plans, rate limits, and policies—become agent-accessible without redevelopment.

## Create an API tool

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section, select **Tools**.
3. Select **Create tool**, and then choose **API tool**.
4. On the **Pick sources** step, search for one or more APIs that have OpenAPI documentation to shape the tool. Selected APIs display their version and their published security plans.
5. On the **Choose capabilities** step, review the endpoints, or capabilities, detected from each selected API source, and then select the specific endpoints, such as `GET /pets`, that you want to transform into tools.
6. Review and adjust the generated **Tool name** and **Tool description** to ensure agents understand when and how to invoke the tool.
7. On the **Review** step, confirm the selected capabilities and APIs.
8. Select **Create API tool**.

The capabilities are extracted, analyzed, and added to the Catalog as individual tools. They become available in MCP Studio's tool palette.

## What an API tool inherits

When you create an API tool from an API proxy, the tool inherits the following:

* **Security plans**. The API tool carries over the security types of the source API's published plans, such as API Key, JWT, Keyless, OAuth2, or mTLS. Agents invoking the tool must satisfy these requirements.
* **Endpoint configuration**. The API tool routes through the API Gateway, preserving existing backend security and upstream configuration.
* **Policies**. Request and response policies applied to the source API continue to execute.

## Next steps

* **Compose into a Studio**. Include API tools in a Composite MCP Server alongside MCP-native tools. See [Create an MCP Studio](../build/create-an-mcp-studio.md).
