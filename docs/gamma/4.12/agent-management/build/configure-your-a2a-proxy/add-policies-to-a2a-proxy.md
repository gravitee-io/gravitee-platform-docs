---
hidden: false
noIndex: false
description: Use the Policy Studio to add, configure, and manage policies on your A2A Proxy.
---

# Add policies to your A2A Proxy

You can use the Policy Studio to add, configure, and manage policies on your Agent-to-Agent (A2A) Proxy. Policies enforce security, modify payloads, and control traffic behavior between autonomous agents.

## Configure A2A policies

To attach policies to your A2A Proxy:

1. In the Gamma console, navigate to **Agent Management**. In the **Secure** section of the sidebar, select **A2A Proxies**.
2. Select your A2A proxy from the proxy list.
3. In the **Design** section of the proxy sidebar, select **Policy Studio**.
4. Create a flow. A flow is a combination of a selector, such as a path or condition, and a set of policies to execute when the selector matches. Click **Add plan flow** to scope the flow to a subscription plan, or **Add common flow** to apply the flow to all traffic regardless of plan.
5. Select the flow, and then click **Browse all** on either the **Request Phase** or the **Response Phase**. The **Add Policy** panel lists the policies available for the phase you selected. To narrow the list, use the search field or the **Category** filter.
6. Select a policy to review its documentation, and then click **Add to flow**.
7. Select the policy in the flow to configure its specific properties.
8. Click **Save** to persist your changes.
9. Click **Deploy** to push your changes to the AI Gateway. Until you deploy, the proxy reports that it is out of sync and your changes are not live.
