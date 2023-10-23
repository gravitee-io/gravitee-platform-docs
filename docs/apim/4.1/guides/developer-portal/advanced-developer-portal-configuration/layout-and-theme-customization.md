---
description: This article describes how to modify how APIs are presented to API consumers
---

# Layout and Theme Customization

## API Sidebar

Clicking on an API in the Developer Portal&#x20;

Administrators can modify what is shown in the sidebar of an API's **General information**.

<div data-full-width="false">

<figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM.png" alt=""><figcaption><p>Developer portal API sidebar</p></figcaption></figure>

</div>

To modify the access URL, select **Organization** in the sidebar of the Management Console. Next, select **Sharding tags** in the sidebar under the **Gateway** subheader. This page allows you to modify the **Default entrypoint** of the Gravitee Gateway. The access URL for each API in the Developer Portal will display the default entrypoint followed by that API's contect path.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-07-28 at 12.51.56 PM.png" alt=""><figcaption><p>Modify the access URL</p></figcaption></figure>

{% hint style="info" %}
&#x20;**Sharding Tags and Gateway Entrypoint Mappings**

At a high-level, sharding tags are assigned to APIs and Gravitee Gateways to provide a method to deploy an API to a subset of gateways. Adding a mapping between these sharding tags and a gateway’s entrypoint URL allows the developer portal to intelligently display different entrypoints depending on the API’s sharding tags.

Sharding tags are used to help manage complex distributed architectures. Check out the [Sharding Tags guide](../../../getting-started/configuration/the-gravitee-api-gateway/configure-sharding-tags-for-your-gravitee-api-gateways.md) to learn more.
{% endhint %}

For the rest of the sidebar settings, return to the Console's homescreen then select **Settings >** **API Portal Information** to display the following options:

<figure><img src="../../../.gitbook/assets/dev_portal_api_display_settings.png" alt=""><figcaption><p>Developer portal API sidebar display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the Developer Portal
  * **Show categories list in the API header:** Display all API categories in the Developer Portal
