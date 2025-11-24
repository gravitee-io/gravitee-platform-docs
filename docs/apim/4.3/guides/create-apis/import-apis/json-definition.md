---
description: An overview about JSON Definition.
---

# JSON Definition

## Overview

The following sections describe the process of importing an API from its JSON definition.

### API definition

An API definition is a JSON representation of an API and its content, e.g., plans, pages, metadata, etc. You can get the API definition by exporting it from the APIM Console. Alternatively, you can use the export endpoint [`GET /apis/{api.id}/export`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/api-definition/get/organizations/{orgId}/environments/{envId}/apis/{api}/definition).

Each entity (API, plan or page) of an API definition contains a crossId and a technical ID.

{% tabs %}
{% tab title="crossId" %}
Uniquely identifies an entity (API, plan, or page) across environments. An entity will use the same `crossId` for all environments.

You can find an API using the `getApis` endpoint and the `crossId` query param: [`GET /apis?crossId=my-cross-id`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/get/organizations/{orgId}/environments/{envId}/apis).
{% endtab %}

{% tab title="Technical ID" %}
Uniquely identifies an entity in one environment only. The same entity will have a different technical ID for each environment.

The API import process uses the `crossId` to match existing entities with those in the API definition. The technical ID is not used during the import process unless the `crossId` isn’t defined, e.g., in the case of an old exported API definition.
{% endtab %}
{% endtabs %}

## Importing endpoints

Importing endpoints allows you to import an API from an API definition. The HTTP request body can contain either the JSON API definition or an HTTP link to the JSON API definition.The link requires the target organization and environment in the prefix: `/organizations/{organization.id}/environments/{environment.id}/`

### Creating a new API from an API definition

To create a new API from an API definition, use [`POST /api/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/post/organizations/{orgId}/environments/{envId}/apis/import).

*   In the API definition, set the `crossId` that will identify your API (and related entities) across environments. You can assign any string to this `crossId`.

    \{% hint style="info" %\} An error will be raised if there is already an existing API in the target environment with the same `crossId`. \{% endhint %\}
* Do not include a technical ID in your API definition. The server will automatically generate an ID for the newly created API. Even if you provide a technical ID, it will not be used.

### Updating an existing API from an API definition

To update an existing API from an API definition, use [`PUT /api/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/put/organizations/{orgId}/environments/{envId}/apis/import).

*   Including the technical ID in the URL is not mandatory. The `crossId` in your API definition will be used to find the target API. This allows you to use the same URL to update your API across all environments.

    \{% hint style="info" %\} Alternatively, you can use the URL containing the API technical ID: [`PUT /api/{api.id}/import`](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/apis/put/organizations/{orgId}/environments/{envId}/apis/{api}/import). An error will be raised if the `crossId` of your definition matches another API in the target environment. \{% endhint %\}

### API content behavior

This section describes how API content behaves during import.

{% tabs %}
{% tab title="Plans" %}
* A plan in an API definition that already exists in the target API will be updated. This will not change the status of the plan.
* A plan in an API definition that does not exist in the target API will be created.
* A plan without subscriptions that exists in the target API and does not exist in the API definition will be deleted. An error would be raised if the plan accrued subscriptions.
{% endtab %}

{% tab title="Pages" %}
* A page in an API definition that already exists in the target API will be updated.
* A page in an API definition that does not exist in the target API will be created.
* A page in a target API that is not present in the API definition will not change.
{% endtab %}

{% tab title="Groups, members, & roles" %}
How groups, members, and roles are imported depends on the installation.

* **When using the import feature to update or create an API for the same environment members:** Groups and roles can be edited, and group memberships are preserved.
* **When importing to another environment:** Groups that are unknown to the target environment will be created, but their memberships will not be preserved.
* **When importing to another environment that runs on the same APIM instance (same database):** Direct members will be preserved in the target environment.
* **When importing to another environment that runs on a separate APIM instance:** Direct members will not be preserved, and groups that are unknown to the target environment will be created without preserving their memberships.
{% endtab %}
{% endtabs %}

## CI/CD use case examples

<details>

<summary>Create your API in a development environment</summary>

Use the APIM Console.

</details>

<details>

<summary>Push your API to a production environment</summary>

*   Get your API definition by exporting it from the APIM Console or using the export endpoint. For example:

    ```bash
    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X GET \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/35a1b7d4-b644-43d1-a1b7-d4b64493d134/export
    ```
*   For each environment where you want to create your API, call the POST endpoint. For example:

    ```bash
    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X POST \
         -d '{
                "name": "my-api",
                "crossId": "3e645da6-039c-4cc0-a45d-a6039c1cc0d3",
                "version": "1",
                [....]
            }' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/import
    ```

</details>

<details>

<summary>Update your API in a production environment</summary>

* Update your API definition manually or by re-exporting the source API from the development environment.
*   For each environment where you want to update your API, call the PUT endpoint. For example:

    ```bash
    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PUT \
         -d '{
                "name": "my-updated-api",
                "crossId": "3e645da6-039c-4cc0-a45d-a6039c1cc0d3",
                "version": "1",
                [....]
            }' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]//management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/import
    ```

</details>
