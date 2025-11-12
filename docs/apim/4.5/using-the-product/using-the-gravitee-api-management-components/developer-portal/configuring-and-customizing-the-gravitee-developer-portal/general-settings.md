---
description: >-
  This section describes how to configure the high-level settings of the
  Developer Portal
---

# Configuring the Developer Portal Settings

## Configure settings

1. Log in to the Management Console
2. Select **Settings** from the left sidebar
3.  Select **Settings** from the inner left sidebar&#x20;

    <figure><img src="../../../../.gitbook/assets/dev portal_settings.png" alt=""><figcaption></figcaption></figure>
4.  Scroll down to the **Portal** header&#x20;

    <figure><img src="../../../../.gitbook/assets/dev portal_portal.png" alt=""><figcaption></figcaption></figure>
5. Configure the settings described below:

{% hint style="info" %}
The general settings of the Developer Portal can be overridden with the `gravitee.yaml` file. For more information about the `gravitee.yaml` file, see the [APIM Configuration documentation.](docs/apim/4.5/using-the-product/using-the-gravitee-api-management-components/configuration.md)
{% endhint %}

* **Api-key Header:** Modify the `api-key` header shown in the Developer Portal's CURL commands. This only impacts what is displayed in the Developer Portal's UI. You must modify the `gravitee.yaml` file to change how the Gateway handles the `api-key` header.
*   **Portal URL:** Enter the URL of the Developer Portal. This will add a link to the Developer Portal on the top navigation bar of the Management Console. Additionally, the [theme editor](general-settings.md#theme-customization) will show a live preview of the Developer Portal.&#x20;

    <figure><img src="../../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to Developer Portal from Management Console</p></figcaption></figure>
* **Override homepage title:** Toggling to ON allows you to change the Developer Portal title from "Unleash the power of your APIs." to a custom title
* **Options**
  * **Use Tiles Mode:** Sets the default view of APIs to tiles as opposed to a list
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API. Email must be configured per the [Email configuration](general-settings.md#email-notifications) section to use the contact form.
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings
  * **Force user to fill comment:** Requires all subscription requests to include a comment
  * **Allow User Registration:** Allow API consumers to create an account from the Developer Portal. Email must be configured per the [Email configuration](general-settings.md#email-notifications) section to enable registration.
    * **Enable automatic validation:** Automatically approve all accounts created on the Developer Portal
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the Developer Portal
  * **Allow Upload Images:** Allows documentation owners to attach images as additional resources
  * **Max size upload file (bytes):** Controls the size of images that documentation owners are allowed to attach
* **OpenAPI Viewers:** Choose a viewer to display your API documentation
* **Schedulers:** Configure the frequency with which the Developer Portal runs background tasks such as syncing data and sending/receiving notifications
*   **(v2 APIs only) Documentation URL:** Set the URL shown at the end of the v2 API creation flow&#x20;

    <figure><img src="../../../../.gitbook/assets/documentation_url (1).png" alt=""><figcaption><p>Documentation URL setting for v2 API creation flow</p></figcaption></figure>
