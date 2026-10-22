---
hidden: false
noIndex: false
description: Write the pages, folders, and links of a Gamma API proxy on its Documentation page, then publish the API to the developer portal. Follow the steps to manage them.
---

# Manage API documentation

The **Documentation** page of an API proxy holds the pages, folders, and links that describe the API in the Developer Portal. They belong to the API. They appear under the API in every portal that lists it, and they stay with the API when you remove it from the portal. You write them on this page, and you publish the API when they're ready.

The New Developer Portal shows these items. The same items appear under the API's entry on the **Navigation** page of the Portal Settings, where a portal designer places the API in the portal. See [Manage Portal Navigation and APIs](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal/customize-the-navigation). When the API is also listed inside an API Product, its entry there doesn't show these items.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Under **General** in the API proxy sidebar, click **Documentation**.

    <figure><img src="../../.gitbook/assets/gamma-api-documentation-page.png" alt="The Documentation page of an API proxy, with a Published in APIs badge, the Unpublish and Add documentation buttons, and a tree of pages, a folder, and a link with their Status and Access badges."><figcaption><p>The Documentation page lists the pages, folders, and links of the API and shows where the API is published.</p></figcaption></figure>

The item doesn't appear when your role doesn't grant read access to the API's documentation. The page then reads **You don't have permission to view this API's documentation.** A TCP Proxy API has no **Documentation** item. A federated API keeps it.

Each item carries a **Status** badge that reads **Published** or **Unpublished**, and an **Access** badge that reads **Public** or **Private**. A **Private** item is shown to signed-in portal users only. A **Synced** badge marks an item whose content is fetched from an external source. The page's publication badge reads **Published in** followed by the section of the portal's top navigation that lists the API, or **Not published**. An entry that a portal designer added to the navigation but kept hidden counts as not published.

**Add documentation** appears when your role lets you create and update the API's documentation. The row menu offers the actions your role grants, and a right-click on a row opens the same menu.

The following table lists the API documentation permission that each action requires:

| Action | Permission |
|---|---|
| See the **Documentation** item and its pages | Read |
| **Add documentation** | Create and Update |
| **Create Overview page** | Create |
| Edit an item, **Configure**, **Fetch now**, publish or unpublish an item, **Publish** and **Unpublish** the API | Update |
| Delete an item | Delete |

## Add a page

To add a page, follow these steps:

1. Click **Add documentation**, and then click **Page**. To add the page inside a folder, open the folder's row menu and click **Add page** instead.

    <figure><img src="../../.gitbook/assets/gamma-api-documentation-add-page.png" alt="The Add a page dialog, with a title entered, the access switch off, Fill in content selected under Content, and Gravitee Markdown selected under Page type."><figcaption><p>The Add a page dialog takes a title, the access, the content source, and the page type.</p></figcaption></figure>
