# Overview

You can use the APIM Console messaging feature to communicate with your
users. You can send notifications at the level of the entire APIM
platform or a specific API.

There are three types of platform-wide and API notifications:

-   Portal notifications

-   Email notifications

-   POST HTTP message notifications

You define the audience for your notifications in terms of roles, as
described in the section below. For a detailed explanation of roles in
APIM, see link:{{
*/apim/3.x/apim\_adminguide\_roles\_and\_permissions.html* |
relative\_url }}\[Roles and permissions^\].

## Platform-wide notifications

You send APIM platform-wide notifications with the **Messages** menu
option:

image:{% link
images/apim/3.x/api-publisher-guide/messaging/message-platform-level.png
%}\[\]

You can send platform-wide notifications to users defined with the
following link:{{
*/apim/3.x/apim\_adminguide\_roles\_and\_permissions.html#scope* |
relative\_url }}\[environment scope^\] roles:

-   ADMIN

-   API\_PUBLISHER

-   USER

## API notifications

You can only send API notifications to consumers with a valid
subscription to your API applications.

You send API notifications with the API **Messages** menu option:

image:{% link
images/apim/3.x/api-publisher-guide/messaging/message-api-level.png
%}\[\]

You can send API notifications to users defined with the following
link:{{ */apim/3.x/apim\_adminguide\_roles\_and\_permissions.html#scope*
| relative\_url }}\[application scope^\] roles:

-   OWNER

-   PRIMARY\_OWNER

-   USER

# Send a notification

## Portal notification

When sending **Portal** notifications, you need to specify:

-   the user role to notify

-   the title of the notification

-   the text of the notification

When you click **SEND**, APIM sends the notification to all users
belonging to the specified role (as long as they have a valid
application subscription, in the case of API level subscriptions). They
can access the notification in APIM Console, by clicking the bell in the
top bar.

image:{% link
images/apim/3.x/api-publisher-guide/messaging/message-notifications.png
%}\[\]

The notification is also visible in the notifications area of the
system, if enabled for the browser:

image:{% link
images/apim/3.x/api-publisher-guide/messaging/message-notifications-system.png
%}\[\]

## Email notification

When sending **Email** notifications, you specify the same information
as for portal notifications.

When you click **SEND**, APIM sends an email to all the users with the
specified role who have an email address configured for their profile
(as long as they have a valid application subscription, in the case of
API level subscriptions).

For more details on configuring user profiles, see link:{{
*/apim/3.x/apim\_adminguide\_users\_and\_groups.html* | relative\_url
}}\[Users and groups^\].

## HTTP POST notification

When sending **POST HTTP message** notifications, you need to specify:

-   HTTP headers

-   whether a system proxy is to be used

-   the URL to use for the HTTP message

-   the text of the message

image:{% link
images/apim/3.x/api-publisher-guide/messaging/message-post-http.png
%}\[\]

When you click **SEND**, APIM sends the message to the URL, including
any HTTP headers specified.

# Example

In this example we will see how to send a notification to all platform
administrators.

1.  link:{{ */apim/3.x/apim\_quickstart\_console\_login.html* |
    relative\_url }}\[Log in to APIM Console^\].

2.  Click **Messages**.

3.  Select **Portal Notifications**.

4.  Choose the **ENVIRONMENT** role to notify as **ADMIN**.

5.  Give the message a **Title** and enter the detail of the message in
    **Text**.

    image:{% link
    images/apim/3.x/api-publisher-guide/messaging/message-portal-example.png
    %}\[\]

6.  Click **SEND**.

    All users with the ADMIN role are notified of new messages by a
    number on the bell in the top bar:

    image:{% link
    images/apim/3.x/api-publisher-guide/messaging/message-notifications.png
    %}\[\]

    Clicking on the bell shows the content of the message:

    image:{% link
    images/apim/3.x/api-publisher-guide/messaging/message-portal-example-notification.png
    %}\[\]
