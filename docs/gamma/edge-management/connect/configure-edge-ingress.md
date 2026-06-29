---
hidden: false
noIndex: true
---

# Configure Edge Ingress

If you are running the Gravitee AI Gateway on Kubernetes, you must expose the Edge Reactor port (`18093`) so that Edge Daemons running on employee devices can connect to the gateway.

Gamma provides native ingress support for the Edge Reactor via the Helm chart.

## Enable Edge Ingress in Helm

Update your `values.yaml` to enable and configure the `ingress_edge` block under the `gateway` component. This provisions a dedicated Kubernetes Ingress resource that routes external traffic directly to the `edge.server.port` (18093) on your gateway pods.

```yaml
gateway:
  ingress_edge:
    enabled: true
    hosts:
      - edge-reactor.example.com
    annotations:
      kubernetes.io/ingress.class: nginx
    tls:
      - secretName: edge-reactor-tls
        hosts:
          - edge-reactor.example.com
```

Apply the Helm upgrade to deploy the new Ingress resource:

```bash
helm upgrade gravitee-gamma graviteeio/gravitee-gamma -f values.yaml
```

Once deployed, configure your Edge Daemons to point to the new `edge-reactor.example.com` host for their control plane connection.
