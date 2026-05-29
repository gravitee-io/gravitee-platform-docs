---
description: An overview about gravitee resources.
metaLinks:
  alternates:
    - example-resource-configurations.md
---

# Gravitee Resources

## Overview

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

Terraform defines resources as basic infrastructure elements. It creates and manages these resources as part of its Infrastructure as Code (IaC) workflow. This lets you use configuration files to automate reproducible and version controlled APIs.

Resources are classified by type, where a resource type is associated with a particular provider. Gravitee's Terraform provider supports several resource types, including v4 APIs, Shared Policy Groups, Applications, and Subscriptions.

To create a resource, you need to add a resource definition to your Terraform configuration file. The definition includes settings such as the resource type, a Human-readable Identifier (hrid) to uniquely identify the resource by name, and arguments to specify other resource parameters.

Terraform uses your configuration files to track the state of your infrastructure. When you update your configuration, Terraform detects the differences between your existing and desired states. It then creates and executes a plan to apply your changes. This is a fully automated alternative to manually updating your APIs in the APIM Console or with mAPI scripts.

## Gravitee resources

The Gravitee Terraform provider supports the following Gravitee resource types:

* HTTP proxy API
* Message API (protocol mediation)
* Kafka Native API
* AI proxy APIs (MCP, A2A, LLM)
* Shared Policy Group
* Application
* Subscription
* Group
* Dictionary

Terraform can create, update, or delete these resources as part of its workflow.

{% hint style="info" %}
Guides and examples can be found in the [Gravitee "apim" Terraform Registry documentation](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs).
{% endhint %}


## Automation API gaps

Missing properties or values in regards of the Management API:

| Resource          | Section                   | Missing Property                   | Type                                  | Supported in Automation API                                           |
|-------------------|---------------------------|------------------------------------|---------------------------------------|-----------------------------------------------------------------------|
| apim_apiv4        | `plans`                   | `commentMessage`                   | string                                | Never will, Subscriptions are always auto-accepted                    |
| apim_apiv4        | `plans`                   | `commentRequired`                  | boolean                               | Never will, Subscriptions are always auto-accepted                    |
| apim_apiv4        | `plans`                   | `order`                            | integer                               | Never will, mapped to the list index, UI feature only                 |
| apim_application  |                           | `apiKeyMode`                       | enum (SHARED, EXCLUSIVE, UNSPECIFIED) | Only EXCLUSIVE is supported, hence property is absent                 |
| apim_application  |                           | `type`                             | string                                | No (simple applications)                                              |
| apim_subscription | `apim_subscriptionSpec`   | `apiKeyMode`                       | enum (SHARED, EXCLUSIVE, UNSPECIFIED) | Only EXCLUSIVE is supported, hence property is absent                 |
| apim_subscription | `apim_subscriptionSpec`   | `startingAt`                       | date-time                             | Never, Subscriptions are always auto-accepted hence started immediately|
| apim_subscription | `apim_subscriptionSpec`   | `generalConditionsAccepted`        | boolean                               | Never, Subscriptions are always auto-accepted                         |
| apim_subscription | `apim_subscriptionSpec`   | `generalConditionsContentRevision` | object (PageRevisionId)               | Never, Subscriptions are always auto-accepted                         |

