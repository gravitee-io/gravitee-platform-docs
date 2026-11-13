---
hidden: false
noIndex: false
description: Choose whether the API Gateway runs every matching policy flow or only the closest match. Follow the steps to set the flow execution mode.
---

# Control how policy flows are matched to requests

You can configure the flow execution mode to control how the API Gateway matches incoming requests against your configured policy flows. 

When configuring an API Proxy, the Gateway evaluates incoming requests against the selectors defined in your flows (such as HTTP path, method, or condition). The flow execution mode determines whether the Gateway executes multiple matching flows or stops at the best match.

## Flow execution modes

Gamma supports two flow execution modes for API Proxies:

* **Default (`DEFAULT`)**: The Gateway executes all flows that match the incoming request. This is useful when you want to apply multiple cross-cutting policies (like logging or header injection) that should trigger cumulatively on a request.
* **Best match (`BEST_MATCH`)**: The Gateway evaluates all flows and executes only the *single* flow that is the closest match to the incoming request. This is useful when you have mutually exclusive behaviors defined on overlapping paths or conditions.


By default, if no flow matches a request, the Gateway still processes it. To reject unmatched requests instead, turn on **Match required** in the Policy Studio, or set `flowExecution.matchRequired` to `true` in the API definition. The Gateway then returns a `404` response when no flow matches. A request counts as matched when an API flow, a plan flow, or an API Product plan flow matches it.

> [!NOTE]
> The Gamma console doesn't list v2 APIs, and the Policy Studio shows the flows of a v2 API as read-only.


## Configure flow execution

To change the flow execution mode for your API:

1. In the Gamma console, navigate to **API Management**.
2. Select your API proxy from the **API Proxies** list.
3. In the sidebar, select **Policy Studio**.
4. Click **Flow execution settings**.
5. In **Mode**, select **Default** or **Best match**.
6. Optional: To reject requests that match no flow, turn on **Match required**.
7. Click **Save** to persist your changes.

