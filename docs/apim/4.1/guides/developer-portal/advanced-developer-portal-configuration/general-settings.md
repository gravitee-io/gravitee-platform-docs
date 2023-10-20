# General Settings

This section details how to configure high-level settings for the Developer Portal. Select the **Settings** tab in the secondary sidebar and scroll down to the **Portal** subheader where you have the following configuration options:

{% hint style="info" %}
`gravitee.yml` override

The top of the **Settings** page states "Depending on your architecture, this configuration may be overridden by a local configuration file. See documentation for more information."

All of the general settings can be overridden with the `gravitee.yaml` file. You can learn more about the `gravitee.yaml` file in the [APIM Configuration documentation.](../../../getting-started/configuration/)
{% endhint %}

* **Api-key Header:** Modify the `api-key` header shown in the Developer Portal's CURL commands

{% hint style="warning" %}
Note, this only impacts what is displayed in the Developer Portal's UI. You must modify the `gravitee.yaml` file to impact how the Gateway handles the `api-key` header.
{% endhint %}

* **Portal URL:** Provide the URL of the Developer Portal. This will add a link to the Developer Portal on the top navigation bar of the Management Console as shown in the image below. Additionally, the [theme editor](general-settings.md#theme-customization) will have a live preview of the Developer Portal.

<figure><img src="../../../.gitbook/assets/dev_portal_link.png" alt=""><figcaption><p>Link to Developer Portal from Management Console</p></figcaption></figure>

* **Override homepage title:** Activating this toggle allows you to change the Developer Portal title from "Unleash the power of your APIs." to a custom title
* **Options**
  * **Use Tiles Mode:** Sets the default all APIs view to tiles as opposed to a list view
  * **Activate Support:** Adds a **Contact** and **Tickets** tab to each API. Email must be configured as detailed in the [Email configuration](general-settings.md#email-notifications) section for the contact form to work
  * **Activate Rating:** Allow API consumers to leave written reviews and ratings
  * **Force user to fill comment:** Requires all subscription requests to have a comment
  * **Allow User Registration:** Allow API consumers to create an account from the Developer Portal. Email must be configured as detailed in the [Email configuration](general-settings.md#email-notifications) section for registration to work.
    * **Enable automatic validation:** Automatically approve all accounts created on the Developer Portal
  * **Add Google Analytics:** Add a Google Analytics tracking ID to the Developer Portal
  * **Allow Upload Images:** Allows documentation owners to attach images as additional resources
  * **Max size upload file (bytes):** Controls the size of images documentation owners are allowed to attach
* **OpenAPI Viewers:** Select the viewer you would like to use to display your API documentation
* **Schedulers:** Configure the frequency the Developer Portal runs background tasks such as syncing data and sending/receiving notifications
* **Documentation URL:** Set the URL shown at the end of the v2 API creation flow. Note, this currently only applies to v2 APIs.

<figure><img src="../../../.gitbook/assets/documentation_url.png" alt=""><figcaption><p>Documentation URL setting for v2 API creation flow</p></figcaption></figure>
