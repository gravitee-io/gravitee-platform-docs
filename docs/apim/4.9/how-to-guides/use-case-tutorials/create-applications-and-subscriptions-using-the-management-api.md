---
description: >-
  An overview about create applications and subscriptions using the management
  api.
metaLinks:
  alternates:
    - create-applications-and-subscriptions-using-the-management-api.md
---

# Create Applications and Subscriptions Using the Management API

## Overview

This tutorial builds upon [create-and-publish-an-api-using-the-management-api.md](create-and-publish-an-api-using-the-management-api.md "mention") to perform the following tasks:

1. Remove the API's Keyless plan and add an API Key plan
2. Create an application for the consumer's identity
3. Subscribe to the API to link the consumer identity to the API
4. Verify functionality

{% hint style="info" %}
This guide uses the Management API (mAPI) v2 to manage v4 HTTP proxy APIs and subscriptions.
{% endhint %}

## Prerequisites

* Complete [create-and-publish-an-api-using-the-management-api.md](create-and-publish-an-api-using-the-management-api.md "mention") to generate the API used for this tutorial.

## Change the API's security

A Gravitee API must be associated with at least one consumer plan before it can be deployed to a Gateway.

Complete the following steps to create an API Key plan and deprecate the existing Keyless plan.

### Create the new API Key plan

1.  To create a new API Key plan using the mAPI, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans" \
         -X POST \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -d '{"definitionVersion":"V4","name":"API Key Plan","description":"Secured using API Keys","security":{"type":"API_KEY"},"mode":"STANDARD"}'
    ```

<details>

<summary>Example response</summary>

If your request is successful, the mAPI endpoint returns an `HTTP 201 Created` status and the plan's full configuration.

```json
{
  "definitionVersion" : "V4",
  "flows" : [ ],
  "id" : "d4896292-61c4-4b3d-8962-9261c46b3d9f",
  "name" : "API Key Plan",
  "description" : "Secured using API Keys",
  "apiId" : "3c054704-65cc-4415-8547-0465cce41582",
  "security" : {
    "type" : "API_KEY"
  },
  "mode" : "STANDARD",
  "characteristics" : [ ],
  "commentRequired" : false,
  "createdAt" : "2025-09-12T14:59:52.664Z",
  "excludedGroups" : [ ],
  "order" : 0,
  "status" : "STAGING",
  "tags" : [ ],
  "type" : "API",
  "updatedAt" : "2025-09-12T14:59:52.664Z",
  "validation" : "MANUAL"
}
```

</details>

2.  Capture the plan `id` from the response. You can set this plan `id` as an environment variable for use in subsequent calls. For example:

    ```sh
    export API_KEY_PLAN_ID="d4896292-61c4-4b3d-8962-9261c46b3d9f" 
    ```

### Publish the plan <a href="#id-5.-publish-the-plan" id="id-5.-publish-the-plan"></a>

1.  To publish the plan, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans/${API_KEY_PLAN_ID}/_publish" \
         -X POST \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8"
    ```

<details>

<summary>Example response</summary>

If the plan is published successfully, an `HTTP 200 OK` status is returned.

```json
{
  "definitionVersion" : "V4",
  "flows" : [ ],
  "id" : "d4896292-61c4-4b3d-8962-9261c46b3d9f",
  "name" : "API Key Plan",
  "description" : "Secured using API Keys",
  "apiId" : "3c054704-65cc-4415-8547-0465cce41582",
  "security" : {
    "type" : "API_KEY"
  },
  "mode" : "STANDARD",
  "characteristics" : [ ],
  "commentRequired" : false,
  "createdAt" : "2025-09-12T14:59:52.664Z",
  "excludedGroups" : [ ],
  "order" : 4,
  "publishedAt" : "2025-09-12T15:03:33.582Z",
  "status" : "PUBLISHED",
  "tags" : [ ],
  "type" : "API",
  "updatedAt" : "2025-09-12T15:03:33.582Z",
  "validation" : "MANUAL"
}
```

</details>

### Deprecate the existing Keyless plan <a href="#id-5.-publish-the-plan" id="id-5.-publish-the-plan"></a>

