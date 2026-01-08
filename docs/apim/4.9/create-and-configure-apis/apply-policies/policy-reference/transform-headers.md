---
description: An overview about transform headers.
metaLinks:
  alternates:
    - transform-headers.md
---

# Transform Headers

## Overview

You can use the `transform-headers` policy to override headers in incoming or outgoing traffic.

### Execution order

Header transformations are executed in the following order:

1. Set/replace headers
2. Append headers: add values to existing headers or add a new header
   * This is not supported for Native APIs
3. Remove headers
4. Keep only whitelisted headers

### Header removal

* Headers added/appended by this policy can be removed
* Whitelisting applies to headers added/appended by this policy

### Native Kafka API Support

For Native Kafka APIs, the transform-headers policy operates on Kafka record headers instead of HTTP headers.

#### **Key differences for Native Kafka APIs:**

* Headers are stored as Kafka record headers
* Header values are stored as Kafka `Buffer` objects
* Append headers functionality is **not supported** for Native Kafka APIs

## Usage

Here are some usage examples of using Transform Headers.

Although each transformation can be configured individually, examples below emphasise that they can be cumulative.

### Set/replace headers

Given the following headers:

```
Content-Type: application/json
```

When applying 'set/replace' with:

* `X-Hello` and value `World`
* `Content-Type` and value `*/*`

Then headers are transformed as follows:

```
X-Hello: World
Content-Type: */*
```

### Amend headers

Given the following headers:

```
X-Hello: World
Content-Type: */*
```

When applying 'amend' with:

* `X-Hello` and value `Good morning`
* `X-Extra` and value `Superfluous`

Then headers are transformed as follows:

```
X-Hello: World,Good morning
X-Extra: Superfluous
Content-Type: */*
```

### Header removal

Given the following headers:

```
X-Hello: World,Good morning
X-Extra: Superfluous
Content-Type: */*
```

When applying 'remove' with:

* name `X-Extra`

Then headers are transformed as follows:

```
X-Hello: World,Good morning
Content-Type: */*
```

### Keep only whitelisted headers

Given the following headers:

```
X-Hello: World,Good morning
Content-Type: */*
```

When applying 'whitelisting' with:

* name `Content-Type`

Then headers are transformed as follows:

```
Content-Type: */*
```

### Native Kafka API Usage

For Native Kafka APIs, the transform-headers policy works with Kafka record headers instead of HTTP headers. Here are examples for both publish and subscribe phases:

#### **Publish Phase Example**

Given the following Kafka record headers:

```
X-Correlation-Id: abc-123
X-Internal-Header: debug-info
```

When applying 'set/replace' with:

* `X-Gravitee-Request-Id` and value `{#request.id}`
* `X-Source-System` and value `api-gateway`

And removing:

* `X-Internal-Header`

Then headers are transformed as follows:

```
X-Correlation-Id: abc-123
X-Gravitee-Request-Id: req-456
X-Source-System: api-gateway
```

#### **Subscribe Phase Example**

Given the following Kafka record headers:

```
X-Correlation-Id: abc-123
X-Debug-Header: debug-info
Content-Type: application/json
```

When applying 'set/replace' with:

* `X-Processing-Timestamp` and value `{#date.now()}`

And removing:

* `X-Debug-Header`

Then headers are transformed as follows:

```
X-Correlation-Id: abc-123
X-Processing-Timestamp: 2024-01-15T10:30:00Z
Content-Type: application/json
```

**Note:** Append headers functionality is not supported for Native Kafka APIs.

## Phases

The `transform-headers` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`
* `NATIVE KAFKA`

### Supported flow phases

* Publish
* Subscribe
* Request
* Response

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version | APIM            |
| -------------- | --------------- |
| 4.x            | 4.6.x to latest |
| 3.x            | 4.0.x to 4.5.x  |
| ~~1.x~~        | ~~3.x~~         |

## Configuration options

| <p>Name<br><code>json name</code></p>                   | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------- | -------------------------------------- | :-------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p>Set/replace headers<br><code>addHeaders</code></p>   | array                                  |           | <p>Values defined here will replace existing values if a header with the same name is already defined in the request.<br>See "Set/replace headers" section.</p>                                                                                                                      |
| <p>Append headers<br><code>appendHeaders</code></p>     | array                                  |           | <p>Similar to set / Replace headers, but the values will be appended instead of being replaced if a header with the same name is already defined in the request. Multiple entries can be used to append several values to the same header name.<br>See "Append headers" section.</p> |
| <p>Remove headers<br><code>removeHeaders</code></p>     | array (string)                         |           |                                                                                                                                                                                                                                                                                      |
| <p>Headers to keep<br><code>whitelistHeaders</code></p> | array (string)                         |           | Works like a whitelist. All other headers will be removed.                                                                                                                                                                                                                           |

#### **Set/replace headers (Array)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description         |
| ------------------------------------- | -------------------------------------- | :-------: | ------------------- |
| <p>Name<br><code>name</code></p>      | <p>string<br><code>^\S*$</code></p>    |     ✅     | Name of the header  |
| <p>Value<br><code>value</code></p>    | string                                 |     ✅     | Value of the header |

#### **Append headers (Array)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description         |
| ------------------------------------- | -------------------------------------- | :-------: | ------------------- |
| <p>Name<br><code>name</code></p>      | <p>string<br><code>^\S*$</code></p>    |     ✅     | Name of the header  |
| <p>Value<br><code>value</code></p>    | string                                 |     ✅     | Value of the header |

## Examples

_Proxy API on Request phase_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Transform Headers example API",
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
            "name": "Transform Headers",
            "enabled": true,
            "policy": "transform-headers",
            "configuration":
              {
                  "addHeaders": [
                      {
                          "name": "X-Gravitee-Request-Id",
                          "value": "{#request.id}"
                      }
                  ],
                  "appendHeaders": [
                      {
                          "name": "Accept-Encoding",
                          "value": "gzip"
                      }
                  ],
                  "removeHeaders": ["User-Agent"]
              }
          }
        ]
      }
    ]
  }
}

```

_Proxy API with whitelisting on Response phase_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Transform Headers example API",
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
        "response": [
          {
            "name": "Transform Headers",
            "enabled": true,
            "policy": "transform-headers",
            "configuration":
              {
                  "whitelistHeaders": ["X-Gravitee-Transaction-Id", "Content-Type", "Content-Length", "Connection"]
              }
          }
        ]
      }
    ]
  }
}

```

_Message API CRD_

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "transform-headers-message-api-crd"
spec:
    name: "Transform Headers example"
    type: "MESSAGE"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
            matchRequired: false
            mode: "DEFAULT"
        subscribe:
          - name: "Transform Headers"
            enabled: true
            policy: "transform-headers"
            configuration:
              addHeaders:
                  - name: X-Gravitee-Request-Id
                    value: '{#request.id}'
              appendHeaders:
                  - name: Accept-Encoding
                    value: gzip
              removeHeaders:
                  - User-Agent

```

_Native Kafka API CRD_

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "transform-headers-kafka-native-api-crd"
spec:
    name: "Transform Headers example"
    type: "NATIVE"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
            matchRequired: false
            mode: "DEFAULT"
        subscribe:
          - name: "Transform Headers"
            enabled: true
            policy: "transform-headers"
            configuration:
              addHeaders:
                  - name: X-Gravitee-Request-Id
                    value: '{#request.id}'
              removeHeaders:
                  - X-Internal-Header
              whitelistHeaders:
                  - X-Internal-Metadata
                  - X-Debug-Header

```

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-transformheaders/blob/master/CHANGELOG.md" %}
