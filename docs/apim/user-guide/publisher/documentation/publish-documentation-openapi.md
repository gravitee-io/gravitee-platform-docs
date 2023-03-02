# publish-documentation-openapi

## Overview

OpenAPI pages can be translated or come from an external source, and their access can be restricted.\
See link:\{{ _/apim/3.x/apim\_publisherguide\_publish\_documentation.html#manage\_pages_ | relative\_url \}}\[Publish documentation] for more information.

The sections below describe specific configuration for OpenAPI pages.

## Edit an OpenAPI page

You can use the **PAGE** editor to edit an OpenAPI page’s raw content and preview it.

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-swagger-editor.png %\}\[]

## Add links to a documentation page

You can add a direct link to an existing OpenAPI or Markdown page. Only _published_ pages can be linked.\
To link a page, click **Insert page link** in the toolbar, select a page and click **ADD**.

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-markdown-add-page-link-1.png %\}\[]

A new link is added in the editor.\
The text of the link can be customized but the _path_ must not be changed.

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-markdown-add-page-link-2.png %\}\[]

## Viewer

You can choose the renderer for your OpenAPI file.

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-swagger-configuration-viewer.png %\}\[,300]

You can also edit this configuration globally in the settings to change your default renderer or disable a renderer.

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-openapi-configuration-viewer.png %\}\[]

### Swagger-UI configuration

If you choose **Swagger-UI** as the viewer, you can configure the following options:

image::\{% link images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-swagger-configuration.png %\}\[]
