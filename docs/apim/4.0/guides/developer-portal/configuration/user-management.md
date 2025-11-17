---
description: This section describes user management configuration in the Developer Portal
---

# User Management

## Overview

When you access the Developer Portal directly from the Management Console, you are automatically signed in with the same account. However, to expose your APIs to consumers you will need to create new accounts, which requires additional configuration.

## User sign-up

To create new user accounts you must:

* Enable the **Allow User Registration** option. This option is a [general setting](broken-reference) and enabled by default.
* Configure simple mail transfer protocol (SMTP) to confirm user account creation. See the sections below for detailed instructions.

### Configure SMTP

To configure SMTP settings:

1. Log in to the Management Console
2. Select **Settings** from the left sidebar
3. Select **Settings** from the inner left sidebar&#x20;
4. Configure the **SMTP** settings are at the bottom of the page

{% hint style="info" %}
By default, the `gravitee.yml` configuration file disables email because email requires configuring an SMTP email service. You must set up email for your APIM deployment per the [SMTP configuration guide](../../../getting-started/configuration/README.md) to be able to modify the SMTP settings.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 12.03.55 PM.png" alt=""><figcaption><p>SMTP default settings</p></figcaption></figure>

### Create a user

After configuring SMTP, you can create a new user in the Developer Portal:

1. Open the Developer Portal in an incognito window to avoid being automatically signed in with the same account used by the Management Console
2. In the new incognito window, select **Sign up** at the bottom of the modal
3. Provide the required information and click the **Sign Up** button

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 12.14.03 PM.png" alt=""><figcaption><p>Developer portal sign up page</p></figcaption></figure>

You will receive a registration confirmation at the email address you provided.&#x20;

### Complete sign-up

To complete the sign-up process:

1. Open the email and click the link
2. Ensure the link opens in the incognito tab (otherwise, the Developer Portal will use the same account as the Management Console)
3. Finalize your account and add a password that meets the following requirements:
   * 8 to 32 characters
   * No more than 2 consecutive identical characters
   * Minimum of 1 special character (@ & # …)
   * Minimum of 1 uppercase character

{% hint style="info" %}
**Password customization**

Password requirements can be modified by changing the regex pattern under **User Management Configuration** in the `gravitee.yml` file or by using environment variables.
{% endhint %}

Once your password has been created, you will be able to sign in.

## User overview

All users can be viewed in the Management Console by anyone with administrator privileges. To view users:

1. Select **Organization** at the bottom of the left sidebar
2. Select **Users** from the organization's left sidebar to display a list of all current users tied to the organization

As an administrator, you can click on an entry for user details and to apply administrative policies. Additionally, admins can pre-register users by clicking the **Add user** button on the top right of the page.

<figure><img src="../../../.gitbook/assets/image (38).png" alt=""><figcaption><p>Management Console user overview</p></figcaption></figure>

{% hint style="info" %}
**Detailed user administration**

For additional information on user management, including roles, groups, and permissions, see the [Administration guide.](../../administration/README.md#introduction)
{% endhint %}
