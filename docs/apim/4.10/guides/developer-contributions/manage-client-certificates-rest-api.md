### Prerequisites

Before managing client certificates via REST API, ensure the following:

* The application exists in the target environment
* You hold `APPLICATION_DEFINITION[CREATE]` permission to add certificates
* The certificate is valid PEM-encoded X.509 format
* The certificate fingerprint does not conflict with active certificates in the same environment

### Gateway Configuration

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

The system processes the request in four steps:

1. Parses the PEM certificate and extracts subject, issuer, expiration date, and SHA-256 fingerprint
2. Checks whether the fingerprint already exists for an active application in the environment
3. If validation passes, stores the certificate with a computed status and returns full metadata including `id`, `crossId`, and parsed certificate details
4. If the fingerprint conflicts, the request fails with a `clientCertificate.alreadyUsed` error

### Updating a Client Certificate

Update a certificate by sending a PUT request to `/applications/{application}/certificates/{certId}` with `name`, `startsAt`, and `endsAt` fields:

```json
{
 "name": "string (max 255 chars, required)",
 "startsAt": "date",
 "endsAt": "date"
}
```

The certificate PEM content cannot be modified after creation. Only metadata and validity dates are editable. The system recalculates status based on the new date range and returns the updated certificate object.

### Listing and Retrieving Certificates

Retrieve all certificates for an application via GET `/applications/{application}/certificates` with query parameters:

* `page`: 1-based page number
* `size`: Items per page

The API returns a paginated response with total count and certificate metadata.

To fetch a single certificate, use GET `/applications/{application}/certificates/{certId}`. This operation requires `APPLICATION_DEFINITION[READ]` permission and returns the full certificate object including PEM content:

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

### Deleting a Client Certificate

Delete a certificate by sending a DELETE request to `/applications/{application}/certificates/{certId}`. The operation requires `APPLICATION_DEFINITION[DELETE]` permission and removes the certificate immediately. When an application is deleted, all associated certificates are automatically removed via cascade deletion.

### Restrictions

* Certificate name must not exceed 255 characters
* Certificate must be valid PEM format containing at least one X.509 certificate
* Fingerprint uniqueness is enforced only for non-REVOKED certificates within the same environment
* Certificate PEM content cannot be modified after creation (only metadata and dates)
* Pagination uses 1-based page numbers in API requests, converted to 0-based for repository layer
* Status computation does not account for certificate revocation lists or OCSP checks—only date-based logic
