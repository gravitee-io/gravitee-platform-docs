---
hidden: false
noIndex: false
---

# Create an agent identity


An agent identity is an OAuth client, registered in Gravitee Access Management (AM) through the Agent Management module, that gives an agent a verifiable identity. Once an agent has an identity, the AI Gateway and your authorization policies can authenticate who (or what) is making a request, attribute usage to it, and trace its actions in audit logs.

You register an agent through a short wizard. The wizard creates the underlying OAuth client in AM and returns its credentials.

{% hint style="info" %}
The Agent Management module must be connected to an AM instance before you can register agents, and the options available in the wizard (such as CIMD and SPIFFE) depend on what is enabled on the AM domain. See [Configure your Access Management instance](configure-your-access-management-instance.md).
{% endhint %}

## Agent personas

Every agent is registered as one of three personas. The persona determines the underlying OAuth client type and the grant flows the agent is allowed to use. **The persona is immutable after creation** — you can't change it later.

| Persona              | OAuth client                                                        | Use it for                                                  |
| -------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------- |
| **User-embedded**    | Native, public client — PKCE enforced, no client secret             | An agent that runs on the user's device.                    |
| **Hosted delegated** | Web, confidential client                                            | An agent that runs on your server, acting per user session. |
| **Autonomous**       | Service client — `client_credentials` or token exchange, no browser | An unattended service worker with no interactive user.      |

What each persona needs in the wizard:

| Persona              | Redirect URIs | Identity provider | Credentials                       |
| -------------------- | ------------- | ----------------- | --------------------------------- |
| **User-embedded**    | Required      | Required          | — (public client)                 |
| **Hosted delegated** | Required      | Required          | Optional JWKS (`private_key_jwt`) |
| **Autonomous**       | —             | —                 | JWKS **or** SPIFFE (required)     |

## The registration wizard

Registering an agent is a three-step wizard:

1. **Persona** — choose how the agent authenticates.
2. **Basics** — name the agent and choose its client identifier.
3. **Flow settings** — provide the OAuth inputs for the chosen persona.

To open it:

1. From the Gamma console, open the **Agent Management** module.
2. In the sidebar, select **Agent Identity**.
3. Select **New agent**.

## Step 1: Pick a persona

Select the persona card that matches how the agent runs — **User-embedded**, **Hosted delegated**, or **Autonomous** (see [Agent personas](#agent-personas)). Select **Next**.

## Step 2: Basics

Enter a **Name** (shown in the catalog and in audit events) and an optional **Description**.

Then choose the agent's **Client identifier**:

{% tabs %}
{% tab title="Client ID" %}
The agent is identified by a standard OAuth `client_id`.

Leave the field blank to let AM generate a client ID, or enter your own. A custom client ID must be unique within the domain.
{% endtab %}

{% tab title="CIMD" %}
The agent is identified by a **Client ID Metadata Document (CIMD)** — a metadata document published at an HTTPS URL that AM uses as the agent's `client_id` ([RFC 9728](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document)).

Enter the metadata document URL (for example, `https://client.example.com/.well-known/oauth-client`) and select **Validate**. AM fetches the document, validates it, and displays a **parsed metadata** preview. When the document includes them, AM auto-populates the agent's name, redirect URIs, `token_endpoint_auth_method`, and `jwks_uri` from the metadata.

If validation fails — for example, the document is missing `redirect_uris` — the error is shown inline, no preview appears, and you can't continue until it's fixed. Editing the URL after a successful validation clears the preview, so re-validate.

{% hint style="info" %}
The **CIMD** option is only selectable when CIMD is enabled on the AM domain. If it's greyed out, enable CIMD in AM first — see [Configure your Access Management instance](configure-your-access-management-instance.md).
{% endhint %}
{% endtab %}
{% endtabs %}

Select **Next**.

## Step 3: Flow settings

This step changes based on the persona you chose.

### User-embedded and Hosted delegated

These personas act on behalf of a user, so they need a redirect target and an identity provider:

* **Redirect URIs** — one per line, or whitespace-separated. (Hidden when you used CIMD, since the redirect URIs come from the metadata document.)
* **Identity provider** — the AM identity provider that users authenticate against. The list is populated from the identity providers configured on the AM domain. If there's exactly one, it's selected automatically.

{% hint style="info" %}
If no identity providers are listed, create one on the AM domain first.
{% endhint %}

For **Hosted delegated** you can also toggle **Enable JWKS** to switch client authentication to `private_key_jwt`. Provide a **jwks\_uri** (where AM fetches the public JWKS document) and/or paste an inline **jwks** JSON object. If you leave this disabled, the client will authenticate using a generated client secret.

### Autonomous

Autonomous agents have no browser and no interactive user, so instead of redirect URIs and an IdP you choose how the agent authenticates. **JWKS and SPIFFE are mutually exclusive.**

{% tabs %}
{% tab title="JWKS" %}
Authenticate with `private_key_jwt`. Provide at least one of:

* **jwks\_uri** — a URL where AM fetches the agent's public JWKS document.
* **jwks** — an inline JWKS JSON object (an object with a non-empty `keys` array). Use this when the agent can't publish a `jwks_uri`.
{% endtab %}

{% tab title="SPIFFE" %}
Authenticate with a SPIFFE JWT-SVID instead of a client secret.

* **Trust domain** — select a registered trust domain from the dropdown list. If you need a new one, select **Register new** and provide the trust-domain name (as it appears in SPIFFE IDs) and a **bundle endpoint URL** (or JWKS URL) that AM polls for the trust bundle used to verify JWT-SVIDs.
* **SPIFFE ID** — enter the subject identifier. It must start with `spiffe://<trust-domain>/` (for example, `spiffe://example.org/workload/my-agent`). Depending on the match mode configured in AM, the ID is validated using an exact match or a prefix match.

{% hint style="info" %}
The **SPIFFE** option is only available for Autonomous agents and requires SPIFFE to be enabled on the AM domain — see [Configure your Access Management instance](configure-your-access-management-instance.md).
{% endhint %}
{% endtab %}
{% endtabs %}

## Create the agent and save the client secret

Select **Create agent**.

For confidential clients, AM returns a **client secret**. The wizard shows a one-time panel with the agent's `client_id` and `client_secret`.

{% hint style="warning" %}
AM only returns the client secret once. Copy it and store it somewhere safe before you leave the page — it can't be retrieved later.
{% endhint %}

Select **Continue to agent** to open the agent's detail page.

Agents registered with CIMD don't have a client secret to reveal, so the wizard takes you straight to the detail page.

## Next steps

* [Expose your agent with the A2A Proxy](expose-agent-with-a2a-proxy.md) — Make the agent's skills discoverable across trust boundaries.
* [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md) — Write authorization policies that reference this agent as a principal.
