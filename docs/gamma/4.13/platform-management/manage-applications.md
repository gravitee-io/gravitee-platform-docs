---
hidden: false
noIndex: false
---

# Manage applications

Applications represent external consumers that call your APIs. The Applications page in the Gamma console lets you view, create, and manage the applications that subscribe to your API plans.

## View applications

From the Gamma console sidebar, select **Platform Management**, then navigate to **Applications**. The page header shows KPI tiles for **Active applications** and **Archived applications** counts.

The applications table displays:

* **Name** — Application name (sortable)
* **Type** — Application type (Backend, Service, Web, etc.)
* **Owner** — The user who created the application
* **Actions** — Edit and management actions

Use the search bar to filter applications by name. The **Active/Archived** dropdown filter toggles between active and archived application views. When viewing archived applications, you can restore them directly from the table using the restore action. The list supports pagination for large application sets.

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-1763f30d911da54e240765f4394566d04264e60d%2Fgamma-platform-applications.png?alt=media" alt="Platform Applications page showing a searchable table of consumer applications with type and owner columns"><figcaption><p>The Applications page lists all consumer applications with their type (Backend, Service, Web) and owner. Use the search bar and Active/Archived filter to find specific applications.</p></figcaption></figure>

## Create an application


1. Select **Register Application** from the applications list.
2. Enter the application details:

| Field           | Description                                                      | Required |
| --------------- | ---------------------------------------------------------------- | -------- |
| **Name**        | A human-readable name to identify the application.               | Yes      |
| **Description** | Freeform text describing the application's purpose.              | Yes      |
| **Domain**      | The domain associated with this application.                     | No       |
| **Groups**      | Assign the application to one or more groups for access control. | No       |

3. Select the application type:

| Type                   | Description                                                             | Redirect URIs required |
| ---------------------- | ----------------------------------------------------------------------- | ---------------------- |
| **Simple**             | Basic application with an optional client ID. No OAuth grant types.     | No                     |
| **SPA (Browser)**      | Single-page application. Default grant type: Authorization Code.        | Yes                    |
| **Web**                | Server-side web application. Default grant type: Authorization Code.    | Yes                    |
| **Native**             | Mobile or desktop application. Default grant type: Authorization Code.  | Yes                    |
| **Backend-to-Backend** | Machine-to-machine application. Default grant type: Client Credentials. | No                     |

4. For OAuth-enabled types (SPA, Web, Native, Backend-to-Backend), configure grant types and redirect URIs as required.
5. For TLS-based authentication, upload a client certificate in the TLS settings section.
6. Select **Create** to register the application.

## Application details

Select an application from the list to view its detail page, which includes:

* **General** — Name, description, type, domain, group membership, client ID, certificates, and metadata. The metadata editor includes built-in safeguards to highlight and prevent saving duplicate custom keys.
* **User Permissions** — Manage direct members, configure group access, and transfer application ownership.
* **Notifications** — Configure email and webhook notifications for application events.
* **Subscriptions** — Active subscriptions to API plans. View subscription status, manage API keys, and see subscription history.
<!-- Source: ApplicationUserPermissionsPage.tsx L1-L100, ApplicationNotificationSettingsPage.tsx L1-L100, gravitee-gamma-module-platform @ d1bb5f8af7 -->

## Next steps

* [Manage resources](manage-resources.md) — Configure shared resources used across your APIs.
* [Establish consumer access](../api-management/build/configure-your-api-proxy/establish-consumer-access.md) — Set up subscriptions between applications and API plans.
