---
description: What the Gamma 4.14 release adds to Edge Management. Browse the new features and changes.
---

# Release Notes

Each Gamma version follows the support period of the API Management version it ships with. For release and end-of-life dates, see [Support Model](https://documentation.gravitee.io/apim/release-information/support-model).

## 4.14 new features

The 4.14 release adds the following capabilities.

### Edge Management

Edge Management secures the calls of the Edge Daemons with Gravitee plans. The daemons identify themselves to the Edge Reactor through a keyless plan, an mTLS plan that matches the certificates of your fleet, or both. The routes of an intercepted agent take an OAuth2 plan of their target API, so that each developer signs in with your identity provider.

#### Daemon authentication

* The new **Daemon authentication** page, in the **Configuration** group, and the new **Authentication** step of the guided setup decide how the daemons of an environment identify themselves to the Edge Reactor.
* The **Keyless** plan serves daemons that present no certificate, and it's published by default. The **mTLS** plan serves daemons that present one of the certificates enrolled on the page, issued by your own PKI. Gravitee never sees a private key.
* Closing the keyless plan makes authentication mandatory. It closes once the mTLS plan is published, a certificate is active, and the fleet subscription is accepted.
* The Edge Reactor listener runs over TLS and asks the daemons for a client certificate once you configure it to. By default, it stays plain HTTP. See [Secure the Edge Reactor listener](../edge-management/connect/secure-the-edge-reactor-listener.md).
* An environment configured before 4.14 has no fleet application yet. The next **Save & Deploy** from any configuration page of Edge Management creates it, along with the **Keyless** and **mTLS** plans if either is missing. Until you close it, the keyless plan keeps serving the daemons.
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
