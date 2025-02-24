# AM API

## Configuration overview

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

```yaml
repositories:
  management:
    mongodb:
      dbname: myDatabase
```

Add this property to the JVM:

```
-Dmanagement.repositories.mongodb.dbname=myDatabase
```

### Environment variables

You can override the default AM configuration (`gravitee.yml`) and system properties by defining environment variables.

To override this property:

```yaml
repositories:
  management:
    mongodb:
      dbname: myDatabase
```

Define one of the following variables:

```
GRAVITEE_REPOSITORIES_MANAGEMENT_MONGODB_DBNAME=myDatabase
GRAVITEE.REPOSITORIES.MANAGEMENT.MONGODB.DBNAME=myDatabase
gravitee_repositories_management_mongodb_dbname=myDatabase
gravitee.repositories.management.mongodb.dbname=myDatabase
```

Some properties are case sensitive and cannot be written in uppercase (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`. We advise you to define environment variables in lowercase and use the correct syntax for each property.

{% hint style="info" %}
In some systems, hyphens are not allowed in variable names. For example, you may need to write `gravitee_http_cookie_allow-credentials` as `gravitee_http_cookie_allowcredentials` .
{% endhint %}

#### **How to manage arrays?**

Some properties are arrays. For example:

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

Below are some examples of how to write your environment variables. In case of doubt, we recommend you try both.

```
gravitee_http_ssl_endpoints_0=token_endpoint
gravitee_http_ssl_endpoints_1=registration_endpoint

gravitee_security_providers_0_type=ldap
gravitee_security_providers_0_context-source-username=cn=Directory Manager
gravitee_security_providers_0_context-source-password=password
```

or

```
gravitee.http.ssl.endpoints[0]=token_endpoint
gravitee.http.ssl.endpoints[1]=registration_endpoint

gravitee.security.providers[0]type=ldap
gravitee.security.providers[0]context-source-username=cn=Directory Manager
gravitee.security.providers[0]context-source-password=password
gravitee.security.providers[0].users[1].password=password
```

## Detailed `gravitee.yml` configuration

### Configure HTTP server

You can update the HTTP server configuration in the following section of the `gravitee.yml` file.

```yaml
jetty:
  port: 8093
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

#### **Enable HTTPS support**

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

You then need to enable secure mode in your `gravitee.yml`:

```yaml
jetty:
  port: 8093
  idleTimeout: 0
  tcpKeepAlive: true
  compressionSupported: false
  pool:
    workers: 100
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

### Security

Since AM 3.10, the security section allows you to define the users available to authenticate to the Management Console after the first start. Until AM 3.9, there was only one user `admin` created in a inline identity provider. In 3.10, this behaviour is preserve by enabling the `security.defaultAdmin` option (default value).

This section introduce a providers section to define a set of identity providers instantiated on startup. These providers are not visible from the Management Console.

Currently, only the provider type `memory` is available. The users known by this provider are defined into a list named `users` (see example here after). For each user, you have to define one organization role:

* ORGANIZATION\_PRIMARY\_OWNER
* ORGANIZATION\_OWNER
* ORGANIZATION\_USER

If a user role or a user password is updated, new values are applied on restart.

```yaml
security:
  # If true create on AM bootstrap an inline identity provider with an admin user (login: admin)
  # this is the legacy mode
  defaultAdmin: true
  ## authentication providers
  ## currently, only "in memory" provider is supported
  providers:
    - type: memory
      enabled: false
      ## Name of IdentityProvider
      ## If missing the type will be used to create a generic name (ex: Memory users)
      #name:
      ## password encoding/hashing algorithm. One of:
      ## - BCrypt : passwords are hashed with bcrypt (supports only $2a$ algorithm)
      ## - none : passwords are not hashed/encrypted
      #default value is BCrypt
      password-encoding-algo: BCrypt
      users:
        - username: admin
          #email:
          firstname: Administrator
          lastname: Administrator
          ## Passwords are encoded using BCrypt
          ## Password value: adminadmin
          password: $2a$10$NG5WLbspq8V1yJDzUKfUK.oum94qL/Ne3B5fQCgekw/Y4aOEaoFZq
          role: ORGANIZATION_OWNER
```

### Configure email

```
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

{% hint style="info" %}
In order to enforce TLS 1.2 uncomment the properties in the above example and change according to your requirements.
{% endhint %}

#### **Email password and name complexity**

You can configure the complexities as per your organizational requirements. The default settings is shown below:

{% code overflow="wrap" %}
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

Gravitee.io Gateway plugins directory configuration.

```yaml
plugins:
  path: ${gravitee.home}/plugins
```

### Configure the Management repository

Management repository is used to store global configuration such as APIs, applications, apikeys, etc. This is the default configuration using MongoDB (single server).&#x20;

{% code overflow="wrap" %}
```yaml
repositories:
  management:
    type: mongodb
    mongodb:
      dbname: ${ds.mongodb.dbname}
      host: ${ds.mongodb.host}
      port: ${ds.mongodb.port}
#     username:
#     password:
#     connectionsPerHost: 0
#     connectTimeout: 500
#     maxWaitTime: 120000
#     socketTimeout: 500
#     socketKeepAlive: false
#     maxConnectionLifeTime: 0
#     maxConnectionIdleTime: 0
#     serverSelectionTimeout: 0
#     description: gravitee.io
#     heartbeatFrequency: 10000
#     minHeartbeatFrequency: 500
#     heartbeatConnectTimeout: 1000
#     heartbeatSocketTimeout: 20000
#     localThreshold: 15
#     minConnectionsPerHost: 0
#     sslEnabled: false
#     threadsAllowedToBlockForConnectionMultiplier: 5
#     cursorFinalizerEnabled: true
#     keystore:
#      keystorePassword:
#      keyPassword

# Management repository: single MongoDB using URI
# For more information about MongoDB configuration using URI, please have a look to:
# - http://api.mongodb.org/java/current/com/mongodb/MongoClientURI.html
#repositories;
#  management:
#    type: mongodb
#    mongodb:
#      uri: mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

# Management repository: clustered MongoDB
#repositories;
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

### Configure the domain <a href="#configure-the-client-secret-hash" id="configure-the-client-secret-hash"></a>

A domain creation comes with default plugins instantiation. To provide the default settings you are expecting, the `domains` section can be updated to specify :

* the technical details of the default certificate
* if a default reporter need to be created
* if a default identity provider need to be created, if so what should be the password encoding&#x20;

```yaml
domains:
#  identities:
#    default:
#      enabled: false
#      passwordEncoder:
#         # Algorithms used to hash the user password.
#         # Can be one of :
#         # "BCrypt", "SHA-256", "SHA-384", "SHA-512", "SHA-256+MD5"
#        algorithm: BCrypt
#        properties:
#          # Number of rounds used by BCrypt
#          rounds: 10
  certificates:
    default:
      keysize: 2048
      alias: default
      keypass: gravitee
      storepass: gravitee
      validity: 365             # Validity of the certificate
      algorithm: SHA256withRSA  # Algorithm used to sign certificate
      name: cn=Gravitee.io      # Certificate X.500 name
#  reporters:
#    default:
#      # should the default (database) reporter be created. E.g. if the organization defines a global reporter,
#      # domain-level reporters might not be necessary
#      enabled: true
```

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
* **algorithm**: PBKDF2 with the specified pseudo-random function (default: PBKDF2WithHmacSHA256**)**

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

### Configure notifications on certificates expiry

New in version 3.17

Gravitee AM provides a notification mechanism to inform about certificates expiry. When enabled, domain primary owners and domain owners will receive a notification using the configured channel (UI or Email). These notifications will be triggered based on several conditions:

* the frequency on which the certificates expiry dates are evaluate
* the number of days before the certificate expiry
* the number of days to wait before a notification is going to be resent

All the settings here after have to be defined into the `services` section of the `gravitee.yaml` file.

{% code overflow="wrap" %}
```yaml
services:
  # platform notifier service
  notifier:
    enabled: true
    tryAvoidDuplicateNotification: false

  # Rules about certificate expiry notifications.
  # Require the platform notifier service.
  certificate:
    enabled: true
    # frequency on which the notifier mechanism will test
    # if new notifications need to be send
    # default: 0 0 5 * * * (every day at 5am)
    cronExpression: 0 0 5 * * *
    # send notification if certificate is going to expire in less than 20 days,
    # then send again the notification 15 days before the expiry, then 10...
    expiryThresholds: 20,15,10,5,1
    # Subject of the email send by the email notifier
    expiryEmailSubject: Certificate will expire soon
```
{% endcode %}

In addition of the configuration for services, the notification channels have to be defined. Currently, there are two channel :

* email: If enable, a notification will be sent by email using the smtp settings defined in this section.
* ui: If enable, a notification icon will be available on top of the console UI to inform about new notifications.

```yaml
notifiers:
  email:
    enabled: false
    host: smtp.my.domain
    port: 587
    username: user@my.domain
    password: password
    from: noreply@my.domain
    startTLSEnabled: false
    sslTrustAll: false
    #sslKeyStore: /path/to/keystore
    #sslKeyStorePassword: changeme
  ui:
    enabled: true
```

![graviteeio am installationguide certificates ui](https://docs.gravitee.io/images/am/current/graviteeio-am-installationguide-certificates-ui.png)

## Configure load balancing

If you are planning to use multiple instances, you need to implement sticky sessions in your load balancer, until [this issue](https://github.com/gravitee-io/issues/issues/2523) is closed.

### Apache

Example using three instances of AM API. We add an additional cookie named ROUTEID. TLS termination is configured in Apache, so we just use HTTP.

{% code overflow="wrap" %}
```
<Proxy balancer://amm_hcluster>
        BalancerMember http://GRAVITEEIO-AM-MGT-API-HOST1:8093 route=apim1-test
        BalancerMember http://GRAVITEEIO-AM-MGT-API-HOST2:8093 route=apim2-test
        BalancerMember http://GRAVITEEIO-AM-MGT-API-HOST3:8093 route=apim3-test
        ProxySet stickysession=ROUTEID
        ProxySet lbmethod=byrequests
        Header add Set-Cookie "ROUTEID=.%{BALANCER_WORKER_ROUTE}e;" env=BALANCER_ROUTE_CHANGED
        Header append Via %{BALANCER_WORKER_ROUTE}e
</Proxy>
```
{% endcode %}

Then, in your VirtualHost configuration, we declare the paths we want to proxy:

```
# Management Realm
ProxyPass /admin balancer://amm_hcluster/admin
ProxyPassReverse /admin balancer://amm_hcluster/admin

# Management
ProxyPass /management balancer://amm_hcluster/management
ProxyPassReverse /management balancer://amm_hcluster/management

```

## Configure default creations

### Default Identity provider

AM API on first startup creates default identity provider in DB (MongoDB or JDBC). To disable this configure in `gravitee.yml`

```yaml
domains:
  identities:
    default:
enabled: false
```

### Default Reporter

AM API on first startup creates default reporter in DB (MongoDB or JDBC) for audit logs. To disable this configure in `gravitee.yml`

```yaml
domains:
  reporters:
    default:
enabled: false
```

{% hint style="info" %}
Please be aware that when you disable default reporter and not specified new one, nothing will be logged in Audit Logs.
{% endhint %}
