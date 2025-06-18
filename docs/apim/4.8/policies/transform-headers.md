---
hidden: true
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

### Supported flow phases:

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

#### [4.1.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/4.0.2...4.1.0) (2025-06-18)

**Features**

* add Kafka usage to docgen documentation ([439ad7a](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/439ad7a172241e233f341455b23da2590035e47a))

[**4.0.2**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/4.0.1...4.0.2) **(2025-06-18)**

**Bug Fixes**

* allow message to be used in EL ([bff1dd4](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/bff1dd4d4e3e7149e56def225d458ebf43f962be))

[**4.0.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/4.0.0...4.0.1) **(2025-06-17)**

**Bug Fixes**

* last review changes and orb for docgen ([14b17bf](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/14b17bf09d198ac6485e3ef0602b8c8d54ac8263))
* rewrite docs with doc-gen ([050c79d](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/050c79d8c1c060e6d5da50cd5abb7501a67c1693))
* update dependencies and orbs ([443ae8d](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/443ae8d62e2eaa8c0074c5a26ef4515ca1266adf))

#### [4.0.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.2.1...4.0.0) (2025-04-17)

**Features**

* handle KafkaPolicy on message request and response ([6c17501](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/6c17501578ae8e14ef91b5ebf2adbb2c512d6dd7))

**BREAKING CHANGES**

* requires APIM version 4.6.0 or later

[**3.2.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.2.0...3.2.1) **(2025-04-16)**

**Bug Fixes**

* revert BC commit -- "feat: handle KafkaPolicy on message request and response" ([855b5c2](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/855b5c2d83cf135f6893e359b20d3cfebf5c93d1))

#### [3.2.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.1.0...3.2.0) (2025-04-16)

**Features**

* handle KafkaPolicy on message request and response ([1002fe1](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/1002fe1330db81cf603f40be4d0d54bb671f9197))

#### [3.1.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.0.2...3.1.0) (2025-04-11)

**Features**

* add append header support ([da55073](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/da55073e6130d868658310cd1b8e019b11201d8b))

[**3.0.2**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.0.1...3.0.2) **(2023-11-13)**

**Bug Fixes**

* make acceptlist case insensitive ([4748140](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/47481407e287057e9bd67f2fed2df200666e2715))

[**3.0.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/3.0.0...3.0.1) **(2023-07-20)**

**Bug Fixes**

* update policy description ([09173df](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/09173dff95254f61d93131975d2e23861c166e88))

#### [3.0.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/2.0.1...3.0.0) (2023-07-18)

**Bug Fixes**

* remove extra compatibility matrix ([88c653d](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/88c653d638b1e012b1cdfbebaa17bf2048f35a89))
* use new execution mode V4 Emulation ([7d17544](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/7d17544f84e529a6763dd1f2a3a3094e1b0e0903))

**chore**

* **deps:** update gravitee-parent ([84ca37a](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/84ca37a428c117eda89a21c8fa4b4740388f5115))

**Features**

* clean and validate json schema for v4 ([da2a5bc](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/da2a5bc90dce520a88c98e8f860c770329c98fa9))

**BREAKING CHANGES**

* **deps:** require Java17

#### [2.1.0-alpha.2](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/2.1.0-alpha.1...2.1.0-alpha.2) (2023-06-29)

**Bug Fixes**

* use new execution mode V4 Emulation ([7d17544](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/7d17544f84e529a6763dd1f2a3a3094e1b0e0903))

#### [2.1.0-alpha.1](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/2.0.1...2.1.0-alpha.1) (2023-06-27)

**Features**

* clean and validate json schema for v4 ([da2a5bc](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/da2a5bc90dce520a88c98e8f860c770329c98fa9))

[**2.0.1-alpha.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/2.0.0...2.0.1-alpha.1) **(2023-06-22)**

**Bug Fixes**

* add missing manifest information ([ee3bf0b](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/ee3bf0b28193a49c88e33bc064c76957cf3004f1))

[**2.0.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/2.0.0...2.0.1) **(2023-06-23)**

**Bug Fixes**

* addition of supported API type & flow phase for this policy ([db53540](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/db53540a233f3be7b77e52d796ee0ea604b13088))

#### [2.0.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/1.10.0...2.0.0) (2023-06-22)

**Bug Fixes**

* fixed little typo in README.adoc ([e88ce29](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/e88ce298d390b4c850aa4c7566c4f5584f893461))

**Features**

* add support of message level transformation ([f821384](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/f821384a56d88d4a8a8b0e2ee157eb1e100a1d14))

**BREAKING CHANGES**

* this version is using the latest dependencies introduced by Gravitee V4.0

#### [1.10.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/1.9.1...1.10.0) (2022-03-24)

**Features**

* Add support for request / response's payload to define HTTP headers values ([0cb0b2c](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/0cb0b2cb6aff125294f6fd4011dba74dd55db8ff)), closes [gravitee-io/issues#7333](https://github.com/gravitee-io/issues/issues/7333)

[**1.9.1**](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/1.9.0...1.9.1) **(2022-01-24)**

**Bug Fixes**

* support arrays with null elements ([140bded](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/140bded708d9fee2b510fdb2ba67b3edffc811d4)), closes [gravitee-io/issues#5778](https://github.com/gravitee-io/issues/issues/5778)
* **transform-headers:** Provide more logs in case of EL error ([f4efd92](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/f4efd9260888c8b57177da1993bd58a68c063335)), closes [gravitee-io/issues#6479](https://github.com/gravitee-io/issues/issues/6479)

#### [1.9.0](https://github.com/gravitee-io/gravitee-policy-transformheaders/compare/1.8.0...1.9.0) (2022-01-22)

**Features**

* **headers:** Internal HTTP headers refactoring ([3b9919e](https://github.com/gravitee-io/gravitee-policy-transformheaders/commit/3b9919ecdf1d1998f7dbebeab79566bbb25975af)), closes [gravitee-io/issues#6772](https://github.com/gravitee-io/issues/issues/6772)
