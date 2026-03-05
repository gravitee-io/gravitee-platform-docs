### Searching Protected Resources

Query Protected Resources by name or client ID using wildcard patterns.

#### Endpoint

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources
```

#### Query Parameters

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `q` | String | — | Search query string. Supports `*` wildcard for pattern matching. |
| `type` | String | — | Resource type filter. |
| `page` | Integer | `0` | Page number for pagination. |
| `size` | Integer | `50` | Number of results per page. |

#### Search Behavior

- **Case-insensitive matching:** The search query is matched against the `name` and `clientId` fields only.
- **Wildcard support:** Use `*` to match zero or more characters. For example, `q=clientId*` matches `clientId`, `clientId2`, and `clientIdTest`.
- **Sorting:** Results are sorted by `updatedAt` in descending order.
- **Pagination:** The response includes a total count of matching resources.

#### Required Permission

`PROTECTED_RESOURCE[READ]`

#### Response

**Status:** `200 OK`

**Body:** `Page<ProtectedResourcePrimaryData>`

The response contains a paginated list of Protected Resources matching the search criteria, along with the total count of results.

#### Example

To search for all Protected Resources with a client ID starting with `clientId`:

```
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources?q=clientId*&page=0&size=50
```
