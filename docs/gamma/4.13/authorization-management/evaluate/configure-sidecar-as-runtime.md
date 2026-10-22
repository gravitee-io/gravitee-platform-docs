---
hidden: false
noIndex: false
description: Run a Gravitee Gateway beside your application as a sidecar, so the application asks for authorization decisions over localhost. Follow the steps to set one up.
---

# Configure a sidecar as runtime

A sidecar is a Gravitee Gateway that you deploy next to your application, for example in the same Kubernetes pod, so that the application asks for decisions over `localhost`. It's the same gateway as your other gateways: the PDP is part of the gateway bundle, and the sidecar gets its policies and entities through the same synchronization.

{% hint style="info" %}
For most environments, the gateways you already run are enough. See [Configure the Gravitee Gateway as a runtime](configure-gravitee-gateway-as-runtime.md). A sidecar is one more gateway to run and upgrade for each application.
{% endhint %}

## How it works

The sidecar gets a sharding tag of its own, and a PDP gateway registered with that tag gives it its own decision engine:

1. The sidecar gateway runs with its own sharding tag, for example `checkout-pod`.
2. A PDP gateway registered with the same sharding tag runs on the sidecar, with an AuthZEN endpoint.
3. Policies and entities that target this PDP gateway reach the sidecar.
4. The application sends AuthZEN requests to the endpoint on `localhost`.

{% hint style="warning" %}
Gateways with no sharding tag also get the sidecar's policies and answer its AuthZEN endpoint. To keep them on the sidecar only, give your other gateways sharding tags, or set `gamma.enabled: false` on the untagged ones. A gateway with Gamma disabled gets no authorization policies at all.
{% endhint %}

## Prerequisites

* A Gravitee Gateway that reaches the same management repository or bridge as your other gateways, with Gamma enabled (`gamma.enabled: true`). A gateway with Gamma disabled answers the AuthZEN endpoint with `503` and `pdp_unavailable`.

## Steps

### 1. Deploy the sidecar gateway

Deploy a Gravitee Gateway next to your application, and give it a sharding tag of its own, for example `checkout-pod`, with `tags` in `gravitee.yml` or the `gravitee_tags` environment variable.

### 2. Register a PDP gateway for the sidecar

In Authorization Management, go to **PDP Gateways**, and then click **Register PDP gateway**:

1. Enter a **Name**, for example `Checkout sidecar`.
2. In **Target PDP ID**, enter an identifier, for example `checkout`.
3. In **Sharding tag**, enter the sidecar's tag, `checkout-pod`.
4. Select **Create AuthZEN endpoint**. The **Endpoint path** fills in as `/<Target PDP ID>-<sharding tag>/`, for example `/checkout-checkout-pod/`. You can change it.
5. Click **Register**.

The PDP gateway is targeted as `<Target PDP ID>@<sharding tag>`, here `checkout@checkout-pod`.

### 3. Target policies and entities at the PDP gateway

Select the PDP gateway in the **Target gateways** of each policy the sidecar evaluates, or attach the policies from the PDP gateway's **Policies** tab. The policies tab also lists the entities these policies use, with **Attach all**. A policy or an entity with no target reaches only the default engine, so attach the entities the sidecar needs, such as the users and groups the policies name.

### 4. Point your application to the sidecar

Send AuthZEN requests from the application to the endpoint on the sidecar, for example:

```
POST http://localhost:8082/checkout-checkout-pod/access/v1/evaluation
```

For the request and the answer, see [AuthZEN endpoint](ask-for-a-decision/authzen-endpoint.md).

### 5. Verify

Send a request that a policy covers. The answer names the policy that decided, and the **Decisions** page lists the decision.

## Next steps

* [Policy syncs](policy-syncs.md). How policies and entities reach a gateway
* [Authorization policy synchronization](../authz-gateway-sync.md). Sync protocol details
