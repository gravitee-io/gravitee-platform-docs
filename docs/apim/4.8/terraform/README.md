# Terraform

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

Terraform lets you use configuration files to build and manage your infrastructure. Starting with Gravitee 4.8, local installations of Gravitee support Terraform for an Infrastructure as Code (IaC) approach to API management. This enables users to automate and version control Gravitee APIs.&#x20;

You can use Terraform to interface with Gravitee much like the Gravitee Kubernetes Operator (GKO), where the CI/CD logic that calls the Gravitee Management API (mAPI) and ensures that your API was created properly is generated automatically. This is especially useful if you want to update a large number of APIs, or if you need to ensure that APIs across multiple environments are identical.

The Gravitee Terraform Provider is an open source plugin that is publicly available for download from the Terraform Registry. You can use the provider to create and configure Gravitee components, which Terraform refers to as resources. Examples of Terraform resources in Gravitee are v4 APIs, Shared Policy Groups, Applications, and Subscriptions.

Terraform configuration files are written in HashiCorp Configuration Language (HCL). They define the properties of providers and resources, which Terraform stores as the desired state of the system. When you update a configuration file, Terraform detects the changes to your resources and applies them automatically.

Click on the cards below to learn more about Gravitee's Terraform provider. If you are familiar with Terraform, you can visit the [Gravitee "apim" Terraform Regisitry documentation](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/setup) to get started.

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><a href="quick-start-guide.md">quick-start-guide.md</a></td><td><a href="../.gitbook/assets/0_zbu2Lu5mHT37DPl0.png">0_zbu2Lu5mHT37DPl0.png</a></td></tr><tr><td><a href="example-resource-configurations.md">example-resource-configurations.md</a></td><td><a href="../.gitbook/assets/gravitee+terraform.png">gravitee+terraform.png</a></td></tr></tbody></table>
