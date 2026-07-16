---
description: Create and manage AsyncAPI documentation pages in the New Developer Portal navigation.
---

# Creating AsyncAPI Documentation Pages

## Overview

The New Developer Portal supports **AsyncAPI** documentation pages alongside Gravitee Markdown and OpenAPI pages. Portal administrators create and edit AsyncAPI pages in the portal navigation editor; portal users browse published content in the portal UI.

AsyncAPI pages use a single interactive documentation viewer — there is no choice of viewer.

## Prerequisites

Before creating AsyncAPI documentation pages, ensure you have the following:

* The New Developer Portal enabled. For more information, see [configure-the-new-portal.md](../configure-the-new-portal.md).
* Access to the portal navigation editor in the Management Console.

## Add an AsyncAPI page

When creating a new documentation page in portal navigation, administrators can choose **AsyncAPI** from the page type selector (alongside Gravitee Markdown and OpenAPI).

1. From the **Dashboard**, click **Settings**.
2. From the **Settings** menu, click **Settings**.
3. Navigate to the **New Developer Portal** section, and then click **Open Settings**. The New Developer Portal settings open on the navigation tab.
4. Click **Add**, and then click **Add Page**.
5. In the **Add page** pop-up screen, type a title for your page.
6. Select **AsyncAPI** as the page type.
7. (Optional) Turn on the **Authentication is required to view this page** toggle.
8. Click **Add**.

New AsyncAPI pages are created with a **starter AsyncAPI 3.0 template** so editing can begin immediately, similar to default content for other page types.

## Editing experience

The AsyncAPI editor follows the same split-panel pattern as the OpenAPI editor:

* **Left:** YAML editor for the specification
* **Right:** Live preview of the rendered documentation

The preview is optimised for the Console's side-by-side layout so the specification remains readable while editing.

## Validation on save

Before a page is saved, the Console checks that the content is valid YAML and looks like an AsyncAPI document:

* The YAML must parse correctly
* The document must include an `asyncapi` version field
* The version must be a valid semantic version (e.g. `3.0.0`)

If validation fails, the user sees an error message and the page is not saved. The platform also rejects empty content.

## Viewing in the portal

Published AsyncAPI pages are rendered using an interactive AsyncAPI documentation viewer. Visitors can browse channels, messages, and other spec details in the same way as for other embedded API documentation formats.

## Typical workflow

1. In the Console, add a new page to portal navigation and select **AsyncAPI** as the type.
2. Edit the starter specification in the YAML editor; use the live preview to check the result.
3. Save and publish the page in the desired folder.
4. Portal users open the page and browse the rendered AsyncAPI documentation.
