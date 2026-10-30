---
description: Overview of Diagnostics.
hidden: true
noIndex: true
---

# Diagnostics

With Ambassador Edge Stack Diagnostics, you get a summary of the current status and Mappings of your cluster and it's services, which gets displayed in Diagnostics Overview.

## Troubleshooting

### Can't access Ambassador Edge Stack Diagnostics Overview?

Create an Ambassador `Module` if one does not already exist, and add the following config to enable diagnostics data.

```yaml
apiVersion: getambassador.io/v3alpha1
kind: Module
metadata:
  name: ambassador
spec:
  config:
    diagnostics:
      enabled: true
```

### Still can't see Ambassador Edge Stack Diagnostics?

Do a port forward on your Ambassador Edge Stack pod

```shell
# Namespace, deployment name, and pod url/port depend on your current install

kubectl port-forward edge-stack-76f785767-n2l2v -n ambassador 8877
```

You will be able to access the diagnostics overview page by going to `http://localhost:8877/ambassador/v0/diag/`

### Ambassador Edge Stack not routing your services as expected?

You will need to examine the logs and Ambassador Edge Stack pod status. See [troubleshooting.md](troubleshooting.md "mention") for more information.
