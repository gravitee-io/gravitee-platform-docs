---
description: >-
  This article walks through how to configure service discovery if using either
  the HashiCorp Consul Service Discovery solution.
---

# Service Discovery

### Introduction

Gravitee supports the following Service Discovery solutions:

* HashiCorp Consul

Please read the following documentation to learn how to configure both.

### Configure HashiCorp Consul Service Discovery

Gravitee.io Service discovery for HashiCorp Consul allows you to bind the backend endpoints of your API to a service managed by HashiCorp Consul so that API requests are always routed to the proper, healthy backend service dynamically managed by HashiCorp Consul.

#### prerequisites

We will be using docker-compose to setup an integration between Gravitee APIM and HashiCorp Consul.

Refer to this [guide](../../../getting-started/install-and-upgrade-guides/install-on-docker/README.md) to install Gravitee with Docker Compose.

#### Install HashiCorp Consul Server

The first step is to install a Consul server. Consul agents that run in server mode become the centralized registry for service discovery information in your network. They answer queries from other Consul agents about where a particular service can be found. For example, if you ask them where the log service is running, they may return to you that it is running on three machines, with these IP addresses, on these ports. Meanwhile, services such as the log service register themselves with the Consul clients so that they can become discoverable.

Read the [official Consul documentation](https://www.consul.io/docs/install) to see how to install a Consul server.

To get started, edit the _docker-compose.yml_ used to install Gravitee and declare an additional service for Consul server as follows:

```
consul-server:
    image: hashicorp/consul:1.15.4
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
     - storage
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

#### Register a Service with HashiCorp Consul

An easy way to register a service in Consul is to request the `/v1/agent/service/register` endpoint of Consul’s [Catalog HTTP API](https://www.consul.io/api-docs/catalog).

Consul does not allow you to directly specify an extra path of your service when registering it.

To overcome this limitation, Gravitee supports extra `Meta` attributes in addition to the standard `Address` attribute.

Meta attributes must be provided as part of the definition of your service:

* `gravitee_path` to specify on which path your service is reachable.
* `gravitee_ssl` to specify whether your service should be called with `http://` or `https://` scheme.\`
* `gravitee_weight` to set a weight on the endpoint to affect the load balancing.
* `gravitee_tenant` to set a tenant value in the endpoint.

Below is a cURL command example to register a service in Consul with extra attributes supported by Gravitee.io:

```shell
curl -X PUT -d '{ "ID": "whattimeisit_1", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/whattimeisit", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```

Check the Consul web UI, and you should see the new service named `whattimeisit`:

<figure><img src="../../../.gitbook/assets/service-discovery-consul-services.png" alt=""><figcaption></figcaption></figure>

You can also verify that your service is successfully registered in Consul by interacting with Consul Agent API. To do so, se the following cURL command:

```shell
curl "http://localhost:8500/v1/agent/services"
```

You should get the following response:

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

To test that incoming requests on the APIM Gateway are dynamically routed to different service instances, let’s register another instance for service `whattimeisit` that serves another content with `gravitee_path` set to `/echo`:

{% code overflow="wrap" %}
```shell
curl -X PUT -d '{ "ID": "whattimeisit_2", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/echo", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```
{% endcode %}

#### Enable Consul Service Discovery in Gravitee API Management

The service discovery feature is enabled at the EndpointGroup level of an API definition:

```
"endpointGroups": [
    {
        "name": "default-group",
        "type": "http-proxy",
        "services": {
            "discovery": {
                "enabled": true,
                "type": "consul-service-discovery",
                "configuration": {
                    "url": "http://consul-server:8500",
                    "service": "whattimeisit"
                }
            }
        },
        "endpoints": []
    }
],
```

Now that you've successfully registered your service instances in Hashicorp Consul, you can enable Hashicorp Consul Service discovery in the Gravitee AP Management Console. To do so, follow these steps:

1. Log in to your Gravitee API Management Console.
2. Either create or select an existing API.

![](https://dubble-prod-01.s3.amazonaws.com/assets/c0164628-49f4-42df-8823-5621fa9339b7.png?0)

3\. Select the **Edit API** icon.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/3e87572b-26b0-4f4e-8f76-99c099d47aa9/1/95.833333333333/49.307436790506?0)

4\. In the **Proxy** section, select **Backend services**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0beadecd-489d-4200-b39a-ac23ad3f033a/1/15.046296296296/55.830753353973?0)

5\. In the **Endpoints** tab, select **Edit group**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/143d94ca-f2f6-4b91-9598-941d251b1006/1.5/87.883391203704/26.625386996904?0)

6\. Select **Service discovery**

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/935ba02e-2c16-4313-8c51-00d5b5ce43f9/2.5/52.611626519097/15.376676986584?0)

7\. Toggle **Enabled service discovery** ON.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/cc47712b-d288-46eb-ace9-c63bf88c88c8/2.5/35.619212962963/25.386996904025?0)

