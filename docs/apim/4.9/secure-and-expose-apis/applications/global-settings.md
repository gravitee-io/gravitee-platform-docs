---
description: An overview about global settings.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/secure-and-expose-apis/applications/global-settings
---

# Global Settings

## Overview

An application's **Global settings** include general application details and a Danger Zone for executing functional and sometimes irreversible actions.

## Configure global settings

To configure global settings, complete the following steps:

1. [create-an-application.md](create-an-application.md "mention").
2. Log in to your APIM Console, and then click **Applications**.
3.  Find the application you want to configure. Use the radio buttons to select either Active or Archived applications. Next, either scroll through the paginated lists of available applications or use the search field to find the application by name.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 7 (1).png" alt=""><figcaption></figcaption></figure>
4. Click on the application you want to configure.
5.  Click on **Global settings** in the Application menu.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 1 (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Some general details are common to all applications, and others vary by application type.
{% endhint %}

## Application management

Initially, only the application’s creator can view and manage the application. By default, APIM includes three membership roles:

<table><thead><tr><th width="228">Role</th><th>Description</th></tr></thead><tbody><tr><td><strong>Primary owner</strong></td><td>The creator of the application. Can perform all possible API actions.</td></tr><tr><td><strong>Owner</strong></td><td>A lighter version of the primary owner role. Can perform all possible actions except delete the application.</td></tr><tr><td><strong>User</strong></td><td>A person who can access the application in read-only mode and use it to subscribe to an API.</td></tr></tbody></table>

{% hint style="info" %}
Only users with the required permissions can manage application members. See [User Management](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md).
{% endhint %}

### Delete and restore applications

To delete an application, the primary owner must:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select your application
4. Select **Global Settings** from the inner left nav
5.  In the **Danger Zone**, click **Delete**

    <figure><img src="../../.gitbook/assets/00 groups added to applications 2 (1).png" alt=""><figcaption></figcaption></figure>

* A deleted application has a status of `ARCHIVED`, meaning:
  * The link to the primary owner of the application is deleted.
  * Its subscriptions are closed. In the case of a subscription to an API Key plan, the keys are revoked.
  * Notification settings are deleted.
* An `ADMIN`can restore applications in the APIM Console and will become the primary owner of the application
  * An application’s subscriptions will be restored with `PENDING` status. The API publisher must manually reactivate previous subscriptions.
