---
hidden: false
noIndex: true
---

# Reuse policies with shared policy groups

A **Shared Policy Group** allows you to configure a set of policies once and reuse them across multiple APIs or flows. This ensures consistent security and behavior enforcement while reducing repetitive configuration.

In Gamma, Shared Policy Groups act as reusable policy components within the Policy Studio. 

## Supported features

Shared Policy Groups integrate seamlessly into your API proxy flows:
* **Phase targeting**: A shared policy group is bound to a specific execution phase (e.g., request, response), ensuring it is only executed in the correct context.
* **API type compatibility**: Shared policy groups are typed and validate compatibility with your API proxy's protocol type.
* **Prerequisite messaging**: If a shared policy group has unfulfilled prerequisites, the Policy Studio will display its configuration prerequisites in the builder.

<!-- Source: types/policyStudio.ts, usePolicyStudioData.ts @ 2a91746280 -->

## Attach a Shared Policy Group

To reuse a Shared Policy Group in your API flows:

1. In the Gamma console, navigate to **API Management**.
2. Select your API proxy from the APIs list.
3. In the sidebar, select **Policy Studio**.
4. Select the flow (Common flow or Plan flow) where you want to attach the group.
5. In the policy palette, search for your **Shared Policy Group**. Shared policy groups are listed alongside standard policies.
6. Drag and drop the Shared Policy Group onto the desired phase in your flow.
7. Click **Save** to deploy the updated flow.

<!-- Source: PolicyStudioPage.tsx, usePolicyStudioData.ts @ 2a91746280 -->
