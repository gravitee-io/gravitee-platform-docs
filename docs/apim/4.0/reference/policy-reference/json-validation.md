---
description: This page provides the technical details of the JSON Validation policy
---

# JSON Validation

## Overview

You can use the `json-validation` policy to validate JSON payloads. This policy uses [JSON Schema Validator](https://github.com/java-json-tools/json-schema-validator). It returns `400 BAD REQUEST` when request validation fails and `500 INTERNAL ERROR` when response validation fails, with a custom error message body. It can inject processing report messages into request metrics for analytics.

Functional and implementation information for the `json-validation` policy is organized into the following sections:

* [Examples](json-validation.md#examples)
* [Configuration](json-validation.md#configuration)
* [Compatibility Matrix](json-validation.md#compatibility-matrix)
* [Errors](json-validation.md#errors)
* [Changelogs](json-validation.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
Sample policy configuration:

````json
```json
{
  "name" : "10 - JSON Validation",
  "crossId" : "e93e55c0-12ef-494a-be55-c012ef594a3f",
  "version" : "1",
  "execution_mode" : "v4-emulation-engine",
  "description" : "",
  "visibility" : "PRIVATE",
  "flows" : [ ],
  "gravitee" : "2.0.0",
  "flow_mode" : "DEFAULT",
  "resources" : [ ],
  "properties" : [ ],
  "members" : [ {
    "source" : "memory",
    "sourceId" : "admin",
    "roles" : [ "a9ffb95e-11a8-4c22-bfb9-5e11a86c223b" ]
  } ],
  "pages" : [ {
    "id" : "1ba43c1d-dfaa-3e0b-b9b7-6adf80c07455",
    "crossId" : "8e76e2f8-568f-4608-b6e2-f8568fc608e9",
    "name" : "Aside",
    "type" : "SYSTEM_FOLDER",
    "order" : 0,
    "lastContributor" : "03d583c3-0bb0-40e7-9583-c30bb040e707",
    "published" : true,
    "visibility" : "PUBLIC",
    "lastModificationDate" : 1696957038226,
    "contentType" : "application/json",
    "homepage" : false,
    "parentPath" : "",
    "excludedAccessControls" : false,
    "accessControls" : [ ],
    "api" : "44407f48-4b26-4c1c-807f-484b264c1c82",
    "attached_media" : [ ]
  } ],
  "plans" : [ {
    "id" : "7c4ae370-ad52-4df1-8ae3-70ad52bdf1b1",
    "crossId" : "4c252b72-2097-45d4-a52b-72209775d4c5",
    "name" : "Keyless Plan",
    "description" : "Keyless plan",
    "validation" : "AUTO",
    "security" : "KEY_LESS",
    "type" : "API",
    "status" : "PUBLISHED",
    "api" : "44407f48-4b26-4c1c-807f-484b264c1c82",
    "order" : 0,
    "characteristics" : [ ],
    "tags" : [ ],
    "created_at" : 1695919747226,
    "updated_at" : 1696957038220,
    "published_at" : 1695919747226,
    "paths" : { },
    "flows" : [ {
      "id" : "0ebceb7d-77a2-43d3-bceb-7d77a2a3d3ee",
      "path-operator" : {
        "path" : "/",
        "operator" : "STARTS_WITH"
      },
      "condition" : "",
      "consumers" : [ ],
      "methods" : [ ],
      "pre" : [ ],
      "post" : [ {
        "name" : "JSON Validation",
        "description" : "",
        "enabled" : true,
        "policy" : "json-validation",
        "configuration" : {"schema":"{\n  \"type\": \"array\",\n  \"items\": {\n    \"type\": \"object\",\n    \"properties\": {\n      \"name\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"common\": { \"type\": \"string\" },\n          \"official\": { \"type\": \"string\" },\n          \"nativeName\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"eng\": {\n                \"type\": \"object\",\n                \"properties\": {\n                  \"official\": { \"type\": \"string\" },\n                  \"common\": { \"type\": \"string\" }\n                },\n                \"required\": [\"official\", \"common\"]\n              },\n              \"urd\": {\n                \"type\": \"object\",\n                \"properties\": {\n                  \"official\": { \"type\": \"string\" },\n                  \"common\": { \"type\": \"string\" }\n                },\n                \"required\": [\"official\", \"common\"]\n              }\n            },\n            \"required\": [\"eng\", \"urd\"]\n          }\n        },\n        \"required\": [\"common\", \"official\", \"nativeName\"]\n      },\n      \"tld\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"cca2\": { \"type\": \"string\" },\n      \"ccn3\": { \"type\": \"string\" },\n      \"cca3\": { \"type\": \"string\" },\n      \"cioc\": { \"type\": \"string\" },\n      \"independent\": { \"type\": \"boolean\" },\n      \"status\": { \"type\": \"string\" },\n      \"unMember\": { \"type\": \"boolean\" },\n      \"currencies\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"PKR\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"name\": { \"type\": \"string\" },\n              \"symbol\": { \"type\": \"string\" }\n            },\n            \"required\": [\"name\", \"symbol\"]\n          }\n        },\n        \"required\": [\"PKR\"]\n      },\n      \"idd\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"root\": { \"type\": \"string\" },\n          \"suffixes\": {\n            \"type\": \"array\",\n            \"items\": { \"type\": \"string\" }\n          }\n        },\n        \"required\": [\"root\", \"suffixes\"]\n      },\n      \"capital\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"altSpellings\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"region\": { \"type\": \"string\" },\n      \"subregion\": { \"type\": \"string\" },\n      \"languages\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"eng\": { \"type\": \"string\" },\n          \"urd\": { \"type\": \"string\" }\n        },\n        \"required\": [\"eng\", \"urd\"]\n      },\n      \"translations\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"ara\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"bre\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"ces\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"cym\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"deu\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"est\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"fin\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"fra\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"hrv\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"hun\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"ita\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"jpn\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"kor\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"nld\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"per\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"pol\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"por\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"rus\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"slk\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"spa\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"srp\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"swe\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"tur\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"urd\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          },\n          \"zho\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"official\": { \"type\": \"string\" },\n              \"common\": { \"type\": \"string\" }\n            },\n            \"required\": [\"official\", \"common\"]\n          }\n        }\n      },\n      \"latlng\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"number\" }\n      },\n      \"landlocked\": { \"type\": \"boolean\" },\n      \"borders\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"area\": { \"type\": \"number\" },\n      \"demonyms\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"eng\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"f\": { \"type\": \"string\" },\n              \"m\": { \"type\": \"string\" }\n            },\n            \"required\": [\"f\", \"m\"]\n          },\n          \"fra\": {\n            \"type\": \"object\",\n            \"properties\": {\n              \"f\": { \"type\": \"string\" },\n              \"m\": { \"type\": \"string\" }\n            },\n            \"required\": [\"f\", \"m\"]\n          }\n        }\n      },\n      \"flag\": { \"type\": \"string\" },\n      \"maps\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"googleMaps\": { \"type\": \"string\" },\n          \"openStreetMaps\": { \"type\": \"string\" }\n        }\n      },\n      \"population\": { \"type\": \"integer\" },\n      \"gini\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"2018\": { \"type\": \"number\" }\n        }\n      },\n      \"fifa\": { \"type\": \"string\" },\n      \"car\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"signs\": {\n            \"type\": \"array\",\n            \"items\": { \"type\": \"string\" }\n          },\n          \"side\": { \"type\": \"string\" }\n        }\n      },\n      \"timezones\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"continents\": {\n        \"type\": \"array\",\n        \"items\": { \"type\": \"string\" }\n      },\n      \"flags\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"png\": { \"type\": \"string\" },\n          \"svg\": { \"type\": \"string\" },\n          \"alt\": { \"type\": \"string\" }\n        }\n      },\n      \"coatOfArms\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"png\": { \"type\": \"string\" },\n          \"svg\": { \"type\": \"string\" }\n        }\n      },\n      \"startOfWeek\": { \"type\": \"string\" },\n      \"capitalInfo\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"latlng\": {\n            \"type\": \"array\",\n            \"items\": { \"type\": \"number\" }\n          }\n        }\n      },\n      \"postalCode\": {\n        \"type\": \"object\",\n        \"properties\": {\n          \"format\": { \"type\": \"string\" },\n          \"regex\": { \"type\": \"string\" }\n        }\n      }\n    },\n    \"required\": [\n      \"name\",\n      \"tld\",\n      \"cca2\",\n      \"ccn3\",\n      \"cca3\",\n      \"cioc\",\n      \"independent\",\n      \"status\",\n      \"unMember\",\n      \"currencies\",\n      \"idd\",\n      \"capital\",\n      \"altSpellings\",\n      \"region\",\n      \"subregion\",\n      \"languages\",\n      \"translations\",\n      \"latlng\",\n      \"landlocked\",\n      \"borders\",\n      \"area\",\n      \"demonyms\",\n      \"flag\",\n      \"maps\",\n      \"population\",\n      \"gini\",\n      \"fifa\",\n      \"car\",\n      \"timezones\",\n      \"continents\",\n      \"flags\",\n      \"coatOfArms\",\n      \"startOfWeek\",\n      \"capitalInfo\",\n      \"postalCode\"\n    ]\n  }\n}\n","scope":"RESPONSE_CONTENT"}
      } ],
      "enabled" : true
    } ],
    "comment_required" : false
  } ],
  "metadata" : [ {
    "key" : "email-support",
    "name" : "email-support",
    "format" : "MAIL",
    "value" : "${(api.primaryOwner.email)!''}",
    "defaultValue" : "support@change.me",
    "apiId" : "44407f48-4b26-4c1c-807f-484b264c1c82"
  } ],
  "id" : "44407f48-4b26-4c1c-807f-484b264c1c82",
  "path_mappings" : [ ],
  "proxy" : {
    "virtual_hosts" : [ {
      "path" : "/10-Example/"
    } ],
    "strip_context_path" : false,
    "preserve_host" : false,
    "logging" : {
      "mode" : "CLIENT_PROXY",
      "content" : "HEADERS_PAYLOADS",
      "scope" : "REQUEST_RESPONSE"
    },
    "groups" : [ {
      "name" : "default-group",
      "endpoints" : [ {
        "backup" : false,
        "inherit" : true,
        "name" : "default",
        "weight" : 1,
        "type" : "http",
        "target" : "https://restcountries.com"
      } ],
      "load_balancing" : {
        "type" : "ROUND_ROBIN"
      },
      "http" : {
        "connectTimeout" : 5000,
        "idleTimeout" : 60000,
        "keepAlive" : true,
        "readTimeout" : 10000,
        "pipelining" : false,
        "maxConcurrentConnections" : 100,
        "useCompression" : true,
        "followRedirects" : false
      }
    } ]
  },
  "response_templates" : { },
  "primaryOwner" : {
    "id" : "03d583c3-0bb0-40e7-9583-c30bb040e707",
    "displayName" : "admin",
    "type" : "USER"
  }
}
```
````
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `json-validation` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `json-validation` policy can be configured with the following options:

<table><thead><tr><th width="227">Property</th><th width="112" data-type="checkbox">Required</th><th width="235">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>Policy scope from where the policy is executed</td><td>Policy scope</td><td>REQUEST_CONTENT</td></tr><tr><td>errorMessage</td><td>true</td><td>Custom error message in JSON format. Spel is allowed.</td><td>string</td><td>{"error":"Bad request"}</td></tr><tr><td>schema</td><td>true</td><td>Json schema.</td><td>string</td><td></td></tr><tr><td>deepCheck</td><td>false</td><td>Validate descendant even if JSON parent container is invalid</td><td>boolean</td><td>false</td></tr><tr><td>validateUnchecked</td><td>false</td><td>Unchecked validation means that conditions which would normally cause the processing to stop with an exception are instead inserted into the resulting report. Warning: this means that anomalous events like an unresolvable JSON Reference, or an invalid schema, are masked!.</td><td>boolean</td><td>false</td></tr><tr><td>straightRespondMode</td><td>false</td><td>Only for RESPONSE scope. Straight respond mode means that responses failed to validate still will be sent to user without replacement. Validation failures messages are still being written to the metrics for further inspection.</td><td>boolean</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `json-validation` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>400</code></td><td><p>Invalid payload</p><p>Invalid JSON schema</p><p>Invalid error message JSON format</p></td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td><p>Invalid payload</p><p>Invalid JSON schema</p><p>Invalid error message JSON format</p></td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The policy sends the following error keys:

<table data-full-width="false"><thead><tr><th width="355.6456692913386">Key</th><th width="171">Parameters</th></tr></thead><tbody><tr><td>JSON_INVALID_PAYLOAD</td><td>-</td></tr><tr><td>JSON_INVALID_FORMAT</td><td>-</td></tr><tr><td>JSON_INVALID_RESPONSE_PAYLOAD</td><td>-</td></tr><tr><td>JSON_INVALID_RESPONSE_FORMAT</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-validation/blob/master/CHANGELOG.md" %}
