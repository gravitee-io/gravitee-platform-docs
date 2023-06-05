---
description: The administrator's guide to the developer portal
---

# Configuration

## Introduction

Configuration of the developer portal takes place through the management UI **Settings** page as highlighted in the image below.&#x20;

<figure><img src="../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

The developer portal settings can be broken into the following major categories:

* General settings
* User management
* Layout and theme customization
* Documentation

## General settings

This section details how to configure high-level settings for the developer portal. Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader where you have the following configuration options:

{% hint style="info" %}
**`gravitee.yaml` override**

The top of the **Settings** page states "Depending on your architecture, this configuration may be overridden by a local configuration file. See documentation for more information."

All of the general settings can be overridden with the `gravitee.yaml` file. You can learn more about the `gravitee.yaml` file in the [APIM Configuration documentation.](../../getting-started/configuration/)
{% endhint %}

* **Api-key Header:** Modify the `api-key` header shown in the developer portal's CURL commands

{% hint style="warning" %}
Note, this only impacts what is displayed in the developer portal's UI. You must modify the `gravitee.yaml` file to impact how the gateway handles the `api-key` header.
{% endhint %}

* **Portal URL:** Provide the URL of the developer portal. This will add a link to the developer portal on the top navigation bar of the management UI as shown in the image below. Additionally, the [theme editor](advanced-developer-portal-configuration.md#theme-customization) will have a live preview of the developer portal.

<figure><img src="../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to developer portal from management UI</p></figcaption></figure>

* **Override homepage title:** Activating this toggle allows you to change the developer portal title from "Unleash the power of your APIs." to a custom title
* **Options**
  * **Use Tiles Mode:** Sets the default all APIs view to tiles as opposed to a list view
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API.  Email must be configured as detailed in the [Email configuration](advanced-developer-portal-configuration.md#email-notifications) section for the contact form to work
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings
  * **Force user to fill comment:** Requires all subscription requests to have a comment
  * **Allow User Registration:** Allow API consumers to create an account from the developer portal. Email must be configured as detailed in the [Email configuration](advanced-developer-portal-configuration.md#email-notifications) section for registration to work.
    * **Enable automatic validation:** Automatically approve all accounts created on the developer portal
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the developer portal
  * <mark style="color:yellow;">**Allow Upload Images:**</mark> <mark style="color:yellow;"></mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>
* **OpenAPI Viewers:** Select the viewer you would like to use to display your API documentation
* **Schedulers:** Configure the frequency the developer portal runs background tasks such as syncing data and sending/receiving notifications
* <mark style="color:yellow;">**Documentation:**</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>

## User management

Accessing the developer portal directly from the management UI automatically signs you in with the same account. However, the power of the developer portal revolves around exposing your APIs to both internal and external API consumers. This necessitates the ability to create new accounts which requires some additional configuration. This section walks administrators through everything they need to know about user management.

### User sign-up

The ability to create new user accounts has two requirements:

1. Enabling the **Allow User Registration** option
2. Simple mail transfer protocol (SMTP) configuration to confirm user account creation

As detailed in [General settings](advanced-developer-portal-configuration.md#general-settings), the **Allow User Registration** option is already enabled by default.&#x20;

To view SMTP settings, navigate to **Settings** in the management UI. Then, in the secondary sidebar, select **Settings** under the **Portal** header in the submenu. The **SMTP** settings are at the bottom of the page; however, for many deployments, these settings will be greyed out. This is due to the `gravitee.yml` configuration file disabling email by default since it requires configuring an SMTP email service. This [SMTP configuration guide](../../getting-started/configuration/) will walk you through setting up email for your APIM deployment.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-05 at 12.03.55 PM.png" alt=""><figcaption><p>SMTP default settings</p></figcaption></figure>

After configuring SMTP, you should be able to create a new user in the developer portal. You can test this by opening the developer portal in an incognito window to avoid being automatically signed in with the same account being used in the management UI. In the new incognito window, select **Sign up** at the bottom of the modal. Provide the required information and select the **Sign Up** button.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-05 at 12.14.03 PM.png" alt=""><figcaption><p>Developer portal sign up page</p></figcaption></figure>

You should receive a registration confirmation and an email to the address you provided. Open the email and open the link. Make sure the link opens in the incognito tab; otherwise, it will just open the developer portal with the account signed into the management UI.

You will be taken to a page to finalize your account and add a password. By default, the password must meet the following requirements:

* 8 to 32 characters
* no more than 2 consecutive equal characters
* min 1 special characters (@ & # …)
* min 1 upper case character

{% hint style="info" %}
**Password customization**

Password requirements can be modified by changing the regex pattern under **User Management Configuration** in the `gravitee.yml` file or by using environment variables. Additionally, you can provide [custom UI errors](https://docs.gravitee.io/am/current/am\_userguide\_user\_management\_password\_policy.html#custom\_ui\_errors) for future new users by modifying the sign-up and register HTML templates.
{% endhint %}

Once you finish creating your password, you should be able to sign in without issue. The newly created external user will also be immediately visible in the admin’s management console. Leave the incognito window and return to the standard window where you are signed in as an admin in the management UI. In the sidebar menu, you can reach your organization settings by clicking on **Organization** at the bottom. Once there, navigate to the **Users** tab in the sidebar. Here you will see a list of all current users tied to the organization. As an admin, you can click on any user for more details and to apply administrative policies. Additionally, admins can pre-register users by clicking the **Add user** button in the top right.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/712b65b5d81ff0459a41a4f2f76487611d5ce4f8_2_690x312.png" alt=""><figcaption></figcaption></figure>

Next, click on **Applications** in the sidebar. Interestingly, you should see a new application called **Default application** which is owned by the user you just created.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/186f0300a51db63b3fece375675232e15e40486e_2_690x312.png" alt=""><figcaption></figcaption></figure>

In order to allow new users to quickly move forward with API consumption, the default settings are every new user automatically has a default application created. This can be easily disabled through the aforementioned three configuration options.

## Layout and theme customization

This section will detail how to modify how APIs are presented to API consumers.

### API Sidebar&#x20;

Administrators can modify what is shown in the sidebar of an API's **General information**.

<div data-full-width="false">

<figure><img src="../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM.png" alt=""><figcaption><p>Developer portal API sidebar</p></figcaption></figure>

</div>

In APIM, select **API Portal Information** in the secondary sidebar to display the following options:

<figure><img src="../../.gitbook/assets/dev_portal_api_display_settings.png" alt=""><figcaption><p>Developer portal API sidebar display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the developer portal
  * **Show categories list in the API header:** Display all API categories in the developer portal
* **Configure the information list:** Display custom values in the developer portal. Use the **+ icon** in the bottom right to add new values.
* **API Page list options:** Detailed in the [catalog tabs](advanced-developer-portal-configuration.md#catalog-tabs) section below

{% hint style="info" %}
Additionally, API publishers can modify the API sidebar by adding links to external documentation as detailed in the [Publish APIs documentation](publish-apis.md).
{% endhint %}

### API Catalog

Administrators can also modify how API consumers browsing experience in the developer portal's API catalog.&#x20;

#### Promotion banner

In APIM, select **API Portal Information** in the secondary sidebar to display the following options shown below.&#x20;

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* The other options are detailed in the [API sidebar](advanced-developer-portal-configuration.md#api-sidebar) section above.
*   **API Page list options**

    * **Display promotion banner:** Adds a banner to the top of each page in the API catalog to promote a particular API. The API that is promoted is determined automatically based on the tab. For example, the **Starred** tab will show the API that was most recently reviewed in the promotion banner.

    <figure><img src="../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM.png" alt=""><figcaption><p>Developer portal promotion banner</p></figcaption></figure>

#### Categories tab

Administrators have the option to include a **Categories** tab in the API catalog. This organizes APIs based on the category applied to a gateway API. Categories can be added on the **General** page of a gateway API as shown below:

<figure><img src="../../.gitbook/assets/api_categories.png" alt=""><figcaption><p>Applying categories to a gateway API</p></figcaption></figure>

To enable the Categories tab in the developer portal, go to APIM and select **Categories** in the secondary sidebar. Here you can also create new categories and modify or delete existing categories.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-01 at 1.59.06 PM.png" alt=""><figcaption><p>APIM categories settings page</p></figcaption></figure>

With the toggle enabled, users accessing the developer portal will have access to the page shown below:

<figure><img src="../../.gitbook/assets/dev_portal_categories.png" alt=""><figcaption><p>Dev portal categories page</p></figcaption></figure>

#### Top/featured APIs

Administrators also have control over what is displayed on the **Featured** page of the API catalog by modifying the top APIs. Navigate to APIM **Settings** and select **Top APIs** in the secondary sidebar.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-01 at 2.10.58 PM.png" alt=""><figcaption><p>Top APIs settings</p></figcaption></figure>

From here, administrators can add new APIs with the **+ icon**, reorder the top APIs, and remove APIs from the list. APIs added here are displayed on both the developer portal's homepage and on the API catalog's **Featured** page as shown below.

<figure><img src="../../.gitbook/assets/dev_portal_homepage.png" alt=""><figcaption><p>Developer portal homepage displaying top APIs</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-01 at 2.14.32 PM.png" alt=""><figcaption><p>Developer portal Featured page in API catalog</p></figcaption></figure>

{% hint style="info" %}
**Top API visibility**

If you are having issues seeing gateway APIs you added to the Top APIs list, make sure the API is public or the user logged into the developer portal has access to that API. Administrators can see all the APIs but individual users are restricted to public APIs and APIs they have been granted access to through user and group access settings.
{% endhint %}

### Navigation

Administrators can customize the developer portal navigation in the header and footer. This is done by creating link pages in Gravitee's system folders. There are three kinds of links:

* External link
* Link to an existing documentation page
* Link to a category

Each link is treated as a new documentation page. To learn about all the features and functionality of developer portal documentation, head to the[ Documentation section](advanced-developer-portal-configuration.md#documentation) of this page.

#### System folders

Gravitee's system folders are accessible in the management UI under **Settings > Documentation** and can be identified by their padlock icon as shown below.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-05 at 10.44.36 AM.png" alt=""><figcaption><p>Gravitee's system folders</p></figcaption></figure>

There are three system folders: `Header`, `TopFooter` and `Footer`. Each system folder corresponds to an area of the developer portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-link-portal-zones.png" alt=""><figcaption><p>Developer portal - system folder mapping</p></figcaption></figure>

{% hint style="warning" %}
**`TopFooter`system folder nesting**

The`TopFooter`system folder is the only system folder that accepts nested folders. As shown in the image above, folders nested under the `TopFooter` system folder are used to group links together.

It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

#### Manage Links <a href="#manage_links" id="manage_links"></a>

To create a link, open a system folder and select the **+ icon** then select the **Link** icon**.** This will take you to a new page to select your link type and provide some additional information about your link.

<figure><img src="../../.gitbook/assets/dev_portal_create_a_link.png" alt=""><figcaption><p>Create a new developer portal link</p></figcaption></figure>

Select **Save**, and navigate to the developer portal to see your new link in action.

<figure><img src="../../.gitbook/assets/dev_portal_custom_link_example.png" alt=""><figcaption><p>Sample "Gravitee Homepage" custom link</p></figcaption></figure>

Each custom link has additional features such as translations and access control that you can learn more about in the [Documentation section](advanced-developer-portal-configuration.md#documentation).

{% hint style="warning" %}
**Publishing`TopFooter`nested folders**

The`TopFooter`system folder is the only system folder that accepts nested folders. It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

### Theming

Administrators can change the default theme of the developer portal to their own custom theme. To modify the theme, in the APIM settings select **Theme** in the secondary sidebar.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-01 at 2.50.54 PM.png" alt=""><figcaption><p>Developer portal theme settings</p></figcaption></figure>

This page allows the administrator to customize every aspect of the developer portal's look and feel. Edits made are shown in a live preview to the right.

{% hint style="warning" %}
**Enable live preview**

If you are not seeing a live preview, this is due to not providing a Portal URL as detailed in the [General settings section](advanced-developer-portal-configuration.md#general-settings).
{% endhint %}

#### Top menu

The top menu provides the following options:

* **Fullscreen:** This button opens the preview in a new window, making it easier to edit if you have several screens
* **Reset:** This button allows you to reset the theme from the last backup. Backups occur when you select the **Save** button
* **Save:** This button saves your theme
* **Enabled:** This toggle activates the theme in APIM Portal
* **Import:** Upload a custom theme in `JSON` format. To see the required structure of the `JSON` file, export the current theme
* **Export:** Download your current theme in `JSON` format
* **Restore Default Theme:** This button overwrites your modifications with the theme provided by default

## Documentation

Outside of APIs and applications, administrators can also provide site-wide documentation for API publishers and consumers. Developer portal site-wide documentation is accessed on the **Documentation** page as shown below.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-05 at 10.24.20 AM.png" alt=""><figcaption><p>Developer portal documentation page</p></figcaption></figure>

