---
description: An overview about gateway internal api.
metaLinks:
  alternates:
    - gateway-internal-api.md
---

# Gateway Internal API

## Overview

The Gravitee APIM Gateway component includes its own internal API for monitoring and retrieving technical information about the component.

## Configuration

Enable the API as a service and update any other required configuration. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
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
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_services_core_http_enabled=true
gravitee_services_core_http_port=18082
gravitee_services_core_http_host=localhost
gravitee_services_core_http_authentication_type=basic
gravitee_services_core_http_authentication_users_admin=adminadmin
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `gateway.services.core.http` block in your `values.yaml` file. The APIM Helm chart renders these values into the Gateway `gravitee.yml` at install time:

```yaml
gateway:
  services:
    core:
      http:
        enabled: true
        port: 18082
        host: localhost
        authentication:
          type: basic
          password: adminadmin
```

{% hint style="info" %}
The chart hardcodes the username to `admin`. To configure additional users, mount a custom `gravitee.yml` into the Gateway container or inject indexed environment variables through the `gateway.env` array.
{% endhint %}
{% endtab %}
{% endtabs %}

The above values are defined as follows:

* `enabled`: Whether the service is enabled (default `true`).
* `port`: The port the service listens on (default `18082`). Ensure you use a port not already in use by another APIM component.
* `host`: The host (default `localhost`).
* `authentication.type`: The authentication type for requests. This value is `none`, if no authentication is required, or `basic` (default `basic`).
* `authentication.users`: A list of `user: password` combinations. Only required if authentication type is `basic`.

## Endpoints

<table data-full-width="true"><thead><tr><th width="201">Operation</th><th width="320.3333333333333">Description</th><th>Example</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node
</code></pre></td><td>Gets generic node information.</td><td><pre data-overflow="wrap"><code>HTTP/1.1 200 OK
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
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/health
</code></pre></td><td><p>Gets the health status of the component.</p><p>Probes can be filtered using the optional <code>probes</code> query parameter, which can handle a list of probes separated by commas (<code>,</code>). If no query param is provided, the health of all probes is returned. If the return status is 200, everything is ok; if it is 500, there is at least one error.</p><p>This endpoint can be used by a load balancer, e.g., to determine if a component instance is not in the pool.</p><p>⚠ The following probes are not displayed by default and you must explicitly use the query param to retrieve them:</p><ul><li><strong>cpu</strong></li><li><strong>memory</strong></li><li><strong>api-sync</strong></li></ul><p>These probes are considered healthy if they are under a configurable threshold (default is 80%). To configure the default, add it to your <code>gravitee.yml</code>:</p><pre><code>
services:
health:
threshold:
cpu: 80
memory: 80
</code></pre></td><td><p><code>GET /_node/health</code></p><pre><code>HTTP/1.1 200 OK
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
</code></pre><p><code>GET /_node/health?probes=management-repository,http-server</code></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"management-repository": {
"healthy": true
},
"http-server": {
"healthy": true
}
}
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/configuration
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
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/logging
POST /_node/logging
</code></pre></td><td><p>Gets or updates the logging configuration.</p><p>Use a <code>GET</code> request to view the current logging configuration. Use a <code>POST</code> request to dynamically change the logging level of a specific package. To reset a logger level, send the same payload with an empty or <code>null</code> level.</p></td><td><p><strong>POST payload example:</strong></p><pre><code>{"org.springframework.data.mongodb.core.MongoTemplate": "DEBUG"}
</code></pre><p><strong>GET/POST response example:</strong></p><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"org.eclipse.jetty": "INFO",
"ROOT": "WARN",
"io.gravitee": "INFO",
"org.springframework.data.mongodb.core.MongoTemplate": "DEBUG"
}
</code></pre></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/cluster
</code></pre></td><td>Gets the current state of the cluster with information about its members.</td><td><pre><code>HTTP/1.1 200 OK
Content-Type: application/json
{
"clusterId": "gio-apim-gateway-cluster-manager-hz55",
"running": true,
"self": {
"primary": true,
"running": true,
"attributes": {
"gio_node_hostname": "node_hostname",
"gio_node_id": "node_id"
},
"version": "5.5.0",
"host": "127.0.0.1",
"id": "member_id",
"self": true
},
"members": [
{
"primary": true,
"attributes": {
"gio_node_hostname": "node_hostname",
"gio_node_id": "node_id"
},
"version": "5.5.0",
"host": "127.0.0.1",
"id": "member_id",
"self": true
}
]
}
</code></pre></td></tr></tbody></table>

## Heap dump and thread dump endpoints

The Gateway internal API exposes two endpoints for capturing JVM heap dumps and thread dumps to help with troubleshooting. Both endpoints are disabled by default for security reasons. Enable them only when you need them, and confirm the Gateway internal API has authentication configured before exposing them.

<table data-full-width="true"><thead><tr><th width="220">Operation</th><th>Description</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>GET /_node/heapdump
</code></pre></td><td><p>Returns a JVM heap dump file as the response body. The file extension is <code>.hprof</code> for HotSpot JVMs and <code>.phd</code> for OpenJ9 JVMs.</p><p>Pass the optional <code>?live=true</code> query parameter to forward the <code>live</code> flag to the HotSpot heap dump API (default <code>false</code>). The flag has no effect on OpenJ9.</p><p>The endpoint serializes heap dump requests. Only one heap dump runs at a time.</p></td></tr><tr><td><pre data-overflow="wrap"><code>GET /_node/threaddump
</code></pre></td><td>Returns a plain-text dump of all live threads as the response body (<code>Content-Type: text/plain;charset=UTF-8</code>). Each request reports locked monitors and locked synchronizers.</td></tr></tbody></table>

### Enable the endpoints

Set the enable flags on the Gateway and restart it. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
services:
  core:
    endpoints:
      heapdump:
        enabled: true
      threaddump:
        enabled: true
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_services_core_endpoints_heapdump_enabled=true
gravitee_services_core_endpoints_threaddump_enabled=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
The APIM Helm chart doesn't expose dedicated values for these endpoints, so inject them as environment variables through the `gateway.env` array. The Gateway container picks them up through Gravitee's `gravitee_` env-var prefix:

```yaml
gateway:
  env:
    - name: gravitee_services_core_endpoints_heapdump_enabled
      value: "true"
    - name: gravitee_services_core_endpoints_threaddump_enabled
      value: "true"
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
These endpoints expose JVM internals and the contents of process memory. Don't enable them on a Gateway that's reachable without authentication, and disable them again once you've captured the dumps you need.
{% endhint %}

### Capture a heap dump

Request the heap dump from the host running the Gateway, replacing the host, port, and credentials with values from your `services.core.http` configuration. The endpoint streams the dump in the response body, so write it to a file:

```bash
curl -u admin:adminadmin \
  http://localhost:18082/_node/heapdump \
  -o heap-$(date +%Y-%m-%d-%H-%M).hprof
```

If the Gateway runs in a Kubernetes pod, forward the internal API port from the Gateway pod first, then run the same `curl` against `localhost`:

```bash
kubectl port-forward -n <namespace> <gateway-pod> 18082:18082
```

To analyze the dump, open the `.hprof` file in a HotSpot-compatible heap analyzer, or open the `.phd` file in an OpenJ9-compatible analyzer. The file format depends on the JVM the Gateway runs on.

### Capture a thread dump

Request the thread dump the same way. The response body is plain text and opens in any text editor:

```bash
curl -u admin:adminadmin \
  http://localhost:18082/_node/threaddump \
  -o thread-$(date +%Y-%m-%d-%H-%M).txt
```

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
