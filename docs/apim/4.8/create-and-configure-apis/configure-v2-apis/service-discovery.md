# Service Discovery

## Overview

Gravitee service discovery for HashiCorp Consul allows you to bind the backend endpoints of your API to a service dynamically managed by HashiCorp Consul so that API requests are always routed to the proper, healthy backend service. By integrating the Gateway with HashiCorp Consul, dynamic load-balancer configuration changes are pulled directly from Consul’s service discovery registry.

This article describes how to configure service discovery using the HashiCorp Consul solution.

## Configure HashiCorp Consul

### Prerequisites

* [Install Gravitee with `docker-compose`](docs/apim/4.8/self-hosted-installation-guides/docker/docker-compose.md)

### 1. Install a HashiCorp Consul server

Consul agents that run in server mode become the centralized registry for service discovery information in your network. Services registered with Consul clients are discoverable, and Consul servers can answer queries from other Consul agents about where a particular service is running, e.g., returning IP addresses and port numbers.

{% hint style="info" %}
Refer to the [official Consul documentation](https://www.consul.io/docs/install) to learn how to install a Consul server.
{% endhint %}

To use `docker-compose` to set up an integration between Gravitee APIM and HashiCorp Consul:

1. Edit the `docker-compose.yml` used to install Gravitee and declare an additional service for the Consul server. The example below declares a read-only volume to mount the directory containing Consul configuration files.

{% code overflow="wrap" %}
```
```
{% endcode %}

\`\`\`\` \`\`\`bash consul-server: image: hashicorp/consul:1.15.4 container\_name: consul-server restart: always volumes: - ./consul/server.json:/consul/config/server.json:ro ports: - "8500:8500" - "8600:8600/tcp" - "8600:8600/udp" command: "agent" networks: - storage \`\`\` \`\`\`\` \{% endcode %\}

2. Consul containers load their configuration from `/consul/config/` at startup. Use the `server.json` below to initialize the Consul server:

\{% code overflow="wrap" %\}

````
```bash
{
  "node_name": "consul-server",
  "server": true,
  "bootstrap" : true,
  "ui_config": {
      "enabled" : true
  },
  "data_dir": "/consul/data",
  "addresses": {
      "http" : "0.0.0.0"
  }
}
```
````

\{% endcode %\}

\`

\`\`

* `server=true` indicates that this Consul agent should run in server mode
* Consul’s web UI is enabled by setting the `enabled` sub-key of the `ui_config` attribute to `true`
* Once Consul server’s container is running, Consul’s web UI is accessible at port `8500`
* The `addresses` field specifies the address that the agent will listen on for communication from other Consul members. By default, this is `0.0.0.0`, meaning Consul will bind to all addresses on the local machine and will advertise the private IPv4 address to the rest of the cluster.

````

### 2. Register a service with HashiCorp Consul

An easy way to register a service in Consul is to request the `/v1/agent/service/register` endpoint of Consul’s [Catalog HTTP API](https://www.consul.io/api-docs/catalog).

Consul does not allow you to directly specify an extra path of your service when registering it. To overcome this limitation, Gravitee supports extra `Meta` attributes in addition to the standard `Address` attribute.

Meta attributes must be provided as part of the definition of your service:

* `gravitee_path` to specify on which path your service is reachable
* `gravitee_ssl` to specify whether your service should be called with `http://` or `https://` scheme
* `gravitee_weight` to set a weight on the endpoint to affect the load-balancing
* `gravitee_tenant` to set a tenant value in the endpoint

#### Example: Register a service

The following cURL command registers a service in Consul with additional attributes supported by Gravitee:

```shell
curl -X PUT -d '{ "ID": "whattimeisit_1", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/whattimeisit", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
````

The Consul web UI should display a new service named `whattimeisit`:

<figure><img src="../../../../../.gitbook/assets/service-discovery-consul-services (1).png" alt=""><figcaption></figcaption></figure>

You can also verify that your service is successfully registered in Consul by interacting with Consul Agent API.

1. Run the command below:

{% code overflow="wrap" %}
````
```json
{
  "whattimeisit_1": {
    "ID": "whattimeisit_1",
    "Service": "whattimeisit",
    "Tags": [],
    "Meta": {
      "gravitee_path": "/whattimeisit",
      "gravitee_ssl": "true"
    },
    "Port": 443,
    "Address": "api.gravitee.io",
    "Weights": {
      "Passing": 1,
      "Warning": 1
    },
    "EnableTagOverride": false,
    "Datacenter": "dc1"
  }
}
```
````
{% endcode %}
