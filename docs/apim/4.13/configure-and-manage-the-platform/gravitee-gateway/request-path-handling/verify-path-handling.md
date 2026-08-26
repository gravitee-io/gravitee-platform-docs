---
description: >-
  Confirm which path handling mode a Gateway actually came up in, and observe
  the path values it holds for a request that carries dot segments.
---

# Verify Path Handling on a Running Gateway

## Overview

An unrecognized `http.pathHandling` value does not stop the Gateway. It falls back to `RAW`, which means the configured mode and the active mode can differ without anything failing.

This page shows how to confirm from the startup log which mode a Gateway actually came up in, what each mode logs at runtime, and how to observe the `path`, `pathInfo`, and `uri` values it holds for a request that carries dot segments.

## Confirm the active mode

At startup the Gateway logs the mode actually in force, in every mode including the default:

```
Request path handling is set to NORMALIZE: dot segments are resolved before the listener is resolved
```

An unrecognized value does not stop the Gateway. It logs a `WARN` naming the accepted values, falls back to `RAW`, and the startup line then reports `RAW`. That line is what confirms, positively, the mode the Gateway actually came up in, which matters on 4.13 because a mistyped value silently drops the deployment back to the pre-4.13 behavior.

Under `NORMALIZE`, the Gateway logs at `DEBUG` every time a path actually changed, carrying both forms:

```
Path normalized from [/proxyv4/a/../b] to [/proxyv4/b]
```

Under `REJECT`, each refusal logs at `WARN`:

```
Rejecting request /proxyv4/a/../b, returning BAD_REQUEST (400)
```

Refusals are also sent to the configured reporter, under a flag of their own, and never appear in the Console. See [Report rejected requests](configure-path-handling.md#report-rejected-requests).

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

Under `RAW` this setting does nothing to it: the Gateway neither refuses nor rewrites the path. What the caller receives then depends on the rest of the chain, the HTTP server layer that parses the request line or the backend that finally reads the path, and it can differ between versions. A `400` observed under `RAW` is not this setting at work, and the `Rejecting request` log line above is what tells a Gateway rejection from any other.

### In the Debug console

Under `NORMALIZE`, the Inspector's **Path** row shows the resolved path rather than the one submitted in the debug form.

Under `REJECT`, a debug session on a non-canonical path ends on a red `400 - Bad Request` with an empty timeline.

## Next steps

* [Request Path Handling Reference](path-handling-reference.md). Read what each mode does to the path, and the `path`, `pathInfo`, and `uri` values that follow from it.
* [What Path Handling does not support](path-handling-limits.md). Check the shapes that pass verification in every mode because no mode acts on them.
