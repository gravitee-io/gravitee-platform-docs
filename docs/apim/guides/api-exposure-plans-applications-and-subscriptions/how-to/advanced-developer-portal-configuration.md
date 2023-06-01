---
description: The administrator's guide to the developer portal
---

# Configuration

## Introduction

Configuration of the developer portal takes place through the management UI settings. Each of the following sections will focus on a tab in the secondary sidebar highlighted in the image below.

<figure><img src="../../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

The developer portal settings can be broken into the following major categories:

* General Settings
* API Configuration
* Theme Customization
* Email Configuration
* Analytics

## General settings

Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader. As shown in the arcade above, you have the following configuration options:

* **Api-key Header:** Modify the `api-key` header shown in the developer portal's CURL commands

{% hint style="warning" %}
Note, this only impacts the developer portal's UI. You must modify the YAML configuration to impact the gateway.
{% endhint %}

* **Portal URL:** Provide the URL of the developer portal. This will add a link to the developer portal on the top navigation bar of the management UI as shown in the image below. Additionally, the [theme editor](advanced-developer-portal-configuration.md#theme-customization) will have a live preview of the developer portal.

<figure><img src="../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to developer portal from management UI</p></figcaption></figure>

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

{% hint style="info" %}
All of the general settings can be overridden in the `gravitee.yaml` file as detailed in the Configuration section.
{% endhint %}

## Layout and Theme customization

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
* **API Page list options:** Detailed in the [catalog tabs](advanced-developer-portal-configuration.md#catalog-tabs) section below

### API Catalog

Administrators can also modify how API consumers browsing experience in the developer portal's API catalog.&#x20;

#### Promotion banner

In APIM, select **API Portal Information** in the secondary sidebar to display the following options shown below.&#x20;

<figure><img src="../../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* The other options are detailed in the [API sidebar](advanced-developer-portal-configuration.md#api-sidebar) section above.
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

### Theming

* Choosing a pre-built theme or creating a custom theme
* Configuring the color scheme and fonts of the Developer Portal
* Uploading custom CSS and JavaScript files

## Email notifications

* Configuring the email server settings
* Enabling and configuring email notifications for developers and API administrators

## Analytics and reporting

* Enabling and configuring analytics for the Developer Portal
* Configuring reporting options for API administrators

## Site Documentation

* Adding a homepage
* Adding high-level docs
