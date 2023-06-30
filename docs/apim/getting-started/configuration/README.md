---
description: Learn how to configure various Gravitee API Management components
---

# Configuration

## Introduction

This guide explains how to configure all of the core aspects of Gravitee API Management (APIM) after installation including, but not limited to, the four main components:

* APIM Gateway
* APIM Management API
* APIM Console
* APIM Developer Portal

## Configuring APIM components

You can configure APIM's four components using three methods:

* Environment variables
* System properties&#x20;
* The `gravitee.yaml` file

{% hint style="info" %}
**Hierarchies**

The order in which they are listed above corresponds to their order of precedence. In other words, system properties override the `gravitee.yml` configuration and environment variables override all other configuration methods.
{% endhint %}

### Environment variables

You can override the default APIM configuration (`gravitee.yml`) and system properties by defining environment variables. You can translate any property in the `yaml` file to an environment variable by prefixing the property with "gravitee" and using `camel_case` or dot notation.

Some properties are case-sensitive and cannot be written in uppercase (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`). Therefore, we advise you to define all Gravitee environment variables in lowercase.

For example, to override this property:

```yaml
management:
  mongodb:
    dbname: myDatabase
```

Define one of the following variables:

```
gravitee_management_mongodb_dbname=myDatabase
gravitee.management.mongodb.dbname=myDatabase
```

{% hint style="info" %}
In some systems, hyphens are not allowed in variable names. For example, you may need to write `gravitee_policy_api-key_header` as `gravitee_policy_apikey_header`. We recommend you check your system documentation.
{% endhint %}

Some properties are arrays like the example below:

```yaml
analytics:
  elasticsearch:
    endpoints:
      - https://my.first.endpoint.com
      - https://my.second.endpoint.com

security:
  providers:
    - type: ldap
      context-source-username: "cn=Directory Manager"
      context-source-password: "password"
```

To translate and override, define one of the following variables:

**`camel_case`**

```
gravitee_analytics_elasticsearch_endpoints_0=https://my.first.endpoint.com
gravitee_analytics_elasticsearch_endpoints_1=https://my.second.endpoint.com

gravitee_security_providers_0_type=ldap
gravitee_security_providers_0_contextsourceusername=cn=Directory Manager
gravitee_security_providers_0_contextsourcepassword=password
```

**Dot notation**

```
gravitee.analytics.elasticsearch.endpoints[0]=https://my.first.endpoint.com
gravitee.analytics.elasticsearch.endpoints[1]=https://my.second.endpoint.com

gravitee.security.providers[0]type=ldap
gravitee.security.providers[0]context-source-username=cn=Directory Manager
gravitee.security.providers[0]context-source-password=password
gravitee.security.providers[0].users[1].password=password
```

### System properties

You can also override the default APIM configuration (`gravitee.yml`) by defining system properties.

To override this property:

```yaml
management:
  mongodb:
    dbname: myDatabase
```

Add this property to the JVM:

```
-Dmanagement.mongodb.dbname=myDatabase
```

### The `gravitee.yaml` file

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td></td><td>APIM Gateway</td><td></td></tr><tr><td></td><td>APIM Management API</td><td></td></tr><tr><td></td><td>APIM Console</td><td></td></tr><tr><td></td><td>APIM Developer Portal</td><td></td></tr><tr><td></td><td>Repositories</td><td></td></tr><tr><td></td><td>Notifications</td><td></td></tr><tr><td></td><td>Reporters</td><td></td></tr><tr><td></td><td>Cache</td><td></td></tr><tr><td></td><td>HTTP Reverse Proxy</td><td></td></tr><tr><td></td><td>Authentication</td><td></td></tr><tr><td></td><td>Production-ready APIM Environment</td><td></td></tr></tbody></table>
