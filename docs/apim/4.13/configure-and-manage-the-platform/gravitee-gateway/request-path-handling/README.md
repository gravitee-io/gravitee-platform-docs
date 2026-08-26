---
description: >-
  The http.pathHandling setting decides how the Gateway treats the request path
  before it resolves the listener context path. Understand the RAW, REJECT, and
  NORMALIZE modes, and which one to choose.
---

# Request Path Handling

## Overview
`http.pathHandling` is available starting with Gravitee APIM 4.13.0. On the maintenance branches it is available starting with 4.11.26 and 4.12.18, where the default stays `RAW`.

The `http.pathHandling` setting decides how the Gateway treats the request path before it resolves the listener context path, and therefore before it enforces any plan.

Without it, the Gateway resolves the listener against the path exactly as it arrived, enforces the plan of the API that matched, then forwards that path upstream without resolving it. A receiver that conforms to [RFC 3986 §5.2.4](https://www.rfc-editor.org/rfc/rfc3986#section-5.2.4) resolves the dot segments itself, and serves a different resource than the one the Gateway authorized.

{% hint style="info" %}
`http.pathHandling` is a Gateway-wide setting. It sits in the `http` block next to the `servers` list rather than inside an entry of it, so it cannot be set for each server, each listener, or each API. It applies to every API definition version, on the reactive engine and on the legacy one.
{% endhint %}

## Modes

| Mode | Behavior |
| --- | --- |
| `RAW` | The path is used, and forwarded, exactly as received. This was the default up to 4.12. |
| `REJECT` | The Gateway answers `400` when the path is not already in its normalized form. Nothing is rewritten, and no routing decision changes. |
| `NORMALIZE` | The Gateway resolves the path, then routes, enforces the plan, and forwards on the result. This is the default from 4.13. |

## Choose a mode

**`NORMALIZE`**, the default, is the semantically correct answer. The Gateway reads the request for what it means, so `/alpha/api/../../beta/api` is a call to beta, beta's plan applies, and the request answers `401` for want of a key. Where the resolved path matches no listener, the Gateway answers `404`. The routing decision and the delivery agree again.

**`REJECT`** closes the exposure without changing any routing decision. Path traversal has more spellings than any normalizer handles, and new ones keep appearing. A normalizer canonicalizes only what it knows about, whereas a rejection also covers what has not been anticipated: any path whose normalized form differs from the one received is refused, whatever the spelling that made it differ. The cost is that a client legitimately sending a non-canonical path receives a `400` where it used to get a response. What it refuses is any path that is not canonical for this normalizer, which is not the same thing as traversal hardening for an arbitrary receiver, so read [What Path Handling does not support](path-handling-limits.md) before you treat it as one.

**`RAW`** is the mode to set when byte preservation is a requirement, typically request signing computed over the exact request line. Note that `NORMALIZE` leaves `%2F` untouched, so encoded slashes inside object keys are not a reason on their own to move to `RAW`. What `RAW` restores is dot-segment handling as received, together with the authorization bypass described under [Roll back to the previous behavior](upgrade-to-the-4-13-default.md#roll-back-to-the-previous-behavior).

### The topology decides how much this matters

When an HTTP-aware hop sits in front of the Gateway, such as an ingress controller or a reverse proxy, it usually normalizes the path before the Gateway ever sees it, and this setting is defense in depth.

With a layer 4 load balancer there is no such hop. Nothing between the client and the Gateway parses the request line, so nothing normalizes it, and the Gateway is the first and only component in the chain that can. That topology is common and fully supported, and in it this setting is not defense in depth, it is the only defense. This is the first reason not to move back to `RAW`.

## Next steps

* [Upgrade to the 4.13 Path Handling Default](upgrade-to-the-4-13-default.md). Understand what the new default changes for an existing deployment, and work through the upgrade checklist.
* [Configure Request Path Handling](configure-path-handling.md). Set the mode in `gravitee.yaml`, the `.env` file, or Helm values.
* [What Path Handling does not support](path-handling-limits.md). No mode resolves or refuses an encoded separator, a double encoding, or an overlong UTF-8 sequence, and `NORMALIZE` does not protect a path-based allow or deny rule against a segment carrying parameters.
