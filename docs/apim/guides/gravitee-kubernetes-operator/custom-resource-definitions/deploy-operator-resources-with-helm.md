# Deploy Operator Resources with Helm

## Overview

Helm helps you manage Kubernetes applications — Helm Charts help you define, install, and upgrade even the most complex Kubernetes application.

You can also use Helm to deploy your CRDs into the cluster and leverage all the features that Helm provides such as templating.

These are the basic steps to deploy CRDs with Helm:sh

1. Create an empty project using Helm
2. Add required templates for the Gravitee CRDs
3. Install/Upgrade your helm charts

You can create an empty project using the following command

```sh
helm create sample-crds
```

And these should give us a project with the following structure

```
sample-crds
├── Chart.yaml
├── charts
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
```

The next step is to get rid of existing templates inside the templates folder and replace them with new templates for our CRDs. For example, this can be something that you can use for `ManagementContext` CRD:

```yaml
{{ - range $context := .Values.contexts }}
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: {{ $context.name }}
spec:
  baseUrl: {{ $context.baseUrl }}
  environmentId: {{ $context.environmentId }}
  organizationId: {{ $context.organizationId }}
  auth:
    secretRef:
      name: {{ $context.name }}
      namespace: {{ $context.namespace }}
{{- end }}
```

Which is based on the following values:

```yaml
contexts:
  - name: staging
    baseUrl: http://localhost:9000
    environmentId: DEFAULT
    organizationId: DEFAULT
    token: de6b0c76-abe1-440d-ab0c-76abe1740d99
```

If you want to reference an `ConfigMap` or a `Secret` inside your templates so that they will be resolved during the deployment by the GKO, you can use the following syntax for the values:

```
[[ secret `YOUR_SECRET_NAME/KEY_NAME` ]]
[[ configmap `YOUR_CONFIGMAP_NAME/KEY_NAME` ]]
```

Once you finished all your templates, you can packages your templates and install/upgrade your helm charts into the cluster with the following commands:

```sh
$ helm package .
$ helm install sample-crds sample-crds-0.1.0.tgz
```

For more information on Helm, head over to the [website](https://helm.sh/).

{% hint style="info" %}
For a complete example around the topic described in this section, you can checkout the [GKO repository guide](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/alpha/docs/guides/deploy-crd-with-helm).
{% endhint %}
