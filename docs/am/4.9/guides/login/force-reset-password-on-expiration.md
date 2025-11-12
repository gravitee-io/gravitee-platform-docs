# Force Reset Password on Expiration

## Overview

If a [password policy](../user-management/password-policy.md#configure-a-password-policy) is configured with an expiration period, you can enable the `Force reset password on expiration` option to prompt users to reset their password during the login phase. Enabling the option lets **email-less** users reset an expired password.

## Configuration

The force reset password functionality can be enabled at the domain level, or for a specific application by toggling the `Force reset password on expiration` option, which can be found under the **Login** settings section. Enabling this option has no effect unless a [password policy](../user-management/password-policy.md#configure-a-password-policy) is configured with an expiration duration.

<figure><img src="../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

## Behavior

When the `Force reset password on expiration` option is enabled:

* Users attempting to log in with an expired password are automatically redirected to the `/resetPassword` page.
* This redirection facilitates a direct password change, even if the user's profile does not have an associated email address.

When the option is disabled:

* Users with expired passwords are redirected back to the login page with the `error_code=account_password_expired` parameter.
* To regain access, users must follow the "forgot password" flow. To use the "forgot password" flow, the user's profile must be associated with a valid email address.
