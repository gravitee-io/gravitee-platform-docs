---
description: >-
  From 4.13 the Gateway resolves the request path before it routes. Understand
  what the new default changes, work through the upgrade checklist, and roll it
  back if you need to.
---

# Upgrade to the 4.13 Path Handling Default

## Overview

The default value of `http.pathHandling` changes in 4.13, and the change alters which API a request reaches.

This page describes what that means for an existing deployment: how dot segments, percent-encoded characters, and duplicate slashes are treated once the Gateway resolves the path before it routes, the checklist to work through before you upgrade, and how to roll back if something depends on the previous behavior.

## From 4.13, `http.pathHandling` defaults to `NORMALIZE`

From 4.13.0 and later, `http.pathHandling` defaults to `NORMALIZE` .

A deployment that upgrades to 4.13 and later without changing its configuration resolves request paths before routing them. This is a breaking change, and it changes which API a request reaches.

## Request with dot segments route on the resolved path

A request carrying dot segments is now routed on the resolved path, so it can reach a different API than it did before, and it is enforced by that API's plan.

Here is an example:

Take two APIs published on the same Gateway: `alpha` on `/alpha/api/` with no plan, and `beta` on `/beta/api/` behind an API key plan.

| Request | Credential | Before 4.13 | From 4.13 |
| --- | --- | --- | --- |
| `/alpha/api/../../beta/api/echo` | none | `200`, beta's backend serves the request | `401`, beta's plan applies |
| `/alpha/api/../../elsewhere/resource` | none | `200`, outside the configured endpoint target | `404`, no listener matches |

That is the point of the change: the Gateway now routes on what the request means. So the API it selects and the plan it enforces agree with the resource the backend serves. It can still break a caller that relied on the previous behavior, and a caller that legitimately sent dot segments now lands somewhere else.

The same applies inside a single API: flow selectors, path mappings, and path parameters all read the resolved path, so a request that used to evade a path-scoped policy no longer does.

## Encoded characters are decoded

Percent-encoded unreserved characters are decoded before routing and before the request is forwarded. `%41` becomes `A`, and `%7E` becomes `~`. A backend that matches on the encoded spelling receives the decoded one, so verify it before you upgrade.

Encoded slashes are not affected: `%2F` stays `%2F` in every mode.

Duplicate slashes are also merged, so `/a//b` is routed and forwarded as `/a/b`.

## Roll back to the previous behavior

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
`RAW` restores the 4.12 behavior, including a known authorization bypass. Under `RAW` the Gateway resolves the listener on the path as received, enforces the plan of the API that matched, and forwards the path unresolved, so a receiver that resolves dot segments serves a resource the Gateway did not authorize. Treat `RAW` as a temporary measure while you fix what depends on it, not as a supported end state.

If you need the exposure closed but cannot accept a routing change, use `REJECT` instead. It answers `400` to a non-canonical path and rewrites nothing.
{% endhint %}

## Upgrade checklist

Before you upgrade to 4.13:

* Look for callers that send dot segments on purpose. Under the previous default they were routed on the path as received. Search your access logs, or the Gateway's `uri` field, for `../`, `%2e%2e`, and `..;`.
* Check any backend or policy that matches on a percent-encoded unreserved character, such as `%41` or `%7E`. It now receives the decoded form.
* Check any route that relies on a duplicate slash, such as `/a//b`. It is now routed and forwarded as `/a/b`.
* Check any caller that sends a malformed percent sequence, such as `/a%zz`. It now receives a `400` from the Gateway, where the outcome previously depended on the rest of the chain.
* Expect reported paths to change. `pathInfo` becomes the resolved path, so dashboards built on it shift. `uri` still reports the path as received.
* Decide what to do about the shapes this setting does not cover, listed under [What the modes do not cover](path-handling-limits.md#what-the-modes-do-not-cover). `NORMALIZE` is not traversal hardening for an arbitrary receiver.

## Next steps

* [Configure Request Path Handling](configure-path-handling.md). Set the mode explicitly, and enable reporting for the requests `REJECT` refuses.
* [Verify Path Handling on a Running Gateway](verify-path-handling.md). Confirm from the startup log which mode the Gateway actually came up in, because a mistyped value falls back to `RAW`.
