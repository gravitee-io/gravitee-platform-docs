---
description: >-
  From 4.13 the Gateway resolves the request path before it routes. Understand
  what the new default changes, how to roll it back, and what the RAW, REJECT,
  and NORMALIZE modes cover.
---

# Request Path Handling

## The default changed in 4.13

`http.pathHandling` defaults to `NORMALIZE` from 4.13.0. In 4.12 and earlier the default was `RAW`.

A deployment that upgrades to 4.13 without changing its configuration resolves request paths before routing them. This is a breaking change, and it changes which API a request reaches.

### What this changes for a request

A request carrying dot segments is now routed on the resolved path, so it can reach a different API than it did before, and it's enforced by that API's plan.

Take two APIs published on the same Gateway: `alpha` on `/alpha/api/` with no plan, and `beta` on `/beta/api/` behind an API key plan.

| Request | Credential | Before 4.13 | From 4.13 |
| --- | --- | --- | --- |
| `/alpha/api/../../beta/api/echo` | none | `200`, beta's backend serves the request | `401`, beta's plan applies |
| `/alpha/api/../../elsewhere/resource` | none | `200`, outside the configured endpoint target | `404`, no listener matches |

That's the point of the change: the Gateway now routes on what the request means, so the API it selects and the plan it enforces agree with the resource the backend will serve. It can still break a caller that relied on the previous behavior, and a caller that legitimately sent dot segments now lands somewhere else.

The same applies inside a single API: flow selectors, path mappings, and path parameters all read the resolved path, so a request that used to evade a path-scoped policy no longer does.

### Encoded characters are decoded

Percent-encoded unreserved characters are decoded before routing and before the request is forwarded. `%41` becomes `A`, and `%7E` becomes `~`. A backend that matches on the encoded spelling receives the decoded one, so verify it before you upgrade.

Encoded slashes are not affected: `%2F` stays `%2F` in every mode.

Duplicate slashes are also merged, so `/a//b` is routed and forwarded as `/a/b`.

### Roll back to the previous behavior

Set the mode explicitly:

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  pathHandling: RAW
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_pathHandling=RAW
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  http:
    pathHandling: RAW
