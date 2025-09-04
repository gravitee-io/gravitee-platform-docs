---
noIndex: true
---

# Ambassador Edge Stack and APIExt

## APIExt Conversion Webhook Service

Ambassador Edge Stack leverages Kubernetes Custom Resource Definitions to provide a friendly self-service api for configuring Ambassador Edge Stack. Over time, these Custom Resources have evolved and Ambassador Edge Stack supports multiple api versions. However, Kubernetes only supports a single `storage` version which means the different versions have to be converted into the `storage` version when applying or fetching resources from the kube-api-server. The APIExt server is a Kubernetes Conversion Webhook providing support for this conversion. To learn more about Custom Resource Definitions, `storage` versions and conversion webhooks see [Versions in CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/).

The kube-api-server requires a Conversion Webhook server to communicate using `https` so by default the APIExt conversion webhook service manages its own CA Certificate and ensures the CustomResourceDefinition is properly patched so that the kube-api-server can properly convert the CustomResources.

Here are the main components of the APIExt Conversion Webhook Service:

| Entity                   | Description                                                                      | Required | Leader Election |
| ------------------------ | -------------------------------------------------------------------------------- | -------- | --------------- |
| ConversionWebhookHandler | An HTTP handler that converts Custom Resource to requested version.              | Yes      | No              |
| CertificateAuthority     | Internal CA Cert cache that generates Server Certificates                        | Yes      | No              |
| CACertController         | Controller watching CA Cert Secret and providing CertificateAuthority the CACert | Yes      | No              |
| CRDPatchController       | Controller patching getambassador.io CRDs to ensure CABundle matches CACert      | No       | Yes             |
| CACertManager            | Runnable watching CA Cert Secret and ensuring it is always valid and non-expired | No       | Yes             |

### Modifying default namespace

{% hint style="info" %}
Currently, Ambassador Edge Stack doesn't provide alternative manifest and it is up to the user to ensure the namespace is updated correctly in all places.
{% endhint %}

By default, Ambassador Edge Stack installs the APIExt Server in the `emissary-system` namespace and the default manifests provided are configured to use this namespace. If you wish to modify this behavior then you must ensure the following objects are updated properly:

1. The `Service` and `Deployment` for the APIExt server
2. RBAC needs to be adjusted for the `ServiceAccount` which is bound to the `ClusterRole` and `Role` for the apiext server
3. Update EdgeStack `Deployment` so that the new waitForAPIExt init container is looking at the correct namespace

### Modifying default CRD labels

By default, Ambassador Edge Stack will only watch CRD's with the label `app.kubernetes.io/part-of=emissary-apiext` which is set on the default crd install manifest. This ensures that the CRD Manager only patches the `getambassador.io` CRD's that leverage the APIExt Server as a Conversion Webhook. If you need to modify these the APIExt Server has the `--crd-label-selector` flag that can be modified in the APIExt Server Deployment.

For example, if you want to modify or add additional selectors then you can modify the `--crd-label-selector` passed to the Deployment:

```yaml
# additional config removed for brevity
containers:
  - name: emissary-apiext
    image: docker.io/datawire/aes:3.10.1
    imagePullPolicy: IfNotPresent
    command: [ "apiext", "emissary-apiext" ]
    args: ["--crd-label-selector", "app.kubernetes.io/part-of=ext-gateway,app=gateway"]
```

Alternatively, if you do **NOT** want to set any label selectors you can remove it:

{% hint style="warning" %}
Removing the label selector will cause APIExt Server to watch and cache all CRD's within a cluster. If you have a lot of CRDs installed in your cluster this can increase the memory usage for your APIExt server pods.The CRD Manager will still only patch the `getambasador.io` resources but it is recommended to add labels to limit the memory usage.
{% endhint %}

```yaml
# additional config removed for brevity
containers:
  - name: emissary-apiext
    image: docker.io/datawire/aes:3.10.1
    imagePullPolicy: IfNotPresent
    command: [ "apiext", "emissary-apiext" ]
    args: []
```

### Disable CA Certification and CRD Patching

By default, the APIExt server manages its own CA Certificate and patches the CRD with the CABundle but some organizations may already have their own policies and tools that they want to use to manage the CA Certificate and/or CRD Patching. The APIExt server provides the ability to disable the `CRDPatchController` and the `CACertManager`. This can be done by adding the following Environment Variables to the APIExt Deployment.

