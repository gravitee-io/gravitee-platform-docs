### Certificate Lifecycle States

Certificates transition through four states based on their validity period:

| Status | Condition | Description |
|:-------|:----------|:------------|
| `SCHEDULED` | `startsAt` is in the future | Certificate is not yet active |
| `ACTIVE` | `startsAt` is now or past, and `endsAt` is null | Certificate is currently valid with no defined expiration |
| `ACTIVE_WITH_END` | `startsAt` is now or past, and `endsAt` is set | Certificate is currently valid with a defined expiration date |
| `REVOKED` | `endsAt` is in the past | Certificate has expired |

The system computes status automatically from `startsAt` and `endsAt` timestamps on every read operation.

### Fingerprint-Based Uniqueness

Each certificate's SHA-256 fingerprint must be unique across all active applications within an environment. The system rejects certificate creation if the fingerprint already exists for another application in states `ACTIVE`, `ACTIVE_WITH_END`, or `SCHEDULED`. Revoked certificates do not block fingerprint reuse.

When a duplicate fingerprint is detected, the system returns:

```json
{
 "message": "Validation error",
 "detailMessage": "Client certificate with fingerprint [<fingerprint>] is already used by another active application.",
 "technicalCode": "clientCertificate.alreadyUsed",
 "parameters": {
 "fingerprint": "<fingerprint>"
 }
}
```

### Cross-Environment Identity

Each certificate receives both a unique `id` (environment-scoped) and a `crossId` (organization-scoped UUID). The `crossId` enables certificate tracking across environment promotions or migrations. Cross-environment synchronization workflows are not detailed in this document.

### Automatic Cleanup

Certificates are stored at the application level and automatically deleted when their parent application is deleted.

### Prerequisites

Before creating a client certificate:

* Application must exist in the target environment
* User must hold `APPLICATION_DEFINITION[CREATE]` permission
* Certificate must be valid PEM-encoded X.509 format
* Certificate fingerprint must not conflict with active certificates in the same environment

### Creating a Client Certificate

To create a certificate, send a POST request to `/applications/{application}/certificates` with a JSON payload:

```json
{
 "name": "string (max 255 chars, required)",
 "startsAt": "date",
 "endsAt": "date",
 "certificate": "string (PEM format, required)"
}
```

**Validation Rules:**

| Field | Constraint | Error Condition |
|:------|:-----------|:----------------|
| `name` | `@NotNull`, `@Size(max=255)` | Missing or exceeds 255 characters |
| `certificate` | `@NotNull` | Missing PEM certificate |

If the certificate is invalid or does not contain at least one X.509 certificate, the system returns:

```
"Invalid PEM certificate: no certificate found"
```

**Response:**

```json
{
 "id": "string (UUID)",
 "crossId": "string (UUID for all environments)",
 "applicationId": "string",
 "name": "string",
 "startsAt": "date",
 "endsAt": "date",
 "createdAt": "date",
 "updatedAt": "date",
 "certificate": "string (PEM format)",
 "certificateExpiration": "date (from certificate itself)",
 "subject": "string",
 "issuer": "string",
 "fingerprint": "string (SHA-256 hex)",
 "environmentId": "string",
 "organizationId": "string",
 "status": "ACTIVE | ACTIVE_WITH_END | SCHEDULED | REVOKED"
}
```

### Updating a Client Certificate

To update a certificate, send a PUT request to `/applications/{application}/certificates/{certId}` with a JSON payload:

```json
{
 "name": "string (max 255 chars, required)",
 "startsAt": "date",
 "endsAt": "date"
}
```

**Validation Rules:**

| Field | Constraint | Error Condition |
|:------|:-----------|:----------------|
| `name` | `@NotNull`, `@Size(max=255)` | Missing or exceeds 255 characters |

The certificate content itself cannot be updated. To replace a certificate, delete the existing certificate and create a new one.

### Retrieving Client Certificates

To retrieve all certificates for an application, send a GET request to `/applications/{application}/certificates`. The endpoint supports pagination with 1-based page numbers (e.g., `page=1` for the first page).

To retrieve a single certificate, send a GET request to `/applications/{application}/certificates/{certId}`.

If the certificate ID is not found, the system returns:

```json
{
 "message": "Client certificate [<id>] cannot be found.",
 "technicalCode": "clientCertificate.notFound",
 "parameters": {
 "clientCertificate": "<id>"
 }
}
```

### Deleting a Client Certificate

To delete a certificate, send a DELETE request to `/applications/{application}/certificates/{certId}`.

### Permissions

| Operation | Permission Required |
|:----------|:-------------------|
| List certificates | `APPLICATION_DEFINITION[READ]` |
| Get single certificate | `APPLICATION_DEFINITION[READ]` |
| Create certificate | `APPLICATION_DEFINITION[CREATE]` |
| Update certificate | `APPLICATION_DEFINITION[UPDATE]` |
| Delete certificate | `APPLICATION_DEFINITION[DELETE]` |

## Overview

Client Certificate Management allows API administrators to associate X.509 client certificates with applications for mutual TLS authentication. Certificates are stored at the application level, validated for uniqueness within an environment, and automatically managed through lifecycle states. This feature is available through REST API endpoints and supports pagination, CRUD operations, and automatic cleanup when applications are deleted.
