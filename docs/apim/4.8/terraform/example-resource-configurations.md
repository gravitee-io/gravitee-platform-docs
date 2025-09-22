# Gravitee Resources

## Overview

Terraform defines resources as basic infrastructure elements. It creates and manages these resources as part of its Infrastructure as Code (IaC) workflow. This lets you use configuration files to automate reproducible and version controlled APIs.

Resources are classified by type, where a resource type is associated with a particular provider. Gravitee's Terraform provider supports several different resource types, such as v4 APIs and Shared Policy Groups.

To create a resource, you need to add a resource definition to your Terraform configuration file. The definition includes settings such as the resource type, a Human-readable Identifier (hrid) to uniquely identify the resource by name, and arguments to specify other resource parameters.

Terraform uses your configuration files to track the state of your infrastructure. When you update your configuration, Terraform detects the differences between your existing and desired states. It then creates and executes a plan to apply your changes. This is a fully automated alternative to manually updating your APIs in the APIM Console or with mAPI scripts.

## Gravitee resources

The Gravitee Terraform provider supports the following Gravitee resource types:&#x20;

* v4 HTTP proxy API
* v4 message API
* v4 Native Kafka API
* Shared Policy Group

Terraform can create, update, or delete these resources as part of its workflow.&#x20;

{% hint style="info" %}
Guides and examples can be found in the [Gravitee "apim" Terraform Registry documentation](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs).
{% endhint %}

## Known limitations

The following known limitations apply to the 0.2.x version of the Gravitee Terraform provider:

* APIs created with Terraform are shown in the Console with the 'Kubernetes' icon because they are read-only.
* In the `flows` section of the API resource definition, the `name` of the request should match the name of the Shared Policy Group to avoid inconsistencies when `terraform plan` is executed.
* In the `plans` section of the API resource definition, the `name` of the plan should match the key to avoid inconsistencies when `terraform plan` is executed.
* An API that uses a Shared Policy Group in its flow has a field named `sharedPolicyGroupId`  in its state, instead of `hrid`. This has no implications and will be fixed in upcoming releases.
* The `definition_context` section of the API resource definition will be removed in future versions, as it is deprecated but still mandatory.
* `pages` are not yet supported, but will be in an upcoming minor release. Examples will be added.
