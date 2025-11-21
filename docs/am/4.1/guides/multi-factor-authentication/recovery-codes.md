# Recovery Codes

The **recovery code** factor generates a set of recovery codes that the user can use to authenticate in case the other options are not available. The recovery codes are generated and shown only once to the user during the enrollment or login process. It is thus advisable to download and keep the recovery codes in a safe place.

{% hint style="info" %}
The generated recovery codes are alphanumeric and each recovery code can only be used once to ensure greater security.
{% endhint %}

The image below shows an example recovery code factor configuration. The configuration is flexible and allows to set the number of recovery codes and the number of digits for each recovery code as per the customer’s requirements.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-recovery-code-config.png" alt=""><figcaption><p>Configure recovery code</p></figcaption></figure>

This is an example of what it looks like when the recovery codes are generated during the enrollment process. The download option allows users to download the recovery codes in pdf format.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-recovery-code-sample.png" alt=""><figcaption><p>Recovery codes example</p></figcaption></figure>

The image below shows the option when an application is configured with an active recovery code factor:



<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-recovery-code-option.png" alt=""><figcaption><p>Recovery code option</p></figcaption></figure>
