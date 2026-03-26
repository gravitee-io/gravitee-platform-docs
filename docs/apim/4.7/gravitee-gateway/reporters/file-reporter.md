---
description: Configuration and setup guide for file reporter.
---

# File Reporter

## Configuration

The file reporter has the following configuration parameters:

<table><thead><tr><th width="181">Parameter name</th><th width="248.28246753246754">Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>enabled</code></td><td>This setting determines whether the file reporter should be started or not. The default value is <code>false</code>.</td><td>false</td></tr><tr><td><code>fileName</code></td><td>The path events should be written to. Use the <code>%s-yyyy_mm_dd</code> pattern to create one file per event type on a daily basis.</td><td>#{systemProperties['gravitee.home']}/metrics/%s-yyyy_mm_dd}</td></tr><tr><td><code>output</code></td><td>Output file type - json, message_pack, elasticsearch, csv.</td><td>json</td></tr><tr><td><code>flushInterval</code></td><td>File flush interval (in ms).</td><td>1000</td></tr><tr><td><code>retainDays</code></td><td>The number of days to retain files before deleting one.</td><td>0 (to retain forever)</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.exclude</code></td><td>Fields to exclude from the output. Available for <code>json</code> and <code>message_pack</code> outputs only.</td><td>none</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.include</code></td><td>Fields to include in the output. Available for <code>json</code> and <code>message_pack</code> outputs and only if excludes have been defined.</td><td>none</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.rename</code></td><td>Fields to rename when writing the output. Available for <code>json</code> and <code>message_pack</code> outputs only.</td><td>none</td></tr></tbody></table>

{% hint style="info" %}
\<EVENT\_TYPE> refers to the kind of event reported by the Gateway and can be either `request`, `log`, `node` or `health-check`. Fields referenced as `exclude`, `include` and `rename` items all support [jsonPath](https://github.com/json-path/JsonPath) for accessing nested elements.
{% endhint %}

## Example

The configuration example below excludes all fields from the request JSON file except the `api` and `application` fields, renames the `application` field to `app`, and excludes `log`, `node`, and `health-check` events from being reported:

```yaml
reporters:
  file:
    enabled: true
    fileName: ${gravitee.home}/metrics/%s-yyyy_mm_dd
    output: json
    request:
      exclude:
        - "*"
      include:
        - api
        - application
      rename:
        application: app
    log:
      exclude:
        - "*"
    node:
      exclude:
        - "*"
    health-check:
      exclude:
        - "*"
```
