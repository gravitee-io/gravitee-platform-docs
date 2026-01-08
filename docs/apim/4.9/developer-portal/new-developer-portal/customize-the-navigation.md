# Customize the navigation

## Overview&#x20;

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

In the New Developer Portal, you can customize the navigation of your Developer Portal by using the **Navigation items** section of the New Developer Portal settings.

You can create the following elements for your navigation:

* **Pages**: Content of your New Developer Portal documentation.&#x20;
* **Folders**: Use these to group related pages together into sections.
* **Links**: Connect your documentation to external sites or other internal resources.

When you add a new page, you can customize the page with Gravitee Markdown, which is standard Markdown enriched with dynamic components. For more information about Gravitee Markdown, see[gravitee-markdown-components.md](gravitee-markdown-components.md "mention").

### Default navigation items

By default some pages already created for you with content. These pages are published and public by default. Here are the following folders pages, and links that are created by default:

* A folder named Guides, which contains a Getting Started page.
* A folder Core concepts, which contains a page that describes making your first API call and a page that describes authentication.
* A link to Docs that brings you to the Gravitee documentation.

#### Console view

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.05.51.png" alt=""><figcaption></figcaption></figure>

#### Developer portal view

The default navigation appears on your New Developer Portal

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.06.57.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-19 at 19.07.11.png" alt=""><figcaption></figcaption></figure>

## Prerequisites&#x20;

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Customizing your navigation

With the New Developer Portal, you can customize your navigation in the following ways:

* [#add-a-page](customize-the-navigation.md#add-a-page "mention")
* [#add-a-folder](customize-the-navigation.md#add-a-folder "mention")
* [#add-a-link](customize-the-navigation.md#add-a-link "mention")

1.  From the **Dashboard**, click **Settings**.<br>

    <figure><img src="../../.gitbook/assets/EB3744C8-A282-4EC2-9DB6-218361CB3FA7_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  From the **Settings** menu, click **Settings**. <br>

    <figure><img src="../../.gitbook/assets/CF7527D1-5E90-4637-8C70-FF5125AEB0BF_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  Navigate to the **New Developer Portal** section, and then click **Open Settings**. The New Developer Portal settings open on the navigation tab.<br>

    <figure><img src="../../.gitbook/assets/7C64309D-426F-4F5D-B48D-2224931FC9F3_4_5005_c.jpeg" alt=""><figcaption></figcaption></figure>
4. Customize your navigation using the following components:

{% tabs %}
{% tab title="Pages" %}
When you add a page that is not in a folder, the page appears as a root level menu item. When you publish the page, the page appears in the top navigation bar of your New Developer Portal.

### Add a page&#x20;

1.  Click **Add**, and then click **Add Page**. <br>

    <figure><img src="../../.gitbook/assets/FB8F0725-08EB-4B68-B365-122337D12C4F_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2. In the **Add page** pop-up screen, type a title for your page.
3. (Optional) Turn on the **Authentication is required to view this page.** toggle. This toggle ensures that the user must be signed in to the New Developer Portal to see the page.&#x20;
4.  Click **Add**.<br>

    <figure><img src="../../.gitbook/assets/A492BF45-07AE-4443-91F6-DF15C255160E_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
5. Customize your page. The page contains default content that you can use to customize your new page with unique content. For more information about customizing your page with Gravitee Markdown, see [gravitee-markdown-components.md](gravitee-markdown-components.md "mention")
6. Publish the page by completing either of the following steps:
   *   Click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/138D78C1-526C-4741-89DF-C8F9BCF8137D_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>


   *   Navigate to the page in the navigation bar, click the **ellipses** (<i class="fa-ellipsis-vertical">:ellipsis-vertical:</i>), and then click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/1A5E08E1-648C-4437-81C6-F4C480F04193_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
7.  In the **Publish page** pop-up window, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/C52E694A-6761-45A5-B46B-998AE39FF5E1_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>


{% endtab %}

{% tab title="Folders" %}
Folders group related pages together. A folder is a section on your New Developer Portal. When you add pages to your folder, they appear in the menu for that section instead of the top navigation.&#x20;

### Add a folder

1.  Click **Add**, and then click **Add Folder**. <br>

    <figure><img src="../../.gitbook/assets/B4C6D536-2F1D-453D-9269-F80B53854B3F_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2. In the **Add folder** **pop-up** menu, type a title for the folder.&#x20;
3. (Optional) Turn on the **Authentication is required to view this folder**. toggle. This ensures that the user has to sign in to the New Developer Portal to view the folder.&#x20;
4.  Click **Add**.<br>

    <figure><img src="../../.gitbook/assets/46A3BA38-DD28-42B3-8BBC-BA5B2ABABBE2_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5. Publish the folder. To publish the folder, complete either of the following steps:
   *   Click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>
   *   Navigate to the folder in the navigation bar, click the **ellipses**, and then click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/FAD5D2FB-4EEE-49B7-8081-F790D1AE0EC4_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
6.  In the **Publish folder**, pop-up box, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/0C92FAF4-F289-4D79-89D2-62448A9E8FE8_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

### Add a page to a folder

When you add a page to a folder, that page becomes a menu item within that section of the New Developer Portal.&#x20;

1. Navigate to the the folder in the **Navigation items** menu.&#x20;
2. Click **the ellipsis**.&#x20;
3.  Click **Add page**. <br>

    <figure><img src="../../.gitbook/assets/E4576EEE-A99A-40AF-A637-9AC6F6C44D4A.jpeg" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Links" %}
When you add a link, the link appears as a root level menu item. When you publish the link, the page appears in the top navigation bar of your New Developer Portal.

### Add a link

1.  Click **Add**, and then click **Add Link**.<br>

    <figure><img src="../../.gitbook/assets/26E3BF6E-215F-43C8-850F-752A02323AEF_1_201_a (2).jpeg" alt=""><figcaption></figcaption></figure>
2. In the **Add link** pop-up box, complete the following sub-steps:
   1. In the **Title** field, type a title for the link.
   2. In the **Link settings** field, enter the URL for the link.
   3. (Optional) Turn on the **Authentication is required to view this link**. toggle. This toggle ensures that the user has to sign in to the New Developer Portal to view the link.
3.  Click **Add**.<br>

    <figure><img src="../../.gitbook/assets/3476293A-507F-401E-855B-1CD3999E207E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4. Publish the page. To publish the page, complete either of the following steps:
   *   Click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/image (80).png" alt=""><figcaption></figcaption></figure>
   *   Navigate to link in the navigation bar, click the **ellipses**, and then click **Publish**.<br>

       <figure><img src="../../.gitbook/assets/D897DBD4-B160-4F29-ACD8-14E5D0959CF5_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
5.  In the **Publish link** pop-up menu, click **Publish**.<br>

    <figure><img src="../../.gitbook/assets/B33EB73A-836D-4E7F-A297-53C23A7AB324_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

## Verification&#x20;

The content appears on the New Developer Portal. To view the content, complete the following step:

*   Click **Open website**. <br>

    <figure><img src="../../.gitbook/assets/120FA470-17E8-4D1A-AFB2-2D620EAFA8C2 (2).jpeg" alt=""><figcaption></figcaption></figure>

The new root-level items appear in the navigation bar.

<figure><img src="../../.gitbook/assets/DE69377A-0A4D-4A3A-9A79-82F608F2526A.jpeg" alt=""><figcaption></figcaption></figure>
