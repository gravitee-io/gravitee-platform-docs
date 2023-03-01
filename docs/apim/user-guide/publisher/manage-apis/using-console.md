# Overview

The following sections describe the different ways you can create an API
using APIM Console.

For a quick introduction to creating an API in APIM, see the link:{{
*/apim/3.x/apim\_quickstart\_publish\_ui.html* | relative\_url }}\[Quick
Start Guide^\].

From APIM 3.5.x, the recommended way to create an API is using the
**DESIGN STUDIO** method described in the next section. For APIs created
using this method, clicking the **Design** menu option automatically
opens Design Studio. Old API definitions or APIs created using the
**PATH BASED** option must be migrated before you can update them in
Design Studio. For more information, see the link:{{
*/apim/3.x/apim\_publisherguide\_design\_studio\_overview.html* |
relative\_url }}\[Design Studio Guide^\].

# Get started

Using APIM Console, you can create new API definitions from scratch, or
import existing definitions.

You can also create APIs using APIM API. For more details, see the
link:{{ */apim/3.x/apim\_quickstart\_publish\_api.html* | relative\_url
}}\[Quick Start Guide^\].

To start creating an API:

1.  In APIM Console, click **APIs**.

2.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] at the bottom right of the page.

    image::{% link images/apim/3.10/apim-console-create-api.png
    %}\[Create API\]

    APIM presents you with two options for creating APIs. The
    recommended option is **DESIGN STUDIO**.

    image::{% link
    images/apim/3.x/quickstart/publish/graviteeio-create-api-2.png
    %}\[\]

3.  Under **DESIGN STUDIO**, click:

    -   **CREATE** to create an API from scratch.

        Learn how to [???](#create_an_api_from_scratch)

    -   **IMPORT** to import an external API definition.

        Learn how to [???](#import_an_api_definition)

# Create an API from scratch

These steps describe how to create all of the basic API configuration
your developers need to call your API. If a short TTFAC (time to first
API call) is your goal, configure only the mandatory parts and a basic
plan now — you can always update these later on.

You need to create a plan before you can accept user subscriptions to
your API. You can do that now or when you get to the link:{{
*/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html* |
relative\_url }}\[Plans and subscriptions^\] section, but the plan
options available to you now are more limited.

1.  Enter the general details of the API:

    -   A **Name**, **Version**, and **Description**.

    -   The **Context-path** where the API will be exposed on APIM
        Gateway, starting from **/**.

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/create-api-general-withgroups.png
        %}\[\]

2.  (Optional) Associate a group with the API, if any are defined (see
    link:{{ */apim/3.x/apim\_adminguide\_users\_and\_groups.html* |
    relative\_url }}\[Users and Groups\] for more details):

    -   Select a group which can access the API in **Groups**.

    -   If the link:{{
        */apim/3.x/apim\_adminguide\_users\_and\_groups.html#primary\_owner\_mode*
        | relative\_url }}\[Primary owner mode^\] is **HYBRID**, click
        the **Advanced mode** link to associate a primary owner group.

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-api-primaryowner-mode-3.png
        %}\[\]

3.  Click **NEXT**.

4.  Enter the details of the gateway:

    -   A backend URL for receiving API calls.

    -   (Optional) Click the **Advanced mode** link to specify details
        of tenants and sharding tags.

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/create-api-gateway.png
        %}\[\]

5.  Click **NEXT**.

6.  (Optional) If you want to create a plan for the API, enter the
    following details and click **NEXT**, otherwise click **SKIP**:

    -   The **Name**, **Security type**, and **Description**.

    -   If subscription auto-validation is required, toggle on the
        **Auto validate subscription** option.

    -   The **Characteristics**.

    -   **Rate limit** and **Quota** details. In this example, we are
        specifying a rate limit of 1 request every 5 seconds.

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/create-api-plan1.png
        %}\[\] \* **Resource filtering** details, using link:{{
        */apim/3.x/apim\_policies\_overview.html#ant-notation* |
        relative\_url }}\[Ant^\] notation and an HTTP method.

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/create-api-plan-path.png
        %}\[\]

7.  (Optional) Import a documentation specification file, otherwise
    click **SKIP**.

8.  Review the details of the API, then click one of the following
    options, depending on whether you want to create and deploy the API
    or simply create it:

    -   **CREATE THE API WITHOUT DEPLOYING IT**

    -   **CREATE AND START THE API**

        image::{% link
        images/apim/3.x/api-publisher-guide/manage-apis/create-api-confirm.png
        %}\[\]

