---
hidden: false
noIndex: false
description: Refresh imported AI models and MCP servers against the source they came from, and read what changed. Follow the steps to re-sync a catalog asset.
---

# Re-sync catalog assets

A catalog asset is a copy of what its source offered at the moment you imported it. Providers add models, change context windows, adjust prices, and drop models entirely, and an MCP server changes the tools it exposes. Re-syncing refreshes the copy.

The two asset types re-sync differently, and they differ in what happens to an entry the source no longer offers. Read the section for the asset you're re-syncing.

## Re-sync your AI models

AI models are re-synced for a whole environment at once, against the provider registry.

### Before you start

The **Re-sync from provider** button appears only when the remote provider registry is configured. It needs both of the following properties:

```yaml
modules:
  aim:
    catalog:
      llm-providers:
        remote:
          enabled: true
          url: <provider registry URL>
```

`enabled` defaults to `false`, so the button is hidden until you turn it on. `url` already defaults to a Gravitee-hosted registry, and the button stays hidden if you override it with a blank value.

### Run the re-sync

To re-sync every registry-backed provider source in the environment, follow these steps:

1. Click **AI Models** in the module sidebar.
2. Click **Re-sync from provider**.

The button reads **Re-syncing…** while the request is in flight.

Re-sync refreshes the fields the registry owns: provider, family, context window, capabilities, and pricing. The name and description you edited are kept. Sources whose models are discovered live rather than read from the registry, such as Azure Foundry, are skipped.

<!-- TODO: Screenshot of the AI Models page showing the Re-sync from provider button -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-resync-models-button.png" alt=""><figcaption><p>The AI Models page</p></figcaption></figure>

### Read the result

Each outcome is reported separately, so one re-sync can raise several messages at once:

| Outcome | What it means |
| --- | --- |
| Models were updated | The registry data for those models changed, and the catalog copies were rewritten. |
| Models are already up to date | Every model matched the registry. This is reported only when nothing was updated **and** none of the warnings below were raised. |
| Models are no longer offered by the provider | The registry no longer carries those models. **They stay in the catalog, untouched.** |
| Providers are no longer available | The registry no longer carries those provider sources. |
| Providers couldn't be re-synced | Reading those sources raised an error and they were skipped. The rest of the sweep still ran. |

A model the registry has dropped is reported as a warning rather than removed, so the record of what you imported survives the provider retiring it.

If the registry itself can't be fetched, the re-sync fails with **Failed to re-sync models** and changes nothing. An unreachable or empty registry never empties the catalog.

### Re-sync automatically

Models are also re-synced without anyone clicking the button, so a catalog can move on its own.

Every node boot re-syncs the imported provider models of every environment. This is on by default:

```yaml
modules:
  aim:
    catalog:
      auto-resync:
        enabled: true
```

Set `enabled` to `false` to turn the boot sweep off. On a cluster, only the primary node runs it. The sweep is skipped when the configured remote registry was unreachable at boot, so a registry outage can't overwrite your imported models with older bundled data.

A periodic re-sync is available as well. It re-fetches the registry on a fixed delay and re-syncs when the registry changed:

```yaml
modules:
  aim:
    catalog:
      auto-resync:
        delay: 60
        unit: MINUTES
```

`delay` has no default, which leaves the periodic re-sync off. Set it to a positive number of `unit` to turn it on. `unit` defaults to `MINUTES`. The periodic re-sync also needs the remote registry configured, and it stays off while `delay` is absent, blank, zero, negative, or not a number.

## Re-sync an MCP server

MCP servers are re-synced one at a time. Re-sync re-probes the server over the endpoint, transport, and credentials stored when you imported it, and then **replaces the previous entries** with what the server exposes now. A tool the server has dropped doesn't survive the re-sync, which is the opposite of how AI models behave.

To re-sync a server, follow these steps:

1. Click **MCP Servers** in the module sidebar.
2. Locate the server in the list.
3. Open the actions menu, and then click **Re-sync**. The server's detail page carries the same **Re-sync** action.

The action reads **Re-syncing…** while the request is in flight. On success the console reports the server name and how many tools it found.

Re-sync fails and changes nothing in the following cases:

* No MCP server was imported for that source.
* The stored server has no endpoint or transport to re-sync from.
* The server authenticates with OAuth2 and the stored configuration is incomplete. The client ID, the client secret, and the token URL must all be present.

<!-- TODO: Screenshot of the MCP Servers list with the actions menu open, showing the Re-sync action -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-resync-mcp-server.png" alt=""><figcaption><p>The Re-sync action on an MCP server</p></figcaption></figure>
