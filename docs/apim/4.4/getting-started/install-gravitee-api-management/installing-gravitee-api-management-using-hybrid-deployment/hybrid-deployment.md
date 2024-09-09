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

* An HTTP B_ridge_ Server  (APIM Gateway as shown in green in the diagram above) exposes extra HTTP services for bridging HTTP calls to the underlying repository, which can be any of our supported repositories: MongoDB, JDBC, etc.
* A _standard_ APIM Gateway (shown in red in the diagram above) with the default repository plugin switched to the bridge repository plugin.

In this infrastructure, the standard APIM Gateway can communicate with the bridge APIM Gateway through an HTTP/S channel, and your cloud data center does not need to have a datastore installed.

## HTTP Bridge server

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, Bridge Server are an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/gravitee-apim-enterprise-edition/)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

What we describe as an _HTTP Bridge server_ is a standard APIM Gateway or APIM Management API workload (if you prefer to limit the number of components to deploy) augmented with a set of plugins.

By default, an APIM Gateway needs to connect to a repository (e.g., mongoDB) to retrieve the list of APIs, plans, subscriptions, etc.&#x20;

When deployed in a more complex environment (with network zones, different data centers, etc.), there are concerns associated with an open connection to a database outside the network. The solution is to deploy a HTTP Bridge server. It acts like a proxy for the database and allows an APIM Gateway to access it via HTTP instead of the native database protocol: API Gateway > HTTP Bridge Server > Database.

### **Basic installation**

In APIM 4.x, the bridge plugin is part of the default bundle (in both the API Gateway and Management API), so there is no specific installation step to prepare for deploying a hybrid architecture.

### **Basic configuration**

Enable and configure the plugin in the `gravitee.yaml` file.

{% code title="gravitee.yml" %}
```yaml
services:
  bridge:
    http:
      enabled: true
      port: 18092
      authentication:
        type: none  # no auth
      secured: false # plain text
```
{% endcode %}

### **Check the HTTP bridge server node is running**

You can test that your HTTP Bridge server node is running by sending an HTTP request to port `18092` on `localhost`:

```sh
curl http://localhost:18092/_bridge/environments/_byOrganizationsAndHrids
```

This should receive an empty JSON array.

{% hint style="info" %}
Be sure to setup an authentication and secure your connection once you have tested you setup work
{% endhint %}

### **Advanced configuration example**

Here we configure basic authentication, alpn, TLS and mTLS using PEM files&#x20;

{% code title="gravitee.yml" %}
```yaml
services:
  bridge:
    http:
      enabled: true
      port: 18092
      host: 0.0.0.0
      alpn: true
      authentication:
        # default is 'basic'
        type: basic # others are 'none', 'jwt'
        users:
          admin: adminadmin
        # jwt:
        #      signature:
        #        algorithm: RS256
        #        path: ${gravitee.home}/security/bridge/public_key.pem
        #        # path and value mutually exclusive
        #        value: <public key pem with headers>
        #      verifyClaims: true
      secured: true
      ssl:
        clientAuth: request # can 'none' (no mTLS) '
        keystore:
          type: pem # can be 'jks' or 'pkcs12'
          watch: true # enable hot reload in all cases
          # for keystores
          # path: 
          # password:
          certificates: 
            - cert: ${gravitee.home}/security/bridge/cert.pem
              key: ${gravitee.home}/security/bridge/key.pem
          # alternative to "certificates"
          # secret: secret://kubernetes/bridge-server-tls
        truststore:
          type: pem # can be 'jks' 'pkcs12'
          path: ${gravitee.home}/security/bridge-mtls-ca.pem
          password: # for keystores only
          # for pem only
          # secret: secret://kubernetes/bridge-server-mtls:ca.crt
```
{% endcode %}

## Standard APIM Gateway - HTTP repository (client)

### Basic installation

In APIM 4.x, http repository plugin is part of the default bundle, so there is no specific installation step to prepare for deploying a hybrid architecture.

{% hint style="info" %}
Make sure that authentication type between HTTP repository and Bridge Server match (as well as TLS configuration)

The following are just examples to expose configuration options.
{% endhint %}

### **Basic configuration**

Configure the new plugin in the `gravitee.yaml` file in the APIM Gateway `config` directory.

{% code title="gravitee.yml" %}
```yaml
management:
  type: http
  http:
    url: "http://localhost:18092"
    authentication:
      type: basic # 'none' to disable auth
      basic:
        username: admin
        password: adminadmin    
```
{% endcode %}

### Example advanced configuration

Here we configure the client to use a JWT token for authentication,  http/2, custom CA in a PEM file for  TLS and mTLS using a p12 keystore. We also expose all configuration parameters with most of their default values.

{% code title="gravitee.yaml" %}
```yaml
management:
  type: http
  http:
    url: "https://bridge.example.com:18092"
    # will add /_bridge to the URL 
    appendBridgeBasePath: true
    # default
    keepAlive: true
    idleTimeout: 30000
    connectTimeout: 5000
    readTimeout: 10000
    useCompression: true
    # HTTP_1_1 by default
    version: HTTP_2
    # retry less and less often until we reach 60s (default)
    connectionRetry:
      delaySec: 2
      maxDelaySec: 60
      backoffFactor: 1.5 # how exponential we get to 60s (1 means linear)
    authentication:
      type: jwt
      jwt:
        token: eyJhbGciOiJIUzI1NiI...  
    ssl:
      # defaults
      ### beware: since 4.4 default is false (see upgrade guide) 
      trustAll: false
      verifyHostname: true
      # custom config for mTLS
      keystore:
        type: pkcs12 # can be jks / pkcs12 / pem
        path: ${gravitee.home}/security/bridge/mtls-keystore.p12
        password: s3cr3t
        # for pem 
        # certPath: ${gravitee.home}/security/mtls-bridge-cert.pem
        # keyPath: ${gravitee.home}/security/mtls-bridge-key.pem
        # certContent: secret://...  # raw pem, same for 
        # keyContent: ...
      # config for non public CAs
      truststore:
        type: pem # can be jks / pkcs12 / pem
        path: ${gravitee.home}/security/bridge/rootCA.pem
        # for jks/pkcs12
        # password:
   # proxy:
   #   enabled: true
   #   host: proxy.example.com
   #   port: 8080
   #   username: proxy
   #   password: pa$$w0rd
   #   type: HTTP
   #   # useSystemProxy: true # reuses apim-gateway proxy config for other services 
        
```
{% endcode %}

### Start the APIM Gateways

Start the HTTP Bridge server and then _standard APIM Gateways_.&#x20;

Your API consumers will be able to call the _standard APIM Gateway_ as usual; APIs, plans, subscriptions etc. will synchronise transparently via HTTP.
