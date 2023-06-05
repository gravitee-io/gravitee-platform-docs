---
description: The administrator's guide to the developer portal
---

# Configuration

## Introduction

Configuration of the developer portal takes place through the management UI **Settings** page as highlighted in the image below.&#x20;

<figure><img src="../../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

The developer portal settings can be broken into the following major categories:

* General Settings
* User sign-up and support
* Layout and theme customization
* Documentation

## General settings

Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader. As shown in the arcade above, you have the following configuration options:

* **Api-key Header:** Modify the `api-key` header shown in the developer portal's CURL commands

{% hint style="warning" %}
Note, this only impacts the developer portal's UI. You must modify the YAML configuration to impact the gateway.
{% endhint %}

* **Portal URL:** Provide the URL of the developer portal. This will add a link to the developer portal on the top navigation bar of the management UI as shown in the image below. Additionally, the [theme editor](./#theme-customization) will have a live preview of the developer portal.

<figure><img src="../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to developer portal from management UI</p></figcaption></figure>

* **Override homepage title:** Activating this toggle allows you to change the developer portal title from "Unleash the power of your APIs." to a custom title
* **Options**
  * **Use Tiles Mode:** Sets the default all APIs view to tiles as opposed to a list view
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API.  Email must be configured as detailed in the [Email configuration](./#email-notifications) section for the contact form to work
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings
  * **Force user to fill comment:** Requires all subscription requests to have a comment
  * **Allow User Registration:** Allow API consumers to create an account from the developer portal. Email must be configured as detailed in the [Email configuration](./#email-notifications) section for registration to work.
    * **Enable automatic validation:** Automatically approve all accounts created on the developer portal
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the developer portal
  * <mark style="color:yellow;">**Allow Upload Images:**</mark> <mark style="color:yellow;"></mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>
* **OpenAPI Viewers:** Select the viewer you would like to use to display your API documentation
* **Schedulers:** Configure the frequency the developer portal runs background tasks such as syncing data and sending/receiving notifications
* <mark style="color:yellow;">**Documentation:**</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>

{% hint style="info" %}
All of the general settings can be overridden in the `gravitee.yaml` file as detailed in the Configuration section.
{% endhint %}

## User sign-up and support

Email settings

## Layout and theme customization

This section will detail how to modify how APIs are presented to API consumers.

### API Sidebar&#x20;

Administrators can modify what is shown in the sidebar of an API's **General information**.

<div data-full-width="false">

<figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM.png" alt=""><figcaption><p>Developer portal API sidebar</p></figcaption></figure>

</div>

In APIM, select **API Portal Information** in the secondary sidebar to display the following options:

<figure><img src="../../../.gitbook/assets/dev_portal_api_display_settings.png" alt=""><figcaption><p>Developer portal API sidebar display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the developer portal
  * **Show categories list in the API header:** Display all API categories in the developer portal
* **Configure the information list:** Display custom values in the developer portal. Use the **+ icon** in the bottom right to add new values.
* **API Page list options:** Detailed in the [catalog tabs](./#catalog-tabs) section below

{% hint style="info" %}
Additionally, API publishers can modify the API sidebar by adding links to external documentation as detailed in the [Publish APIs documentation](../publish-apis.md).
{% endhint %}

### API Catalog

Administrators can also modify how API consumers browsing experience in the developer portal's API catalog.&#x20;

#### Promotion banner

In APIM, select **API Portal Information** in the secondary sidebar to display the following options shown below.&#x20;

<figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* The other options are detailed in the [API sidebar](./#api-sidebar) section above.
*   **API Page list options**

    * **Display promotion banner:** Adds a banner to the top of each page in the API catalog to promote a particular API. The API that is promoted is determined automatically based on the tab. For example, the **Starred** tab will show the API that was most recently reviewed in the promotion banner.

    <figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM.png" alt=""><figcaption><p>Developer portal promotion banner</p></figcaption></figure>

#### Categories tab

Administrators have the option to include a **Categories** tab in the API catalog. This organizes APIs based on the category applied to a gateway API. Categories can be added on the **General** page of a gateway API as shown below:

<figure><img src="../../../.gitbook/assets/api_categories.png" alt=""><figcaption><p>Applying categories to a gateway API</p></figcaption></figure>

To enable the Categories tab in the developer portal, go to APIM and select **Categories** in the secondary sidebar. Here you can also create new categories and modify or delete existing categories.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 1.59.06 PM.png" alt=""><figcaption><p>APIM categories settings page</p></figcaption></figure>

With the toggle enabled, users accessing the developer portal will have access to the page shown below:

<figure><img src="../../../.gitbook/assets/dev_portal_categories.png" alt=""><figcaption><p>Dev portal categories page</p></figcaption></figure>

#### Top/featured APIs

Administrators also have control over what is displayed on the **Featured** page of the API catalog by modifying the top APIs. Navigate to APIM **Settings** and select **Top APIs** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.10.58 PM.png" alt=""><figcaption><p>Top APIs settings</p></figcaption></figure>

From here, administrators can add new APIs with the **+ icon**, reorder the top APIs, and remove APIs from the list. APIs added here are displayed on both the developer portal's homepage and on the API catalog's **Featured** page as shown below.

<figure><img src="../../../.gitbook/assets/dev_portal_homepage.png" alt=""><figcaption><p>Developer portal homepage displaying top APIs</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.14.32 PM.png" alt=""><figcaption><p>Developer portal Featured page in API catalog</p></figcaption></figure>

{% hint style="info" %}
**Top API visibility**

If you are having issues seeing gateway APIs you added to the Top APIs list, make sure the API is public or the user logged into the developer portal has access to that API. Administrators can see all the APIs but individual users are restricted to public APIs and APIs they have been granted access to through user and group access settings.
{% endhint %}

### Navigation

Administrators can customize the developer portal navigation in the header and footer. This is done by creating link pages in Gravitee's system folders. There are three kinds of links:

* External link
* Link to an existing documentation page
* Link to a category

Each link is treated as a new documentation page. To learn about all the features and functionality of developer portal documentation, head to the[ Documentation section](./#documentation) of this page.

#### System folders

Gravitee's system folders are accessible in the management UI under **Settings > Documentation** and can be identified by their padlock icon as shown below.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.44.36 AM.png" alt=""><figcaption><p>Gravitee's system folders</p></figcaption></figure>

There are three system folders: `Header`, `TopFooter` and `Footer`. Each system folder corresponds to an area of the developer portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-link-portal-zones.png" alt=""><figcaption><p>Developer portal - system folder mapping</p></figcaption></figure>

{% hint style="warning" %}
**`TopFooter`system folder nesting**

The`TopFooter`system folder is the only system folder that accepts nested folders. As shown in the image above, folders nested under the `TopFooter` system folder are used to group links together.

It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

#### Manage Links <a href="#manage_links" id="manage_links"></a>

To create a link, open a system folder and select the **+ icon** then select the **Link** icon**.** This will take you to a new page to select your link type and provide some additional information about your link.

<figure><img src="../../../.gitbook/assets/dev_portal_create_a_link.png" alt=""><figcaption><p>Create a new developer portal link</p></figcaption></figure>

Select **Save**, and navigate to the developer portal to see your new link in action.

<figure><img src="../../../.gitbook/assets/dev_portal_custom_link_example.png" alt=""><figcaption><p>Sample "Gravitee Homepage" custom link</p></figcaption></figure>

Each custom link has additional features such as translations and access control that you can learn more about in the [Documentation section](./#documentation).

{% hint style="warning" %}
**Publishing`TopFooter`nested folders**

The`TopFooter`system folder is the only system folder that accepts nested folders. It is important to note that nested folders must be published to be seen in the developer portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

### Theming

Administrators can change the default theme of the developer portal to their own custom theme. To modify the theme, in the APIM settings select **Theme** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.50.54 PM.png" alt=""><figcaption><p>Developer portal theme settings</p></figcaption></figure>

This page allows the administrator to customize every aspect of the developer portal's look and feel. Edits made are shown in a live preview to the right.

{% hint style="warning" %}
**Enable live preview**

If you are not seeing a live preview, this is due to not providing a Portal URL as detailed in the [General settings section](./#general-settings).
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

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.24.20 AM.png" alt=""><figcaption><p>Developer portal documentation page</p></figcaption></figure>

