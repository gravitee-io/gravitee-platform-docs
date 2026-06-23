# API Product Deployment Configuration Overview

## Overview

API Product deployment configuration controls where API Products and their plans are deployed across gateway instances using sharding tags. Administrators assign organization-level sharding tags to API Products and their plans to target specific gateway clusters, enabling multi-region deployments, environment isolation, and selective API exposure. This capability extends the existing API sharding tag model to API Products, allowing member APIs to inherit deployment eligibility from their parent products.

## Key Concepts

### Sharding Tags

Sharding tags are organization-level identifiers that control which gateway instances serve specific API Products, plans, and APIs. Each tag consists of a key, name, and optional description. Tags may be restricted to specific user groups, limiting which administrators can assign them. Gateway instances declare their sharding tags in configuration files; only entities whose tags intersect with a gateway's configured tags are indexed and served on that gateway.

### API Product Tags

API Product tags define the maximum deployment scope for the product and all its plans. When an API Product is assigned sharding tags, only gateway instances with matching tags will index and serve the product after deployment. A product with no tags is eligible on all gateways. Product tags are validated against the organization's tag registry and the current user's allowed tags (unrestricted tags for all users; group-restricted tags only for members of those groups).

### Plan Tags

Plan tags control deployment at the plan level and must be a subset of the parent API Product's tags. Plans cannot reference tags that the product does not have. A plan with no tags inherits the product's deployment scope—it is eligible on every gateway where the parent product is eligible. Plan tags enable fine-grained control, such as deploying a premium plan only to production gateways while deploying a free plan to all regions.

### Member API Deployment Eligibility

Member APIs linked to an API Product can deploy on a gateway through two paths: their own sharding tags match the gateway, or they have at least one published or deprecated API Product plan indexed on that gateway. For the product plan path, the product's tags must match the gateway, and the plan's tags must be empty (inheriting product placement) or match the gateway. This allows APIs without matching tags to run on gateways via product eligibility. Standalone APIs (not members of any product) deploy only when their own tags match the gateway.

## Prerequisites

- Organization-level sharding tags must be defined in **Organization → Entrypoints & Sharding Tags** before they can be assigned to API Products or plans.
- Gateway instances must declare corresponding sharding tag keys in their configuration files. Console tag assignment alone does not enable deployment—the gateway must recognize the tag.
- Users assigning tags must have the `API_PRODUCT_DEFINITION:UPDATE` permission for API Products and `API_PRODUCT_PLAN:CREATE` or `API_PRODUCT_PLAN:UPDATE` for plans.
- Group-restricted tags can only be assigned by members of the specified groups.
