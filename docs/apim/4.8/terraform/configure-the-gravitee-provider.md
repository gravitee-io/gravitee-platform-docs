# Configure the Gravitee Provider

## Overview

The Gravitee Terraform Provider plugin lets you use your infrastructure's tooling and pipelines to access and manage Gravitee APIs.

Gravitee's provider enables Terraform to interact with Gravitee resources, such as APIs and Shared Policy Groups. It specifies how Terraform communicates with these resources, and lets Terraform create, update, or destroy them as part of its workflow.

The provider is declared in a Terraform configuration file, along with access credentials and region-specific parameters. It defines authentication schemes, available API endpoints, and the translations between Terraform configuration blocks and API calls. This is required for reproducible and compatible configurations.

## Prerequisites

Before you configure your provider, ensure you have the following:

* The host and port for your Management API
* Credentials:
  * Service account [define-an-apim-service-account-for-terraform.md](define-an-apim-service-account-for-terraform.md "mention")&#x20;
* (Optional) For a multi-tenant setup:
  * Organization ID&#x20;
  * Environment ID&#x20;

## Provider configuration

The Gravitee Terraform provider is declared and configured in a `.tf` Terraform configuration file.&#x20;

### Declaration block

The provider is defined in the `required_providers` section of the `terraform` code block. The specified version of the Gravitee provider is pulled from the Terraform Registry.&#x20;

Here is a sample declaration block:

```hcl
# When published to the public Terraform Registry, this configuration is all
# that is necessary to use the provider:

terraform {
  required_providers {
    apim = {
      source  = "gravitee-io/apim"
    }
  }
}
```

### Configuration block

The `provider` code block defines the organization settings, credentials, and endpoints that are required by the Gravitee provider. These parameters identify and provide access to a specific Gravitee instance.

#### Example 1

Here is a sample configuration block for a self-hosted Gravitee deployment:

```hcl
provider "apim" {
  server_url      = "https://<mAPI host and port>/automation"
  bearer_auth     = "c7783347-f1bc-45fd-8199-d2ef18d24717" 
}
```

#### Example 2

Here is a sample configuration block for a multi-tenant setup:

```hcl
provider "apim" {
  server_url      = "https://<mAPI host and port>/automation"
  bearer_auth     = "c7783347-f1bc-45fd-8199-d2ef18d24717" 
  environment_id  = "b64ba3fa-1786-455c-a62d-a86cb6db999f"
  organization_id = "c3bfc0f6-e072-4754-b124-7013f1dd51a3"
}
```

## Environment variables

Gravitee Terraform provider can be configured using the following environment variables:&#x20;

| Variable          | Corresponding provider field |
| ----------------- | ---------------------------- |
| APIM\_SERVER\_URL | server\_url                  |
| APIM\_SA\_TOKEN   | bearer\_auth                 |
| APIM\_ORG\_ID     | organization\_id             |
| APIM\_ENV\_ID     | environment\_id              |

If you use only environment variables to configure your provider, then your configuration block looks like this:

```hcl
provider "apim" {
  # Hooray, nothing is hardcoded!
}
```
