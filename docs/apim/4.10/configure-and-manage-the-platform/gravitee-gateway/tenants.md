---
description: An overview about tenants.
metaLinks:
  alternates:
    - tenants.md
---

# Tenants

Overview

Tenants are a way to leverage Gravitee's multi-endpoint capability, which is the ability to specify multiple upstream systems per single API. Gravitee allows you to assign endpoints and Gateways to specific tenants to control the endpoints to which requests are proxied.

## Tagged Gateway / API endpoint behavior

Endpoint deployment is impacted by how tags are applied to API endpoints and Gateways.

### Rules

* A Gateway that is not configured with a tenant deploys all API endpoints, regardless of whether the endpoint has a tenant.
* An API endpoint that is not configured with a tenant is deployed to all Gateways, regardless of whether the Gateway is configured with a tenant.
* A Gateway configured with the tenant `foo` deploys all API endpoints that include `foo` in their tenant list.

## Configuring Tenants <a href="#id-9c4f" id="id-9c4f"></a>

To explain tenant usage and behavior, we will build off of our example use case for [sharding tags](sharding-tags.md#configure-sharding-tags-for-your-gravitee-api-gateways). A single API can be deployed to many different Gateways and endpoints, but by using sharding tags you can specify the target Gateway(s), and by using tenants you can specify the target endpoint(s).

Similar to sharding tags, tenant configuration is a two-step process. You must “tag” a Gateway to identify in which region it has been deployed. To demonstrate, we will add the following configuration to each Gateway's `gravitee.yaml` file, where all USA-deployed Gateways are tagged with "usa" and all EU-deployed Gateways are tagged with "eu"

```yaml
# Multi-tenant configuration
# Allow only a single-value

# USA Region:
tenant: 'usa'

# ...or...

# EU Region:
tenant: 'eu'
```

Once the Gateway has been configured, the tenant definition must be added via the API Management Console:

1.  Navigate to **Organization Settings** and select **Tenants**_**.**_ Select **Add a tenant** and enter the value for each of your regions, e.g., “usa” and “eu." We also recommend giving each tenant a descriptive name.

    <div align="left"><figure><img src="../../.gitbook/assets/tenant_create (1).png" alt="" width="375"><figcaption></figcaption></figure></div>
2.  Next, configure the Backend and Customer APIs by adding two different endpoints. In our example, these will point to the USA and EU upstream systems (the backend server or the Customer API, depending on which API you are configuring).

    <figure><img src="../../.gitbook/assets/tenant_BE &#x26; customer.png" alt=""><figcaption></figcaption></figure>
3.  Specify which tenant a backend will apply to. Our two endpoints each point to different backends and are each assigned to a different tenant:

    <figure><img src="../../.gitbook/assets/tenant_specify (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Now that the two endpoints are defined, Gateways GWI1, GWI2, GWI3 and GWI4 will apply this logic:

* If a tenant configuration is “eu,” a request to Backend API is proxied to `https://eu.backend.com`
* If a tenant configuration is “usa,” a request to Backend API is proxied to `https://usa.backend.com`

Similarly, Gateways GWE1, GWE2, GWE3, GWE4 will apply the following logic when serving partner requests to the Customer API:

* If a tenant configuration is “eu,” a request to Customer API is proxied to `https://eu.customer-api.com`
* If a tenant configuration is “usa,” a request to Backend API is proxied to `https://usa.backend-api.com`
{% endhint %}

### Tenant-based endpoint selection

When a Gateway has a tenant configured, it selects the first valid endpoint from the first Endpoint Group. An endpoint is considered valid if it meets one of the following criteria:

* The endpoint has no tenant configuration (shared endpoint)
* The endpoint has a tenant configuration that exactly matches the tenant configured on the Gateway

#### Selection rules

The Gateway applies the following logic when selecting an endpoint:

1. **Gateway without tenant**: Selects the first endpoint from the first Endpoint Group, regardless of tenant configuration.
2. **Gateway with tenant**: Selects the first valid endpoint from the first Endpoint Group where:
   * The endpoint has no tenant configuration, **or**
   * The endpoint's tenant list includes the Gateway's configured tenant

Endpoints whose tenant configuration does not match the Gateway's tenant are ignored. If no valid endpoint is found after tenant filtering, the Gateway returns a `503 No endpoint available` error.

{% hint style="info" %}
Only the first Endpoint Group is considered for selection. Future releases may introduce additional configuration options (e.g., Dynamic Routing Policy) to enable selection from other endpoint groups.
{% endhint %}

#### Priority order

Endpoints are evaluated in the order they appear within the Endpoint Group. The first valid endpoint is selected and used for all requests routed through that Gateway.

<!-- GAP: No information provided about how endpoint order is configured or modified in the Console UI -->