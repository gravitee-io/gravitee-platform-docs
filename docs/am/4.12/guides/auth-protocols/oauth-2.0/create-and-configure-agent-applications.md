# Create and Configure Agent Applications

## Creating Agent Applications

Navigate to **Agents** in the domain sidebar and click **Add Agent**. Choose between **Manual** or **CIMD** configuration mode.

### Manual Configuration

1. Enter an **Application Name** and optional **Description**.
2. Select an **Agent Sub-Type** from the dropdown: **User-Embedded**, **Hosted Delegated**, or **Autonomous**.
3. Configure **Redirect URIs** (required for User-Embedded and Hosted Delegated agents).
4. Select **Grant Types** appropriate to the agent persona.
5. Choose a **Token Endpoint Auth Method**:
   - **SPIFFE JWT**: Authenticate using SPIFFE JWT-SVIDs.
   - **Agent JWT-Bearer**: Authenticate using a blueprint-signed JWT assertion.
   - **Private Key JWT**: Authenticate using a client-signed JWT with JWKS.
6. If using SPIFFE JWT, configure workload identity settings:
   - Select a **Trust Domain** from the dropdown.
   - Enter a **SPIFFE Subject** (e.g., `spiffe://prod.example/agent/billing`).
   - Select a **Subject Match Mode**: **Exact** or **Prefix**.
7. Save the application.

| Field | Description |
|:------|:------------|
| **Application Name** | Display name for the agent application |
| **Description** | Optional description of the agent's purpose |
| **Agent Sub-Type** | Agent persona: User-Embedded, Hosted Delegated, or Autonomous |
| **Redirect URIs** | OAuth callback URLs (required for user-bound agents) |
| **Grant Types** | OAuth grant types allowed for this agent |
| **Token Endpoint Auth Method** | How the agent authenticates to the token endpoint |
| **Trust Domain** | SPIFFE trust domain for SVID verification |
| **SPIFFE Subject** | Expected SPIFFE ID in the SVID `sub` claim |
| **Subject Match Mode** | Exact (full match) or Prefix (path prefix match) |

### CIMD Configuration

1. Toggle to **CIMD** mode.
2. Enter the **Document URL** (e.g., `https://agents.example.com/.well-known/client-metadata`).
3. Click **Validate**. Access Management fetches and parses the document.
4. Review the parsed metadata in the confirmation step. If the document lacks a `client_name`, enter an **Application Name**.
5. Click **Create** to save the application. The CIMD URL becomes the `client_id`.

| Field | Description |
|:------|:------------|
| **Document URL** | HTTPS URL hosting the client metadata document |
| **Application Name** | Display name (auto-filled from `client_name` if present) |
