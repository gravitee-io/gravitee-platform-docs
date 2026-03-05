### Management API Endpoints

#### Secret Management

**Base Path:** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets`

| Method | Path | Description | Required Permission |
|:-------|:-----|:------------|:-------------------|
| GET | `/` | List secrets of a protected resource | PROTECTED_RESOURCE[LIST] |
| POST | `/` | Create a secret for a protected resource | PROTECTED_RESOURCE[CREATE] |
| POST | `/{secretId}/_renew` | Renew a secret for a protected resource | PROTECTED_RESOURCE[UPDATE] |
| DELETE | `/{secretId}` | Remove a secret for a protected resource | PROTECTED_RESOURCE[DELETE] |

**Request Body for POST (Create Secret):**

**Response Schema:**

#### Membership Management

**Base Path:** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members`

| Method | Path | Description | Required Permission |
|:-------|:-----|:------------|:-------------------|
| GET | `/` | Get members of a protected resource | PROTECTED_RESOURCE_MEMBER[LIST] |
| POST | `/` | Add or update a member | PROTECTED_RESOURCE_MEMBER[CREATE] |
| GET | `/permissions` | Get permissions for authenticated user | PROTECTED_RESOURCE[READ] |
| DELETE | `/{member}` | Remove a membership | PROTECTED_RESOURCE_MEMBER[DELETE] |

**Request Body for POST (Add Member):**

**Permission Hierarchy:**

1. Resource-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on specific resource
2. Domain-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on domain
3. Environment-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on environment
4. Organization-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on organization

#### Search

**Query Parameters:**

* `q`: Search query string. Supports wildcards (`*`). Searches against `name` and `clientId` fields.
* `type`: Resource type filter
* `page`: Page number (default: 0)
* `size`: Page size (default: 50)

**Example:**

**Search Behavior:**

| Query Type | Behavior |
|:-----------|:---------|
| Exact match | `q=clientId` matches `clientId` or `name` exactly |
| Wildcard | `q=client*` performs case-insensitive prefix match on `clientId` or `name` |
| Case sensitivity | All searches are case-insensitive |

### Database Schema Changes

#### JDBC: `protected_resources` Table

**Added Column:**

#### MongoDB: `protected_resources` Collection

**Added Field:**

### Repository Methods

#### New Methods in `ProtectedResourceRepository`

| Method | Return Type | Description |
|:-------|:------------|:------------|
| `findByCertificate(String certificateId)` | `Flowable<ProtectedResource>` | Find all Protected Resources using a specific certificate |
| `search(String domain, String query, PageSortRequest)` | `Single<Page<ProtectedResourcePrimaryData>>` | Search Protected Resources by name or clientId with wildcard support |

#### JDBC Implementation

**SQL Query for `findByCertificate`:**

**SQL Query for `search` (wildcard):**

#### MongoDB Implementation

**Query for `findByCertificate`:**

**Query for `search`:**

The `pattern` is a case-insensitive regex built from the query string.

### Event System

#### Event Type: `PROTECTED_RESOURCE_SECRET`

**Actions:**

* `CREATE` — maps to `Action.CREATE`
* `RENEW` — maps to `Action.UPDATE`
* `DELETE` — maps to `Action.DELETE`

**Event Payload:**

#### Event Listener: `ProtectedResourceSecretManager`

**Lifecycle:**

* Subscribes to `ProtectedResourceSecretEvent` on startup
* Initializes client secret notifications for all existing Protected Resources
* Handles CREATE, RENEW, DELETE events to manage expiration notifications

### Notification System

#### Client Secret Expiration Notifications

**Notification Data:**

**Metadata:**

**Log Message Format:**

Example: `Client Secret default-secret of class io.gravitee.am.model.ProtectedResource mcp-server in domain test-domain expires on 2025-12-31`

### Model Changes

#### `ProtectedResource` Model

**Added Field:**

**Updated Constructor:**

**Updated `toClient()` Method:**

The `toClient()` method copies the `certificate` field to the resulting `Client` object, ensuring certificate-based authentication configurations propagate correctly.

#### `ProtectedResourcePrimaryData` Record

**Added Field:**

**Updated Factory Method:**

### Service Layer Changes

#### `ProtectedResourceService` Interface

**Added Methods:**

#### `ClientSecretNotifierService` Interface

**Added Method:**

### Token Introspection

#### Audience Validation

**Flow:**

1. Introspect token using `IntrospectionTokenService`
2. Attempt to resolve client by `jwt.getAud()`:
 * First check `ClientSyncService.findByDomainAndClientId()`
 * If not found, check `ProtectedResourceSyncService.findByDomainAndClientId()`
3. If neither found, return error: `Client or resource not found: {aud}`
4. Return `OAuth2AuthResponse` with resolved client

**Error Message:**

### Error Classes

| Exception | Package | Purpose |
|:----------|:--------|:--------|
| `CertificateWithProtectedResourceException` | `io.gravitee.am.service.exception` | Thrown when attempting to delete a certificate referenced by Protected Resources |
| `ClientSecretNotFoundException` | `io.gravitee.am.service.exception` | Thrown when a client secret ID is not found |
| `ProtectedResourceNotFoundException` | `io.gravitee.am.service.exception` | Thrown when a protected resource ID is not found |
