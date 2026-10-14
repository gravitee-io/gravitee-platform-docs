---
description: Manage Access Management 4.13 security domains, identity providers, certificates, reporters, and data planes from Terraform configuration files with the AM Terraform provider.
---

# Manage AM with Terraform

The AM Terraform provider manages Access Management resources from Terraform configuration files. It makes every change through the [Automation API](automation-api.md), so each resource it creates is identified by a key you choose, and a key reaches only a resource that the Automation API created.

{% hint style="warning" %}
The AM Terraform provider is an alpha release that works with AM 4.13.0. Its version numbers don't follow AM's.
{% endhint %}

## What the provider manages

The provider manages the following resources:

| Resource | Manages | Identified by |
| -------- | ------- | ------------- |
| `am_data_plane` | A data plane of the environment. | `id` |
| `am_domain` | A security domain of the environment. | `key` |
| `am_identity_provider` | An identity provider of a security domain. | `domain_key` and `key` |
| `am_certificate` | A certificate of a security domain. | `domain_key` and `key` |
| `am_reporter` | A reporter of a security domain. | `domain_key` and `key` |

Each resource has a data source of the same name, which reads an existing resource without managing it. For every attribute of each resource and data source, see the [AM provider documentation](https://registry.terraform.io/providers/gravitee-io/am/latest/docs) in the Terraform Registry.

## Prerequisites

Before you use the AM Terraform provider, complete the following steps:

* Enable the Automation API on the AM Management API. See [Automation API](../getting-started/configuration/configure-automation-api.md).
* Get a token for the Automation API, such as a service account access token. See [Authentication](automation-api.md#authentication).
* Install Terraform. See [Install Terraform](https://developer.hashicorp.com/terraform/install).

## Configure the provider

To configure the provider, complete the following steps:

1. In a new directory, create a `provider.tf` file with the following content. Replace `<management-api-host>` with the host of your AM Management API.

    ```hcl
    terraform {
      required_providers {
        am = {
          source = "gravitee-io/am"
        }
      }
    }

    provider "am" {
      server_url = "https://<management-api-host>/automation"
    }
    ```

2. Set the `AM_SA_TOKEN` environment variable to your token:

    ```bash
    export AM_SA_TOKEN=<token>
    ```

3. Initialize the directory:

    ```bash
    terraform init
    ```

The provider takes the following settings. When a setting is absent from the `provider` block, the provider reads its environment variable instead.

| Setting | Environment variable | Description | Default |
| ------- | -------------------- | ----------- | ------- |
| `server_url` | `AM_SERVER_URL` | URL of the Automation API: the Management API URL followed by the Automation API entrypoint, `/automation` by default. | `http://localhost:8093/automation` |
| `bearer_auth` | `AM_SA_TOKEN` | Token sent with every request. | None. A plan without a token fails with `Missing Provider Security Configuration`. |
| `organization_id` | `AM_ORG_ID` | Identifier of the organization that owns the environment. | `DEFAULT` |
| `environment_id` | `AM_ENV_ID` | Identifier of the environment the provider manages. | `DEFAULT` |
| `http_headers` | None | Headers added to every request. | None |

## Create a security domain

By default, a security domain created in AM Console gets a default certificate, identity provider, and reporter. A security domain that the Automation API creates gets none of them. To add them, declare each one with `system = true`. AM then builds it from the default settings of your installation, and it needs only a `domain_key` and a `key`.

To create a security domain with its default identity provider, certificate, and reporter, complete the following steps:

1. In the same directory, create a `domain.tf` file with the following content:

    ```hcl
    resource "am_domain" "example" {
      key           = "example-domain"
      name          = "Example domain"
      path          = "/example-domain"
      data_plane_id = "default"
    }

    resource "am_identity_provider" "default" {
      domain_key = am_domain.example.key
      key        = "default-idp"
      system     = true
    }

    resource "am_certificate" "default" {
      domain_key = am_domain.example.key
      key        = "default-certificate"
      system     = true
    }

    resource "am_reporter" "default" {
      domain_key = am_domain.example.key
      key        = "default-reporter"
      system     = true
    }
    ```

2. Review the changes Terraform plans to make:

    ```bash
    terraform plan
    ```

3. Apply them:

    ```bash
    terraform apply
    ```

## Change a resource

Terraform applies most changes to the existing resource. The following changes work differently:

* **A new `key`, or a new `id` or `type` for a data plane.** Terraform deletes the resource and creates it again.
* **A new `data_plane_id` for a security domain.** Terraform deletes the security domain and creates it again on the other data plane. Deleting a security domain also deletes its applications, identity providers, certificates, reporters, and the rest of its configuration, so read the plan before you apply this change.
* **A new `type`, or a change to `system`, for an identity provider, a certificate, or a reporter.** AM rejects the change with a message that says the field is immutable, and the resource stays as it is. To change either one, delete the resource and create it again.

## How secrets are handled

The Automation API never returns secret values, so the provider handles them as follows:

* AM returns each sensitive setting in the `configuration` of an identity provider, a certificate, or a reporter as `********`. The provider treats `********` as equal to the value in your configuration, so a plan shows no change for it, and the Terraform state keeps the value you configured.
* AM never returns the `configuration` of a data plane. The provider sends the value in your configuration with every change.
* Terraform can't detect a secret changed outside Terraform. The next apply that changes the resource sends the configured value again.

Because the Terraform state holds the secrets you configure, store the state where only the people who manage AM can read it.

## Delete a resource

AM refuses some deletions that `terraform destroy` or a removed resource block requests:

* A data plane isn't deleted while a security domain uses it.
* A certificate isn't deleted while an application, an identity provider, or a protected resource uses it.
* An identity provider isn't deleted while an application uses it.

## Import a resource

To manage a resource that the Automation API created outside your Terraform configuration, import it with an `import` block. The import ID is a JSON object that names the resource:

```hcl
import {
  to = am_identity_provider.users
  id = jsonencode({
    organization_id = "DEFAULT"
    environment_id  = "DEFAULT"
    domain_key      = "example-domain"
    key             = "users"
  })
}
```

For a security domain, leave out `domain_key`. For a data plane, leave out `domain_key` and replace `key` with `id`. A resource that was created in AM Console or through the Management API has no key, so it can't be imported this way.

## Limitations

The provider has the following limitations:

* `am_data_plane` can't manage the `default` data plane or a data plane declared in the configuration of your installation. AM rejects it with `'<id>' is reserved for a data plane declared in the gravitee.yml`. To create a security domain on one of these data planes, set its identifier in `data_plane_id`.
* To leave the gateway URL of a data plane unset, leave out `gateway_url`. AM stores an empty value as unset.
* When the Management API runs on several nodes, a node that hasn't loaded a new data plane yet rejects a security domain created on it with `An error occurred while trying to create a domain. Data Plane [<id>] is not loaded on this node.` This can happen when the data plane and the security domain are created in the same apply. Run `terraform apply` again.
