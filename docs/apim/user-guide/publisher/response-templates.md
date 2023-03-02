# response-templates

## Overview

You can use response templates to override the default values sent in response to consumer calls to an API.

Response template overrides are triggered by _error keys_, which are specific to policies. Each response template defines the new values to be returned for one or more status codes when the template is triggered.

For the full list of policy error keys for which you can override the values, see the \[???]\(#Policy error keys you can override) table below.

### Global response templates

As well as creating templates associated with a specific error key, you can create two types of global templates for an API:

* Templates with a template key of `DEFAULT`, which are always triggered, regardless of the error key
* Templates with one of a set of error keys which are not policy-specific and are triggered in specific circumstances, such as an invalid request or response (designated in \[???]\(#Policy error keys you can override) as applying to all policies)

## Before you begin

Before you can define response templates for your API, you need to know:

* which policies are defined in the API plans associated with your API (see link:\{{ _/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html_ | relative\_url \}}\[Plans and subscriptions^])
* which error keys you can override for the policies associated with your API plans (see \[???]\(#Policy error keys you can override))

## Configure a response template

You can define:

* multiple templates for one API (for multiple policies and/or multiple error keys sent by the same policy)
* multiple template definitions for the same error key in a single template (for different content types or status codes)

To configure a response template:

1. link:\{{ _/apim/3.x/apim\_quickstart\_console\_login.html_ | relative\_url \}}\[Log in to APIM Console^].
2. Click **APIs** and select the API.
3. Click **Proxy > Response Templates**.
4. Click the plus icon image:\{% link images/icons/plus-icon.png %\}\[role="icon"] to add a new template.
5. Select the **Template key**. This can be either:
   * one of the error keys associated with the policy (see the \[???]\(#Policy error keys you can override) table below for more details)
   * `DEFAULT`, applying to all errors returned (as long as they correspond to the content type specified in the next step)
   *   one of the global error keys (keys described as applying to all policies in the \[???]\(#Policy error keys you can override) table)

       image:\{% link images/apim/3.x/api-publisher-guide/response-templates/template-key.png %\}\[]
6. To send the template override values only for JSON or XML requests, specify `JSON` or `XML` as the **Content type**. The default value `\*/*` applies to all content types.
7. Specify the status code for which the new values are sent.
8.  Specify the override values to send to the API consumer, which can be one or more of the following:

    * one or more HTTP headers to include in the response
    * body of the response

    image:\{% link images/apim/3.x/api-publisher-guide/response-templates/template-vals.png %\}\[]
9. Click **ADD A NEW REPONSE TEMPLATE** to add more templates for the same error key, then repeat the previous three steps.
10. Click **SAVE**.
11. Click the **deploy your API** link with the changes.

    image:\{% link images/apim/3.x/api-publisher-guide/response-templates/template-deploy.png %\}\[]

The next time a call triggering the error associated with your template is sent to the API, the consumer will see the override values.

## Policy error keys you can override

| Key                                                                               | Policy                                                                                          |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `API_KEY_MISSING`                                                                 | link:\{{ _/apim/3.x/apim\_policies\_apikey.html_                                                |
| relative\_url \}}\[API key]                                                       | `API_KEY_INVALID`                                                                               |
| link:\{{ _/apim/3.x/apim\_policies\_apikey.html_                                  | relative\_url \}}\[API key]                                                                     |
| `QUOTA_TOO_MANY_REQUESTS`                                                         | link:\{{ _/apim/3.x/apim\_policies\_rate\_limiting.html_                                        |
| relative\_url \}}\[Rate limiting]                                                 | `RATE_LIMIT_TOO_MANY_REQUESTS`                                                                  |
| link:\{{ _/apim/3.x/apim\_policies\_rate\_limiting.html_                          | relative\_url \}}\[Rate limiting]                                                               |
| `REQUEST_CONTENT_LIMIT_TOO_LARGE`                                                 | link:\{{ _/apim/3.x/apim\_policies\_request\_content\_limit.html_                               |
| relative\_url \}}\[Request content limit]                                         | `REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED`                                                         |
| link:\{{ _/apim/3.x/apim\_policies\_request\_content\_limit.html_                 | relative\_url \}}\[Request content limit]                                                       |
| `REQUEST_TIMEOUT`                                                                 | link:\{{ _/apim/3.x/apim\_policies\_mock.html_                                                  |
| relative\_url \}}\[Mock], link:\{{ _/apim/3.x/apim\_policies\_callout\_http.html_ | relative\_url \}}\[Callout HTTP], link:\{{ _/apim/3.x/apim\_policies\_request\_validation.html_ |
| relative\_url \}}\[Request validation]                                            | `REQUEST_VALIDATION_INVALID`                                                                    |
| link:\{{ _/apim/3.x/apim\_policies\_request\_validation.html_                     | relative\_url \}}\[Request validation]                                                          |
| `RESOURCE_FILTERING_METHOD_NOT_ALLOWED`                                           | link:\{{ _/apim/3.x/apim\_policies\_resource\_filtering.html_                                   |
| relative\_url \}}\[Resource filtering]                                            | `RBAC_INVALID_USER_ROLES`                                                                       |
| link:\{{ _/apim/3.x/apim\_policies\_role\_based\_access\_control.html_            | relative\_url \}}\[Role-based access control]                                                   |
| `RESOURCE_FILTERING_FORBIDDEN`                                                    | link:\{{ _/apim/3.x/apim\_policies\_resource\_filtering.html_                                   |
| relative\_url \}}\[Resource filtering]                                            | `RBAC_FORBIDDEN`                                                                                |
| link:\{{ _/apim/3.x/apim\_policies\_role\_based\_access\_control.html_            | relative\_url \}}\[Role-based access control]                                                   |
| `RBAC_NO_USER_ROLE`                                                               | link:\{{ _/apim/3.x/apim\_policies\_role\_based\_access\_control.html_                          |
| relative\_url \}}\[Role-based access control]                                     | `OAUTH2_MISSING_SERVER`                                                                         |
| link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                  | relative\_url \}}\[OAuth2]                                                                      |
| `OAUTH2_MISSING_HEADER`                                                           | link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                                |
| relative\_url \}}\[OAuth2]                                                        | `OAUTH2_MISSING_ACCESS_TOKEN`                                                                   |
| link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                  | relative\_url \}}\[OAuth2]                                                                      |
| `OAUTH2_INVALID_ACCESS_TOKEN`                                                     | link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                                |
| relative\_url \}}\[OAuth2]                                                        | `OAUTH2_INSUFFICIENT_SCOPE`                                                                     |
| link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                  | relative\_url \}}\[OAuth2]                                                                      |
| `OAUTH2_INVALID_SERVER_RESPONSE`                                                  | link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                                |
| relative\_url \}}\[OAuth2]                                                        | `OAUTH2_SERVER_UNAVAILABLE`                                                                     |
| link:\{{ _/apim/3.x/apim\_policies\_oauth2.html_                                  | relative\_url \}}\[OAuth2]                                                                      |
| `HTTP_SIGNATURE_INVALID_SIGNATURE`                                                | link:\{{ _/apim/3.x/apim\_policies\_http\_signature.html_                                       |
| relative\_url \}}\[HTTP Signature]                                                | `JWT_MISSING_TOKEN`                                                                             |
| link:\{{ _/apim/3.x/apim\_policies\_jwt.html_                                     | relative\_url \}}\[JWT]                                                                         |
| `JWT_INVALID_TOKEN`                                                               | link:\{{ _/apim/3.x/apim\_policies\_jwt.html_                                                   |
| relative\_url \}}\[JWT]                                                           | `JSON_INVALID_PAYLOAD`                                                                          |
| link:\{{ _/apim/3.x/apim\_policies\_json\_validation.html_                        | relative\_url \}}\[JSON validation]                                                             |
| `JSON_INVALID_FORMAT`                                                             | link:\{{ _/apim/3.x/apim\_policies\_json\_validation.html_                                      |
| relative\_url \}}\[JSON validation]                                               | `JSON_INVALID_RESPONSE_PAYLOAD`                                                                 |
| link:\{{ _/apim/3.x/apim\_policies\_json\_validation.html_                        | relative\_url \}}\[JSON validation]                                                             |
| `JSON_INVALID_RESPONSE_FORMAT`                                                    | link:\{{ _/apim/3.x/apim\_policies\_json\_validation.html_                                      |
| relative\_url \}}\[JSON validation]                                               | `GATEWAY_INVALID_REQUEST`                                                                       |
| All                                                                               | `GATEWAY_INVALID_RESPONSE`                                                                      |
| All                                                                               | `GATEWAY_OAUTH2_ACCESS_DENIED`                                                                  |
| All                                                                               | `GATEWAY_OAUTH2_SERVER_ERROR`                                                                   |
| All                                                                               | `GATEWAY_OAUTH2_INVALID_CLIENT`                                                                 |
| All                                                                               | `GATEWAY_MISSING_SECURITY_PROVIDER`                                                             |
| All                                                                               | `GATEWAY_PLAN_UNRESOLVABLE`                                                                     |
| All                                                                               | `GATEWAY_POLICY_INTERNAL_ERROR`                                                                 |
