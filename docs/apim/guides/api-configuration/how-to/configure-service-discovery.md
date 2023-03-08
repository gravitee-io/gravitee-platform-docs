---
description: >-
  This article walks through how to configure service discovery if using either
  the Gravitee-supported Eureka or Hashicorp Consul Service Discovery solutions.
---

# Configure Service Discovery

### Introduction



### Configure Hashicorp Consul Service Discovery

Gravitee.io Service discovery for HashiCorp Consul allows you to bind the backend endpoints of your API to a service managed by HashiCorp Consul so that API requests are always routed to the proper, healthy backend service dynamically managed by HashiCorp Consul.

#### Prerequisities

We will be using docker-compose to setup an integration between Gravitee.io APIM and HashiCorp Consul.

Refer to this [guide](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_compose.html) to install Gravitee thanks to docker-compose.

#### Install Hashicorp Consul Server

The first step is to install a Consul server. Consul agents that run in server mode become the centralized registry for service discovery information in your network. They answer queries from other Consul agents about where a particular service can be found. For example, if you ask them where the log service is running, they may return to you that it is running on three machines, with these IP addresses, on these ports. Meanwhile, services such as the log service register themselves with the Consul clients so that they can become discoverable.

Read the [official Consul documentation](https://www.consul.io/docs/install) to see how to install a Consul server.

To get started, edit the _docker-compose.yml_ used to install Gravitee and declare an addtional service for Consul server as follows:

```
consul-server:
    image: hashicorp/consul:1.11.4
    container_name: consul-server
    restart: always
    volumes:
     - ./consul/server.json:/consul/config/server.json:ro
    ports:
     - "8500:8500"
     - "8600:8600/tcp"
     - "8600:8600/udp"
    command: "agent"
    networks:
     - backend
```

In the example above, we declare a volume to mount the directory containing Consul configuration files as a read-only (:ro) volume.

Consul containers load their configuration from `/consul/config/` folder, at startup.

We use the following `server.json` to initialize the Consul server:

```
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

Notice that the `server` field is set to true to indicate that this Consul agent should run in server mode.

We are also enabling Consul’s web UI via `ui_config` attribute by setting sub key `enabled` to `true`.

Once Consul server’s container is running, Consul’s web UI is accessible at port `8500`.

The `addresses` field specifies the address that the agent will listen on for communication from other Consul members.

By default, this is `0.0.0.0`, meaning Consul will bind to all addresses on the local machine and will advertise the private IPv4 address to the rest of the cluster.

#### Register a Service with Haashcorp Consul

An easy way to register a service in Consul is to request the `/v1/agent/service/register` endpoint of Consul’s [Catalog HTTP API](https://www.consul.io/api-docs/catalog).

Consul does not allow you to directly specify an extra path of your service when registering it.

To overcome this limitation, Gravitee.io supports extra `Meta` attributes in addition to the standard `Address` attribute.

Meta attributes must be provided as part of the definition of your service:

{% code overflow="wrap" %}
```
curl -X PUT -d '{ "ID": "whattimeisit_1", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/whattimeisit", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```
{% endcode %}

Check the Consul web UI and you should see the new service named `whattimeisit`:

<figure><img src="../../../.gitbook/assets/service-discovery-consul-services.png" alt=""><figcaption></figcaption></figure>

You can also verify that your service is successfully registered in Consul by interacting with Consul Agent API. To do so, se the following cURL command:

```
curl "http://localhost:8500/v1/agent/service/whattimeisit"
```

You should get the following response:

```
{
   "ID":"whattimeisit",
   "Service":"whattimeisit",
   "Tags":[

   ],
   "Meta":{
      "gravitee_path":"/whattimeisit",
      "gravitee_ssl":"true"
   },
   "Port":443,
   "Address":"api.gravitee.io",
   "Weights":{
      "Passing":1,
      "Warning":1
   },
   "EnableTagOverride":false,
   "ContentHash":"d43a25497735099",
   "Datacenter":"dc1"
}
```

In order to test that incoming requests on APIM gateway are dynamically routed to different service instances, let’s register another instance for service `whattimeisit` that serves a different content with `gravitee_path` set to `/echo`:

{% code overflow="wrap" %}
```
curl -X PUT -d '{ "ID": "whattimeisit_2", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/echo", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```
{% endcode %}



### Eureka Service Discovery