{% hint style="warning" %}
The CA Certificate and the CRD's being properly patches are required for the APIExt server to properly run so if these components are disabled it is up to the user to ensure these are properly managed or else Ambassador Edge Stack will not properly operate.
{% endhint %}

* `DISABLE_CRD_MANAGEMENT` - If this env var exists then the CRD Patching will be disabled and it will be up to the user to ensure the CA Bundle is correctly patched.
* `DIABLE_CA_MANAGEMENT` - If this env var exists then the server will **not** generate or renew the root CA Certificate stored in `emissary-ingress-webhook-ca` in the `emissary-system` namespace. This will be up to the user to manage.

```yaml
# additional fields truncated for brevity...
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emissary-apiext
  namespace: emissary-system
spec:
  replicas: 3
  template:
    spec:
      serviceAccountName: emissary-apiext
      containers:
        - name: emissary-apiext
          image: docker.io/datawire/aes:3.10.1
          command: [ "apiext", "emissary-apiext" ]
          env:
            - name: DISABLE_CRD_MANAGEMENT
              value: "true" # any value can be provided, checks if env var exists or not
            - name: DISABLE_CA_MANAGEMENT
              value: "true" # any value can be provided, checks if env var exists or not
```

#### Using CertManager to manage CA Certificate

Many organizations already leverage CertManager for generating Certificates for applications or leverage it for ACME support with Ambassador Edge Stack. It is a good alternative that allows the CA Certificate and CRD patching to be handled externally from the APIExt service.

{% hint style="info" %}
This guide assumes you are already familiar with Cert Manager, and you can check out their [docs for more details](https://cert-manager.io/docs/).
{% endhint %}

Here are the steps for setting it up:

* Disable CACertController and CRDPatchController on [APIExt deployment](ambassador-edge-stack-and-apiext.md#disable-ca-certification-and-crd-patching)
* Setup `Issuer` and `Certificate`
* Annotate each CustomResourceDefinition

**Setup Issuer and Certificate**

{% hint style="warning" %}
The example below configures the Certificate with the same settings that the APIExt server uses internally and is also part of the current automated testing suite. Other configurations (i.e. other private key algorithms) are not guaranteed to work at this time and may not be supported.
{% endhint %}

The following YAML instructs CertManager to generate a self-signed root CA Certificate and inject it into the `emissary-system/emissary-ingress-webhook-ca` Secret. The APIExt server will watch that secret, load it and use it to generate Server certificates used for incoming connections.

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned
  namespace: emissary-system
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: emissary-ingress-webhook-ca
  namespace: emissary-system # ensure this is in the correct namespace
spec:
  secretName: emissary-ingress-webhook-ca
  subject:
    organizations:
      - "Ambassador Labs"
  dnsNames:
  - "*"
  isCA: true
  privateKey:
    algorithm: RSA
    encoding: PKCS8
    size: 4096
  issuerRef:
    name: selfsigned
```

**Annotate each CustomResourceDefinition**

Cert Manager can be taught to inject the CABundle from the CA Secret by adding an Annotation to each CustomResourceDefinition. All CustomResourceDefinitions (Mappping, Host, Filter, etc...) will need to have the following annotation `cert-manager.io/inject-ca-from: emissary-system/emissary-ingress-webhook-ca` added before applying or patched if already installed in a cluster.

{% hint style="info" %}
The CustomResourceDefinition manifest hosted at https://app.getambassador.io/yaml/edge-stack/latest/aes-crds.yaml does not add this annotation by default and it is up to the user to add this annotation.
{% endhint %}

Here is an example of the CustomResourceDefinition for `authservice.getambassador.io` annotated:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.13.0
    cert-manager.io/inject-ca-from: emissary-system/emissary-ingress-webhook-ca
  labels:
    app.kubernetes.io/instance: emissary-apiext
    app.kubernetes.io/managed-by: kubectl_apply_-f_emissary-apiext.yaml
    app.kubernetes.io/name: emissary-apiext
    app.kubernetes.io/part-of: emissary-apiext
  name: authservices.getambassador.io
spec:
  conversion:
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          name: emissary-apiext
          namespace: emissary-system
          path: /webhooks/crd-convert
          port: 443
      conversionReviewVersions:
      - v1
# additional fields truncated for brevity...
```
