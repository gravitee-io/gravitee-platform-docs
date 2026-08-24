---
hidden: false
noIndex: false
description: Add an AI model to the Catalog so authorization policies, observability, and cost attribution can reference it. Follow the steps to import one.
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
| **Pricing**            | Input and output cost per 1M tokens, used for cost attribution.               |

## Import models

To add new AI models to your catalog, connect a provider and import them:

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **AI Models**.
3. Select **Add AI Model**.
4. **Choose source type**: Select an LLM provider or Azure AI Foundry to import deployed models.
5. **Configure connection**: Enter the required credentials (e.g., Azure Subscription ID, Resource Group, Account Name, and Bearer Token).
6. **Select models**: Select which available models from the provider to activate in the catalog.
7. **Review**: Confirm the inventory result (available models vs. active models) and the detected capabilities.
8. Select **Import**.

The selected models appear in the Catalog and become available for use in LLM Proxy configurations.

## Edit model details

You can adjust the display name and description of an imported model:

1. In the **Catalog** section of the sidebar, select **AI Models**.
2. Select the model.
3. Update the **Display name** and **Description**.
   _Note: The Provider, Query name, Family, Context window, Capabilities, and Pricing are derived from the model source and cannot be changed._
4. Select **Save**.

You can also record a price you negotiated with the provider, which replaces the suggested price wherever the price is shown and wherever cost is computed. In the model edit form, enter the negotiated rate in the **Input price ({currency} per 1M tokens)** field, enter the negotiated rate in the **Output price ({currency} per 1M tokens)** field, then select **Save changes**. `{currency}` is the currency of the suggested price and defaults to `USD` when the provider doesn't suggest one. Set both prices, or clear both, and enter a price of `0` or more. Entering `0` in both fields is valid, because a free model is still a priced model.

To go back to the price suggested by the provider, enter that price in both fields again and select **Save changes**.

A model with a negotiated price shows a `Custom` badge next to its price, together with the suggested rate and the date and author of the last change. The negotiated price appears in the **Price / 1M** column of the AI Models list, on the model detail page, and on the models page of an LLM Proxy, and it's used for cost estimates in the AI workspace detail view. Refreshing the catalog updates the provider-derived fields and keeps your display name, description, and negotiated price.

## Next steps

* **Create an LLM Proxy**: Route traffic to cataloged models. See [Create an LLM Proxy](../build/create-an-llm-proxy.md).
* **Republish an LLM Proxy**: Republish any LLM Proxy that consumes a repriced model so cost tracking picks up the negotiated rate.
