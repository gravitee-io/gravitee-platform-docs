# publish-documentation

\= Publish documentation :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_publisherguide\_publish\_documentation.html :page-folder: apim/user-guide/publisher :page-layout: apim3x

\== Overview

APIM includes a feature for publishing documentation in APIM Portal. You can publish documentation for the whole portal and for individual APIs.

The APIM Portal documentation creates a direct line of communication with your developer community through a single channel. For example, you can use it to communicate your best practices or even to configure your own homepage.

_Documentation is the key to a successful API._ It is the best way to promote your web services and give developers all the information they need to consume them successfully.

\=== System folders

You can use system folders to customize the APIM Portal menu header, footer and navigation by adding custom links. For more information, see link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_system\_folders.html' | relative\_url \}}\[Customize the APIM Portal navigation^].

\=== Documentation set To add some documentation, you can either create new pages or import them from a file or external source.

APIM supports multiple types of documentation:

* Markdown (for more information, see link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_markdown.html' | relative\_url \}}\[Markdown documentation] and link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_markdown\_template.html' | relative\_url \}}\[Markdown templates])
* AsciiDoc (for more information, see link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_asciidoc.html' | relative\_url \}}\[AsciiDoc documentation])
* OpenAPI (Swagger) (for more information, see link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_openapi.html' | relative\_url \}}\[OpenAPI documentation])

You can create folders to organize your documentation.

\=== External documentation

You can fetch your documentation from external sources.

APIM includes 5 types of fetchers:

* GitHub: fetch your documentation from a GitHub repository
* GitLab: fetch your documentation from a GitLab repository
* Git: fetch your documentation from a Git repository
* WWW: fetch your documentation from the web
* Bitbucket: fetch your documentation from a Bitbucket repository

The documentation is fetched and stored locally in APIM when you first create it, and at regular intervals if you configure auto-fetch.

image::

\[]

\=== Manage documentation pages and folders

To create new pages and folders in APIM Console:

* for an API, click _APIs_ and select the API, then click _Pages_
* for the whole APIM Portal, click _Settings > Documentation_

\== Create a new folder

. Click the plus icon image:

\[role="icon"] and select the folder icon. + image:\[]

. Specify your folder name and click _SAVE_. + APIM adds your folder to a list, where you can select it and:

* add different language versions of the folder name by clicking _TRANSLATE FOLDER_
* start creating documentation pages in your folder by clicking the plus icon image:\[role="icon"] and following the steps below

\== Create a new page

. Click the plus icon image:

\[role="icon"] and choose the documentation type. + image::\[]

. (Optional) Set the page as your API Portal home page by selecting the _Set as homepage_ option. . Choose whether to import the documentation or create it directly in the editor. If importing, specify the file details or the external documentation source. . If you are creating a Markdown page and want to use an existing template, select the template. . If the page is ready to publish, select _Publish this page_. The page will not be visible until this option is selected. You can also publish it later from the documentation list. . Click _SAVE_.

NOTE: For Markdown pages, you can link:\{{ '/apim/3.x/apim\_publisherguide\_publish\_documentation\_markdown\_template.html' | relative\_url \}}\[create and use templates].

\== Import multiple pages

If you have an existing documentation set for your API in a GitHub or GitLab repository, you can configure the GitHub or GitLab fetcher to import the complete documentation structure on a one-off or regular basis. You can import the documentation into APIM in a different structure from the source repository structure.

In order for the fetcher to locate the documentation in your repository structure and create the documentation structure you need in APIM, you first create a JSON file in the repository describing both the source and destination structure. You can then configure a fetcher in APIM to read the JSON file and import the documentation according to the structure defined in the file.

\=== Example JSON file

The following example JSON file describes a documentation set which includes:

* a home page in Markdown format in a folder called `/newdoc`, to be placed at the root of the APIM documentation structure.
* a JSON file containing a Swagger specification at the root of the repository, to be placed in a folder called `/technical` in the APIM documentation structure.

### \[source,json]

### { "version": 1, "documentation": { "pages": \[ { "src": "/newdoc/readme.md", "dest": "/", "name": "Homepage", "homepage": true }, { "src": "/test-import-swagger.json", "dest": "/technical", "name": "Swagger" } ] } }

\=== Configure a fetcher

. Click _Import multiple files_. . If you want to publish the pages on import, select _Publish all imported pages_. + image:

\[] . Click the GitHub or GitLab fetcher. . Specify the details of the external source, such as the URL of the external API, name of the repository and the branch. The fields vary slightly depending on the fetcher. + image:\[] . In _Filepath_, enter the path to your JSON documentation specification file. . Enter an access token, which you need to generate in your GitHub or GitLab user profile. . Select _Auto Fetch_ and specify the `crontab` update frequency, if you want the pages to be updated dynamically. . Click _IMPORT_. + APIM adds the files to your documentation set. + image:\[]

\=== Publish your page

Once your page is created, you can view it before publishing it. APIM displays the following message:

image::

\[]

You can publish a page in one of the following ways:

* Check the _Publish this page_ option in the _CONFIGURATION_ tab:
*

image::

\[] + When you publish the page in this way, you can enable the option _Allow access to anonymous user_ to display the page to users browsing APIM Portal without logging in. The option is checked by default.

* Click the cloud icon in the documentation list:

image::

\[]

\== Configure a page

You can select a page from the list and configure it using the tabs, as described in the sections below.

\=== Translate a page

You can add translations for your pages. In the _TRANSLATIONS_ tab:

. Click _ADD A TRANSLATION_. . Enter your 2 character language code (FR for french, CZ for czech, IT for italian and so on). . Enter the translated title. . (Optional) You can edit the content to add translated content by toggling on the switch. . Click _SAVE TRANSLATION_ at the bottom of the page.

image::

\[]

image::

\[]

\=== Auto fetch from an external source

To periodically fetch your documentation from external sources, you can enable the auto-fetch option and specify the fetch frequency. In the _EXTERNAL SOURCE_ tab:

. Select the external source type. . Enter the source details, such as URL, username and so on. . Specify the _Update frequency_ as a `cron` expression. This is a string consisting of six fields that describe the schedule (representing seconds, minutes, hours, days, months and weekdays). + For example:

* Fetch every second: `* * */1 * * *`
* At 00:00 on Saturday : `0 0 0 * * SAT`

NOTE: If the APIM administrator configured a maximum fetch frequency, the value configured by the APIM administrator will override the frequency you specify.

\=== Access control

In the _ACCESS CONTROL_ tab, you can mark a page as PRIVATE if you want to deny access to anonymous user.

For private pages, you can configure access lists by required or to be excluded roles/groups.

image::

\[]

\== Templating

This example shows how to create documentation templates based on the Apache https://freemarker.apache.org\[FreeMarker template engine, window="\_blank"].

\=== Syntax

You can access your API data in your API documentation with the following format: `${api.name} or ${api.metadata['foo-bar']}`

\== Available API properties

\[width="100%",cols="20%,10%,70%",options="header"] |====================== |Field name |Field type |Example |id |String |70e72a24-59ac-4bad-a72a-2459acbbad39 |name |String |My first API |description |String |My first API |version |String |1 |metadata |Map |{"email-support": "support.contact@company.com"} |createdAt |Date |12 juil. 2018 14:44:00 |updatedAt |Date |12 juil. 2018 14:46:00 |deployedAt |Date |12 juil. 2018 14:49:00 |picture |String |data:image/png;base64,iVBO... |state |String |STARTED/STOPPED |visibility |String |PUBLIC/PRIVATE |tags |Array |\["internal", "sales"] |proxy.contextPath |String |/stores |primaryOwner.displayName |String |Firstname Lastname |primaryOwner.email |String |firstname.lastname@company.com |======================

\== Example

The following example shows an API documentation template.

### \[source,markdown]

<#if api.picture??> ![]($%7Bapi.picture%7D) \</#if>

## Welcome to the API ${api.name}(${api.version})!

The API is ${api.state}.

This API has been created on ${api.createdAt?datetime} and updated on ${api.updatedAt?datetime}.

<#if api.deployedAt??> This API has been deployed on ${api.deployedAt?datetime}. <#else> This API has not yet been deployed. \</#if>

<#if api.visibility=='PUBLIC'> This API is publicly exposed. <#else> This API is not publicly exposed. \</#if>

<#if api.tags?has\_content> Sharding tags: ${api.tags?join(", ")} \</#if>

### Description

${api.description}

### How to access

The API can be accessed through https://api.company.com${api.proxy.contextPath}:

curl https://api.company.com${api.proxy.contextPath}

### Rating

You can rate and put a comment for this API [here](../../../../../#!/apis/${api.id}/ratings).

### Contact

The support contact is [${api.metadata\['email-support'\]}](mailto:${api.metadata\['email-support']}).

### The API owner is <#if api.primaryOwner.email??>[${api.primaryOwner.displayName}](mailto:${api.primaryOwner.email})<#else>${api.primaryOwner.displayName}\</#if>.

Let's see the result in APIM Portal:

image::

\[]
