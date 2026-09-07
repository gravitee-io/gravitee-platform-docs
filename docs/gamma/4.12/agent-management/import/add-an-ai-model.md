---
hidden: false
noIndex: false
description: Add an AI model to the Catalog so an LLM Proxy can route to it. Follow the steps to import models from a provider and edit their details.
---

# Add an AI model

AI models are Catalog entities that represent the models an LLM Proxy can route to. Cataloging a model records the metadata a proxy needs to reach it, in one entry that every proxy in the environment can reuse. You add models by connecting a provider and selecting which of its models to activate.

## AI model catalog fields

Each AI model in the Catalog records the following metadata:

| Field              | Description                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| **Provider**       | The upstream provider, derived from the connection the model was imported from.                 |
| **Query name**     | The technical identifier a proxy sends upstream when it calls this model.                       |
| **Display name**   | The name shown for this model across the console.                                                |
| **Description**    | What this model is best used for.                                                                |
| **Family**         | The model family, for example, `gpt` or `claude-sonnet`.                                          |
| **Context window** | The maximum token context this model supports.                                                   |
| **Capabilities**   | What the model can handle, for example, `text`, `vision`, `reasoning`, or `function-calling`.     |
| **Pricing**        | Input and output cost per 1M tokens, as the source records them.                                 |

## Import models

Models reach the Catalog through the same flow that connects a provider.

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **AI Models**.
3. Click **Add provider**.
4. On the **Choose source type** step, select a model provider or **Azure AI Foundry**.
5. Click **Next**. Selecting **Azure AI Foundry** adds a **Configure connection** step, where you enter the Azure subscription ID, resource group, account name, and bearer token before continuing.
6. On the **Select models** step, select the models to activate in the catalog.
7. Click **Next**.
8. On the **Review** step, confirm the connection and the inventory result, which reports the number of available models, the number that become active in AI Models, and the capabilities the selection covers.
9. Click **Import**. The button carries the number of models you selected.

The selected models appear in the Catalog and become available to LLM Proxy configurations. Models you already imported from that connection are skipped rather than duplicated.

For the full connection details of each source type, see [Connect integrations](connect-integrations.md).

## Edit model details

You can change the display name and the description of a model in the Catalog. The rest of a model's metadata comes from the source it was imported from and is read-only.

1. In the **Catalog** section of the sidebar, select **AI Models**.
2. Select the model.
3. Click **Edit**.
4. Update the **Display name** and the **Description**.
5. Click **Save changes**.

Both edits survive a re-sync. Re-syncing a model provider refreshes only the fields that provider owns, so a display name and description you set aren't overwritten. See [Connect integrations](connect-integrations.md).

## Next steps

* **Create an LLM Proxy.** Route traffic to cataloged models. See [Create an LLM Proxy](../build/create-an-llm-proxy.md).
