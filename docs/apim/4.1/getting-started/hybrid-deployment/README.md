---
description: An overview of hybrid deployments
---

# Hybrid Deployment

## Introduction

Hybrid architectures (i.e., a combination of on-premise and cloud deployments) present unique technical and/or cost constraints when deploying Gravitee API Management (APIM) components in different data centers.

The APIM hybrid deployment solution (in the form of hybrid components, or plugins) overcomes these constraints, giving you freedom and flexibility when defining your architecture and deployment.

## Architecture

The following diagram shows a typical hybrid APIM architecture:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_architecture.png" alt=""><figcaption><p>Hybrid deployment architecture</p></figcaption></figure>

## Configuration

For the APIM Gateway to work in this setup, you need two components:

* A _bridge_ API Gateway (shown in green in the diagram above) exposes extra HTTP services for bridging HTTP calls to the underlying repository, which can be any of our supported repositories: MongoDB, JDBC, etc.
* A _standard_ APIM Gateway (shown in red in the diagram above) with the default repository plugin switched to the bridge repository plugin.

In this infrastructure, the standard APIM Gateway can communicate with the bridge API Gateway through a secure HTTP/S channel, and your cloud data center does not need to have a datastore installed.

### **Bridge Gateways**

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, Bridge Gateways are an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/ee-vs-oss/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

What we describe as a _bridge_ API Gateway is a standard APIM Gateway augmented with a new plugin.

By default, an API Gateway needs to connect to a repository (e.g., mongoDB) to retrieve the list of APIs, plans, subscriptions, etc. When deployed in a more complex environment (with network zones, different data centers, etc.), there are concerns associated with an open connection to a database outside the network. The solution is to deploy a bridge Gateway, which acts as a proxy for the repository and allows for the sync between the API Gateway and database to take place over HTTP instead of the database protocol: API Gateway > bridge Gateway > database.

## HTTP bridge Gateway (server)

{% hint style="info" %}
The bridge plugin can be enabled on both the API Gateway and the Management API if you prefer to limit the number of components to deploy.
{% endhint %}

### **Basic installation**

In APIM 4.x, the bridge plugin is part of the default bundle (in both the API Gateway and Management API), so there is no specific installation step to prepare for deploying a hybrid architecture.

### **Basic configuration**

Configure the new plugin in the `gravitee.yaml` file.

{% code title="gravitee.yml" %}
```yaml
services:
  bridge:
    http:
      enabled: true
      port: 18092
      host: localhost
      authentication:
        # authentication type to be used for the core services
        # - none : to disable authentication
        # - basic : to use basic authentication
        # default is "basic"
        type: basic
        users:
          admin: adminadmin
      secured: true
      ssl:
        clientAuth: false
        keystore:
          type: # can be jks / pem / pkcs12
          path:
          password:
          certs: # Required for pem
            -  /path/to/cert
          keys:
            -  /path/to/key
        truststore:
          type: # can be jks / pem / pkcs12
          path:
          password:
```
{% endcode %}

### **Check the APIM Gateway (HTTP bridge server) node is running**

You can test that your APIM Gateway (HTTP bridge server) node is running by sending an HTTP request to port `18092` on `localhost`:

```sh
curl -X GET http://localhost:18092/_bridge/apis
```

You should receive a response containing an empty array or a list of APIs.

## Standard APIM Gateway - HTTP repository (client)

### **Basic installation**

To consume the HTTP bridge, you need to replace default repository plugins (usually a MongoDB repository) with a new HTTP repository in the APIM Gateway `plugins` directory. This plugin can be found [here](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-gateway-bridge-http-client/).

You can learn how to add this plugin to your deployment [here](../../overview/plugins.md#deployment).

### **Basic configuration**

Configure the new plugin in the `gravitee.yaml` file in the APIM Gateway `config` directory.

{% code title="gravitee.yaml" %}
```yaml
management:
  type: http
  http:
    url: http://localhost:18092/
    keepAlive: true
    idleTimeout: 30000
    connectTimeout: 10000
    authentication:
      basic:
        username: admin
        password: adminadmin
    ssl:
      trustAll: true
      verifyHostname: true
      keystore:
        type: # can be jks / pem / pkcs12
        path:
        password:
      truststore:
        type: # can be jks / pem / pkcs12
        path:
        password:
```
{% endcode %}

## Start the APIM Gateways

Start the bridge and standard APIM Gateways. Your consumers will be able to call the standard APIM Gateway with the HTTP repository as in a normal deployment.
