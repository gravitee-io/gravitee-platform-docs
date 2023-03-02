# api-consumer-api

\= Consuming an API with APIM API :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_quickstart\_consume\_api.html :page-folder: apim/quickstart :page-layout: apim3x

\== Overview

This guide walks you through creating your first application and subscribing to your first API with APIM API. For a brief overview of how to set up your first API, see the _Publish your first API_ section of the Quick Start Guide.

NOTE: APIM includes several ways to access and secure an API, as described in (link:\{{ '/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html' | relative\_url \}}\[API Publisher Plans and subscriptions]). In this example, we will access an API using an link:\{{ '/apim/3.x/apim\_policies\_apikey.html' | relative\_url \}}\[API Key]. Only trusted applications can access the API data by requesting an API Key.

\== Create your application and subscribe to an API

### Create application request:: \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type:application/json;charset=UTF-8" -X POST -d '{"name":"My first Application","type":"Web","description":"Web client for Gravitee.io Echo API"}' http://MANAGEMENT\_API\_SERVER\_DOMAIN/portal/environments/DEFAULT/applications

### Subscribe to API request:: \[source]

### curl -H "Authorization: Basic $lmA\_AUTH" -H "Content-Type:application/json;charset=UTF-8" -X POST -d '{"application":"\[APPLICATION\_ID]","plan":"\[PLAN\_ID]"' http://MANAGEMENT\_API\_SERVER\_DOMAIN/portal/environments/DEFAULT/subscriptions

For more information, see the complete link:\{{ '/apim/3.x/apim\_installguide\_rest\_apis\_documentation.html' | relative\_url \}}\[Rest API documentation].
