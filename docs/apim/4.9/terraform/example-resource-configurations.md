# Gravitee Resources

## Overview

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

Terraform defines resources as basic infrastructure elements. It creates and manages these resources as part of its Infrastructure as Code (IaC) workflow. This lets you use configuration files to automate reproducible and version controlled APIs.

Resources are classified by type, where a resource type is associated with a particular provider. Gravitee's Terraform provider supports several different resource types, such as v4 APIs, Shared Policy Groups, Applications, and Subscriptions.

To create a resource, you need to add a resource definition to your Terraform configuration file. The definition includes settings such as the resource type, a Human-readable Identifier (hrid) to uniquely identify the resource by name, and arguments to specify other resource parameters.

Terraform uses your configuration files to track the state of your infrastructure. When you update your configuration, Terraform detects the differences between your existing and desired states. It then creates and executes a plan to apply your changes. This is a fully automated alternative to manually updating your APIs in the APIM Console or with mAPI scripts.

## Gravitee resources

The Gravitee Terraform provider supports the following Gravitee resource types:&#x20;

* v4 HTTP proxy API
* v4 message API
* v4 Native Kafka API
* Shared Policy Group
* Application
* Subscription

Terraform can create, update, or delete these resources as part of its workflow.&#x20;

{% hint style="info" %}
Guides and examples can be found in the [Gravitee "apim" Terraform Registry documentation](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs).
{% endhint %}

## Known limitations

The following known limitations apply to the 0.2.x version of the Gravitee Terraform provider:

* APIs created using Terraform are shown in the Console with the 'Kubernetes' icon because they are read only.
* When you run `terraform plan` for APIs, several differences exist between state and remote. These do not impact runtime and will be fixed in upcoming patches.&#x20;
  * Pages appear as changed, but they are unordered.
  * State stores the dynamic properties service configuration as an encoded JSON string instead of plain JSON.
  * The encrypted properties payload is marked as changed because encrypted values replace unencrypted values.
  * A plan's "general conditions" page cannot be linked to the plan using the page hrid.
* APIKey subscriptions are not supported.
