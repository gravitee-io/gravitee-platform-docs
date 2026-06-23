---
description: Reference for filtering, cursor pagination, and field expansion parameters for the Access Management Application list API.
---

# Application Filtering, Cursor Pagination, and Expand Parameters

## Overview

Application Filtering, Cursor Pagination, and Expand Parameters extend the Access Management Application list API with query filters, field expansion, and cursor-based pagination. You can filter Applications by status and owner email, expand responses to include OAuth client IDs, and paginate large result sets efficiently using cursor tokens. These enhancements improve API performance and enable more granular Application discovery workflows.

## Key Concepts

### Query Filters

The Application list endpoint supports two filters: `status` filters Applications by enabled or disabled state, and `owner.email` filters by the primary owner's email address. Filters combine using AND logic with permission-scoped Application IDs—the final result respects both the filter criteria and your access permissions. When `owner.email` resolves to zero users or permission-scoped IDs are empty, the API returns an empty page without querying the database.

### Field Expansion

The `expand` parameter controls which additional fields appear in the response. Setting `expand=clientId` includes the OAuth client ID for each Application. Unknown expansion values are silently ignored. This feature reduces the need for follow-up API calls when client IDs are required for integration workflows.

### Cursor Pagination

Cursor-based pagination replaces offset-based paging for large Application lists. The API returns a `nextCursor` path containing a Base64-encoded token that encodes the last item's ID and sort value. Pass this token to retrieve the next page. Cursor tokens are opaque and must not be parsed or modified. If the underlying dataset changes between requests and Applications are deleted or updated, cursor tokens may become invalid.

The following table describes the available pagination types:

| Pagination Type | Endpoint | Token Format | Use Case |
|:----------------|:---------|:-------------|:---------|
| Offset-based (legacy) | `/applications` | `page` and `size` parameters | Small datasets, simple navigation |
| Cursor-based | `/applications/search/_cursor` | Base64-encoded `cursor` token | Large datasets, efficient traversal |

## Prerequisites

Ensure the following prerequisites are met:

- Access Management 4.12.0 or later
- `DOMAIN_APPLICATION[LIST]` permission for the target domain
- `ORGANIZATION_USER[READ]` permission to filter by `owner.email`

## Create application queries

To filter and paginate Applications, construct a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/search` with query parameters. Use `status=enabled` or `status=disabled` to filter by Application state. Add `owner.email={email}` to filter by primary owner—this requires `ORGANIZATION_USER[READ]` permission on the organization. Include `expand=clientId` to retrieve OAuth client IDs in the response. For wildcard searches, use `q=alpha*` to match Application names starting with "alpha". Combine filters as needed: `status=enabled&owner.email=admin@example.com&type=WEB,SERVICE` returns enabled Web or Service Applications owned by the specified owner. The API applies AND logic between `status` and `owner.email`, and OR logic within the `type` array.

The following query parameters are available:

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `status` | string | — | Filter by status. Values: `enabled`, `disabled` |
| `owner.email` | string | — | Filter by owner email address |
| `expand` | array[string] | — | Fields to expand. Supported: `clientId` |
| `q` | string | — | Search query (supports wildcard `*`) |
| `type` | array[string] | — | Filter by type. Values: `WEB`, `NATIVE`, `BROWSER`, `SERVICE`, `RESOURCE_SERVER`, `AGENT` |
| `limit` | integer | 50 | Maximum results per page |
| `sort` | string | `updatedAt` | Sort field. Supported: `updatedAt`, `name` |
| `dir` | string | `DESC` | Sort direction. Values: `ASC`, `DESC` |
| `page` | integer | 0 | Page number (zero-indexed) |

## Paginate with cursors

To paginate large result sets, use the cursor-based search endpoint at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/applications/search/_cursor`. The initial request omits the `cursor` parameter and returns an `ApplicationCursorPage` response. This response contains a `data` array, `nextCursor` path, `hasNext` boolean, `totalCount`, and `page` number. If `hasNext` is true, extract the full `nextCursor` path from the response and issue a GET request to that URL to retrieve the next page. Repeat until `nextCursor` is null. The cursor token encodes the last item's ID and sort value in Base64 format, following the pattern `lastId##lastSortValue`. You must treat the token as opaque and pass it unmodified. Cursor tokens become invalid if Applications are deleted or updated between requests.

The following table describes the cursor response schema:

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | array | Array of `FilteredApplication` objects |
| `nextCursor` | string | Path to next page (null if no more pages) |
| `hasNext` | boolean | Whether additional pages exist |
| `totalCount` | integer | Total matching Applications |
| `page` | integer | Current page number |

The following table describes the `FilteredApplication` schema:

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Application ID |
| `name` | string | Application name |
| `description` | string | Application description |
| `type` | string | Application type enum |
| `enabled` | boolean | Whether the Application is enabled |
| `template` | boolean | Whether the Application is a template |
| `updatedAt` | date | Last update timestamp |
| `clientId` | string | OAuth client ID. This field is only present when `expand=clientId` is set. |

## Restrictions

Note the following restrictions:

- Filtering by `owner.email` requires `ORGANIZATION_USER[READ]` permission on the organization; requests without this permission return `403 Forbidden`
- Only `updatedAt` and `name` are supported as sort fields; other values cause `400 Bad Request`
- Wildcard searches using `*` cannot leverage database indexes efficiently and may perform poorly on large datasets
- Cursor tokens are invalidated if Applications are deleted or updated between pagination requests
- Unknown values in the `expand` parameter are silently ignored
- The `status` parameter accepts only `enabled` or `disabled`; other values cause `400 Bad Request`
- Cursor tokens must be valid Base64 strings with a `##` separator; malformed tokens cause `400 Bad Request`

## Related Changes

The Application list response now includes an optional `clientId` field when `expand=clientId` is specified. The cursor pagination endpoint returns a `nextCursor` path in the format `/organizations/{orgId}/environments/{envId}/domains/{domainId}/applications/search/_cursor?cursor={base64Token}&page={nextPage}&q={query}&status={status}&type={type}`. Database indexes are created automatically on the JDBC `applications` table or MongoDB `applications` collection during upgrade to support efficient cursor pagination by `updatedAt` and `name` fields. No manual migration steps are required.
