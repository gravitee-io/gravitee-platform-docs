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

## API display configuration

This section will detail how to modify the way your APIs are presented to API consumers. Specifically, what is shown in the sidebar of the **General information** screen of an API.

<div data-full-width="false">

<figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM.png" alt=""><figcaption><p>Developer portal API sidebar</p></figcaption></figure>

</div>

In APIM, select **API Portal Information** in the secondary sidebar to display the following options:

<figure><img src="../../../.gitbook/assets/dev_portal_api_display_settings.png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the developer portal
  * **Show categories list in the API header:** Display all API categories in the developer portal
* **Configure the information list:** Display custom values in the developer portal. Use the **+ icon** in the bottom right to add new values
* #### API Page list options
  *   **Display promotion banner:** Adds a banner to the top of each API tab to promote a particular API. The API that is promoted is determined automatically based on the tab. For example, the **Starred** tab will show the API that most recently reviewed in the promotion banner

      <figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM.png" alt=""><figcaption></figcaption></figure>





*   #### API Page list options


*
* Configuring the API listing and sorting options
* Setting the default API category and tags
* Enabling and configuring the API search bar

## Theme customization

* Choosing a pre-built theme or creating a custom theme
* Configuring the color scheme and fonts of the Developer Portal
* Uploading custom CSS and JavaScript files

## Localization and internationalization

* Configuring the default language and locale settings
* Adding and managing translations for the Developer Portal

## Email notifications

* Configuring the email server settings
* Enabling and configuring email notifications for developers and API administrators

## Analytics and reporting

* Enabling and configuring analytics for the Developer Portal
* Configuring reporting options for API administrators

## Conclusion

* Summary of the configuration settings covered in the documentation
* Additional resources for further learning and troubleshooting.
