---
description: An overview about notifications.
---

# Notifications

## Overview

Gravitee allows you to set up alerts and notifications based on events recognized by the Gateway. You can [set up notifications](notifications.md#configure-notifications-for-your-apis) that appear in the Gravitee API Management Console or that are sent to Gravitee users via email. You can also [create custom alerts](notifications.md#configure-alerts) based on user-defined rules and conditions.

## Configure notifications for your APIs

APIM includes 3 categories of notifications and 3 types of notifiers. Their purpose and configuration are described below, along with customization via templates.

### Notifications

{% tabs %}
{% tab title="Portal" %}
Portal notifications relate to the platform and include the following:

<table><thead><tr><th width="265">Name</th><th>What triggers it?</th></tr></thead><tbody><tr><td>First Login</td><td>User logs in for the first time</td></tr><tr><td>Group invitation</td><td>User is invited in a group</td></tr><tr><td>Message</td><td>Custom message is sent to an Environment Role via notification</td></tr><tr><td>New Support Ticket</td><td>New support ticket is created</td></tr><tr><td>Password Reset</td><td>Password is reset</td></tr><tr><td>User Created</td><td>New user is created</td></tr><tr><td>User Registered</td><td>User is registered</td></tr><tr><td>User Registration Request</td><td>New user is created and automatic validation is disabled</td></tr></tbody></table>

To subscribe to Portal notifications, go to **APIM Console > Settings > Notifications**:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="API" %}
API notifications relate to a specific API and include the following:

<table><thead><tr><th width="268.5">Name</th><th>What triggers it?</th></tr></thead><tbody><tr><td>Accept API review</td><td>API review is accepted</td></tr><tr><td>API Deprecated</td><td>API is deprecated</td></tr><tr><td>API key Expired</td><td>API key is expired</td></tr><tr><td>API key Renewed</td><td>API key is renewed</td></tr><tr><td>API key Revoked</td><td>API key is revoked</td></tr><tr><td>API Started</td><td>API is started</td></tr><tr><td>API Stopped</td><td>API is stopped</td></tr><tr><td>Ask for API review</td><td>API is ready for review</td></tr><tr><td>Message</td><td>Custom message is sent to an Application Role via notification</td></tr><tr><td>New Rating</td><td>New rating is submitted</td></tr><tr><td>New Rating Answer</td><td>New answer is submitted</td></tr><tr><td>New Subscription</td><td>Subscription is created</td></tr><tr><td>New Support Ticket</td><td>New support ticket is created</td></tr><tr><td>Reject API review</td><td>API review is rejected</td></tr><tr><td>Subscription Accepted</td><td>Subscription is accepted</td></tr><tr><td>Subscription Closed</td><td>Subscription is closed</td></tr><tr><td>Subscription Paused</td><td>Subscription is paused</td></tr><tr><td>Subscription Rejected</td><td>Subscription is rejected</td></tr><tr><td>Subscription Resumed</td><td>Subscription is resumed</td></tr><tr><td>Subscription Transferred</td><td>Subscription is transferred</td></tr></tbody></table>

To subscribe to notifications related to a specific API:

1. Log in to your **APIM Console**
2. Select **APIs**, from the left nav
3. Select your API
4. Select **Configuration** from the inner left nav
5. Select the **Notifications** header

<figure><img src="../../4.6/.gitbook/assets/A%201%20config%20notifications%20(1).png" alt=""><figcaption></figcaption></figure>

From here, you can either edit an existing notification or click **+ Add notification** to create a new one.
{% endtab %}

{% tab title="Application" %}
Application notifications relate to a specific application and include the following:

| Name                     | What triggers it?             |
| ------------------------ | ----------------------------- |
| New Subscription         | Subscription is created       |
| New Support Ticket       | New support ticket is created |
| Subscription Accepted    | Subscription is accepted      |
| Subscription Closed      | Subscription is closed        |
| Subscription Paused      | Subscription is paused        |
| Subscription Rejected    | Subscription is rejected      |
| Subscription Resumed     | Subscription is resumed       |
| Subscription Transferred | Subscription is transferred   |

To subscribe to notifications related to a specific application, go to **APIM Console >** **Applications**, select the application, and click **Notifications**:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

### Notifiers

