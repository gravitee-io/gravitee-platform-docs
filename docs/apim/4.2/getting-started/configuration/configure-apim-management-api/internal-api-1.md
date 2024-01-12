# Internal API

## Overview

The Gravitee API Management (APIM) Management API component includes its own internal API for monitoring and retrieving technical information about the component.

## Configuration

Enable the API as a service in the `gravitee.yml` file and update any other required configuration:

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

The above values are defined as follows:

* `enabled`**:** Whether the service is enabled (default `true`).
* `port`**:** The port the service listens on (default `18083`). Ensure you use a port not already in use by another APIM component.
* `host`**:** The host (default `localhost`).
* `authentication.type`**:** Authentication type for requests (default `basic`). Use the value `none` if no authentication is required.&#x20;
* `authentication.users`**:** A list of `user: password` combinations. Only required if authentication type is `basic`.

## Endpoints

<table><thead><tr><th width="172.33333333333331">Operation</th><th width="193">Description</th><th>Example</th></tr></thead><tbody><tr><td><code>GET /_node</code></td><td>Gets generic node information.</td><td><pre><code>HTTP/1.1 200 OK
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
</code></pre></td></tr><tr><td><code>GET /_node/health?probes=#probe1,#probe2</code></td><td><p>Gets the health status of the component. </p><p>Probes can be filtered using the optional <code>probes</code> query parameter, which can handle a list of probes separated by commas (<code>,</code>). If no query param is provided, the health of all probes is returned. If the return status is 200, everything is ok; if it is 500, there is at least one error. </p><p>This endpoint can be used by a load balancer, e.g., to determine if a component instance is not in the pool.</p><p>The following probes are not displayed by default and you must explicitly use the query param to retrieve them:</p><p>- <strong>cpu</strong></p><p>- <strong>memory</strong></p><p>- <strong>api-sync</strong></p><p>These probes are considered healthy if they are under a configurable threshold (default is 80%). To configure the default, add it to your <code>gravitee.yml</code>:</p><p>[source, yml] ---- services: health: threshold: cpu: 80 memory: 80 ----</p></td><td><p><code>GET /_node/health?probes=management-api,management-repository</code></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"management-api": {
"healthy": true
},
"management-repository": {
"healthy": true
},
"api-sync": {
"healthy": true
},
"api-sync": {
"healthy": true
}
}
</code></pre></td></tr><tr><td><code>GET /_node/configuration</code></td><td>Gets the node configuration from the <code>gravitee.yml</code> file and/or environment variables.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"analytics.elasticsearch.endpoints[0]": "http://${ds.elastic.host}:${ds.elastic.port}",
"analytics.type": "elasticsearch",
"ds.elastic.host": "localhost",
"ds.elastic.port": 9200,
...
}
</code></pre></td></tr><tr><td><code>GET /_node/monitor</code></td><td>Gets monitoring information from the JVM and the server.</td><td><pre><code>HTTP/1.1 200 OK
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
