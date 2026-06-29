---
hidden: false
noIndex: false
---
# Activate Gamma with Kubernetes (Helm)
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Gravitee Gamma is Gravitee's next-generation unified control plane. It brings API Management, Event Management, Agent Management, Authorization Management, and Platform Management together in a single console, so you manage your APIs, Kafka streams, AI agents and MCP servers, and authorization policies from one place.

{% hint style="warning" %}
Gamma ships in 4.12 (`4.12.0`). Activating Gamma moves your deployment to that build. Use this for development and quick-start purposes only. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

If you already run Gravitee API Management with the Helm chart, you turn Gamma on by moving to the Gamma build, enabling Gamma, and adding the Gamma console to your `values.yaml`. This page covers only those changes. For a full install, follow the Helm guide for your cluster: [Vanilla Kubernetes](../self-hosted-installation-guides/kubernetes/vanilla-kubernetes.md), [AWS EKS](../self-hosted-installation-guides/kubernetes/aws-eks.md), [Azure AKS](../self-hosted-installation-guides/kubernetes/azure-aks.md), or [OpenShift](../self-hosted-installation-guides/kubernetes/openshift.md).

## Activate Gamma

Add the following to your existing `values.yaml`, then run `helm upgrade`.

1. Use the Gamma build. Set the image tags for `api`, `gateway`, `ui`, and `portal` to `4.12.0`.
2. Turn on Gamma:

   ```yaml
   gamma:
     enabled: true
   ```
3. Allow the Gamma console to sign in. Adjust the CORS origin to the URL where you serve the Gamma console:

   ```yaml
   api:
     env:
       - name: gravitee_http_cors_enabled
         value: "true"
       - name: gravitee_http_cors_allow-origin
         value: "<your console origin>"
       - name: gravitee_http_cors_allow-credentials
         value: "true"
       - name: gravitee_http_cookie_sameSite
         value: "Lax"
       - name: gravitee_http_cookie_secure
         value: "false"
   ```
4. Add the Gamma console:

   ```yaml
   gammaUi:
     enabled: true
     image:
       repository: graviteeio/gamma-ui
       tag: 4.12.0
     app:
       gammaBaseURL: "<your host>/gamma"
     env:
       - name: GAMMA_CONSOLE_BASE_HREF
         value: /
   ```
5. Apply the change. Replace `<release-name>` and `<namespace>`:

   ```bash
   helm upgrade <release-name> graviteeio/apim \
     --version 4.12.0 --devel \
     --namespace <namespace> \
     -f values.yaml
   ```

{% hint style="warning" %}
**Gamma uses two Helm flags**

* `gamma.enabled` is the global master switch (default `false`). It turns Gamma on in the Management API and unlocks the Gamma ingress and the Gamma console deployment.
* `gammaUi.enabled` is the per-component switch for the Gamma console (default `false`). It deploys the `graviteeio/gamma-ui` console.

When `gamma.enabled` is `true`, you choose which components to deploy:

* `gamma.enabled: true` with `gammaUi.enabled: true` enables Gamma on the API and deploys the Gamma console.
* `gamma.enabled: true` with `gammaUi.enabled: false` enables Gamma on the API without the console.

If `gamma.enabled` is `false`, Gamma stays off everywhere, and the Gamma console doesn't deploy even when `gammaUi.enabled` is `true`.
{% endhint %}

For the complete `values.yaml`, the ingress and single-host layout, and the enterprise license step for Agent Management, follow the Helm guide for your cluster (links above).

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../agent-management/get-started/create-your-first-mcp-server.md).