{% tabs %}
{% tab title="Portal" %}
The Portal notifier is the default notifier and sends messages to users logged in to the Developer Portal. Notifications appear in the Portal or Management Console.

They can be displayed by clicking the bell icon in the header menu of APIM Console:

<div align="left"><figure><img src="broken-reference" alt="" width="375"><figcaption></figcaption></figure></div>

In the Developer Portal, notifications are displayed in a page accessible from the user menu:

<div align="left"><figure><img src="broken-reference" alt="" width="188"><figcaption></figcaption></figure></div>

The templates of Portal notifications can be customized in **Settings**. For more information, see [Templates](notifications.md#templates).
{% endtab %}

{% tab title="Email" %}
Email notifiers send an email to a specific list of email addresses. To create a new email notifier:

1. Define the email notifier (who the email notification will come from).
2. Define the email list (who the email notification will be sent to). Multiple emails can be added as long as they are separated by a `,` or a `;`.
3. Subscribe to the desired notifications.

{% hint style="info" %}
A default email notifier is created for every API. All notifications are preselected and email is sent to the primary owner.
{% endhint %}

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

The [templates](notifications.md#templates) of email notifications can be customized in **Settings.**
{% endtab %}

{% tab title="Webhook" %}
Webhook notifiers send an HTTP POST request to a configured URL. The request contains two headers and a JSON body representing the message. The headers are:

* `X-Gravitee-Event` : Contains the event ID (e.g., `API_KEY_REVOKED`)
* `X-Gravitee-Event-Scope` : Contains the type of notification (e.g., `API`)

The JSON body is similar to the following (depending on the notification type, some fields may not be present in the body):

```json
{
  "event": "",
  "scope": "",
  "api": {
    "id": "",
    "name": "",
    "version": ""
  },
  "application": {
    "id": "",
    "name": ""
  },
  "owner": {
    "id": "",
    "username": "",
    "owner": ""
  },
  "plan": {
    "id": "",
    "name": "",
    "security": "",
    "plan": ""
  },
  "subscription": {
    "id": "",
    "status": "",
    "subscription": ""
  }
}
```

To create a Webhook notifier:

1. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
2. Choose the **Default Webhook Notifier** type and give the notifier a name.
3. Add the URL which APIM will call to send notifications.
4. Subscribe to the desired notifications.
{% endtab %}
{% endtabs %}

### Templates

Email and Portal notification templates are based on HTML and YML files, located here:

```sh
templates:
  path: ${gravitee.home}/templates
```

These templates can be overridden in **APIM Console > Organization > Notifications > Templates**:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

Email templates that are sent for specific actions and not related to a notification can be customized. Typically, these emails are intended for specific users.

The `header.html` file that is included by default in all email templates can also be customized.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

#### Customize a template

Portal and email notifiers can be configured for most notifications. To customize a template, toggle the switch **Override default template** and update the title and/or content.

<div><figure><img src="broken-reference" alt=""><figcaption></figcaption></figure> <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure></div>

The available attributes are summarized below. Use the [Apache Freemarker template engine](https://freemarker.apache.org/) to add specific information to templates, e.g., ${user.name} or ${api.metadata\['foo-bar']}.

| API               | Application      | Group            | Plan               | Owner/User  | Subscription |
| ----------------- | ---------------- | ---------------- | ------------------ | ----------- | ------------ |
| name              | name             | name             | name               | username    | status       |
| description       | description      | -                | description        | firstname   | request      |
| version           | type             | -                | order              | lastname    | reason       |
| role              | status           | -                | publishedAt (Date) | displayName | processedAt  |
| metadata (Map)    | role             | -                | closedAt (Date)    | email       | startingAt   |
| deployedAt (Date) | -                | -                | -                  | -           | endingAt     |
| createdAt (Date)  | createdAt (Date) | createdAt (Date) | createdAt (Date)   | -           | closedAt     |
| updatedAt (Date)  | updatedAt (Date) | updatedAt (Date) | updatedAt (Date)   | -           | subscribedAt |

{% code title="Example template" %}
```ftl
<html>
	<body style="text-align: center;">
		<header>
			<#include "header.html" />
		</header>
		<div style="margin-top: 50px; color: #424e5a;">
			<h3>Hi ${owner.username},</h3>
			<p>The API Key <code>${apiKey}</code> has been expired.
		</p>
	</body>
</html>
```
{% endcode %}
