= Status Code Transformation Policy

== Phase

|===
|onRequest |onResponse

|          | X
|===

== Description

The `status-code` policy allows you to transform the response status code sent from the upstream service to a different HTTP status code based on configured mappings.

This policy is useful when you need to present a specific status code to the client without altering the upstream service. For example, if the upstream service returns a `202 Accepted` status code but you prefer to send a `200 OK` to the client, you can configure the policy to perform this transformation.

== Configuration

To configure the policy, define a list of status code mappings. Each mapping specifies an input status code to match and an output status code to transform it into.

The policy processes the response status code from the upstream service and, if it matches an input status code in the mappings, changes it to the corresponding output status code before sending it to the client.

If there is no matching input status code, the policy leaves the status code unchanged.

=== Configuration Properties

|===
|Property |Required |Description |Type |Default

|`statusMappings` |X|List of status code mappings|Array of mappings|N/A

|`statusMappings[].inputStatusCode` |X|Input status code to match|Integer (Standard HTTP status code)|N/A

|`statusMappings[].outputStatusCode` |X|Output status code to transform to|Integer (Standard HTTP status code)|N/A
|===

=== Notes

- **Input and Output Status Codes**: The status codes should be standard HTTP status codes ranging from `100` to `511`. The policy supports a predefined list of status codes.

- **Multiple Mappings for Same Input Status Code**: If multiple mappings are defined for the same input status code, the last mapping in the list takes precedence.

== Example

Given the following configuration:

[source,json]
----
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
----

In this configuration:

- When the upstream service returns a `202 Accepted`, the policy transforms it to a `200 OK` before sending the response to the client.
- When the upstream service returns a `404 Not Found`, the policy transforms it to a `200 OK`.
- When the upstream service returns a `500 Internal Server Error`, the policy transforms it to a `503 Service Unavailable`.

== Limitations

- **Status Code Only**: The policy only modifies the response status code. It does not alter the response body or headers.

- **Status code range**: The policy only modifies HTTP status codes in the range from 100 till 599 only. For example it will not be possible to modify HTTP status code 600, or 703.

- **No Matching Mapping**: If the response status code does not match any input status code in the mappings, the original status code is retained.

== Attributes

This policy does not set or modify any specific attributes in the execution context.

== Errors

The `status-code` policy does not generate errors on its own. It operates silently, modifying the status code when a mapping is matched. If an exception occurs during policy execution, standard error handling mechanisms apply.

== Compatibility with APIM

|===
|Plugin Version | APIM Version

|1.x            | 4.2.x to latest
|===

== Related Information

- **HTTP Status Codes**: For a complete list of HTTP status codes and their meanings, refer to the https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html[HTTP/1.1 Status Code Definitions].

- **Gravitee.io Documentation**: For more information on policies and API management, visit the https://docs.gravitee.io[Gravitee.io API Management Documentation].

== Changelog

- **Version 1.0.0**:
- Initial release of the Status Code Transformation Policy.

== License

This policy is licensed under the terms and conditions of the https://www.apache.org/licenses/LICENSE-2.0[Apache License, Version 2.0].

---

By using the `status-code` policy, you can have finer control over the status codes returned to your API clients, improving consistency and meeting specific client requirements without altering your backend services.
