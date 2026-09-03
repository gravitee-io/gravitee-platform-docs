---
hidden: false
noIndex: false
description: Connect Gamma to a model provider or to Azure AI Foundry so their models import into the Catalog, then keep those models in sync. Follow the steps to connect an integration.
---

# Connect integrations

An integration connects Gamma to an upstream AI platform so the models it offers can be imported into the AI Models catalog. You connect an integration from the AI Models import flow, and the same flow selects which models to activate.

## Integration types

Gamma offers two kinds of model integration, and they differ in where the list of importable models comes from.

**Model provider.** Gamma carries a registry of model providers. Selecting one records that provider's base URL, request format, and authentication type on the connection, and the models you can import are the ones the registry lists. Connecting a model provider takes no credentials.

**Azure AI Foundry.** Gamma calls the Azure Resource Manager API with the credentials you supply and lists the model deployments in your Azure AI Foundry account. Only deployments whose provisioning state is `Succeeded` are offered for import.

A connection never stores the credential that reaches the provider. You supply that credential on each LLM Proxy that routes to the imported models. See [Create an LLM Proxy](../build/create-an-llm-proxy.md).

## Supported model providers

The registry lists the following providers. Each provider card shows how many models the registry currently carries for it. The request format is the upstream API an LLM Proxy speaks when it routes to that provider.

| Provider          | Request format | Base URL                                           | Authentication                             |
| ----------------- | -------------- | -------------------------------------------------- | ------------------------------------------ |
| **OpenAI**        | OpenAI         | `https://api.openai.com/v1`                        | Bearer token                               |
| **Anthropic**     | Anthropic      | `https://api.anthropic.com`                        | API key in the `x-api-key` header          |
| **Mistral AI**    | OpenAI         | `https://api.mistral.ai/v1`                        | Bearer token                               |
| **Google Gemini** | Gemini         | `https://generativelanguage.googleapis.com/v1beta` | API key in the `x-goog-api-key` header     |
| **DeepSeek**      | OpenAI         | `https://api.deepseek.com`                         | Bearer token                               |
| **Groq**          | OpenAI         | `https://api.groq.com/openai/v1`                   | Bearer token                               |
| **xAI**           | OpenAI         | `https://api.x.ai/v1`                              | Bearer token                               |
| **Together AI**   | OpenAI         | `https://api.together.xyz/v1`                      | Bearer token                               |
| **Fireworks AI**  | OpenAI         | `https://api.fireworks.ai/inference/v1`            | Bearer token                               |

**Azure AI Foundry** appears in the same list as a separate source type. It takes Azure credentials, and its models come from your Azure account rather than from the registry.

For what each request format supports once traffic flows through a proxy, see [LLM Proxy provider support](../build/llm-proxy-provider-support.md).

## Connect a model provider

Connecting a model provider takes three steps: choose the provider, select its models, and review the import.

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **AI Models**.
3. Click **Add provider**.
4. On the **Choose source type** step, select the provider you want to connect.
5. Click **Next**. Gamma records the connection and loads the models the registry lists for that provider.
6. On the **Select models** step, select the models to activate in the catalog. Click **Select all** to select every model that isn't already imported, and **Clear all** to reset the selection. A model already in the catalog carries an **Already imported** badge and can't be selected again.
7. Click **Next**.
8. On the **Review** step, confirm the connection and the inventory result, which reports the number of available models, the number that become active in AI Models, and the capabilities the selection covers.
9. Click **Import**. The button carries the number of models you selected.

The imported models appear in the AI Models catalog and become available to LLM Proxy configurations.

Connecting the same provider again reuses the existing connection instead of creating a second one. Return to this flow whenever you want to import more of that provider's models.

## Connect Azure AI Foundry

Azure AI Foundry adds a connection step to the flow, because Gamma queries your Azure account for its deployments.

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **AI Models**.
3. Click **Add provider**.
4. On the **Choose source type** step, select **Azure AI Foundry**.
5. Click **Next**.
6. On the **Configure connection** step, generate a bearer token with the Azure CLI. The step shows the command to copy:

    ```sh
    az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv
    ```

7. Enter the **Subscription ID**, **Resource Group**, **Account Name**, and **Bearer Token**. All four are required.
8. Click **Next**. Gamma records the connection and lists the deployments in that account.
9. On the **Select models** step, select the deployments to activate in the catalog.
10. Click **Next**.
11. On the **Review** step, confirm the connection, which reports the provider, account, and resource group, and the inventory result.
12. Click **Import**. The button carries the number of deployments you selected.