8\. Select **Consul.io Service Discovery** from the **Type** dropdown.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/d17cb969-d679-4960-8806-a5d1bc5646b0/1.2507598784195/64.178240740741/32.992292311662?0)

9\. Enter the name of the service registered in Consul. For this article, it is "whattimeisit."

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f23c9553-10b2-4ef0-96c4-44bc3fb1fd14/1/64.178240740741/106.73374613003?0)

10\. Define your **DC** setting. "DC" refers to the consul datacenter. This is an optional part of the Fully Qualified Domain Name (FQDN). If not provided, it defaults to the datacenter of the agent. Refer to [this documentation](https://developer.hashicorp.com/consul/docs/architecture) for more details.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/dab3173b-6d55-45c0-8770-6b8e4c270ed5/1/64.178240740741/105.16560242518?0)

11\. Define **ACL** settings. This is where you provide the ACL token if you’ve secured the access to Consul. For more information on how to setup ACLs, refer to [this ACL tutorial](https://developer.hashicorp.com/consul/tutorials/security/access-control-setup-production).

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/bce05dbf-c51c-46f5-8256-413abe3c2f48/1/64.178240740741/105.16560242518?0)

12\. Define your **Truststore Type**. You can select the type of truststore (Java KeyStore or PKCS#12) storing the certificates that will be presented from the Consul agent to Gravitee during the secure connection handshake (SSL/TLS). When selecting None (Trust All) you configure Gravitee to trust all certificates presented by Consul during the connection handshake. You can either copy/paste the content of your Truststore directly in the Truststore content field or provide the path to you external Truststore in the Truststore path field. At least one of the two must be provided.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/9b92b3a6-d5a3-46c6-a6de-9977c0948dd6/1/64.178240740741/81.636190660475?0)

13\. Define your **KeyStore Type**. You can select the type of keystore (Java KeyStore or PKCS#12) storing certificates that will be presented by Gravitee to the Consul agent during the secure connection handshake (SSL/TLS). You can either copy/paste the content of your keystore directly in the KeyStore content field or provide the path to you external Keystore in the KeyStore path field. At least one of the two must be provided.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f0085922-f6da-4ee7-8606-93fadeee3747/1/64.178240740741/47.786861455108?0)

{% hint style="success" %}
Select **Save** to finish configuring your Service discovery settings. Your API should now appear out of sync in the top banner. Be sure to click **deploy your API**.
{% endhint %}

Please note that endpoints configured through the APIM console before service discovery was enabled are not removed. The Gravitee Gateway will continue to consider those endpoints in addition to the ones discovered through Consul integration. The endpoints dynamically discovered through Consul are not displayed in the Gravitee API Management (APIM) UI. You can remove the defined endpoints through the Gravitee APIM UI. However, we encourage you to keep at least one endpoint declared as secondary. Secondary endpoints are not included in the load-balancer pool and are only selected to handle requests if Consul is no longer responding. To declare an endpoint as secondary, please follow these steps:

1\. In the **Backend services** section, locate your endpoint that you want to define as secondary. For that endpoint, select **Edit endpoint**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/373fcf82-31ee-4b3b-96ac-a3272c3e24a2/1.5/92.523758499711/38.38616244195?0)

2\. Select the **Secondary endpoint** checkbox. Select **Save**.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ef0dd779-712f-4dfd-9d8c-938f000d3dbe/2.5/35.474537037037/76.989809081527?0)

## Verify that the APIM Gateway properly discovers your service

You can check the API Gateway’s logs to verify that your service has been successfully found thanks to HashiCorp Consul:

```
INFO  i.g.a.p.a.s.c.ConsulServiceDiscoveryService - Starting service discovery service for api my-api.
INFO  i.g.g.r.c.v.e.DefaultEndpointManager - Start endpoint [consul#whattimeisit_1] for group [default-group]
```

You can now try to call your API to ensure incoming API requests are routed to the appropriate backend service.

You can also deregister your service instance from Consul by referring to their ID and calling your API again to observe how APIM dynamically routes the traffic based on Consul’s Service Catalog.

```shell
curl -X PUT -v "http://localhost:8500/v1/agent/service/deregister/whattimeisit_1"
```

{% hint style="success" %}
You've now integrated the Gravitee API Gateway with HashiCorp Consul, which enables dynamic load balancer configuration changes that are pulled directly from Consul’s service discovery registry.
{% endhint %}

{% hint style="info" %}
**Additional considerations if integrating Gravitee with HashiCorp Consul:**

If you have integrated Gravitee and HashiCorp Consul for Service Discovery, you may want to enable health checks for your API. This will allow you to view the status of all endpoints under the Per-endpoint availability section in Gravitee, including the endpoints managed by HashiCorp Consul. For more details on how to enable Gravitee health checks, refer to [this documentation](load-balancing-failover-and-health-checks.md#configure-gravitee-health-checks).

<img src="../../../.gitbook/assets/service-discovery-consul-healthcheck.png" alt="" data-size="original">
{% endhint %}
