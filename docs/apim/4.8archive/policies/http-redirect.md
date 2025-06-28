---
hidden: true
---

# HTTP Redirect


## Overview
The `http-redirect` policy is used to send redirect responses to an HTTP client as described in
[RFC7231](https://datatracker.ietf.org/doc/html/rfc7231#section-6.4).

The URI for redirection is sent back to the HTTP client using a `Location` header and a 3xx HTTP status code.



## Usage

You can configure multiple rules and their respective redirections relative to the
initial request path (excluding the API context path).

The first rule defined in the rule list that matches the request path will trigger a redirect response with the associated status.

In a rule, `path` and `location` both support [Gravitee Expression Language](https://documentation.gravitee.io/apim/getting-started/gravitee-expression-language) expressions. The `path` property
supports regular expression matching, which allows capturing groups that can be reused to build the location
URL using expression language.

Two variables are added to the expression language context when the policy runs:

- `group` identifies regular expression groups that are captured following their index (starting from 0).
- `groupName` identifies regular expression groups that are captured using named groups.

### Rules configuration

Redirections triggered by various rules are summarized in the following table:

| Rule path | Rule location | Rule status | Incoming path | Location Header | Status |
|---|---|---|:-------------:|:---:|:---:|
| `/headers` | `https://httpbin.org/headers` | 302 |   `/headers`    | `https://httpbin.org/headers` | 302 |
| `/status/(?<code>.*)` | `https://httpbin.org/status/{#groupName['code']}` | 301 |  `/status/201`  | `https://httpbin.org/status/201` | 301 |
| `/(.*)` | `https://httpbin.org/anything/{#group[0]}` | 308 |     `/foo`      | `https://httpbin.org/anything/foo` | 308 |
| `/(.*)` | `https://httpbin.org/anything/{#group[0]}` | 301 | `/foo/bar/baz`  | `https://httpbin.org/anything/foo/bar/baz` | 301 |

### Cache configuration

The policy caches regular expression patterns compiled from the incoming request path to alleviate the cost compilation has on response times. 

Cache configuration is optional. By default, the cache is configured to store an unlimited number of items with no expiration.

For statically defined paths, the number of items stored in the cache will be equal to the number of rules defined for the policy.

If expression language is used to build rule paths dynamically, configuring the cache allows control of how memory consumption will be impacted by the use of the cache.



## Phases
The `http-redirect` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`

### Supported flow phases:

* Request

## Compatibility matrix
Strikethrough text indicates that a version is deprecated.

| Plugin version| APIM| Java version |
| --- | --- | ---  |
|1.0.0 and after|4.7.x and after|21 |


## Configuration options


#### 
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Description  |
|:----------------------|:-----------------------|:----------:|:-------------|
| Cache configuration<br>`cache`| object|  | Cache configuration for regular expressions compiled from inbound request paths.<br/>See "Cache configuration" section.|
| Redirect rules<br>`rules`| array| ✅| Ordered list of rules to apply to inbound request.<br/>See "Redirect rules" section.|


#### Cache configuration (Object)
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Default  | Description  |
|:----------------------|:-----------------------|:----------:|:---------|:-------------|
| Maximum items<br>`maxItems`| integer<br>`[0, +Inf]`|  | `0`| Maximum number of regular expression patterns stored in the cache. 0 means no maximum.|
| Time to live<br>`timeToLive`| integer<br>`[0, +Inf]`|  | `0`| The duration in milliseconds before a regular expression pattern stored in the cache gets evicted. 0 means no eviction.|


#### Redirect rules (Array)
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Default  | Description  |
|:----------------------|:-----------------------|:----------:|:---------|:-------------|
| Redirect to<br>`location`| string| ✅| | The  value to set in the Location header of the response (Supports EL).|
| Match expression<br>`path`| string| ✅| | Regular expression to match incoming path (Supports EL).|
| Response status<br>`status`| enum (integer)| ✅| `301`| Status of the HTTP redirect response<br>Values: `300` `301` `302` `303` `304` `305` `306` `307` `308`|




## Examples

*API with HTTP Redirect*
```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "HTTP Redirect example API",
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
            "name": "HTTP Redirect",
            "enabled": true,
            "policy": "http-redirect",
            "configuration":
              {
                  "rules": [
                      {
                          "path": "/headers",
                          "location": "https://httpbin.org/headers",
                          "status": 302
                      },
                      {
                          "path": "/status/(?<code>.*)",
                          "location": "https://httpbin.org/status/{#groupName['code']}",
                          "status": 301
                      },
                      {
                          "path": "/(.*)",
                          "location": "https://httpbin.org/anything/{#group[0]}",
                          "status": 301
                      }
                  ],
                  "cache": {
                      "maxItems": 0,
                      "timeToLive": 0
                  }
              }
          }
        ]
      }
    ]
  }
}

```
*CRD API with HTTP Redirect*
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "http-redirect-proxy-api-crd"
spec:
    name: "HTTP Redirect"
    type: "PROXY"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
          - type: "HTTP"
            path: "/"
            pathOperator: "STARTS_WITH"
        request:
          - name: "HTTP Redirect"
            enabled: true
            policy: "http-redirect"
            configuration:
              cache:
                  maxItems: 0
                  timeToLive: 0
              rules:
                  - location: https://httpbin.org/headers
                    path: /headers
                    status: 302
                  - location: https://httpbin.org/status/{#groupName['code']}
                    path: /status/(?<code>.*)
                    status: 301
                  - location: https://httpbin.org/anything/{#group[0]}
                    path: /(.*)
                    status: 301

```

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-http-redirect/blob/master/CHANGELOG.md" %}