# Import an API definition

You can import external API definitions using one of the following
methods.

## Import an existing API definition

You can import and export your APIs to a Gravitee API definition format
(see the example below).

To import an API from an API definition:

-   If the definition is a file, select **IMPORT FILE** and browse your
    file system to select it.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-definition-file.png
%}\[Import from definition file, 300\]

-   If the definition is a link, select **IMPORT FROM LINK**, then
    choose **API Definition** and enter the definition URL.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-definition-link.png
%}\[Import from definition link, 300\]

Learn more about API definition import process link:{% link
pages/apim/3.x/user-guide/publisher/import-apis.adoc %}\[here\].

## Import an OpenAPI specification

One of the most powerful features of APIM is its ability to import an
OpenAPI specification to create an API. When you import an existing
specification you do not have to complete all the fields required when
you create a new API.

To import an API from OpenAPI:

-   If the OpenAPI specification is a file, select **IMPORT FILE** and
    browse your file system to select it.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-file.png
%}\[Import from definition file, 300\]

-   If the OpenAPI specification is a link, select **IMPORT FROM LINK**,
    choose **Swagger / OpenAPI** and enter the definition URL.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-link.png
%}\[Import from definition link, 300\]

### How the context-path is determined

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Specification version</p></td>
<td style="text-align: left;"><p>Definition</p></td>
<td style="text-align: left;"><p>Example</p></td>
<td style="text-align: left;"><p>Context-path</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Swagger (V2)</p></td>
<td style="text-align: left;"><p><code>basePath</code> field, if it
exists.</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb1"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;swagger&quot;</span><span class="fu">:</span> <span class="st">&quot;2.0&quot;</span><span class="fu">,</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;info&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;description&quot;</span><span class="fu">:</span> <span class="st">&quot;...&quot;</span><span class="fu">,</span></span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;version&quot;</span><span class="fu">:</span> <span class="st">&quot;1.0.5&quot;</span><span class="fu">,</span></span>
<span id="cb1-6"><a href="#cb1-6" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;title&quot;</span><span class="fu">:</span> <span class="st">&quot;Swagger Petstore&quot;</span></span>
<span id="cb1-7"><a href="#cb1-7" aria-hidden="true" tabindex="-1"></a>  <span class="fu">},</span></span>
<span id="cb1-8"><a href="#cb1-8" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;host&quot;</span><span class="fu">:</span> <span class="st">&quot;petstore.swagger.io&quot;</span><span class="fu">,</span></span>
<span id="cb1-9"><a href="#cb1-9" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;basePath&quot;</span><span class="fu">:</span> <span class="st">&quot;/v2&quot;</span><span class="fu">,</span></span>
<span id="cb1-10"><a href="#cb1-10" aria-hidden="true" tabindex="-1"></a>  <span class="er">...</span></span>
<span id="cb1-11"><a href="#cb1-11" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
<td style="text-align: left;"><p>/v2</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>If not, lowercase trimmed
<code>info.title</code>.</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;swagger&quot;</span><span class="fu">:</span> <span class="st">&quot;2.0&quot;</span><span class="fu">,</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;info&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;description&quot;</span><span class="fu">:</span> <span class="st">&quot;...&quot;</span><span class="fu">,</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;version&quot;</span><span class="fu">:</span> <span class="st">&quot;1.0.5&quot;</span><span class="fu">,</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;title&quot;</span><span class="fu">:</span> <span class="st">&quot;Swagger Petstore&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>  <span class="fu">},</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;host&quot;</span><span class="fu">:</span> <span class="st">&quot;petstore.swagger.io&quot;</span><span class="fu">,</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>  <span class="er">...</span></span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
<td style="text-align: left;"><p>/swaggerpetstore</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>OpenAPI (V3)</p></td>
<td style="text-align: left;"><p>Path of the first
<code>servers.url</code>, if it exists, without "/".<br />
</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb3"><pre
class="sourceCode yaml"><code class="sourceCode yaml"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="fu">openapi</span><span class="kw">:</span><span class="at"> </span><span class="st">&quot;3.0.0&quot;</span></span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a><span class="fu">info</span><span class="kw">:</span></span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">version</span><span class="kw">:</span><span class="at"> </span><span class="fl">1.0.0</span></span>
<span id="cb3-4"><a href="#cb3-4" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">title</span><span class="kw">:</span><span class="at"> Swagger Petstore</span></span>
<span id="cb3-5"><a href="#cb3-5" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">license</span><span class="kw">:</span></span>
<span id="cb3-6"><a href="#cb3-6" aria-hidden="true" tabindex="-1"></a><span class="at">    </span><span class="fu">name</span><span class="kw">:</span><span class="at"> MIT</span></span>
<span id="cb3-7"><a href="#cb3-7" aria-hidden="true" tabindex="-1"></a><span class="fu">servers</span><span class="kw">:</span></span>
<span id="cb3-8"><a href="#cb3-8" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="kw">-</span><span class="at"> </span><span class="fu">url</span><span class="kw">:</span><span class="at"> http://petstore.swagger.io/v1</span></span>
<span id="cb3-9"><a href="#cb3-9" aria-hidden="true" tabindex="-1"></a><span class="fu">paths</span><span class="kw">:</span></span>
<span id="cb3-10"><a href="#cb3-10" aria-hidden="true" tabindex="-1"></a><span class="co">...</span></span></code></pre></div></td>
<td style="text-align: left;"><p>/v1</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>If not, lowercase trimmed
<code>info.title</code>.</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb4"><pre
class="sourceCode yaml"><code class="sourceCode yaml"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a><span class="fu">openapi</span><span class="kw">:</span><span class="at"> </span><span class="st">&quot;3.0.0&quot;</span></span>
<span id="cb4-2"><a href="#cb4-2" aria-hidden="true" tabindex="-1"></a><span class="fu">info</span><span class="kw">:</span></span>
<span id="cb4-3"><a href="#cb4-3" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">version</span><span class="kw">:</span><span class="at"> </span><span class="fl">1.0.0</span></span>
<span id="cb4-4"><a href="#cb4-4" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">title</span><span class="kw">:</span><span class="at"> Swagger Petstore</span></span>
<span id="cb4-5"><a href="#cb4-5" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="fu">license</span><span class="kw">:</span></span>
<span id="cb4-6"><a href="#cb4-6" aria-hidden="true" tabindex="-1"></a><span class="at">    </span><span class="fu">name</span><span class="kw">:</span><span class="at"> MIT</span></span>
<span id="cb4-7"><a href="#cb4-7" aria-hidden="true" tabindex="-1"></a><span class="fu">servers</span><span class="kw">:</span></span>
<span id="cb4-8"><a href="#cb4-8" aria-hidden="true" tabindex="-1"></a><span class="at">  </span><span class="kw">-</span><span class="at"> </span><span class="fu">url</span><span class="kw">:</span><span class="at"> http://petstore.swagger.io/</span></span>
<span id="cb4-9"><a href="#cb4-9" aria-hidden="true" tabindex="-1"></a><span class="fu">paths</span><span class="kw">:</span></span>
<span id="cb4-10"><a href="#cb4-10" aria-hidden="true" tabindex="-1"></a><span class="at">  ...</span></span></code></pre></div></td>
<td style="text-align: left;"><p>/swaggerpetstore</p></td>
<td></td>
</tr>
</tbody>
</table>

