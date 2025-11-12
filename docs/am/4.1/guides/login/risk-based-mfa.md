# Risk-based MFA

### Overview

Gravitee Access Management (AM) brings up a new way to configure Multi-Factor authentication.

It is composed of four steps:

* The first step allows you to select your [application factors](docs/am/4.1/guides/multi-factor-authentication/factors.md)
* The second step allows you to configure the way end users will be prompted MFA
* The third step allows you to configure [remember device](remember-authentication-device.md)
* The last step allows you to configure [step-up authentication](step-up-authentication.md)

## Activate MFA

Adaptive access allows you to choose between 4 MFA strategies:

* **OPTIONAL**: The end user can skip MFA for a given amount of time (default is 10 hours)

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-risk-based-optional.png" alt=""><figcaption><p>Optional MFA</p></figcaption></figure>

* **REQUIRED**: The end user will be required to enroll. They will also be challenged at every login.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-risk-based-required.png" alt=""><figcaption><p>Required MFA</p></figcaption></figure>

* **CONDITIONAL**: The end user will be prompted to enroll and challenge in regard to [Adaptive MFA](adaptive-multi-factor-authentication.md)

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-risk-based-conditional.png" alt=""><figcaption><p>Conditional MFA</p></figcaption></figure>

* **RISK-BASED**: The end user will be intelligently prompted MFA based on risk assessments
  1. `Devices`: Will check the device of the User across the security domain (Remember Device needs to be activated to collect the user’s device)
  2. `Ip Reputation score`: Will prompt MFA based on the severity of the IP score (LOW, MEDIUM, HIGH)
  3. `Geolocation Velocity`: Will prompt MFA based on the speed between the 2 last login locations (LOW, MEDIUM, HIGH)

{% hint style="info" %}
If device assessment is enabled, we won’t prompt MFA with `Remember Device` as it would be redundant
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-risk-based-intelligent.png" alt=""><figcaption><p>Risk-based MFA</p></figcaption></figure>

In order to have the GeoVelocity working, you will need:

* The [Gravitee Geoip Plugin](https://download.gravitee.io/#plugins/services/gravitee-service-geoip/) installed in your gateway
* The [Risk Assyassment Plugin](https://download.gravitee.io/#graviteeio-ee/plugins/services/risk-assessment/gravitee-risk-assessment-core/) installed in your gateway
* You will need to activate User activity on both your Gateway and Management API in the `gravitee.yml`

{% code overflow="wrap" %}
```yaml
user:
   activity:
      enabled: true # default is false
      anon: #used to anonymize the user activity
         algorithm: SHA256|SHA512|NONE #default SHA256
         salt: some-salt # default is null meaning the key generated will change every time and data won't be exploitable
      retention:
         time: 3
         unit: MONTHS
      geolocation:
         variation:
            latitude: 0.07 # default to have a geolocation randomised, 0 will give the exact position
            longitude: 0.07 # default to have a geolocation randomised, 0 will give the exact position
```
{% endcode %}

{% hint style="info" %}
If you enable Brute Force Detection, we will also capture the user login attempts.
{% endhint %}

{% hint style="info" %}
User activity won’t be captured with Social login now due to security reasons.
{% endhint %}

### User activity and consent

To capture user activity, the user will have to consent to store the geolocation extracted from the IP as well as the user\_agent.

* `uc_geoip` : consent for IP and geolocation
* `uc_ua` : consent for User Agent

{% code overflow="wrap" %}
```html
    <input class="mdl-checkbox__input" type="checkbox" th:checked="${uc_geoip}" id="uc_geoip" name="uc_geoip">
    <input class="mdl-checkbox__input" type="checkbox" th:checked="${uc_ua}" id="uc_ua" name="uc_ua">
```
{% endcode %}

If they already have consented to these, you can simply add those inputs as `hidden` form fields

{% code overflow="wrap" %}
```html
    <input class="mdl-checkbox__input" type="hidden" value="on" id="uc_geoip" name="uc_geoip">
    <input class="mdl-checkbox__input" type="hidden" value="on" id="uc_ua" name="uc_ua">
```
{% endcode %}

Implicit user consent can be activated via the `gravitee.yml` file on the Gateway side. In the **consent** section of the yaml file, variable **ip** and **user-agent** is introduced for collecting user consent implicitly. Here is an example of how the variables can be set in the `gravitee.yml` file:

```yaml
consent:
  ip: true
  user-agent: true
```
