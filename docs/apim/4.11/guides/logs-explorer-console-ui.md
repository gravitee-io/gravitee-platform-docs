### Console UI

The Console UI introduces a new Logs Explorer page at `/logs-explorer` with a filter bar, paginated logs table, and side-drawer detail view.

#### Logs Table

The logs table displays one row per connection with the following columns:

| Column | Description |
|:-------|:------------|
| Timestamp | Clickable link to open detail drawer |
| API | API name |
| Type | API type indicator |
| Application | Application name |
| Method | HTTP method (displayed as colored badge) |
| Path | Request URI |
| Status | HTTP status code (color-coded: green for <400, yellow for 400-499, red for ≥500) |
| Response Time | Gateway response time in milliseconds |
| Gateway | Gateway identifier |

Clicking a timestamp or preview icon opens the detail drawer.

#### Detail Drawer

The detail drawer displays:

* **Overview** — Timestamp, method, URI, request ID, transaction ID, remote IP, status, and response time
* **Request** — Consumer request headers/body and Gateway request headers/body
* **Response** — Consumer response headers/body and Gateway response headers/body
* **Expandable Panels** — Application, plan, and endpoint metadata

If the log ID or API ID is missing, or if the fetch fails, an error banner is displayed.

#### Filter Bar

The filter bar includes:

* Time range selection
* "More Filters" button to open the filter panel
* Refresh button

#### More Filters Panel

The More Filters panel provides the following filters:

* Entrypoints
* HTTP Methods
* Plans (multi-select, only shown when exactly one API is selected)
* Transaction ID (text input, UUID format, max 36 characters)
* Request ID (text input, UUID format, max 36 characters)
* URI (text input, max 2048 characters, no invalid characters)
* Response Time (number input, min 0)
* Error Types

Validation rules:

* Transaction ID and Request ID must be valid UUIDs
* Response Time must be ≥ 0
* URI must not contain invalid characters

The Apply button is disabled when the form is invalid.

#### Name Resolution

Name resolution for APIs, applications, plans, and gateways is performed client-side by fetching metadata from their respective endpoints. If resolution fails, the ID is displayed as a fallback.

Application ID `1` is treated as the default keyless application and displayed as "Unknown application (keyless)".

#### OpenAPI Documentation

The OpenAPI documentation is published at `/openapi/index-logs.html` using the Stoplight Elements renderer.
