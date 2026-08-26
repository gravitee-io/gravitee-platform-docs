---
description: >-
  What the NORMALIZE and REJECT modes each do to a request path, the values the
  Gateway holds afterwards, and the conditions REJECT refuses on.
---

# Request Path Handling Reference

## Overview

This page is the reference for what each active mode does to a request path: everything `NORMALIZE` resolves, decodes, merges, or refuses before the listener is resolved, the `path`, `pathInfo`, and `uri` values that follow from it, and the exact conditions `REJECT` answers `400` on.

`RAW` uses and forwards the path exactly as received, so it appears here only for comparison.

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

Because `pathInfo` feeds analytics and path mappings, reported paths become the resolved ones under `NORMALIZE`. That is a visible change in dashboards built on `pathInfo`. Dashboards built on `uri` are unaffected, which is what lets you correlate with the logs of whatever sits in front of the Gateway. Where the two disagree, the request carried something the Gateway resolved, and that disagreement is itself the signal.

## What REJECT changes

`REJECT` answers `400` to any request whose path is not already in its normalized form, and rewrites nothing. A path that is already canonical is routed exactly as it is under `RAW`, so no routing decision and no upstream request line changes.

The response body is `The request path is not in its normalized form.`, sent as `text/plain`. Override both with `http.errors[400].message` and `http.errors[400].contentType`. When the request's `Content-Type` is `application/grpc`, the Gateway also sets `grpc-status: 3` (`INVALID_ARGUMENT`) and `grpc-message` on the response, so the refusal carries a gRPC reason and not only an HTTP status.

`REJECT` refuses on exactly the conditions that `NORMALIZE` acts on: a path that is empty or does not start with `/`, two consecutive separators, a segment that is `.` or `..`, a percent sequence that decodes to an unreserved character, and a percent sequence that is truncated or not hexadecimal.

It deliberately accepts two shapes that a coarser filter would refuse, because both are common and both are already canonical:

* a dot inside a segment, such as `/v1/orders/12345.json`
* a percent sequence that stays encoded because it does not decode to an unreserved character, such as `/a/b%2Fc`

## Next steps

* [What Path Handling does not support](path-handling-limits.md). The path shapes neither mode resolves nor refuses, and why a segment carrying parameters can defeat a path-based allow or deny rule.
* [Verify Path Handling on a Running Gateway](verify-path-handling.md). Observe these values on a running Gateway rather than inferring them.
