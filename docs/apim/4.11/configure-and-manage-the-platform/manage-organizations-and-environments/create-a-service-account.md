---
description: Create a service account in Gravitee API Management for non-human authentication.
metaLinks:
  alternates:
    - create-a-service-account.md
---

# Create a service account

## Overview

A service account is a non-human user account that automated tools, integrations, and agents use to authenticate against the Gravitee API Management (APIM) Management API. Service accounts authenticate using personal access tokens, not passwords, and they carry the same organization and environment roles as human users.

Use a service account when you need a dedicated identity for:

* The Gravitee Federation Agent connecting to APIM
* Terraform provider calls to the Management API
* A third-party federation provider integration, such as AWS API Gateway, Azure API Management, IBM API Connect, MuleSoft Anypoint, Confluent Platform, Solace, or Apigee X
* An MCP server, CI/CD pipeline, or any custom automation that calls the Management API

## Prerequisites

Before creating a service account, confirm the following:

* You have the `ADMIN` role on the target organization, or equivalent permissions to create users.
* You know which organization and environment roles the service account needs for its purpose.

## Create the service account

To create a service account, follow these steps:

1. Log in to your APIM Console.
2. Open **Organization** from the left navigation.
3. Click **Users** under **User Management**.
4. Click **Add user**.

   <!-- TODO: Screenshot of the Users page with the Add user button highlighted -->
   <figure><img src="../../.gitbook/assets/PLACEHOLDER-create-service-account-users-page.png" alt=""><figcaption><p>Users page with the Add user button</p></figcaption></figure>
5. In the **User type** section, select the **Service Account** card.
6. In the **Service Name** field, enter a meaningful name for the service account.
7. Optional: in the **Email** field, enter an address to receive notifications related to this account.

   <!-- TODO: Screenshot of the Pre-register a user form with Service Account selected -->
   <figure><img src="../../.gitbook/assets/PLACEHOLDER-create-service-account-form.png" alt=""><figcaption><p>Service Account form</p></figcaption></figure>
8. Click **Create**.

The service account appears in the **Users** table.

## Assign roles

Assign the service account the minimum roles required for its purpose.

To assign roles, follow these steps:

1. On the **Users** page, click the service account name.
2. In the **Organization** section, select the organization-level roles from the **Roles** dropdown.
3. In the **Environments** section, select the environment roles for each target environment from the **Environment roles** dropdown.

   <!-- TODO: Screenshot of the user detail page showing Organization and Environments sections -->
   <figure><img src="../../.gitbook/assets/PLACEHOLDER-create-service-account-roles.png" alt=""><figcaption><p>Organization and environment role assignment</p></figcaption></figure>
4. Save your changes.

Use-case-specific guidance on role selection:

* **Federation Agent:** requires CRUD permissions on the Integration object at environment level. For details, see [Federation Agent Service Account](../../govern-apis/federation/federation-agent-service-account.md).
* **Terraform:** requires the `ADMIN` role on the organization and the `API_PUBLISHER` role on the environment. For details, see [Define an APIM service account for Terraform](../../terraform/define-an-apim-service-account-for-terraform.md).
* **Third-party federation providers:** see the provider-specific guide under [3rd-party providers](../../govern-apis/federation/3rd-party-providers/).

## Generate a personal access token

The service account authenticates by presenting a personal access token in the `Authorization` header of Management API requests.

To generate a token, follow these steps:

1. On the service account's detail page, scroll to the **Tokens** section.
2. Click **Generate a personal token**.
3. In the **Name** field, enter a name that describes the token's purpose. The name is between 2 and 64 characters.
4. Click **Generate**.

   <!-- TODO: Screenshot of the Generate a token dialog with the Name field -->
   <figure><img src="../../.gitbook/assets/PLACEHOLDER-create-service-account-generate-token.png" alt=""><figcaption><p>Generate a token dialog</p></figcaption></figure>
5. Copy the token from the **Token** field and store it securely.

{% hint style="warning" %}
Copy the token immediately. After you close the dialog, the token can't be displayed again.
{% endhint %}

## Verification

To verify that the service account is configured correctly, follow these steps:

1. Open the **Users** page and confirm the service account appears with the expected roles on the organization and environments.
2. Use the token to call the Management API. For example:

   ```bash
   curl -H "Authorization: Bearer <TOKEN>" \
        https://<apim-host>/management/v2/organizations/<org>/environments/<env>/apis
   ```
3. Confirm the response returns the expected data and isn't rejected with a 401 or 403 error.
