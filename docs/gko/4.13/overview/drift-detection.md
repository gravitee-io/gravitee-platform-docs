---
description: Drift detection checks an update to a Gravitee Kubernetes Operator 4.13 resource against the resource's current state in APIM, so a change made in APIM isn't replaced without notice. Learn how to turn it on and read its reports.
---

# Drift detection

## Overview

A resource that the Gravitee Kubernetes Operator (GKO) manages can still be changed in APIM by something other than GKO. For example, another automation tool or a script can change it through the Automation API. The resource in your cluster and its state in APIM then no longer match. The next time GKO applies the resource, it sends the whole resource to APIM, and the change made in APIM is replaced.

Drift detection catches this before it happens. It's a check in the GKO validating admission webhook. When you update a resource, GKO reads the resource's current state from APIM and compares it with your resource. When APIM was changed outside GKO, GKO reports the drift. A policy then decides whether the update is rejected, accepted with a warning, or accepted with an entry in the operator logs.

Drift detection is disabled by default. Turn it on for every supported resource with a Helm value, or for a single resource with an annotation.

## How GKO compares your resource with APIM

Drift detection runs only when you update a resource. Creating or deleting a resource is never checked.

On an update, GKO fetches the resource's current state from APIM. It compares that state with two versions of your resource: the version already stored in the cluster, and the version you're applying. It reports drift only when the state in APIM matches neither of them:

| State in APIM                                   | Result      |
| ----------------------------------------------- | ----------- |
| Matches the version already stored in the cluster | Allowed   |
| Matches the version you're applying             | Allowed     |
| Matches neither version                         | Drift       |

So when someone changes a description in APIM, you can update your resource to the same description and apply it. Reapplying the unchanged resource, or applying a different description, reports drift.

A field that neither version of your resource sets isn't reported, even when APIM sets a value for it, unless the field belongs to an item of a list.

GKO compares your resource in the form it sends to APIM, not the YAML you wrote. Values that your resource takes from templates are compared after GKO resolves them in the version you're applying. Identifiers that APIM generates aren't compared. Most other fields must match exactly. For some fields, GKO ignores differences that don't change the meaning. For example, it accepts a date written in another time zone, or an empty list compared with a list that isn't set. Lists such as endpoint groups are compared item by item and in order, so reordering their items in APIM counts as drift.

Drift detection has the following requirements:

* The resource is synchronized with APIM through a `ManagementContext`. A subscription, a documentation page, a portal link, or a portal listing uses the `ManagementContext` of the resource it belongs to. An `ApiV4Definition` without a `contextRef` isn't checked.
* The admission webhooks are enabled. GKO doesn't start when `manager.driftDetection.enabled` is `true` and the webhooks are disabled. With the webhooks disabled, the annotation has no effect, because no admission check runs.

