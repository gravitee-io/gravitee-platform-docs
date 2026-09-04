---
hidden: false
noIndex: false
description: Let consumers subscribe to the plan of an A2A Proxy from the Developer Portal, with terms to accept, a subscription form to fill in, and an approval that activates access. Follow the steps to set it up.
---

# Let consumers subscribe to your agent

A consumer gets access to an agent by subscribing an application to a plan of the A2A Proxy that exposes it. The plan decides how the consumer authenticates and whether a request is approved automatically or by you. A page of general conditions on the plan makes the consumer accept your terms, and the Developer Portal's subscription form collects the details you need before you approve. When the request is approved, the subscription becomes active and the consumer receives the credentials.

## The plan the wizard creates

When you create an A2A Proxy, the wizard's **Secure** step creates one plan and publishes it. With **API Key** the plan is named **Default API Key Plan** and reads the key as a bearer token. With **mTLS** the plan is named **Default mTLS Plan**. The plan uses manual validation, so every subscription request waits for your approval. The wizard also makes the proxy's API public and starts it.

At this version, the A2A Proxy pages in the Gamma console have no plan or subscription pages. The API behind the proxy is listed in the APIM Console with the type **A2A Proxy**, and that's where you manage its plans and its subscriptions. The API doesn't appear in the API Management module of the Gamma console, which lists HTTP proxies only.

## Prepare the plan for consumers

1. In the APIM Console, open **APIs**.
2. Select the A2A Proxy's API.
3. Under **Consumers**, click **Plans**.
4. Open the plan.
5. Set the following on the plan's general settings, and then save.

<table><thead><tr><th width="330">Setting</th><th>What it does</th></tr></thead><tbody><tr><td><strong>Page of General Conditions</strong></td><td>The documentation page that holds your terms. When it's set, the Developer Portal shows the page in a <strong>Terms and Conditions</strong> dialog when the consumer subscribes, and the subscription is created only after the consumer clicks <strong>Accept</strong>.</td></tr><tr><td><strong>Auto validate subscription</strong></td><td>Off by default on the plan the wizard created. Leave it off to approve each request yourself, or turn it on to accept requests as they arrive.</td></tr><tr><td><strong>Consumer must provide a comment when subscribing to the plan (Classic Portal only)</strong></td><td>Requires a comment from the consumer, with an optional <strong>Custom message to display to consumer</strong>. As the label says, it applies to the Classic Developer Portal only.</td></tr></tbody></table>

## Add a subscription form

The subscription form is defined once for the New Developer Portal and shown for every API a consumer subscribes to.

1. In the APIM Console, open **Settings**.
2. Under **Portal**, click **Settings**.
3. Scroll to the **New Developer Portal** section.
4. Click **Open Settings**.
5. Click **Subscription Form**.
6. Define the form, and then save.

## What the consumer does

Once the proxy's API is listed in the Developer Portal, the consumer opens it and clicks **Subscribe**. The subscription flow has four steps:

1. **Choose a plan**. The consumer picks the plan. When the plan has a page of general conditions, the **Terms and Conditions** dialog shows the page and the consumer clicks **Accept**.
2. **Choose an application**. The consumer picks the application that will hold the credentials.
3. **Configure Consumer**. For an API Key plan, the consumer chooses the API Key management mode. When a subscription form is defined, it appears here for the consumer to fill in.
4. **Review**. The consumer clicks **Subscribe**.

With manual validation, the subscription is created in **Pending** status.

## Approve the request

1. In the APIM Console, open **APIs**.
2. Select the A2A Proxy's API.
3. Under **Consumers**, click **Subscriptions**.
4. Open the pending subscription.
5. Click **Validate subscription**. In the **Validate your subscription** dialog, set a **Validation period (optional)** and a **Message (optional)**, and then click **Validate**. To refuse the request instead, click **Reject subscription**.

The subscription is accepted. For an API Key plan, the consumer sends the key as a bearer token in the `Authorization` header of every call to the proxy.

## Next steps

* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md): Create the proxy and its default plan.
* [Establish consumer access](../../api-management/build/configure-your-api-proxy/establish-consumer-access.md): Applications, subscription lifecycle, and API key management for API proxies.
