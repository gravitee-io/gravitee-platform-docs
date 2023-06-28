# Configure Notifications

## Introduction

APIM includes 3 categories of notifications and 3 types of notifiers. The following sections describe what these are and how they can be configured.

## Notifications

### Portal notifications

Portal notifications relate to the platform and include the following:

| Name                      | What triggers it?                                              |
| ------------------------- | -------------------------------------------------------------- |
| First Login               | User logs in for the first time                                |
| Group invitation          | User is invited in a group                                     |
| Message                   | Custom message is sent to an Environment Role via notification |
| New Support Ticket        | New support ticket is created                                  |
| Password Reset            | Password is reset                                              |
| User Created              | New user is created                                            |
| User Registered           | User is registered                                             |
| User Registration Request | New user is created and automatic validation is disabled       |

To subscribe to Portal notifications, go to **APIM Console > Settings > Notifications**:

<figure><img src="../../.gitbook/assets/portal_notifications.png" alt=""><figcaption></figcaption></figure>

### API notifications

API notifications relate to a specific API and include the following:

| Name                     | What triggers it?                                              |
| ------------------------ | -------------------------------------------------------------- |
| Accept API review        | API review is accepted                                         |
| API Deprecated           | API is deprecated                                              |
| API key Expired          | API key is expired                                             |
| API key Renewed          | API key is renewed                                             |
| API key Revoked          | API key is revoked                                             |
| API Started              | API is started                                                 |
| API Stopped              | API is stopped                                                 |
| Ask for API review       | API is ready for review                                        |
| Message                  | Custom message is sent to an Application Role via notification |
| New Rating               | New rating is submitted                                        |
| New Rating Answer        | New answer is submitted                                        |
| New Subscription         | Subscription is created                                        |
| New Support Ticket       | New support ticket is created                                  |
| Reject API review        | API review is rejected                                         |
| Subscription Accepted    | Subscription is accepted                                       |
| Subscription Closed      | Subscription is closed                                         |
| Subscription Paused      | Subscription is paused                                         |
| Subscription Rejected    | Subscription is rejected                                       |
| Subscription Resumed     | Subscription is resumed                                        |
| Subscription Transferred | Subscription is transferred                                    |

To subscribe to notifications related to a specific API, go to **APIM Console > APIs**, select the API, and click **Notifications**:

<figure><img src="../../.gitbook/assets/api_notifications.png" alt=""><figcaption></figcaption></figure>

### Application notifications

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

<figure><img src="../../.gitbook/assets/application_notifications.png" alt=""><figcaption></figcaption></figure>

## Notifiers

In addition to the following standard notifiers, new notifiers can be created.

### Portal notifiers

The Portal notifier is the default notifier and sends messages to users logged in to the Developer Portal. Notifications can be displayed by clicking the bell icon in the header menu of APIM Console:

<div align="left">

<figure><img src="../../.gitbook/assets/console_notification_link.png" alt="" width="375"><figcaption></figcaption></figure>

</div>

In the Developer Portal, notifications are displayed in a page accessible from the user menu:

<div align="left">

<figure><img src="../../.gitbook/assets/portal_notification_link.png" alt="" width="188"><figcaption></figcaption></figure>

</div>

The templates of Portal notifications can be customized in **Settings**. For more information, see [Templates](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#templates).

### Email notifiers

Email notifiers send an email to a specific list of email addresses. To create a new email notifier:

1. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) .
2. Choose the **Default Email Notifier** type and give the notifier a name.
3. Add one or more email addresses.
4. Subscribe to the desired notifications.

{% hint style="info" %}
A default email notifier is created for every API. All notifications are preselected and email is sent to the primary owner.
{% endhint %}

<figure><img src="../../.gitbook/assets/default_mail_notifier.png" alt=""><figcaption></figcaption></figure>

The [templates](notifications.md#templates) of email notifications can be customized in **Settings.**

### Webhook notifiers

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

## Templates

Email and Portal notification templates are based on HTML and YML files. They are located here:

```sh
templates:
  path: ${gravitee.home}/templates
```

These templates can be overridden in APIM Console:

![Templates edition in the settings](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-1.png)

Also customizable:

* Email templates that are sent for specific actions and not related to a notification. Typically, these emails are intended for specific users.
* The `header.html` file that is included by default in all email templates.

![Specific templates](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-2.png)

### Customize a template

Portal and email notifiers can be configured for most notifications. To customize a template, toggle the switch **Override default template** and update the title and/or content.

![Portal template edition](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-edition-1.png)![Email template edition](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-edition-2.png)

### Attributes

Available attributes are summarized below. Use the [Apache Freemarker template engine](https://freemarker.apache.org/) to add specific information to templates, e.g., ${user.name} or ${api.metadata\['foo-bar']}.

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

The following is a sample template:

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
