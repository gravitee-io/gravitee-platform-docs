---
description: An overview about management api reference.
---

# Management API Reference

## Overview

The Gravitee Management API is the programmatic interface to the Gravitee APIM backend. The Management API consists of two main subcomponents:

* The **management** component. This component exposes the core functionality of APIM. For example, creating APIs, deploying APIs to the gateway, and analytics.
* The **portal** component. This component exposes endpoints for listing and managing APIs and applications in Gravitee's Developer Portal UI. Also, you can use the portal API endpoints to build custom developer portals.

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
