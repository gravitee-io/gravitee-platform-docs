---
description: Configuration guide for api secrets.
---

# API Secrets

Gravitee offers an [integration](../../../readme/integrations.md#secret-managers-integration) with secret managers to obscure secrets and avoid clear text credentials stored in configuration files. Gravitee's secret manager integrations rely on the `secret-provider` plugin type.

You can obscure secrets in `gravitee.yml`, Helm charts, and environment variables.

This feature is available for the Gateway and Management API in both Gravitee Access Management and Gravitee API Management.

{% hint style="warning" %}
This feature works for only v4 APIs.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Quick start</strong></td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Configuration</strong></td><td><a href="../configure-secrets/configuration.md">configuration.md</a></td></tr><tr><td><strong>Reference secrets in APIs</strong></td><td><a href="reference-secrets-in-apis.md">reference-secrets-in-apis.md</a></td></tr></tbody></table>
