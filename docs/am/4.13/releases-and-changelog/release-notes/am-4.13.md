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

#### **DPoP sender-constrained tokens**

* AM supports OAuth 2.0 Demonstrating Proof of Possession (RFC 9449). A client that sends a `DPoP` proof header to the token endpoint receives an access token whose `token_type` is `DPoP` and that's bound to the client's key through the `cnf.jkt` claim. The refresh token is bound to the same key, and the `dpop_jkt` authorization parameter binds an authorization code to the key before the client redeems it.
* The AM Gateway endpoints that accept an access token, such as the UserInfo endpoint, the dynamic client registration endpoints, the UMA 2.0 protection API, and the SCIM 2.0 endpoints, reject a DPoP-bound token that's presented without a valid proof or with the `Bearer` scheme. Tokens issued without a proof keep working as bearer tokens.
* The new **DPoP-bound access tokens** application setting and the new **Require DPoP for all clients** security domain setting make the proof mandatory at the token endpoint. The security domain settings also carry an allowlist of proof signing algorithms, which the OpenID discovery document advertises as `dpop_signing_alg_values_supported`.
* New `handlers.oauth2.dpop` properties in the AM Gateway `gravitee.yml` control the validity window of a proof and the replay cache. See [Demonstrating Proof of Possession (DPoP)](../../guides/auth-protocols/oauth-2.0/demonstrating-proof-of-possession-dpop.md) for the configuration and the client contract.

#### **Reporter attribute mapping**

* File, Kafka, and TCP reporters export extra fields alongside each audit record they write. Each mapping pairs an expression, evaluated against the audit context when the event is reported, with the name that value takes in the exported payload. A reporter carries up to 20 mappings.
* The audit context carries the user the event concerns, the application it was raised for, the request's `ip` and `userAgent`, and the audit record's own `id`, `type`, `transactionId`, and `status`.
* The new **Limit to event types** list restricts the mapped attributes to the event types you select. Leaving it empty exports them on every audit record the reporter writes, and it never changes which events AM reports.
* AM never exports an attribute whose name holds a credential or a token. The new `reporters.audits.attribute_mappings.denied_attributes` property in `gravitee.yml` extends that built-in list.
* A reporter with no attribute mappings exports the payload it exported before. See [Reporters](../../getting-started/configuration/configure-reporters.md#attribute-mapping) for the configuration.

#### **OCI KMS certificate plugin**

* A new Enterprise Edition certificate plugin signs the tokens of a security domain with a key stored in an Oracle Cloud Infrastructure (OCI) Vault. AM reads the public key from the vault and sends every signing operation to OCI KMS.
* The plugin authenticates to OCI with an API key, an OCI config file, instance principals, resource principals, or OKE workload identity, and signs with `RS256`, `RS384`, `RS512`, `PS256`, `PS384`, `PS512`, `ES256`, `ES384`, or `ES512`.
* The plugin isn't bundled with AM. Install it on the AM Management API and the AM Gateway, with a license that contains the `enterprise-secret-manager` pack. See [Configure the OCI KMS certificate plugin](../../guides/certificates/oci-kms-certificate-plugin.md).

#### **Data planes in the Automation API**

* The Automation API lists, registers, updates, and deletes the data planes of an environment at `/organizations/<orgId>/environments/<envId>/dataplanes`. A data plane is identified by its `id`, responses never include its `configuration`, and every Management API node serves a new data plane without a restart.
* A `PUT` that repeats a data plane's stored settings leaves it as it is, and a data plane that a security domain uses isn't deleted. An update that points a data plane at another database doesn't copy any data: the Management API uses the new store, and Gateways keep the store their own configuration names.
* Data planes registered through the Management API internal API are reached with the `id:` prefix, and an update by `id:` doesn't add them to the Automation API list.
* A domain `PUT` that updates a security domain no longer requires `dataPlaneId`, and one that names a different data plane is rejected with `400`. See [Breaking Changes for Access Management](../../getting-started/install-and-upgrade-guides/breaking-changes-for-access-management.md).
* The `ORGANIZATION_OWNER`, `ORGANIZATION_PRIMARY_OWNER`, `ENVIRONMENT_OWNER`, and `ENVIRONMENT_PRIMARY_OWNER` roles, which listed and read data planes before, now also register, update, and delete them. See [Automation API](../../guides/automation-api.md#manage-data-planes).

#### **Data planes provisioned at runtime**

* A data plane can be added while the Management API runs, by posting its definition to the `/_node/dataplanes` endpoint of the Management API internal API. Every Management API node loads it without a restart, and loads it again after one. Its `id` can't be `default` or an identifier already declared in `gravitee.yml`, and the response never returns the credentials.
* A provisioned data plane is offered in the **Data Plane** list when a security domain is created in its environment. Before the first domain is created on it, the Management API checks that the store answers with the settings it was provisioned with, and rejects the domain when it doesn't. The data planes declared in `gravitee.yml` aren't checked. The new `dataPlaneVerification` properties control the check.
* `GET /_node/dataplanes` lists the provisioned data planes and `DELETE /_node/dataplanes/{id}` removes one, once no security domain uses it. The new `DATA_PLANE_CREATED`, `DATA_PLANE_UPDATED`, and `DATA_PLANE_DELETED` audit events record every change.
* A security domain created without a `dataPlaneId` is assigned to `default` when `default` is the only data plane the node declares and none has been provisioned for the environment. AM Console shows the identifier beside each data plane name.
* Deleting a security domain now purges everything it holds in its data plane, including users, groups, WebAuthn credentials, devices, login attempts, password history, consents, UMA resources, and user activity, and the deletion still completes when the data plane can't be reached. See [Configure Multiple Data Planes](../../getting-started/install-and-upgrade-guides/configure-multiple-data-planes.md#provision-a-data-plane-at-runtime).

#### **Identity provider storage on the system cluster**

* The new `repositories.system-cluster-restricted` property in the Management API `gravitee.yml` lets the platform own where a MongoDB identity provider created with **Use System Cluster** stores its users: the database is the one the node serving the provider reads, and the collection is named after the provider. Under this rule, those settings and the **Use System Cluster** toggle of every MongoDB identity provider can't be changed after creation. Gravitee-managed deployments always apply it.
* The default identity provider created with a security domain now relies on the system cluster instead of carrying its own copy of the management connection settings, and reuses the security domain's data plane when `repositories.system-cluster` is `gateway`. The new `domains.identities.default.useSystemCluster` property turns that off on a self-hosted installation. See [MongoDB](../../guides/identity-providers/database-identity-providers/mongodb.md#store-users-on-the-system-cluster) and [Repositories & Data Plane](../../getting-started/configuration/configure-repositories.md#system-cluster).
