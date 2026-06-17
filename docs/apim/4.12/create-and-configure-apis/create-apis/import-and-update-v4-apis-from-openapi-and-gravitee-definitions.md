---
description: Import a Gravitee v4 API definition or an OpenAPI Specification to create or update v4 APIs.
---

# Import and Update v4 APIs from OpenAPI and Gravitee Definitions

## Overview

API import and update enables you to create or update v4 APIs by importing a Gravitee v4 API definition or an OpenAPI Specification. The imported file acts as the source of truth and overwrites the existing configuration of the API, including endpoints, flows, plans, pages, and metadata. This feature is available for v4 HTTP proxy APIs, Message APIs, and Native APIs, excluding Federated APIs and Federated A2A agents.

## Key Concepts

### Import Formats

The wizard interface supports the following three import formats:

* **Gravitee v4 Definition**. This format imports a complete API configuration from a JSON or YAML file exported from Gravitee.
* **OpenAPI Specification**. This format imports an OpenAPI descriptor, which is a JSON or YAML file, and generates flows, endpoints, and optionally documentation and validation policies. This format is applicable to v4 HTTP proxy APIs only.
* **WSDL**. This format is displayed in the wizard but is currently disabled and coming soon.

<figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-01.png" alt="Import API format selection showing Gravitee definition, OpenAPI specification, and WSDL options"><figcaption></figcaption></figure>

### Import Sources

APIs can be imported from the following two sources:

* **Local file**. This source uploads a definition file from your machine by using drag-and-drop or a file picker.
* **Remote URL**. This source fetches the definition from an HTTP or HTTPS endpoint. You can optionally provide an Authorization header for authenticated sources. Remote sources require the target URL to allow CORS requests from the Management Console origin.

### Update Behavior

The import fully overwrites the API configuration. The API ID, deployment state, and origin metadata are preserved. Plans present in the database but absent from the import are deleted. Pages and flows are matched by identifier or key, and then they are updated in place. Unmatched items are removed. For OpenAPI imports that contain no Gravitee-specific properties, existing custom properties are preserved. The update is atomic, meaning it is either fully applied or rejected with validation errors.

## Prerequisites

To update an existing v4 API, you must meet the following prerequisites:

* You must have the `API_DEFINITION[UPDATE]` permission for the Management API (mAPI) or the `api-definition-c` permission for the Management Console.
* The target API must be a v4 API. v2 APIs use the legacy import dialog.
* The API origin must not be Kubernetes. The import button is disabled for Kubernetes-managed APIs.
* For OpenAPI imports with the OAS Validation policy option, the [OpenAPI Specification Validation policy](../apply-policies/policy-reference/oas-validation.md) must be installed in the API Gateway.

## Create or Update an API

To update an existing v4 API, complete the following steps:

1. On the API details page in the Management Console, open the API, and then click **Import**.
2. In the **Update API** modal, select the API format. You can select **Gravitee v4 Definition** for a complete Gravitee export or **OpenAPI Specification** for an OpenAPI descriptor.

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-07.png" alt="Select API format"><figcaption></figcaption></figure>
3. Choose the file source. You can select **Local file** to upload a `.json`, `.yml`, or `.yaml` file, or you can select **Remote URL** to fetch from an HTTP or HTTPS endpoint. You can optionally provide an Authorization header for the remote URL.

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-04.png" alt="Update API dialog from Configuration page showing file source selection with drag and drop area for JSON files"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-06.png" alt="Import API file source configuration with local file selected and drag and drop upload area showing supported JSON format"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-02.png" alt="Import API dialog showing step 2 with local file and remote source options, and file upload field displaying kafka-1.json"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-05.png" alt="Update API dialog showing local file option selected with kafka-1.json file uploaded"><figcaption></figcaption></figure>
4. For OpenAPI imports, configure the following options:
    * Enable **Create documentation page from spec** to generate a Documentation page from the imported specification.
    * Enable **Add OpenAPI Specification Validation policy** to attach the OAS Validation policy to generated flows. This option is enabled by default if the policy is installed.
