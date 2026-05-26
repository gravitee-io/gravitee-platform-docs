# CIMD Logo Endpoint API Reference

## CIMD Logo Endpoint

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

**Query Parameters:**

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `clientId` | Yes | The canonical CIMD metadata URL |

**Response Codes:**

| Code | Description |
|:-----|:------------|
| `200 OK` | Logo retrieved successfully. Response includes `Content-Type: image/*` and `Cache-Control: max-age={seconds}` headers. |
| `404 Not Found` | Logo not cached and metadata absent or has no `logo_uri` field. |

Logos are fetched on-demand with the same SSRF protection as metadata documents and cached with the same TTL. Maximum logo size is 256 KB.
