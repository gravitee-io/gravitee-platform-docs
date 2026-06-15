# mTLS certificate management API reference

This page lists the REST endpoints used to manage application client certificates for mTLS authentication. There are two API surfaces:

- **Management API v1** is used by administrators and integrations that authenticate against the Management Console.
- **Portal API** is used by the new Developer Portal when application owners manage their own certificates.

Both APIs operate on the same underlying client certificates and share the same validation rules, but they have different base URLs and different permission requirements.

## Management API v1

Base path: `/management/v1/organizations/{orgId}/environments/{envId}`

### Certificate Management

| Method | Path | Description | Permission |
|:-------|:-----|:------------|:-----------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination. | `APPLICATION_DEFINITION[READ]` |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate. | `APPLICATION_DEFINITION[CREATE]` |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Parse and validate a PEM certificate without persisting it. | `APPLICATION_DEFINITION[READ]` |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate. | `APPLICATION_DEFINITION[READ]` |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update a certificate's name or activation window. | `APPLICATION_DEFINITION[UPDATE]` |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate. | `APPLICATION_DEFINITION[DELETE]` |

#

## Portal API

Base path: `/portal/environments/{envId}/applications/{applicationId}/certificates`

The Portal API is the one called by the new Developer Portal. It exposes the same operations but the create, update, and delete operations all check for `APPLICATION_DEFINITION[UPDATE]`, so an application owner with `READ` and `UPDATE` on the application can perform every certificate management action through the Developer Portal.

| Method | Path | Description | Permission |
|:-------|:-----|:------------|:-----------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination. | `APPLICATION_DEFINITION[READ]` |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate. | `APPLICATION_DEFINITION[UPDATE]` |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Parse and validate a PEM certificate without persisting it. | `APPLICATION_DEFINITION[READ]` |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate. | `APPLICATION_DEFINITION[READ]` |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update a certificate's name or activation window. | `APPLICATION_DEFINITION[UPDATE]` |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate. | `APPLICATION_DEFINITION[UPDATE]` |

## Certificate properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Certificate display name. Required. Maximum 255 characters. | `production-client-cert` |
| `certificate` | PEM-encoded certificate body. Required. | `-----BEGIN CERTIFICATE-----...` |
| `startsAt` | ISO 8601 date when the certificate becomes eligible to authenticate subscriptions. If null, the certificate is active immediately. | `2026-01-15T00:00:00Z` |
| `endsAt` | ISO 8601 date when the certificate is automatically revoked. If null, the certificate stays active until explicitly deleted or its X.509 expiration date passes. | `2027-01-15T00:00:00Z` |

## Restrictions

- The certificate body must be a valid X.509 certificate in PEM format. CA certificates are rejected.
- If the PEM contains a chain, only the first certificate is stored.
- The certificate name can't be longer than 255 characters.
- The grace period end date on the previously active certificate can't be later than that certificate's own X.509 expiration date.
- Deleting the last active certificate of an application that still has active mTLS subscriptions returns HTTP 400.
- Uploading a PEM whose SHA-256 fingerprint is already in use by a non-revoked certificate on another active application in the same environment returns HTTP 400.
- Certificate validation runs server-side before creation. Invalid PEM content returns HTTP 400.

## Related pages

- [mTLS certificate management for applications](../../secure-and-expose-apis/applications/mtls-certificate-management-for-applications-overview-and-concepts.md)
- [Configure mTLS certificate management (administrator guide)](../../developer-portal/new-developer-portal/configuring-mtls-certificate-management-administrator-guide.md)
- [Create and manage mTLS certificates (application owner guide)](../../developer-portal/new-developer-portal/creating-and-managing-mtls-certificates-application-owner-guide.md)
