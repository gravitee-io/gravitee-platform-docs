---
description: Terraform authenticates to API Management 4.12 as a user of the instance. Follow the steps to create a Terraform service account.
metaLinks:
  alternates:
    - define-an-apim-service-account-for-terraform.md
---

# Define an APIM service account for Terraform

## Overview


For Terraform to use APIM, it needs to authenticate as a user of the APIM instance.

To set Terraform up as an APIM user, you need to create a service account with specific roles on the organization and environment. This provides Terraform with the minimum set of permissions to manage APIs, applications, and other assets in APIM.

This guide explains how to define an APIM service account for Terraform so it can call the Management API (mAPI).

## Create a Terraform service account

To create a Terraform service account, complete the following steps:

1. Log in to your APIM Console.
2.  Select **Organization** from the navigation menu.

    <figure><img src="../.gitbook/assets/00.png" alt="The console dashboard with Organization highlighted at the foot of the left navigation, showing no APIs and one application."><figcaption></figcaption></figure>
3.  From the Organization navigation menu, select **Users**, and then click **Add user**.

    <figure><img src="../.gitbook/assets/01 (1).png" alt="The organization Users page with Users highlighted in the left navigation and the Add user button highlighted, listing one administrator."><figcaption></figcaption></figure>
4. Select **Service Account** as the service type, and then enter a value for **Service Name**. Providing a service account email is optional.
5.  Click **Create**.

    <figure><img src="../.gitbook/assets/02 (1).png" alt="The Pre-register a user page with Service Account selected, a service name entered, and the Create button highlighted."><figcaption></figcaption></figure>
6.  From the **Users** screen, click on your service account.

    <figure><img src="../.gitbook/assets/03 (1).png" alt="The organization Users page listing an administrator and a service account, with the service account row highlighted."><figcaption></figcaption></figure>
7.  Ensure that your service account has the ADMIN role on the organization, and the API\_PUBLISHER role on the desired environment.

    <figure><img src="../.gitbook/assets/04 (2).png" alt="The detail page of a service account, with the organization role set to ADMIN highlighted in two places and the environment role set to API_PUBLISHER."><figcaption></figcaption></figure>

    \
    The following screenshot shows the environment-level permissions that are included in the API\_PUBLISHER role:

    <figure><img src="../.gitbook/assets/05 (1).png" alt="A permissions matrix for a role, with create, read, update, and delete ticked for API, application, integration, and shared policy group, and read ticked for group and platform."><figcaption></figcaption></figure>
8.  From your newly created service account, scroll to the **Tokens** section, and then click **Generate a personal token**.

    <figure><img src="../.gitbook/assets/06 (1).png" alt="The detail page of a service account scrolled to the Tokens panel, with the Generate a personal token button highlighted above empty API, application, and token lists."><figcaption></figcaption></figure>
9.  Give your token a name, and then click **Generate**.

    <figure><img src="../.gitbook/assets/07 (1).png" alt="The Generate a token dialog with a token name entered and the Generate button highlighted."><figcaption></figcaption></figure>
10. Copy your token and store it securely. You won’t be able to see it again.

{% hint style="success" %}
You can now use this token as credentials in your Terraform provider configuration file.
{% endhint %}
