# Install from OperatorHub

## Overview

Starting with version 4.10.9, the Gravitee Kubernetes Operator (GKO) is available on [OperatorHub.io](https://operatorhub.io/operator/gravitee-kubernetes-operator) under the package name `gravitee-kubernetes-operator`. This gives Kubernetes and OpenShift users an additional installation path alongside the existing Helm chart.

## Channels

GKO uses a per-minor-version channel strategy. Every release is published to two OLM channels:

| Channel                   | Description                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alpha`                   | Receives all releases across all minor versions. Subscribe to this channel to receive cross-minor upgrades automatically.                                         |
| `stable-v{MAJOR}.{MINOR}` | Receives only patch releases for a specific minor version (for example, `stable-v4.10`). Subscribe to this channel to pin a specific minor version in production. |

The default channel is the `stable-v{MAJOR}.{MINOR}` channel matching the latest available minor release.

## Versioning and upgrade strategy

Bundle versions match GKO release versions exactly (for example, `4.10.9`, `4.10.10`, `4.11.0`).

The update graph uses `semver-mode`. OLM determines valid upgrade paths automatically based on semantic versioning. There are no manual `replaces` or `skips` fields to maintain.

Upgrade approval depends on the subscription configuration:

* **Automatic** — OLM installs new versions as soon as they appear in the subscribed channel.
* **Manual** — OLM creates an `InstallPlan` that requires explicit approval before the upgrade proceeds.

## Installation

GKO is available on both OpenShift and vanilla Kubernetes clusters that run the Operator Lifecycle Manager (OLM).

### OpenShift

GKO appears in the OperatorHub section of the OpenShift web console.

1. Navigate to **Operators > OperatorHub** in the console.
2. Search for **Gravitee Kubernetes Operator**.
3. Select the operator and click **Install**.
4. Choose the desired channel (`stable-v4.10`, `alpha`, etc.), namespace, and approval strategy (**Automatic** or **Manual**).
5. Click **Install** to create the subscription.

OpenShift handles the rest: pulling the bundle, installing the CRDs, creating the operator deployment, and configuring webhook certificates.

### Kubernetes (with OLM)

On vanilla Kubernetes, OLM is required as a prerequisite. For OLM installation instructions, refer to the [Operator Lifecycle Manager documentation](https://olm.operatorframework.io/docs/getting-started/).

Once OLM is running, install GKO by creating the following resources:

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: gravitee-kubernetes-operator
  namespace: operators
spec:
  channel: stable-v4.10
  name: gravitee-kubernetes-operator
  source: operatorhubio-catalog
  sourceNamespace: olm
```

Replace `stable-v4.10` with the channel matching the minor version you want to track.

## Install modes

GKO supports all four OLM install modes:

| Install mode      | Description                                                                    |
| ----------------- | ------------------------------------------------------------------------------ |
| `OwnNamespace`    | The operator runs and watches resources in the namespace where it's installed. |
| `SingleNamespace` | The operator watches resources in a single specified namespace.                |
| `MultiNamespace`  | The operator watches resources in a defined set of namespaces.                 |
| `AllNamespaces`   | The operator watches resources across all namespaces in the cluster.           |

## Differences from Helm installation

Users familiar with the Helm chart need to be aware of the following behavioral differences when GKO is installed via OLM.

### Webhook certificates

When installed via Helm, GKO generates self-signed TLS certificates for its admission webhooks and stores them in a Kubernetes Secret. When installed via OLM, webhook certificate management is handled by OLM itself. The operator detects this automatically and defers to OLM for certificate injection.

### Namespace scoping

With Helm, the operator reads its target namespace from a ConfigMap (`gko-config`). With OLM, the target namespace is injected via the `olm.targetNamespaces` pod annotation, and the ConfigMap isn't used.

### Security context

The OLM bundle ships with hardened security defaults:

* `runAsNonRoot: true` at the pod level
* `allowPrivilegeEscalation: false` at the container level
* `readOnlyRootFilesystem: true` at the container level
* All Linux capabilities dropped (`capabilities.drop: ["ALL"]`)

These are the same defaults now present in the Helm chart's `values.yaml`, so both installation methods converge on the same security posture.

## Maturity

The operator is currently published with `alpha` maturity in the ClusterServiceVersion metadata. This reflects the initial OperatorHub listing. The maturity level may be promoted in future releases as the OLM distribution matures.

## Quick reference

| Item                     | Value                                    |
| ------------------------ | ---------------------------------------- |
| OperatorHub package name | `gravitee-kubernetes-operator`           |
| Default channel          | `stable-v{MAJOR}.{MINOR}` (latest minor) |
| Update strategy          | `semver-mode`                            |
| Minimum GKO version      | `4.10.9`                                 |
