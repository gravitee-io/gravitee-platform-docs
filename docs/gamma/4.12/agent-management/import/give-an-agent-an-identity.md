---
hidden: true
noIndex: true
description: The Identity page of an agent creates the gateway application that acts for it and gives that application an OAuth identity from Gravitee Access Management. Follow the steps to set both up.
---

# Give an agent an identity

An agent reaches models and tools through subscriptions, and subscriptions belong to an application at the AI Gateway. The agent's **Identity** page creates that application, named after the agent, and can give it an OAuth identity issued by Gravitee Access Management, so the agent authenticates as a client of its own wherever it presents itself.

The two are separate steps. The gateway application is enough for API Key plans. A JWT or OAuth2 plan needs a client ID on the application, which you either type or let an OAuth identity supply.

## Open the Identity page

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Agent** section of the agent's sidebar, click **Identity**.

## Create the gateway application

Until the agent has an application, the page shows a **Gateway application** card that explains the application is named after the agent and that the name can't be edited.

1. Optional: Enter a **Client ID**. The hint explains that OAuth2 and JWT plan subscriptions need one, and that you can set it later or let an OAuth identity supply it.
2. Click **Create application**.

A **Created application** notification appears with the application's name. The card then shows the application's **Name**, its **Application ID** with a copy button, its **Client ID**, and a **Platform** row with an **Open the application** link that opens the application in Platform Management in a new tab. The card describes the application's role in one sentence: its subscriptions are what the agent can reach through it.

Until an OAuth identity is attached, the **Client ID** row reads **None yet — set one, or create an OAuth identity below** and carries an **Edit** button. Once an identity is attached, the row reads **Supplied by the OAuth identity** and can't be edited here.

<!-- TODO: Screenshot of the Identity page of an agent with the Gateway application card filled in and the OAuth identity card below it -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-aim-agent-identity.png" alt=""><figcaption><p>The Identity page of an agent</p></figcaption></figure>

## Create an OAuth identity

The **OAuth identity** card gives the application a real identity: the identity's client ID becomes the application's. The identity is created in Gravitee Access Management, so the environment's Access Management connection has to be set up first. Without it, the card reads **Identity service not connected** and links to the Access Management settings of Platform Management.

1. In the **OAuth identity** card, click **Create an OAuth identity**. When the application already carries a client ID you typed, the card warns that attaching an identity replaces it with the identity's.
2. In the **Persona** step, pick how the agent authenticates: **Desktop Productivity Agent**, a public client with PKCE enforced and no secret, **Hosted Agent**, a confidential client that acts for a signed-in user or on its own, or **Workload Agent**, a confidential client. The persona can't be changed after creation.
3. In the **Basics** step, review the **Name**, which is the agent's name and isn't editable here, and optionally enter a **Display name** for the catalog.
4. In the **Flow settings** step, enter the OAuth inputs the persona asks for. Enter the redirect URIs and the identity provider with care: once the identity is created, the attached identity's panel edits its name, display name, description, and credentials, and nothing else.
5. In the **Review** step, click **Create identity**.

An **Identity created** notification reports the client ID the application now presents. For a confidential persona, a **Save the client secret now** dialog shows the secret once. Store it before closing the dialog, because it can't be read again and the identity would have to be recreated to get a new one.

## Manage an attached identity

Once an identity is attached, the **OAuth identity** card shows what the identity is and how it authenticates, with **Edit** and **Delete identity** in the card's header. **Edit** opens the **Name**, **Display name**, and **Description** fields and the credentials in place, with **Save changes** and **Cancel**, and confirms with an **Identity updated** notification. The persona, the redirect URIs, and the identity provider are fixed when the identity is created. Switching the credential mode asks you to confirm, because whatever authenticates with the previous credentials stops working when you save.

**Delete identity** opens the **Delete this identity?** dialog. The application stays and can be given a new identity. Whatever authenticates with the deleted client ID can no longer do so, and the deletion can't be undone. Click **Delete identity** to confirm. An **Identity deleted** notification appears. When the identity could be detached from the application but not removed from Access Management, the notification says so and asks you to remove it there.

## Next steps

* [Manage subscriptions](../publish/manage-subscriptions.md). Approve and manage the subscriptions the application holds on your proxies.
* [Manage a registered agent](manage-a-registered-agent.md). Find the **Identity** item and the rest of the agent's page.
* [Create an agent identity](../build/create-an-agent-identity.md). Create an identity from the **Agent Identity** catalog instead of from an agent's page.
