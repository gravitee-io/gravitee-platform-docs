---
description: Guide to configuring APIM Developer Portal.
---

# Configure APIM Developer Portal

## Configuration file

The configuration file for APIM Portal is `assets\config.json`. The default configuration is included below:

{% code title="config.json" %}
```json
{
  "baseURL": "/portal/environments/DEFAULT",
  "homepage": {
    "featured": {
      "size": 9
    }
  },
  "loaderURL": "assets/images/gravitee-loader.gif",
  "pagination": {
    "size": {
      "default": 10,
      "values": [5, 10, 25, 50, 100]
    }
  }
}
```
{% endcode %}

The only mandatory value in `config.json` file is `baseURL`, which describes the location of the APIM API Portal endpoint. You must set this value for APIM Portal to send requests to the endpoint.

## Configure the Portal theme

The default theme of the Developer Portal can be customized in the APIM Console via **Settings > Theme**:

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
To use the live preview on the right, the Portal settings must be configured with a Portal URL. Whenever a setting is changed, the change is reflected in the live preview.
{% endhint %}

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

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

Each component uses its own properties but, where possible, the properties are grouped into common variables such as the basic examples above. To further customize the Portal, you can define the graphic properties to expose for each component.

For example, hover your mouse over the color bubble to see common component colors. For other property types, if a common property is used, it appears in the placeholder field.

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

By default, this configuration is commented out and the path is `${gravitee.home}/themes`.

For assistance creating a theme, use the editor in **Settings > Theme** and export it to a JSON file via the EXPORT button in the header menu. Keep in mind:

* Images and logos cannot be changed using this method. The two files must be edited in the distribution.
* Exported themes do not have the same format as the provided `definition.json` file, which requires minor edits to the exported theme.

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
