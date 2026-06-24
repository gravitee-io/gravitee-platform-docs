# Portal documentation management (Next-Gen Developer Portal)

## Create portal documentation

Portal-scoped documentation pages provide platform-level guides and reference material. Each page attaches to a portal and appears at a specified location in the portal's navigation hierarchy.

{% hint style="info" %}
Navigation paths referenced in the `location` field exist in the portal's navigation hierarchy. When a documentation page references a location that does not exist yet, the page is created as an orphan and reconnects when the folder appears, so apply order does not matter.
{% endhint %}

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` with the documentation specification.
2. Specify the page's HRID, display name, type (Gravitee Markdown, OpenAPI, or AsyncAPI), content, location, and optional order.
3. Retrieve a documentation page by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}`.
4. Delete a documentation page by sending a `DELETE` request to the same path.

**Example request:**

```http
PUT /organizations/{orgId}/environments/{envId}/portals/default-portal/documentations
Content-Type: application/json

{
  "hrid": "getting-started",
  "name": "Getting Started",
  "type": "GRAVITEE_MARKDOWN",
  "content": "# Getting Started\nWelcome to the developer portal.",
  "location": "/projects/alpha",
  "order": 1
}
```

When `dryRun` validation fails, the response returns the errors under the `errors` field. The validation messages are:

| Field | Constraint | Validation message |
|:------|:-----------|:-------------------|
| `name` | Required | `name must not be blank` |
| `type` | Required: `GRAVITEE_MARKDOWN`, `OPENAPI`, or `ASYNCAPI` | `type must not be null` |
| `content` | Required | `content must not be null` |

## Automation API endpoints

These endpoints require the `ENVIRONMENT_PORTAL` permission.

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations` | PUT | Create or update portal documentation. Supports the `dryRun` query parameter. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | GET | Retrieve portal documentation by HRID. |
| `/organizations/{orgId}/environments/{envId}/portals/{portalHrid}/documentations/{docHrid}` | DELETE | Delete portal documentation by HRID. Returns HTTP 204 on success. |

When the portal navigation is re-synced, automation-managed portal documentation is re-placed to reflect parent folder changes.
