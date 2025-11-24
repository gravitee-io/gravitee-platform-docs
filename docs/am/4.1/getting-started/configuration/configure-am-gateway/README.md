---
description: Configuration guide for Configure AM Gateway.
---

# Configure AM Gateway

## Overview

There are three different ways to configure AM Gateway components. These are:

* environment variables
* system properties
* `gravitee.yml`

The order in which they are listed above corresponds to their order of precedence. In other words, environment variables override the other two configuration types, and system properties override `gravitee.yml`.

### gravitee.yml

The `gravitee.yml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure AM.

{% hint style="info" %}
YAML (`yml`) format is very sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

### System properties

You can override the default AM configuration (`gravitee.yml`) by defining system properties.

To override this property:

{% code title="gravitee.yml" %}
```yaml
management:
  mongodb:
    dbname: myDatabase
```
{% endcode %}

Add this property to the JVM:

```yaml
-Dmanagement.mongodb.dbname=myDatabase
```

### Environment variables

You can override the default AM configuration (`gravitee.yml`) and system properties by defining environment variables.

To override this property:

{% code title="gravitee.yml" %}
```yaml
management:
  mongodb:
    dbname: myDatabase
```
{% endcode %}

Define one of the following variables:

{% code title="Environment variables" %}
```
GRAVITEE_MANAGEMENT_MONGODB_DBNAME=myDatabase
GRAVITEE.MANAGEMENT.MONGODB.DBNAME=myDatabase
gravitee_management_mongodb_dbname=myDatabase
gravitee.management.mongodb.dbname=myDatabase
```
{% endcode %}

Some properties are case-sensitive and cannot be written in uppercase (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`. We advise you to define environment variables in lowercase and use the correct syntax for each property.

{% hint style="info" %}
In some systems, hyphens are not allowed in variable names. For example, you may need to write `gravitee_http_cookie_allow-credentials` as `gravitee_http_cookie_allowcredentials` .
{% endhint %}

#### **How to manage arrays?**

Some properties are arrays. For example:

{% code title="gravitee.yml" %}
```yaml
http:
  ssl:
    endpoints:
      - token_endpoint
      - registration_endpoint

security:
  providers:
    - type: ldap
      context-source-username: "cn=Directory Manager"
      context-source-password: "password"
```
{% endcode %}

Below are some examples of how to write your environment variables. In case of doubt, we recommend you try both.

{% code title="" %}
```
gravitee_http_ssl_endpoints_0=token_endpoint
gravitee_http_ssl_endpoints_1=registration_endpoint

gravitee_security_providers_0_type=ldap
gravitee_security_providers_0_context-source-username=cn=Directory Manager
gravitee_security_providers_0_context-source-password=password
```
{% endcode %}

or

{% code title="Environment variables" %}
```
gravitee.http.ssl.endpoints[0]=token_endpoint
gravitee.http.ssl.endpoints[1]=registration_endpoint

gravitee.security.providers[0]type=ldap
gravitee.security.providers[0]context-source-username=cn=Directory Manager
gravitee.security.providers[0]context-source-password=password
gravitee.security.providers[0].users[1].password=password
```
{% endcode %}

## Detailed `gravitee.yml` configuration

### Configure HTTP server

You can update the HTTP server configuration in the following section of the `gravitee.yml` file.

{% code title="gravitee.yml" %}
```yaml
http:
  port: 8092
  idleTimeout: 0
  tcpKeepAlive: true
  compressionSupported: false
  pool:
    workers: 100
  secured: false
  ssl:
    clientAuth: false
    keystore:
      path:
      password:
    truststore:
      path:
      password:
```
{% endcode %}

### **Enable HTTPS support**

First, you need to provide a keystore. If you don’t have one, you can generate it:

```sh
keytool -genkey \
  -alias test \
  -keyalg RSA \
  -keystore server-keystore.jks \
  -keysize 2048 \
  -validity 360 \
  -dname CN=localhost \
  -keypass secret \
  -storepass secret
```

You then need to enable secure mode in `gravitee.yml`:

{% code title="gravitee.yml" %}
```yaml
http:
  port: 8092
  idleTimeout: 0
  tcpKeepAlive: true
  compressionSupported: false
  instances: 0
  secured: true
  ssl:
    clientAuth: false
    keystore:
      path: /path/to/keystore.jks
      password: secret
    truststore:
      path:
      password:
```
{% endcode %}

### Configure email

