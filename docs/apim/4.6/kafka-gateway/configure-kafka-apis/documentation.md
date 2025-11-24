---
description: An overview about documentation.
---

# Documentation

## Overview

In the **Documentation** section, you can click on the following headers to create pages that will appear in the Developer Portal and inform API consumers how to use your API:

* [Main Pages](documentation.md#main-pages)
* [Documentation Pages](documentation.md#documentation-pages)
* [Metadata](documentation.md#metadata)

## Main Pages

Under the **Main Pages** header, you can set up a homepage for your API in the Developer Portal. You can either create a new page or choose from existing pages.

To create a homepage:

1. Click **Create New Page**.
2.  Select the format of the page content. You can choose between Markdown, an OpenAPI definition, or an AsyncAPI definition. The next steps in the page creation process are identical regardless of which format you choose.

    <figure><img src="../../.gitbook/assets/1 docs 1.png" alt=""><figcaption></figcaption></figure>
3.  Choose whether to set your page visibility to **Public** or **Private**.

    <figure><img src="../../.gitbook/assets/01.png" alt=""><figcaption></figcaption></figure>

    If you select **Private**, you have the option to choose which groups can view your page. You can also exclude the selected groups, in which case the groups that are not selected will be able to view your page. If you do not select any groups, all groups will be able to view your page.

    <figure><img src="../../.gitbook/assets/10 1.png" alt=""><figcaption></figcaption></figure>
4.  Choose how to create the content. You can fill in the content yourself, import a file, or link to an external source.

    <figure><img src="../../.gitbook/assets/02.png" alt=""><figcaption></figcaption></figure>

    The format you chose for the page content may impact how you create page content:

    *   If you choose to fill in the content yourself, you'll need to write the content in Markdown, provide an OpenAPI definition, or provide an AsyncAPI definition.

        <figure><img src="../../.gitbook/assets/1 fill.png" alt=""><figcaption></figcaption></figure>
    *   If you choose to import content from a file in your local directory, you'll need to import a Markdown or text file if you chose the Markdown format, or import a JSON or YAML file if you chose either the OpenAPI or AsyncAPI format.

        <figure><img src="../../.gitbook/assets/1 import.png" alt=""><figcaption></figcaption></figure>
    *   If you choose to link to an external source, you'll be presented with the same set of options, regardless of format.

        <figure><img src="../../.gitbook/assets/1 link.png" alt=""><figcaption></figcaption></figure>
5.  After you've provided your page content, click **Save** to generate an unpublished page, or **Save and publish** to publish the page to the Developer Portal.

    <figure><img src="../../.gitbook/assets/04.png" alt=""><figcaption></figcaption></figure>

    Your page will appear with its name, publication status, and visibility, as well as the time it was last updated. Under ACTIONS, you can click the pencil icon to edit your page, the cloud to publish/unpublish it, and the trash can to delete it.

Instead of creating a new homepage, you can choose one from your existing documentation pages by clicking **Choose Existing Page**. You can select any page within your documentation page directory.

{% hint style="warning" %}
Once you select an existing page as your homepage, it will be removed from your documentation pages. This action is irreversible.
{% endhint %}

<figure><img src="../../.gitbook/assets/12.png" alt=""><figcaption></figcaption></figure>

## Documentation Pages

Click the **Documentation Pages** header to view a directory of the pages you've created to document your API. All published pages will appear in the Developer Portal.

The process for creating a documentation page is identical to that for creating a homepage, except a documentation page requires a name.

<figure><img src="../../.gitbook/assets/05.png" alt=""><figcaption></figcaption></figure>

In addition, **Documentation Pages** supports the creation of folders. To create a folder, click **Add new folder**.

<figure><img src="../../.gitbook/assets/09.png" alt=""><figcaption></figcaption></figure>

When prompted, give your folder a name and select either **Public** or **Private** visibility. A folder will be hidden, or not visible in the Developer Portal, until it contains published pages.

<figure><img src="../../.gitbook/assets/18.png" alt=""><figcaption></figcaption></figure>

**Documentation Pages** supports a nested structure. Once you've added a folder, you can click into it to create additional folders or pages.

{% hint style="info" %}
The ACTIONS of a documentation page include arrows. If more than one page or folder is present, you can use arrows to move the entry up or down in the directory structure.
{% endhint %}

## Metadata

Dynamic API documentation pages can be created by adding metadata. To view and filter metadata, select the **Metadata** header.

<figure><img src="../../.gitbook/assets/1 meta.png" alt=""><figcaption></figcaption></figure>

To create metadata for your documentation, click **+** **Add API Metadata**:

<div align="left"><figure><img src="broken-reference" alt="" width="375"><figcaption><p>Add API metadata</p></figcaption></figure></div>

Enter a name and value for the metadata, and select a metadata format from the drop-down menu. Available options are **string**, **numeric**, **boolean**, **date**, **mail**, or **url**.

You can edit existing metadata by clicking on the pencil icon. Changes to metadata values are reflected on the Developer Portal.
