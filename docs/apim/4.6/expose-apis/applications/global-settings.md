# Global Settings

## Overview

The **Global settings** section displays general application details and includes a Danger Zone for executing functional and sometimes irreversible actions.&#x20;

<figure><img src="../../.gitbook/assets/1 global 1.png" alt=""><figcaption></figcaption></figure>

Some general details are common to all applications, and others vary by application type.

## Manage applications

An application is usually shared through a developer application and retrieves information such as API keys and API analytics. Initially, only the application’s creator can view and manage the application. By default, APIM includes three membership roles:

<table><thead><tr><th width="228">Role</th><th>Description</th></tr></thead><tbody><tr><td><strong>Primary owner</strong></td><td>The creator of the application. Can perform all possible API actions.</td></tr><tr><td><strong>Owner</strong></td><td>A lighter version of the primary owner role. Can perform all possible actions except delete the application.</td></tr><tr><td><strong>User</strong></td><td>A person who can access the application in read-only mode and use it to subscribe to an API.</td></tr></tbody></table>

{% hint style="info" %}
Only users with the required permissions can manage application members. See [User Management](../../administration/user-management.md).
{% endhint %}

### Delete and restore applications

To delete an application, the primary owner must:

1. Log in to your APIM Console
2. Select **Applications** from the left nav
3. Select your application
4. Select **Global Settings** from the inner left nav
5.  In the **Danger Zone**, click **Delete**&#x20;

    <figure><img src="../../.gitbook/assets/delete application.png" alt=""><figcaption><p>Delete an application</p></figcaption></figure>

* A deleted application has a status of `ARCHIVED`, meaning:
  * The link to the primary owner of the application is deleted.
  * Its subscriptions are closed. In the case of a subscription to an API Key plan, the keys are revoked.
  * Notification settings are deleted.
* An `ADMIN`can restore applications in the APIM Console and will become the primary owner of the application
  * An application’s subscriptions will be restored with`PENDING` status. The API publisher must manually reactivate previous subscriptions.
