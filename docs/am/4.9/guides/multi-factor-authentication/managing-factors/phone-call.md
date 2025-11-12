# Phone Call

With phone call verification, you can receive a verification code via a phone call to be used as the second factor to validate a user’s account.

{% hint style="info" %}
Phone call MFA requires a compatible [resource](docs/am/4.9/guides/resources.md).
{% endhint %}

If you enable a **Call** type factor for your application, the next time your users log in they will see the following screens:

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-call-enroll.png" alt=""><figcaption><p>Voice call MFA screen 1</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-call-challenge.png" alt=""><figcaption><p>Voice call MFA screen 2</p></figcaption></figure>

{% hint style="info" %}
You can change the look and feel of forms using [custom pages](../../branding/#custom-pages). The enrollment form must send the phone number using the `phone` parameter in E.164 notation.
{% endhint %}

#### Twilio phone factor enhancement

Support for phone number extensions promotes the adoptability of MFA by offering a solution that does not require the involvement of a personal device. Instead, MFA can use office extensions to rely on a corporate phone network.

To implement this service, the enrollment screen for a Twilio phone factor offers an optional field in which to enter an extension. If an extension is present in the user's enrollment data, the MFA call utilizes Twilio's sendDigits function to direct the call to the extension before playing the audible message containing the MFA code.
