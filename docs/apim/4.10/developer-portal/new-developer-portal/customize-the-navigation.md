---
description: Customize New Developer Portal 4.10 navigation and manage which APIs appear in it. Follow the steps to organize the portal.
---

# Customize the navigation

## Overview


In the New Developer Portal, you can customize the navigation of your Developer Portal by using the **Navigation items** section of the New Developer Portal settings.

You can create the following elements for your navigation:

* **Pages**: Content of your New Developer Portal documentation.
* **Folders**: Use these to group related pages together into sections.
* **Links**: Connect your documentation to external sites or other internal resources.
* **APIs**: List your APIs in the New Developer Portal documentation.

When you add a new page, you can customize the page with Gravitee Markdown, which is standard Markdown enriched with dynamic components. For more information about Gravitee Markdown, see[gravitee-markdown-components.md](gravitee-markdown-components.md "mention").

{% hint style="info" %}
In releases earlier than APIM 4.10.5, navigation items aren't shown to unauthenticated users of the New Developer Portal. If anonymous visitors don't see public navigation items, upgrade to APIM 4.10.5 or later. AsyncAPI page rendering in the New Developer Portal requires APIM 4.10.7 or later.
{% endhint %}

### Default navigation items

By default, some pages are already created for you with content. These pages are published and public by default. Here are the following folders, pages, and links that are created by default:

* A folder named Guides, which contains a Getting Started page.
* A folder Core concepts, which contains a page that describes making your first API call and a page that describes authentication.
* A link to Docs that brings you to the Gravitee documentation.

#### Console view

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.05.51.png" alt="The Manage your navigation page, with a navigation tree on the left, a Markdown editor in the middle, and a live preview of the rendered page on the right."><figcaption></figcaption></figure>

#### Developer portal view

The default navigation appears on your New Developer Portal

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.06.57.png" alt="The developer portal home page, showing a welcome headline, Explore all APIs and Get started buttons, a banner image, and a toolkit section below."><figcaption></figcaption></figure>

Welcome page in the Developer Portal:

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.07.11.png" alt="A rendered guide page in the developer portal, showing the welcome content beside a navigation tree of guides and core concepts."><figcaption></figcaption></figure>

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Customizing your navigation

With the New Developer Portal, you can customize your navigation in the following ways:

