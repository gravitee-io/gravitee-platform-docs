# Automation API

## Overview

The Automation API provides a machine-oriented HTTP interface for managing Access Management resources declaratively. It enables infrastructure-as-code workflows by exposing domain, identity provider, certificate, and reporter resources through a stable, versioned OpenAPI specification served at the configured entrypoint. The API is designed for CI/CD pipelines, Terraform providers, and other automation tools that require idempotent, key-based resource management.

## Key concepts

### Automation API vs Management REST API

The Automation API is a separate HTTP endpoint optimized for declarative resource management. Unlike the Management REST API, which uses database-generated identifiers, the Automation API uses stable, user-defined keys for all resources. Resources created through the Automation API are isolated from those created via the Management REST API or UI. For example, identity providers created outside the Automation API are not returned by Automation API list endpoints. The API is primarily documented via the generated OpenAPI specification served at the configured entrypoint when the API is enabled (`/openapi.json` and `/openapi.yaml` — also see [Automation API Reference](../reference/automation-api-reference.md)).

#### Timestamps

The Automation API serializes server-assigned timestamps — `createdAt`, `updatedAt`, and (for certificates) `expiresAt` - as **ISO-8601 / RFC 3339 strings in UTC**, with millisecond precision and a `Z` zone designator, for example `2026-06-17T10:00:00.000Z`. The fields are read-only: they're returned on `GET` but ignored on `PUT`, so they're safe to leave in a round-tripped document.

**This timestamp format differs from the Management REST API.** The Management REST API serializes the same fields as **epoch milliseconds** (a JSON number, e.g. `1718616600000`).

### Resource keys

Every resource in the Automation API is identified by a **key**: a stable, immutable identifier you define when creating the resource. Keys are scoped to their parent resource. For example, identity provider keys are unique within a domain. Once created, a resource's key can't be changed. Keys enable idempotent PUT operations — sending the same PUT request multiple times produces the same result.

#### Example keys:

| Resource | Key Scope | Example Key |
|:---------|:----------|:------------|
| Domain | Environment | `example-domain` |
| Identity Provider | Domain | `corporate-ldap` |
| Certificate | Domain | `signing-cert` |
| Reporter | Domain | `audit-kafka` |

### System resources

Identity providers, reporters and certificates can be marked as **system resources** by setting `system: true`. System identity providers are built from the `domains.identities.default.*` configuration in `gravitee.yml` and require only a `key` field alongside `system: true` — all other configuration is inherited from the `gravitee.yml` configuration file. System resources are immutable through the Automation API. Re-PUTting a system resource is an idempotent no-op. Each domain can have at most one system identity provider, one system reporter and one system certificate.

{% hint style="info" %}
**Automation-managed domains start empty.** Unlike domains created in the console, a domain created through the Automation API is **not** seeded with a default identity provider, reporter, or certificate. Declare whatever you need explicitly — including the built-in defaults via `system: true`.
{% endhint %}

### Declarative resource management

Every PUT carries the **complete desired state** of a resource, not a partial patch. To change a single field, read the resource, edit the returned document, and PUT the whole thing back. A `GET` → edit → `PUT` round-trip is lossless and idempotent.

### Resource visibility and ownership

Resources created through the Automation API are stamped as automation-managed. Addressed by `key`, the API only ever sees, updates, or deletes its **own** resources — resources created via the console or Management REST API are invisible to its list and get-by-key operations, and a key whose deterministic id collides with a non-automation resource is rejected. This ownership boundary is what keeps automation-driven and manually managed resources from interfering with each other. (To deliberately cross it, see [Brownfield resources](#brownfield-resources).)

### Brownfield resources

*Brownfield* resources are those the Automation API did **not** create — those provisioned earlier through the console or the Management REST API. They have a database-generated internal id and no automation `key`, so key-based addressing can't see them. To manage one, address it by its internal id with the `id:` prefix (for example `id:94157683-f481-45a9-9576-83f48145a9a0`) anywhere a reference is accepted — a path segment, the PUT body `key`, or a cross-resource reference. You can mix `key` and `id:` references in a single path.

`id:` addressing behaves differently from key addressing in a few important ways:

* **Update-only** — `GET`, `PUT`, and `DELETE` require the resource to already exist; there is no create-by-id. Creation is always by `key`.
* **Non-adopting** — a PUT edits the resource's fields in place and leaves its ownership untouched. The resource is not converted into an automation-managed resource and gains no key.
* **Scope-checked** — the id must belong to the addressed parent (a child to its domain, a domain to the path environment); a cross-scope or unknown id returns `404`.
* **Not enumerable** — `id:`-reached resources never appear in list responses, so brownfield management requires you to already know the id.

## Prerequisites

Before using the Automation API, ensure the following requirements are met:

* Automation API is enabled (See [Enabling the Automation API](../getting-started/configuration/configure-automation-api.md))
* A user with organization-level permissions
* Either a JWT bearer token or an opaque user service-account access token for authentication (see following)

## Authentication

Every Automation API request must include an `Authorization: Bearer <token>` header. The OpenAPI specification endpoints (`/openapi.json` and `/openapi.yaml`) are the only exceptions and can be fetched without authentication.

Example:

```bash
curl -H "Authorization: Bearer <TOKEN>" \
  "https://<am-host>/automation/organizations/<orgId>/environments/<envId>/domains"
```

The API accepts two bearer token types.

### JWT bearer token

A JWT bearer token is the short-lived access token issued by the AM Management API authentication endpoints. Use this approach for interactive tooling, local development, or any workflow where a human user signs in and exchanges credentials for a token.

To obtain a token, call the Management API token endpoint with the user's credentials. For details, see [Authorization](../reference/am-api-reference.md#authorization).

```bash
TOKEN=$(curl -s https://<am-host>/management/auth/token \
  -u admin:adminadmin \
  -d "grant_type=password&username=admin&password=adminadmin" | jq -r '.access_token')
```

JWTs are subject to session invalidation: tokens issued before the user's last logout or username reset are rejected.

### Service account token

An opaque service-account access token is the recommended authentication method for CI/CD pipelines, Terraform providers, and other non-interactive automation. Unlike a JWT, the token is an opaque, Base64-encoded value that does not expire on a fixed schedule but can be revoked individually.

#### Create a service account

To create a service account, follow these steps:

1. Log in to your AM Console.
2. Open **Organization** from the left navigation.
3. Click **Users** under **User Management**.
4. Click **Add User**.
5. In the **User Type** section, select the **Service Account** card.
6. In the **Service Name** field, enter a meaningful name for the service account.
7. Optional: in the **Email** field, enter an address to receive notifications related to this account.
8. Click **Create**.

Assign the service account the minimum organization and environment roles required for the Automation API operations it performs.
