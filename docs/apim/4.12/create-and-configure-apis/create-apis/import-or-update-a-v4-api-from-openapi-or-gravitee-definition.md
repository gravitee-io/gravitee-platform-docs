# Import or Update a V4 API from OpenAPI or Gravitee Definition

## Overview

This guide explains how to create or update V4 APIs by importing OpenAPI specifications or Gravitee API definitions. The import wizard supports both local file uploads and remote URL fetching, with optional policy and documentation generation.

## Key Concepts

### Import Formats

The import wizard supports two primary formats for API creation and update operations.

**Gravitee Definition** imports use JSON-formatted Gravitee API definitions (V4 only) and preserve all Gravitee-specific configuration including flows, policies, plans, and properties.

**OpenAPI** imports accept YAML or JSON OpenAPI specifications and automatically generate API paths, flows, and optional [oas-validation](../apply-policies/policy-reference/oas-validation.md) policies from the specification.

| Format | File Extensions | Source Modes | Generated Artifacts |
|:-------|:----------------|:-------------|:--------------------|
| Gravitee Definition | json | Local, Remote | None (full definition provided) |
| OpenAPI | yml, yaml | Local, Remote | Flows, documentation page, OAS validation policy (optional) |

### Update Matching Strategy

When updating an existing API, the system matches imported resources to existing resources using a fallback hierarchy.

**Plans** are matched first by `crossId` (if present in both import and database), then by plan `id` if no `crossId` match is found. Plans present in the database but absent from the import definition are automatically deleted.

**Pages** are matched first by `crossId`, then by `type` and `name` if no `crossId` match is found. Unmatched pages are created as new resources.

**Flows** (OpenAPI re-import only) are matched by HTTP selector key (path + alphabetically sorted methods); matching flows preserve their existing IDs, while new flows receive generated IDs.

### File Source Modes

Administrators can import API definitions from two sources.

**Local** mode accepts file uploads via drag-and-drop or file picker, with allowed extensions dynamically filtered by selected format.

**Remote** mode fetches definitions from HTTP(S) URLs, with optional authorization header support. Remote endpoints must be CORS-enabled when accessed from the Console.

## Prerequisites

Before you import or update an API, ensure the following:

* Gravitee API Management Console with V4 API support
* `API_DEFINITION[UPDATE]` permission for update operations
* For OpenAPI imports with OAS validation policy: `oas-validation` policy plugin installed
* For remote source mode: target URL must use `http:` or `https:` protocol and allow CORS requests from Console origin

## Creating or updating an API

To import or update an API, navigate to the import wizard (create mode) or open the import dialog from an existing V4 API's General Info page (update mode).

1. Select the API format: **Gravitee Definition** for full Gravitee API definitions or **OpenAPI** for OpenAPI specifications.

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-05.png" alt="Import API wizard step 1 showing API format selection with Gravitee definition, OpenAPI specification, and WSDL options"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-07.png" alt="Update API dialog from Configuration page showing format selection with Gravitee definition, OpenAPI specification, and WSDL options"><figcaption></figcaption></figure>

2. Configure the file source: choose **Local** to upload a file via drag-and-drop or file picker, or **Remote** to fetch from an HTTP(S) URL (optionally providing an authorization header).

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-06.png" alt="Import API wizard step 2 showing file source options with Local file and Remote source, and drag-and-drop area for JSON files"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-01.png" alt="Import API wizard step 2 showing file source configuration with Local file and Remote source options, and a file upload field displaying kafka-1.json"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-03.png" alt="Update API dialog showing file source configuration with Local file selected and drag-and-drop area for JSON files"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-04.png" alt="Update API dialog with file source configuration showing kafka-1.json file selected in the upload field"><figcaption></figcaption></figure>

3. (Optional) For OpenAPI imports, enable **With Documentation** to create a published documentation page from the specification, and **With OAS Validation Policy** to add an OpenAPI validation policy (if the plugin is installed).

4. Review the configuration summary and submit.

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-02.png" alt="Import API wizard step 3 review screen showing configuration summary with Gravitee definition format and Local file source"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-import-update-from-openapi-and-gravitee-definition-step-08.png" alt="Update API review screen showing configuration summary with Gravitee definition format and Local file source before updating"><figcaption></figcaption></figure>

In update mode, the system matches plans and pages using `crossId` or fallback identifiers, deletes plans absent from the import, and preserves existing properties and flow IDs where applicable. Context path conflicts with other APIs return an error.

{% hint style="warning" %}
The import operation is destructive — the imported file is the source of truth and overwrites settings, endpoints, flows, plans, pages, and metadata. The API ID and deployment state are preserved across the update.
{% endhint %}

## Verification

After importing or updating an API, verify the following:

* **General / Entrypoints / Endpoints / Plans / Flows** tabs reflect the imported configuration.
* For OpenAPI imports with **With Documentation** enabled: a new page appears under **Documentation → Pages**.
* For OpenAPI imports with **With OAS Validation Policy** enabled: the **OpenAPI Specification Validation** policy appears on the generated flows in **Policy Studio**.
* Gateway sync indicator on the API header shows the API as out-of-sync until redeployment (expected).
* Audit log entry recorded for the import or update action.

{% hint style="info" %}
If remote source mode returns a status 0 error, check that the URL is reachable and allows CORS requests from the Console.
{% endhint %}
