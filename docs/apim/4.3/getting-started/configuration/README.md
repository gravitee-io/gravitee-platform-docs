---
description: Learn how to configure various Gravitee API Management components
---

# Configuration

## Introduction

APIM components can be configured using:

1. Environment variables
2. System properties
3. The `gravitee.yaml` file

{% hint style="warning" %}
The order in which they are listed corresponds to their order of precedence. System properties override the `gravitee.yml` configuration and environment variables override all other configuration methods.
{% endhint %}

## Environment variables

You can override the default APIM configuration (`gravitee.yml`) and system properties by defining environment variables. Any property in the `yaml` file can be translated to an environment variable by prefixing the property with "gravitee" and using `camel_case` or dot notation.

{% hint style="warning" %}
Certain properties are case-sensitive and cannot use uppercase characters. We recommend using lowercase characters to define all Gravitee environment variables. To ensure compatibility and avoid or confusion, refer to your system documentation for environment variable naming best practices.
{% endhint %}

<details>

<summary>Environment variable override examples</summary>

#### Example 1

To override this property:

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

#### Example 2

Some properties are arrays:

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

</details>

## System properties

You can override the default APIM configuration (`gravitee.yml`) by defining system properties.

<details>

<summary>System property override example</summary>

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

</details>

## The `gravitee.yaml` file

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
YAML format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}
