# mTLS Certificate Management API Reference

## End-User Configuration

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Validate a PEM certificate before upload |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update a certificate |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate |

### Certificate Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Certificate identifier | `production-client-cert` |
| Certificate | PEM-encoded certificate content | `-----BEGIN CERTIFICATE-----...` |
| Starts At | ISO 8601 date when certificate becomes active | `2024-01-15T00:00:00Z` |
| Ends At | ISO 8601 date when certificate expires | `2025-01-15T00:00:00Z` |

## Restrictions

- mTLS certificate management UI is only available in the new Developer Portal (`portal.next`)
- Certificates must be in PEM format with `.pem`, `.crt`, or `.cer` file extensions
- Certificate name is limited to 256 characters
- Grace period end date cannot exceed the current certificate's expiration date
- Deleting the last active certificate when active mTLS subscriptions exist returns HTTP 400
- Invalid PEM content triggers HTTP 400 validation errors
- Certificate validation is performed server-side before creation
