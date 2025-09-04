---
hidden: true
noIndex: true
---

# Diagnostics

With Ambassador Edge Stack Diagnostics and Ambassador Cloud, you get a summary of the current status and Mappings of your cluster and it's services, which gets displayed in Diagnostics Overview.

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

Next, ensure that the `AES_REPORT_DIAGNOSTICS_TO_CLOUD` environment variable is set to `"true"` on the Agent deployment to allow diagnostics information to be reported to the cloud.

```shell
# Namespace and deployment name depend on your current install

kubectl set env deployment/edge-stack-agent -n ambassador AES_REPORT_DIAGNOSTICS_TO_CLOUD="true"
```

Finally, set the `AES_DIAGNOSTICS_URL` environment variable to `"http://emissary-ingress-admin:8877/ambassador/v0/diag/?json=true"`

```shell
# Namespace, deployment name, and pod url/port depend on your current install

kubectl set env deployment/edge-stack-agent -n ambassador AES_DIAGNOSTICS_URL="http://emissary-ingress-admin:8877/ambassador/v0/diag/?json=true"
```

After setting up `AES_DIAGNOSTICS_URL`, you can access diagnostics information by using the same URL value.

### Still can't see Ambassador Edge Stack Diagnostics?

Do a port forward on your Ambassador Edge Stack pod

```shell
# Namespace, deployment name, and pod url/port depend on your current install

kubectl port-forward edge-stack-76f785767-n2l2v -n ambassador 8877
```

You will be able to access the diagnostics overview page by going to `http://localhost:8877/ambassador/v0/diag/`

### Ambassador Edge Stack not routing your services as expected?

You will need to examine the logs and Ambassador Edge Stack pod status. See [troubleshooting.md](troubleshooting.md "mention") for more information.
