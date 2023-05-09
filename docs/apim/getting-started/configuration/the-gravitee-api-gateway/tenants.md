---
description: Learn how to configure tenants.
---

# Tenants

## Introduction

Tenants are a way to leverage Gravitee multi-endpoints capabilities (i.e. the ability to specify multiple upstream systems per single API). Gravitee allows you to assign an endpoint to a specific tenant so the request will be proxied to a different endpoint, depending on which tenant the Gateway has been tagged with.

## Configuring Tenants <a href="#9c4f" id="9c4f"></a>

Similar to sharding tags, tenant configuration is also a two-step process. You will need to “tag” a Gateway to identify in which region it has been deployed. You will do this by adding the following setting to each Gateway’s _`gravitee.yaml`_ configuration file:

```
# Multi-tenant configuration
# Allow only a single-value
USA Region: tenant: ‘tenant name’
EU Region: tenant: ‘tenant name’
```

For the rest of this article, we will tag all Gateways deployed in the USA region with “usa”. We will tag all EU-deployed Gayeways with "eu." The `gravitee.yaml` file will look as such:

```
# Multi-tenant configuration
# Allow only a single-value
USA Region: tenant: ‘usa’
EU Region: tenant: ‘eu’
```

Once the Gateway has been configured, you would need to add the tenant definition within the API Management UI. To do so, follow these steps:

1. Navigate to **Organization Settings** and select **Tenants**_**.**_ Select **Add a tenant**_**,**_ and enter the required value for each of your regions. For our example, this will be “usa” and “eu". We also recommend giving each tenant a descriptive name.

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*dqayn7uZPfVmyQgT" alt=""><figcaption></figcaption></figure>

2. Next, Configure the Backend and Customer APIs by adding two separate “Endpoints”. For our example, this will point to the USA and EU upstream systems (the backend server or the Customer API depending on which API you are configuring).

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*en1j7FLNVLWpoOkn" alt=""><figcaption></figcaption></figure>

You will also have the ability to specify which tenant this backend will apply to. You now have two endpoints defined, each pointing to different backends, and each one is assigned to a different tenant:

<figure><img src="https://miro.medium.com/v2/resize:fit:1400/0*ZhfPrNuU0Aa7YQ8c" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Nicely done!

So, now that you have the two endpoints defined, Gateways GWI1, GWI2, GWI3 and GWI4 will apply this logic:

* If my tenant configuration is “eu” then proxy a request to Backend API to [https://us.backend-api.mycompany.com](https://us.backend-api.mycompany.com/)
* If my tenant configuration is “usa” then proxy a request to Backend API to [https://usa.backend.com](https://usa.backend.com/)

On the same lines, Gateways GWE1, GWE2, GWE3, GWE4 will apply the following logic when serving partners requests to the Customer API:

* If my tenant configuration is “eu” then proxy a request to Customer API to [https://eu.backend-api.com](https://eu.backend.com/)
* If my tenant configuration is “usa” then proxy a request to Backend API to [https://usa.backend-api.com](https://usa.backend.com/)
{% endhint %}

[\
](https://medium.com/tag/gravitee?source=post\_page-----471f4d3c49a9---------------gravitee-----------------)
