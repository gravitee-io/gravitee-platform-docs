---
hidden: false
noIndex: false
description: Choose which API Gateway instances load an A2A Proxy by assigning sharding tags. Follow the steps on the Deployment Configuration page.
---

# Configure deployment

The **Deployment Configuration** page controls where this A2A Proxy is deployed on the gateway mesh. Only gateway instances advertising matching sharding tags load its API definition.

To open the page, follow these steps:

1. Click **A2A Proxies** in the module sidebar.
2. Select your A2A Proxy.
3. Click **Deployment** in the A2A Proxy sidebar.
4. Click **Configuration**.

<!-- TODO: Screenshot of the Deployment Configuration page with sharding tags -->

To edit this page, you need the `API_DEFINITION` permission with Update access. Without it, the tag picker is disabled and the page reads **You do not have permission to change sharding tags for this API.**

## Assign sharding tags

The **Sharding tags** section lists the tags defined for your organization. To assign them, follow these steps:

1. Click the tag field, and then select a tag from the list. Gateways advertise matching tags, and only those instances load this API definition.
2. Repeat for each tag you want to assign.
3. Click **Save changes**, or **Discard** to revert.

Each selected tag appears as a chip. To remove one before you save, click **Remove {tag name}** on its chip. To filter the list, type in the tag field. When nothing matches, the list reads **No matching tags**. **Save changes** and **Discard** appear only once the selection differs from the saved one.

Tags assigned to the proxy but no longer defined for the organization still appear as a chip, and they're kept when you save.

When no tags exist, the page reads **No sharding tags configured**. Sharding tags are managed at the organization level under the Gateway settings.

When the tags can't be loaded, the page reads **Failed to load sharding tags. Please try again.**

{% hint style="info" %}
When the A2A Proxy is managed by the Kubernetes operator, the page shows **This API is managed by the Kubernetes operator. Sharding tags can only be changed from its source definition.**
{% endhint %}

Saving the selection marks the A2A Proxy out of sync. Deploy it to push the change to the gateway.

## Verification

To verify the deployment configuration is working as expected, follow these steps:

1. Assign a sharding tag that one of your gateway instances advertises, and click **Save changes**.
2. Deploy the A2A Proxy.
3. Send a request through a gateway instance advertising the tag. The request is served. Gateway instances without a matching tag don't load the API definition.
