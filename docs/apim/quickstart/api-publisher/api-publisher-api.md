# api-publisher-api

\= Publish your first API with APIM API :page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_quickstart\_publish\_api.html :page-folder: apim/quickstart/api-publisher :page-layout: apim3x

\== Overview

This section walks you through creating and publishing your first API with APIM API. You can find more information in the link:\{{ '/apim/3.x/apim\_publisherguide\_manage\_apis.html' | relative\_url \}}\[API Publisher Guide].

NOTE: In this example we will use the https://api.gravitee.io/echo\[Gravitee.io Echo API] to set up our first proxy API. The Gravitee.io Echo API returns JSON-formatted data via the following URL: https://api.gravitee.io/echo

IMPORTANT: If option _Enable API review_ is enabled in APIM Console, the API `workflow_state` attribute must be set to `REVIEW_OK` before you can deploy or start the API. See _APIs > Manage the API's review state_ in the link:\{{ '/apim/3.x/apim\_installguide\_rest\_apis\_documentation.html' | relative\_url \}}\[API Reference^].

\== Create your API with APIM API

### Create API request:: \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type:application/json;charset=UTF-8" -X POST -d '{"name":"My first API","version":"1","description":"Gravitee.io Echo API Proxy","contextPath":"/myfirstapi","endpoint":"https://api.gravitee.io/echo"}' http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis

Create Plan request::

### \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type:application/json;charset=UTF-8" -X POST -d '{"name":"My Plan","description":"Unlimited access plan","validation":"auto","characteristics":\[],"paths":{"/":\[]},"security":"api\_key"}' http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis/{api-id}/plans

Publish Plan request::

### \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type:application/json;charset=UTF-8" -X POST http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis/{api-id}/plans/{plan-id}/\_publish

### Deploy API request:: \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -X POST http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis/{api-id}/deploy

### Start API request:: \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -X POST http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis/{api-id}?action=START

Publish API on APIM Portal request::

### From the JSON response of the _Create API Request_, add the field `lifecycle_state` with value =`"published"` and send the result in a PUT request. \[source]

### curl -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type:application/json;charset=UTF-8" -X PUT -d '\<RESPONSE\_FROM\_CREATE\_API\_REQUEST + ",lifecycle\_state":"published">' ' http://MANAGEMENT\_API\_SERVER\_DOMAIN/management/organizations/DEFAULT/environments/DEFAULT/apis/{api-id}

For more information, see the complete link:\{{ '/apim/3.x/apim\_installguide\_rest\_apis\_documentation.html' | relative\_url \}}\[APIM API documentation].