Each checked update adds a call to APIM during admission. The call uses the same HTTP client timeout as the dry-run call, and runs within the same webhook timeout. See [Admission timeouts](admission-validation.md#admission-timeouts).

## Supported resources

Drift detection applies to the following resources:

| Resource            | Drift detection                                                   |
| ------------------- | ----------------------------------------------------------------- |
| `ApiV4Definition`   | Supported                                                         |
| `Application`       | Supported                                                         |
| `Subscription`      | Supported, except for a subscription to an `ApiDefinition` (v2 API) |
| `SharedPolicyGroup` | Supported                                                         |
| `Group`             | Supported                                                         |
| `Dictionary`        | Supported                                                         |
| `Portal`            | Supported                                                         |
| `PortalLink`        | Supported                                                         |
| `PortalListing`     | Supported                                                         |
| `PortalTheme`       | Supported                                                         |
| `Documentation`     | Supported                                                         |

Drift detection doesn't apply to other resources, such as an `ApiDefinition` (v2 API), a `ManagementContext`, or an `ApiResource`. These resources, and subscriptions to a v2 API, ignore the annotation.

## Turn on drift detection

Turn drift detection on for every supported resource with a Helm value, or for a single resource with an annotation.

### Turn it on for every resource

Set `manager.driftDetection.enabled` to `true` in your Helm values:

{% code title="values.yaml" %}
```yaml
manager:
  driftDetection:
    enabled: true
```
{% endcode %}

The chart passes the value to the operator as the `DRIFT_DETECTION_ENABLED` environment variable. Drift detection is on only when that variable is set to `true`.

### Turn it on or off for a single resource

Set the `gravitee.io/drift-detection` annotation on the resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Dictionary
metadata:
  name: shared-properties
  annotations:
    gravitee.io/drift-detection: "true"
spec:
  # ...
```

The annotation takes precedence over the Helm value:

| `gravitee.io/drift-detection` | `manager.driftDetection.enabled` | Drift detection |
| ----------------------------- | -------------------------------- | --------------- |
| `"true"`                      | `true` or `false`                | On              |
| `"false"`                     | `true` or `false`                | Off             |
| Not set, or another value     | `true`                           | On              |
| Not set, or another value     | `false`                          | Off             |

The value must be exactly `true` or `false`, in lowercase. GKO reads the annotation from the version you're applying, so a new value takes effect in the same update.

Drift detection also runs on an update that changes only the metadata of a resource, such as its annotations. Adding `gravitee.io/drift-detection: "true"` to a resource that has already drifted is therefore checked, and rejected with the default policy.

## Choose what happens when drift is found

Three policies decide what happens to the update. Each one applies to a different outcome of the check:

| Helm value                                      | Environment variable                 | Applies when                                                                 | Default |
| ----------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------- | ------- |
| `manager.driftDetection.policy`                 | `DRIFT_DETECTION_POLICY`             | GKO finds drift.                                                             | `deny`  |
| `manager.driftDetection.onRemoteMissing.policy` | `DRIFT_DETECTION_ON_REMOTE_MISSING`  | The resource doesn't exist in APIM, and APIM answers with HTTP 404.          | `deny`  |
| `manager.driftDetection.onFetchFailure.policy`  | `DRIFT_DETECTION_ON_FETCH_FAILURE`   | GKO can't fetch the resource from APIM for any other reason, such as a network error or another HTTP error. | `deny`  |

Each policy accepts one of the following values:

| Policy  | Result                                                                                         |
| ------- | ---------------------------------------------------------------------------------------------- |
| `deny`  | The update is rejected. The error returned to `kubectl` contains the report.                   |
| `warn`  | The update is accepted. The report is returned to `kubectl` as a warning.                      |
| `allow` | The update is accepted. GKO writes a warning to the operator logs instead.                     |

A value that isn't `deny`, `warn`, or `allow` falls back to `deny`. The policies apply to every resource. The annotation only turns drift detection on or off.

When the resource doesn't exist in APIM, GKO has nothing to compare, and the report is a single line:

```
remote [Application] [team-a/internal-app] not found during drift detection
```

When GKO can't fetch the resource, the report starts with `failed to fetch remote`, followed by the kind and the namespace and name of the resource, and the error returned by the call to APIM.

Whatever the policies, GKO rejects the update when it can't resolve the references of the resource, or its `ManagementContext`, because it can't build the version to compare in that case.

## Read a drift report

A drift report starts with `drift detected:`, and lists only the fields that differ, one per line:

```
drift detected:
description: "local CRD description" != "remote updated description"
```

The value on the left of `!=` comes from the version you're applying, and the value on the right is the current value in APIM. The field names are those of the resource in the form GKO sends it to APIM, so a few of them differ from the field names of the custom resource.

The report uses the following conventions:

* **Nested fields** are indented by two spaces under the field that contains them. Only the fields on the way to a difference are printed:

  ```
  drift detected:
  failover:
    maxRetries: 5 != 2
  ```
* **List items** are identified by their index in square brackets, for example `apis[0]:` for an item that is an object, or `tags[1]:` for a single value. When an item exists on one side only, the other side shows an empty value, such as `""` or `0`. A field that isn't set on one side shows `<nil>`.
* **Map entries** are sorted by key, so the report is the same from one run to the next.
* **Long values** are cut after 60 characters, followed by the number of hidden characters, for example `(120 chars hidden)`.
* **Text on several lines** is compared line by line and shown side by side. Runs of identical lines are replaced by a line count, and `!=` marks the first line that differs.

For example, when the second and third lines of the content of a `Documentation` resource differ, the report looks like this:

```
content:  ... 1 identical line
          left-two    !=  right-two
          left-three      right-three
```

When `manager.driftDetection.policy` is `allow`, the operator logs contain the following line instead of the report, without the list of differences:

```
drift detected for resource [Application] [team-a/internal-app], drift policy is 'allow': drift is ignored
```

## Resolve a reported drift

To resolve a reported drift, use one of the following options:

* **Keep the change made in APIM.** Update your resource so that the fields in the report match the values on the right of `!=`, and then apply it. APIM then matches the version you're applying, so the update is accepted.
* **Undo the change made in APIM.** Set the fields in APIM back to the values of the version already stored in the cluster, and then apply your resource again. APIM then matches the stored version, so the update is accepted.
* **Replace the change made in APIM.** Add the `gravitee.io/drift-detection: "false"` annotation to your resource in the same update. Drift detection doesn't run for that update, so GKO applies your resource and the change made in APIM is replaced. Afterward, restore the previous value of the annotation, so that GKO checks the resource for drift again.

## Roll out drift detection

To introduce drift detection without blocking updates, complete the following steps:

1. Set `manager.driftDetection.policy` to `warn`, and set `manager.driftDetection.enabled` to `true`. Updates with drift are accepted, and each drift report comes back as a warning.
2. Resolve the drifts that the warnings report.
3. Set `manager.driftDetection.policy` back to `deny`.

To check only some resources, leave `manager.driftDetection.enabled` set to `false`, and add the `gravitee.io/drift-detection: "true"` annotation to those resources.
