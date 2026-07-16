---
description: An overview about quick start guide.
metaLinks:
  alternates:
    - quick-start-guide.md
---

# Quick Start Guide

## Overview


Terraform lets you manage APIs and other entities via configuration rather than manual updates in the APIM Console. This lets you automate and version changes to your APIM instance for an Infrastructure as Code (IaC) experience.

You can use Gravitee's Terraform provider to create and manage Gravitee's Terraform resources. The role of the provider is to apply your resources and synchronize them with the Control Plane.

This guide demonstrates Gravitee's Terraform capabilities with a working example.

{% hint style="info" %}
For resource setup details, we strongly encourage you to refer to the [Terraform registry documentation.](https://registry.terraform.io/providers/gravitee-io/apim/latest)
{% endhint %}

## Prerequisites

Before you can use Terraform with Gravitee, you must install Terraform, have a running APIM environment, and obtain credentials to call the Management API (mAPI). To satisfy these prerequisites, complete the following steps:

* Install Terraform. For more information about installing Terraform, see [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
* Install APIM. To quickly get APIM up and running, see the[getting-started](../getting-started/ "mention") guide.

## Install the Gravitee Terraform provider

To install the Gravitee Terraform provider, complete the following steps:

1. Create a directory.
2.  Create a Terraform `provider.tf` configuration file with the following content:

    1.  If you are using a local or self-managed instance:&#x20;

        * Replace `<mAPI host and port>` with the host and port pair corresponding to your Management API. For example, `http://localhost:8083/automation`.
        * Replace xxx with the bearer token you generated in[define-an-apim-service-account-for-terraform.md](define-an-apim-service-account-for-terraform.md "mention").

        ```hcl
        terraform {
          required_providers {
            apim = {
              source  = "gravitee-io/apim"
            }
          }
        }

        provider "apim" {
          server_url = "http://<mAPI host and port>/automation"
          bearer_auth = "xxx"
        }
        ```
    2. If you are using Gravitee Cloud
       * Create a Gravitee Cloud Token
       * Replace 'xxx' with its content, the rest will be set (server, org, env) automatically

    ```tf
    terraform {
      required_providers {
        apim = {
          source  = "gravitee-io/apim"
        }
      }
    }

    provider "apim" {
      cloud_auth  = "xxx"
    }
    ```
3.  To start Terraform, run the following command:

    ```bash
    terraform init
    ```
4.  In the same directory, create a resource configuration file called `api.tf` that has the following content. This instructs Terraform to add a v4 HTTP proxy API with a Keyless plan to your APIM instance.

    ```hcl
    resource "apim_apiv4" "quick-start-api" {
      # should match the resource name
      hrid            = "quick-start-api"
      name            = "[Terraform] Quick Start PROXY API"
      description     = "A simple API that routes traffic to Gravitee echo API"
      version         = "1.0"
      type            = "PROXY"
      state           = "STARTED"         # API will be deployed
      lifecycle_state = "PUBLISHED"       # Will be published in Portal 
      visibility      = "PUBLIC"          # Will be public in the Portal
      listeners = [
        {
          http = {
            type = "HTTP"
            entrypoints = [
              {
                type = "http-proxy"
              }
            ]
            paths = [
              {
                path = "/quick-start-api/"
              }
            ]
          }
        }
      ]
      endpoint_groups = [
        {
          name = "Default HTTP proxy group"
          type = "http-proxy"
          load_balancer = {
            type = "ROUND_ROBIN"
          }
          endpoints = [
            {
              name   = "Default HTTP proxy"
              type   = "http-proxy"
              weight = 1
              inherit_configuration = false
              # Configuration is JSON as endpoint can be custom plugins
              configuration = jsonencode({
                target = "https://api.gravitee.io/echo"
              })
            }
          ]
        }
      ]
      plans = [ 
        {
          hrid = "keyless"
          name        = "KeyLess"
          type        = "API"
          mode        = "STANDARD"
          validation  = "AUTO"
          status      = "PUBLISHED"
          description = "This plan does not require any authentication"
          security = {
            type = "KEY_LESS"
          }
        }
      ]
    }

    ```
5.  To apply the v4 API resource, run the following command:

    ```bash
    terraform apply
    ```

{% hint style="success" %}
The API "\[Terraform] Quick Start PROXY API" has been created, is visible (read-only), and has been deployed to your APIM instance.
{% endhint %}

Next, see the [Terraform registry documentation](https://registry.terraform.io/providers/gravitee-io/apim/latest) for the full set of resources and attributes supported by the APIM Terraform provider.
