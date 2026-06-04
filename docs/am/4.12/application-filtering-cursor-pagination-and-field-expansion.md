# Application Filtering, Cursor Pagination, and Field Expansion

## Overview

Application Filtering, Cursor Pagination, and Expand Parameters extend the Access Management application list API with query-based filtering, cursor-based pagination for large datasets, and selective field expansion. Administrators can filter applications by status, owner email, and type; paginate efficiently using cursor tokens; and optionally include the OAuth client ID in responses. These capabilities improve performance and usability when managing large application inventories.

## Key Concepts

### Query-Based Filtering

The application list endpoint supports three filter parameters: `status` (enabled or disabled), `owner.email` (primary owner's email address), and `type` (application type). Filters combine using AND logic. The `owner.email` filter requires `ORGANIZATION_USER[READ]` permission on the organization; users without this permission cannot filter by owner. When `owner.email` resolves to zero applications or the user lacks permission to view any matching applications, the API returns an empty result set.

### Cursor Pagination

Cursor pagination replaces offset-based pagination for large datasets. The initial request omits the `cursor` parameter and uses `page=0`. The response includes a `nextCursor` field containing an opaque Base64-encoded token. Subsequent requests pass this token to retrieve the next page. When `nextCursor` is `null`, no more pages exist. Cursor tokens encode the last record's ID and sort value; they are deployment-specific and may not work after schema changes. Only `updatedAt` and `name` sort fields are supported.

| Response Field | Type | Description |
|:---------------|:-----|:------------|
| `data` | array | Array of `FilteredApplication` objects |
| `nextCursor` | string | Path to next page (null if no more pages) |
| `hasNext` | boolean | Whether additional pages exist |
| `totalCount` | integer | Total matching applications |
| `page` | integer | Current page number (zero-based) |

### Field Expansion

The `expand` parameter controls optional fields in the response. When `expand=clientId` is present, each `FilteredApplication` object includes the OAuth `clientId` field. When omitted, `clientId` is `null`. This reduces payload size when client IDs are not needed.

## Prerequisites

- Access Management 4.12.0 or later
- `APPLICATION[LIST]` permission on the domain, environment, or organization
- `ORGANIZATION_USER[READ]` permission (required only for `owner.email` filter)

## Creating applications

## Filtering and Paginating Applications

### Offset Pagination with Filters

To filter applications using offset-based pagination, send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications` with query parameters. Include `status=enabled` or `status=disabled` to filter by enabled state, `owner.email=<email>` to filter by primary owner, `type=<type>` to filter by application type (repeatable for multiple types), and `expand=clientId` to include OAuth client IDs in the response. Use `page` and `size` parameters for pagination. The response includes `data`, `currentPage`, and `totalCount` fields.

### Cursor Pagination

To use cursor pagination, send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/search` with `limit` (default 50), `sort` (`updatedAt` or `name`), and `dir` (`ASC` or `DESC`) parameters. Include `status`, `owner.email`, `type`, `expand`, and `q` (wildcard search) as needed. The response includes a `nextCursor` field containing the path to the next page. For subsequent pages, send a GET request to the `nextCursor` path or to `/applications/search/_cursor?cursor=<token>` with the cursor token. When `nextCursor` is `null`, no more pages exist.

**Example: Initial cursor request**
```http
GET /domains/{domain}/applications/search?limit=50&sort=updatedAt&dir=DESC&status=enabled&expand=clientId
```

**Example: Subsequent cursor request**
```http
GET /domains/{domain}/applications/search/_cursor?cursor=<encoded-token>&page=1&limit=50&sort=updatedAt&dir=DESC
```

### Management API

**Endpoint:** `GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications`

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `status` | string | Filter by status. Values: `enabled`, `disabled` |
| `owner.email` | string | Filter by owner email address |
| `expand` | array | Expand fields. Supported: `clientId` |
| `page` | integer | Page number (zero-based) |
| `size` | integer | Results per page |

**Endpoint:** `GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/search`

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `limit` | integer | 50 | Maximum results per page |
| `sort` | string | `updatedAt` | Sort field. Values: `updatedAt`, `name` |
| `dir` | string | `DESC` | Sort direction. Values: `ASC`, `DESC` |
| `page` | integer | 0 | Page number (zero-based) |
| `expand` | array | — | Expand fields. Supported: `clientId` |
| `q` | string | — | Search query (supports wildcard `*`) |
| `status` | string | — | Filter by status. Values: `enabled`, `disabled` |
| `owner.email` | string | — | Filter by owner email |
| `type` | array | — | Filter by type. Values: `WEB`, `NATIVE`, `BROWSER`, `SERVICE`, `RESOURCE_SERVER`, `AGENT` |

**Endpoint:** `GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/search/_cursor`

Same parameters as `/search`, plus:

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `cursor` | string | Opaque cursor token for pagination continuation |

## Restrictions

- Cursor tokens are opaque and deployment-specific; tokens from one deployment may not work after schema changes.
- Wildcard search queries (`q=alpha*`) with cursor pagination cannot leverage indexes efficiently in MongoDB and may degrade performance with large datasets.
- The `owner.email` filter requires `ORGANIZATION_USER[READ]` permission; users without this permission cannot filter by owner email and receive HTTP 403.
- Only `updatedAt` and `name` sort fields are supported for cursor pagination; other fields return HTTP 400.
- The `status` parameter must match `enabled` or `disabled`; invalid values are rejected.
- Invalid cursor tokens return HTTP 400.

## Related Changes

The application list API now returns a `FilteredApplication` object with an optional `clientId` field controlled by the `expand` parameter. New cursor pagination endpoints (`/search` and `/search/_cursor`) return an `ApplicationCursorPage` response with `nextCursor`, `hasNext`, `totalCount`, and `page` fields. Database indexes on the `applications` table (`idx_application_domain_updated_at_id`, `idx_application_domain_name_id`, and descending variants) support efficient cursor pagination. MongoDB indexes (`d1u1i1`, `d1n1i1`, and descending variants) provide equivalent support. Existing offset-based pagination endpoints remain unchanged; cursor pagination is additive and opt-in.
