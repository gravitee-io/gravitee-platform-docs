---
description: Configuration guide for domain secrets.
---

# Domain Secrets

Gravitee offers an [integration](../secret-providers.md) with secret managers to obscure secrets and avoid clear text credentials that are stored in configuration files. Gravitee's secret manager integrations rely on the `secret-provider` plugin type.

You can obscure secrets in `gravitee.yml`, Helm charts, and environment variables.

This feature is available for the Gateway and Management API.

Also, Access Management grants access to the secret provider at domain definition level to provide secret resolution in plugin configurations.&#x20;

For more information about Sensitive Data Management in domain definition, see the following articles:

<table data-view="cards"><thead><tr><th></th></tr></thead><tbody><tr><td><a href="configure-secret-providers.md">Configure Secret Providers</a></td></tr><tr><td><a href="apply-secret-to-domains.md">Apply Secret to Domains</a></td></tr><tr><td><a href="plugins-support.md">Plugins Support</a></td></tr></tbody></table>
