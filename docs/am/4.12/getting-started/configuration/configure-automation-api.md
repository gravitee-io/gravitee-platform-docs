# Automation API

## Enabling the Automation API

The Automation API is disabled by default. Enable it by setting the following properties in `gravitee.yml`:

```yaml
http:
  api:
    automation:
      enabled: true
```

{% hint style="info" %}
Requires Access Management version 4.12 or later.
{% endhint %}

When the Automation API is enabled, the OpenAPI specification is served at the configured entrypoint.

## Helm Chart Configuration

For Helm deployments, add the following to your `values.yaml`:

```yaml
api:
  http:
    api:
      automation:
        enabled: true
        entrypoint: /automation
```
