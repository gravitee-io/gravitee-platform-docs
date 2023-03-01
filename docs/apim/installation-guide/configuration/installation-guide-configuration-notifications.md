# Overview

APIM includes three categories of notifications:

-   **Portal** — notifications about the platform

-   **API** — notifications about a specific API

-   **Application** — notifications about a specific application

There are also three types of notifiers:

-   **Portal** — this is the default notifier; messages are sent to
    users logged in to APIM Portal

-   **Email** — you can configure an email notifier to send messages to
    a specific list of email addresses

-   **Webhook** — you can configure a webhook notifier to send an HTTP
    POST request to a specific URL

APIM includes a standard set of notifiers. You can also create new
notifiers. For more details, see [???](#Notifiers).

# Subscribe to Portal notifications

To subscribe to Portal notifications:

1.  In APIM Console, click **Settings &gt; Notifications**.

    image:{% link
    images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-subscriptions-portal.png
    %}\[Subscribe to portal notifications\]

2.  Select the required notifications. For details, see [Portal
    notifications](#portal-notifications).

3.  Click **SAVE**.

# Subscribe to API notifications

To subscribe to notifications about a specific API:

1.  In APIM Console, click **APIs**.

2.  Select the API and click **Notifications**.

    image:{% link
    images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-subscriptions-api.png
    %}\[Subscribe to API notifications\]

3.  Select the required notifications. For details, see [API
    notifications](#api-notifications).

4.  Click **SAVE**.

# Subscribe to application notifications

To subscribe to notifications about a specific application:

1.  In APIM Console, click **Applications**.

2.  Select the application and click **Notifications**.

    image:{% link
    images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-subscriptions-application.png
    %}\[Subscribe to application notifications\]

3.  Select the required notifications. For details, see [Application
    notifications](#application-notifications).

4.  Click **SAVE**.

# Categories of notifications

## Portal notifications

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>What triggers it?</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>First Login</p></td>
<td style="text-align: left;"><p>User logs in for the first
time</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Group invitation</p></td>
<td style="text-align: left;"><p>User is invited in a group</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Message</p></td>
<td style="text-align: left;"><p>Custom message needs to be sent to an
Environment Role (the message is sent in the notification)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>New Support Ticket</p></td>
<td style="text-align: left;"><p>New support ticket is created</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Password Reset</p></td>
<td style="text-align: left;"><p>Password is reset</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>User Created</p></td>
<td style="text-align: left;"><p>New user is created</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>User Registered</p></td>
<td style="text-align: left;"><p>User is registered</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>User Registration Request</p></td>
<td style="text-align: left;"><p>New user is created and automatic
validation is disabled</p></td>
</tr>
</tbody>
</table>

## API notifications

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>What triggers it?</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Accept API review</p></td>
<td style="text-align: left;"><p>API review is accepted</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>API Deprecated</p></td>
<td style="text-align: left;"><p>API is deprecated</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API key Expired</p></td>
<td style="text-align: left;"><p>API key is expired</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>API key Renewed</p></td>
<td style="text-align: left;"><p>API key is renewed</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API key Revoked</p></td>
<td style="text-align: left;"><p>API key is revoked</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>API Started</p></td>
<td style="text-align: left;"><p>API is started</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API Stopped</p></td>
<td style="text-align: left;"><p>API is stopped</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Ask for API review</p></td>
<td style="text-align: left;"><p>API is ready for review</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Message</p></td>
<td style="text-align: left;"><p>Custom message needs to be sent to an
Application Role (the message is sent in the notification)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>New Rating</p></td>
<td style="text-align: left;"><p>New rating is submitted</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>New Rating Answer</p></td>
<td style="text-align: left;"><p>New answer is submitted</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>New Subscription</p></td>
<td style="text-align: left;"><p>Subscription is created</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>New Support Ticket</p></td>
<td style="text-align: left;"><p>New support ticket is created</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Reject API review</p></td>
<td style="text-align: left;"><p>API review is rejected</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Accepted</p></td>
<td style="text-align: left;"><p>Subscription is accepted</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Closed</p></td>
<td style="text-align: left;"><p>Subscription is closed</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Paused</p></td>
<td style="text-align: left;"><p>Subscription is paused</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Rejected</p></td>
<td style="text-align: left;"><p>Subscription is rejected</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Resumed</p></td>
<td style="text-align: left;"><p>Subscription is resumed</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Transferred</p></td>
<td style="text-align: left;"><p>Subscription is transferred</p></td>
</tr>
</tbody>
</table>

## Application notifications

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>What triggers it?</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>New Subscription</p></td>
<td style="text-align: left;"><p>Subscription is created</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>New Support Ticket</p></td>
<td style="text-align: left;"><p>New support ticket is created</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Accepted</p></td>
<td style="text-align: left;"><p>Subscription is accepted</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Closed</p></td>
<td style="text-align: left;"><p>Subscription is closed</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Paused</p></td>
<td style="text-align: left;"><p>Subscription is paused</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Rejected</p></td>
<td style="text-align: left;"><p>Subscription is rejected</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Subscription Resumed</p></td>
<td style="text-align: left;"><p>Subscription is resumed</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Subscription Transferred</p></td>
<td style="text-align: left;"><p>Subscription is transferred</p></td>
</tr>
</tbody>
</table>

# Notifiers

## Portal

The Portal notifier sends messages to logged in users. Notifications can
be displayed by clicking the bell icon in the top menu of APIM Console.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-portal-notifier-console.png
%}\[Notifications in the APIM Administration console, 300\]

In APIM Portal, notifications are displayed in a specific page,
accessible from the user menu.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-portal-notifier-portal.png
%}\[Notifications in the developer portal\]

The templates of portal notifications can be customized in **Settings**.
For more information, see [???](#Templates).

## Email

Email notifiers send an email to a specific list of email addresses. To
create a new email notifier:

1.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] .

2.  Choose the **Default Email Notifier** type and give your notifier a
    name.

3.  Add one or more email addresses.

4.  Subscribe to the notifications you want.

When you create an API, a default email notifier is created. All
notifications are selected and email are send to the primary owner.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-email-notifier-api.png
%}\[Default configuration of an email notifier\]

The templates of email notifications can be customized in **Settings**.
See [???](#Templates)

## Webhook

Webhook notifiers send an HTTP POST request to a configured URL. The
request contains two headers and a JSON body that represents the
message. Headers are:

-   `X-Gravitee-Event` — contains the event id (e.g. `API_KEY_REVOKED`)

-   `X-Gravitee-Event-Scope` — contains the category of the notification
    (e.g. `API`)

The JSON body looks like this (depending on the category of the
notification, some fields may not be present in the body): \`\`\`json {
"event": "", "scope": "", "api": { "id": "", "name": "", "version": ""
}, "application": { "id": "", "name": "" }, "owner": { "id": "",
"username": "", "owner": "" }, "plan": { "id": "", "name": "",
"security": "", "plan": "" }, "subscription": { "id": "", "status": "",
"subscription": "" } } \`\`\`

To create a new webhook notifier:

1.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] .

2.  Choose the **Default Webhook Notifier** type and give your notifier
    a name.

3.  Add the URL which APIM will call to send notifications.

4.  Subscribe to the notifications you want.

# Templates

Email and portal notification templates are based on HTML and YML files.
They are located here:

    templates:
      path: ${gravitee.home}/templates

Starting from APIM version 3.4.0, you can override these templates in
APIM Console.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-1.png
%}\[Templates edition in the settings\]

You can also customize:

-   Email templates that are sent for specific actions and not related
    to a notification. Most of the time, these emails are for specific
    users.

-   The `header.html` file that is included by default in all email
    templates.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-2.png
%}\[Specific templates\]

## Customize a template

For almost all notifications, you can configure both Portal and email
notifications.

To customize a template, toggle the switch **Override default template**
and update the title and/or the content.

image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-edition-1.png
%}\[Portal template edition\] image::{% link
images/apim/3.x/installation/notification/graviteeio-installation-configuration-notifications-templates-edition-2.png
%}\[Email template edition\]

## Attributes

You can use [Freemarker template engine](http://freemarker.org) to add
specific information to your templates (e.g. ${user.name} or
${api.metadata\[*foo-bar*\]}.

Available attributes  

<table style="width:100%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Api</th>
<th style="text-align: left;">Application</th>
<th style="text-align: left;">Group</th>
<th style="text-align: left;">Plan</th>
<th style="text-align: left;">Owner/User</th>
<th style="text-align: left;">Subscription</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>name</p></td>
<td style="text-align: left;"><p>name</p></td>
<td style="text-align: left;"><p>name</p></td>
<td style="text-align: left;"><p>name</p></td>
<td style="text-align: left;"><p>username</p></td>
<td style="text-align: left;"><p>status</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>description</p></td>
<td style="text-align: left;"><p>description</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>description</p></td>
<td style="text-align: left;"><p>firstname</p></td>
<td style="text-align: left;"><p>request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>version</p></td>
<td style="text-align: left;"><p>type</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>order</p></td>
<td style="text-align: left;"><p>lastname</p></td>
<td style="text-align: left;"><p>reason</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>role</p></td>
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>publishedAt (Date)</p></td>
<td style="text-align: left;"><p>displayName</p></td>
<td style="text-align: left;"><p>processedAt</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metadata (Map)</p></td>
<td style="text-align: left;"><p>role</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>closedAt (Date)</p></td>
<td style="text-align: left;"><p>email</p></td>
<td style="text-align: left;"><p>startingAt</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>deployedAt (Date)</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>endingAt</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>createdAt (Date)</p></td>
<td style="text-align: left;"><p>createdAt (Date)</p></td>
<td style="text-align: left;"><p>createdAt (Date)</p></td>
<td style="text-align: left;"><p>createdAt (Date)</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>closedAt</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>updatedAt (Date)</p></td>
<td style="text-align: left;"><p>updatedAt (Date)</p></td>
<td style="text-align: left;"><p>updatedAt (Date)</p></td>
<td style="text-align: left;"><p>updatedAt (Date)</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>subscribedAt</p></td>
</tr>
</tbody>
</table>

An example template is as follows:

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
