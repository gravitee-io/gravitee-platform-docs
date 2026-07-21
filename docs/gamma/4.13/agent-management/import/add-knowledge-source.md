---
hidden: false
noIndex: false
---

# Add a knowledge source

A knowledge source provides contextual data — documentation, knowledge bases, structured reference material — that agents can access through the Catalog. Adding a knowledge source makes its contents available as context for agents operating through the AI Gateway.

## Knowledge families

When creating a knowledge source, you must first select a resource **Family** so the required configuration stays specific and predictable. 

Currently, the **Documents** family is supported. This is used for assets that should be readable directly as MCP resources, such as repository bundles, file sets, manuals, and curated collections. Other families (such as Vector store, Structured data, Search index, Memory store, and Graph store) are planned for future releases.

## Source modes

You can define the document content using one of two **Source Modes**:

* **Inline**: Paste or type the exact document content directly into the Gamma console.
* **Remote fetch**: Provide a URL or path to a remote document or bundle. Gamma will read the remote file and store its content in the catalog resource. 

For Remote fetch, you can configure the **Document type**:
* **Individual document** (`document.remote_file`)
* **Bundle** (e.g., OpenAPI spec, AsyncAPI spec, GraphQL schema, JSON Schema)

## Add a knowledge source

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Knowledge** list.
3. Select **Add Knowledge Source**.
4. Select the **Family** (e.g., Documents).
5. Select the **Source** mode:
   - For **Inline**, enter the **Document content** directly.
   - For **Remote fetch**, select the **Document type**, enter the **Document URL or path**, and select **Fetch document**.
6. Enter a **Display name** and **Description**.
7. Provide the **Provider**, **Source name**, and **Technical label**.
8. Review the **Preview** section to ensure the runtime-facing summary and content appear correctly.
9. Select **Save**.

## Next steps

* **Add MCP resources** — Catalog server resources. See [Add MCP resources](add-mcp-resources.md).
* **Compose into a Studio** — Include knowledge sources as context in a Composite MCP Server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/knowledge/KnowledgeForm.tsx -->