* **Configure the information list:** Display custom values in the Developer Portal. Use the **+ icon** in the bottom right to add new values.
* **API Page list options:** Detailed in the [catalog tabs](layout-and-theme-customization.md#catalog-tabs) section below

## API Catalog

Administrators can also modify how API consumers browsing experience in the Developer Portal's API catalog.

#### Promotion banner

In APIM, select **API Portal Information** in the secondary sidebar to display the following options shown below.

<figure><img src="../../../.gitbook/assets/image (41).png" alt=""><figcaption><p>Developer portal API display settings</p></figcaption></figure>

* The other options are detailed in the [API sidebar](layout-and-theme-customization.md#api-sidebar) section above.
*   **API Page list options**

    * **Display promotion banner:** Adds a banner to the top of each page in the API catalog to promote a particular API. The API that is promoted is determined automatically based on the tab. For example, the **Starred** tab will show the API that was most recently reviewed in the promotion banner.

    <figure><img src="../../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM.png" alt=""><figcaption><p>Developer portal promotion banner</p></figcaption></figure>

#### Categories tab

Administrators have the option to include a **Categories** tab in the API catalog. This organizes APIs based on the category applied to a Gateway API. Categories can be added on the **General** page of a Gateway API as shown below:

<figure><img src="../../../.gitbook/assets/api_categories.png" alt=""><figcaption><p>Applying categories to a Gateway API</p></figcaption></figure>

To enable the Categories tab in the Developer Portal, go to APIM and select **Categories** in the secondary sidebar. Here you can also create new categories and modify or delete existing categories.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 1.59.06 PM.png" alt=""><figcaption><p>APIM categories settings page</p></figcaption></figure>

With the toggle enabled, users accessing the Developer Portal will have access to the page shown below:

<figure><img src="../../../.gitbook/assets/dev_portal_categories.png" alt=""><figcaption><p>Dev portal categories page</p></figcaption></figure>

#### Top/featured APIs

Administrators also have control over what is displayed on the **Featured** page of the API catalog by modifying the top APIs. Navigate to APIM **Settings** and select **Top APIs** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.10.58 PM.png" alt=""><figcaption><p>Top APIs settings</p></figcaption></figure>

From here, administrators can add new APIs with the **+ icon**, reorder the top APIs, and remove APIs from the list. APIs added here are displayed on both the Developer Portal's homepage and on the API catalog's **Featured** page as shown below.

<figure><img src="../../../.gitbook/assets/dev_portal_homepage.png" alt=""><figcaption><p>Developer portal homepage displaying top APIs</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.14.32 PM.png" alt=""><figcaption><p>Developer portal Featured page in API catalog</p></figcaption></figure>

{% hint style="info" %}
**Top API visibility**

If you are having issues seeing Gateway APIs you added to the Top APIs list, make sure the API is public or the user logged into the Developer Portal has access to that API. Administrators can see all the APIs but individual users are restricted to public APIs and APIs they have been granted access to through user and group access settings.
{% endhint %}

## Custom navigation

Administrators can customize the Developer Portal navigation in the header and footer. This is done by creating link pages in Gravitee's system folders. There are three kinds of links:

* External link
* Link to an existing documentation page
* Link to a category

Each link is treated as a new documentation page. To learn about all the features and functionality of Developer Portal documentation, head to the[ Documentation section](layout-and-theme-customization.md#documentation) of this page.

#### System folders

Gravitee's system folders are accessible in the Management Console under **Settings > Documentation** and can be identified by their padlock icon as shown below.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.44.36 AM.png" alt=""><figcaption><p>Gravitee's system folders</p></figcaption></figure>

There are three system folders: `Header`, `TopFooter` and `Footer`. Each system folder corresponds to an area of the Developer Portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-link-portal-zones.png" alt=""><figcaption><p>Developer portal - system folder mapping</p></figcaption></figure>

{% hint style="warning" %}
**`TopFooter`system folder nesting**

The`TopFooter`system folder is the only system folder that accepts nested folders. As shown in the image above, folders nested under the `TopFooter` system folder are used to group links together.

It is important to note that nested folders must be published to be seen in the Developer Portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

#### Manage Links <a href="#manage_links" id="manage_links"></a>

To create a link, open a system folder and select the **+ icon** then select the **Link** icon. This will take you to a new page to select your link type and provide some additional information about your link.

<figure><img src="../../../.gitbook/assets/dev_portal_create_a_link.png" alt=""><figcaption><p>Create a new Developer Portal link</p></figcaption></figure>

Select **Save**, and navigate to the Developer Portal to see your new link in action.

<figure><img src="../../../.gitbook/assets/dev_portal_custom_link_example.png" alt=""><figcaption><p>Sample "Gravitee Homepage" custom link</p></figcaption></figure>

Each custom link has additional features such as translations and access control that you can learn more about in the [Documentation section](layout-and-theme-customization.md#documentation).

{% hint style="warning" %}
**Publishing`TopFooter`nested folders**

The`TopFooter`system folder is the only system folder that accepts nested folders. It is important to note that nested folders must be published to be seen in the Developer Portal.

<img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM.png" alt="" data-size="original">
{% endhint %}

## Theming

Administrators can change the default theme of the Developer Portal to their own custom theme. To modify the theme, in the APIM settings select **Theme** in the secondary sidebar.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-01 at 2.50.54 PM.png" alt=""><figcaption><p>Developer portal theme settings</p></figcaption></figure>

This page allows the administrator to customize every aspect of the Developer Portal's look and feel. Edits made are shown in a live preview to the right.

{% hint style="warning" %}
**Enable live preview**

If you are not seeing a live preview, this is due to not providing a Portal URL as detailed in the [General settings section](layout-and-theme-customization.md#general-settings).
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
