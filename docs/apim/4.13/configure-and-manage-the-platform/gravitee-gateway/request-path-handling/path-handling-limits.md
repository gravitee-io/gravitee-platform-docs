---
description: >-
  The path shapes no mode resolves or refuses, and why a segment carrying
  parameters can defeat a path-based allow or deny rule.
---

# What Path Handling does not support

## Overview

No path handling mode makes the Gateway a general defense against path traversal, and `REJECT` in particular refuses less than its name suggests.

This page lists the path shapes that are canonical for this normalizer, and are therefore neither resolved nor refused in any mode, and it explains the one case where the Gateway is deliberately stricter than RFC 3986: a dot segment carrying path parameters. It ends with what that asymmetry costs a path-based allow or deny rule.

## What the modes do not cover

Both active modes assume a receiver that decodes percent sequences once ([RFC 3986 §2.3](https://www.rfc-editor.org/rfc/rfc3986#section-2.3)) and treats only `/` as a segment separator. Against a receiver that does something else, the following shapes are canonical for this normalizer. They are neither resolved nor refused, in any mode:

| Shape | Example |
| --- | --- |
| Encoded separator | `..%2f..` |
| Double encoding | `%252e%252e` |
| Overlong UTF-8 | `%c0%ae` |
| Null byte | `%00` |
| Backslash treated as a separator | `..\..` |
| Segment parameters on an ordinary segment | `/admin;x/secret` |

`REJECT` refuses paths that are not canonical. It is not traversal hardening for an arbitrary receiver. An operator who reads `REJECT` and understands "protected against path traversal" is mistaken, and it is the most expensive misunderstanding to leave in place, because it is the one that stops a platform from hardening the components that do decode these forms.

## Dot segments carrying path parameters

A path segment can carry parameters after a `;`. RFC 3986 §5.2.4 resolves only the exact strings `.` and `..`, so by the specification `..;x` is an ordinary segment. The Servlet specification is equally clear that a container strips `;params` from every segment *before* it resolves dot segments, which is what Tomcat, Jetty, and Spring do.

The Gateway takes the second reading and treats a segment that is entirely dots before the `;` as a dot segment, because a Gateway cannot know what sits behind it. Being stricter than the receiver costs an over-refused request. Being laxer authorizes one resource and lets another be served.

| Request | `RAW` | `NORMALIZE` | `REJECT` |
| --- | --- | --- | --- |
| `/proxyv4/orders/..;/echo` | routed on `/proxyv4/orders/..;/echo` | routed on `/proxyv4/echo` | `400` |
| `/proxyv4/orders;v=2/echo` | `200` | `200` | `200` |

Only a segment that is entirely dots before the `;` counts as a dot segment. An ordinary segment carrying parameters is untouched in every mode.

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

## Next steps

* [Configure Request Path Handling](configure-path-handling.md). Change the mode, and enable reporting so you can see the paths being refused.
* [Upgrade to the 4.13 Path Handling Default](upgrade-to-the-4-13-default.md). Work the shapes above into the upgrade checklist before you rely on the new default.
