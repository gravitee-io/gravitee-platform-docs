# APIM 4.9 Elasticsearch Index Template Changes

APIM 4.9 introduces new analytics capabilities that require Elasticsearch index template updates:

* [V2 and V4 API Analytics Templates:](apim-4.9-elasticsearch-index-template-changes.md#template-changes-for-v2-and-v4-apis) Enhanced error component tracking and warning metrics for REST API analytics.
* [Kafka Metrics Templates:](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-index-templates-for-kafka-metrics) Time-series templates for event-driven API metrics.&#x20;

## **Template Changes for V2 and V4 APIs**

Elasticsearch index template mappings have been updated to support execution transparency analytics. These changes apply to both v2 API metrics and v4 API metrics for Elasticsearch `7.x` and `8.x`.&#x20;

{% hint style="warning" %}
When using the Elasticsearch reporter, APIM handles these template updates automatically during upgrade. If you manage templates independently, apply these updates manually before upgrading.
{% endhint %}

Add the following fields to your existing templates to enable error component and warning tracking:

1. [#elasticsearch-7.x-v2-request-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-7.x-v2-request-template "mention")
2. [#elasticsearch-7.x-v4-metrics-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-7.x-v4-metrics-template "mention")
3. [#elasticsearch-8.x-v2-request-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-8.x-v2-request-template "mention")
4. [#elasticsearch-8.x-v4-metrics-template](apim-4.9-elasticsearch-index-template-changes.md#elasticsearch-8.x-v4-metrics-template "mention")

### Elasticsearch 7.x V2 Request Template

For the Elasticsearch `7.x` V2 Request Template, use the following field mappings:

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

### Elasticsearch 7.x V4 Metrics Template&#x20;

For the Elasticsearch `7.x` V4 Metrics Template, use the following field mappings:

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

### Elasticsearch 8.x V2 Request Template&#x20;

For the Elasticsearch `8.x` V2 Request Template, use the following field mappings:

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

### Elasticsearch 8.x V4 Metrics Template&#x20;

For the Elasticsearch `8.x` V4 Metrics Template, use the following field mappings:

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

**Error Component Fields**

* `error-component-type`: Identifies the type of component that caused an error.
* `error-component-name`: Identifies the specific component instance that caused an error.

**Warnings Field** \
A nested array structure for capturing multiple warnings per request:

* `warnings.key`: Warning identifier.
* `warnings.message`: Warning description.
* `warnings.component-type`: Component type that generated the warning.
* `warnings.component-name`: Component name that generated the warning.

## Elasticsearch Index Templates for Kafka Metrics

Elasticsearch index templates have been introduced for storing Kafka Gateway metrics. These templates define the structure and settings for time-series data:

### Elasticsearch 7.x Template&#x20;

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

### Elasticsearch 8.x Template

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

