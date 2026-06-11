# Conditional Updates for Plans

## Creating Conditional Update Workflows

To implement conditional updates, retrieve the plan's current ETag, then include it in the `If-Match` header when performing mutating operations. The following example demonstrates the round-trip flow:

```http
# 1. Retrieve the plan and its ETag
GET /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
→ 200 OK
→ ETag: "1705314645123"
→ Last-Modified: Mon, 15 Jan 2024 10:30:45 GMT
```

```http
# 2. Update the plan with the retrieved ETag
PATCH /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
If-Match: "1705314645123"
Content-Type: application/merge-patch+json

{"description": "Updated description"}

→ 200 OK
→ ETag: "1705314678456"   # New ETag after successful update
```

If another client modifies the plan between steps 1 and 2, the server rejects the update:

```http
PATCH /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
If-Match: "1705314645123"   # Stale ETag
Content-Type: application/merge-patch+json

{"description": "Updated description"}

→ 412 Precondition Failed
```

A `412` response does not include a fresh ETag. The client must re-fetch the plan to obtain the current version before retrying.

Omitting the `If-Match` header (or sending `If-Match: *`) skips the concurrency check entirely, implementing last-write-wins behavior identical to PUT operations.

### Response Header Reference

| Header | Description | Example |
|:-------|:------------|:--------|
| **ETag** | Opaque quoted string identifying the plan version. Derived from the plan's `updatedAt` timestamp as epoch milliseconds. Use this value in `If-Match` headers for conditional requests. | `"1705314645123"` |
| **Last-Modified** | Plan's last-updated timestamp in RFC 7231 HTTP-date format (one-second resolution). Informational only; do not use for conditional requests due to precision loss. | `Mon, 15 Jan 2024 10:30:45 GMT` |
