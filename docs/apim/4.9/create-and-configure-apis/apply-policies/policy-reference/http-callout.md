---
description: An overview about http callout.
---

# HTTP Callout

## Overview

You can use the `callout-http` policy to invoke an HTTP(S) URL and place a subset, or all, of the content in one or more variables of the request execution context.

This can be useful if you need some data from an external service and want to inject it during request processing.

The result of the callout is placed in a variable called `calloutResponse` and is only available during policy execution. If no variable is configured the result of the callout is no longer available.

The CalloutHttpPolicy includes comprehensive OpenTelemetry tracing support using the V4 API, allowing you to monitor and debug HTTP callout operations with detailed span information. The tracing integration is automatically enabled when OpenTelemetry tracing is configured in your Gravitee environment and enabled in API context.

## Errors

These templates are defined at the API level, in the "Entrypoint" section for v4 APIs, or in "Response Templates" for v2 APIs.\
The error keys sent by this policy are as follows:

| Key                      |
| ------------------------ |
| CALLOUT\_EXIT\_ON\_ERROR |
| CALLOUT\_HTTP\_ERROR     |

## Phases

The `policy-http-callout` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`

### Supported flow phases:

* `Request`
* `Response`

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version       | APIM                 |
| -------------------- | -------------------- |
| 5.x                  | 4.6.x to latest      |
| 4.x                  | 4.4.x to 4.5.x       |
| 3.x                  | 4.0.x to 4.3.x       |
| ~~2.x~~              | ~~3.18.x to 3.20.x~~ |
| ~~1.15.x and upper~~ | ~~3.15.x to 3.17.x~~ |
| ~~1.13.x to 1.14.x~~ | ~~3.10.x to 3.14.x~~ |
| ~~Up to 1.12.x~~     | ~~Up to 3.9.x~~      |

## Configuration

### Gateway configuration

### System proxy

If the option `useSystemProxy` is checked, proxy information will be read from `JVM_OPTS`, or from the `gravitee.yml` file if `JVM_OPTS` is not set.

For example:

gravitee.yml

```yaml
system:
  proxy:
    type: HTTP      # HTTP, SOCK4, SOCK5
    host: localhost
    port: 3128
    username: user
    password: secret
```

### Configuration options

| <p>Name<br><code>json name</code></p>                    | <p>Type<br><code>constraint</code></p> | Mandatory | Default                                                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------- | -------------------------------------- | :-------: | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p>Request body<br><code>body</code></p>                 | string                                 |           |                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <p>Error condition<br><code>errorCondition</code></p>    | string                                 |           | `{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}` | The condition which will be verified to end the request (supports EL).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| <p>Error response body<br><code>errorContent</code></p>  | string                                 |           |                                                                       | The body response of the error if the condition is true (supports EL).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| <p>Error status code<br><code>errorStatusCode</code></p> | enum (string)                          |           | `500`                                                                 | <p>HTTP Status Code send to the consumer if the condition is true.<br>Values: <code>100</code> <code>101</code> <code>102</code> <code>200</code> <code>201</code> <code>202</code> <code>203</code> <code>204</code> <code>205</code> <code>206</code> <code>207</code> <code>300</code> <code>301</code> <code>302</code> <code>303</code> <code>304</code> <code>305</code> <code>307</code> <code>400</code> <code>401</code> <code>402</code> <code>403</code> <code>404</code> <code>405</code> <code>406</code> <code>407</code> <code>408</code> <code>409</code> <code>410</code> <code>411</code> <code>412</code> <code>413</code> <code>414</code> <code>415</code> <code>416</code> <code>417</code> <code>422</code> <code>423</code> <code>424</code> <code>429</code> <code>500</code> <code>501</code> <code>502</code> <code>503</code> <code>504</code> <code>505</code> <code>507</code></p> |
| <p>Exit on error<br><code>exitOnError</code></p>         | boolean                                |     ✅     |                                                                       | Terminate the request if the error condition is true.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| <p>Fire &#x26; forget<br><code>fireAndForget</code></p>  | boolean                                |           |                                                                       | Make the HTTP call without expecting any response. When activating this mode, context variables and exit on error are useless.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| <p>Request Headers<br><code>headers</code></p>           | array                                  |           |                                                                       | <p><br>See "Request Headers" section.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| <p>HTTP Method<br><code>method</code></p>                | enum (string)                          |     ✅     | `GET`                                                                 | <p>HTTP method to invoke the endpoint.<br>Values: <code>GET</code> <code>POST</code> <code>PUT</code> <code>DELETE</code> <code>PATCH</code> <code>HEAD</code> <code>CONNECT</code> <code>OPTIONS</code> <code>TRACE</code></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <p>URL<br><code>url</code></p>                           | string                                 |     ✅     |                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <p>Use system proxy<br><code>useSystemProxy</code></p>   | boolean                                |           |                                                                       | Use the system proxy configured by your administrator.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| <p>Context variables<br><code>variables</code></p>       | array                                  |           |                                                                       | <p><br>See "Context variables" section.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### Request Headers (Array)

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ----------- |
| <p>Name<br><code>name</code></p>      | string                                 |           |             |
| <p>Value<br><code>value</code></p>    | string                                 |           |             |

#### Context variables (Array)

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default                                            | Description |
| ------------------------------------- | -------------------------------------- | :-------: | -------------------------------------------------- | ----------- |
| <p>Name<br><code>name</code></p>      | string                                 |           |                                                    |             |
| <p>Value<br><code>value</code></p>    | string                                 |           | `{#jsonPath(#calloutResponse.content, '$.field')}` |             |

## Examples

_API with basic callout_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "HTTP Callout example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "request": [
          {
            "name": "HTTP Callout",
            "enabled": true,
            "policy": "policy-http-callout",
            "configuration":
              {
                  "method": "GET",
                  "url": "https://api.gravitee.io/echo",
                  "headers": [
                      {
                          "name": "X-Gravitee-Request-Id",
                          "value": "{#request.id}"
                      }
                  ],
                  "variables": [
                      {
                          "name": "my-server",
                          "value": "{#jsonPath(#calloutResponse.content, '$.headers.X-Forwarded-Server')}"
                      }
                  ],
                  "exitOnError": true
              }
          }
        ]
      }
    ]
  }
}

```

_API CRD with basic callout_

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "policy-http-callout-proxy-api-crd"
spec:
    name: "HTTP Callout"
    type: "PROXY"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
          - type: "HTTP"
            path: "/"
            pathOperator: "STARTS_WITH"
        request:
          - name: "HTTP Callout"
            enabled: true
            policy: "policy-http-callout"
            configuration:
              method: GET
              url: https://api.gravitee.io/echo
              headers:
                  - name: X-Gravitee-Request-Id
                    value: "{#request.id}"
              variables:
                  - name: my-server
                    value: "{#jsonPath(#calloutResponse.content, '$.headers.X-Forwarded-Server')}"
              exitOnError: true

```

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-callout-http/blob/master/CHANGELOG.md" %}
