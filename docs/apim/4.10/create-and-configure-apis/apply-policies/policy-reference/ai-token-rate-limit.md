# AI - Token Rate Limit

### Overview

This policy allows you to configure the number of total of inbound tokens and outbound tokens allowed over a limited period of time in minutes and seconds.

### Usage

This rate limit operates with a **one-request latency**. Since the final token count is only known and updated **after** the request has been processed and the full response has been delivered.

To manage potential technical failures within the distributed counter system. For example, a database failure, the strategy is employed:

* `BLOCK_ON_INTERNAL_ERROR` is chosen when security and precision are paramount, rejecting queries if the counter system fails.
* `FALLBACK_PASS_THROUGH` prioritizes availability, allowing queries to proceed if the counter system fails.
* `ASYNC_MODE` when low latency and high throughput are prioritized. Rate-limiting is applied asynchronously, meaning the distributed counter value is not strictly accurate.

You may use the `key` if you need an identifier to count the requests. It can be dynamic. You can use Gravitee Expression Language. Also, you can enable `useKeyOnly` to ensure that the plan and subscription are ignored.

For example, you could use an Expression Language like `{#request.remoteAddress}` and enable `useKeyOnly` to identify per-IP traffic and apply the policy's limit.

### Phases

The `token-ratelimit` policy can be applied to the following API types and flow phases.

#### Compatible API types

* `LLM PROXY`

#### Supported flow phases:

* Request

### Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version  | APIM             | Java version |
| --------------- | ---------------- | ------------ |
| 1.0.0 and after | 4.10.x and after | 21           |

### Configuration options

| <p>Name<br><code>json name</code></p>                  | <p>Type<br><code>constraint</code></p> | Mandatory | Default      | Description                                                                                                                                                                                                         |
| ------------------------------------------------------ | -------------------------------------- | :-------: | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p>Add response headers<br><code>addHeaders</code></p> | boolean                                |           |              | Add X-Token-Rate-Limit-Limit, X-Token-Rate-Limit-Remaining and X-Token-Rate-Limit-Reset headers in HTTP response                                                                                                    |
| <p>Apply rate-limiting<br><code>rate</code></p>        | object                                 |     ✅     |              | <p><br>See "Apply rate-limiting" section.</p>                                                                                                                                                                       |
| <p>Strategy<br><code>strategy</code></p>               | enum (string)                          |     ✅     | `ASYNC_MODE` | <p>Defines the strategy for rate-limiting, including execution mode and behavior on internal errors.<br>Values: <code>BLOCK_ON_INTERNAL_ERROR</code> <code>FALLBACK_PASS_THROUGH</code> <code>ASYNC_MODE</code></p> |

**Apply rate-limiting (Object)**

| <p>Name<br><code>json name</code></p>                    | <p>Type<br><code>constraint</code></p>   | Mandatory | Default   | Description                                                                                                                                                  |
| -------------------------------------------------------- | ---------------------------------------- | :-------: | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p>Max tokens (dynamic)<br><code>dynamicLimit</code></p> | string                                   |           |           | Dynamic limit on the number of tokens that can be used (this limit is used if static limit = 0). The dynamic value is based on EL expressions.               |
| <p>Key<br><code>key</code></p>                           | string                                   |           |           | Key to identify a consumer against whom the rate-limiting will be applied. Leave it empty to use the default behavior (plan/subscription pair). Supports EL. |
| <p>Max tokens (static)<br><code>limit</code></p>         | <p>integer<br><code>[0, +Inf]</code></p> |           |           | Static limit on the number of tokens that can be used (this limit is used if the value > 0).                                                                 |
| <p>Time duration<br><code>periodTime</code></p>          | integer                                  |     ✅     | `1`       | How long to reset the limit                                                                                                                                  |
| <p>Time unit<br><code>periodTimeUnit</code></p>          | enum (string)                            |     ✅     | `SECONDS` | Values: `SECONDS` `MINUTES`                                                                                                                                  |
| <p>Use key only<br><code>useKeyOnly</code></p>           | boolean                                  |           |           | Only uses the custom key to identify the consumer, regardless of the subscription and plan.                                                                  |

### Examples

_Token rate limiting_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Token Rate Limit example API",
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
            "name": "Token Rate Limit",
            "enabled": true,
            "policy": "token-ratelimit",
            "configuration":
              {
                  "strategy": "ASYNC_MODE",
                  "addHeaders": true,
                  "rate": {
                      "key": "customer",
                      "useKeyOnly": true,
                      "limit": 100,
                      "periodTime": 1,
                      "periodTimeUnit": "MINUTES"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

_Dynamic limit_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Token Rate Limit example API",
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
            "name": "Token Rate Limit",
            "enabled": true,
            "policy": "token-ratelimit",
            "configuration":
              {
                  "strategy": "ASYNC_MODE",
                  "addHeaders": true,
                  "rate": {
                      "dynamicLimit": "{#context.attributes['limit']}",
                      "periodTime": 60,
                      "periodTimeUnit": "MINUTES"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

_Async mode_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Token Rate Limit example API",
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
            "name": "Token Rate Limit",
            "enabled": true,
            "policy": "token-ratelimit",
            "configuration":
              {
                  "strategy": "ASYNC_MODE",
                  "addHeaders": true,
                  "rate": {
                      "limit": 100,
                      "periodTime": 1,
                      "periodTimeUnit": "MINUTES"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

_Block on internal error_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Token Rate Limit example API",
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
            "name": "Token Rate Limit",
            "enabled": true,
            "policy": "token-ratelimit",
            "configuration":
              {
                  "strategy": "BLOCK_ON_INTERNAL_ERROR",
                  "addHeaders": true,
                  "rate": {
                      "limit": 100,
                      "periodTime": 1,
                      "periodTimeUnit": "MINUTES"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

_Fallback pass through_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Token Rate Limit example API",
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
            "name": "Token Rate Limit",
            "enabled": true,
            "policy": "token-ratelimit",
            "configuration":
              {
                  "strategy": "FALLBACK_PASS_THROUGH",
                  "addHeaders": true,
                  "rate": {
                      "limit": 100,
                      "periodTime": 1,
                      "periodTimeUnit": "MINUTES"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

### Changelog

#### [1.0.0-alpha.2](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/compare/1.0.0-alpha.1...1.0.0-alpha.2) (2025-11-27)

**Bug Fixes**

* schema ([d45afc3](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/d45afc3e47fb0d1c32568fad22b94ddd76fe50f7))

#### 1.0.0-alpha.1 (2025-11-21)

**Bug Fixes**

* assembly ([8565b05](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/8565b05b5bbc0d055452e501f2c4fe0e86a37139))
* stream mode ([32251e0](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/32251e0c5792155798a751741161e7decbc42c21))
* stream mode without cached chunks ([bda69c7](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/bda69c7598fdf3fea20c571a316b30176d31cea8))

**Features**

* handle errors ([d50cd3b](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/d50cd3b797a145352306f8596dc23f295bdb7364))
* token based rate limiting policy ([95f4e5b](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/95f4e5b7d7975fc0b269a2d0209b1c48689c7cc5))
* use dynamic limit and add limit headers ([153aa8b](https://github.com/gravitee-io/gravitee-policy-token-ratelimit/commit/153aa8b010266dd4a133bd6ed178c4d4d7598ef7))
