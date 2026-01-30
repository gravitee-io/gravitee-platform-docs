# Managing Factors

## Overview

Gravitee Access Management (AM) supports various factors out of the box. These factors can be used as MFA for protecting user account access.

Factors are created and managed on Security Domain level, and can then be reused across all of your applications within that Security Domain.\
\
Some factors also require a [**Resource**](../../resources.md).

## Create a factor

1. In AM Console UI, click **Settings > Multifactor Auth**.
2. Click the plus icon.
3.  Select the factor type and click **Next.**

    <figure><img src="../../../.gitbook/assets/john cr 1.png" alt=""><figcaption><p>Setting up Multifactor Auth from you Security Domain settings.</p></figcaption></figure>
4. Enter the factor details and click **Create**.

You now have a factor that can be enabled on Application level!

### Supported Factors

Gravitee Access Management supports the following Factors:

* Email
* One-time-password (OTP)
* SMS
* Phone Call
* MFA with FIDO2
* Alternative Methods
* Recovery Codes
* HTTP Factor
