---
description: Guide to deploying Operator Resources with Helm.
---

# Deploy Operator Resources with Helm

## Overview

Helm assists in the management of Kubernetes applications. In particular, Helm Charts facilitate the definition, installation, and upgrade of even the most complex Kubernetes applications.

You can also use Helm to deploy your CRDs into your cluster and leverage all of the features that Helm provides (e.g., templating).

Below are the basic steps to deploy CRDs with Helm:

1. Create an empty project using Helm
2. Add required templates for the Gravitee CRDs
3. Install/upgrade your Helm Charts

You can create an empty project using the following command:

```sh
helm create sample-crds
```

The project will have the following structure:

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

The next step is to delete existing templates from the templates folder and replace them with new templates for your CRDs. For example, the template below can be used for the `ManagementContext` CRD:

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

The GKO can resolve a `ConfigMap` or `Secret` during deployment if it is referenced in a template. Use the following syntax:

```
[[ secret `YOUR_SECRET_NAME/KEY_NAME` ]]
[[ configmap `YOUR_CONFIGMAP_NAME/KEY_NAME` ]]
```

Once your templates have been created, you can package them and install/upgrade your Helm Charts by running the following commands:

```sh
$ helm package .
$ helm install sample-crds sample-crds-0.1.0.tgz
```

For more information on Helm, see the [documentation](https://helm.sh/).

{% hint style="info" %}
For a comprehensive example of the topics introduced in this section, check out the [GKO repository guide](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/alpha/docs/guides/deploy-crd-with-helm).
{% endhint %}
