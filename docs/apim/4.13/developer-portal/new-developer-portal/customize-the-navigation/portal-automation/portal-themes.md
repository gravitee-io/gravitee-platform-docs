---
description: Declare the colors, font, custom CSS, logo, favicon, and background image of the New Developer Portal as code, and select the theme a portal uses. Learn how themes and portals relate.
---

# Automate portal themes

## Overview

A theme is the look and feel of the New Developer Portal: its colors, font, custom CSS, logo, favicon, and background image. With the Automation API, you declare a theme as code and select it on the portal. The same settings are available on the **Theme** page of the New Developer Portal settings. For more information, see [Style the New Developer Portal](../../layout-and-theme.md).

## How themes and portals relate

An environment holds several themes, and the portal shows one of them. Applying a theme stores it without activating it. The portal's `activeThemeHrid`, or `spec.themeRef` on the `Portal` resource, selects the theme consumers see:

* Applying the portal with `activeThemeHrid` enables that theme and disables the other New Developer Portal themes of the environment.
* Applying the portal without `activeThemeHrid`, after a theme was active, disables that theme and re-enables the theme of the environment that was updated most recently, preferring a theme that isn't managed by the Automation API. When no other theme exists, the portal shows the default theme.
* Applying the portal with an `activeThemeHrid` that matches no theme fails with `404`.
* Changing the active theme of a portal requires the `ENVIRONMENT_THEME` update permission, in addition to the portal permissions. Without it, the request fails with `403`.
* Deleting a theme that a portal uses fails with `400` and the message `Theme cannot be deleted as it is still referenced by portal(s).` Remove `activeThemeHrid` from the portal first. Deleting a theme that no portal uses re-enables another theme the same way as clearing `activeThemeHrid` does.

## Create a theme

### Using the Automation API

1. Send a `PUT` request to `/organizations/{orgId}/environments/{envId}/portal-themes` with the theme specification.
2. Specify the theme's HRID, display name, and definition, and optionally its logo, optional logo, favicon, and background image.
3. Apply the portal with `activeThemeHrid` set to the theme's HRID. For more information, see [Create a portal](README.md#create-a-portal).
4. Retrieve a theme by sending a `GET` request to `/organizations/{orgId}/environments/{envId}/portal-themes/{hrid}`.
5. Delete a theme by sending a `DELETE` request to the same path.

| Property          | Description                                                                                                                                                                 | Example                                   |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `hrid`            | Human-readable ID of the theme. Required.                                                                                                                                   | `brand-theme`                             |
| `name`            | Display name of the theme. Required.                                                                                                                                        | `Brand theme`                             |
| `definition`      | Visual definition of the theme. Required. Holds `customCss`, `font.fontFamily`, and `color` with `primary`, `secondary`, `tertiary`, `error`, `background.page`, and `background.card`. Each value is optional, and an omitted value keeps the APIM default. | See the example                           |
| `logo`            | Logo shown in the portal header, as an inline data URI. Optional.                                                                                                           | `data:image/png;base64,...`               |
| `optionalLogo`    | Alternate logo for contexts where the primary logo doesn't render well, as an inline data URI. Optional.                                                                    | `data:image/png;base64,...`               |
| `favicon`         | Browser tab icon, as an inline data URI. Optional.                                                                                                                          | `data:image/svg+xml;base64,...`           |
| `backgroundImage` | Image shown behind the portal header, as an inline data URI. Optional.                                                                                                      | `data:image/png;base64,...`               |

Font and color values are CSS values: a `font-family` value for `font.fontFamily`, and a color value for each entry of `color`.

**Example request:**

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portal-themes?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "brand-theme",
  "name": "Brand theme",
  "definition": {
    "customCss": ".portal { padding: 0; }",
    "font": {
      "fontFamily": "\"Inter\", sans-serif"
    },
    "color": {
      "primary": "#123456",
      "secondary": "#654321",
      "tertiary": "#abcdef",
      "error": "#ff0000",
      "background": {
        "page": "#ffffff",
        "card": "#f4f4f4"
      }
    }
  },
  "favicon": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxIDEiLz4="
}
```
{% endcode %}

Then select the theme on the portal:

{% code overflow="wrap" %}
```http
PUT /organizations/{orgId}/environments/{envId}/portals?dryRun=false
Content-Type: application/json
Authorization: Bearer {token}

{
  "hrid": "default-portal",
  "name": "Default Portal",
  "structure": {
    "topNavbar": [
      {
        "path": "/projects/alpha",
        "displayName": "Alpha"
      }
    ]
  },
  "activeThemeHrid": "brand-theme"
}
```
{% endcode %}

For the full endpoint reference, see [Automation API endpoint reference](README.md#automation-api-endpoint-reference).

### Using Kubernetes CRDs

1. Define a `PortalTheme` resource with a reference to your `ManagementContext`, a display name, and a definition.
2. Reference the theme from the `Portal` resource with `spec.themeRef`.
3. Apply both manifests with `kubectl apply -f portal-theme.yaml -f portal.yaml`.

**Example PortalTheme custom resource:**

{% code title="portal-theme.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: PortalTheme
metadata:
  name: brand-theme
  namespace: gravitee
spec:
  contextRef:
    name: "apim-context"
  name: "Brand theme"
  definition:
    customCss: |
      .portal { padding: 0; }
    font:
      fontFamily: '"Inter", sans-serif'
    color:
      primary: "#123456"
      secondary: "#654321"
      tertiary: "#abcdef"
      error: "#ff0000"
      background:
        page: "#ffffff"
        card: "#f4f4f4"
  favicon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxIDEiLz4="
```
{% endcode %}

**Example Portal custom resource that uses the theme:**

{% code title="portal.yaml" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Portal
metadata:
  name: default-portal
  namespace: gravitee
spec:
  contextRef:
    name: "apim-context"
  name: "Default Portal"
  themeRef:
    name: brand-theme
    kind: PortalTheme
  structure:
    topNavbar:
      - path: /projects/alpha
        displayName: Alpha
```
{% endcode %}

{% hint style="warning" %}
**Constraints:**

* `spec.contextRef` is required on a `PortalTheme`.
* `spec.themeRef` on a `Portal` resolves to a `PortalTheme` resource. The `kind` defaults to `PortalTheme` when omitted, and any other kind is rejected with `themeRef [<name>] is of kind <kind>, but only PortalTheme is supported`. A reference that doesn't resolve is rejected with `portal [<name>] references theme [<ref>] that can't be resolved`.
* Removing `spec.themeRef` from a `Portal` deactivates the theme, as described in [How themes and portals relate](#how-themes-and-portals-relate).
* The GKO admission webhook rejects the deletion of a `PortalTheme` that a `Portal` still references.
{% endhint %}
