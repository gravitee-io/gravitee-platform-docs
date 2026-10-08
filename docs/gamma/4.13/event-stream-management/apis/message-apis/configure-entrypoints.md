---
hidden: false
noIndex: false
description: Add, configure, and delete the entrypoints of a Message API in Event Stream Management, and set its context paths or virtual hosts. Follow the steps to change them.
---

# Configure entrypoints

The entrypoints of a Message API decide how clients connect to it, for example **HTTP GET**, **HTTP POST**, **Server-Sent Events**, or **Webhook**. The entrypoints that listen over HTTP share the context paths of the Message API, or its virtual hosts.

## Open the entrypoints

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Design** group of the Message API sidebar, click **Entrypoints**.

<figure><img src="../../.gitbook/assets/gamma-esm-message-api-entrypoints.png" alt="The Entrypoints page of a Message API, with the Exposed entrypoints, Entrypoint context-paths, and Entrypoint types cards"><figcaption><p>The Entrypoints page of a Message API</p></figcaption></figure>

The page holds three cards:

* **Exposed entrypoints**. The addresses that consumers call, as the Developer Portal lists them, each with a copy button. While no address is available, the card shows **Available once the Message API is deployed**.
* **Entrypoint context-paths**. The context paths, or the virtual hosts, of the entrypoints that listen over HTTP. The card appears only while the Message API has such an entrypoint. Of the entrypoints that Gravitee ships for Message APIs, only **Webhook** doesn't listen over HTTP.
* **Entrypoint types**. A table of the entrypoints of the Message API, with their **Entrypoint type** and **Quality of service**.

Without permission to change the Message API's definition, or when the Gravitee Kubernetes Operator manages the Message API, the page is read-only. The **Entrypoint types** table then offers a view icon instead of the edit and delete icons, and the view opens the configuration of the entrypoint with every field disabled. See [Manage general settings](manage-general-settings.md#kubernetes-managed-message-apis).

## Add an entrypoint

