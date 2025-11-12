# SMS

With SMS verification, you can receive a verification code on your mobile phone to be used as the second factor to validate a user’s account.

SMS MFA requires a compatible [resource](docs/am/4.8/guides/resources.md). Some providers allow you to define the duration of the code sent by SMS. If possible, we advise setting a duration of 2 minutes.

{% hint style="info" %}
Gravitee 4.2 supports a new SMS resource provider based on the SFR vendor. Administrators can set up their SFR credentials to link Gravitee AM to SFR SMS service and activate the MFA SMS factor for selected applications.
{% endhint %}

If you enable an SMS type factor for your application, next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-sms-enroll.png" alt=""><figcaption><p>SMS MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-sms-challenge.png" alt=""><figcaption><p>SMS MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../../branding/#custom-pages). The enrollment form must send the phone number using the `phone` parameter in E.164 notation.
{% endhint %}
