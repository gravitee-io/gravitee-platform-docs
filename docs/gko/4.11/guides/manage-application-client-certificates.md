### Certificate Lifecycle

Certificates transition through four states based on their `startsAt` and `endsAt` dates:

| Status | Condition |
|:-------|:----------|
| `ACTIVE` | `startsAt` is null or in the past, and `endsAt` is null |
| `ACTIVE_WITH_END` | `startsAt` is null or in the past, and `endsAt` is set |
| `SCHEDULED` | `startsAt` is in the future |
| `REVOKED` | `endsAt` is in the past |

The platform computes status automatically on every read operation.

### Fingerprint Uniqueness

Each certificate's SHA-256 fingerprint must be unique across all active applications in the same environment. The platform allows duplicate fingerprints only if the existing certificate has status `REVOKED` or belongs to an application with status `ARCHIVED`. This prevents accidental reuse of the same certificate across multiple active applications.

### Cross-Environment Identity

Every certificate receives two identifiers:

* `id`: A UUID unique to the certificate's environment
* `crossId`: A UUID that remains consistent across environment promotions

Use `crossId` when referencing certificates in multi-environment workflows.

## Prerequisites

Before you manage application certificates, ensure the following:

* The application exists and is accessible to the user.
* The user has the following permissions:
  * `APPLICATION_DEFINITION[CREATE]` to add certificates
  * `APPLICATION_DEFINITION[UPDATE]` to modify certificates
  * `APPLICATION_DEFINITION[DELETE]` to remove certificates
* The certificate is in valid PEM format (X.509).

## Overview

Client Certificate Management enables applications to store and manage X.509 client certificates for mutual TLS (mTLS) authentication. Administrators can create, update, and delete certificates with lifecycle scheduling, while the platform enforces uniqueness constraints and automatically computes certificate status based on validity periods.

### Overview

This guide explains how to manage X.509 client certificates for applications using the Gravitee REST API. Client certificates enable mutual TLS authentication and support lifecycle scheduling with automatic status computation.

### Prerequisites

Before managing client certificates, ensure the following:

* Application exists and is accessible to the user
* User has `APPLICATION_DEFINITION[CREATE]` permission to add certificates
* User has `APPLICATION_DEFINITION[UPDATE]` permission to modify certificates
* User has `APPLICATION_DEFINITION[DELETE]` permission to remove certificates
* Certificate is in valid PEM format (X.509)

### Certificate lifecycle

