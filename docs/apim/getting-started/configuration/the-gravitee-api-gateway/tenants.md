---
description: Learn how to configure tenants.
---

# Tenants

## Introduction

Tenants are a way to leverage Gravitee multi-endpoints capabilities (i.e. the ability to specify multiple upstream systems per single API). Gravitee allows you to assign an endpoint to a specific tenant so the request will be proxied to a different endpoint, depending on which tenant the Gateway has been tagged with.

## Revisiting the scenario <a href="#edd8" id="edd8"></a>

To shed more light on tenants, let's start by revisiting a scenario that we [introduced in our documentation on sharding tags](../configure-sharding-tags-for-your-gravitee-api-gateways.md). In the diagram below, we have an example of a typical deployment an organization may use for their API Management.&#x20;

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*hrzp_87Mxed4QdvD" alt=""><figcaption><p>Example of cross-region deployment</p></figcaption></figure>

This scenario has two APIs deployed in a distributed manner, providing high availability across different regions and in different network environments.

There are three requirements to address:

1. Ensure the Customer API is deployed to the Gateways available within the DMZ network.
2. Ensure the Backend API is deployed to internal Gateways.
3. To avoid high latency, we need to ensure that a request hitting a Gravitee Gateway in the US region only proxies that request to an upstream API deployed in the US. In Gravitee parlance, we need to instruct Gravitee to select the right API _endpoint_ based on the region where the Gateway has been deployed.

Sharding tags allowed us to take care of the first two requirements. We now want to address our final requirement. We will do this via tenants.

Since the API will be deployed to all Gatewayd with a sharding tag of “internal” or “external” from our previous example, we want to find a way to “tag” upstream systems so that the API deployed in a certain region will only forward the request to an upstream system in the same region. Tenants allow you to assign API endpoints (i.e. upstream systems) to certain Gateways so that the Gateway will proxy the request to the endpoint assigned to the tenant the Gateway itself has been tagged with.

Let’s look at how upstream endpoints would be assigned to tenants based on the architecture above, taking into account the Backend API:

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/1*qzd6GYJKZ_qLtXuhSC8hIQ.png" alt=""><figcaption></figcaption></figure>

In this example, when a request hits the Backend API within the US, GWI1 or GWI2 will forward the request to [https://us.backend-api.mycompany.com](https://us.backend-api.mycompany.com/) (“DB — USA Replica” in the architecture diagram). This is because GWI1 and GWI2 have the tenant “usa” assigned, and the endpoint [https://us.backend-api.mycompany.com](https://us.backend-api.mycompany.com/) is also assigned to tenant “usa”.

Let’s take a look at how to get this configured within the product.

## Configuring Tenants <a href="#9c4f" id="9c4f"></a>

Similar to sharding tags, tenant configuration is also a two-step process. You will need to “tag” a Gateway to identify in which region it has been deployed. You will do this by adding the following setting to each Gateway’s _gravitee.yaml_ configuration file:

```
# Multi-tenant configuration
# Allow only a single-value
USA Region: tenant: ‘usa’
EU Region: tenant: ‘eu’
```

So, in this example, you would tag all Gateways deployed in the USA region with “usa”. The same will be done to all Gateways deployed in the EU.

The same setting should also be applied to the Gateways hosting the Customer API. This will allow the Customer API to hit a Backend API’s load balancer in the same region (refer to the architecture diagram) to avoid cross-region traffic.

Once the Gateway has been configured, you would need to add the tenant definition within API Manager.

Navigate to _**Organization Settings**_ and click on _**Tenants.**_ Click on _**Add a tenant**_ and enter the required value for each of our regions: “usa” and “eu”:

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*dqayn7uZPfVmyQgT" alt=""><figcaption></figcaption></figure>

Now that the tenants have been added within API Manager, you will need to configure the Backend and Customer APIs by adding two separate “Endpoints”. These will point to the USA and EU upstream systems (the backend server or the Customer API depending on which API you are configuring).

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*en1j7FLNVLWpoOkn" alt=""><figcaption></figcaption></figure>

Note how, when specifying a new backend, we will also have the ability to specify which tenant this backend will apply to. We now have two endpoints defined pointing to different backends, and each one is assigned to a different tenant:

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*ZhfPrNuU0Aa7YQ8c" alt=""><figcaption></figcaption></figure>

So, now that you have the two endpoints defined, Gateways GWI1, GWI2, GWI3 and GWI4 will apply this logic:

* If my tenant configuration is “eu” then proxy a request to Backend API to [https://us.backend-api.mycompany.com](https://us.backend-api.mycompany.com/)
* If my tenant configuration is “usa” then proxy a request to Backend API to [https://usa.backend.com](https://usa.backend.com/)

On the same lines, Gateways GWE1, GWE2, GWE3, GWE4 will apply the following logic when serving partners requests to the Customer API:

* If my tenant configuration is “eu” then proxy a request to Customer API to [https://eu.backend-api.com](https://eu.backend.com/)
* If my tenant configuration is “usa” then proxy a request to Backend API to [https://usa.backend-api.com](https://usa.backend.com/)

## Wrapping it up <a href="#4c11" id="4c11"></a>

In this blog we’ve provided a definition of what tenants are, along with an example that would typically be seen by an organization looking to deploy APIs for different requirements.

We have also shown you a step-by-step approach on how to configure tenants for your deployment, based on a typical architecture common to many organizations.

Tenants can be used to help the Gateway choose which upstream endpoint an API should invoke. This is particularly important when you have different replicas of your upstream API and, in order to reduce latency, you want to ensure the closest possible backend is consumed. This is a rather common challenge in multi-layered API architectures like the one described in this article.

[\
](https://medium.com/tag/gravitee?source=post\_page-----471f4d3c49a9---------------gravitee-----------------)
