---
hidden: false
noIndex: false
description: Configure Gamma Edge Management for an environment, from the gateway addresses to interception, daemon authentication, and the daemon deployment. Learn what each page covers.
---

# Configure

The **Configuration** group of the sidebar holds **Gateway**, **Interception**, **Shadow AI**, **Daemon authentication**, and **Daemon deployment**.

* [**Set up Edge Management**](set-up-edge-management.md). Create the configuration of an environment through the guided setup.
* [**Configure interception**](configure-edge-management.md). Choose which agents are intercepted, which target API receives each route, and the plan that secures it.
* [**Target API reference**](proxy-api-reference.md). What an API must be to receive intercepted traffic, and what Edge Management creates for you.
* [**Configure daemon authentication**](configure-daemon-authentication.md). Decide how the daemons identify themselves to the Edge Reactor, and enrol the certificates of your fleet.
* [**Secure the Edge Reactor listener**](secure-the-edge-reactor-listener.md). Run the listener over TLS and ask the daemons for a certificate.
* [**Configure Edge Ingress**](configure-edge-ingress.md). Expose the Edge Reactor port when the gateway runs on Kubernetes.
* [**Configure Kandji to deploy the Edge Daemon**](configure-kandji-daemon.md). Use Kandji to deploy the Edge Daemon across your device fleet.
* [**Connect Claude Code to the Edge Daemon**](../connect-claude-code-to-daemon.md). What to do on a device, and how to confirm that interception works.

Three of these pages have no sidebar item: Secure the Edge Reactor listener, Configure Edge Ingress, and Connect Claude Code to the Edge Daemon.
