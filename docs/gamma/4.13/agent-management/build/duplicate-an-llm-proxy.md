---
hidden: false
noIndex: false
description: Copy an existing LLM Proxy with a new context path and version instead of rebuilding it in the wizard. Follow the steps to duplicate one.
---

# Duplicate an LLM Proxy

When you run several LLM Proxies over a consistent set of providers and policies, copying one is faster than repeating the wizard. The **Duplicate** action creates a new LLM Proxy from the source proxy's configuration. It asks you for the context path and version that the copy can't share with its source.

Use **Duplicate** to copy a proxy inside one environment. To move a proxy to a different environment, export it and import the file there instead. See [Export and import an LLM Proxy](export-and-import-an-llm-proxy.md).

## Duplicate the proxy

To duplicate an LLM Proxy, complete the following steps:

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**.
3. Select the LLM Proxy that you want to copy.
4. Under **General**, select **Configuration**.
5. Select **Duplicate**.

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-llm-proxy-duplicate-sheet.png" alt=""><figcaption><p>The Duplicate LLM proxy panel with the Context path and Version fields and the include checkboxes</p></figcaption></figure>

6. In the **Duplicate LLM proxy** panel, complete the following fields:

| Field            | Required | Description                                                                                                                                                                                      |
| ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Context path** | Yes      | The path prefix that consumers call on the copy. It starts with `/`, is longer than three characters, uses only letters, digits, and the `/`, `.`, `-`, and `_` characters, and holds no `//`. The source proxy's own path is shown as a hint. |
| **Version**      | Yes      | The version of the copy, up to 32 characters. The source proxy's version is shown as a hint, and isn't used until you type a value.                                                                |

7. Under **Include additional data**, clear any of the **Groups**, **Members**, **Pages**, and **Plans** checkboxes you want to leave out of the copy. All four are selected by default.
8. Select **Duplicate**.

The console creates the copy and opens its **Configuration** page.

The copy takes the source proxy's name. Give it a distinct name from its **Configuration** page when you want the two to be told apart in the **LLM Proxies** list.

## Context path availability

The panel checks the context path against the other APIs of the environment as you type, with a short pause after your last keystroke. **Checking availability** appears while the check runs, and a path that's already in use is reported under the field.

The check runs again when you select **Duplicate**, so a path taken between your keystroke and your submission is still caught. If the check itself can't reach the platform, the panel doesn't block you and the platform enforces the path on submission.

## Deploy the copy

The copy is created but not deployed. Deploy it from the out-of-sync banner on the copy once its configuration is right. See [Configure LLM Proxy deployment](configure-llm-proxy-deployment.md).

{% hint style="warning" %}
Clearing the **Plans** checkbox leaves the copy with no plan, and a proxy with no plan can't be consumed. Add a plan to the copy before you deploy it. See [Create an LLM Proxy](create-an-llm-proxy.md) for the plan types.
{% endhint %}

## Verification

To verify the copy, follow these steps:

1. Under **Secure**, select **LLM Proxies**. The list holds a second proxy with the source proxy's name.
2. Open the copy, and under **Design**, select **Models**. The providers and models match the source proxy.
3. Under **Consumer Access**, select **Plans**. The plans are present when you left the **Plans** checkbox selected, and absent when you cleared it.
4. Deploy the copy from the out-of-sync banner, and send it a prompt on its own context path as described in [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). The gateway routes the request.

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-llm-proxy-duplicate-result.png" alt=""><figcaption><p>The Configuration page of the duplicated LLM Proxy</p></figcaption></figure>

## Next steps

* **Adjust the copy**. Change its providers, models, and policies. See [Configure an LLM Proxy](configure-an-llm-proxy.md).
* **Change its entrypoints**. Add context paths or switch to virtual hosts. See [Configure LLM Proxy entrypoints](configure-llm-proxy-entrypoints.md).
* **Publish the copy**. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).
