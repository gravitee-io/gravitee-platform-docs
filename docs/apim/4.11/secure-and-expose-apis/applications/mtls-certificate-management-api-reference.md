# mTLS Certificate Management API Reference

## End-User Configuration

### Certificate Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Certificate identifier | `prod-client-cert` |
| Certificate | PEM-encoded certificate data | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |
| Starts At | Optional activation date | `2024-01-15T00:00:00Z` |
| Ends At | Optional expiration date | `2025-01-15T23:59:59Z` |

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination (default 10 per page) |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Validate a certificate PEM before creation |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Retrieve a single certificate |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update certificate name, start date, or end date |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate |

## Restrictions

- Certificate management is only available when `portal.next.mtls.enabled` is set to `true`
- Certificate upload accepts only `.pem`, `.crt`, and `.cer` file formats
- Certificate name is limited to 256 characters
- Grace period end date cannot exceed the active certificate's expiration date
- Grace period is required when uploading a certificate while an active certificate exists
- Deleting the last active certificate requires a second confirmation step
- Deleting a certificate with active **M Tls** subscriptions returns HTTP 400 and prevents deletion
- Certificate table pagination defaults to 10 items per page
