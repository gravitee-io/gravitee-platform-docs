---
hidden: false
noIndex: true
---

# Control how policy flows are matched to requests

You can configure the flow execution mode to control how the API Gateway matches incoming requests against your configured policy flows. 

When configuring an API Proxy, the Gateway evaluates incoming requests against the selectors defined in your flows (such as HTTP path, method, or condition). The flow execution mode determines whether the Gateway executes multiple matching flows or stops at the best match.

## Flow execution modes

Gamma supports two flow execution modes for API Proxies:

* **Default (`DEFAULT`)**: The Gateway executes all flows that match the incoming request. This is useful when you want to apply multiple cross-cutting policies (like logging or header injection) that should trigger cumulatively on a request.
* **Best match (`BEST_MATCH`)**: The Gateway evaluates all flows and executes only the *single* flow that is the closest match to the incoming request. This is useful when you have mutually exclusive behaviors defined on overlapping paths or conditions.

<!-- Source: usePolicyStudioData.ts, types/policyStudio.ts @ 2a91746280 -->

> [!NOTE]
> V2 API definition proxies support the same flow execution semantics via their legacy `flowMode` configuration, which is fully compatible with the new Policy Studio interface.

<!-- Source: v2FlowAdapter.ts @ 2a91746280 -->

## Configure flow execution

To change the flow execution mode for your API:

1. In the Gamma console, navigate to **API Management**.
2. Select your API proxy from the APIs list.
3. In the sidebar, select **Policy Studio**.
4. Adjust the **Flow Execution** setting to either `DEFAULT` or `BEST_MATCH`.
5. Click **Save** to persist your changes.

<!-- Source: PolicyStudioPage.tsx, usePolicyStudioSave.ts @ 2a91746280 -->
