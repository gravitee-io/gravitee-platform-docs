---
hidden: false
noIndex: false
---

# Register an agent

Agents in the Catalog represent autonomous systems that perform tasks. You can register an external agent by pointing Gamma to its endpoint and importing its Agent Card. This registers the agent in the Catalog and makes it available for identity assignment, authorization policies, and A2A proxy exposure.

## Register an A2A agent

You can register any agent that exposes its capabilities via an A2A-compliant Agent Card (`/.well-known/agent-card.json`).

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Agents** list.
3. Select **Add Agent**.
4. Enter the **Endpoint URL** for the agent (e.g., `https://agents.example.com/a2a/flight-status`).
5. Select **Fetch card** to automatically retrieve the agent's capabilities, skills, and metadata.
   - *Note: If the agent endpoint requires authentication to fetch the card, you can supply transient credentials under the **Authentication** section (Header or OAuth client credentials). These credentials are only used to fetch the card and are never stored on the agent in the catalog.*
6. Review the pre-filled fields:
   - **Name**: The display name for the agent.
   - **Description**: What this agent does and when to use it.
   - **Version**: The current version of the agent.
7. Select **Register agent**.

## Agent catalog fields

Each agent in the Catalog records:

| Field               | Description                                              |
| ------------------- | -------------------------------------------------------- |
| **Endpoint URL**    | The upstream URL where the agent can be reached.         |
| **Name**            | The display name of the agent.                           |
| **Description**     | What this agent does and when to use it.                 |
| **Version**         | The semantic version of the agent.                       |
| **Capabilities**    | Supported features, such as streaming.                   |
| **Declared skills** | The set of tasks this agent can perform.                 |

## After registration

Once an agent is registered in the Catalog, you can:

* **Assign an identity** — Register the agent as an OAuth client with a persona (User-embedded, Hosted delegated, or Autonomous) and optional CIMD or SPIFFE credentials. See [Create an agent identity](../build/create-an-agent-identity.md).
* **Apply authorization policies** — Control which resources and tools this agent can access.
* **Expose via the A2A Proxy** — Make this agent's skills discoverable and callable by other agents. See [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md).

## Next steps

* [Create an agent identity](../build/create-an-agent-identity.md) — Assign a verifiable identity to a registered agent.
* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md) — Make agent skills available across trust boundaries.

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/agents/NewAgentPage.tsx -->
