---
description: Learn how to configure the internal Gateway API
---

# Internal API

## Introduction

The Gravitee APIM Gateway component includes its own internal API for monitoring and retrieving technical information about the component.

## Configuration

Enable the API as a service in the `gravitee.yaml` file and update any other required configuration:

```yaml
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

The above values are defined as follows:

* `enabled`: Whether the service is enabled (default `true`).
* `port`: The port the service listens on (default `18082`). Ensure you use a port not already in use by another APIM component.
* `host`: The host (default `localhost`).
* `authentication.type`: The authentication type for requests. This value is `none`, if no authentication is required, or `basic` (default `basic`).
* `authentication.users`: A list of `user: password` combinations. Only required if authentication type is `basic`.

## Endpoints

<table data-full-width="true">
  <thead>
    <tr>
      <th width="201">Operation</th>
      <th width="320.3333333333333">Description</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><pre data-overflow="wrap"><code>GET /_node</code></pre></td>
      <td>Gets generic node information.</td>
      <td>
        <pre data-overflow="wrap"><code>HTTP/1.1 200 OK
Content-Type: application/json
{
    "id": "a70b9fd9-9deb-4ccd-8b9f-d99deb6ccd32",
    "metadata": {},
    "name": "Gravitee.io - Management API",
    "version": {
        "BUILD_ID": "309",
        "BUILD_NUMBER": "309",
        "MAJOR_VERSION": "1.20.14",
        "REVISION": "132e719ef314b40f352e6399034d68a9a95e95ef"
    }
}
        </code></pre>
      </td>
    </tr>
    <tr>
    <td><pre data-overflow="wrap"><code>GET /_node/health</code></pre></td>
    <td>
      <p>Gets the health status of the component.</p>
      <p>Probes can be filtered using the optional <code>probes</code> query parameter, which can handle a list of probes separated by commas (<code>,</code>). If no query param is provided, the health of all probes is returned. If the return status is 200, everything is ok; if it is 500, there is at least one error.</p>
      <p>This endpoint can be used by a load balancer, e.g., to determine if a component instance is not in the pool.</p>
      <p>
        &#9888; The following probes are not displayed by default and you must explicitly use the query param to retrieve them:
        <lu>
          <li><strong>cpu</strong></li>
          <li><strong>memory</strong></li>
          <li><strong>api-sync</strong></li>
        </lu>
      </p>
      <p>
        These probes are considered healthy if they are under a configurable threshold (default is 80%). To configure the default, add it to your <code>gravitee.yml</code>:
        <pre><code class="yaml">
services:
  health:
    threshold:
      cpu: 80
      memory: 80
        </code></pre>
      </p>
    </td>
    <td>
      <p>
        <code>GET /_node/health</code>
        <pre><code>HTTP/1.1 200 OK
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
        </code></pre>
      </p>
      <p>
        <code>GET /_node/health?probes=management-repository,http-server</code>
        <pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
  "management-repository": {
    "healthy": true
  },
  "http-server": {
    "healthy": true
  }
}
        </code></pre>
      </p>
    </td>
  </tr>
  <tr><td><pre data-overflow="wrap"><code>GET /_node/configuration
</code></pre></td><td>Gets the node configuration from the <code>gravitee.yml</code> file and/or environment variables.</td><td><pre><code><strong>HTTP/1.1 200 OK
</strong>Content-Type: application/json
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
"collectors": [
{
"collectionCount": 7,
"collectionTime": 98,
"name": "young"
},
{
"collectionCount": 3,
"collectionTime": 189,
"name": "old"
}
]
},
"mem": {
...
}
</code></pre></td></tr></tbody></table>

## Component-specific endpoints

In addition to the main endpoints listed above, the internal API includes dedicated endpoints to get more information about the APIs deployed on the APIM Gateway instance.

<table data-full-width="true"><thead><tr><th width="227">Operation</th><th width="220.66666666666669">Description</th><th>Example</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node/apis
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
</code></pre></td></tr></tbody></table>
