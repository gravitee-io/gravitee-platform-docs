---
hidden: false
noIndex: false
description: Create and manage the resources that the policies of an LLM, MCP, or A2A Proxy reference at runtime. Follow the steps to add, edit, or remove one.
---

# Configure resources for your proxies

Each LLM Proxy, MCP Proxy, and A2A Proxy detail view includes a **Resources** page that manages the resources of the proxy. A resource holds shared configuration, such as a cache, an OAuth provider, or a guardrail detector. Policies reference the resource by name at runtime instead of embedding their own copy of the connection details.

For the AI resource types that the AI policies call, and how the AI Gateway loads their models, see [AI resources](ai-resources.md).

## Open the Resources page

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
3. Select the proxy you want to configure.
4. Under **Design** for an LLM Proxy, or under **General** for an MCP Proxy or an A2A Proxy, select **Resources**.

<!-- TODO: Screenshot of the Resources page listing a configured resource -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-resources.png" alt=""><figcaption><p>The Resources page</p></figcaption></figure>

Until the proxy has a resource, the page shows a **No resources yet** card instead of the table.

## Read the resource list

The table lists one row per resource, with the following columns:

| Column       | Description                                             |
| ------------ | ------------------------------------------------------- |
| **Resource** | The name of the resource, next to the icon of its type. |
| **Type**     | The resource type.                                      |
| **Status**   | **Enabled** or **Disabled**.                            |

Each row ends with an actions menu that offers **Edit**, **Enable** or **Disable**, and **Delete**. To find a resource, use the search field, which matches the name and the type. The table shows 10 resources per page by default.

## Add a resource

To add a resource, follow these steps:

1. Click **Add resource**.
2. In the **Select resource type** step, select a resource type, and then click **Next**. The list offers the resource plugins installed on your platform, and the search field filters it.
3. Enter a **Resource name**. The name is unique within the proxy, and policies reference the resource by this name, so keep it stable once it's in use.
4. Complete the **Configuration** form. The fields come from the configuration schema of the selected resource type.
5. Click **Next**.
6. In the **Review & create** step, check the resource details, and then click **Create resource**.

The new resource appears in the table with its **Status** set to **Enabled**.

## Edit a resource

To edit a resource, follow these steps:

1. Open the actions menu of the resource, and then click **Edit**.
2. Adjust the **Resource name** or the **Configuration** form. The resource type can't be changed.
3. Click **Next**.
4. In the **Review & save** step, check the changes, and then click **Save changes**.

## Enable or disable a resource

To toggle a resource, open its actions menu, and then click **Enable** or **Disable**. The **Status** column shows the new state.

## Remove a resource

To remove a resource, follow these steps:

1. Open the actions menu of the resource, and then click **Delete**.
2. In the **Remove this resource?** dialog, click **Remove resource**.

{% hint style="warning" %}
Policies that reference the removed resource fail until they're updated. The **Remove this resource?** dialog carries this warning.
{% endhint %}

## Deploy the change

Saving a resource change doesn't deploy it. The proxy shows the **This API is out of sync** banner until the change is deployed. Click **Deploy** on the banner, and then confirm to push the configuration to the gateway.

## Verification

To verify a resource is configured as expected, follow these steps:

1. Add a resource, and leave it enabled.
2. Click **Deploy** on the **This API is out of sync** banner, and then confirm.
3. Return to the **Resources** page. The resource is listed with its **Status** set to **Enabled**, and the out-of-sync banner is gone.

<!-- TODO: Screenshot of the Resources page after deployment, with the resource listed as Enabled -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-resources-verification.png" alt=""><figcaption><p>The deployed resource</p></figcaption></figure>

## Next steps

* [AI resources](ai-resources.md). Compare the resource types that the AI policies call at runtime.
* [Configure text classification](configure-text-classification.md). Tune the **AI - Prompt Guard Rails** policy that reads its model from a text classification resource.
* [Configure an LLM Proxy](configure-an-llm-proxy.md). Cover the rest of the post-creation configuration of an LLM Proxy.