### Vendor extensions

You can use a vendor extension to add more information to OpenAPI
specifications about your API. To do this, you need to add the
`x-graviteeio-definition` field at the root of the specification. The
value of this field is an `object` that follows this [JSON
Schema^](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-rest-api/gravitee-apim-rest-api-service/src/main/resources/schema/xGraviteeIODefinition.json)

-   `categories` must contain either a key or an id. Only existing
    categories are imported.

-   Import will fail if `virtualHosts` are already in use by **other**
    APIs.

-   If set, `virtualHosts` will override `contextPath`.

-   `groups` must contain group names. Only existing groups are
    imported.

-   `metadata.format` is case-sensitive. Possible values are:

    -   STRING

    -   NUMERIC

    -   BOOLEAN

    -   DATE

    -   MAIL

    -   URL

-   `picture` only accepts Data-URI format (see example below).

Here is an example: \`\`\`yaml openapi: "3.0.0" info: version: 1.2.3
title: Gravitee.io Echo API license: name: MIT servers: - url:
<https://demo.gravitee.io/gateway/echo> x-graviteeio-definition:
categories: - supplier - product virtualHosts: - host: api.gravitee.io
path: /echo overrideEntrypoint: true groups: - myGroupName labels: -
echo - api metadata: - name: relatedLink value: <http://external.link>
format: URL picture:
data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
properties: - key: customHttpHeader value: X-MYCOMPANY-ID tags: - DMZ -
partner - internal visibility: PRIVATE paths: … \`\`\`

### Policies on path

When importing an OpenAPI definition, you can select the option **Create
policies on path** in the import form. This specifies that all routes
declared in the OpenAPI specification are to be automatically created in
APIM. You can navigate to the policy management view to check.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-openapi-policies-path.png
%}\[Policies view - all routes imported\]

You can also choose to activate policies that will be configured using
the OpenAPI specification.

JSON Validation  
For each operation, if an `application/json` request body exists, then a
JSON schema is computed from this body to configure a JSON Validation
policy.  
REQUEST only  
More information is available link:{{
*/apim/3.x/apim\_policies\_json\_validation.html* | relative\_url
}}\[here\].

REST to SOAP transformer  
For each operation, if the definition contains some specific vendor
extensions, a REST to SOAP policy can be configured.  
These extensions are:

-   `x-graviteeio-soap-envelope`: contains the SOAP envelope

-   `x-graviteeio-soap-action`: contains the SOAP action

    REQUEST only  
    More information is available link:{{
    */apim/3.x/apim\_policies\_rest2soap.html* | relative\_url
    }}\[here\].

Mock  
For each operation, a mock policy is configured, based on the `example`
field if it exists, or by generating a random value for the type of the
attribute to mock.  
REQUEST only  
More information is available link:{{
*/apim/3.x/apim\_policies\_mock.html* | relative\_url }}\[here\].

Validation Request  
For each operation, `NOT__ __NULL` rules are created with query
parameters and headers.  
REQUEST only  
More information is available link:{{
*/apim/3.x/apim\_policies\_request\_validation.html* | relative\_url
}}\[here\]-

XML Validation  
For each operation, if a `application/xml` request body exists, then a
XSD schema is computed from this body to configure an XML Validation
policy.  
REQUEST only  
More information is available link:{{
*/apim/3.x/apim\_policies\_xml\_validation.html* | relative\_url
}}\[here\].

## Import a WSDL

APIM can import a WSDL to create an API. This means you do not have to
declare all the routing and policies to interact with your service.

To import an API from a WSDL:

-   If the WSDL is a file, select **IMPORT FILE** and browse your file
    system to select it.

-   If the WSDL is a link, select **IMPORT FROM LINK**, choose **WSDL**
    and enter the definition URL.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-wsdl-rest-to-soap-options.png
%}\[Import from WSDL link\]

If you select the option **Apply REST to SOAP Transformer policy** in
addition to the option **Create policies on path** in the import form, a
REST-To-SOAP policy will be generated for each path. These policies
provide a SOAP envelope for each method with sample data that you can
change using expression language. An XML-to-JSON policy will also be
generated to convert the entire SOAP response to JSON format.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-import-wsdl-rest-to-soap-policy.png
%}\[WSDL REST to SOAP policy\]

# Manage your API

The API is created private, so it is only accessible in APIM Portal to
users after you:

-   Publish it

-   Make it public or add new members or groups to it

The process for adding new members or groups to the API is explained in
link:{{ */apim/3.x/apim\_publisherguide\_manage\_members.html* |
relative\_url }}\[API users and ownership^\].

You can publish the API or make it public, as well as remove it from
APIM Portal or delete it, in the **Danger Zone**:

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/danger-zone.png %}\[\]

# Organize your APIs into categories

You can create *categories* to group APIs. The purpose of categories is
to group APIs so consumers can easily find the APIs they need in APIM
Portal.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-categories-1.png
%}\[\]

You can describe a category with the following characteristics:

-   Name

-   Description

-   Picture

-   Markdown page as documentation

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-categories-2.png
%}\[\]

Once you have finished describing the category, you select the APIs you
want to include in it.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-categories-3.png
%}\[\]

You can also choose to highlight a particular API. This API will be
shown at the top of the category page.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-categories-4.png
%}\[\] image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-categories-4.png
%}\[\] The next time you enter labels for an API, APIM Console makes
suggestions based on your registered labels.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-labels-2.png
%}\[\]

You can search for APIs by label.

image::{% link
images/apim/3.x/api-publisher-guide/manage-apis/graviteeio-manage-apis-labels-3.png
%}\[\]
