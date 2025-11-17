# APIM 4.9 Elasticsearch Index Template Changes

## Overview

APIM 4.9 enables new analytics capabilities via the following Elasticsearch index templates:

* [v2 and v4 API analytics templates](apim-4.9-elasticsearch-index-template-changes.md#template-changes-for-v2-and-v4-apis) now contain enhanced error component tracking and warning metrics for REST API analytics.
* [Kafka metrics templates](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-index-templates-for-kafka-metrics) are new time-series templates for event-driven API metrics.&#x20;

## **Template updates for v2 and v4 APIs**

Elasticsearch index template mappings have been updated to support execution transparency analytics. These changes apply to both v2 API metrics and v4 API metrics for Elasticsearch 7.x and 8.x.&#x20;

{% hint style="warning" %}
If you are using the Elasticsearch reporter, APIM automatically performs these template updates during the upgrade. If you manage templates independently, apply these updates manually before upgrading.
{% endhint %}

Add the following fields to your existing templates to enable error component and warning tracking:

1. [#elasticsearch-7.x-v2-request-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-7.x-v2-request-template "mention")
2. [#elasticsearch-7.x-v4-metrics-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-7.x-v4-metrics-template "mention")
3. [#elasticsearch-8.x-v2-request-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-8.x-v2-request-template "mention")
4. [#elasticsearch-8.x-v4-metrics-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-8.x-v4-metrics-template "mention")

### Elasticsearch 7.x v2 Request Template

For the Elasticsearch 7.x v2 Request Template, use the following field mappings:

```json
"error-component-type": {
      "type": "keyword",
      "index": true
  },
  "error-component-name": {
      "type": "keyword",
      "index": true
  },
  "warnings": {
      "type": "nested",
      "properties": {
          "key": {
              "type": "keyword",
              "index": true
          },
          "message": {
              "type": "text"
          },
          "component-type": {
              "type": "keyword",
              "index": true
          },
          "component-name": {
              "type": "keyword",
              "index": true
          }
      }
  }
```

### Elasticsearch 7.x v4 Metrics Template&#x20;

For the Elasticsearch 7.x v4 Metrics Template, use the following field mappings:

```json
"error-component-type": {
      "type": "keyword",
      "index": true
  },
  "error-component-name": {
      "type": "keyword",
      "index": true
  },
  "warnings": {
      "type": "nested",
      "properties": {
          "key": {
              "type": "keyword",
              "index": true
          },
          "message": {
              "type": "text"
          },
          "component-type": {
              "type": "keyword",
              "index": true
          },
          "component-name": {
              "type": "keyword",
              "index": true
          }
      }
  }
```

### Elasticsearch 8.x v2 Request Template&#x20;

For the Elasticsearch 8.x v2 Request Template, use the following field mappings:

```json
"error-component-type": {
      "type": "keyword",
      "index": true
  },
  "error-component-name": {
      "type": "keyword",
      "index": true
  },
  "warnings": {
      "type": "nested",
      "properties": {
          "key": {
              "type": "keyword",
              "index": true
          },
          "message": {
              "type": "text"
          },
          "component-type": {
              "type": "keyword",
              "index": true
          },
          "component-name": {
              "type": "keyword",
              "index": true
          }
      }
  }
```

### Elasticsearch 8.x v4 Metrics Template&#x20;

For the Elasticsearch 8.x v4 Metrics Template, use the following field mappings:

```json
"error-component-type": {
      "type": "keyword",
      "index": true
  },
  "error-component-name": {
      "type": "keyword",
      "index": true
  },
  "warnings": {
      "type": "nested",
      "properties": {
          "key": {
              "type": "keyword",
              "index": true
          },
          "message": {
              "type": "text"
          },
          "component-type": {
              "type": "keyword",
              "index": true
          },
          "component-name": {
              "type": "keyword",
              "index": true
          }
      }
  }
```

### Field Description&#x20;

The following fields are added to the templates:

**Error component fields**

* `error-component-type`: Component type that caused the error.
* `error-component-name`: Specific component instance that caused the error.

**Warnings field** \
The warnings field is a nested array structure for capturing multiple warnings per request.

* `warnings.key`: Warning identifier.
* `warnings.message`: Warning description.
* `warnings.component-type`: Component type that generated the warning.
* `warnings.component-name`: Component name that generated the warning.

## Elasticsearch index templates for Kafka metrics

Elasticsearch index templates have been introduced to store Kafka Gateway metrics. These templates define the structure and settings to use for time series data.

### Elasticsearch 7.x template&#x20;

For Elasticsearch 7.x, use the following index template:

```json
{
      "index_patterns": ["${indexName}*"],
      "settings": {
          "index.lifecycle.name": "event-metrics-ilm-policy"
      },
      "mappings": {
          "properties": {
              "gw-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "org-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "env-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "api-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "plan-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "app-id": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "topic": {
                  "type": "keyword",
                  "time_series_dimension": true
              },
              "downstream-publish-messages-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "downstream-publish-message-bytes": {
                  "type": "long",
                  "time_series_metric": "counter"
              },
              "upstream-publish-messages-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "upstream-publish-message-bytes": {
                  "type": "long",
                  "time_series_metric": "counter"
              },
              "downstream-subscribe-messages-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "downstream-subscribe-message-bytes": {
                  "type": "long",
                  "time_series_metric": "counter"
              },
              "upstream-subscribe-messages-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "upstream-subscribe-message-bytes": {
                  "type": "long",
                  "time_series_metric": "counter"
              },
              "downstream-active-connections": {
                  "type": "integer",
                  "time_series_metric": "gauge"
              },
              "upstream-active-connections": {
                  "type": "integer",
                  "time_series_metric": "gauge"
              },
              "upstream-authenticated-connections": {
                  "type": "integer",
                  "time_series_metric": "gauge"
              },
              "downstream-authenticated-connections": {
                  "type": "integer",
                  "time_series_metric": "gauge"
              },
              "downstream-authentication-failures-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "upstream-authentication-failures-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "downstream-authentication-successes-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "upstream-authentication-successes-total": {
                  "type": "integer",
                  "time_series_metric": "counter"
              },
              "@timestamp": {
                  "type": "date"
              }
          }
      }
  }
```

### Elasticsearch 8.x template

For Elasticsearch 8.x, use the following data stream template:

```json
{
      "index_patterns": ["${indexName}*"],
      "data_stream": {},
      "template": {
          "settings": {
              "index.mode": "time_series",
              "index.lifecycle.name": "event-metrics-ilm-policy"
          },
          "mappings": {
              "properties": {
                  "gw-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "org-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "env-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "api-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "plan-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "app-id": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "topic": {
                      "type": "keyword",
                      "time_series_dimension": true
                  },
                  "downstream-publish-messages-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "downstream-publish-message-bytes": {
                      "type": "long",
                      "time_series_metric": "counter"
                  },
                  "upstream-publish-messages-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "upstream-publish-message-bytes": {
                      "type": "long",
                      "time_series_metric": "counter"
                  },
                  "downstream-subscribe-messages-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "downstream-subscribe-message-bytes": {
                      "type": "long",
                      "time_series_metric": "counter"
                  },
                  "upstream-subscribe-messages-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "upstream-subscribe-message-bytes": {
                      "type": "long",
                      "time_series_metric": "counter"
                  },
                  "downstream-active-connections": {
                      "type": "integer",
                      "time_series_metric": "gauge"
                  },
                  "upstream-active-connections": {
                      "type": "integer",
                      "time_series_metric": "gauge"
                  },
                  "upstream-authenticated-connections": {
                      "type": "integer",
                      "time_series_metric": "gauge"
                  },
                  "downstream-authenticated-connections": {
                      "type": "integer",
                      "time_series_metric": "gauge"
                  },
                  "downstream-authentication-failures-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "upstream-authentication-failures-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "downstream-authentication-successes-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "upstream-authentication-successes-total": {
                      "type": "integer",
                      "time_series_metric": "counter"
                  },
                  "@timestamp": {
                      "type": "date"
                  }
              }
          }
      },
      "priority": 9344593,
      "_meta": {
          "description": "Template for event metrics time series data stream"
      }
  }
```
