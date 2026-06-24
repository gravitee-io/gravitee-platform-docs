# Portal Automation API Overview

## Overview

The Portal Automation API enables CI/CD-driven configuration of next-generation developer portals through declarative resource definitions. Platform administrators and DevOps teams can define portal structure, published APIs, and documentation as code, allowing the API Management platform to reconcile desired state into live portal navigation trees. The API is consumable from Gravitee Kubernetes Operator (GKO) custom resources or Terraform providers.

## Key Concepts

### Portal

A Portal represents a next-generation developer portal instance bound to an environment. Each portal maintains its own navigation hierarchy, published API catalog, and documentation library. By default, one portal per environment is permitted; the `automation.portal.allowMultiplePortalPerEnv` configuration property controls this constraint.

Portal identifiers are derived deterministically from human-readable IDs (HRIDs) using the pattern `HRIDToUUID.portal().context(executionContext).hrid(hrid).id()`, ensuring idempotent create-or-update operations. Portals with the same ID in different environments are treated as distinct resources.

When a new environment is created via Cockpit, a default portal with HRID `default-portal` and name `Default Portal` is automatically created.

### Navigation Path

Navigation paths define the portal's folder hierarchy as a flat list of slash-separated strings (e.g., `/projects/alpha`, `/projects/alpha/docs`). Intermediate folders are created implicitly when not listed explicitly. Listing a path explicitly is the only way to attach optional metadata such as `displayName` (human-friendly label) or `order` (sibling display sequence).

Paths are ordered — the sequence in the input list is preserved during materialization. Each folder segment is slugified (lowercased, non-alphanumeric runs replaced with hyphens) to produce URL-safe identifiers. Slugification is idempotent: `slug(slug(x)) == slug(x)`. If a derived segment collides with a sibling, a suffix `-2`, `-3`, … is appended.

Folders match by **path** (not by ID). Path is reconstructed from the segment chain: `/a/b/c` → folder `a` (root) → folder `b` (parent=a) → folder `c` (parent=b). Order is assigned by **first appearance position** in the input list. Folder IDs are generated deterministically from `organizationId`, `environmentId`, `portalId`, and `path` using `HRIDToUUID.navigation().context(auditInfo).portal(portalId.toString()).folder(path).id()`.

Navigation path validation enforces the following rules (all errors are severe and block persistence):

* Path must not be empty
* Path must start with `/`
* Path must not contain consecutive `/`
* Path must not contain `..`
* Path must not end with `/` (when length > 1)

### Portal Listing

A Portal Listing publishes one or more APIs to specific locations in the portal navigation. Each listing entry specifies an API HRID, a `location` path matching a folder in the portal's navigation, and an optional `order` value to control display sequence relative to sibling APIs at the same location. When multiple listings place APIs at the same location, the `order` field disambiguates their display order.

Listing identifiers are derived deterministically from `(portalHrid, listingHrid)` using `HRIDToUUID.portalListing().context(auditInfo).portal(portalHrid).hrid(listingHrid).id()` to ensure idempotent updates. A unique constraint on `(environmentId, portalId, hrid)` keeps re-PUT idempotent. Conflict validation ensures two listings do not place different APIs at the same location segment.

The next-generation portal only supports V4 APIs.

### Documentation

Documentation resources represent content pages (Markdown, OpenAPI, or AsyncAPI) attached to either a portal or an API. Portal-scoped documentation appears at declared paths in the portal's top-level navigation. API-scoped documentation is materialized under every published instance of the API, with `location` paths relative to the API's internal documentation folder tree (defined by the API's `portalNavigation` field).

Documentation pages are stored with automation metadata that tracks their parent reference, name, location, and order for efficient reconciliation. Pages created via the Automation API have the `automationMetadata` field populated with reference type, reference ID, name, location, and order. Pages created outside the Automation API have the `automationMetadata` field set to `null`.

External link navigation items remain a console concern in this release — the Automation API documentation types are `GRAVITEE_MARKDOWN`, `OPENAPI`, and `ASYNCAPI` only.

## Prerequisites

* Gravitee API Management 4.12.0 or later
* `ENVIRONMENT_PORTAL` permission for all portal automation operations (create, read, update, delete)
* For Kubernetes deployments: Gravitee Kubernetes Operator with Portal, PortalListing, and Documentation CRD support
* For multi-portal environments: `automation.portal.allowMultiplePortalPerEnv` must be set to `true` in gateway configuration

## Gateway Configuration

### Portal scope control

| Property | Description | Default |
|:---------|:------------|:--------|
| `automation.portal.allowMultiplePortalPerEnv` | Controls whether multiple portals can be created in a single environment via the Automation API. When `false`, only one portal is allowed per environment; attempts to create a second portal return HTTP 400. When `true`, multiple portal records are permitted, but navigation tree materialization (folder sync, listing materialization, documentation materialization) runs only for the environment's established (first-created) portal. | `false` |

Configure this property in `gravitee.yml` or the APIM Helm chart (`api-configmap.yaml`).
