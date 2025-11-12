# Email

With Email verification, you can receive a verification code on your email address to be used as the second factor to validate a user’s account.

{% hint style="info" %}
Email MFA requires a compatible [resource](docs/am/4.6/guides/resources.md).
{% endhint %}

Using the `email-am-factor` plugin configuration form, you can define the number of digits used to generate the verification code. The configured resource must be an [SMTP Resource](docs/am/4.6/guides/resources.md#resource-types). The email template used by this plugin is defined in the design section of the domain or application.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-config.png" alt=""><figcaption><p>Email MFA configuration</p></figcaption></figure>

**Subject** and **Template** fields use the freemarker syntax to customize the message content. The generated **code** is available using the expression `${code}`. The user profile and the application are accessible using the expressions `${user}` and `${client}` (ex: `${client.clientName}` will return the application name and `${user.firstName}` will return the first name of the user.)

If you enable an Email type factor for your application, next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-enroll.png" alt=""><figcaption><p>Email MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-email-challenge.png" alt=""><figcaption><p>Email MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../../branding/#custom-pages). The enrollment form must send the email address using the `email` parameter.
{% endhint %}