1. Obtain the Keyless plan `id` using one of the following methods:
   * Reference the plan `id` obtained from [create-and-publish-an-api-using-the-management-api.md](create-and-publish-an-api-using-the-management-api.md "mention"), or
   *   To retrieve a list of Keyless plan `id`s, run the following command:

       ```sh
       curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans?securities=KEY_LESS,KEY_LESS" \
            -X GET \
            -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
            -H "Content-Type:application/json;charset=UTF-8"
       ```

<details>

<summary>Example response</summary>

If your request is successful, an `HTTP 201 Created` status is returned. In the example response below, the Keyless Plan `id` is `581ef289-35b6-4bb2-9ef2-8935b64bb2a6`.

```json
{
  "data" : [ {
    "definitionVersion" : "V4",
    "id" : "581ef289-35b6-4bb2-9ef2-8935b64bb2a6",
    "name" : "keyless",
    "description" : "",
    "apiId" : "3c054704-65cc-4415-8547-0465cce41582",
    "security" : {
      "type" : "KEY_LESS",
      "configuration" : { }
    },
    "mode" : "STANDARD",
    "characteristics" : [ ],
    "commentMessage" : "",
    "commentRequired" : false,
    "createdAt" : "2025-09-12T14:02:01.378Z",
    "excludedGroups" : [ ],
    "generalConditions" : "",
    "order" : 3,
    "publishedAt" : "2025-09-12T14:02:04.627Z",
    "status" : "PUBLISHED",
    "tags" : [ ],
    "type" : "API",
    "updatedAt" : "2025-09-12T14:02:04.627Z",
    "validation" : "MANUAL"
  } ]
}
```

</details>

2.  Capture the Keyless plan `id` from the response. You can set this plan `id` as an environment variable for use in subsequent calls. For example:

    ```sh
    export KEYLESS_PLAN_ID="581ef289-35b6-4bb2-9ef2-8935b64bb2a6" 
    ```
3.  To delete the Keyless plan, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans/${KEYLESS_PLAN_ID}" \
         -X DELETE \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8"     
    ```

    If the plan is deleted successfully, an `HTTP 204 No Content` status is returned.

### Redeploy the API configuration <a href="#id-5.-publish-the-plan" id="id-5.-publish-the-plan"></a>

1.  To redeploy the updated API configuration to the Gateway, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/deployments" \
         -X POST \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8"
    ```

    If the API redeployment is successful, an `HTTP 202 Accepted` status is returned.

## Create an Application

{% hint style="info" %}
You can opt to use an existing application instead of creating a new one.
{% endhint %}

1.  To create a new application to hold the consumer's identity, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/organizations/DEFAULT/environments/DEFAULT/applications" \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X POST \
         -d '{"name":"My Application 1","description":"An example application to record subscriptions to APIs"}'
    ```

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>To create an application, you must use the mAPI v1.</p></div>

Example response

If the application is created successfully, an `HTTP 201 Created` status is returned.

```json
{
  "id" : "4984c004-39e1-4ca1-84c0-0439e13ca1a9",
  "name" : "My Application 1",
  "description" : "An example application to record subscriptions to APIs",
  "environmentId" : "DEFAULT",
  "status" : "ACTIVE",
  "type" : "SIMPLE",
  "created_at" : 1757690270995,
  "updated_at" : 1757690270995,
  "api_key_mode" : "UNSPECIFIED",
  "owner" : {
    "id" : "dbb5eb4c-3fdg-4f5d-b5db-4d3fdb0f5de5",
    "displayName" : "admin",
    "type" : "USER"
  }
}  
```

2.  Capture the application `id` from the response. You can set this application `id` as an environment variable for use in subsequent calls. For example:

    ```sh
    export APPLICATION_ID="4984c004-39e1-4ca1-84c0-0439e13ca1a9"
    ```

## Subscribe to the API

A valid subscription links the application to the API Key plan. This enables authentication and lets you make API requests using the API Key.

1.  To create a new subscription, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/subscriptions" \
         -X POST \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -d '{"applicationId":"${APPLICATION_ID}","planId":"${API_KEY_PLAN_ID}"}'
    ```

<details>

<summary>Example response</summary>

If the subscription is created successfully, an `HTTP 201 Created` status is returned.

