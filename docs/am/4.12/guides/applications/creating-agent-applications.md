# Creating Agent Applications

Navigate to **Agents** in the management console and click **Add Agent**. The wizard presents two creation modes: **Manual** (enter settings directly) or **CIMD** (bootstrap from a metadata document URL). CIMD mode is available only when CIMD is enabled on the domain.

<figure><img src="../../.gitbook/assets/am-agents-list.png" alt="AM agents list showing agent applications"><figcaption></figcaption></figure>

## Manual Creation

1. Select an **Agent Persona** from the dropdown: **User-Embedded**, **Hosted Delegated**, or **Autonomous**.
2. Enter an **Application Name** in the text field.
3. (Optional) Enter a **Description** in the text area.
4. Toggle **Use as DCR / CIMD Registration Template** to mark this agent as the domain's registration template.
5. Click **Next** to configure OAuth/OIDC settings (redirect URIs, grants, scopes).
6. Click **Create** to save the agent application.

**Agent Persona Reference:**

| Field | Description | Constraints |
|:------|:------------|:------------|
| **Agent Persona** | Agent sub-type: User-Embedded, Hosted Delegated, or Autonomous | Required when application type is AGENT |
| **Application Name** | Human-readable name for the agent | Required |
| **Description** | Optional description of the agent's purpose | Optional |
| **Use as DCR / CIMD Registration Template** | Mark this agent as the domain's DCR/CIMD registration template | Optional |

## CIMD Creation

1. Toggle the creation mode to **CIMD**.

    <figure><img src="../../.gitbook/assets/am-agent-wizard-cimd-mode.png" alt="Agent creation wizard in CIMD mode"><figcaption></figcaption></figure>

2. Enter the **Document URL** in the text field (the CIMD endpoint serving the client metadata JSON).
3. Click **Validate**. AM fetches and validates the document server-side.
4. Review the **CIMD Confirm** preview showing parsed metadata (redirect URIs, grants, scopes, JWKS, mTLS settings).
5. If the document lacks a `client_name`, enter an **Application Name** in the prompt field.
6. Click **Create** to save the agent application. The CIMD URL becomes the application's `client_id`.

**CIMD Validation Reference:**

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Document URL** | HTTPS endpoint serving the CIMD JSON | Must be `http(s)://` URL; HTTP allowed only if `allowUnsecuredHttpUri=true`; host must be in `allowedDomains` (if non-empty); must not resolve to private/reserved IP unless `allowPrivateIpAddress=true` |
| **Application Name** | Auto-filled from document's `client_name`; prompted if absent | Required |
