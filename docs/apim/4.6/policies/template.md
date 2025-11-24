---
description: Configuration guide for ---.
hidden: true
---

# Template

### Phases <a href="#user-content-phases" id="user-content-phases"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          | X                | X                 |

### Description <a href="#user-content-description" id="user-content-description"></a>

A policy template to fork and use as a quick starter.

This policy will compare `X-Template-Policy` header value with its configuration `errorKey` field, if both values are equal, then the policy will interrupt the request with a failure execution error.

Implements `TemplatePolicy#onRequest(HttpExecutionContext context)` and `TemplatePolicy#onResponse(HttpExecutionContext context)` to develop your own policy.

| Note | This policy is designed to work with at least APIM 4.0.0. |
| ---- | --------------------------------------------------------- |

#### AM and APIM V2 API compatibility <a href="#user-content-am-and-apim-v2-api-compatibility" id="user-content-am-and-apim-v2-api-compatibility"></a>

To develop a policy working with AM or a v2 definition of an API in APIM, please follow [the v3 example implementation of the policy](https://github.com/gravitee-io/gravitee-policy-template/blob/main/src/main/java/io/gravitee/policy/template/v3/TemplatePolicyV3.java).

### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property | Required | Description                                                                  | Type   | Default   |
| -------- | -------- | ---------------------------------------------------------------------------- | ------ | --------- |
| errorKey | X        | Policy will fail if header `X-Template-Policy` value is equal to this field. | string | "failure" |

Example configuration:

```
{
    "configuration": {
        "errorKey": "value-to-fail-the-policy"
    }
}
```

### Errors <a href="#user-content-errors" id="user-content-errors"></a>

With the provided default implementation, policy will fail if header `X-Template-Policy` value is equal to configured `errorKey` value.

| Phase    | Code                          | Error template key           | Description                     |
| -------- | ----------------------------- | ---------------------------- | ------------------------------- |
| REQUEST  | `400 - BAD REQUEST`           | POLICY\_TEMPLATE\_ERROR\_KEY | An error occurs during request  |
| RESPONSE | `500 - INTERNAL SERVER ERROR` | POLICY\_TEMPLATE\_ERROR\_KEY | An error occurs during response |
