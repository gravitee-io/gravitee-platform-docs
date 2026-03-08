### Prerequisites

Before managing client certificates via API, ensure the following:

* The application exists in the environment
* You have `APPLICATION_DEFINITION[CREATE]` permission to add certificates
* You have `APPLICATION_DEFINITION[UPDATE]` permission to modify certificates
* You have `APPLICATION_DEFINITION[DELETE]` permission to remove certificates
* The certificate is in valid X.509 PEM format

### Gateway Configuration

<!-- EMPTY: Gateway Configuration -->

### Creating a Client Certificate

To create a certificate, send a POST request to `/applications/{application}/certificates` with a JSON body.

**Required fields:**

* `name` (string, max 255 characters)
* `certificate` (string, PEM format)

**Optional fields:**

* `startsAt` (date)
* `endsAt` (date)

The gateway processes the request in four steps:

1. **PEM parsing**: The gateway parses the PEM block to extract subject, issuer, and expiration metadata.
2. **Fingerprint computation and uniqueness check**: The gateway computes a SHA-256 fingerprint and checks for uniqueness across active applications in the environment. Certificates with `REVOKED` status and applications with `ARCHIVED` status are excluded from this check.
3. **Validation and storage**: If validation passes, the certificate is stored with a computed status (`ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, or `REVOKED`) and a unique `id` and `crossId` (UUID for cross-environment tracking).
4. **Response with metadata**: The response includes all certificate metadata: `id`, `crossId`, `applicationId`, `name`, `startsAt`, `endsAt`, `createdAt`, `updatedAt`, `certificate` (PEM), `certificateExpiration`, `subject`, `issuer`, `fingerprint`, `environmentId`, `organizationId`, and `status`.

### Updating a Client Certificate

To update a certificate's metadata, send a PUT request to `/applications/{application}/certificates/{certId}` with `name`, `startsAt`, and `endsAt` fields.

The certificate content itself cannot be modified. To replace a certificate, create a new one and delete the old one after the grace period.

Updates to `startsAt` or `endsAt` trigger status recalculation, potentially transitioning the certificate between `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, and `REVOKED` states.

### Deleting a Client Certificate

To remove a certificate, send a DELETE request to `/applications/{application}/certificates/{certId}`.

Deletion is immediate and cannot be undone. If the application is deleted, all associated certificates are automatically removed via cascade deletion.

### Listing Certificates

To retrieve all certificates for an application, send a GET request to `/applications/{application}/certificates`.

Results are paginated with 1-indexed page numbers (e.g., `?page=1`). The gateway converts user-facing page numbers to 0-indexed repository queries internally.

Each certificate in the response includes full metadata: `id`, `crossId`, `applicationId`, `name`, `startsAt`, `endsAt`, `createdAt`, `updatedAt`, `certificate` (PEM), `certificateExpiration`, `subject`, `issuer`, `fingerprint`, `environmentId`, `organizationId`, and `status`.

### Restrictions

* Certificate fingerprints (SHA-256) must be unique across active applications in the same environment
* Certificate content cannot be updated after creation — rotation requires creating a new certificate and deleting the old one
* Certificates must be in valid X.509 PEM format
* `name` field is limited to 255 characters
* Pagination uses 1-indexed page numbers in API requests, converted to 0-indexed internally
* Certificates with `REVOKED` status are excluded from uniqueness checks
* Applications with `ARCHIVED` status are excluded from uniqueness checks
* Deleting an application cascades to all associated certificates
