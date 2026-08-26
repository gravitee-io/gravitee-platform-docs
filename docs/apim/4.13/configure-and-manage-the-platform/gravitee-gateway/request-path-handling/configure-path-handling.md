---
description: >-
  Set http.pathHandling in gravitee.yaml, the .env file, or Helm values, and
  enable reporting for requests the Gateway refuses.
---

# Configure Request Path Handling

## Overview

`http.pathHandling` is a Gateway-wide setting. It sits in the `http` block next to the `servers` list, so it applies to every server, every listener, and every API on that Gateway.

This page shows how to set the mode in `gravitee.yaml`, in the `.env` file, or in Helm values, and how to control the reporting of the requests that `REJECT` refuses. To choose between `RAW`, `REJECT`, and `NORMALIZE`, see [Request Path Handling](README.md).

## Configure the Request Path Handling

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

The flag defaults to `true`, deliberately independent of `handlers.notfound.analytics.enabled` next to it, which defaults to `false`. A control whose value lies in telling an operator that someone is probing the platform cannot be silent by default.

{% hint style="info" %}
A rejected request does not appear in the Console. Both the platform logs and the logs explorer scope their query to concrete API ids, and a rejection is reported before any API is selected. Read rejections from the reporter output, such as Elasticsearch, a file, or TCP, rather than from the Console. This behavior is shared with unmatched context paths.
{% endhint %}

The Gateway also logs each refusal at `WARN`, which is what distinguishes a rejection it issued from a `400` returned by anything else in the chain. See [Confirm the active mode](verify-path-handling.md#confirm-the-active-mode).

## Next steps

* [Verify Path Handling on a Running Gateway](verify-path-handling.md). Confirm the mode in force, and observe the path values the Gateway holds for a request that carries dot segments.
* [Request Path Handling Reference](path-handling-reference.md). Read exactly what `NORMALIZE` changes and what `REJECT` refuses on.
