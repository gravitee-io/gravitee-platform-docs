---
hidden: false
noIndex: false
description: The PDP Gateways group of the Authorization Management sidebar holds the gateways that evaluate your policies and how policies reach them.
---

# PDP Gateways

The **PDP Gateways** group of the Authorization Management sidebar holds the **PDP Gateways** page.

* [**Configure the Gravitee Gateway as a runtime**](configure-gravitee-gateway-as-runtime.md). Register a Gravitee Gateway as a Policy Decision Point so authorization decisions are evaluated at the wire level.
* [**Configure a sidecar as runtime**](configure-sidecar-as-runtime.md). Run a Gravitee Gateway beside your application as a sidecar, so the application asks for authorization decisions over localhost.
* [**Policy syncs**](policy-syncs.md). How authorization policies travel from the control plane to your runtime gateways, and how long it takes.
* [**Ask for a decision**](ask-for-a-decision/README.md). Compare the Authorization PEP policy, the AuthZEN endpoint of a PDP gateway, and the AuthZEN PDP policy, and see how each one builds the request your policies evaluate.
* [**Analytics sent to the control plane**](analytics-sent-to-control-plane.md). What your gateways record for each authorization decision, and where you read those records.
* [**Authorization policy synchronization**](../authz-gateway-sync.md). Gamma Authorization Management evaluates policies locally inside the API Gateway.
