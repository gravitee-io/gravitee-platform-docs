# mTLS Certificate Management API Reference

## End-User Configuration

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Validate a certificate PEM before creation |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update a certificate |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate |

### Certificate Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| **Name** | Certificate display name (required, max 256 characters) | `prod-client-cert` |
| **Certificate** | PEM-formatted certificate content (required) | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |
| **Starts At** | Optional date when certificate becomes active | `2024-01-15T00:00:00Z` |
| **Ends At** | Optional date when certificate stops being active | `2025-01-15T00:00:00Z` |
