---
'0': G
'1': r
'2': a
'3': v
'4': i
'5': t
'6': e
'7': e
'8': ' '
'9': K
'10': u
'11': b
'12': e
'13': r
'14': 'n'
'15': e
'16': t
'17': e
'18': s
'19': ' '
'20': O
'21': p
'22': e
'23': r
'24': a
'25': t
'26': o
'27': r
'28': ' '
'29': '4'
'30': .
'31': '9'
'32': ' '
'33': R
'34': e
'35': l
'36': e
'37': a
'38': s
'39': e
'40': ' '
'41': 'N'
'42': o
'43': t
'44': e
'45': s
'46': .
description: Overview of GKO.
---

# GKO 4.9

## Highlights

Gravitee Kubernetes Operator (GKO) 4.9 introduces several key improvements focused on enhanced configuration, better support for notifications, and simplified troubleshooting.

## Product

### New Features

#### Helm Chart configuration

The GKO 4.9 Helm Chart offers new customization options for the operator manager pod's deployment. You can now set node selectors to control where the pod is scheduled, apply common annotations and labels to all Helm release components, configure an HTTP proxy for the operator manager's internal client, and set a security context on the deployment.

#### Notification enhancements

The Notification Custom Resource now supports groups created directly within the Gravitee API Management (APIM) Console, as opposed to only those created through a Group Custom Resource. This new feature allows the `groups` attribute within a Notification Custom Resource to reference these Console-defined groups.

#### Simplified troubleshooting

GKO 4.9 simplifies troubleshooting by using resource status conditions to reflect reconciliation errors. This new feature provides a more transparent view of the resource's state without requiring users to dive into the operator manager's logs. When a resource encounters a problem, its status conditions provide direct feedback, making it easier to identify and fix issues.

## Deprecation notice

`processingStatus` is being deprecated in favor of conditions for custom resource statuses.
