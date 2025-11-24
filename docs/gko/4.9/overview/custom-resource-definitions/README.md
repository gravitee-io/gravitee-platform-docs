---
description: Overview of Custom Resource Definitions.
---

# Custom Resource Definitions

## Custom Resource Definitions

The Gravitee Kubernetes Operator (GKO) comes with several custom resource definitions (CRDs):

* [`ManagementContext`](managementcontext.md)
* [`ApiV4Definition`](apiv4definition.md) and [`ApiDefinition`](apidefinition.md)
* [`Application`](application.md)
* [`ApiResource`](apiresource.md)
* [`Subscription`](subscription.md)
* [`Group`](group.md)
* [`SharedPolicyGroup`](sharedpolicygroup.md)
* [`Notification`](notification.md)
* [`GatewayClassParameters`](gatewayclassparameters.md)
* [`KafkaRoute`](kafkaroute.md)

{% hint style="info" %}
Sample CRDs are available in the GKO GitHub [repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/4.8.x/examples).
{% endhint %}

The `ApiV4Definition` and `ApiDefinition` custom resources are used to define individual APIs that run on the Gateway. APIs are the most important resource that GKO manages. `ApiV4Definition` is used to define v4 Gravitee APIs. It supports both traditional proxy APIs and event APIs and was introduced in GKO 4.4. `ApiDefinition` is used to define v2 Gravitee APIs.

`Resources` are objects that allow you to define pointers to external resources, such as authentication providers and caches, that can then be referenced from an API definition's policies. For example, an OAuth2 provider can be referenced from an API's OAuth2 authentication policy by pointing to the right `Resource`. Resources are referenced from `ApiV4Definitions` and `ApiDefinitions`.

The `Application` custom resource represents the configuration for an application. Applications are used to identify the consumer of an API, and to carry subscriptions and credentials.

Finally, the purpose of the `ManagementContext` is to provide a connection from GKO to your Gravitee API Management installation. GKO uses this connection to synchronize the resources it manages (APIs, applications, ...) with the Gravitee Console, Developer Portal, and Gateway.

## Custom Resource Definition (CRD) Status

When you deploy Custom Resources (CRDs) with the Gravitee Kubernetes Operator (GKO), the `status` field is populated with the latest information about the resource's state within the cluster. The 4.9 version of GKO introduces enhancements to the CRD status fields, providing clearer insights, streamlined troubleshooting, and improved support for GitOps workflows.

These enhancements include more structured, descriptive status information that aligns with best practices and offers consistent conventions across CRDs. This enables tighter integration with tools like ArgoCD and simplifies operational management for platform teams.

Prerequisites

* Gravitee Kubernetes Operator version 4.9.0 or above
* A Kubernetes cluster with the GKO installed. For more information about installing GKO, see \[https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/getting-started/quickstart-guide]\(Quick Start Guide)
* Access to view CRDs with `kubectl get` commands

### Viewing CRD Status

1. Get a list of deployed V4 APIs using the following command:

```bash
kubectl get apiv4definitions.gravitee.io
```

2. Inspect the `status` section of an API V4 CRD using the following command:

```bash
kubectl get apiv4definitions.gravitee.io  <api-name> -o yaml
```

There is an organized `status` section with the following fields:

```yaml
status:
  conditions:
    - lastTransitionTime: "2025-10-03T09:20:04Z"
      message: Successfully reconciled
      observedGeneration: 1
      reason: Accepted
      status: "True"
      type: Accepted
    - lastTransitionTime: "2025-10-03T09:20:04Z"
      message: All References successfully resolved
      observedGeneration: 1
      reason: ResolvedRefs
      status: "True"
      type: ResolvedRefs
  crossId: 8905ba8d-79b9-c446-5cee-71ab8c6ea6f9
  environmentId: DEFAULT
  errors: {}
  id: 3872738b-0aa6-ed7e-1f7b-386d80125412
  organizationId: DEFAULT
  plans:
    KeyLess: d50628d2-cb86-01bc-0393-cdc0a0ce32e4
  processingStatus: Completed
  state: STARTED
```

The `conditions` array captures key lifecycle states and potential issues, while top-level fields like `state` and `environmentId` provide an operational summary.

Also, the Application's status is organized with the following fields:

```bash
kubectl get applications.gravitee.io <app-name> -o yaml
```

```yaml
status:
  conditions:
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: Successfully reconciled
      observedGeneration: 1
      reason: Accepted
      status: "True"
      type: Accepted
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: All References successfully resolved
      observedGeneration: 1
      reason: ResolvedRefs
      status: "True"
      type: ResolvedRefs
  environmentId: DEFAULT
  errors: {}
  id: 011b0a6b-59d8-452b-95a4-30db51783b83
  organizationId: DEFAULT
  processingStatus: Completed
```

### Possible CRD conditions

When a Custom Resource Definition (CRD) is successfully applied without issues, your CRD's status section displays conditions like the following example:

```yaml
status:
  conditions:
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: Successfully reconciled
      observedGeneration: 1
      reason: Accepted
      status: "True"
      type: Accepted
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: All References successfully resolved
      observedGeneration: 1
      reason: ResolvedRefs
      status: "True"
      type: ResolvedRefs
```

If GKO encounters issues resolving resources referenced within your CRD such as ManagementContext, Secrets, Groups, andAPIs, the conditions reflect a failure like the following example:

```yaml
status:
  conditions:
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: ReconcileFailed
      observedGeneration: 1
      reason: Accepted
      status: "False"
      type: Accepted
    - lastTransitionTime: "2025-10-03T09:25:22Z"
      message: "can not find Management Context [dev-ctx]"
      observedGeneration: 1
      reason: ResolvedRefs
      status: "False"
      type: ResolvedRefs
```

Common Causes of Unaccepted CRDs

* ResolveRefError (Unresolved References): GKO is unable to resolve references within your CRD, such as Management Contexts, Shared Policy Groups, or APIs.
* IllegalStateError: It indicates that there is inconsistency in the CRD. For example in the case of a V2 API CRD, you set local=true, but you didn't specify a Management Context.
* CompileTemplateError: This error might happen when our template engine can't compile the CRD (due to invalid characters or other reasons)
* ControlPlaneError: Errors occurring during runtime, such as invalid values or misconfigurations passed when importing your API into APIM.

### Leveraging Status with GitOps

The improved structured status output allows for tighter integration with GitOps tools that watch Kubernetes events.

For example, when using ArgoCD:

1. Define an ArgoCD Application that monitors the GKO namespace.
2. ArgoCD detects any drifts between the desired state (Git repo) and the current status fields.
3. Based on the CRD status messages, ArgoCD takes the appropriate actions:
   * Apply resources if creation failed (`*Accepted` condition false)
   * Set the resource as "Degraded" if operations failed (`*ResolvedRefs` false)
   * Trigger notifications based on configured events

The standardized schema lets you create cleaner, more automated GitOps workflows around the full API lifecycle on Kubernetes.

The following sections explain each CRD
