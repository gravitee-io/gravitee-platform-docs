### UI Component Changes

#### Grant Flows Component

The Grant Flows component filters grant types and token endpoint authentication methods based on context:

| Context | Behavior |
|:--------|:---------|
| `McpServer` | Hides Refresh Token and PKCE sections; filters grant types to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`; filters token endpoint auth methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt` |
| `Application` | Displays all grant types and token endpoint authentication methods |

**Help Text for MCP Servers:**

### Notification System

Protected Resource secrets support expiration notifications using the same notification system as Application secrets. Notifications are registered on secret creation/renewal and unregistered on secret deletion.

**Log Message Format:**

**Notification Subject Data:**

**Metadata:**

### Event Types

#### PROTECTED_RESOURCE_SECRET

**Actions:**
- `CREATE` — Secret created
- `RENEW` — Secret renewed (maps from `Action.UPDATE`)
- `DELETE` — Secret deleted

### Database Schema Changes

#### protected_resources Table

**New Column:**
- `certificate` (nvarchar(64), nullable)

**Liquibase Changeset:**

### Search Implementation

#### MongoDB Repository

Search queries use regex patterns for wildcard matching:

**Wildcard Handling:**

#### JDBC Repository

Search queries use `LIKE` clauses with case-insensitive matching:
