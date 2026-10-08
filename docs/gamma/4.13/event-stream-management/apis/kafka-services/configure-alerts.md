---
hidden: false
noIndex: false
description: Set up runtime alerts on the connections, topic traffic, operations, policy rejections, and authentications of a Kafka Service in Event Stream Management, with Alert Engine rules, dampening, and notifications. Follow the steps to create an alert.
---

# Configure alerts

A runtime alert watches the events that the Event Gateway sends about a Kafka Service, and notifies you when a condition is met. For example, an alert can fire when clients fail to connect, when a topic stops receiving messages, or when a policy starts rejecting requests. Alerts are evaluated by Alert Engine.

A Kafka Service has its own alert catalogue. The rules watch Kafka events, not HTTP requests, so the catalogue differs from the one of a Message API.

## Prerequisites

* A license that includes Alert Engine. Without it, the **Alerts** page shows that the feature is locked.
* Alert Engine installed and connected. When it isn't, the **Alerts** page warns that **The Alert Engine is not enabled on this installation**, and alerts can be configured but aren't evaluated.
* Permission to read the alerts of the Kafka Service. Without it, the **Alerts** item doesn't appear in the sidebar.
* For every category except **Connection**, analytics turned on for the Kafka Service. See [Alerts and analytics](#alerts-and-analytics).

## Open the alerts

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **Monitoring** group of the Kafka Service sidebar, click **Alerts**.

The **Runtime Alerts** card lists each alert with its **Name**, **Rule**, **Severity**, **Last alert**, and whether it's **Enabled**. It also shows how many times each alert fired in the last five minutes, hour, day, and month. While the Kafka Service has no alert, the card lists the available rules. Once alerts exist, the info button next to **Runtime Alerts** shows that list again.

## Alerts and analytics

The Event Gateway builds most Kafka alert events from the metrics it collects for the Kafka Service. It collects them only when analytics are on, which is the **Aggregated metrics** checkbox of the Kafka Service's reporter settings. See [Configure reporter settings](../../observability/configure-reporter-settings.md).

<table>
    <thead>
        <tr>
            <th width="200">Category</th>
            <th>Needs analytics</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Connection</strong></td>
            <td>No. Connection events are sent whatever the reporter settings.</td>
        </tr>
        <tr>
            <td><strong>Topic traffic</strong></td>
            <td>Yes.</td>
        </tr>
        <tr>
            <td><strong>Operations</strong></td>
            <td>Yes.</td>
        </tr>
        <tr>
            <td><strong>Policy rejections</strong></td>
            <td>Yes.</td>
        </tr>
        <tr>
            <td><strong>Authentication</strong></td>
            <td>Yes.</td>
        </tr>
    </tbody>
</table>

When analytics are off, the **Alerts** page and the alert form show **Aggregated metrics are off, so most rules here will not work**. The warning names the topic traffic, operations, policy rejections, and authentication rules, and says that the connection rules are unaffected. The rules of the other categories can still be saved, but threshold, rate, and aggregation rules stay silent, and rules that alert when no event is received fire continuously. The warning links to **Reporter Settings**.

## Create an alert

1. Click **Add alert**.
2. On the **Alerts** tab, complete the general settings:
    * **Name**. Required. Between 3 and 50 characters.
    * **Enable alert**. Selected by default.
    * **Rule**. The kind of condition that the alert evaluates, grouped by category. See [Alert rules](#alert-rules).
    * **Severity**. `info`, `warning`, or `critical`.
    * **Description**. Optional. Up to 256 characters.
3. Optional: Under **Timeframes**, add a timeframe to limit the days and the hours when the alert notifies.
4. Under **Conditions**, set the condition of the rule on one of the metrics of its category.
5. Optional: Under **Filters**, click **Add filter** to evaluate the condition on part of the events only, for example one application, one plan, or one topic.
6. On the **Notifications** tab, choose the **Mode** of **Dampening**, which limits how many notifications a condition that stays true sends.
7. Under **Notifications**, add a notification, select a notifier, then complete its configuration.
8. Click **Create**.

The console confirms with **Alert created**. If you leave the form with unsaved changes, the console asks you to confirm.

## Alert rules

Each category offers the rules that its events can answer.

<table>
    <thead>
        <tr>
            <th width="160">Category</th>
            <th width="260">Rules</th>
            <th>Metrics</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Connection</strong></td>
            <td><strong>Alert when a connection metric validates a condition</strong>, <strong>Alert when the rate of a connection condition rises a threshold</strong></td>
            <td><strong>Connection Status</strong>, <strong>Failure Side</strong>, <strong>Error Key</strong>, <strong>Client ID</strong>, <strong>Broker ID</strong>, <strong>Remote Address</strong>, <strong>Subscription</strong>, <strong>Application</strong>, <strong>Plan</strong></td>
        </tr>
        <tr>
            <td><strong>Topic traffic</strong></td>
            <td>The four rules: metric condition, no event received, aggregated value, and rate</td>
            <td><strong>Messages Published</strong>, <strong>Bytes Published</strong>, <strong>Messages Consumed</strong>, <strong>Bytes Consumed</strong>, <strong>Topic</strong>, <strong>Application</strong>, <strong>Plan</strong></td>
        </tr>
        <tr>
            <td><strong>Operations</strong></td>
            <td>The four rules</td>
            <td><strong>Requests</strong>, <strong>Responses</strong>, <strong>Policy Rejections</strong>, <strong>Broker Duration (ms)</strong>, <strong>Kafka Operation</strong>, <strong>Application</strong>, <strong>Plan</strong></td>
        </tr>
        <tr>
            <td><strong>Policy rejections</strong></td>
            <td><strong>Alert when a policy rejection metric validates a condition</strong>, <strong>Alert when the aggregated value of a policy rejection metric rises a threshold</strong></td>
            <td><strong>Rejections by this policy</strong>, <strong>Policy</strong>, <strong>Kafka Operation</strong></td>
        </tr>
        <tr>
            <td><strong>Authentication</strong></td>
            <td>The four rules</td>
            <td><strong>Authentication Successes</strong>, <strong>Application</strong>, <strong>Plan</strong></td>
        </tr>
    </tbody>
</table>

The rule labels name their category. For example, the **Topic traffic** rules are **Alert when a topic traffic metric validates a condition**, **Alert when no topic traffic event is received for a period of time**, **Alert when the aggregated value of a topic traffic metric rises a threshold**, and **Alert when the rate of a topic traffic condition rises a threshold**.

Consider the following when you choose a rule:

* **Connection** events are sent when a client connection is established and when a connection fails. No event is sent while a connection stays open, so the **Connection** category offers no rule that alerts when no event is received. A connection refused before authentication carries no application and no plan, so a condition filtered on an application ignores those failures.
* Authentication failures are watched with the **Connection** rules, which name the client, the failure side, and the error. The **Authentication** category counts successes only.
* **Policy rejections** events tell which policy rejected requests. They carry no application and no plan. To compare rejections with requests, use the **Policy Rejections** and **Requests** metrics of the **Operations** category.
* An aggregation rule aggregates a numeric metric of its category, with **count**, **average**, **min**, **max**, or a percentile. **Group by** evaluates the condition per value of a text metric of the same category, for example per **Topic**.

The rule of an existing alert can't change.

## Manage the alerts

* To turn an alert on or off, use the switch in its **Enabled** column. The console confirms with **Alert updated**.
* To change an alert, click its row, or select **Edit** in its actions menu. Your changes show **Unsaved changes** at the bottom of the page. Click **Save changes**, or **Discard** to restore the saved alert.
* To see when an alert fired, open it and select the **History** tab. It lists the **Date** and the **Message** of each notification.
* To remove an alert, select **Delete** in its actions menu, then click **Delete** in the **Delete alert `<name>`?** dialog. The console confirms with **Alert deleted**.

## Verification

To verify an alert, follow these steps:

1. Open **Alerts** for the Kafka Service.
2. Check that the alert is listed with the rule and the severity you chose, and that its **Enabled** switch is on.
3. Unless the alert uses a **Connection** rule, check that the page doesn't show **Aggregated metrics are off, so most rules here will not work**.