```json
{
  "id" : "3a1fb667-0642-44ea-9fb6-670642e4eac8",
  "api" : {
    "id" : "3c054704-65cc-4415-8547-0465cce41582"
  },
  "plan" : {
    "id" : "d4896292-61c4-4b3d-8962-9261c46b3d9f"
  },
  "application" : {
    "id" : "4984c004-39e1-4ca1-84c0-0439e13ca1a9"
  },
  "metadata" : { },
  "status" : "ACCEPTED",
  "consumerStatus" : "STARTED",
  "processedBy" : {
    "id" : "dbb5db4c-3fdb-4f5d-b5db-4c3fdb9f5de5"
  },
  "subscribedBy" : {
    "id" : "dbb5db4c-3fdb-4f5d-b5db-4c3fdb9f5de5"
  },
  "processedAt" : "2025-09-12T15:36:42.407Z",
  "startingAt" : "2025-09-12T15:36:42.407Z",
  "createdAt" : "2025-09-12T15:36:42.351Z",
  "updatedAt" : "2025-09-12T15:36:42.407Z",
  "origin" : "MANAGEMENT"
}
```

</details>

2.  Capture the subscription `id` from the response. You can set this subscription `id` as an environment variable for use in subsequent calls. For example:

    ```sh
    export SUBSCRIPTION_ID="3a1fb667-0642-44ea-9fb6-670642e4eac8"
    ```
3.  To retrieve the autogenerated API Key from the subscription, run the following command:

    ```sh
    curl "https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/subscriptions/${SUBSCRIPTION_ID}/api-keys" \
         -X GET \
         -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}"
    ```

<details>

<summary>Example response</summary>

In this example, the API Key is `3c1da7be-bd10-464f-9da7-bebd10d64fee`.

```json
{
  "data" : [ {
    "id" : "24904132-4041-475f-9041-324041775fd3",
    "key" : "3c1da7be-bd10-464f-9da7-bebd10d64fee",
    "application" : {
      "id" : "4984c004-39e1-4ca1-84c0-0439e13ca1a9",
      "name" : "My Application 1",
      "description" : "An example application to record subscriptions to APIs",
      "type" : "SIMPLE",
      "primaryOwner" : {
        "id" : "dbb5db4c-3fdb-4f5d-b5db-4c3fdb9f5de5",
        "displayName" : "admin",
        "type" : "USER"
      }
    },
    "subscriptions" : [ {
      "id" : "3a1fb667-0642-44ea-9fb6-670642e4eac8"
    } ],
    "revoked" : false,
    "paused" : false,
    "expired" : false,
    "createdAt" : "2025-09-12T15:36:42.407Z",
    "updatedAt" : "2025-09-12T15:36:42.407Z"
  } ]
} 
```

</details>

4.  Capture the API Key `data[0].key` from the response. You can set this API Key as an environment variable for use in subsequent calls. For example:

    ```sh
    export API_KEY="3c1da7be-bd10-464f-9da7-bebd10d64fee"
    ```

## Test and Confirm

1.  To verify the API Key authentication, run the following command:

    ```sh
    curl "https://${GATEWAY_URL}/myfirstapi" \
         -X POST \
         -H "X-Gravitee-Api-Key: ${API_KEY}"
    ```

<details>

<summary>Example successful response</summary>

A successful response shows a match between the provided and stored API Keys.

```json
{
    "headers": {
        "Host": "api.gravitee.io",
        "Accept": "*/*",
        "Postman-Token": "11a0ce89-4e68-4c00-bc73-571c78788fd1",
        "User-Agent": "PostmanRuntime/7.46.0",
        "X-Gravitee-Api-Key": "3c1da7be-bd10-464f-9da7-bebd10d64fee",
        "X-Gravitee-Request-Id": "aa38ca36-1828-4b2d-b8ca-361828fb2dbd",
        "X-Gravitee-Transaction-Id": "dab113f5-b678-4666-b113-f5b678866631",
        "accept-encoding": "deflate, gzip"
    },
    "query_params": {},
    "bodySize": 0
} 
```

</details>

<details>

<summary>Example failure response</summary>

An authentication failure occurs when the API Key is missing or incorrect.

```json
{
    "message": "Unauthorized",
    "http_status_code": 401
} 
```

</details>
