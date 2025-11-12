---
description: >-
  This page provides the technical details of the Rate Limit policy in Access
  Management
---

# Rate Limit Policy

## **Overview**

A Rate Limit policy configures the number of requests allowed over a limited period of time.

For any [`rate-limit` policy](../../../../../apim/4.3/reference/policy-reference/rate-limit.md), you can select the option to ignore the IP address and only use a custom key for the quota. You can then share an API's rate limit calculations across machines to enforce the limit, regardless of caller IP. If you use a custom key, the quota increments after each call to the API, across multiple hosts.

To dynamically set the custom key, you can define it using Gravitee Expression Language (EL).

{% hint style="warning" %}
An arbitrary custom key can be incorrectly defined via Gravitee EL, and then potentially bypass the constraints of this mechanism to impact the quota of a different user. Users must assess this risk when  using custom keys.
{% endhint %}

### Repository Configuration

You can configure the rate limit repository to store the rate limit data in MongoDB, Postgres, or Redis (recommended).&#x20;

You can define the rate limit data store either in your `gravitee.yml` file or via environment variables.

{% hint style="info" %}
If no configuration values are provided for the rate limit repository, it falls back to the repository implementation used by the Gateway. For example, if the Gateway uses Postgres, the rate limit repository uses Postgres.
{% endhint %}

To set the rate limit repository using `gravitee.yml`, choose one of the following configuration options:

{% tabs %}
{% tab title="Redis" %}
The following `gravitee.yml` configuration uses Redis to store rate limit data:

```yaml
repositories:
    ratelimit:
        type: redis
        redis:
            host: my.redis
            port: 6397
            password: 'compl3xPa$$`
```
{% endtab %}

{% tab title="Mongo" %}
The following `gravitee.yml` configuration uses MongoDB to store rate limit data:

```yaml
repositories:  
  ratelimit:
    type: mongodb
    mongodb:
      dbname: gravitee-am
      host: localhost
      port: 27017
```
{% endtab %}

{% tab title="R2DBC" %}
The following `gravitee.yml` configuration uses R2DBC to store rate limit data:

```yaml
repositories:  
  ratelimit:
    type: jdbc
    jdbc:
      driver: postgresql
      database: gravitee
      username: admin
      password: pass
      host: localhost
      port: 5432
```
{% endtab %}
{% endtabs %}

To set the rate limit repository using environment variables, choose one of the following configuration options:

{% tabs %}
{% tab title="Redis" %}
```
GRAVITEE_REPOSITORIES_RATELIMIT_TYPE=redis
GRAVITEE_REPOSITORIES_RATELIMIT_REDIS_HOST=my.redis
GRAVITEE_REPOSITORIES_RATELIMIT_REDIS_PORT=6397
GRAVITEE_REPOSITORIES_RATELIMIT_REDIS_PASSWORD='compl3xPa$$'
```
{% endtab %}

{% tab title="MongoDB" %}
```
GRAVITEE_REPOSITORIES_RATELIMIT_TYPE=mongodb
GRAVITEE_REPOSITORIES_RATELIMIT_MONGODB_DBNAME=gravitee-am
GRAVITEE_REPOSITORIES_RATELIMIT_MONGODB_HOST=localhost
GRAVITEE_REPOSITORIES_RATELIMIT_MONGODB_PORT=27017
```
{% endtab %}

{% tab title="R2DBC" %}
```
GRAVITEE_REPOSITORIES_RATELIMIT_TYPE=jdbc
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_DRIVER=postgresql
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_DATABASE=gravitee
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_USERNAME=admin
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_PASSWORD=pass
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_HOST=localhost
GRAVITEE_REPOSITORIES_RATELIMIT_JDBC_PORT=5432
```
{% endtab %}
{% endtabs %}

### Rate Limit

The Rate Limit policy configures the number of requests allowed over a limited period of time. This policy does not prevent request spikes.

<table><thead><tr><th width="146.73828125">Property</th><th width="113.36328125" data-type="checkbox">Required</th><th width="408.46875">Description</th><th>Type</th></tr></thead><tbody><tr><td>key</td><td>false</td><td>Key to identify a consumer to apply rate-limiting against. Leave it empty to use the default behavior . Supports Expression Language.</td><td>String</td></tr><tr><td>limit</td><td>false</td><td>Static limit on the number of requests that can be sent (this limit is used if the value > 0).</td><td>Integer</td></tr><tr><td>dynamicLimit</td><td>false</td><td>Dynamic limit on the number of requests that can be sent (this limit is used if static limit = 0). The dynamic value is based on Expression Language expressions.</td><td>String</td></tr><tr><td>periodTime</td><td>true</td><td>Time duration</td><td>Integer</td></tr><tr><td>periodTimeUnit</td><td>true</td><td>Time unit ("SECONDS", "MINUTES" )</td><td>String</td></tr></tbody></table>

### Rate limited flow example

The following example shows how to configure the Pre-Token flow with a rate limit. The rate limit returns an error if the requesting resource has called the endpoint 5 times in the last 1 minute.

```json
   {
        "id": "{{token-id}}",
        "name": "TOKEN",
        "pre": [
            {
                "name": "Rate Limit",
                "policy": "rate-limit",
                "description": "",
                "configuration": "{\"async\":false,\"addHeaders\":true,\"rate\":{\"useKeyOnly\":true,\"periodTime\":1,\"periodTimeUnit\":\"MINUTES\",\"key\":\"abcd\",\"limit\":5,\"dynamicLimit\":\"5\"}}",
                "enabled": true,
                "condition": ""
            }
        ],
        "post": [],
        "enabled": true,
        "type": "token"
    },
```

### Errors

When the rate limit threshold is reached, the requesting client receives an error. The Rate Limit policy sends the following error key:

<table><thead><tr><th width="339.1015625">Key</th><th width="278.58984375">Parameters</th><th>Status Code</th></tr></thead><tbody><tr><td>RATE_LIMIT_TOO_MANY_REQUESTS</td><td>limit - period_time - period_unit</td><td>429</td></tr></tbody></table>
