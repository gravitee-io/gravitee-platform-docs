---
hidden: false
noIndex: false
---

# Connect integrations

Integrations connect Gamma to upstream AI platforms so that their deployed models can be imported into the Catalog. In Gamma, connecting an integration is done directly through the AI Model import flow.

## Supported integrations

Gamma supports two categories of integrations for model discovery:

**LLM Provider integrations** — Connect to an AI model provider using an API Key or Bearer Token to import their available models into the AI Models catalog. 

**Azure AI Foundry** — Connect to Microsoft Azure to import deployed models from your Azure AI Foundry account.

| Integration                    | Category       | Connection Method                                                                           |
| ------------------------------ | -------------- | ------------------------------------------------------------------------------------------- |
| **Anthropic**                  | Model provider | API Key or Bearer Token.                                                                    |
| **OpenAI**                     | Model provider | API Key or Bearer Token.                                                                    |
| **Google**                     | Model provider | API Key or Bearer Token.                                                                    |
| **Mistral**                    | Model provider | API Key or Bearer Token.                                                                    |
| **Cohere**                     | Model provider | API Key or Bearer Token.                                                                    |
| **Microsoft Azure AI Foundry** | Federation     | Azure credentials (Subscription ID, Resource Group, Account Name, and Azure Bearer Token).  |

## Connect an integration

You connect an integration by importing models from it.

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **AI Models** list.
3. Select **Add AI Model**.
4. **Choose source type**: Select the provider you want to integrate with (e.g., Azure AI Foundry or OpenAI).
5. **Configure connection**: 
   - For **LLM Providers**, this typically uses the built-in integration template.
   - For **Azure AI Foundry**, enter your Subscription ID, Resource Group, Account Name, and an Azure Bearer Token (which you can generate using the Azure CLI: `az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv`).
6. Complete the wizard to import models from the newly connected integration.

Once connected and imported, the models appear in the AI Models catalog and become available for LLM Proxy routing.

## Next steps

* **Add models manually** — For providers without an integration, register models individually. See [Add an AI model](add-an-ai-model.md).
* **Import agents** — View and manage agents synced from connected integrations. See [Import an agent](import-an-agent.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/models/ImportModelsPage.tsx -->
