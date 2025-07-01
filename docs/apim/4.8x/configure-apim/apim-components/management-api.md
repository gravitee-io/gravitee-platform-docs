# Management API

## Overview

This guide will walk through how to configure your general Gravitee APIM Management API settings using the `gravitee.yaml` file. As detailed in [APIM Components](./#configuring-apim-components), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Configure HTTP server

You configure the HTTP Server configuration in the following section of the `gravitee.yml` file:

```yaml
jetty:
  port: 8083
  idleTimeout: 30000
  acceptors: -1
  selectors: -1
  pool:
    minThreads: 10
    maxThreads: 200
    idleTimeout: 60000
    queueSize: 6000
  jmx: false
  statistics: false
  accesslog:
    enabled: true
    path: ${gravitee.home}/logs/gravitee_accesslog_yyyy_mm_dd.log
```

### Enable HTTPS support

First, you need to provide a keystore. If you do not have one, you can generate it:

```
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

```yaml
jetty:
  ...
  secured: true
  ssl:
    keystore:
      path: ${gravitee.home}/security/keystore.jks
      password: secret
    truststore:
      path: ${gravitee.home}/security/truststore.jks
      password: secret
```

{% hint style="info" %}
Truststore and Keystore settings defined within the `jetty` section are only used to secure access to APIM API. These are not used by HTTP client calls for any other purpose (such as Fetch and DCR).
{% endhint %}

## Configure the Management and Portal APIs

You can configure APIM API to start only the Management or Portal API. You can also change the API endpoints from their default values of `/management` and `/portal`.

```yaml
http:
  api:
    # Configure the listening path for the API. Default to /
#    entrypoint: /
    # Configure Management API.
#    management:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}management
#      cors: ...
    # Configure Portal API.
#    portal:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}portal
#      cors: ...
```

## CORS configuration

CORS (Cross-Origin Resource Sharing) is a mechanism that allows resources on a web page to be requested from another domain.

For more information on CORS, take a look at the [CORS specification](https://www.w3.org/TR/cors).

CORS can be applied at three different levels:&#x20;

1. API
2. Environment
3. Organization

where the more specific levels override the broader levels: API > Environment > Organization.

You can configure CORS at the organization level using `gravitee.yml`, environment variables or directly in APIM Console. Here's an example of configuring CORS using the `gravitee.yml` file:

{% code title="gravitee.yaml" %}
```yaml
http:
  api:
    # Configure the listening path for the API. Default to /
#    entrypoint: /
    # Configure Management API.
#    management:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}management
#      cors:
    # Allows to configure the header Access-Control-Allow-Origin (default value: *)
    # '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#       allow-origin: http://developer.mycompany.com
    # Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#       max-age: 864000
    # Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE)
#      allow-methods: 'OPTIONS, GET, POST, PUT, DELETE'
    # Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#      allow-headers: 'X-Requested-With'
  # Configure Portal API.
#    portal:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}portal
#      cors:
    # Allows to configure the header Access-Control-Allow-Origin (default value: *)
    # '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#       allow-origin: http://developer.mycompany.com
    # Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#       max-age: 864000
    # Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE)
#      allow-methods: 'OPTIONS, GET, POST, PUT, DELETE'
    # Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#      allow-headers: 'X-Requested-With'
```
{% endcode %}

### Configure in APIM Console

{% hint style="info" %}
If you change the CORS settings using the `gravitee.yml` or environment variables, then the CORS settings will be greyed out in the APIM console.
{% endhint %}

You can also configure CORS at the organization level in the **Organization > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-30 at 2.35.47 PM.png" alt=""><figcaption><p>Organization CORS settings</p></figcaption></figure>

Or at the environment level in the **Settings > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.20.53 PM.png" alt=""><figcaption><p>Environment CORS settings</p></figcaption></figure>

## Configure the Management repository

The Management repository is used to store global configurations such as APIs, applications, and API keys. The default configuration uses MongoDB (single server).

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
#    threadsAllowedToBlockForConnectionMultiplier: 5
#    cursorFinalizerEnabled: true
## SSL settings (Available in APIM 3.10.14+, 3.15.8+, 3.16.4+, 3.17.2+, 3.18+)
#    sslEnabled:
#    keystore:
#      path:
#      type:
#      password:
#      keyPassword:
#    truststore:
#      path:
#      type:
#      password:
## Deprecated SSL settings that will be removed in 3.19.0
#    sslEnabled:
#    keystore:
#    keystorePassword:
#    keyPassword:

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

## Configure the Analytics repository

The Analytics repository stores all reporting, metrics, and health-checks for all APIM Gateway instances. The default configuration uses [Elasticsearch](https://www.elastic.co/products/elasticsearch).

```yaml
  type: elasticsearch
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    security:
#       username:
#       password:
```

## SMTP configuration

This section shows the SMTP configuration used for sending email.

You can configure SMTP using `gravitee.yml`, environment variables or directly in APIM Console. If SMTP is configured with `gravitee.yml` or environment variables, then that configuration will be used, even if settings exist in the database.

SMTP can be applied at two different levels:&#x20;

1. Environment
2. Organization

where the more specific level overrides the broader level:  Environment > Organization.

Here's an example of configuring SMTP using the `gravitee.yml` file:

```yaml
email:
  host: smtp.my.domain
  port: 465
  from: noreply@my.domain
  subject: "[Gravitee.io] %s"
  username: user@my.domain
  password: password
```

### Configure in APIM Console

{% hint style="info" %}
If you change the SMTP settings using the `gravitee.yml` or environment variables, then the SMTP settings will be greyed out in the APIM console.
{% endhint %}

You can also configure SMTP at the organization level in the **Organization > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.27.18 PM.png" alt=""><figcaption><p>Organization SMTP settings</p></figcaption></figure>

Or at the environment level in the **Settings > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.30.01 PM.png" alt=""><figcaption><p>Environment SMTP settings</p></figcaption></figure>

### Configure the Gmail SMTP server

If required, you can configure the GMAIL SMTP server in `gravitee.yml` as follows:

```yaml
email:
  enabled: true
  host: smtp.gmail.com
  port: 587
  from: user@gmail.com
  subject: "[Gravitee.io] %s"
  username: user@gmail.com
  password: xxxxxxxx
  properties:
    auth: true
    starttls.enable: true
    ssl.trust: smtp.gmail.com
```

If you are using 2-Factor Authentication (which is recommended), you need to [generate an application password](https://security.google.com/settings/security/apppasswords).

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Management API in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-rest-api/gravitee-apim-rest-api-standalone/gravitee-apim-rest-api-standalone-distribution/src/main/resources/config/gravitee.yml" %}
