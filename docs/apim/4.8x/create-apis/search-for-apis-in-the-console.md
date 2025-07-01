# Search for APIs in the Console

## Overview

The **APIs** page in the APIM Console displays all of the APIs that have been created or imported into Gravitee, along with specific columns like the API definition type, status, entrypoint path or hostname, ([sharding](../gravitee-gateway/sharding-tags.md)) tags, categories, owner, and visibility status.

From this page you can complete the following actions:

* [Add](v4-api-creation-wizard.md), [design](https://documentation.gravitee.io/api-designer), or [import](import-apis.md) a new API
* [Search](search-for-apis-in-the-console.md#searching-apis) or filter your APIs
* Browse the list of your APIs
* View/edit an API by clicking its name or the pencil icon

<figure><img src="../.gitbook/assets/image (244).png" alt=""><figcaption><p>Example screenshot of the API menu (in the Gravitee API Management Console)</p></figcaption></figure>

## Search for APIs

It can be challenging to browse through a long list of APIs to find a specific API. You can use the search box to filter and find your API.

<figure><img src="../.gitbook/assets/image (245).png" alt=""><figcaption><p>Search APIs</p></figcaption></figure>

Here is the list of API fields that you can use as search filters:

* Name: `name`
* Description: `description`
* Owner Name: `ownerName`
* Labels: `labels`
* Categories: `categories`
* Paths: `paths`
* Tags: `tags`
* Definition Version: `definition_version`
* Origin: `origin`
* Has Health Check: `has_health_check`

### Search Examples

Here are some examples of what you can enter into the search bar to filter the results:

* For a label: `labels:NewLabel`
* For an API that matches a given name and a given description: `name:"Butterfly*" & description:"This*"`
* For any API that matches the name or the description: `name:"Butterfly*" description:"*REST*"`
* For all v4 APIs: `definition_version:4.0.0`
* For APIs that have either of the given [sharding tags](../gravitee-gateway/sharding-tags.md): `tags:china-internet tags:china`
* For an API name that contains one term but not another: `name:"*Allan*" NOT name:"*Test_"`
* For any APIs that have [health checks](../configure-v4-apis/health-checks.md) configured:  `has_health_check:true`

{% hint style="info" %}
Gravitee uses [Apache Lucene](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html) so you can create your own queries using its rich query language.
{% endhint %}
