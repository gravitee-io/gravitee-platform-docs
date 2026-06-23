# Token-Bucket Rate Limiting

## Overview

Token-bucket rate limiting provides a flexible alternative to traditional rate-limiting policies by allowing controlled bursts of traffic while maintaining a steady average request rate. Unlike fixed-window rate limits, the token-bucket algorithm permits clients to consume tokens up to a configured burst capacity, with the bucket refilling at a constant rate over time. This policy is available for both HTTP proxy APIs and V4 message APIs, with support for strict (per-request) and async (approximate) enforcement modes.

## Key Concepts

### Token-Bucket Algorithm

The token-bucket algorithm maintains a bucket of tokens that refills at a constant rate. Each request consumes one token from the bucket. When the bucket is empty, requests are rejected with HTTP 429 (or message stream interruption on message APIs). The bucket starts full at its burst capacity, allowing immediate bursts of traffic up to that limit. Refill occurs continuously: tokens are added to the bucket at the configured **Refill Rate** every **Refill Period Time** (measured in the specified **Refill Period Time Unit**). The bucket never exceeds its **Burst Capacity**—excess tokens from refill are discarded. All calculations use whole-token arithmetic with integer division; fractional tokens are never credited or consumed.

| Parameter | Description | Example |
|:----------|:------------|:--------|
| **Burst Capacity** | Maximum tokens the bucket can hold (≥ 1) | 100 tokens |
| **Refill Rate** | Tokens added per refill period (≥ 1) | 10 tokens |
| **Refill Period Time** | Length of refill period (≥ 1) | 1 |
| **Refill Period Time Unit** | Time unit for refill period | `SECONDS` (options: `SECONDS`, `MINUTES`, `HOURS`, `DAYS`) |

For example, a configuration with `refillRate=100`, `refillPeriodTime=1`, `refillPeriodTimeUnit=MINUTES` adds 100 tokens per minute. A fresh bucket starts at full capacity, so the first burst is allowed immediately.

### Enforcement Modes

The policy supports two enforcement modes: strict and async (non-strict). Strict mode enforces the token-bucket limit on every request with atomic refill-and-consume operations against the distributed store, providing exact request-for-request accuracy. Async mode maintains a local bucket per gateway node that is reconciled to the distributed store periodically (every **Flush Interval** milliseconds), offering higher throughput at the cost of approximate enforcement. In async mode, backends may receive more requests than the configured rate within a reconcile window, and the distributed bucket is only eventually consistent across nodes.

| Mode | Behavior | Store Round-Trips | Accuracy |
|:-----|:---------|:------------------|:---------|
| Strict (`async=false`) | Every request: atomic refill-and-consume against store | One per request | Exact, request-for-request |
| Async (`async=true`) | Local bucket per node, reconciled to store every **Flush Interval** ms | One per **Flush Interval** per active key | Approximate; backend may receive more than configured rate |

During async reconciliation, the node's locally-consumed delta is pushed to the store as a single consume operation. If the store has fewer tokens than the delta, it debits nothing and returns `allowed=false`, causing the node to throttle to zero (local refill rate only). Over-served deltas (where the node admitted more requests than the store can cover) are dropped as a bounded one-time overshoot, not carried forward.

### Bucket Key Composition

Each token bucket is identified by a key composed from the plan, subscription, and an optional custom key. The **Key** field (supporting Expression Language) allows you to identify consumers by custom attributes (e.g., IP address, user ID). The **Use Key Only** flag determines whether the custom key is used alone or combined with the plan and subscription identifiers. All token-bucket keys include a `:tb` suffix to distinguish them from rate-limit, quota, and spike-arrest keys.

| **Use Key Only** | **Key** | Resulting Key Format |
|:-----------------|:--------|:---------------------|
| `true` | `"custom-key"` | `"custom-key:tb"` |
| `false` | `"custom-key"` | `"<plan><subscription>:custom-key:tb"` |
| `false` | `null` or `""` | `"<plan><subscription>:tb"` |

### Error Handling Strategy

The **Error Strategy** field controls how the policy responds to infrastructure failures (e.g., store outages). The default `FALLBACK_PASS_TROUGH` strategy fails open: when the store is unavailable, requests pass through without throttling. The `BLOCK_ON_INTERNAL_ERROR` strategy fails closed: store failures result in HTTP 429 rejections, ensuring the rate limit is never bypassed.

