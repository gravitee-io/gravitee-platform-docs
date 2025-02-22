# AM Gateway

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
repositories:
  management:
    mongodb:
      dbname: myDatabase
```
{% endcode %}

Add this property to the JVM:

```yaml
-Dmanagement.repositories.mongodb.dbname=myDatabase
```

### Environment variables

You can override the default AM configuration (`gravitee.yml`) and system properties by defining environment variables.

To override this property:

{% code title="gravitee.yml" %}
```yaml
repositories:
  management:
    mongodb:
      dbname: myDatabase
```
{% endcode %}

Define one of the following variables:

{% code title="Environment variables" %}
```
GRAVITEE_REPOSITORIES_MANAGEMENT_MONGODB_DBNAME=myDatabase
GRAVITEE.REPOSITORIES.MANAGEMENT.MONGODB.DBNAME=myDatabase
gravitee_repositories_management_mongodb_dbname=myDatabase
gravitee.repositories.management.mongodb.dbname=myDatabase
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
repositories:
  management:
    type: mongodb
    mongodb:
      dbname: ${ds.mongodb.dbname}
      host: ${ds.mongodb.host}
      port: ${ds.mongodb.port}
#      username:
#      password:
#      connectionsPerHost: 0
#      connectTimeout: 500
#      maxWaitTime: 120000
#      socketTimeout: 500
#      socketKeepAlive: false
#      maxConnectionLifeTime: 0
#      maxConnectionIdleTime: 0
#      serverSelectionTimeout: 0
#      description: gravitee.io
#      heartbeatFrequency: 10000
#      minHeartbeatFrequency: 500
#      heartbeatConnectTimeout: 1000
#      heartbeatSocketTimeout: 20000
#      localThreshold: 15
#      minConnectionsPerHost: 0
#      sslEnabled: false
#      threadsAllowedToBlockForConnectionMultiplier: 5
#      cursorFinalizerEnabled: true
#      keystore:
#        keystorePassword:
#        keyPassword

# Management repository: single MongoDB using URI
# For more information about MongoDB configuration using URI, please have a look to:
# - http://api.mongodb.org/java/current/com/mongodb/MongoClientURI.html
#repositories:
#  management:
#    type: mongodb
#    mongodb:
#      uri: mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

# Management repository: clustered MongoDB
#repositories:
#  management:
#    type: mongodb
#    mongodb:
#      servers:
#        - host: mongo1
#          port: 27017
#        - host: mongo2
#          port: 27017
#      dbname: ${ds.mongodb.dbname}
#      connectTimeout: 500
#      socketTimeout: 250
```
{% endcode %}

### Configure the client secret hash

As of AM 4.2.0, the client secret can be hashed when stored into the database. Five hash algorithms are supported:

* None (default)
* SHA-256
* SHA-512
* BCrypt
* PBKDF2

To specify which hash algorithm is in used, update the `applications` section of `gravitee.yml`:&#x20;

```yaml
applications:
  secret:
    # Algorithms used to hash the client secret.
    # Can be one of :
    # "PBKDF2", "BCrypt", "SHA-512", "SHA-256", "None"
    algorithm: None
    #properties:
    #  rounds: 4
```

BCrypt and PBKDF2 support additional properties to adapt the strength of the algorithm.

{% hint style="warning" %}
BCrypt and PBKDF2 are designed to be slow to prevent brute force attacks. The AM default properties are based on the OWASP recommendation. If you plan to use one on these algorithms, we strongly recommend that you evaluate the performance impact of the default settings on your environment, then adapt the property values as needed.
{% endhint %}

#### BCrypt properties

The BCrypt algorithm accepts a number of `rounds`. The default value is 10, as recommended by OWASP.

```yaml
applications:
  secret:
    # Algorithms used to hash the client secret.
    # Can be one of :
    # "PBKDF2", "BCrypt", "SHA-512", "SHA-256", "None"
    algorithm: BCrypt
    properties:
      rounds: 8
```

#### PBKDF2 properties

The PBKDF2 algorithm accepts three properties:

* **rounds**: The number of iterations (default: 600000)
* **salt**: The length in bits of the salt value (default: 16)
* **algorithm**: PBKDF2 with the specified pseudo-random function (default: PBKDF2WithHmacSHA25&#x36;**)**

The default values are those recommended by OWASP.

```yaml
applications:
  secret:
    # Algorithms used to hash the client secret.
    # Can be one of :
    # "PBKDF2", "BCrypt", "SHA-512", "SHA-256", "None"
    algorithm: PBKDF2
    properties:
      rounds: 300000
      salt: 16
      algorithm: PBKDF2WithHmacSHA256
```

### Token request response

By default, all additional parameters, except for the following standard parameters are mapped to `/token` response:&#x20;

* `access_token`
* `token_type`
* `expires_in`
* `scope`
* `refresh_token`
* `id_token`

To block adding those parameters to response, specify the block in `gravitee.yml`:

```yaml
handlers:
  oauth2:
    response:
      strict: true
```

### Synchronization process

If a configuration is updated on the AM Console, it needs to be propagated on the AM Gateway instances. To check for an update to a configuration, the AM gateway periodically checks the database to detect new events to synchronize the configuration state. You can configure the synchronization process in `services.sync` section of the `gravitee.yaml` file.

In this section, you specify the frequency of the synchronization process using a cron expression. To save database access during user authentication,  the synchronization process enables the `permissions` option to load Groups and role definitions into the Gateway memory.&#x20;

```yaml
services:
  sync:
    enabled: true
    # sync frequency (default: every 5 seconds)
    cron: */5 * * * * *
    # synchronize groups & roles
    permissions: false
```

### Cache

To reduce the load on database, a cache layer is available to manage user profile linked to a session. When this case is enable, the user profile is persisted into a cache using the identifier preserved into the session. As a consequence each request made on the gateway in a scope of a user session will rely on this cache to retrieve the user profile information.

To use this cache layer, first configure a cache implementation before enabling it under the user section.

{% hint style="info" %}
The cache implementations available within AM are either `standalone` or `redis`.

In development environment with a single AM Gateway you can use standalone without issue but for production environment (or any environment with more than one AM Gateway) please use the redis implementation to share the cache between the gateways.
{% endhint %}

```yaml
# Configure cache implementation
cache:
  type: redis
  redis:
    host: localhost
    port: 6379
    password: ***
    ssl: false
    ## Sentinel mode settings (optional)
    # sentinel:
    #   master: mymaster
    #   password: ***
    #   nodes:
    #     host: host
    #     port: 6379
    ## SSL options  (optional if ssl is false)
    #hostnameVerificationAlgorithm: NONE
    #trustAll: false
    #keystore:
    #  type: PKCS12
    #  path: /path/to/pkcs.12
    #  password: ***
    #  keyPassword: ***
    #  alias: certalias
    #truststore:
    #  type: PKCS12
    #  path: /path/to/pkcs.12
    #  password: ***
    #  alias: certalias
```

Configuring the `cache` section is not enough, the second step is to enable the cache usage for user profile into the `user` section.

```yaml
# User management configuration
user:user
  # keep user profile during authentication flow
  # into a cache to limit read access to the Database
  # when the Gateway is looking for the profile linked to the session
  cache:
    enabled: false
    # retention duration in seconds
    ttl: 3600
```

