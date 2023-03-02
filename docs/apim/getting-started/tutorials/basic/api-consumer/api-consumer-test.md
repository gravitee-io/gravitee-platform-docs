# api-consumer-test

\= Test your API :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_quickstart\_consume\_test.html :page-folder: apim/quickstart :page-layout: apim3x

Now that you have created your application, you can go ahead and obtain your API key.

. Click _Applications_ in the top menu. . Click _My subscriptions_ in the sub-menu. + image::

\[]

## . Select your application in the list on the left. . Select the API in the list on the right. . Copy the `curl` command at the bottom of the page. + \[IMPORTANT]

By default, the host in the command is `https://api.company.com`. You need to change this value in the _Sharding Tags_ section of the Management UI settings.

## image::\[]

*

### You can use your API Key by setting the HTTP Header `X-Gravitee-Api-Key` or using the request query parameter `api-key`. + \[source]

### curl http://GATEWAY\_SERVER\_DOMAIN/myfirstapi -H "X-Gravitee-Api-Key:"

*

The Gravitee.io Echo API data is returned successfully.

You can now test API requests, as described in the https://github.com/gravitee-io/gravitee-sample-apis/blob/master/gravitee-echo-api/README.md\[Gravitee.io Echo API documentation].
