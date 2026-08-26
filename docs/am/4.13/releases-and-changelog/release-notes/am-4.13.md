# AM 4.13

## New Features

#### **Organization licenses on Gravitee-managed deployments**

* On a Gravitee-managed deployment, AM applies the license Gravitee assigns to your organization across both the AM API and the AM Gateway, and keeps it in step with your subscription. Self-hosted installations aren't affected and keep applying the license installed on each node.
* A request that creates or updates a configuration for a plugin your license doesn't include is rejected with `403 Forbidden`, and AM Console opens an upgrade dialog instead of saving. Reading and deleting an existing configuration isn't restricted.
* A security domain that references an unlicensed plugin still deploys. The AM Gateway skips that plugin and keeps serving the rest of the domain's configuration. After an expiry or a downgrade, the new restriction takes effect the next time the domain is updated or the Gateway restarts.
* New `ORGANIZATION_LICENSE_CREATED`, `ORGANIZATION_LICENSE_UPDATED`, and `ORGANIZATION_LICENSE_DELETED` audit events record every license change. See [Gravitee AM Enterprise Edition](../../overview/open-source-vs-enterprise-am/README.md#how-am-applies-your-license) for the behavior and [Audit Trail](../../guides/audit-trail.md) for the events.

#### **Federated CIBA with rich authorization requests**

* AM accepts the RFC 9396 `authorization_details` parameter on the backchannel authentication endpoint when the selected device notifier supports rich authorization requests. AM relays the authorization details to the notifier, denies the transaction when the details approved upstream differ from the relayed details, and returns the approved details in the token response and in the access token.
* Security domains that don't select a CIBA Federation notifier keep the existing CIBA behavior. See [CIBA](../../guides/auth-protocols/ciba.md#ciba-federation) for the configuration.

#### **Select scopes to consent**

* Users choose which of the requested scopes they grant on the consent page. Each scope is presented with its own checkbox, and the authorization response and the issued tokens carry the approved scopes only.
* A new **Preselect consent for all scopes** application setting controls whether the checkboxes start checked. Applications that existed before the upgrade keep the previous all-checked behavior, and applications created in AM Console or through the AM Management API start with the setting off.
* Scopes can be marked as **Required** on the application's scopes list. AM presents a required scope first, labels it **Required**, and locks its checkbox, so users grant it whenever they allow the request.
* Customized consent page templates keep working after the upgrade. See [user consent](../../guides/user-management/user-consent.md) for the application settings, and [branding](../../guides/branding/README.md#customize-the-user-consent-page) for the template contract.

#### **Environment-scoped entrypoints on Gravitee-managed deployments**

* On a Gravitee-managed deployment, AM stores each environment's gateway access points from Gravitee Cloud as entrypoints of that environment, and the entrypoints list in AM Console shows the environment each entrypoint belongs to. Adding, editing, and deleting entrypoints in AM Console is disabled, because Gravitee Cloud is the source of truth, and switching a security domain between the context-path and virtual hosts modes is unavailable.
* AM builds user-facing URLs from the environment's entrypoint: the **Domain entrypoint url** AM Console shows for a security domain, and the links in the emails sent by the Management API and by the Gateway. A custom domain attached to the environment is preferred over its default Gravitee Cloud URL, and a request that arrived on the host of one of the environment's entrypoints keeps that host in the URLs AM builds from it.
* WebAuthn ceremonies verify against the origin of the environment entrypoint that matches the request, and a relying party ID set explicitly in a security domain's WebAuthn settings is preserved.
* Self-hosted installations keep local entrypoint management, and keep building URLs from the data plane's `gateway.url` or the Management API's global `gateway.url`. See [Entrypoints](../../guides/entrypoints.md).
