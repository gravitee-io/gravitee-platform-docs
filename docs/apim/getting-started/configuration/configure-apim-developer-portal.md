# Configure APIM Developer Portal

## Configuration file

The configuration file for APIM Portal is `assets\config.json`. The default configuration is included below:

```
Unresolved directive in installation-guide-portal-ui-configuration.adoc - include::https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-portal-webui/src/assets/config.json[]
```

The only mandatory value in `config.json` file is `baseURL`, which describes the location of the APIM API Portal endpoint. You must set this value for APIM Portal to send requests to the endpoint.

## Configure the Portal theme

The default theme of the Developer Portal can be customized in the APIM Console via **Settings > Theme**:

<figure><img src="../../.gitbook/assets/settings_theme.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
To use the live preview on the right, the Portal settings must be configured with a Portal URL. Whenever a setting is changed, the change is reflected in the live preview.
{% endhint %}

<figure><img src="../../.gitbook/assets/portal_url.png" alt=""><figcaption></figcaption></figure>

### Top menu

| Button                   | Function                                                                        |
| ------------------------ | ------------------------------------------------------------------------------- |
| FULLSCREEN               | Opens the preview in a new window. Only visible if the Portal UI is configured. |
| RESET                    | Resets the theme using the last backup.                                         |
| SAVE                     | Saves the theme.                                                                |
| ENABLED                  | Activates the theme in the Portal                                               |
| RESTORE TO DEFAULT THEME | Overwrites modifications with the default theme.                                |

### Basic customization

| Property | Use case                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------- |
| Images   | Show logos. Optional logo is used for the home page and the footer. Use default logo overrides Optional logo. |
| Homepage | Add a Homepage background image.                                                                              |
| Colors   | Define primary, neutral, and font colors.                                                                     |
| Fonts    | Choose font family and sizes. Medium sizes are used by default.                                               |

### Advanced customization

If you want to customize further, you can define the graphic properties to expose for each component.

Each component uses its own properties, but where possible, we group the properties into common variables such as the ones listed in [Basic customization](https://docs.gravitee.io/apim/3.x/apim\_installguide\_portal\_ui\_configuration.html#basic\_customization) above.

You can see common component colors, for example, by holding your mouse over the color bubble. For other property types, if a common property is used, you can see this in the placeholder field.

## Override theme files

APIM API includes a default theme and two default logos, located in the `/themes` folder of the API distribution folder:

* `definition.json`
* `logo.png`
* `logo-light.png`

To customize the Portal theme, either modify these three files or specify a new folder in the `gravitee.yml` file:

```
# Portal themes
portal:
  themes:
    path: ${gravitee.home}/themes
```

By default, this configuration is commented out and the path is `${gravitee.home}/themes`

For assistance creating a theme, use&#x20;

|   | <p>To help you to create your theme, you can use the editor in <strong>Settings > Theme</strong> and export it to a JSON file with the <strong>EXPORT</strong> button in the top menu. However, there are two important things to keep in mind:</p><ul><li>Images and logos cannot be changed using this method. You need to edit the two files in the distribution.</li><li>Exported themes do not have the same format as the provided <code>definition.json</code> file. You will need to make some minor edits to the exported theme.</li></ul><p><strong>Expected format</strong></p><pre><code>{
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
</code></pre> |
| - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
