---
description: Configuration guide for status code transformation.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/status-code-transformation
---

# Status Code Transformation

### Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse |
| --------- | ---------- |
|           | X          |

### Description <a href="#user-content-description" id="user-content-description"></a>

The `status-code` policy allows you to transform the response status code sent from the upstream service to a different HTTP status code based on configured mappings.

This policy is useful when you need to present a specific status code to the client without altering the upstream service. For example, if the upstream service returns a `202 Accepted` status code but you prefer to send a `200 OK` to the client, you can configure the policy to perform this transformation.

### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

To configure the policy, define a list of status code mappings. Each mapping specifies an input status code to match and an output status code to transform it into.

The policy processes the response status code from the upstream service and, if it matches an input status code in the mappings, changes it to the corresponding output status code before sending it to the client.

If there is no matching input status code, the policy leaves the status code unchanged.

#### Configuration Properties <a href="#user-content-configuration-properties" id="user-content-configuration-properties"></a>

| Property                            | Required | Description                        | Type                                | Default |
| ----------------------------------- | -------- | ---------------------------------- | ----------------------------------- | ------- |
| `statusMappings`                    | X        | List of status code mappings       | Array of mappings                   | N/A     |
| `statusMappings[].inputStatusCode`  | X        | Input status code to match         | Integer (Standard HTTP status code) | N/A     |
| `statusMappings[].outputStatusCode` | X        | Output status code to transform to | Integer (Standard HTTP status code) | N/A     |

#### Notes <a href="#user-content-notes" id="user-content-notes"></a>

* **Input and Output Status Codes**: The status codes should be standard HTTP status codes ranging from `100` to `511`. The policy supports a predefined list of status codes.
* **Multiple Mappings for Same Input Status Code**: If multiple mappings are defined for the same input status code, the last mapping in the list takes precedence.

### Example <a href="#user-content-example" id="user-content-example"></a>

Given the following configuration:

```
{
  "statusMappings": [
    {
      "inputStatusCode": 202,
      "outputStatusCode": 200
    },
    {
      "inputStatusCode": 404,
      "outputStatusCode": 200
    },
    {
      "inputStatusCode": 500,
      "outputStatusCode": 503
    }
  ]
}
```

In this configuration:

* When the upstream service returns a `202 Accepted`, the policy transforms it to a `200 OK` before sending the response to the client.
* When the upstream service returns a `404 Not Found`, the policy transforms it to a `200 OK`.
* When the upstream service returns a `500 Internal Server Error`, the policy transforms it to a `503 Service Unavailable`.

### Limitations <a href="#user-content-limitations" id="user-content-limitations"></a>

* **Status Code Only**: The policy only modifies the response status code. It does not alter the response body or headers.
* **Status code range**: The policy only modifies HTTP status codes in the range from 100 till 599 only. For example it will not be possible to modify HTTP status code 600, or 703.
* **No Matching Mapping**: If the response status code does not match any input status code in the mappings, the original status code is retained.

### Attributes <a href="#user-content-attributes" id="user-content-attributes"></a>

This policy does not set or modify any specific attributes in the execution context.

### Errors <a href="#user-content-errors" id="user-content-errors"></a>

The `status-code` policy does not generate errors on its own. It operates silently, modifying the status code when a mapping is matched. If an exception occurs during policy execution, standard error handling mechanisms apply.

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin Version | APIM Version    |
| -------------- | --------------- |
| 1.x            | 4.2.x to latest |

### Related Information <a href="#user-content-related-information" id="user-content-related-information"></a>

* **HTTP Status Codes**: For a complete list of HTTP status codes and their meanings, refer to the [HTTP/1.1 Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).
* **Gravitee.io Documentation**: For more information on policies and API management, visit the [Gravitee.io API Management Documentation](https://docs.gravitee.io/).

### Changelog <a href="#user-content-changelog" id="user-content-changelog"></a>

* **Version 1.0.0:** Initial release of the Status Code Transformation Policy.

### License <a href="#user-content-license" id="user-content-license"></a>

This policy is licensed under the terms and conditions of the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

***

By using the `status-code` policy, you can have finer control over the status codes returned to your API clients, improving consistency and meeting specific client requirements without altering your backend services.
