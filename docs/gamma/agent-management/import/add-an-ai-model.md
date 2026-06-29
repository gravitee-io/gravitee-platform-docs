---
hidden: false
noIndex: false
---

# Add an AI model

AI models are Catalog entities that represent LLMs from any provider. Cataloging a model gives it an identity that authorization policies, observability, and cost attribution can reference. You can add models by configuring a provider connection and selecting which models to activate.

## AI model catalog fields

Each AI model in the Catalog records the following metadata:

| Field                  | Description                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Provider**           | The upstream provider (derived from the model source).                        |
| **Query name**         | The technical identifier sent to the provider during invocation.              |
| **Display name**       | The human-readable name for this model (e.g., `Claude 3 Opus`).               |
| **Description**        | What this model is best used for.                                             |
| **Family**             | The model family.                                                             |
| **Context window**     | The maximum token context length supported by this model.                     |
| **Capabilities**       | Supported interaction types (e.g., `chat`, `embeddings`).                     |
| **Pricing**            | Input and output cost per 1M tokens, used for cost attribution and routing.   |

## Import models

To add new AI models to your catalog, connect a provider and import them:

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **AI Models** list.
3. Select **Add AI Model**.
4. **Choose source type**: Select an LLM provider or Azure AI Foundry to import deployed models.
5. **Configure connection**: Enter the required credentials (e.g., Azure Subscription ID, Resource Group, Account Name, and Bearer Token).
6. **Select models**: Select which available models from the provider to activate in the catalog.
7. **Review**: Confirm the inventory result (available models vs. active models) and the detected capabilities.
8. Select **Import**.

The selected models appear in the Catalog and become available for use in LLM Proxy routing configurations.

## Edit model details

You can adjust the display name and description of an imported model:

1. Navigate to the **Catalog** → **AI Models** list.
2. Select the model.
3. Update the **Display name** and **Description**. 
   _Note: The Provider, Query name, Family, Context window, Capabilities, and Pricing are derived from the model source and cannot be changed._
4. Select **Save**.

## Next steps

* **Create an LLM Proxy** — Route traffic to cataloged models. See [Create an LLM Proxy](../build/create-an-llm-proxy.md).
* **Configure routing** — Use cost-based or latency-based routing across multiple cataloged models. See [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/models/ModelForm.tsx -->
<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/models/ImportModelsPage.tsx -->
