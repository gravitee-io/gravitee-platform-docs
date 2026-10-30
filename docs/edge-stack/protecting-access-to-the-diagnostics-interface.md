---
description: Overview of Diagnostics Interface.
hidden: true
noIndex: true
---

# Protecting Access to the Diagnostics Interface

Out of the box, Ambassador Edge Stack enables `Mapping`s to provide access to the diagnostics interfaces that can help you debug your installation. In a production environment, though, public access to these endpoints is not an ideal situation. To solve this, we will be using the Ambassador `Module` to remove the default mappings, after which we'll create a new, host-based `mapping` to expose the diagnostics interface more securely. The Ambassador `Module` applies system-wide configuration settings for Ambassador Edge Stack to follow.

```yaml
apiVersion: getambassador.io/v3alpha1
kind: Module
metadata:
  name: ambassador
spec:
  config:
    diagnostics:
      enabled: false
```

After applying this module, the diagnostics interface are no longer accessible from the outside world. Administrators can still reach it with Kubernetes port forwarding, which is limited to users who have permission to port-forward to the Ambassador Edge Stack pods:

```
kubectl port-forward -n ambassador deploy/edge-stack 8877
```

Then visit `http://localhost:8877/ambassador/v0/diag/`. Use the namespace and deployment name of your installation.

{% hint style="info" %}
Starting with 3.15.0, Ambassador Edge Stack rejects a `Mapping` that routes to its own admin port (8877) unless the `Mapping` can only reach the readiness, liveness, or `/metrics` endpoints, so you can't expose the diagnostics interface with a `Mapping`.
{% endhint %} To learn more about Ambassador `Module` configurations, see [the-module-resource.md](technical-reference/using-custom-resources/the-module-resource.md "mention").
