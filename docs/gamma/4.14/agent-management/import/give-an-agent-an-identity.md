---
description: Give an agent an identity with Gravitee Access Management or another provider. Follow the steps to create, link, or associate an OAuth client.
---

# Give an agent an identity

An agent's identity is the OAuth client it presents to prove who it is. The **Identity** page uses that identity for delegated access, authorization policies, and observability. The page description reads **Manage this Agent's Identity that is used for the Agent to prove who it is, delegated access, authorization policies, and observability. An Agent may also have other credentials tied to it, such as API Keys, although it is not recommended.**

You can give an agent an identity in three ways. Create an OAuth client in Gravitee Access Management, use a client that already exists in Access Management, or associate a client from another Identity Provider, such as Microsoft Entra or Okta. A gateway application acts for the agent at the AI Gateway, and the subscriptions to proxies belong to it.

## Open the Identity page

1. In the Gamma console, open **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click the agent's name.
4. In the **Agent** group of the agent's sidebar, click **Identity**.

What the page offers follows your role in the environment, and a button you lack the permission for is hidden. To create an identity in Access Management, you need the permissions to create and read agent identities, to update Catalog items, and to read the Access Management configuration. To use an existing client, you need the permissions to read agent identities and to update Catalog items. To associate a client, you need the permission to update Catalog items. To use **Delete**, you need the permission to delete Catalog items. **Edit** also needs the permission to update agent identities.

When the identity cannot be read, the page shows **Could not load the identity of this agent** and **Retry**.

An agent without an identity shows two cards. **Gravitee Agent Identity (Access Management)** carries a **Recommended** badge, and **External Identity Provider** offers a client from another provider. A user who cannot update the Catalog reads **This agent has no identity yet.** on the external card.

## When the import found a Microsoft Entra identity

When the import of the agent found a Microsoft Entra identity, an alert reads **The import found a Microsoft Entra identity for this agent.** It says **Use it as the agent's identity, or choose another option below. The agent keeps the client it already runs with; nothing changes in Entra.**

The alert lists **OAuth client ID**, **Agent blueprint ID** when the import has one, **Issuer URL**, and **Agent Identity Provider**. The provider reads **None registered for this issuer yet** when none is registered.

**Use this identity** opens the association on that client. **Add the provider and use this identity** adds the provider first, offered as **Microsoft Entra**, and then opens the same association. A user who cannot add a provider reads that using it takes an Identity Provider for this issuer, and that an administrator adds one in **Agent Identity Providers**.

## Create an identity in Access Management

The identity is created in Gravitee Access Management, so you configure the environment's Access Management connection first. Without it, the card reads **Access Management is not connected yet. Once it is, an identity can be created for this agent here.** and offers **Connect Access Management**.

When Access Management is connected and you cannot create or link a client, the card reads **Creating an identity in Access Management takes the permissions to create and read agent identities and to read the Access Management configuration.**

1. In the **Gravitee Agent Identity (Access Management)** card, click **Create in Access Management**.
2. In the **Persona** step, pick how the agent authenticates, and then continue.
3. In the **Basics** step, choose the **Client identifier**, and then continue.
4. In the **Flow settings** step, enter what the persona asks for, and then continue.
5. In the **Review** step, check the settings, and then click **Create identity**.

The page title is **Create an identity for &lt;agent&gt;**. The client takes the agent's name, and the gateway application is created with it. An **Identity created** page reports the client ID. Click **Back to Identity** to return to the agent. **Identity** in the header leaves the wizard.

### Pick a persona

The persona sets the OAuth client type and how the agent authenticates:

<table>
    <thead>
        <tr>
            <th width="240">Persona</th>
            <th width="140">Client type</th>
            <th>How it authenticates</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Desktop Productivity Agent</strong></td>
            <td>Public</td>
            <td>Public client, PKCE enforced, no secret. Like Claude Desktop.</td>
        </tr>
        <tr>
            <td><strong>Hosted Agent</strong></td>
            <td>Confidential</td>
            <td>Confidential client that acts for a signed-in user, or on its own. Like a backend running on a server.</td>
        </tr>
        <tr>
            <td><strong>Workload Agent</strong></td>
            <td>Confidential</td>
            <td>No browser and no secret. It authenticates with a JWKS key or SPIFFE. Like LangChain, n8n, or CrewAI.</td>
        </tr>
    </tbody>
</table>

To get a recommendation, click **Help me choose**, and answer two questions. The first is **Is a real person signed in when the agent acts?** Its answers are **Yes — agent acts on behalf of a signed-in user** and **No — agent runs unattended (cron, queue, daemon)**. The second is **Where does the agent code run?** Its answers are **On the user's own device (mobile app, browser, desktop)** and **On infrastructure I control (backend, container, function)**. Then click **Use this persona**. Once you move past the **Persona** step, **Change** in the persona summary bar returns you to it.

### Set the client identifier

The client in Access Management is named after the agent. Under **Client identifier**, choose one of two modes:

* **Client ID.** Enter a client ID, or leave the field blank so Access Management generates one. The client ID is optional and must be unique within the domain.
* **CIMD.** Enter the URL of the metadata document, and then click **Validate**. **CIMD** is unavailable when it isn't enabled on the Access Management domain. When its support can't be checked, the tooltip tells you to check your connection and reload the page.

### Enter the flow settings

The **Flow settings** step asks for the following inputs, which depend on the persona:

