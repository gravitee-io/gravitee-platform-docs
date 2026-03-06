### Notification System

Client secret expiration notifications are registered automatically when secrets are created or renewed, and deregistered when secrets are deleted. Notifications use the following data structure:

**Notification Data:**
```json
{
  "clientSecret": {
    "name": "string",
    "expiresAt": "date"
  },
  "application": {
    "name": "string"
  },
  "resourceType": "string"
}
```

**Metadata:**
```json
{
  "domainId": "string",
  "domainOwner": "string",
  "{resourceType}Id": "string",
  "clientSecretId": "string"
}
```

The `resourceType` field is derived from the target class name and formatted for display (e.g., "protected resource"). The metadata key for the resource ID is dynamically constructed based on the resource type (e.g., `protectedResourceId`).

**Log Message Format:**
```
Client Secret {name} of {className} {resourceName} in domain {domainId} expires on {expiresAt}
```

### Related Changes

#### UI Filtering

The UI filters grant types and token endpoint authentication methods when the context is MCP Server, hiding options incompatible with that resource type.

**Filtered Grant Types for MCP Server:**
* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

**Filtered Token Endpoint Auth Methods for MCP Server:**
* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

#### Database Schema

**JDBC:**

The `protected_resources` table adds a `certificate` column:

```yaml
- column:
    name: certificate
    type: nvarchar(64)
    constraints:
      nullable: true
```

**MongoDB:**

The `protected_resources` collection adds a `certificate` field:

```java
public final static String CERTIFICATE_FIELD = "certificate";
private String certificate;
```

#### Repository Methods

New methods support certificate-based lookups and wildcard search queries:

| Method | Return Type | Description |
|:-------|:------------|:------------|
| `findByCertificate(String certificateId)` | `Flowable<ProtectedResource>` | Find all Protected Resources using a specific certificate |
| `search(String domain, String query, PageSortRequest)` | `Single<Page<ProtectedResourcePrimaryData>>` | Search Protected Resources by name or clientId with wildcard support |

**JDBC Implementation:**

```sql
SELECT * FROM protected_resources a WHERE a.certificate = :certificateId
```

```sql
SELECT * FROM protected_resources pr WHERE 
  pr.domain_id = :domain_id 
  AND (
    upper(pr.name) LIKE :value 
    OR upper(pr.client_id) LIKE :value
  )
```

**MongoDB Implementation:**

Query for `findByCertificate`:
```java
eq(CERTIFICATE_FIELD, certificateId)
```

Query for `search`:
```java
and(
  eq(DOMAIN_ID_FIELD, domain),
  or(
    new BasicDBObject(CLIENT_ID_FIELD, pattern),
    new BasicDBObject("name", pattern)
  )
)
```

The `pattern` is a case-insensitive regex built from the query string.

#### Event System

The event system introduces `PROTECTED_RESOURCE_SECRET` events with the following actions:

* `CREATE` — maps to `Action.CREATE`
* `RENEW` — maps to `Action.UPDATE`
* `DELETE` — maps to `Action.DELETE`

**Event Payload:**
```java
new Payload(secretId, ReferenceType.PROTECTED_RESOURCE, protectedResourceId, action)
```

The event listener subscribes to `ProtectedResourceSecretEvent` on startup, initializes client secret notifications for all existing Protected Resources, and handles CREATE, RENEW, and DELETE events to manage expiration notifications.

#### Token Introspection Logic

Token introspection now queries both Application and Protected Resource repositories when resolving audience claims:

1. Introspect token
2. Attempt to resolve client by audience:
   * First check Applications by client ID
   * If not found, check Protected Resources by client ID
3. If neither found, return error: `"Client or resource not found: {aud}"`
