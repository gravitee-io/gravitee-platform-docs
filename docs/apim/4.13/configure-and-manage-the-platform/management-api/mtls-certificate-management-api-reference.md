---
description: The REST endpoints that manage application client certificates for mTLS in API Management 4.13. Browse the full reference.
---

# mTLS certificate management API reference

This page lists the REST endpoints that manage the client certificates of an application for mTLS plans, and describes what the application endpoints return and accept about certificates. For the statuses, the grace period, and the automatic revocation, see [mTLS certificate management for applications](../../secure-and-expose-apis/applications/mtls-certificate-management-for-applications-overview-and-concepts.md).

Two API surfaces expose the certificates endpoints:

- **Management API** is used by the APIM Console and by integrations that authenticate against the Management Console.
- **Portal API** is used by the New Developer Portal when application owners manage their own certificates.

Both APIs operate on the same underlying client certificates and share the same validation rules, but they have different base URLs and different permission requirements.

## Management API

Base path: `/management/organizations/{orgId}/environments/{envId}/applications/{applicationId}/certificates`

| Method | Path | Description | Permission |
|:-------|:-----|:------------|:-----------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List the certificates of the application with pagination, whatever their status. | `APPLICATION_DEFINITION[READ]` |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate. | `APPLICATION_DEFINITION[CREATE]` |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Parse and validate a PEM certificate without persisting it. | `APPLICATION_DEFINITION[READ]` |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate. | `APPLICATION_DEFINITION[READ]` |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update the name or the activation window of a certificate. | `APPLICATION_DEFINITION[UPDATE]` |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate. | `APPLICATION_DEFINITION[DELETE]` |

## Portal API

Base path: `/portal/environments/{envId}/applications/{applicationId}/certificates`

The Portal API is the one called by the New Developer Portal. It exposes the same operations, but the create, update, and delete operations all check for `APPLICATION_DEFINITION[UPDATE]`. An application owner with `READ` and `UPDATE` on the application can therefore perform every certificate management action through the Developer Portal.

| Method | Path | Description | Permission |
|:-------|:-----|:------------|:-----------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List the certificates of the application with pagination, whatever their status. | `APPLICATION_DEFINITION[READ]` |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate. | `APPLICATION_DEFINITION[UPDATE]` |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Parse and validate a PEM certificate without persisting it. | `APPLICATION_DEFINITION[READ]` |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate. | `APPLICATION_DEFINITION[READ]` |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update the name or the activation window of a certificate. | `APPLICATION_DEFINITION[UPDATE]` |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate. | `APPLICATION_DEFINITION[UPDATE]` |

On the Portal API, the single-certificate endpoints answer `404` when the certificate belongs to another application.

## Request properties

The `POST` body carries the following properties. The `PUT` body carries `name`, `startsAt`, and `endsAt` only, because the content of a certificate can't be changed after creation.

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Certificate display name. Required. Maximum 255 characters. | `production-client-cert` |
| `certificate` | PEM-encoded certificate body. Required on creation. When the PEM content contains a chain, only the first certificate is kept. | `-----BEGIN CERTIFICATE-----...` |
| `startsAt` | ISO 8601 date from which the certificate is eligible to authenticate subscriptions. If null, the certificate is active immediately. | `2026-01-15T00:00:00Z` |
| `endsAt` | ISO 8601 date from which the certificate is revoked by the scheduled job of the Management API. If null, the certificate stays active until you delete it. APIM doesn't revoke a certificate when the expiration date of the certificate itself passes. | `2027-01-15T00:00:00Z` |

## Response properties

The `GET`, `POST`, and `PUT` operations return the certificate with the following properties.

| Property | Description |
|:---------|:------------|
| `id` | Identifier of the certificate. |
| `crossId` | Identifier of the certificate shared across environments. |
| `applicationId` | Identifier of the application that owns the certificate. |
| `name` | Certificate display name. |
| `startsAt`, `endsAt` | The activation window, as sent on creation or update. |
| `createdAt`, `updatedAt` | When the certificate was created and last updated. |
| `certificate` | The PEM-encoded certificate body. |
| `certificateExpiration` | The expiration date read from the certificate itself. |
| `subject`, `issuer` | The subject and issuer read from the certificate. |
| `fingerprint` | The SHA-256 fingerprint of the certificate. |
| `environmentId` | The environment in which the certificate was created. |
| `status` | `ACTIVE`, `ACTIVE_WITH_END`, `SCHEDULED`, or `REVOKED`, computed from `startsAt` and `endsAt`. |

