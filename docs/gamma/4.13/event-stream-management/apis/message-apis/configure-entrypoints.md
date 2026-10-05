---
hidden: false
noIndex: false
description: Add, remove, and configure the entrypoints of a Message API in Event Stream Management, and set the context path that its HTTP entrypoints listen on. Follow the steps to change them.
---

# Configure entrypoints

The entrypoints of a Message API decide how clients connect to it. The **Entrypoints** page shows one card per entrypoint that your Gravitee installation offers for Message APIs, and the enabled ones are checked. The configuration of each enabled entrypoint appears below the cards.

## Open the entrypoints

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **Entrypoints**.

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-entrypoints.png" alt="The Entrypoints page of a Message API, with one card per entrypoint, the enabled ones checked, and the configuration of an enabled entrypoint below the cards"><figcaption><p>The Entrypoints page of a Message API</p></figcaption></figure>

Without permission to change the Message API's definition, the page shows a read-only list of the enabled entrypoints, their quality of service, and the context path.

## Add or remove an entrypoint

The cards cover every entrypoint that supports Message APIs, for example **HTTP GET**, **HTTP POST**, **Server-Sent Events**, and **Webhook**. A checked card is enabled on the Message API.

* To add an entrypoint, click its card. Its configuration appears below the cards.
* To remove an entrypoint, click its card again, or click **Remove** under its configuration.

A Message API keeps at least one entrypoint. While only one is enabled, its card and its **Remove** button are disabled.

Adding **Webhook** also lets the **Plans** page create Push plans. See [Manage plans](manage-plans.md). To record the calls that the gateway makes to the callback URLs of its subscribers, select **Enable callback metrics** under **Callback reporting settings** in its configuration. See [View webhook delivery attempts](view-webhook-delivery-attempts.md).

## Configure an entrypoint

Each enabled entrypoint shows the following settings:

* **Quality of service**. Appears when the entrypoint declares quality-of-service levels. Choose one of the levels it offers: **None**, **Automatic**, **At most once**, or **At least once**. A newly added entrypoint starts on **Automatic** when it offers that level.
* The entrypoint's own configuration form, built from the entrypoint. An entrypoint with nothing to configure shows **No additional configuration required.**

## Set the context path

The **Context path** field appears while at least one enabled entrypoint listens over HTTP. Of the entrypoints that Gravitee ships for Message APIs, only **Webhook** doesn't listen over HTTP, so a Message API whose only entrypoint is **Webhook** has no context path.

Enter the path that clients call, starting with `/`. A path that doesn't start with `/` shows **Context path must start with a slash (/).** under the field. When the path is empty or doesn't start with `/`, clicking **Save changes** doesn't save: the save bar shows **Fix the errors to save** with **Context path must start with a slash (/).**, and the focus moves to **Context path**.

The context path can't overlap the context path of another API in the environment, unless that API listens on a virtual host. Two paths overlap when they're identical, or when one extends the other by whole path segments. For example, `/orders` and `/orders/eu` overlap, but `/orders` and `/orders-eu` don't. When the path overlaps, the save fails, and the save bar shows **Couldn't save** with the message of the Management API.

## Save your changes

As soon as the page holds an unsaved change, a save bar at the bottom of the page shows **Unsaved changes**, **Discard**, and **Save changes**.

1. Click **Save changes**.

The console saves the entrypoints and confirms with **API updated**. The save fails when an endpoint connector of the Message API doesn't support the quality of service of an entrypoint. The change reaches the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

When the save fails, the save bar shows **Couldn't save** with the reason, and **Save changes** becomes **Try again**.

To drop your changes instead, click **Discard**. If you leave the page with unsaved changes, for example from the sidebar or the breadcrumb, the **Leave without saving?** dialog asks you to confirm. Click **Stay** to keep editing, or **Leave and discard** to leave. The browser's back and forward buttons don't ask.

## Verification

To verify that the entrypoints are saved, follow these steps:

1. Reload the **Entrypoints** page.
2. Check that the cards of the entrypoints you enabled are checked, and that **Context path** shows the path you entered, ending with `/`.
3. Check that the header of the Message API sidebar shows **Out of sync**, and, if you can deploy the Message API, that the page header shows **Deploy**.
