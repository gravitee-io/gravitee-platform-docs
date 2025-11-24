---
description: Overview of Gravitee Access Management.
---

# Device Identifier

## Overview

Gravitee Access Management (AM) includes various device identifier mechanisms for remembering the devices your users use for MFA.

## Create a new device identifier

1. In AM Console, click **Settings > Device Identifier**.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3. Select the device identifier type and click **Next**.
4. Enter the configuration details and click **Create**.

## FingerprintJs v3 Community

You don’t need to configure anything extra for FingerprintJS v3 Community device identifiers. Just create the configuration and enable the [remember device feature.](login/remember-authentication-device.md)

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-device-identifier-fpjsv3community.png" alt=""><figcaption><p>FpJS v3 community</p></figcaption></figure>

## FingerprintJs v3 Pro

For FingerprintJs v3 Pro device identifiers, you need to create an account and enter your **Browser token** and **Registration region** (this field is optional for non-European accounts).

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-device-identifier-fpjsv3pro.png" alt=""><figcaption><p>FpJS v3 pro</p></figcaption></figure>
