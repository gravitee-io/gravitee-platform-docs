---
description: >-
  This article describes how to configure service discovery using the HashiCorp
  Consul solution
---

# Service Discovery

## Introduction

Gravitee service discovery for HashiCorp Consul allows you to bind the backend endpoints of your API to a service dynamically managed by HashiCorp Consul so that API requests are always routed to the proper, healthy backend service. By integrating the Gateway with HashiCorp Consul, dynamic load-balancer configuration changes are pulled directly from Consul’s service discovery registry.

The following sections describe how to:

* [Configure HashiCorp Consul](service-discovery.md#configure-hashicorp-consul)
* [Establish secondary endpoints](service-discovery.md#secondary-endpoints)
* [Verify service discovery and traffic routing](service-discovery.md#verification)

## Configure HashiCorp Consul

### prerequisites

* [Install Gravitee with `docker-compose`](../../../../installation-and-upgrades/install-on-docker/)

### 1. Install a HashiCorp Consul server

Consul agents that run in server mode become the centralized registry for service discovery information in your network. Services registered with Consul clients are discoverable, and Consul servers can answer queries from other Consul agents about where a particular service is running, e.g., returning IP addresses and port numbers.

{% hint style="info" %}
Refer to the [official Consul documentation](https://www.consul.io/docs/install) to learn how to install a Consul server.
{% endhint %}

To use `docker-compose` to set up an integration between Gravitee APIM and HashiCorp Consul:

1.  Edit the `docker-compose.yml` used to install Gravitee and declare an additional service for the Consul server. The example below declares a read-only volume to mount the directory containing Consul configuration files.

    \{% code overflow="wrap" %\}

    ```bash
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

    \{% endcode %\}
2.  Consul containers load their configuration from `/consul/config/` at startup. Use the `server.json` below to initialize the Consul server:

    \{% code overflow="wrap" %\}

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

    \{% endcode %\}

    * `server=true` indicates that this Consul agent should run in server mode
    * Consul’s web UI is enabled by setting the `enabled` sub-key of the `ui_config` attribute to `true`
    * Once Consul server’s container is running, Consul’s web UI is accessible at port `8500`
    * The `addresses` field specifies the address that the agent will listen on for communication from other Consul members. By default, this is `0.0.0.0`, meaning Consul will bind to all addresses on the local machine and will advertise the private IPv4 address to the rest of the cluster.

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
```

The Consul web UI should display a new service named `whattimeisit`:

<figure><img src="../../../../../../../.gitbook/assets/service-discovery-consul-services (1).png" alt=""><figcaption></figcaption></figure>

You can also verify that your service is successfully registered in Consul by interacting with Consul Agent API.

1.  Run the command below:

    \{% code overflow="wrap" %\}

    ```bash
    curl "http://localhost:8500/v1/agent/services"
    ```

    \{% endcode %\}
2.  Verify the following response is returned:

    \{% code overflow="wrap" %\}

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

    \{% endcode %\}

To test that incoming requests on the APIM Gateway are dynamically routed to different service instances, register another instance for service `whattimeisit` that serves another client with `gravitee_path` set to `/echo`:

{% code overflow="wrap" %}
```shell
curl -X PUT -d '{ "ID": "whattimeisit_2", "Name": "whattimeisit", "Address": "api.gravitee.io", "Meta": {"gravitee_path":"/echo", "gravitee_ssl":"true" }, "Port": 443}' http://localhost:8500/v1/agent/service/register
```
{% endcode %}

### 3. Enable Consul service discovery in APIM

The service discovery feature is enabled at the `EndpointGroup` level of an API definition. The `service` field lists a service instance that has been successfully registered in HashiCorp Consul.

```json
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

To enable HashiCorp Consul service discovery in your APIM Console:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  Select **Endpoints** from the **Backend services** section of the inner left nav

    <figure><img src="../../../../../../../.gitbook/assets/v2 service discovery_endpoints (1).png" alt=""><figcaption></figcaption></figure>
5. Click **Edit group**
6. Click on the **Service discovery** tab
7.  Toggle **Enabled service discovery** ON, then configure the following:

    <figure><img src="../../../../../../../.gitbook/assets/v2 service discovery_configure (1).png" alt=""><figcaption></figcaption></figure>

    * **Type:** Select **Consul.io Service Discovery** from the drop-down menu
    * **Service:** Enter the name of the service registered in Consul, e.g., "whattimeisit"
    * **DC:** Enter the Consul data center name. This is an optional part of the Fully Qualified Domain Name (FQDN). Refer to [this documentation](https://developer.hashicorp.com/consul/docs/architecture) for more details.
    * **ACL:** Provide the ACL token if you’ve secured the access to Consul. For more information on how to setup ACLs, refer to [this ACL tutorial](https://developer.hashicorp.com/consul/tutorials/security/access-control-setup-production).
    * **Truststore Type:** Use the drop-down menu, where **NONE** (Trust All) configures Gravitee to trust all certificates presented by Consul during the secure connection handshake (SSL/TLS)
    * Copy/paste the content of your truststore directly into the **Truststore content** field and/or enter the path to your external truststore in the **Truststore path** field
    * **KeyStore Type:** Use the drop-down menu to select the type of keystore Gravitee will present to the Consul agent during the secure connection handshake (SSL/TLS)
    * Copy/paste the content of your keystore directly into the **KeyStore content** field or enter the path to your external keystore in the **KeyStore path** field
8. Click **Save**
9. Redeploy your API

{% hint style="info" %}
The endpoints dynamically discovered through Consul are not displayed in the APIM Console and do not replace endpoints that were previously configured. The Gateway will continue to use pre-existing endpoints in addition to those discovered via Consul.
{% endhint %}

## Secondary endpoints

APIM requires that at least one endpoint is defined in the Console, but this endpoint can be declared as secondary. Secondary endpoints are not included in the load-balancer pool and are only selected to handle requests if Consul is no longer responding.

To declare an endpoint as secondary:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  Select **Endpoints** from the **Backend services** section of the inner left nav

    <figure><img src="../../../../../../../.gitbook/assets/v2 service discovery_endpoints (1).png" alt=""><figcaption></figcaption></figure>
5. Click the pencil icon next to the endpoint you want to make secondary
6.  Under the **General** tab, click the box next to **Secondary endpoint**

    <figure><img src="../../../../../../../.gitbook/assets/v2 service discovery_secondary endpoint (1).png" alt=""><figcaption></figcaption></figure>
7. Click **Save**

## **Verification**

### Confirm service discovery

To confirm service discovery:

1.  Check the API Gateway’s logs to verify that your service has been successfully found by HashiCorp Consul:

    \{% code overflow="wrap" %\}

    ```bash
    INFO  i.g.a.p.a.s.c.ConsulServiceDiscoveryService - Starting service discovery service for api my-api.
    INFO  i.g.g.r.c.v.e.DefaultEndpointManager - Start endpoint [consul#whattimeisit_1] for group [default-group]
    ```

    \{% endcode %\}
2. Try to call your API to ensure incoming API requests are routed to the appropriate backend service.

### Observe traffic routing

To observe how APIM dynamically routes traffic based on Consul’s Service Catalog:

1.  Deregister your service instance from Consul by referring to it's ID:

    ```bash
    curl -X PUT -v "http://localhost:8500/v1/agent/service/deregister/whattimeisit_1"
    ```
2. Call your API

{% hint style="info" %}
**Additional considerations**

Consider enabling health-checks for your API to view the status of all endpoints, including the endpoints managed by HashiCorp Consul. For more information on how to enable Gravitee health-checks, refer to [this documentation](load-balancing-failover-and-health-checks.md#configure-gravitee-health-checks).

<img src="../../../../../../images/apim/3.x/api-publisher-guide/service-discovery/service-discovery-consul-healthcheck (1).png" alt="" data-size="original">
{% endhint %}
