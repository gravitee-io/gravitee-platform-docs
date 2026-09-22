---
description: An application's global settings hold its details and a danger zone for destructive actions in API Management 4.11. Learn what each does.
metaLinks:
  alternates:
    - global-settings.md
---

# Global Settings

## Overview

An application's **Global settings** include general application details and a Danger Zone for executing functional and sometimes irreversible actions.

## Configure global settings

To configure global settings, complete the following steps:

1. [create-an-application.md](create-an-application.md "mention").
2. Log in to your APIM Console, and then click **Applications**.
3.  Find the application you want to configure. Use the radio buttons to select either Active or Archived applications. Next, either scroll through the paginated lists of available applications or use the search field to find the application by name.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 7.png" alt="The Applications list filtered by a search term, showing two matching applications with their type and owner."><figcaption></figcaption></figure>
4. Click on the application you want to configure.
5.  Click on **Global settings** in the Application menu.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 1.png" alt="An application&#x27;s Global settings page, showing its name and description beside the owner, creation date, type, and API key mode, above OAuth2 and TLS panels and a Danger Zone."><figcaption></figcaption></figure>

{% hint style="info" %}
Some general details are common to all applications, and others vary by application type.
{% endhint %}

## Certificates

The **Certificates** section of the **Global settings** page lists the client certificates of the application. An application needs at least one active certificate to subscribe to an [mTLS plan](../plans/mtls.md), and it holds several certificates at once so that you rotate them without downtime. For the statuses, the grace period, and the automatic revocation, see [mTLS certificate management for applications](mtls-certificate-management-for-applications-overview-and-concepts.md).

<figure><img src="../../.gitbook/assets/application-certificates-section.png" alt="The Certificates section of an application&#x27;s Global settings page, empty, with the Add certificate button"><figcaption><p>Certificates section of the Global settings page</p></figcaption></figure>

The section shows one row per certificate.

| Column                   | Description                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**                 | The name given to the certificate when it was added.                                                                                                          |
| **Uploaded**             | When the certificate was added.                                                                                                                               |
| **Expiry date and time** | The expiration date of the certificate itself.                                                                                                                |
| **Status**               | **Active**, **Scheduled**, or **Expired**. An active certificate whose end date is 15 days away or less shows the number of days left instead of **Active**.  |
| **Actions**              | **View details** shows the name, subject, issuer, and expiration of the certificate. **Revoke certificate** deletes the certificate after a confirmation.     |

To add a certificate, click **Add certificate** and follow the steps in [How to add a client certificate](../plans/mtls.md#how-to-add-a-client-certificate). Users who aren't allowed to update the application don't see the **Add certificate** button. When the application is archived or managed by the Gravitee Kubernetes Operator, the section is read-only: neither **Add certificate** nor **Revoke certificate** is shown.

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

    <figure><img src="../../.gitbook/assets/00 groups added to applications 2.png" alt="An application&#x27;s Global settings page with the Delete action circled in the Danger Zone."><figcaption></figcaption></figure>

* A deleted application has a status of `ARCHIVED`, meaning:
  * The link to the primary owner of the application is deleted.
  * Its subscriptions are closed. In the case of a subscription to an API Key plan, the keys are revoked.
  * Notification settings are deleted.
* An `ADMIN`can restore applications in the APIM Console and will become the primary owner of the application
  * An application’s subscriptions will be restored with `PENDING` status. The API publisher must manually reactivate previous subscriptions.