{% code title="gravitee.yml" %}
```yaml
# SMTP configuration used to send mails
email:
  enabled: false
  host: smtp.my.domain
  subject: "[Gravitee.io] %s"
  port: 587
  from: noreply@my.domain
  username: user@my.domain
  password: password
#  properties:
#    auth: true
#    starttls.enable: true
#    ssl.trust: smtp.gmail.com
#    ssl.protocols: TLSv1.2

# Mail templates
#templates:
#  path: ${gravitee.home}/templates
```
{% endcode %}

{% hint style="info" %}
In order to enforce TLS 1.2 uncomment the properties in the above example and change according to your requirements.
{% endhint %}

#### **Email password and name complexity**

You can configure the complexities as per your organizational requirements. The default settings is shown below:

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
user:
  email:
    policy:
      pattern: ^[a-zA-Z0-9_+-]+(?:\.[a-zA-Z0-9_+-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$
  # Password complexity validation policy
  # Applications should enforce password complexity rules to discourage easy to guess passwords.
  # Passwords should require a minimum level of complexity that makes sense for the application and its user population.
  password:
    policy:
      # Regex pattern for password validation (default to OWASP recommendations).
      # 8 to 32 characters, no more than 2 consecutive equal characters, min 1 special characters (@ & # ...), min 1 upper case character.
      pattern: ^(?:(?=.*\d)(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[a-z])|(?=.*[^A-Za-z0-9])(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[A-Z])(?=.*[^A-Za-z0-9]))(?!.*(.)\1{2,})[A-Za-z0-9!~<>,;:_\-=?*+#."'&§`£€%°()\\\|\[\]\-\$\^\@\/]{8,32}$
        # Example : ^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$
        # ^                # start-of-string
        #(?=.*[0-9])       # a digit must occur at least once
        #(?=.*[a-z])       # a lower case letter must occur at least once
        #(?=.*[A-Z])       # an upper case letter must occur at least once
        #(?=.*[@#$%^&+=])  # a special character must occur at least once
        #(?=\S+$)          # no whitespace allowed in the entire string
        #.{8,}             # anything, at least eight places though
        #$                 # end-of-string

      ## Password dictionary to exclude most commons passwords
      ## You need to enable the feature in the AM Management Console

      #dictionary:
      #  filename: /path/to/dictionary  # if null `resources/dictionaries/10k-most-common.txt` will be loaded
      #  watch: true #if true, watches periodically for any changes in the file
  name:
    strict:
      policy:
        pattern: ^[^±!@£$%^&*_+§¡€#¢¶•ªº«»\\/<>?:;|=.,]{0,100}$
    lax:
      policy:
        pattern: ^[^±!£$%^&*§¡€¢¶•ªº«»\\/<>?|=]{0,100}$
  username:
    policy:
      pattern: ^[^±!£$%^&*§¡€¢¶•ªº«»\\/<>?:;|=,]{1,100}$
```
{% endcode %}

### Configure the Plugins repository

Gravitee AM Gateway plugins directory configuration.

```yaml
plugins:
  path: ${gravitee.home}/plugins
```

### Configure the Management repository

Management repository is used to store global configurations such as security domains, clients, tokens, users, etc. ​This is the default configuration using MongoDB (single server).

{% code title="gravitee.yml" %}
```yaml
management:
  type: mongodb
  mongodb:
    dbname: ${ds.mongodb.dbname}
    host: ${ds.mongodb.host}
    port: ${ds.mongodb.port}
#    username:
#    password:
#    connectionsPerHost: 0
#    connectTimeout: 500
#    maxWaitTime: 120000
#    socketTimeout: 500
#    socketKeepAlive: false
#    maxConnectionLifeTime: 0
#    maxConnectionIdleTime: 0
#    serverSelectionTimeout: 0
#    description: gravitee.io
#    heartbeatFrequency: 10000
#    minHeartbeatFrequency: 500
#    heartbeatConnectTimeout: 1000
#    heartbeatSocketTimeout: 20000
#    localThreshold: 15
#    minConnectionsPerHost: 0
#    sslEnabled: false
#    threadsAllowedToBlockForConnectionMultiplier: 5
#    cursorFinalizerEnabled: true
#    keystore:
#    keystorePassword:
#    keyPassword

# Management repository: single MongoDB using URI
# For more information about MongoDB configuration using URI, please have a look to:
# - http://api.mongodb.org/java/current/com/mongodb/MongoClientURI.html
#management:
#  type: mongodb
#  mongodb:
#    uri: mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

# Management repository: clustered MongoDB
#management:
#  type: mongodb
#  mongodb:
#    servers:
#      - host: mongo1
#        port: 27017
#      - host: mongo2
#        port: 27017
#    dbname: ${ds.mongodb.dbname}
#    connectTimeout: 500
#    socketTimeout: 250
```
{% endcode %}
