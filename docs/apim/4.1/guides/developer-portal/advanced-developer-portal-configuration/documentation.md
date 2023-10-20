# Documentation

Outside of APIs and applications, administrators can also provide site-wide documentation for API publishers and consumers. This documentation creates a direct line of communication with your developer community through a single channel. For example, you can use it to communicate your best practices, configure your own homepage, or even reference it in links when using [custom navigation](documentation.md#custom-navigation). All published documentation can be accessed in the Developer Portal's **Documentation** page as shown below.

{% hint style="info" %}
Site-wide documentation is separate from API documentation which can be added to an API by an API publisher.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 10.24.20 AM.png" alt=""><figcaption><p>Developer portal documentation page</p></figcaption></figure>

### Documentation types

To add some documentation, you can either create new pages or import them from a file or external source.

APIM supports multiple types of documentation:

* Markdown (for more information, see [Markdown documentation](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_publish\_documentation\_markdown.html) and [Markdown templates](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_publish\_documentation\_markdown\_template.html))
* AsciiDoc (for more information, see [AsciiDoc documentation](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_publish\_documentation\_asciidoc.html))
* OpenAPI (Swagger) (for more information, see [OpenAPI documentation](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_publish\_documentation\_openapi.html))
* AsynAPI (for more information, see [AsycAPI documentation](https://www.asyncapi.com/docs))

### Create documentation

To create documentation, go to **Settings > Documentation** in the Management Console.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 3.22.29 PM.png" alt=""><figcaption><p>Documentation settings page</p></figcaption></figure>

{% hint style="info" %}
**System folders**

Header, TopFooter, and Footer are known as system folders. They can be used to customize the Developer Portal's navigation by adding custom links. For more information, see [Custom navigation.](documentation.md#custom-navigation)
{% endhint %}

From here, you can create a new documentation page by selecting the **+ icon** in the bottom right. This presents you with the following options:

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 3.45.43 PM.png" alt=""><figcaption><p>Create new documentation options</p></figcaption></figure>

* **Folder:** Generate a folder to organize your documentation. This also allows you to quickly generate translations of the entire folder by selecting **Translate Folder**. More information is provided on [translations below](documentation.md#translate-a-page).

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 3.49.15 PM.png" alt=""><figcaption><p>Sample documentaion folder</p></figcaption></figure>

* **Markdown Template:** Create templates to be re-used for both site-wide and API markdown documentation.
* **Markdown:** Use the Markdown syntax for the documentation page
* **Asciidoc:** Use the Asciidoc syntax for the documentation page
* **OpenAPI (Swagger):** Use the OpenAPI syntax for the documentation page
* **AsyncAPI:** Use the AsyncAPI syntax for the documentation page

Regardless of your selection, each documentation type provides similar configuration options followed by a text editor matching the type of document you selected.

<figure><img src="../../../.gitbook/assets/new_docs_page.png" alt=""><figcaption><p>Creating a documentation page</p></figcaption></figure>

* **Name:** Provide a label for your documentation page
* **Set as homepage:** Use the documentation page on the homepage of the Developer Portal

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-07 at 3.04.50 PM.png" alt=""><figcaption><p>Custom homepage example</p></figcaption></figure>

{% hint style="info" %}
If you set multiple documentation pages as the homepage, only the page most recently set as the homepage will be active.
{% endhint %}

* **Publish this page:** Make the page available in the Developer Portal
* **Make private:** Make the page private to you and the users you explicitly allow through access control. Access control is detailed in the [Page configuration](documentation.md#configure-a-page) section.

The rest of the settings revolve around generating content for your new documentation page. APIM provides three main methods for generating documentation content

* Fill the content inline
  * Supports templating with API properties
* Import from file
* Import from an external source (Gitlab, Bitbucket, etc.)

### Fill the content inline (templating support)

This method is mostly self-explanatory as you will use the text editor to generate content based on the documentation type you selected. However, APIM also supports templating with API properties.

#### Templating with API properties

You can access your API data in your API documentation with the following syntax: `${api.name} or ${api.metadata['foo-bar']}`. This example shows how to create documentation templates based on the Apache [FreeMarker template engine](https://freemarker.apache.org/). Below the example, you can find a full reference table of available API properties.

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

## How to access

The API can be accessed through https://api.company.com${api.proxy.contextPath}:

curl https://api.company.com${api.proxy.contextPath}

## Rating

You can rate and put a comment for this API <a href='/#!/apis/${api.id}/ratings'>here</a>.

## Contact

The support contact is <a href="mailto:${api.metadata['email-support']}">${api.metadata['email-support']}</a>.

The API owner is <#if api.primaryOwner.email??><a href="mailto:${api.primaryOwner.email}">${api.primaryOwner.displayName}</a><#else>${api.primaryOwner.displayName}</#if>.
```
{% endcode %}

This has the following result in the Developer Portal:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-template.png" alt=""><figcaption><p>Result of templating engine example</p></figcaption></figure>

#### API properties reference

<table data-full-width="false"><thead><tr><th>Field name</th><th>Field type</th><th>Example</th></tr></thead><tbody><tr><td>id</td><td>String</td><td>70e72a24-59ac-4bad-a72a-2459acbbad39</td></tr><tr><td>name</td><td>String</td><td>My first API</td></tr><tr><td>description</td><td>String</td><td>My first API</td></tr><tr><td>version</td><td>String</td><td>1</td></tr><tr><td>metadata</td><td>Map</td><td>{"email-support": "<a href="mailto:support.contact@company.com">support.contact@company.com</a>"}</td></tr><tr><td>createdAt</td><td>Date</td><td>12 juil. 2018 14:44:00</td></tr><tr><td>updatedAt</td><td>Date</td><td>12 juil. 2018 14:46:00</td></tr><tr><td>deployedAt</td><td>Date</td><td>12 juil. 2018 14:49:00</td></tr><tr><td>picture</td><td>String</td><td>data:image/png;base64,iVBO…​</td></tr><tr><td>state</td><td>String</td><td>STARTED/STOPPED</td></tr><tr><td>visibility</td><td>String</td><td>PUBLIC/PRIVATE</td></tr><tr><td>tags</td><td>Array</td><td>["internal", "sales"]</td></tr><tr><td>proxy.contextPath</td><td>String</td><td>/stores</td></tr><tr><td>primaryOwner.displayName</td><td>String</td><td>Firstname Lastname</td></tr><tr><td>primaryOwner.email</td><td>String</td><td><a href="mailto:firstname.lastname@company.com">firstname.lastname@company.com</a></td></tr></tbody></table>

### Import from file

This method allows you to import a file matching the documentation type to generate the content.

### External source

The final method allows you to import your documentation from external sources. APIM includes five types of fetchers:

* **GitHub:** fetch your documentation from a GitHub repository
* **GitLab:** fetch your documentation from a GitLab repository
* **Git:** fetch your documentation from any Git repository
* **WWW:** fetch your documentation from the web
* **Bitbucket:** fetch your documentation from a Bitbucket repository

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-external-source-auto-fetch.png" alt=""><figcaption><p>Documentation fetcher configuration</p></figcaption></figure>

The documentation is fetched and stored locally in APIM in the following three scenarios:

1. Documentation is fetched a single time after you finish configuring your fetcher
2. Any time you select **Fetch All**

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-07 at 4.02.38 PM.png" alt=""><figcaption><p>Update all documentation from external sources</p></figcaption></figure>

3. At regular intervals if you configure auto-fetch

#### Import multiple pages

If you have an existing documentation set for your API in a GitHub or GitLab repository, you can configure the GitHub or GitLab fetcher to import the complete documentation structure on a one-off or regular basis.

Additionally, you can import the documentation into APIM in a different structure from the source repository structure. To do this, you need to create a Gravitee descriptor file (`.gravitee.json`), at the root of the repository, describing both the source and destination structure.

You can then configure a fetcher in APIM to read the JSON file and import the documentation according to the structure defined in the file.

{% hint style="warning" %}
The Gravitee descriptor file must be named `.gravitee.json` and must be placed at the root of the repository.
{% endhint %}

The following Gravitee descriptor describes a documentation set that includes:

* A home page in Markdown format in a folder called `/newdoc` to be placed at the root of the APIM documentation structure
* A JSON file containing a Swagger specification at the root of the repository, to be placed in a folder called `/technical` in the APIM documentation structure.

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

The following steps detail how to actually configure a fetcher to import multiple files:

1. Select **Import multiple files**

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-07 at 4.04.23 PM.png" alt=""><figcaption><p>Import multiple documentation files</p></figcaption></figure>

2. If you want to publish the pages on import, select **Publish all imported pages**

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/import-multiple-files.png" alt=""><figcaption></figcaption></figure>

3. Select the **GitHub** or **GitLab** fetcher
4.  Specify the details of the external source, such as the URL of the external API, the name of the repository, and the branch. The fields vary slightly depending on the fetcher.

    <figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/import-multiple-file-dets.png" alt=""><figcaption><p>Configure a fetcher</p></figcaption></figure>
5. In **Filepath**, enter the path to your JSON documentation specification file
6. Enter an access token, which you need to generate in your GitHub or GitLab user profile
7. Select **Auto Fetch** and specify the `crontab` update frequency, if you want the pages to be updated at regular intervals.

{% hint style="info" %}
**`cron` expressions**

A `cron` expression is a string consisting of six fields that describe the schedule (representing seconds, minutes, hours, days, months and weekdays).

For example:

* Fetch every second: `* * */1 * * *`
* At 00:00 on Saturday : `0 0 0 * * SAT`

If the APIM administrator [configured a maximum fetch frequency](documentation.md#general-settings), the value configured by the APIM administrator will override the frequency you specify.
{% endhint %}

8. Select **IMPORT** and APIM adds the files to your documentation set.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/import-multiple-files-result.png" alt=""><figcaption><p>Import technical folder documentation with fetcher</p></figcaption></figure>

### Page management

You can select a page from the list and configure the settings below. For

* [**Page:**](documentation.md#create-documentation) Manage the content of the documentation page by using the inline editor or importing files
* [**Translations:**](documentation.md#translate-a-page) Add translations of your page
* **Configuration:** Toggle options to publish your page and use it as the homepage
* [**External Source:**](documentation.md#external-source) Configure a fetcher for the page
* [**Access Control:**](documentation.md#access-control) Fine-grained access control over your page
* **Attached Resources:** Add additional files to your documentation page. This [setting must be enabled](documentation.md#general-settings) by the administrator.

#### Translations

You can add translations for your pages. In the **Translations** tab:

1. Select **Add a translation**
2. Enter your 2-character language code (FR for French, CZ for Czech, IT for Italian, etc.)
3. Enter the translated title
4. (Optional) You can edit the content to add translated content by toggling on the switch
5. Click **Save Translation** at the bottom of the page

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-translations-1.png" alt=""><figcaption><p>Translate a page</p></figcaption></figure>

#### Access control

In the **Access Control** tab, you can mark a page as **Private** if you want to deny access to anonymous users.

For private pages, you can configure access lists by required or to be excluded roles/groups. You can learn more about creating roles/groups in our [Administration Guide](../../administration/).

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/documentation/graviteeio-page-documentation-access-control.png" alt=""><figcaption><p>Documentation access control</p></figcaption></figure>