2. Enter a **Title**.
3. To show the page to signed-in users only, under **Access**, turn on **Authentication is required to view this page**. Inside a private folder, the switch is locked on, and the dialog says why.
4. Under **Content**, choose one of the following content sources:
    * **Fill in content**. You write the page in the editor.
    * **Import from file**. Choose a `.md`, `.yaml`, `.yml`, or `.json` file of up to 10 MB. A `.md` file is imported as Gravitee Markdown. A YAML or JSON file is imported as OpenAPI when its root has an `openapi` or `swagger` property, and as AsyncAPI when its root has an `asyncapi` property. A file with neither is refused. The file name becomes the title until you change it.
    * **Link to external source**. The content is fetched from a repository or a URL, and it stays read-only in the console. See [Fetch content from an external source](#fetch-content-from-an-external-source).
5. Under **Page type**, choose **Gravitee Markdown**, **OpenAPI**, or **AsyncAPI**. The choice isn't offered for an imported file, whose type is detected.
6. Click **Create**.

The page is created unpublished and opens in the editor.

## Edit a page

Click the title of a page to open it. The editor shows the content alongside a preview, and the preview follows what you type. An OpenAPI page previews in the viewer it's configured for: Redoc by default, or Swagger UI. Click **Save changes** to save the content. If you close or reload the browser tab with unsaved changes, you're asked to confirm first. If you move to another page of the console, you aren't.

<figure><img src="../../.gitbook/assets/gamma-api-documentation-editor.png" alt="The editor of a Gravitee Markdown page, with the page title, its Published and Public badges, the Edit details and Save changes buttons, the Markdown on the left, and the rendered preview on the right."><figcaption><p>The editor shows the content and its preview side by side.</p></figcaption></figure>

Click **Edit details** to change the title or the access. A page synced from an external source keeps its title while it keeps the source, and a page inside a synced folder can't be edited at all.

### Configure the OpenAPI viewer

To choose how the portal renders an OpenAPI page, follow these steps:

1. On the OpenAPI page, click **Configure**.
2. Under **OpenAPI Documentation Viewer**, choose **SwaggerUI** or **Redoc**.
3. Set a **Base URL** that starts with `http://` or `https://`, or leave it empty.
4. With **SwaggerUI**, turn on the options you need, such as **Use API entrypoints as server URLs** or **Enable "Try It!" mode**.
5. Click **Save**.

The configuration is saved on its own, apart from the content, and the preview follows it. For what each option does, see [Creating OpenAPI Documentation Pages](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal/customize-the-navigation/creating-openapi-documentation-pages). **Configure** isn't offered on a page inside a synced folder.

## Add a folder

To add a folder, follow these steps:

1. Click **Add documentation**, and then click **Folder**. To nest it, open the parent folder's row menu and click **Add folder** instead.
2. Under **Contents**, keep **Empty folder**, or choose **Import from a repository** to fill the folder with pages fetched from a folder of a repository. The pages stay read-only. A `.gravitee.json` manifest in the repository decides the hierarchy, and without one the folder tree is mirrored. Only source types that can list a folder are offered.
3. Enter a **Title**. To show the folder to signed-in users only, turn on **Authentication is required to view this folder**.
4. Click **Create**, or **Import** for a repository import.

The folder is created unpublished. To change its title or access, click **Edit details** in its row menu. When you make a folder private, every item inside it becomes private too, and an item inside a private folder can't be made public.

## Add a link

To add a link, follow these steps:

1. Click **Add documentation**, and then click **Link**.
2. Enter a **Title** and the **URL**. The URL has to be a valid address, such as `https://status.example.com`.
3. Choose the access.
4. Click **Create**.

A link has no content to open, so clicking its title in the list opens its details instead.

## Fetch content from an external source

A page or a folder linked to an external source takes its content from a repository or a URL. The source types are the fetcher plugins installed with the Management API, and APIM bundles the GitHub, GitLab, Git, Bitbucket, and HTTP fetchers. Only the ones that can list a folder are offered for a folder import.

When you link a source, choose a **Source type**, enter its settings, and turn on **Fetch automatically** to fetch the content on a schedule. **Schedule (cron)** takes a six-field cron expression, and **Quick select** offers presets from **Every 5 minutes** to **Every day at midnight**. **Edit as JSON** shows the settings as JSON instead of a form. The content is fetched when the page is created. When that first fetch fails, the page is still created, and its editor shows the error.

A synced page is read-only. In its editor, a bar names the source type, says when the content was last fetched, and shows the schedule. Click **Fetch now** to fetch the content again. The row menu offers **Fetch now** on a synced page, on an imported folder, and on a folder that holds synced pages.

To change the source of a page, follow these steps:

1. Click **Edit details**.
2. Change the source settings or the schedule.
3. Click **Save**. The content is fetched again. A saved secret, such as a token, is kept unless you enter a new one. When you change the address, the saved secrets are cleared.

To write the page by hand again, turn off **Fetch this page from an external source**, and then click **Save**. The source is removed, and the page keeps its current content. A folder imported from a repository changes or removes its source the same way, with **Fetch this folder from an external source**.

The pages inside an imported folder can't be edited or deleted one by one. The folder manages them, and when you delete the folder, they're deleted with it.

## Publish the API to the Developer Portal

Until the API is published, its documentation stays out of the portal, and no item can be published on its own. To publish the API, follow these steps:

1. Click **Publish**.
2. If the API has no page yet, the dialog reads **Add a page before publishing**, because an API needs at least one page to be shown in the Developer Portal. Click **Create Overview page** to create an unpublished **Overview** page from the API overview template. The page opens in the editor, which shows the template's placeholders, such as `${api.name}`, as written. The Developer Portal replaces them with the API's details each time it displays the page. Review the page, return to the **Documentation** page, and click **Publish** again. Folders and links don't count as a page. Without permission to create documentation, the dialog says to ask someone who can add documentation to this API.
3. In the **Publish to the developer portal** dialog, select the **Section** of the portal's top navigation to list the API in. The list holds the published top-level folders of the portal's main navigation. The dialog preselects the section where a hidden entry of the API already sits, otherwise the section named **APIs**, and otherwise the first one. Every environment has an **APIs** section by default, which the dialog offers unless it was renamed, unpublished, or deleted. When no section is available, the field reads **No sections available**, and the dialog says to ask a portal administrator to add one.

    <figure><img src="../../.gitbook/assets/gamma-api-documentation-publish-dialog.png" alt="The Publish to the developer portal dialog, with the Section field set to APIs and the Publish button."><figcaption><p>The Publish to the developer portal dialog lists the API in the section you choose.</p></figcaption></figure>
4. Click **Publish**.

The API appears in the section, and every page, folder, and link is published, including the ones that were unpublished one by one. If a portal designer already added the API to the navigation and kept it hidden, the publish action reuses that entry and moves it to the section you chose. The badge then reads **Published in** and the section, and the button reads **Unpublish**.

### Unpublish the API

To remove the API from the portal, follow these steps:

1. Click **Unpublish**.
2. In the confirmation, click **Unpublish**.

The API and its documentation become invisible in the Developer Portal. Nothing is deleted. The entry stays in the navigation, hidden, and when you publish the API again, it and its documentation are shown.

## Show or hide one item

Once the API is published, you can publish or unpublish each item on its own. To show or hide one item, follow these steps:

1. Open the item's row menu.
2. Click **Publish** or **Unpublish**.
3. Confirm.

The following rules apply to publishing and unpublishing one item:

* When you unpublish a folder, the items inside it are hidden too.
* When you publish a folder, the dialog offers to publish the items inside it too. The checkbox is selected by default, and if you clear it, only the folder is published.
* An item inside an unpublished folder can't be published, and the menu says so.
* When you publish the API again, every item is published, including the ones you hid one by one.

## Delete an item

To delete an item, follow these steps:

1. Open the item's row menu, and then click **Delete**.
2. In the confirmation, click **Delete**. A folder is deleted with everything inside it, and the dialog gives the count.

The item disappears from every portal that lists the API. An item inside an imported folder can't be deleted on its own. When you delete the API, its documentation is deleted with it.

## Verification

To verify the documentation is in the Developer Portal, follow these steps:

1. Open the Developer Portal, and in its top navigation, click the section you published the API in, such as **APIs**.
2. Click the API. Its published pages, folders, and links are listed, and a **Private** item appears only after you sign in.

    <figure><img src="../../.gitbook/assets/gamma-api-documentation-portal.png" alt="The developer portal showing the Orders API under the APIs section, with its Guides folder, Orders API reference, Changelog, and Status page in the navigation tree."><figcaption><p>The Developer Portal lists the API and its documentation.</p></figcaption></figure>

## Next steps

* [Manage Portal Navigation and APIs](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal/customize-the-navigation). Place the API in the portal navigation and manage the same documentation from the Portal Settings.
* [Import content from external sources](https://documentation.gravitee.io/apim/developer-portal/new-developer-portal/customize-the-navigation/import-content-from-external-sources). Look up the settings of each source type.
