---
description: An overview about management api reference.
metaLinks:
  alternates:
    - management-api-reference.md
---

# Management API Reference

## Overview

The Gravitee Management API is the programmatic interface to the Gravitee APIM backend. The Management API consists of two main subcomponents:

* The **Management** component. This component exposes the core functionality of APIM. For example, creating APIs, deploying APIs to the gateway, and analytics.
* The **Portal** component. This component exposes endpoints for listing and managing APIs and applications in Gravitee's Developer Portal UI. Also, you can use the Portal API endpoints to build custom developer portals.

Gravitee V4 and Federated APIs are managed within the **v2** subcomponent of the management API. You can access the v2 subcomponent through the `/management/v2` subpath.

## Documentation

To explore the API documentation, select any of the following endpoint categories to open an integrated API viewer and client. The viewer includes an option to download the API specification.

* [**/management component documentation**](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/api-alerts)**:** provides the specification for the `management` endpoints. Use this component to complete the following actions:
  * Manage V2 APIs
  * Configure applications, dictionaries, sharding tags, users, and other entities
* [**/management/v2 subcomponent documentation**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-apis/)**:** provides the specification for `management/v2` endpoints. Use this component to complete the following actions:
  * Manage V4 and Federated APIs
  * Configure multi-tenant aspects of APIM such as licenses, plugins, and OEM customization
* [**/portal component documentation**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-portal/)**:** productize APIs and manage applications and subscriptions

## Application Certificate Management

Application owners interact with certificates via the following REST endpoints:

| Method | Path | Description |
|:-------|:-----|:------------|
| `GET` | `/applications/{applicationId}/certificates?page={page}&size={size}` | List certificates with pagination |
| `POST` | `/applications/{applicationId}/certificates` | Create a new certificate |
| `POST` | `/applications/{applicationId}/certificates/_validate` | Validate a PEM certificate before upload |
| `GET` | `/applications/{applicationId}/certificates/{certId}` | Get a single certificate |
| `PUT` | `/applications/{applicationId}/certificates/{certId}` | Update a certificate |
| `DELETE` | `/applications/{applicationId}/certificates/{certId}` | Delete a certificate |

### Certificate Upload Fields

| Field | Description | Example |
|:------|:------------|:--------|
| **Name** | Certificate name (max 256 characters) | `"Production Client Cert"` |
| **Certificate (PEM)** | PEM-encoded certificate content | `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----` |
| **Active Until** | Optional expiry date (ISO 8601) | `"2025-12-31T23:59:59Z"` |

### Certificate Update Fields

| Field | Description | Example |
|:------|:------------|:--------|
| **Name** | Updated certificate name | `"Updated Cert Name"` |
| **Active Until** | Updated expiry date | `"2026-01-15T00:00:00Z"` |

### Grace Period Configuration

| Field | Description | Example |
|:------|:------------|:--------|
| **Grace Period End** | End date for the current active certificate during rotation (required when active certificates exist; must not exceed active certificate expiration) | `"2025-06-30T23:59:59Z"` |

### Restrictions

* Certificate name is limited to 256 characters
* File upload only accepts `.pem`, `.crt`, `.cer` extensions
* Grace Period End date cannot exceed the active certificate's expiration date
* Deleting the last active certificate is blocked if active **M Tls** subscriptions exist (returns HTTP 400)
* Certificate validation is performed server-side; invalid PEM format is rejected at upload time
* Feature is only available in the new Developer Portal when `portal.next.mtls.enabled` is `true`