1. In the **Entrypoint types** card, click **Add an entrypoint**. The button is disabled when the Message API already has every entrypoint that your installation offers.
2. Select the cards of one or more entrypoints.
3. If the Message API has no entrypoint that listens over HTTP yet, and you selected one that does, enter at least one context path under **Configure your context-paths**. The rules are the same as in [Set the context paths](#set-the-context-paths).
4. Click **Add entrypoint**, or **Add entrypoints** when you selected several.

The new entrypoints start with an empty configuration, and with the **Automatic** quality of service when they offer it. To change them, edit them. To leave without adding anything, click **Back to list**.

Adding **Webhook** also lets the **Plans** page create Push plans. See [Manage plans](manage-plans.md).

## Configure an entrypoint

1. In the **Entrypoint types** table, click the edit icon of the entrypoint.
2. Change the settings you need:
    * **Quality of service**. Appears when the entrypoint declares quality-of-service levels: **None**, **Automatic**, **At most once**, or **At least once**. The list offers only the levels that the endpoints of the Message API also support.
    * The entrypoint's own configuration form, built from the entrypoint. An entrypoint with nothing to configure shows **No additional configuration required.**
    * **Dead letter queue**, for the entrypoints that support one, such as **Webhook**. See [Send failed messages to a dead letter queue](#send-failed-messages-to-a-dead-letter-queue).
3. Click **Save entrypoint**. The button stays disabled while a required field is empty or invalid.

To record the calls that the gateway makes to the callback URLs of its subscribers, edit the **Webhook** entrypoint, and select **Enable callback metrics** under **Callback reporting settings**. The **Settings** button of the **Webhooks** page sets the same option. See [View webhook delivery attempts](view-webhook-delivery-attempts.md).

### Send failed messages to a dead letter queue

A dead letter queue receives each message that the entrypoint fails to push to a subscriber. The queue is an endpoint group of the Message API, or a single endpoint of one.

1. Under **Dead letter queue**, select **Enable dead letter queue**.
2. In **Dead letter queue endpoint**, select an endpoint or an endpoint group.
3. Click **Save entrypoint**.

The list offers the endpoints and the endpoint groups of every group except the first one, which serves the Message API, and only the groups whose connector can publish messages, such as **Kafka**. When no group qualifies, the list shows **No compatible endpoint or endpoint group available**. Add a second endpoint group on the **Endpoints** page first. See [Configure endpoints and failover](configure-endpoints-and-failover.md).

While **Enable dead letter queue** is selected, **Save entrypoint** stays disabled until you select an endpoint or a group.

## Delete an entrypoint

1. In the **Entrypoint types** table, click the delete icon of the entrypoint.
2. In the **Delete entrypoint?** dialog, click **Delete**.

A Message API keeps at least one entrypoint. While only one remains, its delete icon is disabled and shows **At least one entrypoint is required.**

Deleting the last entrypoint that listens over HTTP also removes the context paths of the Message API. Adding such an entrypoint again asks for a context path.

## Set the context paths

The **Entrypoint context-paths** card lists the paths that clients call, in the **Context-path** column.

* To add a path, click **Add context-path**. The new row starts with `/`.
* To remove a path, click the remove icon of its row. A Message API keeps at least one context path, so the icon is disabled on the last row and shows **At least one context path is required.**

The console checks each path as you type, and shows the problem under the field:

* A path is required: **Context path is required.**
* A path starts with `/`, and holds only letters, digits, `/`, `.`, `-`, and `_`, without two slashes in a row: **Context path is not valid.**
* A path has more than three characters: **Context path has to be more than 3 characters long.** This rule doesn't apply in virtual-host mode.
* Two rows can't hold the same path: **Duplicated context path not allowed**. A trailing `/` doesn't make two paths different.

Once the card holds a change and a path passes these rules, the console asks the Management API whether it's available, and shows **Checking availability…** meanwhile. A path that overlaps the context path of another API in the environment shows **This context path is already in use.**, or the reason that the Management API gives. Two paths overlap when they're identical, or when one extends the other by whole path segments. For example, `/orders` and `/orders/eu` overlap, but `/orders` and `/orders-eu` don't.

### Use virtual hosts

With virtual hosts, the gateway routes a request to the Message API by its host and its path.

1. Click **Enable virtual hosts**. The table gains the **Virtual host** and **Override access** columns.
2. For each row, enter the host in **Virtual host**. When the environment restricts the domains of its APIs, select the domain in the list next to the field, and enter only the part before it.
3. Optional: Select **Enable** under **Override access**.

A virtual host is required. When the environment restricts its domains, the host must end with one of them: **Host is not valid (must end with one of restriction domain).** Two rows can't hold the same host and path: **Duplicated virtual host not allowed**.

To go back to plain context paths, click **Disable virtual hosts**. The **Switch to context-path mode?** dialog warns that every virtual host is lost. Click **Switch**.

### Save the context paths

The **Entrypoint context-paths** card has its own save bar, apart from the entrypoints. As soon as the card holds an unsaved change, the bar shows **Unsaved changes**, **Discard**, and **Save changes**.

1. Click **Save changes**.

While a path is invalid, or still being checked, **Save changes** doesn't save: the bar shows **Fix the errors to save** with the reason, and the focus moves to the invalid field. When the save fails, the bar shows **Couldn't save** with the reason, and **Save changes** becomes **Try again**.

To drop your changes instead, click **Discard**. If you leave the page with unsaved changes, for example from the sidebar or the breadcrumb, the **Leave without saving?** dialog asks you to confirm. Click **Stay** to keep editing, or **Leave and discard** to leave. The browser's back and forward buttons don't ask.

## How your changes are saved

Each change to the entrypoints, an addition, a configuration, or a deletion, is saved as soon as you confirm it, and the console confirms with **API updated**. When the save fails, the **Entrypoint types** card shows **Save failed** with the reason, and the form keeps your input.

The context paths are saved with the **Save changes** button of their card.

Both reach the gateway at the next deployment, and until then the Message API shows **Out of sync**. See [Start, stop, and deploy a Message API](start-stop-and-deploy-a-message-api.md).

## Verification

To verify that the entrypoints are saved, follow these steps:

1. Reload the **Entrypoints** page.
2. Check that the **Entrypoint types** table lists the entrypoints you added, with their quality of service.
3. Check that the **Entrypoint context-paths** card shows the paths you entered, each ending with `/`.
4. Check that the header of the Message API sidebar shows **Out of sync**, and, if you can deploy the Message API, that the page header shows **Deploy**.
