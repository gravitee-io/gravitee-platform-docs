---
hidden: false
noIndex: false
description: >-
  Store custom observability dashboards in the environment they belong to, and
  create, read, update, and delete them over the Gamma API.
---

# Save observability dashboards with the Gamma API

Gamma stores custom observability dashboards in the environment they belong to. A saved dashboard carries its title, its filters, its time range, and its widgets. It stays available after a restart, from any machine, and to every user with read access to that environment's dashboards.

Dashboards are created and maintained over the Gamma API. Each one lives in exactly one environment and is never returned to a request scoped to a different environment.

## Before you begin

The dashboard endpoints live under the environment-scoped observability base path of the Gamma application, `/gamma/organizations/{orgId}/environments/{envId}/observability/dashboards`.

`orgId` is the identifier of the organization. `envId` accepts either the identifier of the environment or its human-readable ID.

The examples on this page use a local installation, the `DEFAULT` organization and environment, and Basic authentication. Substitute your own host, IDs, and credentials:

```bash
export GAMMA=http://localhost:8083/gamma/organizations/DEFAULT/environments/DEFAULT/observability
export AUTH="admin:admin"
```

A personal access token works in place of Basic authentication. Send it in the `Authorization` header:

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$GAMMA/dashboards"
```

A caller who lacks the matching access level on the environment's dashboards receives `403 Forbidden` with the message `You do not have sufficient rights to access this resource`. Reading needs read access, and creating, updating, and deleting each need their own access level.

{% hint style="info" %}
The full Observability API specification, including the dashboard schemas, is served by the Gamma application at `/gamma/docs/observability/`.
{% endhint %}

## Dashboard fields

A dashboard returned by the API carries the following fields.

<table>
    <thead>
        <tr>
            <th width="140">Field</th>
            <th width="120">Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>id</code></td>
            <td>string</td>
            <td>Identifier you choose when you create the dashboard.</td>
        </tr>
        <tr>
            <td><code>title</code></td>
            <td>string</td>
            <td>Required. A blank title is rejected with <code>400</code> and the message <code>Dashboard title is required</code>.</td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td>string</td>
            <td>Optional free text.</td>
        </tr>
        <tr>
            <td><code>filters</code></td>
            <td>array</td>
            <td>Filters applied to every widget of the dashboard. See <a href="#dashboard-filters">Dashboard filters</a>.</td>
        </tr>
        <tr>
            <td><code>timeRange</code></td>
            <td>object</td>
            <td>The window the dashboard opens on. See <a href="#time-ranges">Time ranges</a>.</td>
        </tr>
        <tr>
            <td><code>widgets</code></td>
            <td>array</td>
            <td>Stored and returned exactly as sent. See <a href="#widgets">Widgets</a>.</td>
        </tr>
        <tr>
            <td><code>version</code></td>
            <td>integer</td>
            <td>Server-owned. Starts at <code>1</code> and increases by one on every successful update.</td>
        </tr>
        <tr>
            <td><code>createdAt</code></td>
            <td>integer</td>
            <td>Server-owned. Epoch milliseconds.</td>
        </tr>
        <tr>
            <td><code>updatedAt</code></td>
            <td>integer</td>
            <td>Server-owned. Epoch milliseconds.</td>
        </tr>
    </tbody>
</table>

`version`, `createdAt`, and `updatedAt` are set by Gamma. Sending them in a request body has no effect, and neither does sending an environment identifier: the environment comes from the URL.

### Dashboard filters

Each entry of `filters` applies to every widget of the dashboard.

<table>
    <thead>
        <tr>
            <th width="130">Field</th>
            <th width="130">Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>name</code></td>
            <td>string</td>
            <td>Required. A blank name is rejected with <code>400</code> and the message <code>Dashboard filter name is required</code>.</td>
        </tr>
        <tr>
            <td><code>label</code></td>
            <td>string</td>
            <td>Optional display text, stored and returned as sent.</td>
        </tr>
        <tr>
            <td><code>operator</code></td>
            <td>string</td>
            <td>Required. Read case-insensitively and returned uppercase. An operator Gamma doesn't recognize is rejected with <code>400</code>.</td>
        </tr>
        <tr>
            <td><code>value</code></td>
            <td>string or array</td>
            <td>Accepted as a single value or as an array, and always returned as an array. An omitted value is stored as an empty array.</td>
        </tr>
        <tr>
            <td><code>editable</code></td>
            <td>boolean</td>
            <td>Whether a viewer of the dashboard is allowed to change the value. Gamma stores the flag and returns it unchanged. Omitting it stores <code>false</code>, which locks the filter.</td>
        </tr>
    </tbody>
</table>

Filter names aren't checked against the environment's filter catalog when the dashboard is saved. A name is stored as given, so a dashboard moves between environments whose available filters differ.

### Time ranges

`timeRange` takes one of two shapes, set by its `type`. The value is read case-insensitively and returned lowercase.

<table>
    <thead>
        <tr>
            <th width="130">Type</th>
            <th>Required fields</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>relative</code></td>
            <td><code>period</code>. A relative range without one is rejected with <code>400</code> and the message <code>A relative time range requires a period</code>.</td>
        </tr>
        <tr>
            <td><code>absolute</code></td>
            <td><code>from</code> and <code>to</code>, in epoch milliseconds, with <code>from</code> earlier than <code>to</code>. A range that omits either bound, or sets <code>from</code> at or after <code>to</code>, is rejected with <code>400</code>.</td>
        </tr>
    </tbody>
</table>

Omitting `timeRange` altogether is valid. A `timeRange` without a `type` is rejected with `400`, and so is any `type` other than the two above.

### Widgets

Gamma stores the `widgets` array exactly as you send it and returns it unchanged, so you define the shape of a widget. Three rules apply:

* `widgets` is an array. Any other JSON value is rejected with `400` and the message `Dashboard widgets must be an array`.
* A dashboard holds at most 50 widgets, and the serialized array is at most 1,048,576 characters.
* Every widget carries a non-blank `id`, unique within the dashboard. A missing or repeated `id` is rejected with `400`.

## List the dashboards of an environment

```bash
curl -s -u "$AUTH" "$GAMMA/dashboards?page=1&perPage=20"
```

The response is `200 OK` with the dashboards of the environment, oldest first, and a `pagination` block:

```json
{
  "data": [
    {
      "id": "d7e246cb-ab02-4da4-8f47-f9fa3e061d6b",
      "title": "Performance overview",
      "filters": [],
      "timeRange": { "type": "relative", "period": "24h" },
      "widgets": [],
      "version": 3,
      "createdAt": 1730000000000,
      "updatedAt": 1730600000000
    }
  ],
  "pagination": {
    "totalCount": 1,
    "page": 1,
    "perPage": 20,
    "pageCount": 1,
    "pageItemsCount": 1
  }
}
```

Each entry is a complete dashboard, so no extra call is needed to read one from the list.

`page` is 1-based and defaults to `1`. `perPage` defaults to `20` and is capped at `100`, so a larger value returns 100 items. A `page` or `perPage` of zero or less falls back to the default rather than failing.

## Create a dashboard

You supply the `id`. Generate one client-side, typically a UUID, and reuse it for every later call on that dashboard. A request without an `id` is rejected with `400`.

```bash
curl -s -u "$AUTH" -X POST "$GAMMA/dashboards" \
  -H 'Content-Type: application/json' \
  -d '{
        "id": "d7e246cb-ab02-4da4-8f47-f9fa3e061d6b",
        "title": "Performance overview",
        "description": "MCP traffic health",
        "filters": [
          { "name": "API_TYPE", "label": "API Type", "operator": "EQ", "value": ["MCP"], "editable": false }
        ],
        "timeRange": { "type": "relative", "period": "24h" },
        "widgets": [{ "id": "w1", "type": "metric" }]
      }'
