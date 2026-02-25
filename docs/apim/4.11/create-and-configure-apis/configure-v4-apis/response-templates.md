---
description: An overview about response templates.
metaLinks:
  alternates:
    - response-templates.md
---

# Response Templates

## Overview

{% hint style="warning" %}
Response templates cannot override message-level errors or be applied to TCP proxy entrypoints.
{% endhint %}

You can change the default values in the response to an API call using response templates. Response templates are triggered by template keys. Response templates define the new values to be returned for one or more status codes when the template is triggered. You can implement response templates for the following v4 API HTTP entrypoints:

* HTTP GET
* HTTP POST
* HTTP proxy
* SSE
* Webhook
* WebSocket

You can apply response templates to a response if the error is associated with a policy or endpoint whose error keys can be overridden. For more information about template keys, see [#template-keys](response-templates.md#template-keys "mention").

When you create response templates, you can define templates in the following ways:

* Multiple templates for one API. You can configure response templates for multiple policies or multiple error keys that are sent by the same policy.
* Multiple template definitions for the same error key in a response template. You can configure response templates for different content types or status codes.

## Prerequisites

* A v4 API with the policy or endpoint that you want to set the response template for. For more information about creating a v4 API, see [create-an-api.md](../../getting-started/create-and-publish-your-first-api/create-an-api.md "mention").

## Create a response template

1.  From the **Dashboard**, click **APIs**. <br>

    <figure><img src="../../.gitbook/assets/image (209).png" alt=""><figcaption></figcaption></figure>
2.  Select the API that you want to configure response templates for.<br>

    <figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>
3.  From the API's menu, click **Entrypoints**.<br>

    <figure><img src="../../.gitbook/assets/9DB31EFE-6F36-4050-AD4B-5135E50E66AA.jpeg" alt=""><figcaption></figcaption></figure>
4.  Click **Response Templates**.<br>

    <figure><img src="../../.gitbook/assets/08A581A9-CB23-4B4A-89E8-B5180D4884D8.jpeg" alt=""><figcaption></figcaption></figure>
5.  Click **+ Add new Response Template**.<br>

    <figure><img src="../../.gitbook/assets/84234FCA-B6B2-47E1-9641-2E46450476BA.jpeg" alt=""><figcaption></figcaption></figure>
6. Create the response template. To create the response template, complete the following sub-steps:
   1.  From the **Template key** dropdown menu, select the Template key that you want to apply to the API. For example, `GATEWAY_PLAN_UNRESOLVABLE`. For more information about Template Keys, see [#template-keys](response-templates.md#template-keys "mention").<br>

       <figure><img src="../../.gitbook/assets/image (224).png" alt=""><figcaption></figcaption></figure>
   2. In the **Accept header to match** field, enter the request header or request headers that trigger the response template. The default value is `*/*`.
   3. In the **Status Code** field, add the status code that you want to associate with the response template. For example, `401`.&#x20;
   4. (Optional) In the **HTTP Headers** field, enter the `KEY` and `VALUE` for the response.&#x20;
   5.  (Optional) In the **Body** field, enter the body of response that you want to return to the consumer. For example, `{"error": "Custom Missing Key Message"}`.<br>

       <figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>
7.  Click **Create**. <br>

    <figure><img src="../../.gitbook/assets/EF0E884E-88BE-466F-A0F7-F73C98780115.jpeg" alt=""><figcaption></figcaption></figure>
8.  In the **This API is out of sync** pop-up banner, click **Deploy API**.<br>

    <figure><img src="../../.gitbook/assets/6A4577E6-D8C6-4A3B-8712-37A7428C9A2A.jpeg" alt=""><figcaption></figcaption></figure>
9.  In the **Deploy your API** pop-up menu, click **Deploy**.<br>

    <figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

## Verification

To verify if the complete the following steps:&#x20;

1.  Verify that the response templates appears in the **Response Templates** tab of the **Entrypoints** screen.<br>

    <figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
2.  Call your API to trigger your the error response. For example, if you set an API key plan for your API, call your API without the API key like the following example:<br>

    ```
    curl -i "http://<gateway-domain>:<gateway-port>/<api-context-path>" \
      -H "X-Gravitee-Api-Key: <your-api-key>"
    ```

    * Replace `<gateway_url>` with the URL for your Gateway.
    * Replace `<context_path>` with the context path for your API.

    \
    You receive the following message in the response:&#x20;

    ```bash
    {"error": "My custom missing key error"}% 
    ```

## Template Keys&#x20;

Here are the template keys that you can override by configuring response templates

### Global Gateway Keys

| **Template key**                | **Description**                                                                                                                                    |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GATEWAY_OAUTH2_ACCESS_DENIED`  | <p>No valid subscription can be found for the <code>clientid</code>. </p><p></p><p>This template works for only for JWT or OAuth2 plan.</p><p></p> |
| `GATEWAY_OAUTH2_INVALID_CLIENT` | No clientld found in the Execution context.                                                                                                        |
| `GATEWAY_PLAN_UNRESOLVABLE`     | The Gateway cannot resolve or authenticate a request using any available security plan and must challenge the client for authentication.           |
| `GATEWAY_POLICY_INTERNAL_ERROR` | An internal error occurs during Policies execution.                                                                                                |
| `REQUEST_TIMEOUT`               | A `http.requestTimeout` is configured to be `> 0` with and the request is not finished before that time.                                           |

### Policy-Specific Template Keys

#### API Key

| **Template key**  | **Description**                    |
| ----------------- | ---------------------------------- |
| `API_KEY_MISSING` | No API Key found in the request.   |
| `API_KEY_INVALID` | The API Key is revoked or expired. |

#### Callout HTTP

| **Template key**        | **Description**                                                                  |
| ----------------------- | -------------------------------------------------------------------------------- |
| `CALLOUT_EXIT_ON_ERROR` | The policy configuration `errorCondition` is evaluated to true.                  |
| `CALLOUT_HTTP_ERROR`    | The policy is configured with `exitonError=true` and the call out request fails. |

#### HTTP Signature

| **Template key**                   | **Description**                             |
| ---------------------------------- | ------------------------------------------- |
| `HTTP_SIGNATURE_INVALID_SIGNATURE` | The validation of the signature has failed. |

#### JSON Validation

| **Template key**                | **Description**                             |
| ------------------------------- | ------------------------------------------- |
| `JSON_INVALID_PAYLOAD`          | The request payload validation has failed.  |
| `JSON_INVALID_FORMAT`           | The request payload cannot be parsed.       |
| `JSON_INVALID_RESPONSE_PAYLOAD` | The response payload validation has failed. |
| `JSON_INVALID_RESPONSE_FORMAT`  | The response payload cannot be parsed.      |

#### JWT

| **Template key**    | **Description**                           |
| ------------------- | ----------------------------------------- |
| `JWT_MISSING_TOKEN` | The token cannot be found in the request. |
| `JWT_INVALID_TOKEN` | The token's validation has failed.        |

#### OAuth2

| **Template key**                  | **Description**                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| `OAUTH2_MISSING_SERVER`           | No OAuth2 resource is found.                                                          |
| `OAUTH2_MISSING_HEADER`           | The Authorization header is not present in the request.                               |
| `OAUTH2_MISSING_ACCESS_TOKEN`     | The token extract is empty.                                                           |
| `OAUTH2_INVALID_ACCESS_TOKEN_KEY` | The introspection of the access token is not successful.                              |
| `OAUTH2_INVALID_SERVER_RESPONSE`  | The token introspection result does not have a valid payload.                         |
| `OAUTH2_INSUFFICIENT_SCOPE`       | The scope checking is enabled and the token's scopes do not meet the required scopes. |
| `OAUTH2_SERVER_UNAVAILABLE`       | The request to introspect of the access token fails.                                  |

#### Quota Limiting

| **Template key**                | **Description**                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| `QUOTA_TOO_MANY_REQUESTS`       | The quota policy detects that the limits has been exceeded.                                  |
| `QUOTA_SERVER_ERROR`            | The rate limit service plugin is not found.                                                  |
| `QUOTA_BLOCK_ON_INTERNAL_ERROR` | An error occurs during quota processing and the error strategy is `BLOCK_ON_INTERNAL_ERROR`. |

#### Rate Limiting

| **Template key**                        | **Description**                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------- |
| RATE\_LIMIT\_TOO\_MANY\_REQUESTS        | The ratelimit policy detects that the limits has been exceeded.                                   |
| RATE\_LIMIT\_SERVER\_ERROR              | The rate limit service plugin is not found.                                                       |
| RATE\_LIMIT\_BLOCK\_ON\_INTERNAL\_ERROR | An error occurs during rate limit processing and the error strategy is `BLOCK_ON_INTERNAL_ERROR`. |

#### Spike Arrest

| **Template key**                       | **Description**                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------ |
| `SPIKE_ARREST_TOO_MANY_REQUESTS`       | The spike-arrest policy detects that the limits has been exceeded reached.                 |
| `SPIKE_ARREST_SERVER_ERROR`            | The rate limit service plugin is not found.                                                |
| `SPIKE ARREST_BLOCK_ON_INTERNAL_ERROR` | An error occurs during the processing and the error strategy is `BLOCK_ON_INTERNAL_ERROR`. |

#### Request Content Limit

| **Template key**                        | **Description**                                          |
| --------------------------------------- | -------------------------------------------------------- |
| `REQUEST_CONTENT_LIMIT_TOO_LARGE`       | The request content is higher than the limit configured. |
| `REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED` | The request does not have `Content-Length` header.       |

#### Request Validation

| **Template Key**             | **Description**                    |
| ---------------------------- | ---------------------------------- |
| `REQUEST_VALIDATION_INVALID` | The request validation has failed. |

#### Resource Filtering

| **Template Key**                        | **Description**                                          |
| --------------------------------------- | -------------------------------------------------------- |
| `RESOURCE_FILTERING_METHOD_NOT_ALLOWED` | The policy rejects the usage if the HTTP METHOD is used. |
| `RESOURCE_FILTERING_FORBIDDEN`          | The policy rejects the access to that path.              |

#### Role-Based Access Control

| **Template Key**          | **Description**                                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `RBAC_INVALID_USER_ROLES` | User roles are found but are incorrect. For example, they are not a list or a string.                      |
| `RBAC FORBIDDEN`          | User roles are present and valid, but do not match the required roles defined in the policy configuration. |
| `RBAC_NO_USER_ROLE`       | No user roles can be found in the execution context.                                                       |

***

### Endpoint-Specific Template Keys

#### Kafka

| **Template key**                         | **Description**                        |
| ---------------------------------------- | -------------------------------------- |
| `FAILURE_ENDPOINT_CONFIGURATION_INVALID` | The endpoint configuration is invalid. |
| `FAILURE_ENDPOINT_CONNECTION_CLOSED`     | The kafka connection has been closed.  |
| `FAILURE_ENDPOINT_UNKNOWN_ERROR`         | An unknown error is caught.            |

#### Solace

| **Template key**                      | **Description**                                 |
| ------------------------------------- | ----------------------------------------------- |
| FAILURE\_ENDPOINT\_CONNECTION\_FAILED | The connection to Solace cannot be established. |
| FAILURE\_ENDPOINT\_SUBSCRIBE\_FAILED  | An error occurs during message consumption.     |
| FAILURE\_ENDPOINT\_PUBLISH\_FAILED    | An error occurs when message publication.       |

#### MQTT

| **Template key**                     | **Description**                               |
| ------------------------------------ | --------------------------------------------- |
| `FAILURE_ENDPOINT_CONNECTION_FAILED` | The connection to MQTT cannot be established. |
| `FAILURE_ENDPOINT_UNKNOWN_ERROR`     | When an unknown error is caught.              |
| `FAILURE_ENDPOINT_CONNECTION_CLOSED` | The connection to MQTT has been closed.       |

#### RabbitMQ

| **Template key**                     | **Description**                                 |
| ------------------------------------ | ----------------------------------------------- |
| `FAILURE_ENDPOINT_CONNECTION_FAILED` | The connection to Rabbit cannot be established. |
| `FAILURE_ENDPOINT_UNKNOWN_ERROR`     | When an unknown error is caught.                |