5. Review the selected format, source, and options.

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-03.png" alt="Import API review screen showing configuration summary with Gravitee definition format and local file source"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-08.png" alt="Update API review screen showing Gravitee definition format and local file source before updating"><figcaption></figcaption></figure>
6. Click **Update API**. The API configuration is overwritten atomically. Validation errors are surfaced inline and prevent the update.

## Management API (mAPI)

### Update API from Gravitee Definition

**Endpoint**: `PUT /environments/{envId}/apis/{apiId}/_import/definition`

**Request Body**: A JSON object conforming to the `ExportApiV4` schema, which is a Gravitee v4 API definition.

**Response**: An updated `ApiV4` object with an HTTP 200 status code.

**Permission Required**: `API_DEFINITION[UPDATE]`

### Update API from OpenAPI Specification

**Endpoint**: `PUT /environments/{envId}/apis/{apiId}/_import/swagger`

The request body is an `ImportSwaggerDescriptor` object with the following properties:

| Property | Description | Type |
|:---------|:------------|:-----|
| `payload` | OpenAPI specification content, which is a JSON or YAML format | string |
| `withDocumentation` | Create a documentation page from the specification | boolean |
| `withOASValidationPolicy` | Add an OpenAPI Specification Validation policy to generated flows | boolean |
| `withPolicies` | Policy visitor IDs to apply during import | array of strings |
| `withPolicyPaths` | Create a flow for each path declared in the OpenAPI specification | boolean |

**Response**: An updated `ApiV4` object with an HTTP 200 status code.

**Permission Required**: `API_DEFINITION[UPDATE]`

## Restrictions

The import and update feature has the following restrictions:

* **WSDL import**. This format is displayed in the wizard, but it is currently disabled and coming soon.
* **OpenAPI updates**. OpenAPI updates are applicable to v4 HTTP proxy APIs only. Other v4 API types, such as Message APIs and Native APIs, must use the Gravitee v4 Definition format.
* **Gravitee v4 Definition updates**. Gravitee v4 Definition updates are not supported for Federated APIs or Federated A2A agents.
* **Remote URL sources**. Remote URL sources require the target server to allow CORS requests from the Management Console origin. If CORS is not allowed, the fetch fails with a status of `0` and an error message.
* **Flow ID preservation**. Flow ID preservation applies only to HTTP flows with `HttpSelector`. Flows are matched by the `{path}|{sorted_methods}` key.
* **Plan deletion**. Plans absent from the import definition are deleted, which mimics v2 promotion behavior. Closed plans are not yet supported in the import and update feature.
* **Concurrent imports**. A second import cannot be started while the first is in progress, which is enforced by UI state management.
* **Image validation**. Image validation is applied only to `apiPicture` and `apiBackground` in the Gravitee definition import endpoint. OpenAPI imports do not validate images.
* **Type matching**. The imported definition type must match the existing API type, such as proxy, message, or native. A type mismatch is rejected with an HTTP 400 status code.
* **File format matching**. The file format must match the selected API format. The Gravitee v4 Definition format requires `.json` files with the `MAPI_V2` import type. The OpenAPI Specification format requires `.yml`, `.yaml`, or `.json` files with the `SWAGGER` import type. Format mismatches trigger an error.

## Related Changes

The **Import** button on the v4 API details page is now enabled, and it opens a new **Update API** modal that reuses the v4 import wizard stepper. For v2 APIs, the button continues to open the legacy import dialog. The wizard includes four steps. These steps are select API format, configure file source, options, and review and import. The options step is shown only for OpenAPI and WSDL formats. The file picker clears the selected file when the API format changes, but it preserves the file when you navigate back within the same format or toggle options. After a successful update, the API configuration reflects the imported definition. For OpenAPI imports with documentation enabled, a new page appears under Documentation and Pages. With OAS Validation enabled, the OpenAPI Specification Validation policy appears on generated flows in Policy Studio. The API Gateway sync indicator shows the API as out-of-sync until it is redeployed, and an audit log entry is recorded for the update action.