---
description: Documentation about MongoDB index management in the context of APIs.
metaLinks:
  alternates:
    - mongodb-index-management.md
---

# MongoDB Index Management

The following MongoDB indexes are designed to improve query performance for large datasets. Create these indexes manually before upgrading to avoid extended Management API startup times.

{% hint style="warning" %}
Four new indexes are created on the `events` collection. For databases with event collections of 100GB+, index creation can take **10-20 minutes or longer** per index.
{% endhint %}

| Collection             | Index Name                | Keys                                                                                                               | Type     | Purpose                                       | Collation                                    |
| ---------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------- | -------------------------------------------- |
| `clusters`             | `ce1`                     | `environmentId` (asc)                                                                                              | Standard | Filter clusters by environment                |                                              |
| `apis`                 | `dv1ei1n1`                | `definitionVersion` (asc), `environmentId` (asc), `name` (asc)                                                     | Standard | Search APIs by version, environment, and name |                                              |
| `commands`             | `t1to1`                   | `tags` (asc), `to` (asc)                                                                                           | Standard | Query commands by tags and target             |                                              |
| `events`               | `e1ua`                    | `environments` (desc), `createdAt` (desc)                                                                          | Standard | Fetch recent events by environment            |                                              |
| `events`               | `pads1pgi1ua-1i-1t1`      | `properties.api_debug_status` (asc), `properties.gateway_id` (asc), `updatedAt` (desc), `_id` (desc), `type` (asc) | Standard | API debug mode queries                        |                                              |
| `events`               | `pi1ua-1i-1e1t1`          | `properties.id` (asc), `updatedAt` (desc), `_id` (desc), `environments` (asc), `type` (asc)                        | Standard | Event lookup by property ID                   |                                              |
| `events`               | `u-1i-1`                  | `updatedAt` (desc), `_id` (desc)                                                                                   | Standard | Recent events queries                         |                                              |
| `invitations`          | `ri1rt1e1`                | `referenceId` (asc), `referenceType` (asc), `email` (asc)                                                          | Standard | Search invitations by reference and email     | Locale `en`, strength `SECONDARY` (case-insensitive) |
| `keys`                 | `r1ua-1ea1`               | `revoked` (asc), `updatedAt` (desc), `expireAt` (asc)                                                              | Standard | Query active/revoked API keys                 |                                              |
| `portal_page_contexts` | `ppc_ctx_env1`            | `contextType` (asc), `environmentId` (asc)                                                                         | Standard | Portal page context queries                   |                                              |
| `portal_page_contexts` | `ppc_page_ctx_env_unique` | `pageId` (asc), `contextType` (asc), `environmentId` (asc)                                                         | Unique   | Ensure unique page contexts                   |                                              |
| `subscriptions`        | `s1ca-1ea1`               | `status` (asc), `createdAt` (desc), `endingAt` (asc)                                                               | Standard | Subscription lifecycle queries                |                                              |

## JDBC Invitation Search

For JDBC databases, invitation search uses the following SQL pattern:

```sql
SELECT * FROM invitations 
WHERE reference_id = ? 
  AND reference_type = ? 
  AND lower(email) LIKE ? ESCAPE '\' 
ORDER BY CASE WHEN email IS NULL THEN 1 ELSE 0 END, lower(email) ASC
```

Sortable columns: `id`, `reference_type`, `reference_id`, `email`, `api_role`, `application_role`, `created_at`, `updated_at`

Default sort: `email` ascending, case-insensitive, with null values sorted last.