| Strategy | Store Failure Behavior | Use Case |
|:---------|:------------------------|:---------|
| `FALLBACK_PASS_TROUGH` (default) | Request passes through; throttling disabled | Fail open: store outage must not block traffic |
| `BLOCK_ON_INTERNAL_ERROR` | Request rejected with 429 | Fail closed: store outage must not bypass limit |

## Prerequisites

Before you configure token-bucket rate limiting, ensure the following requirements are met:

* APIM 4.12 or later
* A compatible repository plugin (JDBC, MongoDB, Redis, or Hazelcast) with token-bucket support
* For JDBC deployments: the `tokenbucket` table is created automatically by Liquibase on gateway startup
* For MongoDB deployments: the TTL index on `tokenbucket.expire_at` is created automatically on gateway startup
* For async mode: the async rate-limit service must be enabled (`services.ratelimit.enabled=true`, default)

## Gateway Configuration

### Rate-Limit Service

The async rate-limit service reconciles local token-bucket deltas with the distributed store at a configurable interval. This service is shared by rate-limit, quota, spike-arrest, and token-bucket policies.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `services.ratelimit.enabled` | Boolean | `true` | Enable/disable the async rate-limit service |
| [Flush Interval](#rate-limit-service) | Long (ms) | `5000` | Global interval at which async (non-strict) local counters/buckets are reconciled to the store |

**Helm Chart Configuration:**

```yaml
gateway:
  services:
    ratelimit:
      async:
        flushInterval: 5000  # milliseconds
```

Non-positive flush interval values (0 or negative) are silently clamped to the default 5000ms to prevent CPU busy-looping.

### Repository-Specific Configuration

#### JDBC

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| Rate-Limit Table Prefix | String | `""` | Table name prefix for JDBC token-bucket table |
| Management Table Prefix | String | `""` | Table name prefix for JDBC management schema (used by Liquibase) |

The `tokenbucket` table is created automatically by Liquibase on gateway startup. The table name respects the `ratelimit.jdbc.prefix` configuration (via the `${gravitee_rate_limit_prefix}` Liquibase property).

{% hint style="warning" %}
**JDBC Limitation:** Unlike MongoDB, Redis, and Hazelcast, the JDBC `tokenbucket` table has no native row TTL. Rows persist until purged externally. For high-cardinality keyspaces (per-subscription/per-resource), the table grows with the number of distinct keys ever seen. This is an operational trade-off, not a correctness issue: a stale row refills to full on next touch, identical to a fresh bucket.
{% endhint %}

#### MongoDB

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| Rate-Limit Collection Prefix | String | `""` | Collection name prefix for MongoDB token-bucket collection |

The `tokenbucket` collection and TTL index on `expire_at` are created automatically on gateway startup.

#### Redis

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| Redis Operation Timeout | Integer (seconds) | `10` | Redis operation timeout for token-bucket operations |

The `token-bucket.lua` script is loaded via `SCRIPT LOAD` on gateway startup (or via `EVAL` fallback on first use in Redis Cluster).

#### Hazelcast

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| Hazelcast Configuration Path | String | `${gravitee.home}/config/hazelcast-ratelimit.xml` | Path to Hazelcast configuration file for rate-limit store |

The `token-buckets` map is created on-demand by Hazelcast when the first token-bucket operation occurs.

## Creating a Token-Bucket Rate Limit

To apply token-bucket rate limiting to an API, add the `token-bucket-rate-limit` policy to a plan or flow. Configure the policy with the following fields:

| Field | Type | Required | Default | Description |
|:------|:-----|:---------|:--------|:------------|
| **Burst Capacity** | Long | Yes* | none | Maximum tokens the bucket can hold (≥ 1). Provide either this or **Dynamic Burst Capacity**. |
| **Dynamic Burst Capacity** | String (EL) | Yes* | none | Expression Language expression for burst capacity, evaluated per request. Used only when static **Burst Capacity** is not set. |
| **Refill Rate** | Long | Yes* | none | Tokens added per refill period (≥ 1). Provide either this or **Dynamic Refill Rate**. |
| **Dynamic Refill Rate** | String (EL) | Yes* | none | Expression Language expression for refill rate, evaluated per request. Used only when static **Refill Rate** is not set. |
| **Refill Period Time** | Long | Yes | `1` | Length of refill period (≥ 1), combined with **Refill Period Time Unit**. |
| **Refill Period Time Unit** | String (enum) | Yes | `"SECONDS"` | Time unit: `SECONDS`, `MINUTES`, `HOURS`, `DAYS`. |
| **Add Headers** | Boolean | No | `false` | Add `X-Rate-Limit-*` and `Retry-After` headers to HTTP response. |
| **Async** | Boolean | No | `false` | Enable non-strict mode: local bucket reconciled periodically to store. Higher throughput, approximate enforcement. |
| **Key** | String (EL) | No | `null` | Custom key to identify consumer. Empty = default (plan/subscription pair). Supports Expression Language. |
| **Use Key Only** | Boolean | No | `false` | Use only the custom key (ignore plan/subscription). |
| **Error Strategy** | String (enum) | No | `"FALLBACK_PASS_TROUGH"` | `FALLBACK_PASS_TROUGH` (fail open) or `BLOCK_ON_INTERNAL_ERROR` (fail closed). |

**\* Required Constraint:** Each of **Burst Capacity** and **Refill Rate** is required, but may be supplied *either* as the static value *or* through its dynamic EL variant. A configuration where neither form resolves to a positive value is rejected at request time with HTTP 500 (`TOKEN_BUCKET_RATE_LIMIT_SERVER_ERROR`) and message: `"Token-bucket rate-limit misconfigured: refillRate and burstCapacity must resolve to a positive value (set the static value or a dynamic EL expression)."` If the token-bucket rate-limit service is not installed, the policy rejects with HTTP 500 and message: `"No token-bucket rate-limit service has been installed"`.

**Example Configuration (JSON):**

```json
{
  "burstCapacity": 100,
  "refillRate": 10,
  "refillPeriodTime": 1,
  "refillPeriodTimeUnit": "SECONDS",
  "addHeaders": true,
  "async": false,
  "key": "",
  "useKeyOnly": false,
  "errorStrategy": "FALLBACK_PASS_TROUGH"
}
```

This configuration allows bursts of up to 100 requests, refilling at 10 tokens per second. The bucket starts full, so the first 100 requests are admitted immediately. Subsequent requests are throttled to 10 per second.

## Managing Token-Bucket Rate Limits

### Response Headers

When **Add Headers** is enabled, the policy adds the following headers to HTTP responses:

* `X-Rate-Limit-Limit`: Burst capacity (maximum tokens)
* `X-Rate-Limit-Remaining`: Tokens remaining after this request
* `X-Rate-Limit-Reset`: Epoch milliseconds when the bucket will next refill
* `Retry-After`: Seconds until the next token is available (added to 429 responses only)

### Rate-Limit Rejection

When the bucket is empty (`tokens < tokensRequested`), the request is rejected:

* **HTTP APIs:** HTTP 429 (Too Many Requests) with error key `TOKEN_BUCKET_RATE_LIMIT_TOO_MANY_REQUESTS`
* **V4 Message APIs:** Message stream interrupted via `interruptMessagesWith`

### Error Responses

| Error Key | HTTP Status | Context |
|:----------|:------------|:--------|
| `TOKEN_BUCKET_RATE_LIMIT_TOO_MANY_REQUESTS` | 429 | Bucket empty; request rejected |
| `TOKEN_BUCKET_RATE_LIMIT_SERVER_ERROR` | 500 | Infrastructure failure (no service/config, zero config) |
| `TOKEN_BUCKET_RATE_LIMIT_BLOCK_ON_INTERNAL_ERROR` | 429 | Store failure with `BLOCK_ON_INTERNAL_ERROR` strategy |
| `TOKEN_BUCKET_RATE_LIMIT_NOT_APPLIED` | N/A (warning) | Store failure with `FALLBACK_PASS_TROUGH` strategy |

### Floating-Point Backend Precision

MongoDB and Redis use floating-point arithmetic for refill calculations. For configurations where `capacity * refillPeriodMillis` or `effectiveElapsed * refillRate` exceed 2^53, these backends may land one token off the integer backends (JDBC, Hazelcast, in-memory). This is a benign one-token divergence, never an over-admission. The bound is documented, not enforced, so existing high-capacity configurations are not rejected on upgrade. For realistic rate-limit configurations (e.g., capacity < 1 billion, refill period < 1 day), the products are many orders of magnitude below 2^53, and floating-point results match integer backends exactly.