* [Add a page](customize-the-navigation.md#pages)
* [Add a folder](customize-the-navigation.md#folders)
* [Add a link](customize-the-navigation.md#links)
* [Add an API](customize-the-navigation.md#api)

1.  From the **Dashboard**, click **Settings**.<br>

    <figure><img src="../../.gitbook/assets/EB3744C8-A282-4EC2-9DB6-218361CB3FA7_1_201_a.jpeg" alt="The console dashboard with Settings highlighted in the left navigation, showing 2,711 APIs and 855 applications."><figcaption></figcaption></figure>
2.  From the **Settings** menu, click **Settings**.<br>

    <figure><img src="../../.gitbook/assets/CF7527D1-5E90-4637-8C70-FF5125AEB0BF_1_201_a.jpeg" alt="The portal Analytics settings with Settings highlighted in the portal menu, listing nine platform dashboards."><figcaption></figcaption></figure>
3.  Navigate to the **New Developer Portal** section, and then click **Open Settings**. The New Developer Portal settings open on the navigation tab.<br>

    <figure><img src="../../.gitbook/assets/7C64309D-426F-4F5D-B48D-2224931FC9F3_4_5005_c.jpeg" alt="The portal settings scrolled to the New Developer Portal section, with the portal enabled and the Open Settings button highlighted beside Open Website."><figcaption></figcaption></figure>
4. Customize your navigation using the following components:

{% tabs %}
{% tab title="Pages" %}
When you add a page that is not in a folder, the page appears as a root level menu item. When you publish the page, the page appears in the top navigation bar of your New Developer Portal.

**Add a page**

1.  Click **Add**, and then click **Add Page**.<br>

    <figure><img src="../../.gitbook/assets/FB8F0725-08EB-4B68-B365-122337D12C4F_1_201_a.jpeg" alt="The Manage your navigation page with the Add menu open and Add Page highlighted above Add Link and Add Folder."><figcaption></figcaption></figure>
2. In the **Add page** pop-up screen, type a title for your page.
3. (Optional) Turn on the **Authentication is required to view this page.** toggle. This toggle ensures that the user must be signed in to the New Developer Portal to see the page.
4.  Click **Add**.\
    Here we need to mention that now we can add 2 types of pages Gravitee markdown and OpenAPI. here are the screenshots:

    <figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--251.png" alt="The Add page dialog with Markdown selected as the page type, a page title entered, and authentication not required."><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--252.png" alt="The Add page dialog with OpenAPI selected as the page type instead of Markdown."><figcaption></figcaption></figure>
5. Customize your page. The page contains default content that you can use to customize your new page with unique content. For more information about customizing your page with Gravitee Markdown, see [gravitee-markdown-components.md](gravitee-markdown-components.md "mention")

Open API example content:

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--253.png" alt="The Manage your navigation page, with an OpenAPI page selected in the navigation tree, its specification in the editor, and the rendered API reference on the right."><figcaption></figcaption></figure>

6. Publish the page by completing either of the following steps:

⚠️ A page can only be published if all of its ancestor folders are published or if it's a top level page.

*   Click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/138D78C1-526C-4741-89DF-C8F9BCF8137D_1_201_a.jpeg" alt="The Manage your navigation page with a new unpublished page selected and the Publish button highlighted."><figcaption></figcaption></figure>
*   Navigate to the page in the navigation bar, click the **ellipses** (<i class="fa-ellipsis-vertical">:ellipsis-vertical:</i>), and then click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/1A5E08E1-648C-4437-81C6-F4C480F04193_1_201_a.jpeg" alt="The navigation tree with a page&#x27;s context menu open and Publish highlighted above Edit and Delete."><figcaption></figcaption></figure>

1.  In the **Publish page** pop-up window, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/C52E694A-6761-45A5-B46B-998AE39FF5E1_1_201_a.jpeg" alt="The Publish page dialog, confirming that the page will become visible in the developer portal."><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Folders" %}
Folders group related pages together. A folder is a section on your New Developer Portal. When you add pages to your folder, they appear in the menu for that section instead of the top navigation.

**Add a folder**

1.  Click **Add**, and then click **Add Folder**.<br>

    <figure><img src="../../.gitbook/assets/B4C6D536-2F1D-453D-9269-F80B53854B3F_1_201_a.jpeg" alt="The Manage your navigation page with the Add menu open and Add Folder highlighted."><figcaption></figcaption></figure>
2. In the **Add folder** **pop-up** menu, type a title for the folder.
3. (Optional) Turn on the **Authentication is required to view this folder**. toggle. This ensures that the user has to sign in to the New Developer Portal to view the folder.
4.  Click **Add**.<br>

    <figure><img src="../../.gitbook/assets/46A3BA38-DD28-42B3-8BBC-BA5B2ABABBE2_1_201_a.jpeg" alt="The Add folder dialog, with a folder title entered and authentication not required."><figcaption></figcaption></figure>
5.  Publish the folder. To publish the folder, complete either of the following steps:

    ⚠️ A folder can be only published if all of its ancestor folders are published or if it's a top level folder.

    *   Click **Publish**.<br>

        <figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--89.png" alt="The Manage your navigation page with a new unpublished folder selected, showing empty editor and preview panels and the Publish button highlighted."><figcaption></figcaption></figure>
    *   Navigate to the folder in the navigation bar, click the **ellipses**, and then click **Publish**.<br>

        <figure><img src="../../.gitbook/assets/FAD5D2FB-4EEE-49B7-8081-F790D1AE0EC4_1_201_a.jpeg" alt="The navigation tree with a folder&#x27;s context menu open and Publish highlighted among the add, edit, and delete actions."><figcaption></figcaption></figure>
6.  In the **Publish folder**, pop-up box, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/0C92FAF4-F289-4D79-89D2-62448A9E8FE8_1_201_a.jpeg" alt="The Publish folder dialog, confirming that the folder and its content will become visible in the developer portal."><figcaption></figcaption></figure>

**Unpublishing cascade**

Unpublishing now works by cascade: all navigation items within a folder are unpublished with their parent.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--254.png" alt="The Unpublish folder dialog, warning that the folder and its nested documentation and APIs will be unpublished and that the action cannot be undone automatically."><figcaption></figcaption></figure>

**Add a page to a folder**

When you add a page to a folder, that page becomes a menu item within that section of the New Developer Portal.

1. Navigate to the the folder in the **Navigation items** menu.
2. Click **the ellipsis**.
3.  Click **Add page**.<br>

    <figure><img src="../../.gitbook/assets/E4576EEE-A99A-40AF-A637-9AC6F6C44D4A.jpeg" alt="The Manage your navigation page with the Add menu open and Add Page highlighted, above a tree containing a page, a folder, and a homepage entry."><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Links" %}
When you add a link, the link appears as a root level menu item. When you publish the link, the page appears in the top navigation bar of your New Developer Portal.

**Add a link**

1.  Click **Add**, and then click **Add Link**.<br>

    <figure><img src="../../.gitbook/assets/26E3BF6E-215F-43C8-850F-752A02323AEF_1_201_a.jpeg" alt="The Manage your navigation page with the Add menu open and Add Link highlighted."><figcaption></figcaption></figure>
2. In the **Add link** pop-up box, complete the following sub-steps:
   1. In the **Title** field, type a title for the link.
   2. In the **Link settings** field, enter the URL for the link.
   3. (Optional) Turn on the **Authentication is required to view this link**. toggle. This toggle ensures that the user has to sign in to the New Developer Portal to view the link.
3.  Click **Add**.<br>

    <figure><img src="../../.gitbook/assets/3476293A-507F-401E-855B-1CD3999E207E_1_201_a.jpeg" alt="The Add link dialog, with a link title and an external documentation URL entered and authentication not required."><figcaption></figcaption></figure>
4.  Publish the page. To publish the page, complete either of the following steps:

    ⚠️ A link can be only published if all of its ancestor folders are published or if it's a top level link.

    *   Click **Publish**.<br>

        <figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--90.png" alt="The Manage your navigation page with a new unpublished link selected and the Publish button highlighted."><figcaption></figcaption></figure>
    *   Navigate to link in the navigation bar, click the **ellipses**, and then click **Publish**.<br>

        <figure><img src="../../.gitbook/assets/D897DBD4-B160-4F29-ACD8-14E5D0959CF5_1_201_a.jpeg" alt="The navigation tree with a link&#x27;s context menu open and Publish highlighted."><figcaption></figcaption></figure>
5.  In the **Publish link** pop-up menu, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/B33EB73A-836D-4E7F-A297-53C23A7AB324_1_201_a.jpeg" alt="The Publish link dialog, confirming that the link will become visible in the developer portal."><figcaption></figcaption></figure>
{% endtab %}

{% tab title="API" %}
API navigation items represent actual APIs that exist in the platform.

{% hint style="info" %}
Adding APIs to the documentation is **the only way** to make them visible in the New Developer Portal.

Unlike in the Classic Portal, the property `published` of an API is not taken into account in the New Developer Portal.
{% endhint %}

API navigation items act similarly to folders meaning that they can contain other navigation items like Pages, Folders and Links.

However, there are some limitations of APIs compared to folders:

* APIs cannot contain other APIs and that on any level of the hierarchy, for example API -> Folder -> API chain is not allowed.
* APIs also cannot be at the top level of the navigation structure, they have to be inside a folder.

**Add an API**

1. Open the context menu of a folder in which you want to add your API by clicking the **ellipses**, and then click **Add API**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--255.png" alt="The Manage your navigation page with a folder&#x27;s context menu open, offering Add Page, Add API, Add Folder, Add Link, Edit, Publish, and Delete."><figcaption></figcaption></figure>

2. An **API selection dialog** opens up where you can select APIs to be added.
3. (Optional) Turn on the **Authentication is required to view selected APIs** toggle. This ensures that the user has to sign in to the New Developer Portal to view the APIs.
4. Click **Add**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--257.png" alt="The Add APIs dialog, listing five unpublished APIs with their path and labels, the first ticked, above an authentication toggle."><figcaption></figcaption></figure>

5. Publish the API. To publish the API, complete either of the following steps:

⚠️ An API can be only published if all of its ancestor folders are published.

* Click **Publish**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--245.png" alt="The Manage your navigation page with a newly added, unpublished API selected in the tree and empty editor and preview panels beside it."><figcaption></figcaption></figure>

* Navigate to the folder in the navigation bar, click the **ellipses**, and then click **Publish**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--246.png" alt="The Manage your navigation page with an API&#x27;s context menu open, offering Add Page, Add Folder, Add Link, Edit, Publish, and Delete."><figcaption></figcaption></figure>

6. In the **Publish API** pop-up box, click **Publish**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--247.png" alt="The Publish API dialog, confirming that the API and its content will be published and the change will be visible in the developer portal."><figcaption></figcaption></figure>

**Add a page to an API**

When you add a page to an API, that page becomes a menu item within that API in the New Developer Portal.

1. Navigate to the the folder in the **Navigation items** menu.
2. Click **the ellipsis**.
3. Click **Add page**.

**Add a folder to an API**

When you add a folder to an API, that folder becomes nested within that API in the New Developer Portal.

1. Navigate to the the folder in the **Navigation items** menu.
2. Click **the ellipsis**.
3. Click **Add folder**.
{% endtab %}
{% endtabs %}

## Verification

The content appears on the New Developer Portal. To view the content, complete the following step:

Click **Open website**.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--249.png" alt="The Manage your navigation page with a published Overview page selected, its Markdown template in the editor, and the rendered page on the right."><figcaption></figcaption></figure>

The new root-level items appear in the navigation bar.

<figure><img src="../../.gitbook/assets/devportal-new-portal-customize-the--250.png" alt="The developer portal Catalog in cards view, showing five API cards that each note their description is missing, with a top bar holding Guides, APIs, Docs, and custom links."><figcaption></figcaption></figure>