Three details are specific to Azure AI Foundry:

* **The bearer token isn't stored.** It travels with the requests that list and import deployments, so doing either again means entering a fresh token. If Gamma can't list the deployments, the **Select models** step reports that it couldn't load the models and asks you to check the Azure credentials and token.
* **The deployment name becomes the model's query name.** That's the identifier a proxy sends upstream, so it's the deployment name rather than the underlying model name.
* **No pricing is imported.** Azure deployments arrive without input and output rates, so those models carry no rates for cost attribution.

## Keep imported models in sync

Imported models hold a copy of the registry data they were created from. Re-syncing refreshes that copy.

1. In the **Catalog** section of the sidebar, select **AI Models**.
2. Click **Re-sync from provider**.

A re-sync refreshes the provider, family, context window, capabilities, and pricing of every model imported from a registry provider, and keeps the display name and description you edited. Models the registry no longer lists are left untouched and reported. Only registry providers are re-synced, so Azure AI Foundry connections and every other source are left alone.

The result is reported as a notification: how many models were updated, or that models are already up to date. Separate warnings report models the provider no longer offers, providers that are no longer available, and providers that couldn't be re-synced.

Gamma re-fetches the provider registry before it re-syncs. If that fetch fails or returns nothing, the re-sync stops with `Could not fetch the latest provider registry` rather than syncing against data it couldn't confirm.

{% hint style="info" %}
**Re-sync from provider** appears only when a remote provider registry is configured. Without one, Gamma uses the copy bundled with the module and there's nothing to poll.
{% endhint %}

## Configure the provider registry source

An operator can point Gamma at a hosted provider registry so the provider and model list refreshes without a module upgrade. Set these keys in the Management API `gravitee.yml`, alongside the rest of the Gamma configuration.

```yaml
modules:
  aim:
    catalog:
      llm-providers:
        remote:
          enabled: true
          url: https://download.gravitee.io/graviteeio-ee/gamma/aim/data/v1/llm-providers.json
      auto-resync:
        enabled: true
        delay: 60
        unit: MINUTES
```

| Key                                                | Default                                                                       | Description                                                                                                     |
| -------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `modules.aim.catalog.llm-providers.remote.enabled` | `false`                                                                       | Fetches the provider registry from a URL instead of the copy bundled with the module.                            |
| `modules.aim.catalog.llm-providers.remote.url`     | `https://download.gravitee.io/graviteeio-ee/gamma/aim/data/v1/llm-providers.json` | Where the registry is fetched from. A URL that isn't HTTPS is rejected.                                          |
| `modules.aim.catalog.auto-resync.enabled`          | `true`                                                                        | Re-syncs imported models against the loaded registry when the node starts.                                       |
| `modules.aim.catalog.auto-resync.delay`            | `0`                                                                           | How long to wait between periodic registry refreshes. `0`, blank, or a non-numeric value turns the refresh off.  |
| `modules.aim.catalog.auto-resync.unit`             | `MINUTES`                                                                     | The time unit that `delay` is expressed in.                                                                      |

Two behaviors protect imported models from a registry Gamma can't reach:

* If the configured registry is unreachable when the node starts, Gamma falls back to the bundled copy to serve the provider list, and skips the startup re-sync so imported models aren't rewritten from data that may be older.
* The periodic refresh stays off unless `delay` is positive and a remote registry is configured.

These keys are available from Gravitee 4.12.12. On 4.12.0 through 4.12.11 the provider registry is always the copy bundled with the module, and **Re-sync from provider** is shown without that condition and re-syncs against the bundled copy.

## Verification

To verify an integration is connected as expected, follow these steps:

1. In the **Catalog** section of the sidebar, select **AI Models**.
2. Confirm the models you imported are listed, each showing the provider you connected in the **Provider** column.
3. Click **Add provider**.
4. On the **Choose source type** step, select the same provider again.
5. Click **Next**, and confirm the models you already imported carry an **Already imported** badge.

## Next steps

* **Review what a model records.** See the metadata each imported model carries, and what you can edit. See [Add an AI model](add-an-ai-model.md).
* **Register an agent.** Add an external agent to the Catalog from its A2A agent card. See [Register an agent](import-an-agent.md).
