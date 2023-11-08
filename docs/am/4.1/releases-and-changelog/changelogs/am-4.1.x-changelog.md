---
description: >-
  This page contains the changelog entries for AM 4.1.x and any future minor or
  patch AM 4.1.x releases
---

# AM 4.1.x

## Gravitee Access Management 4.1.5 - November 8, 2023

<details>
<summary>What's new !</summary>
=**What's new!**

* Addition of Consent settings into the Chart values
* Improve FranceConnect IDP to accept additional query parameters
</details>

<details>
<summary>Bug fixes</summary>


**Other**

* Upgrade Groovy policy https://github.com/gravitee-io/issues/issues/9229[#9229]
* EnrollmentMFA policy doesn't manage the useVariableFactorSecurity setting https://github.com/gravitee-io/issues/issues/9365[#9365]
</details>


## Gravitee Access Management 4.1.4 - November 3, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Use SingleSignOut with linked accounts [#9358](https://github.com/gravitee-io/issues/issues/9358)

</details>

## Gravitee Access Management 4.1.3 - October 27, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Application error when using an undefined translation [#9237](https://github.com/gravitee-io/issues/issues/9237)
* Registration confirmation Javascript error (anti-XSRF token) [#9276](https://github.com/gravitee-io/issues/issues/9276)
* Quotes are lost in Gravitee AM forms [#9326](https://github.com/gravitee-io/issues/issues/9326)
* When a resource plugin has been removed from the installation, other resources may not be loaded [#9344](https://github.com/gravitee-io/issues/issues/9344)
* On error during CONNECT flow redirection is not processed [#9346](https://github.com/gravitee-io/issues/issues/9346)
* User created using SCIM is disabled when password is missing [#9347](https://github.com/gravitee-io/issues/issues/9347)

**Management API**

* Management API hangs completely [#9339](https://github.com/gravitee-io/issues/issues/9339)

**Other**

* EnrollMFA should be able to update the factor [#9350](https://github.com/gravitee-io/issues/issues/9350)

</details>

## Gravitee Access Management 4.1.2 - October 19, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Twilio Phone Extension with Self-Service API [#9289](https://github.com/gravitee-io/issues/issues/9289)

**Other**

* EnrichProfile reset factor defined by EnrollMFA policy [#9161](https://github.com/gravitee-io/issues/issues/9161)

</details>

## Gravitee Access Management 4.1.1 - October 16, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Align XSRF token TTL to the user session TTL [#9282](https://github.com/gravitee-io/issues/issues/9282)

**Management API**

* Wrong values returned by Gravitee AM Management API [#9141](https://github.com/gravitee-io/issues/issues/9141)
* AM Management API should start even with missing or unknown Identity Provider plugins [#9230](https://github.com/gravitee-io/issues/issues/9230)

**Other**

* MS SqlServer 10.2 onwards driver support [#9178](https://github.com/gravitee-io/issues/issues/9178)
* Upgrade script for 3.21.6 does not work as expected [#9288](https://github.com/gravitee-io/issues/issues/9288)
* Update Mongo script to create indices [#9291](https://github.com/gravitee-io/issues/issues/9291)

</details>

## Gravitee Access Management 4.1.0 - September 28, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.1 release notes](../release-notes/).

<details>

<summary>What's new</summary>

**Enterprise Edition**

The MFA Challenge policy is now available to apply an MFA step during actions such as reset password or unlock account.

**Twilio phone factor enhancement**

The MFA phone call factor can now use Twilio's sendDigits function to direct a call to an extension before playing the message with the MFA code.

**Account linking**

The new Account Linking feature automatically links user accounts with identical user attributes to bypass re-enrollment during authentication.

**Session management**

Consent to a new session cookie option prevents logout following a period of idling and extends the session expiration.

</details>

<details>

<summary>Breaking changes</summary>

* AM 4.1 requires Java 17 as the runtime
* The versions of the R2DBC drivers must be compatible with R2DBC-SPI 1.0 (i.e., the driver version must start with 1.x). Versions used:
  * postgresql: **1.0.2.RELEASE**\
    mariadb: **1.1.2**\
    mysql: **1.0.2**\
    mssql: **1.0.0.RELEASE**
  * **WARNING** ⚠️ **DO NOT** use the **1.0.2.RELEASE** for **mssql / SQLServer** as this version seems to be buggy (see [r2dbc/r2dbc-mssql#276](https://github.com/r2dbc/r2dbc-mssql/issues/276))
*   Default RDMS timeout and connection pool size values have changed:

    * New values:

    ```
        initialSize: 1
        maxSize: 50
        maxIdleTime: 30000
        maxLifeTime: -1
        maxAcquireTime: 3000
        maxCreateConnectionTime: 5000
    ```

    * Previous values:

    ```
        initialSize: 0
        maxSize: 10
        maxIdleTime: 30000
        maxLifeTime: 0 # not valid anymore with R2BC 1.x
        maxAcquireTime: 0 # not valid anymore with R2BC 1.x
        maxCreateConnectionTime: 0 # not valid anymore with R2BC 1.x
    ```

</details>