```
{% endtab %}
{% endtabs %}

{% hint style="danger" %}
`RAW` restores the 4.12 behavior, including a known authorization bypass. Under `RAW` the Gateway resolves the listener on the path as received, enforces the plan of the API that matched, and forwards the path unresolved, so a receiver that resolves dot segments serves a resource the Gateway didn't authorize. Treat `RAW` as a temporary measure while you fix what depends on it, not as a supported end state.

If you need the exposure closed but can't accept a routing change, use `REJECT` instead. It answers `400` to a non-canonical path and rewrites nothing.
{% endhint %}

### Upgrade checklist

Before you upgrade to 4.13:

* Look for callers that send dot segments on purpose. Under the previous default they were routed on the path as received. Search your access logs, or the Gateway's `uri` field, for `../`, `%2e%2e`, and `..;`.
* Check any backend or policy that matches on a percent-encoded unreserved character, such as `%41` or `%7E`. It now receives the decoded form.
* Check any route that relies on a duplicate slash, such as `/a//b`. It's now routed and forwarded as `/a/b`.
* Check any caller that sends a malformed percent sequence, such as `/a%zz`. It now receives a `400` from the Gateway, where the outcome previously depended on the rest of the chain.
* Expect reported paths to change. `pathInfo` becomes the resolved path, so dashboards built on it shift. `uri` still reports the path as received.
* Decide what to do about the shapes this setting doesn't cover, listed under [What the modes don't cover](request-path-handling.md#what-the-modes-dont-cover). `NORMALIZE` isn't traversal hardening for an arbitrary receiver.

## Overview

`http.pathHandling` is available starting with Gravitee APIM 4.13.0. On the maintenance branches it's available starting with 4.11.26 and 4.12.18, where the default stays `RAW`.

The `http.pathHandling` setting decides how the Gateway treats the request path before it resolves the listener context path, and therefore before it enforces any plan.

Without it, the Gateway resolves the listener against the path exactly as it arrived, enforces the plan of the API that matched, then forwards that path upstream without resolving it. A receiver that conforms to [RFC 3986 §5.2.4](https://www.rfc-editor.org/rfc/rfc3986#section-5.2.4) resolves the dot segments itself, and serves a different resource than the one the Gateway authorized.

{% hint style="info" %}
`http.pathHandling` is a Gateway-wide setting. It sits in the `http` block next to the `servers` list rather than inside an entry of it, so it can't be set per server, per listener, or per API. It applies to every API definition version, on the reactive engine and on the legacy one.
{% endhint %}

## Modes

| Mode | Behavior |
| --- | --- |
| `RAW` | The path is used, and forwarded, exactly as received. This was the default up to 4.12. |
| `REJECT` | The Gateway answers `400` when the path isn't already in its normalized form. Nothing is rewritten, and no routing decision changes. |
| `NORMALIZE` | The Gateway resolves the path, then routes, enforces the plan, and forwards on the result. This is the default from 4.13. |

## Configure the mode

{% tabs %}
{% tab title="gravitee.yaml" %}
Set `pathHandling` in the `http` section of the `gravitee.yaml` file:

```yaml
http:
  port: 8082
  host: 0.0.0.0
  requestTimeout: 30000
  pathHandling: NORMALIZE # Supports RAW, REJECT, NORMALIZE
```
{% endtab %}

{% tab title=".env" %}
Add the variable to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_http_pathHandling=NORMALIZE
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Update the `gateway.http` section of your `values.yaml` file:

```yaml
gateway:
  http:
    pathHandling: NORMALIZE # Supports RAW, REJECT, NORMALIZE
```

The chart renders the key into the Gateway `gravitee.yml` in both the single-server and the multi-server form of the configmap.
{% endtab %}
{% endtabs %}

## What NORMALIZE changes

Normalization is a whole process, not a dot-segment feature. Under `NORMALIZE`, the Gateway applies all of the following before it resolves the listener:

* **Dot segments are resolved.** `/alpha/api/../../beta/api/echo` becomes `/beta/api/echo`. A segment that would climb above the root is discarded rather than treated as an error, as RFC 3986 requires.
* **Percent-encoded unreserved characters are decoded.** `%41` becomes `A`, and `%7E` becomes `~`, per [RFC 3986 §6.2.2.2](https://www.rfc-editor.org/rfc/rfc3986#section-6.2.2.2). This is the rule that turns `%2e%2e` into a dot segment, and it applies to every unreserved character, not only to the dot. Reserved characters are left as they are.
* **Duplicate slashes are merged.** `/a//b` becomes `/a/b`. This is a routing change of its own for anyone relying on `//`.
* **A malformed percent sequence is answered with `400`.** `/a%`, `/a%zz`, and `/a/%2e%2` have no normalized form.
* **Encoded slashes are never decoded.** `%2F` stays `%2F`, so object keys and signed paths that rely on it are unaffected.

The resolved path is then what the Gateway routes on, enforces the plan on, evaluates flow selectors and path mappings against, reads path parameters from, and appends to the endpoint target.

The path as received is still available, and still reported. `uri` keeps the bytes exactly as they arrived, in every mode.

| Value, for `GET /proxyv4/a/../b` | `RAW` | `NORMALIZE` |
| --- | --- | --- |
| `path` | `/proxyv4/a/../b` | `/proxyv4/b` |
| `pathInfo` | `/a/../b` | `/b` |
| `uri` | `/proxyv4/a/../b` | `/proxyv4/a/../b` |
| Request line sent upstream | carries `a/../b` | carries `b` |

Because `pathInfo` feeds analytics and path mappings, reported paths become the resolved ones under `NORMALIZE`. That's a visible change in dashboards built on `pathInfo`. Dashboards built on `uri` are unaffected, which is what lets you correlate with the logs of whatever sits in front of the Gateway. Where the two disagree, the request carried something the Gateway resolved, and that disagreement is itself the signal.

## What REJECT changes

`REJECT` answers `400` to any request whose path isn't already in its normalized form, and rewrites nothing. A path that's already canonical is routed exactly as it is under `RAW`, so no routing decision and no upstream request line changes.

The response body is `The request path is not in its normalized form.`, sent as `text/plain`. Override both with `http.errors[400].message` and `http.errors[400].contentType`. When the request's `Content-Type` is `application/grpc`, the Gateway also sets `grpc-status: 3` (`INVALID_ARGUMENT`) and `grpc-message` on the response, so the refusal carries a gRPC reason and not only an HTTP status.

`REJECT` refuses on exactly the conditions that `NORMALIZE` would act on: a path that's empty or doesn't start with `/`, two consecutive separators, a segment that is `.` or `..`, a percent sequence that decodes to an unreserved character, and a percent sequence that's truncated or not hexadecimal.

It deliberately accepts two shapes that a coarser filter would refuse, because both are common and both are already canonical:

* a dot inside a segment, such as `/v1/orders/12345.json`
* a percent sequence that stays encoded because it doesn't decode to an unreserved character, such as `/a/b%2Fc`

## Choose a mode

**`NORMALIZE`**, the default, is the semantically correct answer. The Gateway reads the request for what it means, so `/alpha/api/../../beta/api` is a call to beta, beta's plan applies, and the request answers `401` for want of a key. Where the resolved path matches no listener, the Gateway answers `404`. The routing decision and the delivery agree again.

**`REJECT`** closes the exposure without changing any routing decision. Path traversal has more spellings than any normalizer handles, and new ones keep appearing. A normalizer canonicalizes only what it knows about, whereas a rejection also covers what hasn't been anticipated: any path whose normalized form differs from the one received is refused, whatever the spelling that made it differ. The cost is that a client legitimately sending a non-canonical path receives a `400` where it used to get a response.

**`RAW`** is the mode to set when byte preservation is a requirement, typically request signing computed over the exact request line. Note that `NORMALIZE` leaves `%2F` untouched, so encoded slashes inside object keys aren't a reason on their own to move to `RAW`. What `RAW` restores is dot-segment handling as received, together with the authorization bypass described under [Roll back to the previous behavior](request-path-handling.md#roll-back-to-the-previous-behavior).

### The topology decides how much this matters

When an HTTP-aware hop sits in front of the Gateway, such as an ingress controller or a reverse proxy, it usually normalizes the path before the Gateway ever sees it, and this setting is defense in depth.

With a layer 4 load balancer there's no such hop. Nothing between the client and the Gateway parses the request line, so nothing normalizes it, and the Gateway is the first and only component in the chain that can. That topology is common and fully supported, and in it this setting isn't defense in depth, it's the only defense. This is the first reason not to move back to `RAW`.

## What the modes don't cover

Both active modes assume a receiver that decodes percent sequences once ([RFC 3986 §2.3](https://www.rfc-editor.org/rfc/rfc3986#section-2.3)) and treats only `/` as a segment separator. Against a receiver that does something else, the following shapes are canonical for this normalizer. They're neither resolved nor refused, in any mode:

| Shape | Example |
| --- | --- |
| Encoded separator | `..%2f..` |
| Double encoding | `%252e%252e` |
| Overlong UTF-8 | `%c0%ae` |
| Null byte | `%00` |
| Backslash treated as a separator | `..\..` |
| Segment parameters on an ordinary segment | `/admin;x/secret` |

`REJECT` refuses paths that aren't canonical. It isn't traversal hardening for an arbitrary receiver. An operator who reads `REJECT` and understands "protected against path traversal" is mistaken, and it's the most expensive misunderstanding to leave in place, because it's the one that stops a platform from hardening the components that do decode these forms.

## Dot segments carrying path parameters

A path segment can carry parameters after a `;`. RFC 3986 §5.2.4 resolves only the exact strings `.` and `..`, so by the specification `..;x` is an ordinary segment. The Servlet specification is equally clear that a container strips `;params` from every segment *before* it resolves dot segments, which is what Tomcat, Jetty, and Spring do.

The Gateway takes the second reading and treats a segment that's entirely dots before the `;` as a dot segment, because a Gateway can't know what sits behind it. Being stricter than the receiver costs an over-refused request. Being laxer authorizes one resource and lets another be served.

| Request | `RAW` | `NORMALIZE` | `REJECT` |
| --- | --- | --- | --- |
| `/proxyv4/orders/..;/echo` | routed on `/proxyv4/orders/..;/echo` | routed on `/proxyv4/echo` | `400` |
| `/proxyv4/orders;v=2/echo` | `200` | `200` | `200` |

Only a segment that's entirely dots before the `;` counts as a dot segment. An ordinary segment carrying parameters is untouched in every mode.

{% hint style="warning" %}
This is the one point where `REJECT` refuses more than RFC 3986 alone would imply. A deployment switching to `REJECT` can see `400`s on paths of this shape.
{% endhint %}

### Why ordinary segments are left alone, and what it costs you

Matrix parameters and `;jsessionid` are legitimate, and clients send them. Refusing them under `REJECT` would turn away well-formed traffic, and stripping them under `NORMALIZE` would forward a path the client never sent — toward a receiver that keeps them, that means serving a different resource, not a stricter one. A dot segment carrying parameters has neither problem, because nobody sends `..;jsessionid=1` on purpose. That asymmetry is deliberate.

The cost lands on allow and deny rules:

{% hint style="danger" %}
`/a/admin;x/secret` is canonical for the Gateway and forwarded byte for byte, while a Servlet container strips the `;x` and serves `/a/admin/secret`. A policy matching on `/admin/**` sees one path and the backend another.

`NORMALIZE` being the default in 4.13 does **not** protect a path-based allow or deny rule against this spelling. If you rely on such a rule, match the parameterized form too, or enforce the restriction somewhere that sees the resolved path.
{% endhint %}

## Report rejected requests

A request refused by `REJECT` is reported to the configured reporter, with status `400` and the URI as received. It reports under its own flag:

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
handlers:
  rejected:
    analytics:
      enabled: true
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_handlers_rejected_analytics_enabled=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  handlers:
    rejected:
      analytics:
        enabled: true
```
{% endtab %}
{% endtabs %}

The flag defaults to `true`, deliberately independent of `handlers.notfound.analytics.enabled` next to it, which defaults to `false`. A control whose value lies in telling an operator that someone is probing the platform can't be silent by default.

{% hint style="info" %}
A rejected request doesn't appear in the Console. Both the platform logs and the logs explorer scope their query to concrete API ids, and a rejection is reported before any API is selected. Read rejections from the reporter output, such as Elasticsearch, a file, or TCP, rather than from the Console. This behavior is shared with unmatched context paths.
{% endhint %}

## Confirm the active mode

At startup the Gateway logs the mode actually in force, in every mode including the default:

```
Request path handling is set to NORMALIZE: dot segments are resolved before the listener is resolved
```

An unrecognized value doesn't stop the Gateway. It logs a `WARN` naming the accepted values, falls back to `RAW`, and the startup line then reports `RAW`. That line is what confirms, positively, the mode the Gateway actually came up in, which matters on 4.13 because a mistyped value silently drops the deployment back to the pre-4.13 behavior.

Under `NORMALIZE`, the Gateway logs at `DEBUG` every time a path actually changed, carrying both forms:

```
Path normalized from [/proxyv4/a/../b] to [/proxyv4/b]
```

Under `REJECT`, each refusal logs at `WARN`:

```
Rejecting request /proxyv4/a/../b, returning BAD_REQUEST (400)
```

## Verify the behavior on a running Gateway

To observe the three values the Gateway holds, publish a v4 HTTP proxy API and attach a `mock` policy to a request flow whose selector is `START_WITH` on `/`, with the content set to:

```
path={#request.path} pathInfo={#request.pathInfo} uri={#request.uri}
```

Then call it:

```sh
curl -s --path-as-is http://localhost:8082/proxyv4/a/../b
```

{% hint style="warning" %}
Two details silently invalidate this test.

`--path-as-is` is required. Without it, curl resolves the dot segments client side and sends an already canonical request line. The Gateway then has nothing to normalize, every mode looks identical, and the test proves nothing. The tell is `uri`: it must still show the `../`, because the Gateway never rewrites it.

The flow selector must be `START_WITH` on `/`, not `EQUALS`. Every path under test carries extra segments, so an `EQUALS` selector matches none of them, the policy never runs, and the request is proxied to the endpoint instead.
{% endhint %}

A malformed percent sequence, such as `/proxyv4/a%zz`, is answered with `400` under `REJECT` and `NORMALIZE`, because it has no normalized form.

Under `RAW` this setting does nothing to it: the Gateway neither refuses nor rewrites the path. What the caller receives then depends on the rest of the chain, the HTTP server layer that parses the request line or the backend that finally reads the path, and it can differ between versions. A `400` observed under `RAW` isn't this setting at work, and the `Rejecting request` log line above is what tells a Gateway rejection from any other.

### In the Debug console

Under `NORMALIZE`, the Inspector's **Path** row shows the resolved path rather than the one submitted in the debug form.

Under `REJECT`, a debug session on a non-canonical path ends on a red `400 - Bad Request` with an empty timeline.
