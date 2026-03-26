---
description: An overview about Internal API.
---

# Internal API

## Overview

The Gravitee API Management (APIM) Management API component comes with its own internal API, for monitoring and retrieving technical information about the component.

### Configuration

You need to enable the API as a service in the `gravitee.yml` file and update any other required configuration.

```yaml
services:
  core:
    http:
      enabled: true
      port: 18083
      host: localhost
      authentication:
        type: basic
        users:
          admin: adminadmin
```

`enabled`**:** (default `true`) Whether the service is enabled.

`port`**:** (default `18083`) The port the service listens on. You must ensure you use a port that is not already in use by another APIM component.

`host`**:** (default `localhost`) The host.

`authentication.type`**:** (default `basic`) Authentication type for requests: `none` if no authentication is required.

`authentication.users`**:** A list of `user: password` combinations. Only required if authentication type is `basic`.

#### Endpoints

<table data-full-width="true"><thead><tr><th>Operation</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node
</code></pre></td><td>Gets generic node information</td><td><pre data-overflow="wrap"><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "id" : "10606a6a-fe49-4144-a06a-6afe494144c9",
  "name" : "Gravitee.io - Rest APIs",
  "metadata" : {
    "node.id" : "10606a6a-fe49-4144-a06a-6afe494144c9",
    "environments" : [ ],
    "installation" : "257ee127-a802-4387-bee1-27a802138712",
    "organizations" : [ ],
    "node.hostname" : "my-host"
  },
  "version" : {
    "BUILD_ID" : "547086",
    "BUILD_NUMBER" : "547086",
    "MAJOR_VERSION" : "4.0.15",
    "REVISION" : "f9ed32f42fd701a44844131ac959790abe10e08a"
  }
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/health?probes=#probe1,#probe2
</code></pre></td><td><p>Gets the health status of the component. Probes can be filtered using the optional <code>probes</code> query param. The parameter can handle a list of probes, separated by commas (<code>,</code>). If no query param, you get the health of default probes. If the return status is 200 then everything is ok, if 500, there is at least one error. This endpoint can be used by a load balancer, to determine if a component instance is not in the pool, for example. Some probes are not displayed by default. You have to explicitly use the query param to retrieve them.</p><p>Available probes are:</p><ul><li><code>management-repository</code>: checks the connection with the database (Mongo, JDBC, ...) [Default]</li><li><code>gravitee-apis</code>: checks if the Management API and Portal API are reachable [Default]</li><li><code>repository-analytics</code>: checks the connection with the analytics database (ElasticSearch or OpenSearch) [Default]</li><li><code>cpu</code></li><li><code>memory</code></li></ul><p>CPU and memory probes are considered healthy if there are under a configurable threshold (default is 80%). To configure it, add in your <code>gravitee.yml</code>:</p><pre data-overflow="wrap"><code>services:
  health:
    threshold:
      cpu: 80
      memory: 80
</code></pre></td><td><p>Response to <code>GET /_node/health</code></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "management-repository": {
    "healthy": true
  },
  "gravitee-apis": {
    "healthy": true
  },
  "repository-analytics": {
    "healthy": true
  }
}
</code></pre><p>Response to <code>GET /_node/health?probes=cpu,memory,management-repository</code></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "cpu": {
    "healthy": true
  },
  "memory": {
    "healthy": true
  },
  "management-repository": {
    "healthy": true
  }
}
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/configuration
</code></pre></td><td>Gets the node configuration from the <code>gravitee.yml</code> file and/or environment variables.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"analytics.elasticsearch.endpoints[0]": "http://${ds.elastic.host}:${ds.elastic.port}",
"analytics.type": "elasticsearch",
"ds.elastic.host": "localhost",
"ds.elastic.port": 9200,
...
}
</code></pre></td></tr><tr><td><pre class="language-sh" data-overflow="wrap"><code class="lang-sh">GET /_node/monitor
</code></pre></td><td>Gets monitoring information from the JVM and the server.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "jvm": {
    "gc": {
      "collectors": [{
        "collectionCount": 7,
        "collectionTime": 98,
        "name": "young"
      },
      {
        "collectionCount": 3,
        "collectionTime": 189,
        "name": "old"
      }]
    },
    "mem": {
      ...
    }
  }
}
</code></pre></td></tr></tbody></table>
