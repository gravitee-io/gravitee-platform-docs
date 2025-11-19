# Layout and Theme Customization

## Overview

Administrators have the option to modify the layout and theme of the Developer Portal to customize how APIs are presented to API consumers. The following sections describe which elements can be modified and provide instructions:

* [API Sidebar](layout-and-theme-customization.md#api-sidebar)
* [API Catalog](layout-and-theme-customization.md#api-catalog)
* [Custom navigation](layout-and-theme-customization.md#custom-navigation)
* [Theming](layout-and-theme-customization.md#theming)

## API Sidebar

You can click on an API in the Developer Portal to access its details. Selecting the **General information** header tab will display the API's description and reviews (if any have been submitted), as well as a sidebar on the right that contains additional information.

<div data-full-width="false"><figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-05-31 at 1.57.16 PM (1).png" alt=""><figcaption><p>Developer Portal API sidebar</p></figcaption></figure></div>

{% tabs %}
{% tab title="Modify the access URL" %}
Administrators can control what is shown in the sidebar. To modify the access URL:

1. Select **Organization** at the bottom of the left sidebar of the Management Console
2. In the organization's left sidebar, select **Sharding tags** under the **Gateway** subheader
3. Modify the **Default entrypoint** of the Gravitee Gateway

The access URL for each API in the Developer Portal is the default entrypoint followed by that API's context path.

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-07-28 at 12.51.56 PM (1).png" alt=""><figcaption><p>Modify the access URL</p></figcaption></figure>

{% hint style="info" %}
**Sharding Tags and Gateway Entrypoint Mappings**

[Sharding Tags](../../../getting-started/configuration/apim-gateway/sharding-tags.md) tags are used to help manage complex distributed architectures:

* By assigning sharding tags to APIs and Gravitee Gateways, an API is deployed to a subset of the available Gateways.
* By mapping sharding tags to a Gateway’s entrypoint URL, the Developer Portal can intelligently display different entrypoints based on an API's sharding tags.
{% endhint %}
{% endtab %}

{% tab title="Modify sidebar settings" %}
To modify the sidebar settings:

1. Return to the Management Console's home page
2. Select **Settings** from the left sidebar
3. Select **API Portal Information** from the inner left sidebar to display the following options:

<figure><img src="../../../../../../.gitbook/assets/dev_portal_api_display_settings (1).png" alt=""><figcaption><p>Developer Portal API sidebar display settings</p></figcaption></figure>

* **Add extra information**
  * **Show tags list in the API header:** Display all API labels in the Developer Portal
  * **Show categories list in the API header:** Display all API categories in the Developer Portal
* **Configure the information list:** Display custom values in the Developer Portal. Use the **+** icon on the bottom right of the page to add new values.
*   **API Page list options:** Display a banner at the top of each page in the API Catalog to promote a particular API. The tab automatically determines which API to promote, e.g., the **Starred** tab will feature the API that was most recently reviewed.

    <figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-05-31 at 2.21.47 PM (1).png" alt=""><figcaption><p>Developer Portal promotion banner</p></figcaption></figure>
{% endtab %}
{% endtabs %}

## API Catalog

### Categories

{% hint style="warning" %}
Categories currently only support v2 APIs. You can learn more about the differences between v4 vs v2 [here](../../../overview/gravitee-api-definitions-and-execution-engines/).
{% endhint %}

{% hint style="info" %}
At least one API inside the category must be published for the category to be visible. You can publish an API from its Info page in the Management Console.
{% endhint %}

Administrators can modify the browsing experience offered by the Developer Portal's API Catalog. To organize APIs by category:

* API categories must be added
* One or more categories must be applied to each API
* The **Categories** tab must be added to the API Catalog

{% tabs %}
{% tab title="Edit and show categories" %}
To enable the **Categories** tab and modify categories:

1. Select **Settings** from the left sidebar of the Management Console
2. Select **Categories** from the inner left sidebar
   * Toggle **Enable Category Mode** to display the **Categories** tab
   * Create new categories and/or modify or delete existing categories

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-01 at 1.59.06 PM (1).png" alt=""><figcaption><p>APIM categories settings page</p></figcaption></figure>
{% endtab %}

{% tab title="Apply categories" %}
To apply categories:

1. Select **APIs** from the left sidebar of the Management Console
2. Select the API to which you want to add categories
3. Select **Info** from the inner left sidebar
4. Use the **Categories** dropdown to select one or more categories to apply to the API

<figure><img src="../../../../../../.gitbook/assets/api catalog_categories (1).png" alt=""><figcaption><p>Apply categories to a Gateway API</p></figcaption></figure>
{% endtab %}
{% endtabs %}

With the toggle enabled, a **Categories** tab will appear in the header of the API Catalog:

<figure><img src="../../../../../../.gitbook/assets/dev_portal_categories (1).png" alt=""><figcaption><p>Dev Portal categories page</p></figcaption></figure>

### Top/featured APIs

Administrators can also control what is displayed on the **Featured** page of the API Catalog by modifying the top APIs:

1. Select **Settings** from the left sidebar of the Management Console
2. Select **Top APIs** from the inner left sidebar

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-01 at 2.10.58 PM (1).png" alt=""><figcaption><p>Top APIs settings</p></figcaption></figure>

Administrators can use the **+** icon to add new APIs, reorder APIs, and remove APIs from the list. APIs added here are displayed on both the Developer Portal's homepage and on the API catalog's **Featured** page:

<figure><img src="../../../../../../.gitbook/assets/dev_portal_homepage (1).png" alt=""><figcaption><p>Developer Portal homepage displaying top APIs</p></figcaption></figure>

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-01 at 2.14.32 PM (1).png" alt=""><figcaption><p>Developer Portal Featured page in the API Catalog</p></figcaption></figure>

{% hint style="info" %}
**Top API visibility**

* Administrators can view all of the Gateway APIs added to the Top APIs list
* The Top APIs visible to individual users are restricted to public APIs and APIs they have been granted access to through user and group access settings
{% endhint %}

## Custom navigation

Administrators can customize the header and footer navigation of the Developer Portal by creating link pages in Gravitee's system folders. There are three types of links:

* External link
* Link to an existing documentation page
* Link to a category

Each link is treated as a new documentation page. To learn about the features and functionality of Developer Portal documentation, see [Documentation](documentation.md).

{% tabs %}
{% tab title="System folders" %}
To access Gravitee's system folders:

1. Select **Settings** from the left sidebar of the Management Console
2. Select **Documentation** from the inner left sidebar

System folders are identified by a padlock icon:

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-05 at 10.44.36 AM (1).png" alt=""><figcaption><p>Gravitee's system folders</p></figcaption></figure>

There are three system folders: `Header`, `TopFooter` and `Footer`. Each system folder corresponds to an area of the Developer Portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-link-portal-zones.png" alt=""><figcaption><p>Developer Portal - system folder mapping</p></figcaption></figure>

{% hint style="warning" %}
**`TopFooter`system folder nesting**

The`TopFooter`system folder is the only system folder that accepts nested folders, which are used to group links together. Nested folders must be published to be visible in the Developer Portal.

<img src="../../../../../../.gitbook/assets/Screenshot 2023-06-05 at 11.24.49 AM (1).png" alt="" data-size="original">
{% endhint %}
{% endtab %}

{% tab title="Manage links" %}
To create a link:

1. Open a system folder
2. Select the **+** icon
3. Select the **Link** icon

This will take you to a new page to select your link type and provide additional information about your link:

<figure><img src="../../../../../../.gitbook/assets/dev_portal_create_a_link (1).png" alt=""><figcaption><p>Create a new Developer Portal link</p></figcaption></figure>

To view your new link, click **Save** and navigate to the Developer Portal:

<figure><img src="../../../../../../.gitbook/assets/dev_portal_custom_link_example (1).png" alt=""><figcaption><p>Sample "Gravitee Homepage" custom link</p></figcaption></figure>

Each custom link offers additional features such as translations and access control. See [Documentation](documentation.md) for more information.
{% endtab %}
{% endtabs %}

## Theming

Administrators can change the default theme of the Developer Portal to a custom theme. To modify the theme:

1. Select **Settings** from the left sidebar of the Management Console
2. Select **Theme** from the inner left sidebar

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-01 at 2.50.54 PM (1).png" alt=""><figcaption><p>Developer Portal theme settings</p></figcaption></figure>

This page allows the administrator to customize every aspect of the Developer Portal's look and feel. Edits are shown in a live preview on the right.

{% hint style="warning" %}
**Enable live preview**

To enable a live preview, you must provide a Portal URL per the [General settings section](general-settings.md#general-settings).
{% endhint %}

The top menu includes the following options:

* **Fullscreen:** Opens the preview in a new window to avoid switching screens when editing.
* **Reset:** Resets the theme from the last backup. Backups occur when you select the **Save** button.
* **Save:** Saves your theme.
* **Enabled:** Activates the theme in APIM Portal.
* **Import:** Upload a custom theme in `JSON` format. To view the required structure of the `JSON` file, **Export** the current theme.
* **Export:** Downloads your current theme in `JSON` format.
* **Restore Default Theme:** Overwrites your modifications with the default theme.

### Basic customization

<table><thead><tr><th width="157.5">Property</th><th>Use case</th></tr></thead><tbody><tr><td>Images</td><td>Show logos. Optional logo is used for the homepage and the footer. Using the default logo overrides the optional logo.</td></tr><tr><td>Homepage</td><td>Add a Homepage background image.</td></tr><tr><td>Colors</td><td>Define primary, neutral, and font colors.</td></tr><tr><td>Fonts</td><td>Choose font family and sizes. Medium sizes are used by default.</td></tr></tbody></table>

### Advanced customization

Each component uses its own properties but, where possible, the properties are grouped into common variables. To further customize the Developer Portal, you can define the graphic properties to expose for each component.

For example, hover your mouse over the color bubble to see common component colors. For other property types, if a common property is used, it appears in the placeholder field.

### Override theme files

APIM API includes a default theme and two default logos, located in the `/themes` folder of the API distribution folder:

* `definition.json`
* `logo.png`
* `logo-light.png`

To customize the Developer Portal theme, either modify these three files or specify a new folder in the `gravitee.yml` file:

```yaml
# Portal themes
portal:
  themes:
    path: ${gravitee.home}/themes
```

By default, this configuration is commented out and the path is `${gravitee.home}/themes`.

For assistance creating a theme, use the editor in **Settings > Theme** and export it to a JSON file via the EXPORT button in the header menu. Keep in mind:

* Images and logos cannot be changed using this method. The two files must be edited in the distribution.
* Exported themes do not have the same format as the provided `definition.json` file, requiring minor edits to the exported theme.

Expected format:

```json
{
  "data": [
    {
      "name": "gv-theme",
      "css": [
        {
          "name": "--gv-theme-color-darker",
          "description": "Primary darker color",
          "type": "color",
          "default": "#383E3F",
          "value": "#383E3F"
        },
        ...
      ]
    },
    ...
  ]
}
```
