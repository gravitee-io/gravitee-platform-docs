---
hidden: false
noIndex: false
description: Register an external agent in the Catalog by fetching its A2A agent card from an endpoint. Follow the steps to fetch the card and review the fields.
---

# Register an agent

Agents in the Catalog represent autonomous systems that perform tasks. You register an external agent by pointing Gamma at its endpoint and fetching its agent card. Once it's in the Catalog, the agent can be given an identity and exposed through an A2A Proxy.

## Register an A2A agent

You can register any agent that publishes an A2A agent card. Gamma fetches the card server-side and fills the form in from it. You can also fill the form in by hand.

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Agents**.
3. Click **Register agent**.
4. Enter the **Endpoint URL** of the agent, for example, `https://agents.example.com/a2a/flight-status`.
5. If the endpoint needs credentials to serve its card, select an **Authentication** mode and complete its fields:
    * **None**. No credentials are sent.
    * **Header**. Gamma sends the **Header name** and **Header value** you enter.
    * **OAuth client credentials**. Gamma requests a token using the **Client ID**, **Client secret**, and **Token URL** you enter, with an optional **Scope**.
6. Click **Fetch card**. Gamma retrieves the agent's capabilities, skills, and metadata, and confirms with an **Agent card imported** banner that reports the number of skills and whether the agent streams.
7. Review the **Name**, **Description**, and **Version** that the card filled in.
8. Click **Register agent**. **Name**, **Endpoint URL**, and **Version** are all required.

Four behaviors are worth knowing before you fetch a card:

* **Credentials are never stored.** They travel with the fetch request and aren't saved on the agent. They're also dropped if the endpoint redirects to a different origin, so they never reach a redirect target.
* **Gamma resolves the card URL for you.** A URL ending in `.json` is fetched as-is. Any other URL is treated as a base, and Gamma tries `/.well-known/agent-card.json` first, then falls back to `/.well-known/agent.json`.
* **Gamma fetches only from a public HTTP or HTTPS host.** An endpoint that resolves to a private or loopback address is rejected, so a locally hosted agent isn't reachable from a default deployment.
* **Editing the endpoint clears a fetched card.** That prevents one agent's capabilities and skills from being registered under another agent's endpoint, so fetch again after you change the URL.

If the endpoint answers with `401` or `403`, the form reports **Authentication required** and asks you to add a header or OAuth credentials and fetch again.

## Agent catalog fields

Each agent in the Catalog records:

| Field            | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| **URL**          | The upstream endpoint where the agent can be reached.              |
| **Name**         | The name shown for the agent across the console.                    |
| **Description**  | What this agent does and when to use it.                            |
| **Version**      | The version the agent card declares.                                |
| **Capabilities** | The optional A2A features the agent declares, such as streaming and push notifications. |
| **Skills**       | The set of tasks the agent declares it can perform.                 |

The agent's detail page also shows the provider organization from the agent card, when the card declares one.

## After registration

Once an agent is registered in the Catalog, you can:

* **Assign an identity**. Give the registered agent a verifiable identity. See [Create an agent identity](../build/create-an-agent-identity.md).
* **Expose it through the A2A Proxy**. Make the agent's skills discoverable and callable by other agents. See [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).

## Next steps

* [Create an agent identity](../build/create-an-agent-identity.md). Assign a verifiable identity to a registered agent.
* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). Make agent skills available across trust boundaries.
