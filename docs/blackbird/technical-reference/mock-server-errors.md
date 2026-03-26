---
description: Troubleshooting guide for Mock Server Errors.
noIndex: true
---

# Mock Server Errors

There are various possible errors when using Blackbird's Mock Server tooling. This document outlines potential errors and how to troubleshoot. All of these error returns conform to [RFC7807](https://datatracker.ietf.org/doc/html/rfc7807).

## Routing Errors

These errors are returned when Blackbird is trying to identify the correct resource to use to respond to the HTTP Request.

### NO\_PATH\_MATCHED\_ERROR

**Error:** `404`: Route not resolved, no path matched

**Detail:** The OpenAPI spec doesn't have any endpoints matching the requested URL.

**Troubleshooting:** Please ensure that the requested URL is reflected in the OpenAPI spec.

**Example:**

```yaml
openapi: 3.0.1
paths:
  /pets:
    get:
      responses:
        200:
          description: Hey
```

`curl -X POST http://mocked-url-here/api-name/hello`

### NO\_METHOD\_MATCHED\_ERROR

**Error:** `405`: Route resolved, but no path matched

**Detail:** The OpenAPI spec has an endpoint with the requested URL, but the specified Verb isn't listed.

**Troubleshooting:** Please ensure that the requested Verb is reflected for the URL in the OpenAPI spec.

**Example:**

```yaml
openapi: 3.0.1
paths:
  /pets:
    get:
      responses:
        200:
          description: Hey
```

`curl -X POST http://mocked-url-here/api-name/pets`

### NO\_SERVER\_CONFIGURATION\_PROVIDED\_ERROR

**Error:** `404`: Route not resolved, no server configuration provided

**Detail:** A base URL has been provided in the request (enabling the server validation feature) but the OpenAPI spec doesn't have any `servers` field/entry.

**Troubleshooting:** Please ensure that the OpenAPI spec has the proper `servers` entry or that the server validation is not enabled in the request.

## Validation Errors

These errors are returned when Blackbird is validating the request/response against the provided OpenAPI file.

### UNPROCESSABLE\_ENTITY

**Error:** `422`: Invalid request

**Detail:** The request hasn't passed the validation rules specified in the OpenAPI file _and_ the current resource is missing an error message.

**Troubleshooting:** Please double check the expected validation rules in the OpenAPI spec and the error messaging.

### NOT\_ACCEPTABLE

**Error:** `406`: The server can't produce a representation for your accept header

**Detail:** This error occurs when the request has asked the response in a format that the current OpenAPI spec isn't able to produce.

**Troubleshooting:** Please double check the expected response for the request in the OpenAPI spec.

**Example:**

```yaml
openapi: 3.0.2
paths:
  /todos:
    get:
      responses:
        200:
          description: Get Todo Items
          examples:
            text/plain: hello
```

`curl http://mocked-url-here/todos -H "accept: application/json"`

### NOT\_FOUND

**Error:** `404`: The server can't find the requested content

**Detail:** The request is asking for a specific status code or example that the OpenAPI spec doesn't have.

**Troubleshooting:** Please double check the status code fields for the requested route in the OpenAPI spec.

## Security Errors

These errors are returned when the current request isn't satisfying the security requirements specified in the OpenAPI spec.

### UNAUTHORIZED

**Error:** `401`: Invalid security scheme used

**Detail:** The security scheme for the OpenAPI spec doesn't match the request being processed.

**Troubleshooting:** Please double check the security schemes in the OpenAPI spec.

## Negotiation Errors

These errors are returned when a valid request can't return a suitable response

### NO\_COMPLEX\_OBJECT\_TEXT

**Error:** `500`: Can't serialise complex objects as text

**Detail:** This error occurs when the current request accepts the `text/*` as the response content type, and Blackbird decided to respond with this content type. However, the schema generated a non-primitive payload and Blackbird couldn't serialise the result.

**Troubleshooting:** Please double check the schema type in the OpenAPI spec with the request's content type.

**Example:**

```yaml
openapi: '3.0.1'
paths:
  /:
    get:
      responses:
        200:
          content:
            text/plain:
              schema:
                type: object
                properties:
                  name:
                    type: string
                    example: Clark
                  surname:
                    type: string
                    example: Kent
```

`curl http://mocked-url-here/api-name/ -A 'Accept: text/plain'`

### NO\_RESPONSE\_DEFINED

**Error:** `500`: No response defined for the selected operation

**Detail:** This error occurs when the request has matched a corresponding operation and passed validation, but there's no response that could be returned.

**Troubleshooting:** Please double check the expected response in the OpenAPI spec.

### INVALID\_CONTENT\_TYPE

**Error:** `415`: Supported content types: _list_

**Detail:** This error occurs when the request specifies a `Content-Type` that isn't supported by the corresponding Operation. In the case there is no request body or `Content-Length` is 0, the `Content-Type` header is ignored.

**Troubleshooting:** Please double check the requests `Content-Type` with the OpenAPI spec and corresponding Operation.

### SCHEMA\_TOO\_COMPLEX

**Error:** `500`: Unable to generate \[body|header] for response. The schema is too complex to generate.

**Detail:** This error occurs when part of the response can't be generated due to complexity. The JSON Schema Sampler is used to generate responses and has been configured to use a limit of 2500 "ticks". A "tick" is loosely defined as any instance of a JSON Schema schema or subschema, thus including a Property, an Object, an Array item, or a Combiner item.

**Troubleshooting:** The response is too complex. Please simplify or shorten the expected response.

## Other Errors

In case you get an `UNKNOWN` error, or an error not on this list, it likely means this particular edge case isn't handled or not properly documented. If you encounter one of these, please reach out to the Ambassador support team.
