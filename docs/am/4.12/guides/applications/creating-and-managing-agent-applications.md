# Creating and Managing Agent Applications

## Creating Agent Applications

<figure><img src="../../.gitbook/assets/am-agents-list.png" alt="AM agents list showing agent applications"><figcaption></figcaption></figure>

### Manual Creation

Navigate to **Agents** in the management console and select **Add Agent**:

1. Enter a **Name** for the agent application.

    <figure><img src="../../.gitbook/assets/am-agent-creation-step1.png" alt="Agent creation wizard - agent type selection"><figcaption></figcaption></figure>

2. Select an **Agent Type** from the dropdown: User-Embedded, Hosted Delegated, or Autonomous.
3. (Optional) Toggle **Use as DCR / CIMD registration template** to mark the application as a registration template.
4. Enter one or more **Redirect URIs** (required for User-Embedded and Hosted Delegated agents).
5. Select **Grant Types**: authorization code (User-Embedded, Hosted Delegated), client credentials (Hosted Delegated, Autonomous), or both (Hosted Delegated only).
6. Select a **Token Endpoint Auth Method**: `none` (User-Embedded default), `private_key_jwt` (Hosted Delegated and Autonomous default), or `spiffe_jwt`.
7. Configure **Workload Identity Settings** (when using `spiffe_jwt`):
    - Enter the **Trust Domain** name (e.g., `example.org`).
    - Enter the **Subject** SPIFFE ID (e.g., `spiffe://example.org/agent/billing`).
    - Select a **Subject Match Mode**: **Exact** or **Prefix** (Prefix requires trailing `/` and is only allowed for Hosted Delegated and Autonomous agents).

| Field | Description |
|:------|:------------|
| Name | Human-readable agent application name |
| Agent Type | Agent persona: User-Embedded, Hosted Delegated, or Autonomous |
| Use as DCR / CIMD registration template | Marks the application as a template for dynamic client registration |
| Redirect URIs | OAuth redirect endpoints (required for User-Embedded and Hosted Delegated) |
| Grant Types | Permitted OAuth grant types (constrained by agent type) |
| Token Endpoint Auth Method | Client authentication method (`none`, `private_key_jwt`, `spiffe_jwt`) |
| Trust Domain | SPIFFE trust domain name (required for `spiffe_jwt`) |
| Subject | SPIFFE ID or prefix (required for `spiffe_jwt`) |
| Subject Match Mode | Exact or Prefix matching for SPIFFE subjects |

### CIMD Creation

Navigate to **Agents** in the management console and select **Add Agent**. Toggle the creation mode to **CIMD**:

1. Enter the **Document URL** (the CIMD metadata endpoint).
2. Select **Validate** to fetch and preview the metadata.
3. Review the parsed metadata in the confirmation step. If the document lacks a `client_name`, enter a **Name** for the application.
4. Select **Create** to finalize the application.

The CIMD URL becomes the application's `client_id`. All metadata (redirect URIs, grants, scopes, JWKS, mTLS settings, CIBA settings, software metadata) is pre-populated from the document.
