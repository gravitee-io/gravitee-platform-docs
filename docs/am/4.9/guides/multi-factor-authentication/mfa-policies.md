# MFA Policies

## Overview

In addition to configuring MFA on application level, you may also use MFA policies in flow.

## MFA Challenge policy

The MFA Challenge policy is an [Enterprise Edition](../../overview/open-source-vs-enterprise-am/README.md) policy plugin. It allows a security domain or application owner to apply an MFA step during password reset or account unlock, etc., to enforce security and ensure that the user account has not been compromised. You can specify which MFA Factor will be used to do the challenge step.

For example, consider an end user who wants to reset their password. After clicking on the RESET PASSWORD email link, the user must complete the form on the MFA Challenge page before their password can be changed.

<figure><img src="../../../4.1/.gitbook/assets/mfa challenge policy (1).png" alt=""><figcaption><p>Password reset triggers MFA Challenge</p></figcaption></figure>

## MFA Enroll policy

The MFA Enroll policy is an [Enterprise Edition](../../overview/open-source-vs-enterprise-am/README.md) policy plugin. It allows a security domain or application owner to apply an MFA enrollment login flow, etc., to enforce security and ensure that the user account is enrolled with MFA depending on the context. You can specify which MFA Factor will be used to do the enrollment step.

<figure><img src="../../../4.3/.gitbook/assets/john 1.png" alt=""><figcaption><p>Login flow with MFA enrollment policy</p></figcaption></figure>
