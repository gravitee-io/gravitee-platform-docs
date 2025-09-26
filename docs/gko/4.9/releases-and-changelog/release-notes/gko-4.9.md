---
Gravitee Kubernetes Operator 4.9 Release Notes.
---

# GKO 4.9

## Highlights

Gravitee Kubernetes Operator (GKO) 4.9 introduces several key improvements focused on enhanced configuration, better support for notifications, and simplified troubleshooting.

## Product

### New Features

#### Helm Chart Configuration

The GKO 4.9 Helm Chart now offers more options for customizing the operator manager pod's deployment. You can now set node selectors to control where the pod is scheduled, and apply common annotations and labels to all Helm release components. Additionally, the release enables the configuration of an HTTP proxy for the operator manager's internal client and allows for the setting of a security context on the deployment.

#### Notification Enhancements

The Notification Custom Resource has been improved to support groups created directly within the Gravitee API Management (APIM) console, as opposed to only those created through a Group Custom Resource. This new feature allows the groups attribute within a Notification Custom Resource to reference these console-defined groups.

#### Simplified Troubleshooting

GKO 4.9 simplifies troubleshooting by reflecting reconciliation errors in the status of resources using conditions. This new feature provides a more transparent view of the resource's state without requiring users to dive into the operator manager's logs. When a resource encounters a problem, its status conditions will provide direct feedback, making it easier to identify and fix issues.

## Deprecation notice

`processingStatus` is being deprecated in favor of conditions for custom resource statuses.