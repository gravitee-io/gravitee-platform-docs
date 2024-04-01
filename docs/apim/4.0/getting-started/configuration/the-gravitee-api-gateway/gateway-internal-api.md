---
description: Learn how to configure the internal Gateway API
---

# Internal API

## Introduction

The Gravitee APIM Gateway component comes with its own internal API, for monitoring and retrieving technical information about the component.

## Configuration

You need to enable the API as a service in the `gravitee.yaml` file and update any other required configuration.

```
services:
  core:
    http:
      enabled: true
      port: 18082
      host: localhost
      authentication:
        type: basic
        users:
          admin: adminadmin
```

The above values can be understood as such:

`enabled`: whether the service is enabled (default `true`).

`port`: the port the service listens on (default `18082`). You must ensure you use a port which is not already in use by another APIM component.

`host`: the host (default `localhost`).

`authentication.type`: the authentication type for requests:

* `none` if no authentication is required or `basic` (default `basic`).

`authentication.users`: a list of `user: password` combinations. Only required if authentication type is `basic`.

### Endpoints

<table data-full-width="true"><thead><tr><th>Operation</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node
</code></pre></td><td>Gets generic node information</td><td><pre data-overflow="wrap"><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "id" : "10606a6a-fe49-4144-a06a-6afe494144c9",
  "name" : "Gravitee.io - API Gateway",
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
</code></pre></td><td><p>Gets the health status of the component. Probes can be filtered using the optional <code>probes</code> query param. The parameter can handle a list of probes, separated by commas (<code>,</code>). If no query param, you get the health of default probes. If the return status is 200 then everything is ok, if 500, there is at least one error. This endpoint can be used by a load balancer, to determine if a component instance is not in the pool, for example. Some probes are not displayed by default. You have to explicitly use the query param to retrieve them.</p><p>Available probes are:</p><ul><li><code>ratelimit-repository</code>: checks the connection with the ratelimit repository (Mongo, Redis, ...) [Default]</li><li><code>management-repository</code>: checks the connection with the database (Mongo, JDBC, ...) [Default]</li><li><code>http-server</code>: checks if the Gateway is reachable [Default]</li><li><code>sync-process</code>: checks if all the initial synchronization services (Platform policies, APIs, properties, dictionaries, debug API) have been successfully executed</li><li><code>cpu</code></li><li><code>memory</code></li></ul><p>CPU and memory probes are considered healthy if there are under a configurable threshold (default is 80%). To configure it, add in your <code>gravitee.yml</code>:</p><pre data-overflow="wrap"><code>services:
  health:
    threshold:
      cpu: 80
      memory: 80
</code></pre></td><td><p>Response to <code>GET /_node/health</code></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "ratelimit-repository": {
    "healthy": true
  },
  "management-repository": {
    "healthy": true
  },
  "http-server": {
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

### Component-specific endpoints

In addition to the main endpoints listed above, the API includes dedicated endpoints to get more information about the APIs deployed on the APIM Gateway instance.

<table data-full-width="true"><thead><tr><th>Operation</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node/apis
</code></pre></td><td>Gets the APIs deployed on this APIM Gateway instance.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
[
  {
    "id": "5b7a30b5-8feb-4c11-ba30-b58feb6c112f",
    "name": "Foo API",
    "version": "1.0.0"
  },
  {
    "id": "5da639b6-a3c7-4cc5-a639-b6a3c75cc5f9",
    "name": "Bar API",
    "version": "v1"
  }
]
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/apis/{api.id}
</code></pre></td><td>Gets the API configuration for this APIM Gateway instance.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "deployedAt": 1552574408611,
  "enabled": true,
  "id": "5b7a30b5-8feb-4c11-ba30-b58feb6c112f",
  "name": "Foo API",
  "pathMappings": {},
  "paths": {
    ...
  }
}
</code></pre></td></tr></tbody></table>
