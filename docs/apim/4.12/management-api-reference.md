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

* [**/management component documentation**](https://apim-api-docs.gravitee.io/?v=4.11&api=management)**:** provides the specification for the `management` endpoints. Use this component to complete the following actions:
  * Manage V2 APIs
  * Configure applications, dictionaries, sharding tags, users, and other entities
* [**/management/v2 subcomponent documentation**](https://apim-api-docs.gravitee.io/?v=4.11&api=mgmt-v2-apis)**:** provides the specification for `management/v2` endpoints. Use this component to complete the following actions:
  * Manage V4 and Federated APIs
  * Configure multi-tenant aspects of APIM such as licenses, plugins, and OEM customization
* [**/portal component documentation**](https://apim-api-docs.gravitee.io/?v=4.11&api=portal)**:** productize APIs and manage applications and subscriptions

## Import API from Remote URL

The Management API v2 provides three endpoints for importing or updating APIs from remote URLs. All endpoints enforce whitelist validation and SSRF protection server-side.

### Create API from Remote Gravitee Definition URL

Creates a v4 API by fetching a Gravitee export from the provided URL.

**Endpoint:**

```
POST /environments/{envId}/apis/_import/definition-url
```

**Permission required:** `ENVIRONMENT_API[CREATE]`

**Request:**

* **Content-Type:** `text/plain`
* **Body:** The URL as a plain text string (e.g., `https://example.com/api-definition.json`)

**Response:** `201 Created` with `ApiV4` JSON body

The URL must be permitted by the configured import whitelist. When private-address blocking is enabled, URLs resolving to private, link-local, or loopback addresses are rejected.

### Update API from Remote Gravitee Definition URL

Updates an existing v4 API by fetching a Gravitee export from the provided URL.

**Endpoint:**

```
PUT /environments/{envId}/apis/{apiId}/_import/definition-url
```

**Permission required:** `API_DEFINITION[UPDATE]`

**Request:**

* **Content-Type:** `text/plain`
* **Body:** The URL as a plain text string

**Response:** `200 OK` with `ApiV4` JSON body

The `apiId` path parameter takes precedence over any `api.id` field in the fetched definition body. The URL must be permitted by the configured import whitelist.


