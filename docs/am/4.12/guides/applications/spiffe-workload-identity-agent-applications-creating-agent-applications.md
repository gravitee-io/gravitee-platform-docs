# SPIFFE Workload Identity & Agent Applications: Creating Agent Applications

## Creating Agent Applications

Navigate to **Agents** in the domain sidebar and click **Add Agent**. The creation wizard offers two modes: Manual and CIMD.

### Manual Creation

1. Navigate to **Agents** and click **Add Agent**.
2. Select **Manual** on the creation mode step.
3. Enter an **Application Name** and optional **Description**.
4. Select an **Agent Sub-Type** from the dropdown: User Embedded, Hosted Delegated, or Autonomous.
5. Configure **Redirect URIs** (required for User Embedded and Hosted Delegated; not applicable to Autonomous).
6. Select **Grant Types** appropriate to the agent persona.
7. Choose a **Token Endpoint Auth Method**: Private Key JWT, TLS Client Auth, Self-Signed TLS Client Auth, SPIFFE JWT, or Agent JWT-Bearer.
8. If using SPIFFE JWT, configure **Workload Identity Settings**:
   1. Select a **Trust Domain** from the dropdown.
   2. Enter a **Subject** (SPIFFE URI, e.g., `spiffe://acme.com/billing-agent`).
   3. Select a **Subject Match Mode** (Exact or Prefix). If Prefix, ensure the subject ends with `/`.
9. If using Private Key JWT or Agent JWT-Bearer, provide a **JWKS** or **JWKS URI**.
10. Click **Create**.

**Reference Table:**

| Field | Description | Required |
|:------|:------------|:---------|
| Application Name | Human-readable agent identifier | Yes |
| Description | Optional agent description | No |
| Agent Sub-Type | Agent persona (User Embedded, Hosted Delegated, Autonomous) | Yes |
| Redirect URIs | OAuth redirect endpoints | Yes (User Embedded, Hosted Delegated) |
| Grant Types | Allowed OAuth grant types | Yes |
| Token Endpoint Auth Method | Client authentication method | Yes |
| Trust Domain | SPIFFE trust domain (SPIFFE JWT only) | Conditional |
| Subject | SPIFFE URI (SPIFFE JWT only) | Conditional |
| Subject Match Mode | Exact or Prefix (SPIFFE JWT only) | Conditional |
| JWKS / JWKS URI | Public keys for signature validation (Private Key JWT, Agent JWT-Bearer) | Conditional |
