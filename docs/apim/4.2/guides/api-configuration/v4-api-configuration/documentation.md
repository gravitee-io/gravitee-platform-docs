# Documentation

{% hint style="warning" %}
As of Gravitee 4.2, the APIM Documentation feature is only available for v4 APIs.
{% endhint %}

## Overview

Documentation can be added via the APIM Management Console to inform API consumers how to use an API. If the API and documentation are both published to the Developer Portal, the documentation will appear in the Portal for consumers to discover.

## Add documentation

To add documentation to an API:

1. Select **APIs** from the left sidebar of the Management Console
2. Select the API you want to document
3. Select **Documentation** from the inner left sidebar
4. Click on **Add new page** or **Add new folder** to start structuring your documentation content

<figure><img src="../../../../../../.gitbook/assets/documentation_nothing added (1).png" alt=""><figcaption><p>Add pages and/or folders to your API documentation</p></figcaption></figure>

### Add folders

Folders allow you to organize your documentation by grouping pages. To configure your first folder:

1. From the top-level **Home** directory, click **Add new folder**
2. Specify the following:
   * **Name:** This field is required
   * **Visibility:** Select whether the folder visibility is **Public** or **Private**
     * **Public:** This is the default visibility. The contents of the folder can be viewed in the Developer Portal by anonymous users.
     * **Private:** Users must be authenticated to view the contents of the folder in the Developer Portal

<figure><img src="../../../../../../.gitbook/assets/docs_add folder (1).png" alt=""><figcaption><p>Add a folder</p></figcaption></figure>

Once you click **Add folder**, the folder will appear at the top-level **Home** directory in **Documentation**. The directory will show the folder's status, visibility, the time the folder was last updated, and a badge indicating that the entry is a folder.

{% hint style="info" %}
A folder will be **Hidden**, or not visible in the Developer Portal, until it contains published pages.
{% endhint %}

<figure><img src="../../../../../../.gitbook/assets/docs_folder added (1).png" alt=""><figcaption><p>Add a folder to Home directory</p></figcaption></figure>

**Documentation** supports a nested structure. Once you've added a folder to the **Home** directory, you can click into it to create additional folders or pages.

### Add pages

Pages allow you to document your API using Markdown. The process of adding a page consists of the following steps:

#### Step 1: Configure a page

The first step is page configuration, which consists of naming the page and selecting whether the page is **Public** or **Private**:

* **Name:** This field is required
* **Visibility:** Select whether the folder visibility is **Public** or **Private**
  * **Public:** This is the default visibility. The page can be viewed in the Developer Portal by anonymous users.
  * **Private:** Users must be authenticated to view the page in the Developer Portal

<figure><img src="../../../../../../.gitbook/assets/docs_add page (1).png" alt=""><figcaption><p>Page configuration</p></figcaption></figure>

#### Step 2: Add content

Enter the page content in the Markdown text editor. **Toggle preview** enables a side-by-side view of the content you enter and the rendered page.

<figure><img src="../../../../../../.gitbook/assets/docs_page content (1).png" alt=""><figcaption><p>Add page content</p></figcaption></figure>

You have the option to save the page with or without publishing it to the Developer Portal. Once the content is saved, the page can be viewed from whichever directory it was added to. The directory will show the page's status, visibility, the time the page was last updated, and a badge indicating that the entry is a page.

<figure><img src="../../../../../../.gitbook/assets/docs_nested (1).png" alt=""><figcaption><p>Test page added to test folder</p></figcaption></figure>

## Editing

To edit or delete folders or pages, or to change the documentation structure, use the icons in the **Actions** section of an entry. All edits are immediately shown in the Developer Portal.

<figure><img src="../../../../../../.gitbook/assets/docs_editing (1).png" alt=""><figcaption><p>Select from Actions to edit</p></figcaption></figure>

**Edit folders:** To edit a folder's name or visibility, click on the pencil icon in the folder's entry, change the name and/or visibility, then click **Save**. The changes made to a folder's visibility will impact who can see it in the Developer Portal.

**Edit pages:** To edit an existing page, click on the pencil icon in the page's entry, and change the name, visibility, and/or content. If the page is already published, click **Publish changes**. If the page is not published, you will have the option to **Save** or **Save and publish** your changes.

**Delete:** To delete a page or folder, click the associated trash icon. Only empty folders can be deleted.

**Publish/unpublish:** To publish or unpublish a page, click the cloud icon.

**Reorder:** To change the order of pages and folders in a directory, use the up and down arrows.

## View documentation

API documentation is visible in the Developer Portal if both the API and documentation have been published. In order for a folder to be visible in the Portal, it must contain at least one published page. Otherwise, the folder will be tagged as **Hidden**.

To view the documentation in the Developer Portal:

1.  Click **Open API in Developer Portal**

    <figure><img src="../../../../../../.gitbook/assets/docs_open api (1).png" alt=""><figcaption><p>Open API in Developer Portal</p></figcaption></figure>
2.  Click on **Documentation** in the header options

    <figure><img src="../../../../../../.gitbook/assets/docs_dev portal docs (1).png" alt=""><figcaption><p>API documentation</p></figcaption></figure>
