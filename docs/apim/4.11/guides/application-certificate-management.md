### Overview

Client Certificate Management allows administrators to attach X.509 certificates to applications for mutual TLS authentication. Certificates are scoped to applications within an environment and validated for uniqueness by fingerprint. The feature supports lifecycle management with scheduled activation and automatic revocation based on validity periods.

### Key Concepts

#### Certificate Lifecycle

Certificates transition through four states based on their validity dates:

* **SCHEDULED**: Certificate is not yet valid. The current date is before the `startsAt` date.
* **ACTIVE**: Certificate is valid and has no expiration date. The `endsAt` field is null.
* **ACTIVE_WITH_END**: Certificate is valid and has a defined expiration date. The current date is between `startsAt` and `endsAt`.
* **REVOKED**: Certificate has expired. The current date is after the `endsAt` date.

Status is computed dynamically when certificates are retrieved or modified.

#### Fingerprint Uniqueness

Each certificate is identified by a SHA-256 fingerprint computed from its PEM-encoded bytes. A fingerprint may only be associated with one active application per environment. Fingerprints from revoked certificates or archived applications become available for reuse. This prevents certificate sharing across active applications while allowing certificate rotation.

#### Cross-Environment Identity

Each certificate receives a `crossId` (UUID) that remains constant across all environments where the certificate is deployed. The `id` field is environment-specific, while `crossId` enables tracking the same logical certificate across development, staging, and production environments.

### Prerequisites

* Application must exist and be in `ACTIVE` state
* User must have `APPLICATION_DEFINITION[CREATE]` permission to add certificates
* Certificate must be valid X.509 format in PEM encoding
* Certificate fingerprint must not be in use by another active application in the same environment

### Gateway Configuration

### Creating a Client Certificate

To create a certificate, send a POST request to `/applications/{application}/certificates` with the certificate name, PEM-encoded certificate body, and optional validity dates.

**Request Body**

```json
{
 "name": "string (max 255 chars, required)",
 "startsAt": "date",
 "endsAt": "date",
 "certificate": "string (PEM format, required)"
}
```

**Validation and Storage Flow**

1. The system parses the certificate to extract subject, issuer, expiration date, and compute the SHA-256 fingerprint.
2. It validates that the fingerprint is not already used by another active application in the environment.
3. If validation passes, the certificate is stored with an initial status computed from the validity dates.
4. The response includes the generated `id`, `crossId`, and all extracted certificate metadata.

Certificates created without a `startsAt` date become immediately active.

**Response Body**

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
 "status": "enum (ACTIVE | ACTIVE_WITH_END | SCHEDULED | REVOKED)"
}
```

### Updating a Client Certificate

To update a certificate, send a PUT request to `/applications/{application}/certificates/{certId}` with the new name and validity dates.

**Request Body**

```json
{
 "name": "string (max 255 chars, required)",
 "startsAt": "date",
 "endsAt": "date"
}
```

**Update Flow**

1. Only the `name`, `startsAt`, and `endsAt` fields may be modified. The certificate body itself is immutable.
2. The system recomputes the status based on the new validity dates.
3. The `updatedAt` timestamp is refreshed.

To revoke a certificate before its natural expiration, set `endsAt` to a past date.

### Listing and Retrieving Certificates

#### List All Certificates

Retrieve all certificates for an application with GET `/applications/{application}/certificates`. Results are paginated using 1-based page numbers (e.g., `?page=1&size=10`). Filter by status using the repository method `findByApplicationIdAndStatuses()` to retrieve only active or scheduled certificates.

#### Retrieve a Single Certificate

Retrieve a single certificate by ID with GET `/applications/{application}/certificates/{certId}`.

All endpoints require `APPLICATION_DEFINITION[READ]` permission.

### Client Configuration

### Restrictions

* **Certificate body immutability**: The certificate body (PEM) cannot be modified after creation. Delete and recreate to rotate certificates.
* **Name length**: Maximum certificate name length is 255 characters.
* **Fingerprint uniqueness scope**: Fingerprint uniqueness is enforced only for applications in `ACTIVE` state. Archived applications release their fingerprints.
* **Cascade deletion**: Certificates are automatically deleted when the parent application is deleted.
* **Status values**: Supported status values are `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, and `REVOKED`. Custom statuses are not supported.

### Error Codes

| Error Code | Condition | Message |
|:-----------|:----------|:--------|
| `clientCertificate.alreadyUsed` | Fingerprint collision with another active application in the same environment | `"Client certificate with fingerprint [{fingerprint}] is already used by another active application."` |
| `TechnicalManagementException` | Invalid PEM format | `"Invalid PEM certificate: no certificate found"` |
| `clientCertificate.notFound` | Certificate ID not found | `"Client certificate [{id}] cannot be found."` |
