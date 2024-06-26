# Remember Authentication Device

## Overview

You can configure AM to register the device a user uses for authentication. After a successful login attempt, AM adds the trusted device to the user account for a certain period of time and skips MFA as long as the device is known.

## Configure AM to remember an authentication device

1. Configure a [device identifier](../device-identifier.md).
2. In AM Console, select your application.
3. Click the **Settings** tab, then click **Multifactor Auth**.
4. Toggle on **Enable Remember Device**.
5. Enter the details of the device identifier and the amount of time you want to remember the device (2 hours by default).
6. Click **SAVE**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-remember-device.png" alt=""><figcaption><p>AM authentication device</p></figcaption></figure>
