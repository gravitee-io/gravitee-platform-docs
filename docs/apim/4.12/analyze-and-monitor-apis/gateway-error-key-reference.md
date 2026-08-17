---
description: >-
  Every error key the Gateway reports, with the status it produces, the message
  it attaches, and what it actually means.
---

# Gateway error key reference

## How to read this reference

The Gateway records an error key on every request it fails. The key appears in the Error Key field of the log details, and in the Gateway analytics. This page lists the keys the Gateway itself produces. Policies and plugins add their own, as described in [Keys reported by policies](gateway-error-key-reference.md#keys-reported-by-policies).

Two properties of these keys matter when you read them.

**The status is a default.** A [response template](../create-and-configure-apis/configure-v4-apis/response-templates.md) configured for a key, or for its parent key, overrides it. A key listed here as a `502` can reach the API consumer as a `500` when the API falls back to a `DEFAULT` template.

**Fine-grained keys carry a parent key.** When no response template targets the specific key, the Gateway falls back to the template configured for its parent. A fine-grained key without its own template still produces a sensible status.

## Backend connection failures

The Gateway raises these keys while it acts as an HTTP client towards the backend.

<table><thead><tr><th width="80">Status</th><th width="330">Error key</th><th>What it means</th></tr></thead><tbody><tr><td>502</td><td><code>GATEWAY_CLIENT_CONNECTION_ERROR</code></td><td>Umbrella key. A backend connection failed for a reason that no more specific key covers.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_CONNECTION_REFUSED</code></td><td>The backend refused the TCP connection. Nothing listens on that port.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_DNS_RESOLUTION_ERROR</code></td><td>The backend hostname didn't resolve.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_UNREACHABLE</code></td><td>No network route to the backend host exists.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_TLS_HANDSHAKE_ERROR</code></td><td>The TLS handshake with the backend failed: certificate, protocol, or cipher mismatch.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_CONNECTION_RESET</code></td><td>The backend reset the connection with a TCP RST, or sent an HTTP/2 RST_STREAM.</td></tr><tr><td>502</td><td><code>GATEWAY_CLIENT_CONNECTION_CLOSED</code></td><td>The connection closed before any response reached the API consumer. See the note that follows this table.</td></tr><tr><td>—</td><td><code>GATEWAY_CLIENT_STREAM_ENDED_EARLY</code></td><td>The backend ended the response body before it was complete, after the status and the headers had already been sent. The API consumer received a valid response with a truncated body, so the status stays as it was, usually <code>200</code>. Available from 4.12.16.</td></tr><tr><td>503</td><td><code>GATEWAY_CLIENT_CONNECTION_POOL_EXHAUSTED</code></td><td>The connection pool and its wait queue are both full, so the Gateway sheds the load deliberately. The request never reached the backend, and it can be retried.</td></tr><tr><td>504</td><td><code>GATEWAY_CLIENT_CONNECT_TIMEOUT</code></td><td>No connection was obtained in time: pool saturation, slow DNS, or slow TCP connect. The request never reached the backend.</td></tr><tr><td>504</td><td><code>GATEWAY_CLIENT_READ_TIMEOUT</code></td><td>A connection was obtained and the request was sent, but the backend stayed silent for longer than <code>readTimeout</code>.</td></tr><tr><td>504</td><td><code>REQUEST_TIMEOUT</code></td><td>Umbrella key for the two timeout keys. Also the key that the Gateway-wide request timeout produces.</td></tr></tbody></table>

The two timeout keys carry `REQUEST_TIMEOUT` as their parent. Every other key in this table carries `GATEWAY_CLIENT_CONNECTION_ERROR`.

{% hint style="warning" %}
`GATEWAY_CLIENT_CONNECTION_POOL_EXHAUSTED` is the one key whose status differs from its parent's: `503` against `502`. With no response template in play, it returns `503` as expected. But a template configured on `GATEWAY_CLIENT_CONNECTION_ERROR` — or a `DEFAULT` one — applies to it as well, and a template always dictates the status: pool exhaustion then reaches the consumer as `502`. Give this key a template of its own when the distinction matters.
{% endhint %}

### On `GATEWAY_CLIENT_CONNECTION_CLOSED` and `GATEWAY_CLIENT_STREAM_ENDED_EARLY`

These keys are misread more often than any other. Neither means that the API consumer went away, and neither means that the Gateway timed out. Both mean the connection closed while the response was still incomplete in HTTP terms.

What separates them is **how far the response had got**:

* `GATEWAY_CLIENT_STREAM_ENDED_EARLY` — the status and the headers had already been sent. The API consumer received a valid response, only with a truncated body. The request did not fail, so the status stays as it was and no response template applies.
* `GATEWAY_CLIENT_CONNECTION_CLOSED` — nothing had reached the API consumer yet, so the Gateway answers `502`.

The common case on streaming APIs is the first: the backend announces `Transfer-Encoding: chunked`, sends data, then closes without the terminating zero-length chunk. Any HTTP client sees the same thing. `curl` reports `transfer closed with outstanding read data remaining`.

A backend that closes *cleanly*, on a response with no announced length, produces **no error key at all**. Closing is a legitimate way to delimit the body in that case.

{% hint style="info" %}
`GATEWAY_CLIENT_STREAM_ENDED_EARLY` is available from **4.12.16**. Before that version, a truncated body was reported as `GATEWAY_CLIENT_CONNECTION_CLOSED`, like a connection that never delivered anything. If your dashboards filter on `GATEWAY_CLIENT_CONNECTION_CLOSED` to track truncated responses, add the new key to the condition when you upgrade.
{% endhint %}

{% hint style="warning" %}
**Check your timeout settings before you blame the backend.**

Both keys are also what you get when the Gateway closes the connection itself, on the endpoint's own `idleTimeout`.

From 4.12.16 the error message tells you: it states how long the backend had been silent, and, when that silence matches the configured `idleTimeout`, that the Gateway is the likely closer, naming the values involved.

On earlier versions the duration is the only clue. An `idleTimeout` produces the same duration every time, within a few milliseconds of the configured value. A genuine backend problem produces scattered durations. Note that the silence, not the total duration of the exchange, is what to compare: `idleTimeout` restarts on every byte received.

For the configuration that causes this, see [Timeout management](../prepare-a-production-environment/timeout-management.md#distinguish-a-backend-closure-from-an-idle-timeout).
{% endhint %}

## The API consumer aborted the request

The Gateway raises these keys when the **caller** goes away. It sets status `499`, but only when no status has been sent yet. On a streamed response the status is already committed, usually `200`, so only the error key is recorded and the status stays as it was.

<table><thead><tr><th width="80">Status</th><th width="330">Error key</th><th>Message</th></tr></thead><tbody><tr><td>499</td><td><code>CLIENT_ABORTED_CHANNEL_CLOSED</code></td><td>The client closed the connection</td></tr><tr><td>499</td><td><code>CLIENT_ABORTED_TCP_RESET</code></td><td>The client reset the connection</td></tr><tr><td>499</td><td><code>CLIENT_ABORTED_BROKEN_PIPE</code></td><td>The client closed the connection while the response was being written</td></tr><tr><td>499</td><td><code>CLIENT_ABORTED_DURING_REQUEST_ERROR</code></td><td>The request was aborted by the client before it was fully received</td></tr><tr><td>499</td><td><code>CLIENT_ABORTED_DURING_RESPONSE_ERROR</code></td><td>The response cannot be sent to the client because the client has aborted</td></tr></tbody></table>

The first three come from the HTTP layer of the Gateway, which classifies them from the underlying exception. The last two are a coarser fallback, used when nothing more precise was recorded.

These keys never overlap with the backend connection keys. An abort by the API consumer is always reported under a `CLIENT_ABORTED_` key, never as `GATEWAY_CLIENT_CONNECTION_CLOSED`.

## Request handling and routing

<table><thead><tr><th width="80">Status</th><th width="330">Error key</th><th>What it means</th></tr></thead><tbody><tr><td>400</td><td><code>REQUEST_NULL_BYTE_REJECTED</code></td><td>The request contained a null byte, and was rejected before processing.</td></tr><tr><td>400</td><td><code>INVALID_HTTP_METHOD</code></td><td>The HTTP method isn't usable for this endpoint.</td></tr><tr><td>400</td><td><code>CORS_PREFLIGHT_FAILED</code></td><td>The CORS preflight request didn't satisfy the configured policy.</td></tr><tr><td>401</td><td><code>GATEWAY_PLAN_UNRESOLVABLE</code></td><td>No plan could be resolved for the request: missing or invalid credentials, or no matching subscription.</td></tr><tr><td>404</td><td><code>FLOW_EXECUTION_FLOW_MATCHED_FAILURE</code></td><td>No flow matched the request while flow matching was mandatory.</td></tr><tr><td>500</td><td><code>GATEWAY_POLICY_INTERNAL_ERROR</code></td><td>A policy failed unexpectedly while streaming.</td></tr><tr><td>500</td><td><code>GATEWAY_UNEXPECTED_ERROR</code></td><td>An error reached the end of the Gateway's processing chain without being turned into a proper failure. See the note that follows this table. Available from 4.12.16.</td></tr><tr><td>503</td><td><code>NO_ENDPOINT_FOUND</code></td><td>The endpoint targeted by the request doesn't exist or isn't available. Often a dynamic routing target that matches no declared endpoint.</td></tr></tbody></table>

### On `GATEWAY_UNEXPECTED_ERROR`

The Gateway answers a bare `500` when an error reaches the end of its processing chain without having been turned into a proper failure — no response template applies on that path, so the body is empty.

Two things make this outcome easy to misread, and both are addressed from 4.12.16:

* **The status you see is not always the one the failure called for.** The `500` overwrites whatever status the request had reached. A request can therefore be reported as a `500` while carrying an error key that belongs to another status, such as a `GATEWAY_CLIENT_` key normally answered with a `502`. The Gateway log now states the status it replaced.
* **The request used to carry no key at all**, which reads as a success in any dashboard that counts failures by key. It now carries `GATEWAY_UNEXPECTED_ERROR`, with the cause in the message.

When an error key had already been attributed to the request, that key is kept — it names what actually went wrong — and the unexpected failure is recorded alongside it as a **warning**, carrying the exception. Warnings appear in the Issues panel of the request details in the Console.

{% hint style="info" %}
The Gateway log line for this path is `Unexpected error while handling request`. From 4.12.16 it carries the request and transaction ids, the status being replaced, the error already attributed, the endpoint, the elapsed time, and the cause — enough to conclude without correlating anything.
{% endhint %}

## Responses with no error key

Two cases produce a completed request that carries no key at all. Both are worth knowing when you build dashboards:

* A normal success.
* A backend that closed cleanly, on a response with no announced length. The response may be shorter than the API consumer expected, but nothing in HTTP terms was violated.

## Keys reported by policies

Policies and plugins report their own keys, in the same field. Their status and their message are defined by the policy, not by the Gateway. Custom keys set through an `interrupt` policy behave the same way.

Common examples in a typical setup: `JWT_INVALID_TOKEN`, `JWT_JWKS_RESOLUTION_ERROR`, `OAS_VALIDATION_ERROR`, `TRANSFORM_HEADERS_FAILURE`, `REQUEST_VALIDATION_INVALID`, `RATE_LIMIT_TOO_MANY_REQUESTS`, and `QUOTA_TOO_MANY_REQUESTS`.

## Use error keys in response templates

Response templates match on the error key, which lets an API return its own payload for a given failure. Target the fine-grained key to handle one case, or the umbrella key to cover a family.

{% hint style="info" %}
On connection failures, the failure carries a key and a cause, but no message. In a response template, use `{#error.cause}` rather than `{#error.message}`, which is empty for these errors.
{% endhint %}

## Related pages

* [Timeout management](../prepare-a-production-environment/timeout-management.md) — which timer produces which timeout key, and how to configure them.
* [Execution transparency analytics](execution-transparency-analytics.md) — where these keys surface in the logs and the analytics.
* [Response templates](../create-and-configure-apis/configure-v4-apis/response-templates.md) — how to map a key to a custom response.
