---
hidden: false
noIndex: false
---

# Configure OpenAPI viewer

The Gamma console and Developer Portal provide native viewers for OpenAPI specifications (OAS). By default, Gamma uses the standard Swagger UI to render OAS files.

You can configure the preferred OpenAPI viewer at the platform level, which applies globally across your environments.

## Supported viewers

Gamma supports the following OpenAPI viewers:

* **Swagger UI** (Default): The standard interactive API documentation viewer.
* **Redoc**: A highly customizable, three-panel viewer optimized for reading complex specifications.
* **Stoplight Elements**: A modern, interactive documentation component that provides a polished developer experience.

## Change the default viewer

To configure the default OpenAPI viewer for your environment:

1. In the Gamma console, navigate to **Platform Management**.
2. Select **Settings** > **OpenAPI Viewer**.
3. Choose your preferred viewer from the dropdown menu (Swagger, Redoc, or Elements).
4. *(Optional)* If using Redoc or Elements, you may configure additional rendering options specific to that viewer, such as theme colors or layout preferences.
5. Click **Save**.

The selected viewer will automatically be used to render all OpenAPI documentation pages in both the console and the Developer Portal.

<!-- Source: OpenapiViewerPage.tsx — gravitee-gamma-module-aim -->
