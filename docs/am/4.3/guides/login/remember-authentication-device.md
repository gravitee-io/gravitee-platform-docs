# Remember Authentication Device

## Overview

You can configure AM to register the device a user uses for authentication. After a successful login attempt, AM adds the trusted device to the user account for a certain period of time and skips MFA as long as the device is known.

## Configure AM to remember an authentication device

1. Configure a [device identifier](docs/am/4.3/guides/device-identifier.md).
2. In AM Console, click on **Application** in the left sidebar and select your application.
3. Click on **Settings** in the inner left sidebar, then scroll through the headers to click on **Multifactor Auth**.
4. Toggle on **Enable Remember Device**.
5. (Optional) If **Activate MFA** is set to **Conditional** and a rule based on context attributes is provided for the **Condition**, you can toggle on **Skip Remember Device collection if conditional MFA evaluates no risk**. If the condition is met, you can bypass MFA regardless of Remember Device settings.
6. Enter the details of the device identifier and the amount of time you want to remember the device (2 hours by default).
7. Click **SAVE**.

<figure><img src="../../.gitbook/assets/skip remember device.png" alt=""><figcaption><p>AM authentication device</p></figcaption></figure>
