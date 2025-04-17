# Types of Assets

{% hint style="warning" %}
API Score is a technology preview. This feature is not recommended for production environments.&#x20;
{% endhint %}

## Overview

API score works by analyzing different parts of your APIs and checking them against rulesets. The parts of your API that API Score uses for scoring are called **assets**. The currently supported assets used by API Score are:

* OpenAPI documentation pages
* AsyncAPI documentation pages
* Gravitee proxy API definitions
* Gravitee message API definitions
* Gravitee native Kafka API definitions
* Gravitee federated API definitions
* Gravitee v2 API definitions

All of the "API definition" asset types are essentially the same as what you get if you export an API from the Gravitee API Management Console. They contain all of your API's settings, such as name, version, labels, categories, plans, policies, etc.&#x20;

To assist you in writing rulesets, the sections below include examples of how to obtain copies of assets.&#x20;

## Export a Gravitee API definition&#x20;

To export a Gravitee API definition, follow these steps:

1. Log in to your APIM Console, then click **APIs**.
2. Click the API that you want to export.&#x20;
3. In the **General** or **Configuration** tab, click **Export**.
4. (Optional) Select the information that you want to export. You can choose the following information to export: Groups, Members, Pages, Plans, and Metadata.&#x20;
5. Click **Export**.

Below is a partial example of an exported API definition for a v4 proxy API. All of the attributes you see here can be used in your API Score custom rulesets.&#x20;

{% code lineNumbers="true" %}
````json
{
  "export": {
    "date": "2025-02-27T14:11:38.684449698Z",
    "apimVersion": "4.7.0-SNAPSHOT"
  },
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "listeners": [
      {
        "type": "HTTP",
        "paths": [
          {
            "path": "/0205-javascript/",
            "overrideAccess": false
          }
        ],
        "entrypoints": [
          {
            "type": "http-proxy",
            "qos": "AUTO",
            "configuration": {}
          }
        ]
      }
    ],
    "endpointGroups": [
      {
        "name": "Default HTTP proxy group",
        "type": "http-proxy",
        "loadBalancer": {
          "type": "ROUND_ROBIN"
        },
        "sharedConfiguration": "{\"proxy\":{\"useSystemProxy\":false,\"enabled\":false},\"http\":{\"keepAliveTimeout\":30000,\"keepAlive\":true,\"followRedirects\":false,\"readTimeout\":10000,\"idleTimeout\":60000,\"connectTimeout\":3000,\"useCompression\":true,\"maxConcurrentConnections\":20,\"version\":\"HTTP_1_1\",\"pipelining\":false},\"ssl\":{\"keyStore\":{\"type\":\"\"},\"hostnameVerifier\":true,\"trustStore\":{\"type\":\"\"},\"trustAll\":false}}",
        "endpoints": [
          {
            "name": "Default HTTP proxy",
            "type": "http-proxy",
            "weight": 1,
            "inheritConfiguration": true,
            "configuration": {
              "target": "https://api.gravitee.io/whattimeisit"
            },
            "sharedConfigurationOverride": "{}",
            "services": {},
            "secondary": false
          }
```
````
{% endcode %}

## Federated API definition&#x20;

Federated APIs ingested from 3rd-party providers like AWS, Apigee, Azure, IBM, Mulesoft, Solace, and Confluent, cannot currently be exported from the user interface.&#x20;

To help you write rulesets against this asset type, you can modify the example below. This example shows the structure of a federated API definition.

````yaml
  "api" : {
    "id" : "b9211075-e090-342f-b8db-9944872934ff",
    "name" : "Shipping logistics SA",
    "description" : "Shipping logistics API",
    "createdAt" : "2025-01-21T15:12:52.058Z",
    "updatedAt" : "2025-01-21T15:12:52.058Z",
    "disableMembershipNotifications" : false,
    "metadata" : { },
    "groups" : [ ],
    "visibility" : "PRIVATE",
    "lifecycleState" : "CREATED",
    "tags" : [ ],
    "primaryOwner" : {
      "id" : "1bb403c2-ff43-415f-b403-c2ff43715f6b",
      "displayName" : "admin",
      "type" : "USER"
    },
    "originContext" : {
      "integrationId" : "a5653514-6223-47e6-a535-146223a7e6df",
      "integrationName" : "MBA test",
      "provider" : "azure-api-management"
    },
    "providerId" : "66d70fba01d13164d6ddd453",
    "definitionVersion" : "FEDERATED"
  },
  "members" : [ {
    "id" : "85ad71f8-b321-4560-ad71-f8b321756060"
  } ],
  "metadata" : [ ],
  "pages" : [ {
    "id" : "787e1a8d-7f12-42f5-be1a-8d7f1202f524",
    "referenceId" : "b9211075-e090-342f-b8db-9944872934ff",
    "referenceType" : "API",
    "name" : "Shipping logistics SA-oas.yml",
    "type" : "SWAGGER",
    "order" : 0,
    "published" : true,
    "visibility" : "PRIVATE",
    "createdAt" : "2025-01-21T15:12:52.095Z",
    "updatedAt" : "2025-01-21T15:12:52.095Z",
    "excludedAccessControls" : false,
    "accessControls" : [ ],
    "content" : "truncated OpenAPI definition",
    "homepage" : true,
    "configuration" : {
      "tryIt" : "true",
      "viewer" : "Swagger"
    }
```
````