See [Certificate lifecycle](#certificate-lifecycle) above for details.
### Fingerprint uniqueness

See [Fingerprint uniqueness](#fingerprint-uniqueness) above for details.
### Cross-environment identity

See [Cross-environment identity](#cross-environment-identity) above for details.
### Create a client certificate

1. Send a POST request to `/applications/{application}/certificates` with the following JSON body:

    ```json
    {
      "name": "string (required, max 255 chars)",
      "startsAt": "date (optional)",
      "endsAt": "date (optional)",
      "certificate": "string (required, PEM format)"
    }
    ```

    The platform performs the following steps:
    1. Parses the PEM certificate and extracts subject, issuer, expiration, and fingerprint
    2. Validates that the fingerprint is not already used by another active application in the environment
    3. Stores the certificate with a computed status
    4. Returns the full certificate object with generated `id` and `crossId`

    If `startsAt` is null, the certificate becomes available immediately for current and future subscriptions.

### Update certificate metadata

1. Send a PUT request to `/applications/{application}/certificates/{certId}` with the following JSON body:

    ```json
    {
      "name": "string (required, max 255 chars)",
      "startsAt": "date (optional)",
      "endsAt": "date (optional)"
    }
    ```

    The certificate PEM itself cannot be modified—only metadata. The platform recomputes status based on the new date values and returns the updated certificate object.

### List and filter certificates

1. Send a GET request to `/applications/{application}/certificates?page={page}&size={size}`.

    Page numbers are 1-based (use `?page=1` for the first page). The response includes total count, page metadata, and an array of certificate objects.

2. (Optional) Filter by status using query parameters to retrieve only `ACTIVE`, `SCHEDULED`, `ACTIVE_WITH_END`, or `REVOKED` certificates.

### Restrictions

* Certificate PEM content cannot be updated after creation; delete and recreate to replace
* Fingerprint uniqueness is enforced only for active applications (`ARCHIVED` applications excluded)
* Certificates with status `REVOKED` do not block fingerprint reuse
* Maximum certificate name length is 255 characters
* All certificates for an application are deleted when the application is deleted
* Page numbers in API requests are 1-based (repository layer converts to 0-based internally)

### Prerequisites

See [Prerequisites](#prerequisites) above for details.
### Gateway Configuration

### Creating a Client Certificate

To create a certificate, send a POST request to `/applications/{application}/certificates` with a JSON body containing `name`, `certificate` (PEM format), and optional `startsAt` and `endsAt` dates. The platform parses the PEM certificate and extracts subject, issuer, expiration, and fingerprint. It validates that the fingerprint is not already used by another active application in the environment. If validation passes, the certificate is stored with a computed status. The response includes the full certificate object with generated `id` and `crossId`. If `startsAt` is null, the certificate becomes available immediately for current and future subscriptions.

### Updating Certificate Metadata

Update a certificate by sending a PUT request to `/applications/{application}/certificates/{certId}` with `name`, `startsAt`, and `endsAt` fields. The certificate PEM itself cannot be modified—only metadata. The platform recomputes status based on the new date values and returns the updated certificate object.

### Listing and Filtering Certificates

Retrieve certificates with GET `/applications/{application}/certificates?page={page}&size={size}`. Page numbers are 1-based (use `?page=1` for the first page). The response includes total count, page metadata, and an array of certificate objects. Filter by status using query parameters to retrieve only ACTIVE, SCHEDULED, ACTIVE_WITH_END, or REVOKED certificates.

### Restrictions

See [Restrictions](#restrictions) above for details.
### REST API Endpoints

The platform exposes five endpoints under `/applications/{application}/certificates`:

| Method | Path | Description | Permission Required |
|:-------|:-----|:------------|:-------------------|
| GET | `/applications/{application}/certificates` | List client certificates for an application (paginated) | `APPLICATION_DEFINITION[READ]` |
| POST | `/applications/{application}/certificates` | Create a client certificate for an application | `APPLICATION_DEFINITION[CREATE]` |
| GET | `/applications/{application}/certificates/{certId}` | Get a single client certificate | `APPLICATION_DEFINITION[READ]` |
| PUT | `/applications/{application}/certificates/{certId}` | Update a client certificate | `APPLICATION_DEFINITION[UPDATE]` |
| DELETE | `/applications/{application}/certificates/{certId}` | Delete a client certificate | `APPLICATION_DEFINITION[DELETE]` |

### Database Schema

Client certificates are stored in a `client_certificates` table (JDBC) or collection (MongoDB) with the following indexes:

**JDBC Indexes:**
* `idx_{prefix}client_certificates_application_id` on `application_id`
* `idx_{prefix}client_certificates_environment_id` on `environment_id`
* `idx_{prefix}client_certificates_app_id_status` on `(application_id, status)`

**MongoDB Indexes:**
* `a1`: `{ applicationId: 1 }`
* `e1`: `{ environmentId: 1 }`
* `f1`: `{ fingerprint: 1 }`
* `s1`: `{ status: 1 }`

Application deletion cascades to client certificates via `deleteByApplicationId`.

### Error Codes

The API returns structured error responses with technical codes:

| Error Code | HTTP Status | Description |
|:-----------|:------------|:------------|
| `clientCertificate.notFound` | 404 | Certificate ID not found |
| `clientCertificate.alreadyUsed` | 400 | Fingerprint already used by another active application |

**Example Error Response:**
```json
{
  "message": "Client certificate [abc123] cannot be found.",
  "technicalCode": "clientCertificate.notFound",
  "parameters": { "clientCertificate": "abc123" }
}
```
