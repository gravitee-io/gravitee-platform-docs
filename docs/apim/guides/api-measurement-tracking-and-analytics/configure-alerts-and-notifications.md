---
description: >-
  This article walks through how to configure alerts and notifications for your
  APIs.
---

# Configure Alerts and Notifications

### Introduction

Gravitee allows you to set up alerts and notifications based on events noticed by the Gateway.&#x20;

You can set up notifications that appear in the Gravitee API Management UI and notifications that are sent to Gravitee users via email.&#x20;

For alerts, you can create custom alerts based on custom rules and conditions. Keep reading to learn how to configure these alerts and notifications.

### Configure notifications for your APIs

{% @arcade/embed flowId="vLOPiPtuGAbHWNJj6LRN" url="https://app.arcade.software/share/vLOPiPtuGAbHWNJj6LRN" %}

Notifications are configured as a part of an API's settings. To configure these settings, you'll need to select your API from the APIs page. Then, when in the APIs settings select **Notifications.**&#x20;

On the **Notifications** page, you are able to configure notifications that appear in the portal (or Management UI) and notifications that will be sent out via email. To configure Portal notifications, select **Portal Notifications** and then choose the events that you want to trigger notifications by checking the checkbox next to your desired events.

To configure email notifications, select **Default Mail Notifications** and then:

* Define your email notifier (who the email notification will come from)
* Email list (who the email notification will be sent to)
  * You can add multiple emails here as long as they are seperated by a `,` or a `;`

<figure><img src="../../.gitbook/assets/Configure notifications.gif" alt=""><figcaption></figcaption></figure>

### Configure alerts

{% @arcade/embed flowId="5HCcKbjuS7rfjlFsxPTI" url="https://app.arcade.software/share/5HCcKbjuS7rfjlFsxPTI" %}

In addition to notifications, you can set up alerting conditions for the Gateway. Like notifications, this done as a part of configuring an APIs settings.

{% hint style="info" %}
**Alert Engine**

While the Gateway and MAnagement UI offer some pre-built alerting capabilities, we recommend that organizations with a need for robust, eneterprise API monitoring nad alerting check out the [Gravitee Alert Engine documentation](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/WAKqxjzYogMr1tk18evT/).&#x20;
{% endhint %}

To configure alerts for your APIs, select your API from the **APIs** menu. Then, under **Notifications,** select **Alerts**.&#x20;

If you already have alerts configured, you'll see the configured Alerts. If not, you'll see a blank alerts menu and a **+** icon.

<figure><img src="../../.gitbook/assets/Alerts menu.png" alt=""><figcaption><p>Blank alerts page</p></figcaption></figure>

Select the **+** icon to start creating your first alert. On the **Create a new alert** page, you are able to configure the following:

* General settings
  * Name
  * Rule: Gravitee comes pre-built with several rules
  * Severity
  * Description
* Timeframe: this is where you create a timeline for this alerting mechanism to run
* Condition: set conditions for when your rule should operate and trigger alerts
* Filters: define a subset of events for which your conditions and rules should be applied

Alerts will, by default, show up in your Dashboard under the Alerts tab and on the Alerts page.&#x20;

<figure><img src="../../.gitbook/assets/Alert areas.gif" alt=""><figcaption><p>You can see alerts in the Alerts tab and the Alerts page.</p></figcaption></figure>

In addition to viewing alerts in these locations, you can also configure notifications that are attached to these alerts. This is done on the **Create a new alert** page under the **Notifications tab.** On this page, you can:

* Define a dampening rule: limit the number of notifications if the trigger is fired multiple times for the same condition
* Add a notification: this allows you to add a notification type to your alerts so that you can trigger notifications when alerts are processed. You'll be able to select from the following notification channels:
  * Email
  * Slack
  * System email
  * Webhook

Depending on the notification channel that you choose, you will need to configure multiple settings. Please see the tabs below for more information.

{% tabs %}
{% tab title="Email" %}
For email notifications, you can define the following:

* SMTP Host
* SMTP Port:&#x20;
* SMTP Username:&#x20;
* SMTP Password:
* Allowed authentication methods
* The "sender" email addresses
* Recipients
* The subject of the email
* The email body content
* Whether or not to enable TLS
* Whether or not to enable SSL trust all
* SSL key store
* SSL key store password

<figure><img src="../../.gitbook/assets/Email alert notifications.png" alt=""><figcaption><p>Email notifications for email alerting</p></figcaption></figure>
{% endtab %}

{% tab title="Slack" %}
If you choose Slack as your notification channel,  you can define the following:

* The Slack channel where you want the alert sent
* The Slack token of the app or the Slackbot
* Whether or not to use the system proxy
* The content of the Slack message

<figure><img src="../../.gitbook/assets/Slack notifications.png" alt=""><figcaption><p>Slack notifications for API alerting</p></figcaption></figure>
{% endtab %}

{% tab title="System email" %}
If you choose System email, you will need to define:

* The "From" email address
* The recipients of the email
* The subject of the email
* The body content of the email

<figure><img src="../../.gitbook/assets/System email notifications.png" alt=""><figcaption><p>System email notifications</p></figcaption></figure>
{% endtab %}

{% tab title="Webhook" %}
If you want to choose Webhook as your notification channel, you will need to define the following:

* **HTTP Method**: this defines the HTTP method used to invoke the Webhook
* **URL**: this defines the url to invoke the webhook
* **Request headers**: add request headers
* **Request body**: the content in the request body
* Whether or not to use the **system proxy** to call the webhook

<figure><img src="../../.gitbook/assets/Webhook notifications.png" alt=""><figcaption><p>Webhook notifications</p></figcaption></figure>
{% endtab %}
{% endtabs %}
