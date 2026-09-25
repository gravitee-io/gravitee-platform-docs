---
hidden: false
noIndex: false
description: Set up runtime alerts on the traffic of a Message API in Event Stream Management, with Alert Engine rules, dampening, and notifications. Follow the steps to create an alert.
---

# Configure alerts

A runtime alert watches the requests that a Message API handles and notifies you when a condition is met. For example, an alert can fire when response times rise or when requests stop coming in. Alerts are evaluated by Alert Engine.

## Prerequisites

* A license that includes the `alert-engine` feature. Without it, the **Alerts** item of the sidebar shows a lock icon.
* Alerting turned on for your organization, and Alert Engine installed on your installation. When alerting is turned off, the **Alerts** page warns that **The Alert Engine is not enabled on this installation**. Without both, alerts can't be created or changed.
* Permission to read the alerts of the Message API. Without it, the **Alerts** item doesn't appear in the sidebar.

## Open the alerts

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Monitoring** group of the Message API sidebar, click **Alerts**.

The **Runtime Alerts** card lists each alert with its **Name**, **Rule**, **Severity**, **Last alert**, and whether it's **Enabled**. It also shows how many times each alert fired in the last five minutes, hour, day, and month.

## Create an alert

1. Click **Add alert**.
2. On the **Alerts** tab, complete the general settings:
    * **Name**. Required. Between 3 and 50 characters.
    * **Enable alert**. On by default.
    * **Rule**. The kind of condition that the alert evaluates. See [Alert rules](#alert-rules).
    * **Severity**. `info`, `warning`, or `critical`.
    * **Description**. Optional. Up to 256 characters.
3. Optional: Under **Timeframes**, click **Add timeframe** to limit the days and the hours when the alert notifies.
4. Under **Conditions**, set the condition of the rule.
5. Optional: Under **Filters**, click **Add filter** to evaluate the condition on part of the traffic only, for example one application or one plan.
6. On the **Notifications** tab, choose the **Mode** of **Dampening**, which limits how many notifications a condition that stays true sends.
7. Under **Notifications**, click **Add notification**, select a notifier, then complete its configuration.
8. Click **Create**.

The console confirms with **Alert created**.

The notifiers are the notifier plugins installed on the environment, plus **System email**.

## Alert rules

<table>
    <thead>
        <tr>
            <th width="300">Rule</th>
            <th>Condition</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Alert when a metric of the request validates a condition</strong></td>
            <td>A metric of each request, compared with, for example, a threshold, a threshold range, or a text pattern.</td>
        </tr>
        <tr>
            <td><strong>Alert when there is no request matching filters received for a period of time</strong></td>
            <td>A duration without any matching request.</td>
        </tr>
        <tr>
            <td><strong>Alert when the aggregated value of a request metric rises a threshold</strong></td>
            <td>An aggregation of a metric over a duration, such as the average or the 95th percentile, compared with a threshold. The condition can also be evaluated per error key, tenant, application, or plan.</td>
        </tr>
        <tr>
            <td><strong>Alert when the rate of a given condition rises a threshold</strong></td>
            <td>The percentage of requests that meet a condition over a duration, compared with a rate threshold.</td>
        </tr>
    </tbody>
</table>

The metrics are **Response Time (ms)**, **Status Code**, **Request Content-Length**, **Response Content-Length**, **Error Key**, **Tenant**, **Application**, and **Plan**. The rule of an existing alert can't change.

## Manage the alerts

* To turn an alert on or off, use the switch in its **Enabled** column.
* To change an alert, click its row, or select **Edit** in its actions menu.
* To remove an alert, select **Delete** in its actions menu.

## Verification

To verify an alert, follow these steps:

1. Open **Alerts** for the Message API.
2. Check that the alert is listed with the rule and the severity you chose, and that its **Enabled** switch is on.
