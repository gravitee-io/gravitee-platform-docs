---
description: The administrator's guide to the developer portal
---

# Configuration

## Introduction

Configuration of the developer portal takes place through the management UI settings as shown in the image below.

<figure><img src="../../../.gitbook/assets/dev_portal_settings.png" alt=""><figcaption><p>Developer portal settings</p></figcaption></figure>

The developer portal settings can be broken into the following major categories:

* General Settings
* API Configuration
* Theme Customization
* Email Configuration
* Analytics

## General settings

Arcade



Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader. As shown in the arcade above, you have the following configuration options:

* **Api-key Header:** Modify the api-key header shown in the developer portal's CURL commands. Note, this only impacts the developer portal's UI. You must modify the YAML configuration to impact the gateway
* **Portal URL:** Provide the URL of the developer portal. This will add a link to the developer portal on the top navigation bar of the management UI as shown in the image below. Additionally, the [theme editor](advanced-developer-portal-configuration.md#theme-customization) will have a live preview of the developer portal.

<figure><img src="../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to developer portal from management UI</p></figcaption></figure>

* **Override homepage title:** Activating this toggle allows you to change the developer portal title from "Unleash the power of your APIs." to a custom title.
* **Options** toggles
  * **Use Tiles Mode:** Sets the default all APIs view to tiles as opposed to a list view.
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API.  Email must be configured as detailed in the [Email configuration](advanced-developer-portal-configuration.md#email-notifications) section for the contact form to work.
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings.
  * **Force user to fill comment:** Unleash the power of your APIs.
  * **Allow User Registration:** Allow API consumers to create an account from the developer portal. Email must be configured as detailed in the [Email configuration](advanced-developer-portal-configuration.md#email-notifications) section for registration to work.
    * **Enable automatic validation:** Automatically approve all accounts created on the developer portal.
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the developer portal.
  * <mark style="color:yellow;">**Allow Upload Images:**</mark> <mark style="color:yellow;"></mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>
* **OpenAPI Viewers:** Select the viewer you would like to use to display your API documentation
* **Schedulers: Configure the frequency the developer portal runs background tasks such as syncing data and sending/receiving notifications**
* <mark style="color:yellow;">**Documentation:**</mark> <mark style="color:yellow;"></mark><mark style="color:yellow;">Unknown</mark>

{% hint style="info" %}
All of the general settings can be overridden in the `gravitee.yaml` file as detailed in the Configuration section.
{% endhint %}

## API configuration

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
