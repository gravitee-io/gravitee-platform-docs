# Alerts

{% hint style="info" %}
The following documentation is only relevant if you have Gravitee Alert Engine enabled, which is an Enterprise-only capability. To enable the following alerting capabilities, please [contact us](https://www.gravitee.io/contact-us) or reach out to your CSM.
{% endhint %}

## Overview

When configuring platform settings, you can also set up alerting conditions for the Gateway.

## Configuration

To configure alerts, select **Alerts** from the left nav of your APIM console. If you already have alerts configured, you'll see the configured alerts. If not, you'll see a blank alerts menu and a **+** icon.

<figure><img src="../../../../../.gitbook/assets/alerts (1).png" alt=""><figcaption><p>Alerts</p></figcaption></figure>

Select the **+** icon to create your first alert. On the **Create a new alert** page, configure the following:

* **General settings:** Name, Rule (Gravitee includes several pre-built rules), Severity, Description
* **Timeframe:** Create a timeline for this alerting mechanism
* **Condition:** Set conditions for when your rule should operate and trigger alerts
* **Filters:** Define a subset of events to which your conditions and rules are applied

By default, alerts will show up in your **Dashboard** under the **Alerts** tab and on the **Alerts** page.

<figure><img src="../../../../../.gitbook/assets/Alert areas (1).gif" alt=""><figcaption><p>You can see alerts in the Alerts tab and the Alerts page.</p></figcaption></figure>

In addition to viewing alerts in these locations, you can configure notifications that are attached to these alerts. This is done on the **Create a new alert** page under the **Notifications** tab. On this page, you can:

* **Define a dampening rule:** Limit the number of notifications if the trigger is fired multiple times for the same condition
* **Add a notification:** Add a notification type to your alerts to trigger notifications when alerts are processed. The available notification channels are email, Slack, system email, and Webhook.

Depending on the notification channel you choose, you will need to configure multiple settings. Please see the tabs below for more information.

{% tabs %}
{% tab title="Email" %}
For email notifications, you can define the following:

* SMTP Host
* SMTP Port:
* SMTP Username:
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

<figure><img src="../../../../../.gitbook/assets/Email alert notifications (1).png" alt=""><figcaption><p>Email notifications for email alerting</p></figcaption></figure>
{% endtab %}

{% tab title="Slack" %}
If you choose Slack as your notification channel, you can define the following:

* The Slack channel where you want the alert sent
* The Slack token of the app or the Slackbot
* Whether or not to use the system proxy
* The content of the Slack message

<figure><img src="../../../../../.gitbook/assets/Slack notifications (1).png" alt=""><figcaption><p>Slack notifications for API alerting</p></figcaption></figure>
{% endtab %}

{% tab title="System email" %}
If you choose System email, you will need to define:

* The "From" email address
* The recipients of the email
* The subject of the email
* The body content of the email

<figure><img src="../../../../../.gitbook/assets/System email notifications (1).png" alt=""><figcaption><p>System email notifications</p></figcaption></figure>
{% endtab %}

{% tab title="Webhook" %}
If you want to choose Webhook as your notification channel, you will need to define the following:

* **HTTP Method**: this defines the HTTP method used to invoke the Webhook
* **URL**: this defines the url to invoke the webhook
* **Request headers**: add request headers
* **Request body**: the content in the request body
* Whether or not to use the **system proxy** to call the webhook

<figure><img src="../../../../../.gitbook/assets/Webhook notifications (1).png" alt=""><figcaption><p>Webhook notifications</p></figcaption></figure>
{% endtab %}
{% endtabs %}

## Example alerts

To assist with alert configuration, sample alert templates useful to many teams are shown below.

### Alerts for when limits are reached

{% tabs %}
{% tab title="Response time limit" %}
To configure an alert for response times exceeding a threshold of 1500ms:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_response_time_threshold.png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="50th percentile reached" %}
To configure an alert for the 50th percentile of response times exceeding 200 ms in the last 5 minutes:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_50percentile.png" alt=""><figcaption><p>Alert for 50th percentile of response time greater than X ms</p></figcaption></figure>
{% endtab %}

{% tab title="Quota reached" %}
To configure an alert for reaching the quota limit on requests:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_quota_too_many_requests.png" alt=""><figcaption><p>Alert for reaching the quota limit on requests</p></figcaption></figure>
{% endtab %}
{% endtabs %}

### Alerts based on errors or low usage

{% tabs %}
{% tab title="Invalid API key" %}
To trigger an alert when an invalid API key is passed to the Gateway:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_api_key_invalid.png" alt=""><figcaption><p>Invalid API key alert</p></figcaption></figure>
{% endtab %}

{% tab title="Errors per interval" %}
To configure an alert for the number of 5xx errors reaching a threshold of 10 in the last 5 minutes:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_api_too_many_errors.png" alt=""><figcaption><p>Alert for too many errors in the last five minutes</p></figcaption></figure>
{% endtab %}

{% tab title="No requests in X min" %}
To configure an alert for no requests made to the API during the last minute:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_api_no_request_last_minute.png" alt=""><figcaption><p>Alert for no API requests in the last minute</p></figcaption></figure>
{% endtab %}

{% tab title="Filtered no requests in X min" %}
The following example is the same as above, but filters on `my-application`:

<figure><img src="https://docs.gravitee.io/images/ae/apim/api_alert_application_no_request_last_minute.png" alt=""><figcaption><p>Alert for no API requests from my application in the last minute</p></figcaption></figure>
{% endtab %}
{% endtabs %}
