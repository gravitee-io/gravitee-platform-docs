# Customize the APIM Portal navigation

3.20.0

### Overview <a href="#overview" id="overview"></a>

You can use the system folders to customize the APIM Portal navigation. You can customize:

* the APIM Portal menu in the header and footer
* the API side menu

#### Links <a href="#links" id="links"></a>

You customize the navigation by create link pages in the folders. There are 3 kinds of link:

* External link
* Link to an existing documentation page
* Link to a category

#### Access system folders <a href="#access_system_folders" id="access_system_folders"></a>

To access system folders:

* for the APIM Portal, click **Settings > Documentation**
* for an APIM menu, click **APIs** and select the API, then click **Pages**

System folders are listed with a padlock icon:



### Manage links <a href="#manage_links" id="manage_links"></a>

To create a link, go to a system folder and click the plus icon .

#### External link <a href="#external_link" id="external_link"></a>

Enter a name and a URL (relative or absolute):

#### Documentation link <a href="#documentation_link" id="documentation_link"></a>

Select an existing page in the documentation:

A documentation link is published only if the target documentation page is published.

#### Category link <a href="#category_link" id="category_link"></a>

Select an existing category in the documentation:

|   | Both documentation and category links inherit the name and translation of their target. You can override these values by toggling off the **Inherit** switches: |
| - | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |

|   | You can create links from documentation by clicking the following icon: |
| - | ----------------------------------------------------------------------- |

### System folders <a href="#system_folders" id="system_folders"></a>

APIM Portal documentation has 3 system folders: `Header`, `TopFooter` and `Footer`.\
API documentation has 1 system folder: `Aside`.

Each system folder corresponds to an area of APIM Portal:

|   | <p>The APIM Portal <code>TopFooter</code> is the only system folder in which you can create standard folders.<br>These folders are used to group links together.</p><table data-header-hidden><thead><tr><th></th><th></th></tr></thead><tbody><tr><td></td><td>For this system folder, only links to folders will be displayed.</td></tr></tbody></table> |
| - | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   | For this system folder, only links to folders will be displayed.                                                                                                                                                                                                                                                                                           |
