# Managing Organization Sharding Tags

## Overview

API Product deployment configuration allows platform administrators to control where API Products and their plans are deployed across gateway instances using sharding tags. By assigning organization-level sharding tags to API Products and their plans, administrators can ensure that products are served only by gateways configured with matching tags, enabling geographic distribution, environment segmentation, and multi-tenant isolation.

## Key Concepts

### Sharding Tags

Sharding tags are organization-level identifiers that control deployment placement. Each tag consists of a key, name, and optional description. Tags may be restricted to specific user groups, limiting which administrators can assign them. API Products and plans reference these tags to declare their deployment targets. Gateways configured with matching tags will index and serve the tagged products and plans; gateways without matching tags will skip them.

Console tag assignment alone is not enough — each target gateway must declare the corresponding tag key in its configuration file to index and serve tagged products. Gateway logs show whether a product is indexed or skipped with a tag mismatch debug message.

### API Product Tags

API Product tags define the maximum deployment scope for the product and all its plans. When an API Product is assigned sharding tags, only gateways whose configured tags intersect with the product's tags will index the product. A product with no tags is eligible on all tagless gateways. Product tags act as the ceiling for plan tags. No plan can be deployed to a gateway that the product itself does not cover.

Saving tags on the Deployment tab marks the product out of sync until the Deploy action is run. An "out of sync" banner does not mean the product is undeployed on gateways — it indicates that the configuration has changed and requires synchronization. After a tag change, the product shows out of sync until deployed.

### Plan Tags

Plan tags refine deployment placement within the scope of the parent API Product. Plan tags must be a subset of the product's tags. A plan with no tags inherits the product's full deployment scope, making it eligible on every gateway where the product is eligible. Plans with specific tags are indexed only on gateways that match both the product's tags and the plan's tags. Only published or deprecated plans are considered for gateway indexing.

### Member API Deployment Eligibility

Member APIs linked to an API Product can become deployable on a gateway through two paths: either the API's own sharding tags match the gateway, or the API has at least one published or deprecated product plan indexed on that gateway. For the product plan path, the product's tags must match the gateway, and the plan's tags must be empty (inheriting product placement) or match the gateway. This allows APIs without matching own tags to deploy when they have at least one indexed published or deprecated product plan on that gateway (where product tags match and plan tags are empty or matching).

An API undeploys when it loses shard eligibility — for example, when the product is removed or no longer matches, no qualifying plan remains, or tags change — not simply because a product undeploy event fired if the API is still eligible via its own tags or another product. Standalone APIs (not members of any product) deploy only when their own tags match the gateway.

### Tag Deletion and Cascading Changes

Organization tag deletion is cascading. Deleting a tag at the organization level removes it from all API Products and their plans in all environments. When tags are removed from an API Product, any plan tags that are no longer on the product are automatically stripped from affected plans. Expanding product tags does not retroactively add tags to existing plans. Clearing all product tags clears all plan tags on that product's plans. All tag changes on API Products and plans produce audit log entries on the affected resource.

## Prerequisites

- Organization-level sharding tags must be defined at **Organization → Entrypoints & Sharding Tags** before they can be assigned to API Products or plans.
- Gateway instances must declare the corresponding tag keys in their configuration files to index and serve tagged products.
- Users assigning tags must have permission to use those tags. Group-restricted tags can only be assigned by members of the specified groups.
- The API Product must be deployed after tag changes to synchronize the updated configuration to gateway instances.
- Users must have the **API_PRODUCT_DEFINITION:UPDATE** permission to assign sharding tags to API Products and to deploy API Products.
- Users must have the **API_PRODUCT_PLAN:CREATE** permission to assign sharding tags when creating a plan, or the **API_PRODUCT_PLAN:UPDATE** permission to assign sharding tags when editing a plan.
- Verifying deployment (license and compatibility check) requires the **API_PRODUCT_DEFINITION:READ** permission.

## Gateway Configuration

After creating sharding tags in the Console, you must add them to your API Gateway configuration file to enable API deployment management based on those tags.

1. Navigate to **Gateway > Entrypoints & Sharding Tags** in the Console sidebar.

2. Review the existing sharding tags in the **Sharding Tags** table. The table displays the key, name, description, and any restricted groups for each tag.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-15.png" alt="Organization settings page showing entrypoints and sharding tags configuration with a table displaying a single sharding tag named 'dit'"><figcaption></figcaption></figure>

3. If you need to delete a tag, click the delete icon in the corresponding row. The tag will be removed from the table.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-16.png" alt="Organization entrypoints and sharding tags page showing empty sharding tags table with success notification"><figcaption></figcaption></figure>

4. To create a new restricted sharding tag, click **+ Add a tag**. In the **Create a tag** dialog, enter the tag name, key, and description. Select one or more groups from the **Restricted groups** dropdown to limit deployment to members of those groups.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-17.png" alt="Edit tag dialog showing form fields for creating a restricted sharding tag with name, key, description, and restricted groups dropdown"><figcaption></figcaption></figure>

5. To create an unrestricted sharding tag, click **+ Add a tag**. In the **Create a tag** dialog, enter the tag name and key. Leave the **Restricted groups** field empty to allow all users to deploy on this tag.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-18.png" alt="Edit tag dialog showing form for creating an 'external' sharding tag with name and key fields populated"><figcaption></figcaption></figure>

6. Click **Ok** to save the tag.

7. Copy the sharding tag key from the Console and add it to your API Gateway configuration file as described in the note: "Add the sharding tag's key to the API Gateway configuration file in order to manage API deployments."
