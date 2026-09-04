---
hidden: false
noIndex: false
description: Open a registered agent's page in the Catalog, read what its agent card declared, edit its name and description, remove it, and find where its gateway controls live.
---

# Manage a registered agent

When you register an agent, the Gamma console opens the agent's page in the Catalog. That page is the record of what the agent declared in its agent card. Come back to it to check the endpoint, version, capabilities, and skills that Gamma holds for the agent, to rename or describe it, or to remove it.

The page is a Catalog record, not a control panel for the running agent. Stopping traffic, deployment, logs, and consumer access belong to the A2A Proxy that exposes the agent through the AI Gateway. The [Where the gateway controls live](#where-the-gateway-controls-live) section maps each of those concerns to its page.

## Open an agent's page

Right after you click **Register agent** on the registration form, the console opens the new agent's page for you. To return to it later, follow these steps:

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name. Optional: To find it in a long list, type part of its name or description in the search box above the list.

The **Agents** list shows each agent's name and description, its **Entity ID**, its **Version**, and its **URL**. The actions menu at the end of each row offers **View details**, **Edit**, and **Remove**.

<!-- TODO: Screenshot of a registered agent's page in the Catalog, showing the header, the Overview card, and the Details card -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-agent-detail.png" alt=""><figcaption><p>The page of a registered agent in the Catalog</p></figcaption></figure>

## What the page shows

The header carries the agent's name and description, a badge with its version, and, when the agent card names one, a badge with the provider organization. Below the header, the **Overview** card lists what the agent declared and the **Details** card lists what the Catalog recorded.

| Card         | Row                     | What it holds                                                                                                                                                                                            |
| ------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overview** | **URL**                 | The endpoint the agent was registered with.                                                                                                                                                              |
| **Overview** | **Version**             | The version from the agent card, or the one you typed when you registered the agent by hand.                                                                                                             |
| **Overview** | **Capabilities**        | A **Streaming** badge, a **Push notifications** badge, or both, when the agent card declares them. The row is blank when the card declares neither, and for an agent registered by hand.                 |
| **Overview** | **Skills**              | Every skill the agent card declares, each with its description. The row is omitted when the card declares no skills.                                                                                     |
| **Details**  | **ID**                  | The Catalog's identifier for this record, with a copy button.                                                                                                                                            |
| **Details**  | **Entity ID**           | The stable identifier that other Gamma modules use to reference the agent. It takes the form `agent.<slug>`, where the slug is derived from the agent's name at registration.                            |
| **Details**  | **Source**              | `manual` for an agent registered from the console.                                                                                                                                                       |
| **Details**  | **Created** and **Updated** | When the record was registered, and when it was last saved.                                                                                                                                          |

The record keeps any other field the agent card carries, such as its documentation URL and its default input and output modes. This page doesn't display them.

Two agents can't share a slug. Registering a second agent whose name reduces to the same slug as an existing one is refused with the message **An agent with this name already exists**.

## Edit the name and description

Only the name and the description are editable. The endpoint URL and the version are fixed when the agent is registered. To point the Catalog at a different endpoint, register the agent again.

1. On the agent's page, click **Edit**.
2. Change the **Name** or the **Description**.
3. Click **Save changes**.

**Save changes** stays disabled until you change something, and a blank name can't be saved. Saving keeps the capabilities and skills that were fetched from the agent card. Renaming the agent doesn't change its Entity ID.

## Remove an agent

1. On the agent's page, click **Remove**.
2. In the **Remove this agent?** dialog, click **Remove agent**.

Removal is immediate and can't be undone. The Catalog doesn't check whether anything references the agent before removing it. Removal also leaves every A2A Proxy untouched, because a proxy stores its own target URL and holds no link to the Catalog record. After removal, the console returns you to the **Agents** list.

## Where the gateway controls live

The agent's page holds no runtime state, no usage or cost figures, no compliance status, and no publication status. Those concerns live on other pages, and none of them link back to the agent's record, so open each one from its own sidebar entry.

| To do this                                                                                     | Go here                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Expose the agent through the AI Gateway so that other agents call it through a governed endpoint | Under **Secure**, create an A2A Proxy. The proxy doesn't read the Catalog, so you enter the agent's endpoint again as its **Target URL**. See [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).                                                                                       |
| Stop or restart the traffic that reaches the agent through the gateway                          | Open the A2A Proxy, click **General** in its sidebar, and use the **API Events** card of its **Settings** page.                                                                                                                                                                                                       |
| Choose which gateway instances load the proxy, and review or roll back its deployments          | In the A2A Proxy sidebar, under **Operations**, click **Deployment**. See [Configure A2A Proxy deployment](../build/configure-a2a-proxy-deployment.md) and [Review A2A Proxy deployment history](../build/review-a2a-proxy-deployment-history.md).                                                                     |
| Read the proxy's logs and traces                                                                | In the A2A Proxy sidebar, under **Observability**. To choose what the proxy reports, see [Configure logging and tracing](../build/configure-your-a2a-proxy/configure-logging-and-tracing.md).                                                                                                                       |
| Give client applications access to the proxy and approve their subscriptions                    | In the APIM console, on the API behind the A2A Proxy. The A2A Proxy sidebar carries no consumer pages in this release. See the **Give a client access** section of [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).                                                                   |
| Give the agent a verifiable identity                                                            | **Agent Identity**, also in the **Catalog** section of the sidebar. An agent identity is a separate record and isn't linked to the agent's page. See [Create an agent identity](../build/create-an-agent-identity.md).                                                                                                |
| See token usage and cost                                                                        | Cost is reported per LLM Proxy. See [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md).                                                                                                                                                                                                                   |

## Verification

To verify the agent's record is working as expected, follow these steps:

1. On the agent's page, click **Edit**.
2. Change the **Description**.
3. Click **Save changes**. An **Agent updated** notification appears, and the console returns to the agent's page with the new description under the agent's name.
4. In the **Catalog** section of the sidebar, select **Agents**. The list shows the new description under the agent's name, and the **Entity ID** column is unchanged.

<!-- TODO: Screenshot of the Agents list showing the updated description under the agent's name -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-agents-list-updated.png" alt=""><figcaption><p>The updated description in the Agents list</p></figcaption></figure>

## Next steps

* [Register an agent](import-an-agent.md). Add another agent to the Catalog from the agent card it publishes.
* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). Put the agent behind the AI Gateway.
* [Create an agent identity](../build/create-an-agent-identity.md). Give the agent a verifiable identity for authentication and audit.
