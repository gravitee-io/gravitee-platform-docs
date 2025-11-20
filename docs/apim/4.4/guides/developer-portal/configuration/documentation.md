# Documentation

## Overview

Site-wide documentation creates a direct line of communication with your developer community. Administrators can use site-wide documentation to communicate best practices, configure pages, or as a reference via [custom navigation](layout-and-theme-customization.md#custom-navigation). Published documentation is accessible from the Developer Portal's **Documentation** page:

{% hint style="info" %}
Site-wide documentation is separate from API documentation, which can be added to an API by an API publisher.
{% endhint %}

<figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-05 at 10.24.20 AM (1).png" alt=""><figcaption><p>Developer Portal documentation page</p></figcaption></figure>

The following sections discuss how to:

* [Create documentation](documentation.md#create-documentation)
* [Generate content](documentation.md#generate-content)
* [Import multiple pages](documentation.md#import-multiple-pages)
* [Page management](documentation.md#page-management)

## Create documentation

To create documentation:

1. Select **Settings** from the left sidebar of the Management Console
2.  Select **Documentation** from the inner left sidebar

    <figure><img src="../../../../../../.gitbook/assets/documentation_settings (1).png" alt=""><figcaption><p>Documentation settings page</p></figcaption></figure>
3.  Select the **+** icon on the bottom right to display the options below.

    <figure><img src="../../../../../../.gitbook/assets/documentation_options (1).png" alt=""><figcaption><p>Create new documentation options</p></figcaption></figure>

*   **Folder:** Generate a folder to organize your documentation. Optionally generate [translations](documentation.md#translations) of the folder by selecting **Translate Folder**.

    <figure><img src="../../../../../../.gitbook/assets/documenation_folder (1).png" alt=""><figcaption><p>Sample documentation folder</p></figcaption></figure>
* **Markdown Template:** Create templates reusable for site-wide and API Markdown documentation.
* **Markdown:** Use the Markdown syntax for the documentation page.
* **AsciiDoc:** Use the Asciidoc syntax for the documentation page.
* **OpenAPI (Swagger):** Use the OpenAPI syntax for the documentation page.
* **AsyncAPI:** Use the AsyncAPI syntax for the documentation page.

Each documentation type provides similar configuration options and a compatible text editor.

<figure><img src="../../../../../../.gitbook/assets/new_docs_page (1).png" alt=""><figcaption><p>Create a documentation page</p></figcaption></figure>

* **Name:** Provide a title for your documentation page.
*   **Set as homepage:** Use the documentation page as the homepage of the Developer Portal. If multiple documentation pages are set as the homepage, the page most recently set will be selected.

    <figure><img src="../../../../../../.gitbook/assets/documentation_homepage (1).png" alt=""><figcaption><p>Custom homepage example</p></figcaption></figure>
* **Publish this page:** Make the page available in the Developer Portal.
* **Make private:** Make the page private to you and the users you explicitly allow using [access control](documentation.md#access-control).

## Generate content

APIM provides three methods for generating documentation content:

* [Fill the content inline (supports templating with API properties)](documentation.md#fill-content-inline)
* [Import from file](documentation.md#import-from-file)
* [External source (Gitlab, Bitbucket, etc.)](documentation.md#external-source)

{% tabs %}
{% tab title="Fill content inline" %}
This method uses the text editor to generate content based on your selected documentation type. In addition, APIM supports templating with API properties.

**Templating with API properties**

Use the following syntax to access the API data in your API documentation: `${api.name} or ${api.metadata['foo-bar']}`.

The sample script below creates a documentation template based on the Apache [FreeMarker template engine](https://freemarker.apache.org/):

{% code overflow="wrap" fullWidth="false" %}
```ftl
<#if api.picture??>
<img src="${api.picture}" style="float: right;max-width: 60px;"/>
</#if>

# Welcome to the API ${api.name}(${api.version})!

The API is <span style="text-transform: lowercase;color: <#if api.state=='STARTED'>green<#else>red</#if>">${api.state}</span>.

This API has been created on ${api.createdAt?datetime} and updated on ${api.updatedAt?datetime}.

<#if api.deployedAt??>
This API has been deployed on ${api.deployedAt?datetime}.
<#else>
This API has not yet been deployed.
</#if>

<#if api.visibility=='PUBLIC'>
This API is publicly exposed.
<#else>
This API is not publicly exposed.
</#if>

<#if api.tags?has_content>
Sharding tags: ${api.tags?join(", ")}
</#if>

## Description

${api.description}

<#if api.proxy??>
## How to access

The API can be accessed through https://api.company.com${api.proxy.contextPath}:

curl https://api.company.com${api.proxy.contextPath}
</#if>

## Rating

You can rate and put a comment for this API <a href='/#!/apis/${api.id}/ratings'>here</a>.

## Contact

<#if api.metadata['email-support']??>
The support contact is <a href="mailto:${api.metadata['email-support']}">${api.metadata['email-support']}</a>.
</#if>

The API owner is <#if api.primaryOwner.email??><a href="mailto:${api.primaryOwner.email}">${api.primaryOwner.displayName}</a><#else>${api.primaryOwner.displayName}</#if>.
```
{% endcode %}

The above sample script creates the following in the Developer Portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-template.png" alt=""><figcaption><p>Result of templating engine example</p></figcaption></figure>

**API properties reference**

The following reference table shows all available API properties. Access these properties in the Freemarker template with `${api.<Field name>}` as in the above sample script.

<table data-full-width="false"><thead><tr><th width="155">Field name</th><th width="124">Field type</th><th>Example</th></tr></thead><tbody><tr><td>id</td><td>String</td><td>70e72a24-59ac-4bad-a72a-2459acbbad39</td></tr><tr><td>name</td><td>String</td><td>My first API</td></tr><tr><td>description</td><td>String</td><td>My first API</td></tr><tr><td>version</td><td>String</td><td>1</td></tr><tr><td>metadata</td><td>Map</td><td>{"email-support": "<a href="mailto:support.contact@company.com">support.contact@company.com</a>"}</td></tr><tr><td>createdAt</td><td>Date</td><td>12 juil. 2018 14:44:00</td></tr><tr><td>updatedAt</td><td>Date</td><td>12 juil. 2018 14:46:00</td></tr><tr><td>deployedAt</td><td>Date</td><td>12 juil. 2018 14:49:00</td></tr><tr><td>picture</td><td>String</td><td>data:image/png;base64,iVBO…​</td></tr><tr><td>state</td><td>String</td><td>STARTED/STOPPED</td></tr><tr><td>visibility</td><td>String</td><td>PUBLIC/PRIVATE</td></tr><tr><td>tags</td><td>Array</td><td>["internal", "sales"]</td></tr><tr><td>proxy.contextPath</td><td>String</td><td>/stores</td></tr><tr><td>primaryOwner.displayName</td><td>String</td><td>Firstname Lastname</td></tr><tr><td>primaryOwner.email</td><td>String</td><td><a href="mailto:firstname.lastname@company.com">firstname.lastname@company.com</a></td></tr></tbody></table>
{% endtab %}

{% tab title="Import from file" %}
This method allows you to generate content by importing a file that matches the documentation type.
{% endtab %}

{% tab title="External source" %}
This method allows you to import your documentation from external sources. APIM includes five types of fetchers:

* **GitHub:** Fetch your documentation from a GitHub repository
* **GitLab:** Fetch your documentation from a GitLab repository
* **Git:** Fetch your documentation from any Git repository
* **WWW:** Fetch your documentation from the web
* **Bitbucket:** Fetch your documentation from a Bitbucket repository

<figure><img src="../../../../../../.gitbook/assets/documentation_external source (1).png" alt=""><figcaption><p>Documentation fetcher configuration</p></figcaption></figure>

The documentation is fetched and stored locally in APIM in the following three scenarios:

* Once, after you finish configuring your fetcher
*   Any time you select **Fetch All** on the **Documentation** page

    <figure><img src="../../../../../../.gitbook/assets/documentation_fetch all (1).png" alt=""><figcaption><p>Update all documentation from external sources</p></figcaption></figure>
* At regular intervals when auto-fetch is configured
{% endtab %}
{% endtabs %}

## Import multiple pages

If you have existing documentation for your API in a GitHub or GitLab repository, you can:

* Configure the GitHub or GitLab fetcher to import the complete documentation structure on a one-off or regular basis
* Import the documentation into APIM in a structure different from that of the source repository by:
  * Creating a Gravitee descriptor file (`.gravitee.json`) at the repository root that describes both the source and destination structures
  * Configuring a fetcher in APIM to read the JSON file and import the documentation according to the structure defined in the file

{% tabs %}
{% tab title="Gravitee descriptor file" %}
{% hint style="warning" %}
The Gravitee descriptor file must be named `.gravitee.json` and must be placed at the root of the repository.
{% endhint %}

The following `.gravitee.json` describes a documentation set that includes:

* A homepage in Markdown format in a folder called `/newdoc`, to be placed at the root of the APIM documentation structure
* A JSON file containing a Swagger specification at the root of the repository, to be placed in a folder called `/technical` in the APIM documentation structure

{% code title=".gravitee.json" %}
```json
{
    "version": 1,
    "documentation": {
        "pages": [
            {
                "src": "/newdoc/readme.md",
                "dest": "/",
                "name": "Homepage",
                "homepage": true
            },
            {
                "src": "/test-import-swagger.json",
                "dest": "/technical",
                "name": "Swagger"
            }
        ]
    }
}
```
{% endcode %}
{% endtab %}

{% tab title="Configure a fetcher" %}
Follow the steps below to configure a fetcher to import multiple files:

1.  From the **Documentation** page, select **Import multiple files**

    <figure><img src="../../../../../../.gitbook/assets/Screenshot 2023-06-07 at 4.04.23 PM (1).png" alt=""><figcaption><p>Import multiple documentation files</p></figcaption></figure>
2.  To publish the pages on import, select **Publish all imported pages**

    <figure><img src="../../../../../../.gitbook/assets/import-multiple-files (1).png" alt=""><figcaption><p>Option to publish all imported files</p></figcaption></figure>
3. Select the **GitHub** or **GitLab** fetcher
4.  Specify the details of the external source, such as the URL of the external API, the name of the repository, and the branch. The fields vary slightly depending on the fetcher.

    <figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/import-multiple-file-dets.png" alt=""><figcaption><p>Configure a fetcher</p></figcaption></figure>
5. In the **Filepath** field, enter the path to your JSON documentation specification file
6. Enter a **Username** to authenticate the request
7. Enter a **Personal Access Token**, which must be generated in your GitHub or GitLab user profile
8. To update the pages at regular intervals, select **Auto Fetch** and specify the `crontab` update frequency

{% hint style="info" %}
**`cron` expressions**

A `cron` expression is a string consisting of six fields (representing seconds, minutes, hours, days, months, and weekdays) that describe the schedule. For example:

* Fetch every second: `* * */1 * * *`
* At 00:00 on Saturday : `0 0 0 * * SAT`

If the APIM administrator configured a [maximum fetch frequency](general-settings.md), the value configured by the APIM administrator will override the frequency you specify.
{% endhint %}

9.  Select **IMPORT** for APIM to add the files to your documentation set

    <figure><img src="../../../../../../.gitbook/assets/import-multiple-files-result (1).png" alt=""><figcaption><p>Import technical folder documentation with fetcher</p></figcaption></figure>
{% endtab %}
{% endtabs %}

## Page management

Select a page to configure the following via the header tabs:

* **Page:** Manage the content of the documentation page by via the inline editor or by importing files
* **Translations:** Add translations of your page
* **Configuration:** Toggle options to publish your page and use it as the homepage
* **External Source:** Configure a fetcher for the page
* **Access Control:** Fine-grained access control over your page
* **Attached Resources:** Add additional files to your documentation page.
  * This requires the administrator to configure **Allow Upload Images** and **Max size upload file (bytes)** in [general settings](general-settings.md).

<figure><img src="../../../../../../.gitbook/assets/documentation_page banner (1).png" alt=""><figcaption><p>Page management options</p></figcaption></figure>

**Page**, **Translations** and **Access Control** are described in greater detail below.

{% tabs %}
{% tab title="Page" %}
If incorrect templating is applied to the Markdown page of an API, errors are generated to alert the user that the page will not be formatted as intended when published to the Developer Portal.

<figure><img src="../../../../../../.gitbook/assets/incorrect templating (1).png" alt=""><figcaption><p>Example of incorrect templating</p></figcaption></figure>
{% endtab %}

{% tab title="Translations" %}
You can add translations for your pages via the **Translations** tab:

1. Select **Add a translation**
2. Enter your 2-character language code (FR for French, CZ for Czech, IT for Italian, etc.)
3. Enter the translated title
4. (Optional) You can edit the content to add translated content by toggling on the switch
5. Click **Save Translation** at the bottom of the page

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-translations-1.png" alt=""><figcaption><p>Translate a page</p></figcaption></figure>
{% endtab %}

{% tab title="Access control" %}
From the **Access Control** tab:

* You can mark a page as **Private** if you want to deny access to anonymous users.
* If a page is **Private**, you can configure access lists to either require or exclude certain [roles and groups](../../../using-the-product/administration/README.md) by toggling the **Excluded** option.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-access-control.png" alt=""><figcaption><p>Documentation access control</p></figcaption></figure>
{% endtab %}
{% endtabs %}
