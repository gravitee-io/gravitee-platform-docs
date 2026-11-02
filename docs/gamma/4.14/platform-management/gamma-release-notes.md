---
description: What the Gamma 4.14 release adds to Agent Management and Edge Management. Browse the new features and changes.
---

# Release Notes

For release and end-of-life dates, see [Support Model](https://documentation.gravitee.io/apim/release-information/support-model).

## 4.14 new features

The 4.14 release adds the following capabilities.

### Agent Management

Agent Management adds the AWS Lambda and Data Cache policies to LLM Proxies.

#### AWS Lambda and Data Cache for LLM Proxies

* In the **Policy Studio** of an LLM Proxy, you can add the **AWS Lambda** and **Data Cache Policy** policies to the request and response phases.
* **AWS Lambda** invokes an AWS Lambda function. It isn't included in the default distribution, so [download](https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-aws-lambda/) version 3.5.0 or later of its plugin and [deploy it](https://documentation.gravitee.io/apim/plugins/deployment) first.
* **Data Cache Policy** reads, writes, and removes values in a cache resource of the LLM Proxy, so add a cache resource on the **Resources** page first. See [Resources](../agent-management/build/configure-an-llm-proxy.md#resources).

### Edge Management

Edge Management decides how the Edge Daemons identify themselves to the Edge Reactor: keyless, mTLS with the certificates of your fleet, or both. The routes of an intercepted agent take an OAuth2 plan of their target API, so that each developer signs in with your identity provider.

#### Daemon authentication

* The new **Daemon authentication** page, in the **Configuration** group, and the new **Authentication** step of the guided setup decide how the daemons of an environment identify themselves to the Edge Reactor.
* **Keyless** serves daemons that present no certificate, and every daemon while mTLS is off. It's on by default. **mTLS** serves daemons that present one of the active certificates enrolled on the page, issued by your own PKI. Gravitee never sees a private key. Both can be on at the same time, and at least one always stays on.
* Turning keyless off makes authentication mandatory. Keyless can be turned off once mTLS is on and an enrolled certificate is active.
* The Edge Reactor listener runs over TLS and asks the daemons for a client certificate once you configure it to. By default, it stays plain HTTP. When the listener requires a certificate, a certificate that it doesn't trust fails at the TLS handshake. It trusts the enrolled certificates, and mTLS only accepts a certificate in the environment that enrolled it. See [Secure the Edge Reactor listener](../edge-management/connect/secure-the-edge-reactor-listener.md).
* After the upgrade, the Edge Reactor refuses every call from the daemons of an environment configured before 4.14, until its Edge API is deployed again. Any change that you save in Edge Management for that environment deploys it, for example enrolling a certificate. The redeployed Edge API has keyless on, as by default.
* See [Configure daemon authentication](../edge-management/connect/configure-daemon-authentication.md).

#### OAuth2 plans on intercepted routes

* On the **Interception** page, each route of an intercepted agent takes a **Keyless** or **OAuth2** plan of its target API. For an OAuth2 plan, choose the application subscribed to it.
* The daemons receive the authorization server of the plan's OAuth2 resource and the client of the application, so that each developer signs in with your identity provider.
* **What this route needs** adds four requirements for the plan of a route. A route of the **Claude Code** preset that isn't secured by an OAuth2 plan reports **Check** rather than **Ready**, even when its target API meets every other requirement.
* A target API created from the picker sends the agent's own key to the AI provider through the API key authentication of its endpoint.
* See [Secure a route with an OAuth2 plan](../edge-management/connect/configure-edge-management.md#secure-a-route-with-an-oauth2-plan).

#### Changes to the Edge Reactor

* If the Edge Reactor listener can't start, the gateway doesn't start either, for example when the port of the listener is already in use, or when its keystore or truststore can't be read. Before 4.14, the gateway started without the listener.
* The setting for the port of the Edge Reactor listener has a new name. The previous name still works, and the gateway logs a warning at startup. See [Rename the port setting](../edge-management/connect/secure-the-edge-reactor-listener.md#rename-the-port-setting).
