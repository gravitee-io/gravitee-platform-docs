---
hidden: true
---

# HTTP Callout

## Overview
You can use the `callout-http` policy to invoke an HTTP(S) URL and place a subset, or all, of the content in
one or more variables of the request execution context.

This can be useful if you need some data from an external service and want to inject it during request
processing.

The result of the callout is placed in a variable called `calloutResponse` and is only available during policy
execution. If no variable is configured the result of the callout is no longer available.





## Errors
These templates are defined at the API level, in the "Entrypoint" section for v4 APIs, or in "Response Templates" for v2 APIs.
The error keys sent by this policy are as follows:

| Key |
| ---  |
| CALLOUT_EXIT_ON_ERROR |
| CALLOUT_HTTP_ERROR |



## Phases
The `policy-http-callout` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`

### Supported flow phases:

* Request
* Response

## Compatibility matrix
Strikethrough text indicates that a version is deprecated.

| Plugin version| APIM |
| --- | ---  |
|4.x|4.4.x to latest |
|3.x|4.0.x to 4.3.x |
|~~2.x~~|~~3.18.x to 3.20.x~~ |
|~~1.15.x and upper~~|~~3.15.x to 3.17.x~~ |
|~~1.13.x to 1.14.x~~|~~3.10.x to 3.14.x~~ |
|~~Up to 1.12.x~~|~~Up to 3.9.x~~ |



## Configuration
### Gateway configuration
### System proxy

If the option `useSystemProxy` is checked, proxy information will be read from `JVM_OPTS`, or from the `gravitee.yml` file if `JVM_OPTS` is not set.

For example: 

gravitee.yml
```YAML
system:
  proxy:
    type: HTTP      # HTTP, SOCK4, SOCK5
    host: localhost
    port: 3128
    username: user
    password: secret
```



### Configuration options


#### 
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Default  | Description  |
|:----------------------|:-----------------------|:----------:|:---------|:-------------|
| Request body<br>`body`| string|  | | |
| Error condition<br>`errorCondition`| string|  | `{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}`| The condition which will be verified to end the request (supports EL).|
| Error response body<br>`errorContent`| string|  | | The body response of the error if the condition is true (supports EL).|
| Error status code<br>`errorStatusCode`| enum (string)|  | `500`| HTTP Status Code send to the consumer if the condition is true.<br>Values: `100` `101` `102` `200` `201` `202` `203` `204` `205` `206` `207` `300` `301` `302` `303` `304` `305` `307` `400` `401` `402` `403` `404` `405` `406` `407` `408` `409` `410` `411` `412` `413` `414` `415` `416` `417` `422` `423` `424` `429` `500` `501` `502` `503` `504` `505` `507`|
| Exit on error<br>`exitOnError`| boolean| ✅| | Terminate the request if the error condition is true.|
| Fire & forget<br>`fireAndForget`| boolean|  | | Make the HTTP call without expecting any response. When activating this mode, context variables and exit on error are useless.|
| Request Headers<br>`headers`| array|  | | <br/>See "Request Headers" section.|
| HTTP Method<br>`method`| enum (string)| ✅| `GET`| HTTP method to invoke the endpoint.<br>Values: `GET` `POST` `PUT` `DELETE` `PATCH` `HEAD` `CONNECT` `OPTIONS` `TRACE`|
| URL<br>`url`| string| ✅| | |
| Use system proxy<br>`useSystemProxy`| boolean|  | | Use the system proxy configured by your administrator.|
| Context variables<br>`variables`| array|  | | <br/>See "Context variables" section.|


#### Request Headers (Array)
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Description  |
|:----------------------|:-----------------------|:----------:|:-------------|
| Name<br>`name`| string|  | |
| Value<br>`value`| string|  | |


#### Context variables (Array)
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Default  | Description  |
|:----------------------|:-----------------------|:----------:|:---------|:-------------|
| Name<br>`name`| string|  | | |
| Value<br>`value`| string|  | `{#jsonPath(#calloutResponse.content, '$.field')}`| |




## Examples

*API with basic callout*
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
*API CRD with basic callout*
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