The `_validate` operation takes a body with a single `certificate` property and returns `certificateExpiration`, `subject`, and `issuer`. It doesn't check whether the fingerprint is already in use.

## Errors

| HTTP status | `technicalCode` | Message | When |
|:------------|:----------------|:--------|:-----|
| `400` | `application.certificate.invalid` | `An error has occurred while parsing client certificate` | The PEM content can't be parsed. |
| `400` | `application.certificate.empty` | `No certificate can be extracted` | The PEM content contains no certificate. |
| `400` | `application.certificate.ca` | `Certificate Authorities are not supported, requires a client certificate` | The certificate is a certificate authority certificate. |
| `400` | `application.certificate.dates` | `Start date must be before end date` | `startsAt` isn't before `endsAt`. |
| `400` | `application.certificate.alreadyUsed` | `Client certificate with fingerprint [<fingerprint>] is already used by another active application.` | A certificate that isn't revoked, on an active application of the environment, has the same SHA-256 fingerprint. On these endpoints, a certificate that the same application already holds is rejected too. |
| `400` | `application.certificate.remove.last` | `Client certificate cannot be revoked for application '<applicationId>': active subscriptions exist, and this is the last certificate.` | The deleted certificate is the last active one and the application has accepted, pending, or paused mTLS subscriptions. |
| `404` | `application.certificate.notFound` | `Client certificate [<certId>] cannot be found.` | The certificate doesn't exist, or, on the Portal API, belongs to another application. |
| `400` | `plan.notSubscribableWithoutClientCertificate` | `You cannot subscribe to a mTLS plan without a client_certificate configured at application level` | A subscription to an mTLS plan is created for an application with no active certificate. |
| `400` | `plan.otherMtlsSubscribed` | `An other mTLS plan is already subscribed by the same application.` | The application already holds a subscription to an mTLS plan of the same API that isn't rejected or closed. |

## Certificates in the application endpoints

The application endpoints predate multiple certificates and keep the single `client_certificate` field for compatibility.

* `GET /management/organizations/{orgId}/environments/{envId}/applications/{applicationId}`: when the application holds exactly one active certificate whose name is the name of the application, which is the case of an application upgraded from APIM 4.10 or earlier, `settings.tls.client_certificate` holds its PEM content and `settings.tls.certificate_count` is `1`. In every other case, `settings.tls.client_certificates` lists the active certificates with their `name`, `certificate`, `startsAt`, and `endsAt`, `certificate_count` is their number, and `client_certificate` is empty. Scheduled and revoked certificates aren't listed.
* `GET /portal/environments/{envId}/applications/{applicationId}`: same as above, except that `client_certificate` also holds the first listed certificate when the list is used.
* `GET /management/organizations/{orgId}/environments/{envId}/applications`: for each application, `settings.tls.client_certificate` holds the most recently added active certificate, `client_certificates` is absent, and `certificate_count` is `0`. Use the certificates endpoints to list every certificate of an application.
* `POST` on the applications endpoints: `settings.tls.client_certificates` creates one certificate per entry, and each entry needs a `name`. The deprecated `settings.tls.client_certificate` creates one certificate named after the application, with no start date and no end date.
* `PUT` on an application, on the Management API and the Portal API: `settings.tls` doesn't create, update, or delete certificates. Use the certificates endpoints instead.
* `PUT` on an application through the Automation API, which GKO and Terraform use: `settings.tls.clientCertificates` replaces the certificates of the application. Certificates that aren't in the list are deleted, certificates whose name or dates changed are updated, and the others are created. Starting with APIM 4.12.20 and 4.13.0, a certificate you send is matched with the stored one by its SHA-256 fingerprint. In earlier versions, it's matched by its exact PEM text, so a certificate whose PEM text differs from the stored copy, for example in its line breaks, is treated as a new certificate and rejected with `application.certificate.alreadyUsed`.

## Related pages

- [mTLS certificate management for applications](../../secure-and-expose-apis/applications/mtls-certificate-management-for-applications-overview-and-concepts.md)
- [Configure mTLS certificate management (administrator guide)](../../developer-portal/new-developer-portal/configuring-mtls-certificate-management-administrator-guide.md)
- [Create and manage mTLS certificates (application owner guide)](../../developer-portal/new-developer-portal/creating-and-managing-mtls-certificates-application-owner-guide.md)
