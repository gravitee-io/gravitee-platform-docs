# User Management

Accessing the Developer Portal directly from the Management Console automatically signs you in with the same account. However, the power of the Developer Portal revolves around exposing your APIs to both internal and external API consumers. This necessitates the ability to create new accounts which requires some additional configuration.

### User sign-up

The ability to create new user accounts has two requirements:

1. Enabling the **Allow User Registration** option
2. Simple mail transfer protocol (SMTP) configuration to confirm user account creation

As detailed in [General settings](user-management.md#general-settings), the **Allow User Registration** option is already enabled by default.

To view SMTP settings, navigate to **Settings** in the Management Console. Then, in the secondary sidebar, select **Settings** under the **Portal** header in the submenu. The **SMTP** settings are at the bottom of the page; however, for many deployments, these settings will be greyed out. This is due to the `gravitee.yml` configuration file disabling email by default since it requires configuring an SMTP email service. This [SMTP configuration guide](../../../getting-started/configuration/) will walk you through setting up email for your APIM deployment.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 12.03.55 PM.png" alt=""><figcaption><p>SMTP default settings</p></figcaption></figure>

After configuring SMTP, you should be able to create a new user in the Developer Portal. You can test this by opening the Developer Portal in an incognito window to avoid being automatically signed in with the same account being used in the Management Console. In the new incognito window, select **Sign up** at the bottom of the modal. Provide the required information and select the **Sign Up** button.

<figure><img src="../../../.gitbook/assets/Screenshot 2023-06-05 at 12.14.03 PM.png" alt=""><figcaption><p>Developer portal sign up page</p></figcaption></figure>

You should receive a registration confirmation and an email to the address you provided. Open the email and click the link. Make sure the link opens in the incognito tab; otherwise, it will just open the Developer Portal with the account signed into the Management Console.

You will be taken to a page to finalize your account and add a password. By default, the password must meet the following requirements:

* 8 to 32 characters
* no more than 2 consecutive equal characters
* min 1 special characters (@ & # …)
* min 1 upper case character

{% hint style="info" %}
**Password customization**

Password requirements can be modified by changing the regex pattern under **User Management Configuration** in the `gravitee.yml` file or by using environment variables.
{% endhint %}

Once you finish creating your password, you will be able to sign in.

### User overview

All users can be viewed in APIM's Management Console by anyone with administrator privileges. To view users, select **Organization** at the bottom of the sidebar. Once there, navigate to the **Users** tab in the sidebar. Here, you will see a list of all current users tied to the organization. As an administrator, you can select any user for more details and to apply administrative policies. Additionally, admins can pre-register users by clicking the **Add user** button in the top right.

<figure><img src="../../../.gitbook/assets/image (38).png" alt=""><figcaption><p>Management Console user overview</p></figcaption></figure>

{% hint style="info" %}
**Detailed user administration**

For a more detailed look at managing users including roles, groups, and permissions, head over to the [Administration guide.](../../administration/#introduction)
{% endhint %}
