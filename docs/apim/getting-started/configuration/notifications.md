# Configure Notifications

## Introduction

APIM includes 3 categories of notifications and 3 types of notifiers. The following sections describe what these are and how they can be configured.

<table><thead><tr><th width="182.5">Notification</th><th>Description</th></tr></thead><tbody><tr><td>API</td><td>Notifications relate to the platform</td></tr><tr><td>Application</td><td>Notifications relate to a specific API</td></tr><tr><td>Portal</td><td>Notifications relate to a specific application</td></tr></tbody></table>

&#x20;and 3 types of notifiers:

<table><thead><tr><th width="183.5">Notification</th><th>Description</th></tr></thead><tbody><tr><td>Email</td><td>Configure an email notifier to send messages to a list of specific email addresses</td></tr><tr><td>Portal</td><td>The default notifier that sends messages to users logged in to APIM Portal</td></tr><tr><td>Webhook</td><td>Configure a webhook notifier to send an HTTP POST request to a specific URL</td></tr></tbody></table>

## Subscribe to Portal notifications

Portal notifications relate to a specific application. To subscribe to Portal notifications, go to **APIM Console > Settings > Notifications**, select the desired notifications, and click SAVE.

<figure><img src="../../.gitbook/assets/portal_notifications.png" alt=""><figcaption></figcaption></figure>

### Subscribe to API notifications

To subscribe to notifications about a specific API:

1. In APIM Console, click **APIs**.
2.  Select the API and click **Notifications**.

    ![Subscribe to API notifications](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-subscriptions-api.png)
3. Select the required notifications. For details, see [API notifications](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#api-notifications).
4. Click **SAVE**.

### Subscribe to application notifications

To subscribe to notifications about a specific application:

1. In APIM Console, click **Applications**.
2.  Select the application and click **Notifications**.

    ![Subscribe to application notifications](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-subscriptions-application.png)
3. Select the required notifications. For details, see [Application notifications](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#application-notifications).
4. Click **SAVE**.

### Categories of notifications

#### Portal notifications

| Name                      | What triggers it?                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| First Login               | User logs in for the first time                                                                  |
| Group invitation          | User is invited in a group                                                                       |
| Message                   | Custom message needs to be sent to an Environment Role (the message is sent in the notification) |
| New Support Ticket        | New support ticket is created                                                                    |
| Password Reset            | Password is reset                                                                                |
| User Created              | New user is created                                                                              |
| User Registered           | User is registered                                                                               |
| User Registration Request | New user is created and automatic validation is disabled                                         |

#### API notifications

| Name                     | What triggers it?                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| Accept API review        | API review is accepted                                                                           |
| API Deprecated           | API is deprecated                                                                                |
| API key Expired          | API key is expired                                                                               |
| API key Renewed          | API key is renewed                                                                               |
| API key Revoked          | API key is revoked                                                                               |
| API Started              | API is started                                                                                   |
| API Stopped              | API is stopped                                                                                   |
| Ask for API review       | API is ready for review                                                                          |
| Message                  | Custom message needs to be sent to an Application Role (the message is sent in the notification) |
| New Rating               | New rating is submitted                                                                          |
| New Rating Answer        | New answer is submitted                                                                          |
| New Subscription         | Subscription is created                                                                          |
| New Support Ticket       | New support ticket is created                                                                    |
| Reject API review        | API review is rejected                                                                           |
| Subscription Accepted    | Subscription is accepted                                                                         |
| Subscription Closed      | Subscription is closed                                                                           |
| Subscription Paused      | Subscription is paused                                                                           |
| Subscription Rejected    | Subscription is rejected                                                                         |
| Subscription Resumed     | Subscription is resumed                                                                          |
| Subscription Transferred | Subscription is transferred                                                                      |

#### Application notifications

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

### Notifiers

APIM includes a standard set of notifiers. You can also create new notifiers. For more details, see [Notifiers](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#notifiers).

#### Portal

The Portal notifier sends messages to logged in users. Notifications can be displayed by clicking the bell icon in the top menu of APIM Console.

![Notifications in the APIM Administration console](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-portal-notifier-console.png)

In APIM Portal, notifications are displayed in a specific page, accessible from the user menu.

![Notifications in the developer portal](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-portal-notifier-portal.png)

The templates of portal notifications can be customized in **Settings**. For more information, see [Templates](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#templates).

#### Email

Email notifiers send an email to a specific list of email addresses. To create a new email notifier:

1. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) .
2. Choose the **Default Email Notifier** type and give your notifier a name.
3. Add one or more email addresses.
4. Subscribe to the notifications you want.

|   | <p>When you create an API, a default email notifier is created. All notifications are selected and email are send to the primary owner.</p><p><img src="https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-email-notifier-api.png" alt="Default configuration of an email notifier"></p> |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

The templates of email notifications can be customized in **Settings**. See [Templates](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_notifications.html#templates)

#### Webhook

Webhook notifiers send an HTTP POST request to a configured URL. The request contains two headers and a JSON body that represents the message. Headers are:

* `X-Gravitee-Event` — contains the event id (e.g. `API_KEY_REVOKED`)
* `X-Gravitee-Event-Scope` — contains the category of the notification (e.g. `API`)

The JSON body looks like this (depending on the category of the notification, some fields may not be present in the body):

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

To create a new webhook notifier:

1. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) .
2. Choose the **Default Webhook Notifier** type and give your notifier a name.
3. Add the URL which APIM will call to send notifications.
4. Subscribe to the notifications you want.

### Templates

Email and portal notification templates are based on HTML and YML files. They are located here:

```
templates:
  path: ${gravitee.home}/templates
```

Starting from APIM version 3.4.0, you can override these templates in APIM Console.

![Templates edition in the settings](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-1.png)

You can also customize:

* Email templates that are sent for specific actions and not related to a notification. Most of the time, these emails are for specific users.
* The `header.html` file that is included by default in all email templates.

![Specific templates](https://docs.gravitee.io/images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-2.png)

#### Customize a template

For almost all notifications, you can configure both Portal and email notifications.

To customize a template, toggle the switch **Override default template** and update the title and/or the content.

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

\
