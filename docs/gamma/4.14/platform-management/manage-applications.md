---
hidden: false
noIndex: false
description: View, create, and manage the consumer applications that subscribe to your API plans. Follow the steps to work with them on the Applications page.
---

# Manage applications

Applications represent external consumers that call your APIs. The Applications page in the Gamma console lets you view, create, and manage the applications that subscribe to your API plans.

## View applications

From the Gamma console sidebar, select **Platform Management**, and then navigate to **Applications**. The page header shows KPI tiles for the **Active applications** and **Archived applications** counts.

The applications table displays the following columns:

* **Name**. The application name. You can sort the table on this column.
* **Type**. The application type, such as Backend, Service, or Web.
* **Owner**. The user who created the application.
* **Actions**. A row menu that contains the **View Details** and **Manage Subscriptions** actions.

Use the search bar to filter applications by name. The **Active**/**Archived** dropdown filter toggles between the active and archived application views. The archived view lists each application with the date it was archived, and you can restore an application directly from its row. The **View** control chooses which columns the table displays, and the list supports pagination for large application sets.

<figure><img src=".gitbook/assets/gamma-platform-applications.png" alt="Platform Applications page showing a searchable table of consumer applications with type and owner columns"><figcaption><p>The Applications page lists all consumer applications with their type (Backend, Service, Web) and owner. Use the search bar and Active/Archived filter to find specific applications.</p></figcaption></figure>

## Create an application

To create an application, complete the following steps:

1. From the applications list, select **Register Application**.
2. In the **General** section, enter the application details described in the following table:

    | Field           | Description                                         | Required |
    | --------------- | --------------------------------------------------- | -------- |
    | **Name**        | A human-readable name to identify the application.  | Yes      |
    | **Description** | Freeform text describing the application's purpose. | Yes      |
    | **Domain**      | The domain associated with this application.        | No       |

3. Optional: under **Groups**, select the groups to attach to the application. The field appears when the environment has groups, and it's required when the organization requires a group on every application. See [Manage groups](manage-groups.md).
4. In the **Security** section, select the application type. **Simple** is a standalone client for which you manage your own client ID. Additional OAuth application types are available only when Dynamic Client Registration is enabled for the environment. See [Configure client registration](configure-client-registration.md).
5. Complete the remaining **Security** fields described in the following table:

    | Field                              | Description                                                                                                   | Required |
    | ---------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------- |
    | **Type**                           | A freeform descriptor of the application, such as mobile or web.                                              | No       |
    | **Client ID**                      | The client ID of the application. This field is required to subscribe to certain types of API plan, such as OAuth2 and JWT. | No       |
    | **Client Certificate (PEM Only)**  | The PEM-encoded client certificate of the application. This field is required to subscribe to certain mTLS plans. | No       |

6. Select **Create Application**.

## Application details

Select an application from the list to open its detail page, which contains the following sections:

* **Overview**. A setup checklist for the application and a snapshot of its subscription counts.
* **Settings**. The application details, OAuth client configuration, and mTLS client certificates. The details include the application name, description, domain, images, owner, creation date, type, API key mode, and client ID. This section also holds the action that archives the application.
* **User Permissions**. Manage direct members, configure group access, and transfer application ownership.
* **Subscriptions**. The plans this application subscribes to. Create a subscription, filter by API and status, search by API key, and review each subscription's status and dates.
* **Shared API Keys**. The API keys that every subscription of the application shares. This section shows only for an application that uses a shared API key. Renew the key, and revoke a key that's still valid. See [Renew the shared API key](#renew-the-shared-api-key).
* **Notifications**. Configure the events that trigger a notifier for this application, using either the default email notifier or the default webhook notifier. This section also holds the custom metadata available in notification templates. The metadata editor rejects a duplicate key and reports that the metadata already exists.

## Renew the shared API key

Renewing the shared API key moves every subscription of the application to a new key, and the previous key stays valid for two hours. When **Allow custom API Key** is turned on in [Configure Security Plan Types](configure-security-plan-types.md), the **Renew API Key** dialog has a **Custom API Key** field. Enter the value that the application's consumers already send, or leave the field empty to generate a random key.

The **Renew** button shows when you can manage the subscriptions of the application, and not for an archived application.

To renew the shared API key, complete the following steps:

1. Open **Platform Management**.
2. Click **Applications**.
3. Select your application.
4. Click **Shared API Keys** in the **Access** group of the application sidebar.
5. Click **Renew**.
6. Optional: In **Custom API Key**, enter the value of the new key.

    <figure><img src=".gitbook/assets/gamma-application-shared-api-key-renew.png" alt="The Renew API Key dialog over the Shared API Keys page of an application, with docbot-shared-key-2026 entered in the Custom API Key field and the Cancel and Renew buttons"><figcaption><p>Renew the shared API key with a custom API key</p></figcaption></figure>
7. Click **Renew**.

A custom API key follows these rules:

* It has between 8 and 128 characters, and `^ # % @ \ / ; = ? | ~ ,` and the space character are invalid. Spaces at the start and the end of the value are removed.
* A value that belongs to another application of the environment, or the application's current key, is refused with `This API key cannot be used`.
* A value of an earlier key of the application, even a revoked or expired one, makes that key valid again. Any other value creates a new key.

The new key shows in the **API Keys** list with no date under **Revoked/Expired at**, and the previous key shows the time it expires.

<figure><img src=".gitbook/assets/gamma-application-shared-api-keys.png" alt="The Shared API Keys page of an application, listing docbot-shared-key-2026 as valid with no Revoked/Expired at date, and the previous key with a Revoked/Expired at time two hours after the renewal"><figcaption><p>The Shared API Keys page after a renewal</p></figcaption></figure>

## Next steps

* [Establish consumer access](../api-management/build/configure-your-api-proxy/establish-consumer-access.md). Configure subscriptions between applications and API plans.
* [Configure client registration](configure-client-registration.md). Choose the application types this environment accepts, and configure the provider that registers OAuth clients for them.
