# Hashicorp Consul Service Discovery

API Service - Service Discovery Consul

Existing doc: [https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html](https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html)

No changes in the following chapters:

## Introduction

[https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#introduction](https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#introduction)

## Prerequisites

[https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#prerequisites](https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#prerequisites)

## Install HashiCorp Consul Server

[https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#install\_hashicorp\_consul\_server](https://docs.gravitee.io/apim/3.x/apim\_service\_discovery\_consul.html#install\_hashicorp\_consul\_server)

## Register a Service with HashiCorp Consul

An easy way to register a service in Consul is to request the endpoint of Consul’s [Catalog HTTP API](https://www.consul.io/api-docs/catalog): `/v1/agent/service/register`&#x20;

Consul does not allow you to directly specify an extra path of your service when registering it.

To overcome this limitation, Gravitee.io supports additional `Meta` attributes besides the standard `Address` attribute.

Meta attributes must be provided as part of the definition of your service:

* `gravitee_path` to specify on which path your service is reachable.
* `gravitee_ssl` to specify whether your service should be called with `http://` or `https://` scheme.\`
* `gravitee_weight` to set a weight on the endpoint to affect the load balancing.
* `gravitee_tenant` to set a tenant value in the endpoint.

Below is a cURL command example to register a service in Consul with extra attributes supported by Gravitee.io:

```
curl -X PUT -d '{ "ID": "whattimeisit_1", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/whattimeisit", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```

Check the Consul web UI, and you should see a new service named `whattimeisit`:

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/W8hm_gmyQVsGbszdfSUQektC.png" alt=""><figcaption></figcaption></figure>

By interacting with Consul Agent API, you can also verify that your service is successfully registered in Consul.

Use the following cURL command:

```
curl "http://localhost:8500/v1/agent/service/whattimeisit"
```

You should get a response as follows:

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

To test that incoming requests on the APIM gateway are dynamically routed to different service instances, let’s register another instance for service `whattimeisit` that serves another content with `gravitee_path` set to `/echo`:

```
curl -X PUT -d '{ "ID": "whattimeisit_2", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/echo", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```

## Enable Consul Service Discovery in Gravitee.io APIM

The service discovery feature is enabled at the EndpointGroup level of an API definition

```yaml
    "endpointGroups": [
        {
            "name": "default-group",
            "type": "http-proxy",
            "services": {
                "discovery": {
                    "enabled": true,
                    "type": "consul-service-discovery",
                    "configuration": {
                        "url": "http://localhost:8500",
                        "service": "whattimeisit"
                    }
                }
            },
            "endpoints": []
        }
    ],
```

## Verify that the APIM gateway properly discovers your service

You can check the API gateway’s logs to verify that your service has been successfully found thanks to HashiCorp Consul:

```
INFO  i.g.a.p.a.s.c.ConsulServiceDiscoveryService - Starting service discovery service for api my-api.
INFO  i.g.g.r.c.v.e.DefaultEndpointManager - Start endpoint [consul#whattimeisit_1] for group [default-group]
```

You can now try to call your API to ensure incoming API requests are routed to the appropriate backend service.

You can also deregister your service instance from Consul by referring to their ID and calling your API again to observe how APIM dynamically routes the traffic based on Consul’s Service Catalog.

```
curl -X PUT -v "http://localhost:8500/v1/agent/service/deregister/whattimeisit"
```

**You learned how to integrate Gravitee.io APIM gateway with HashiCorp Consul, enabling dynamic load balancer configuration changes pulled directly from Consul’s service discovery registry.**