```

The response is `201 Created` with the stored dashboard. Two headers come back with it:

* `Location`, the URL of the new dashboard.
* `ETag`, its version, which starts at `1`. Keep it for the first update.

## Read a dashboard

```bash
curl -si -u "$AUTH" "$GAMMA/dashboards/d7e246cb-ab02-4da4-8f47-f9fa3e061d6b"
```

The response is `200 OK` with the dashboard as it was saved, and an `ETag` header carrying its current version. An identifier that doesn't exist in this environment returns `404 Not Found`.

## Update a dashboard

An update replaces the content of the dashboard, so send the whole object. Anything you leave out is cleared. The identifier comes from the URL, and an `id` in the body is ignored.

Quote the `ETag` you received in an `If-Match` header:

```bash
curl -s -u "$AUTH" -X PUT "$GAMMA/dashboards/d7e246cb-ab02-4da4-8f47-f9fa3e061d6b" \
  -H 'Content-Type: application/json' \
  -H 'If-Match: "3"' \
  -d '{
        "title": "Performance overview",
        "filters": [],
        "timeRange": { "type": "absolute", "from": 1730000000000, "to": 1730600000000 },
        "widgets": [{ "id": "w1", "type": "metric" }]
      }'
```

The response is `200 OK` with the updated dashboard, its incremented `version`, and a fresh `ETag` for the next update.

`If-Match` is required. Without it the request is refused with `428 Precondition Required` rather than treated as an overwrite. Several validators are accepted, either comma-separated or as a repeated header, and one of them matching is enough. Weak validators such as `W/"3"` are accepted as equivalent to `"3"`. A validator this API didn't issue is rejected with `400`.

### Handle a conflicting save

When someone saved the dashboard after you read it, your `If-Match` no longer matches and the update is refused with `412 Precondition Failed`. Nothing changes on the server, and their work stays intact.

The `412` body carries the dashboard as it stands right now, alongside the standard error fields, and the response repeats that version in its `ETag`:

```json
{
  "message": "Dashboard 'd7e246cb-ab02-4da4-8f47-f9fa3e061d6b' has been modified since you loaded it (you required version [3], the current version is 4)",
  "http_status": 412,
  "currentVersion": 4,
  "dashboard": {
    "id": "d7e246cb-ab02-4da4-8f47-f9fa3e061d6b",
    "title": "Performance overview",
    "description": "MCP traffic health",
    "filters": [],
    "timeRange": { "type": "relative", "period": "24h" },
    "widgets": [],
    "version": 4,
    "createdAt": 1730000000000,
    "updatedAt": 1730700000000
  }
}
```

Use `dashboard` to show the author the state they were about to overwrite, and `currentVersion` as the `If-Match` value of a retry.

To overwrite deliberately, send `If-Match: *`. The write then applies over whatever version is current:

```bash
curl -s -u "$AUTH" -X PUT "$GAMMA/dashboards/d7e246cb-ab02-4da4-8f47-f9fa3e061d6b" \
  -H 'Content-Type: application/json' \
  -H 'If-Match: *' \
  -d '{ "title": "Performance overview", "filters": [], "widgets": [] }'
```

An overwrite never restores a deleted dashboard: the request returns `404` when the dashboard no longer exists. Combining `*` with a specific validator is rejected with `400`, because the two state different intents.

## Delete a dashboard

```bash
curl -s -u "$AUTH" -X DELETE "$GAMMA/dashboards/d7e246cb-ab02-4da4-8f47-f9fa3e061d6b"
```

The response is `204 No Content`. The deletion is permanent, with no undo and no soft delete. Recreate the dashboard with `POST` if you need it back.

Deleting an environment removes the dashboards saved in it.

## Environment isolation

Every call resolves the dashboard within the environment in the URL. A dashboard that belongs to another environment returns `404 Not Found` on read, update, and delete, rather than `403`, so nothing reveals that the identifier exists elsewhere. The list endpoint returns only the dashboards of the environment it's called on.