<table>
    <thead>
        <tr>
            <th width="240">Persona</th>
            <th>Inputs</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Desktop Productivity Agent</strong></td>
            <td><strong>Redirect URIs</strong>, one per line or separated by whitespace, and the <strong>Identity provider</strong> that users authenticate against.</td>
        </tr>
        <tr>
            <td><strong>Hosted Agent</strong></td>
            <td>The same two inputs, and an <strong>Enable JWKS</strong> switch that switches client authentication to <code>private_key_jwt</code>. With the switch on, enter a <code>jwks_uri</code>, an inline <code>jwks</code>, or both.</td>
        </tr>
        <tr>
            <td><strong>Workload Agent</strong></td>
            <td>Credentials, either <strong>JWKS</strong> or <strong>SPIFFE</strong>. For JWKS, enter a <code>jwks_uri</code>, an inline <code>jwks</code>, or both. For SPIFFE, select a <strong>Trust domain</strong>, choose a <strong>Subject match</strong> of exact or prefix, and enter the <strong>SPIFFE ID</strong>.</td>
        </tr>
    </tbody>
</table>

To add a trust domain, click **Register new**, enter a **Trust domain name** and a **Bundle endpoint URL**, and click **Register trust domain**. With CIMD, a Desktop Productivity Agent or a Hosted Agent takes its redirect URIs from the metadata document. An alert reads **No redirect URIs from the metadata document** when it declares none. The **Review** step reads **JWKS or SPIFFE (set after creation)** for a Workload Agent with neither.

### Store the client secret

For a persona that has a client secret, the **Identity created** page shows a **Save the client secret now** alert. Access Management returns the secret only once, so store it somewhere safe before you leave the page. **Reveal** and **Copy** show and copy it.

## Use an existing Access Management client

1. In the **Gravitee Agent Identity (Access Management)** card, click **Use an existing client**.
2. In the **Use an existing client** panel, under **Access Management client**, choose a client. The hint reads **Only clients that are not the identity of an agent yet are listed.**
3. Click **Use this client**.

The panel says the client is not changed, and it stays in Access Management if the identity is deleted later. An **Agent identity created** notification appears. When Access Management has no free client, the panel reads **Access Management has no agent client that is free: each one already is the identity of an agent, or none exists yet.** When the clients cannot be read, it reads **Could not load the clients of Access Management** and offers **Retry**.

## Associate a client from another provider

1. In the **External Identity Provider** card, click **Associate OAuth client**.
2. In the **Associate OAuth client** panel, under **Identity Provider**, choose the provider. The description reads **Choose the Identity Provider and enter the OAuth client ID that already exists there.**
3. Under **OAuth client ID**, enter the client ID that already exists at that provider.
4. Click **Associate**.

An **Agent identity created** notification appears. When another application of the environment already uses that client ID, the field reads **Another application of this environment already uses this client id. A client id can be the identity of one agent only.** **Add Identity Provider** in the panel adds a provider and selects it. When no Identity Provider is registered, the card offers **Add Identity Provider** if you can add one. Otherwise, it tells you that an administrator adds one in **Agent Identity Providers**.

## Read, edit, and delete the identity

Once the agent has an identity, an **Agent Identity** card shows:

<table>
    <thead>
        <tr>
            <th width="220">Field</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>OAuth client ID</strong></td>
            <td>The client ID, which you can copy. A dash when there is none.</td>
        </tr>
        <tr>
            <td><strong>Identity type</strong></td>
            <td><strong>OAuth Client</strong>.</td>
        </tr>
        <tr>
            <td><strong>Agent Identity Provider</strong></td>
            <td><strong>Gravitee Access Management</strong> when the client lives there, otherwise the provider's name.</td>
        </tr>
        <tr>
            <td><strong>Gateway application</strong></td>
            <td><strong>Open Application</strong>, which opens the application in Platform Management. <strong>No gateway application</strong> when there is none.</td>
        </tr>
    </tbody>
</table>

When Access Management holds the client, **Open in Access Management** opens it. **Edit** appears when that client can be reached. It opens **Edit the identity of &lt;agent&gt;**, described as **The settings of this agent's client in Gravitee Access Management.** **Identity** returns to the agent. When an identity has a gateway application but no recorded Identity Provider, the card reads **This identity is incomplete.** Delete the identity, then associate the OAuth client again.

To delete the identity, complete the following steps:

1. In the **Agent Identity** card, click **Delete**.
2. In the **Delete Agent Identity?** dialog, read what it removes, and then type the client ID, or the agent's name when there is no client ID, to confirm.
3. Click **Delete**.

The dialog says this removes the OAuth identity from the agent, and that all its subscriptions to proxies on the gateway are deleted too. When Access Management created the client, its OAuth client there is deleted as well. When you linked an existing client, that client stays. This cannot be undone. An **Agent identity deleted** notification appears. When the identity cannot be deleted, the dialog reads **The identity was not deleted** with the reason.

## Read the other credentials

The **Other Credentials** card lists the API keys and other consumption credentials issued through proxy plan subscriptions for this agent. It includes subscriptions where the OAuth Agent Identity is used. Nothing in the table can be changed from this page.

The table shows **Type**, **Plan**, **Proxy**, **Created at**, **Processed at**, **Started at**, and **Status**. The proxy name links to that proxy's **Overview** for a user who can read APIs.

When the agent holds nothing, the card reads **No other credentials yet** and **When this agent's application subscribes to a proxy plan, what the plan gives it appears here.** When the credentials cannot be read, it reads **Could not load the credentials of this agent** and offers **Retry**.

## Next steps

* [Manage subscriptions](../publish/manage-subscriptions.md). Approve and manage the subscriptions the application holds on your proxies.
* [Manage a registered agent](manage-a-registered-agent.md). Find the **Identity** item and the rest of the agent's page.
* **Agent Identity Providers**, in the **Catalog** group. Register the provider an external OAuth client belongs to.
