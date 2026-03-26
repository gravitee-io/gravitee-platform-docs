---
description: API and reference documentation for Language Default Properties Reference.
---

# Language Default Properties Reference

## Email templates

| Property Name                                       | Default Value                                                                                                                                              |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| email.common.unit.hours                             | hour(s)                                                                                                                                                    |
| email.common.unit.minutes                           | minute(s)                                                                                                                                                  |
| common.back.to.sign.in                              | Back to sign in                                                                                                                                            |
| email.blocked\_account.subject                      | Account has been locked                                                                                                                                    |
| email.blocked\_account.header.title                 | Hi {0}, your account has been blocked due to some unusual sign-in activity.                                                                                |
| email.blocked\_account.header.description           | Please contact your administrator for assistance if you believe that you received this message in error.                                                   |
| email.blocked\_account.button                       | Unlock your account                                                                                                                                        |
| email.blocked\_account.description                  | This link will expire in {0,number,integer} {1}. After that, you must submit a new request to your administrator to resend a new recover account email.    |
| email.mfa\_challenge.subject                        | Verification Code                                                                                                                                          |
| email.mfa\_challenge.header.title                   | Hi {0}                                                                                                                                                     |
| email.mfa\_challenge.header.description             | Here is the verification code to login to {0}.                                                                                                             |
| email.mfa\_challenge.description                    | This code is only valid for {0,number,integer} {1}.                                                                                                        |
| email.reset\_password.subject                       | Please reset your password                                                                                                                                 |
| email.reset\_password.header.title                  | Hi {0}, there was a request to reset your password.                                                                                                        |
| email.reset\_password.header.description            | If you didn’t ask to reset your password, you can ignore this email.                                                                                       |
| email.reset\_password.button                        | Reset my password                                                                                                                                          |
| email.reset\_password.description                   | This link will expire in {0,number,integer} {1}. After that, you must submit a new request to ask for a new password.                                      |
| email.registration\_confirmation.subject            | New user registration                                                                                                                                      |
| email.registration\_confirmation.header.title.app   | Welcome on {0}, {1}                                                                                                                                        |
| email.registration\_confirmation.header.title       | Welcome {0}                                                                                                                                                |
| email.registration\_confirmation.header.description | To complete your registration, simply confirm that we have the correct email. If you didn’t create this account, you can ignore this message.              |
| email.registration\_confirmation.button             | Confirm my account                                                                                                                                         |
| email.registration\_confirmation.description        | This link will expire in {0,number,integer} {1}. After that, you must submit a new request to your administrator to resend a new account activation email. |

## Login form

| Property Name               | Default Value                                    |
| --------------------------- | ------------------------------------------------ |
| login.title                 | Sign in                                          |
| login.description           | Don’t have an account yet?                       |
| login.subtitle              | to continue to                                   |
| login.label.username        | Username                                         |
| login.label.password        | Password                                         |
| login.error.default.message | Wrong user or password                           |
| login.button.submit         | Sign in                                          |
| login.forgot.password       | Forgot Password?                                 |
| login.signup                | Sign up!                                         |
| login.switch.account        | Switch account                                   |
| login.passwordless          | Sign in with fingerprint, device or security key |
| login.social.before         | Sign in with                                     |

## Forgot password

| Property Name                            | Default Value                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| forgot\_password.title                   | Change your password                                                                              |
| forgot\_password.description             | We’ll send you reset instructions                                                                 |
| forgot\_password.email.placeholder       | Email                                                                                             |
| forgot\_password.button.submit           | Send                                                                                              |
| forgot\_password.success.title           | Check your email                                                                                  |
| forgot\_password.success.description     | We have sent a reset password link                                                                |
| forgot\_password.error.title             | Forgot password error                                                                             |
| forgot\_password.error.description       | Please go back to your client application and try again, or contact the owner and ask for support |
| forgot\_password.error.description.label | Error description:                                                                                |

## Registration

| Property Name                          | Default Value                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| registration.title                     | Register to                                                                                       |
| registration.description               | Already have an account?                                                                          |
| registration.sign.in                   | Sign in                                                                                           |
| registration.button.submit             | Register                                                                                          |
| registration.first.name.placeholder    | First name                                                                                        |
| registration.last.name.placeholder     | Last name                                                                                         |
| registration.user.name                 | User name                                                                                         |
| registration.email.placeholder         | Email                                                                                             |
| registration.password.placeholder      | Password                                                                                          |
| registration.success.title             | Registered successfully                                                                           |
| registration.success.description       | Thank you for creating an account                                                                 |
| registration.error.title               | Registration failed                                                                               |
| registration.error.description         | Please go back to your client application and try again, or contact the owner and ask for support |
| registration.error.description.label   | Error description:                                                                                |
| registration.error.invalid.password    | Invalid password value. It does not comply with the password policy.                              |
| registration.error.invalid.user        | Invalid first name, last name or username.                                                        |
| registration.error.invalid.email       | Invalid email address.                                                                            |
| registration.error.information.missing | Some information are missing or invalid.                                                          |

## Password validation

| Property Name                           | Default Value                                       |
| --------------------------------------- | --------------------------------------------------- |
| password.validation.label               | Password must contains:                             |
| password.minLength.before               | Contains at least                                   |
| password.minLength.after                | characters                                          |
| password.include.numbers                | Contains a number                                   |
| password.include.special.characters     | Contains a special character                        |
| password.letters.mixed.cases            | Contains letters in mixed case                      |
| password.max.consecutive.letters.before | Max                                                 |
| password.max.consecutive.letters.after  | Consecutive letters or numbers                      |
| password.exclude.common.passwords       | Don’t use common names or passwords                 |
| password.exclude.user.info              | Don’t use your profile information in your password |
| password.confirmation.match             | Passwords match                                     |

## Webauthn register

| Property Name                   | Default Value                                                                                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| webauthn.register.title         | Passwordless Authentication                                                                                                                                                          |
| webauthn.register.description   | Follow the instructions in the next step to sign in without a password. Your device will offer you different options like a security key, a fingerprint reader, facial recognition…​ |
| webauthn.register.button.submit | Next                                                                                                                                                                                 |
| webauthn.register.skip          | Skip this step                                                                                                                                                                       |
| webauthn.error                  | Invalid user                                                                                                                                                                         |

## Webauthn login

| Property Name                    | Default Value                                       |
| -------------------------------- | --------------------------------------------------- |
| webauthn.login.description       | Using fingerprint, device or security key           |
| webauthn.login.button.next       | Next                                                |
| webauthn.login.tips              | Follow the instruction in the security window popup |
| webauthn.login.error             | login\_failed                                       |
| webauthn.login.error.description | Invalid user                                        |

## Common across all MFA

| Property Name     | Default Value     |
| ----------------- | ----------------- |
| mfa.otp           | One-Time Password |
| mfa.sms           | SMS               |
| mfa.email         | Email             |
| mfa.http          | HTTP              |
| mfa.fido          | FIDO2             |
| mfa.recovery.code | Recover Code      |
| mfa.call          | Phone call        |

## MFA enroll

| Property Name                     | Default Value                                                                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| mfa\_enroll.title                 | Select a method                                                                                                               |
| mfa\_enroll.description           | Select the authentication method you want to pair with your account                                                           |
| mfa\_enroll.button.submit         | Next                                                                                                                          |
| mfa\_enroll.button.skip           | Skip for now                                                                                                                  |
| mfa\_enroll.button.back           | Back to methods                                                                                                               |
| mfa\_enroll.otp.description       | Use an authenticator app to authenticate                                                                                      |
| mfa\_enroll.otp                   | Scan the QR code with your authentication app (Google Authenticator or FreeOTP) and enter the code displayed in the next step |
| mfa\_enroll.sms.description       | Receive a verification code to your phone to authenticate                                                                     |
| mfa\_enroll.sms                   | We will send a verification code to your phone number                                                                         |
| mfa\_enroll.call                  | Invalid phone number                                                                                                          |
| mfa\_enroll.email.description     | Send an email to your email address                                                                                           |
| mfa\_enroll.email                 | We will send a verification code to your email address                                                                        |
| mfa\_enroll.email.invalid         | Invalid email address                                                                                                         |
| mfa\_enroll.http.description      | Enter the code provided by the HTTP in the next step                                                                          |
| mfa\_enroll.http                  | Go to the next step and enter the code provided by HTTP                                                                       |
| mfa\_enroll.fido.description      | Select 'Next' button to trigger the registration process                                                                      |
| mfa\_enroll.fido                  | Select 'Next' button to trigger registration process                                                                          |
| mfa\_enroll.call.description      | We will call your number to provide the verification code                                                                     |
| mfa\_enroll.on.select.title       | Multi-factor Authentication                                                                                                   |
| mfa\_enroll.on.select.description | Configure multi-factor authentication by choosing the method to validate your identity                                        |

## MFA challenge

| Property Name                  | Default Value                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| mfa\_challenge.title           | Authenticate your account                                                                 |
| mfa\_challenge.otp             | Please type in the code displayed on your multi-factor authenticator app from your device |
| mfa\_challenge.sms             | Please type in the code sent by SMS to your mobile phone                                  |
| mfa\_challenge.call            | You will receive a call shortly. Follow the instructions and type in the given code       |
| mfa\_challenge.email           | Please type in the code sent by email                                                     |
| mfa\_challenge.fido            | Sign in with fingerprint, device or security key                                          |
| mfa\_challenge.error           | Invalid code                                                                              |
| mfa\_challenge.button.submit   | Verify                                                                                    |
| mfa\_challenge.remember.device | Remember my device for                                                                    |
| mfa\_challenge.alternate       | Having trouble? Try other methods                                                         |

## MFA alternative

| Property Name                  | Default Value                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| mfa\_alternative.title         | Select a method                                                                           |
| mfa\_alternative.description   | Try to sign in using other options                                                        |
| mfa\_alternative.otp           | Use a verification code displayed on your multi-factor authenticator app from your device |
| mfa\_alternative.sms           | Receive a verification code to your phone to authenticate                                 |
| mfa\_alternative.email         | Send an email to your email address                                                       |
| mfa\_alternative.http          | Enter the code provided by HTTP in next step                                              |
| mfa\_alternative.fido          | Select the 'Next' button to trigger the registration process                              |
| mfa\_alternative.call          | We will call your number to provide the verification code                                 |
| mfa\_alternative.recovery.code | Use a recovery code previously generated                                                  |
| mfa\_alternative.submit.button | Next                                                                                      |

## MFA Recovery

| Property Name               | Default Value                                                                                                                            |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| mfa\_recovery.title         | Recovery codes                                                                                                                           |
| mfa\_recovery.description   | Recovery codes are used to access your account when you cannot receive two-factor authentication codes. Each code can only be used once. |
| mfa\_recovery.info          | This recovery codes should be stored somewhere safe. They won’t be displayed again.                                                      |
| mfa\_recovery.download      | Download as PDF                                                                                                                          |
| mfa\_recovery.submit.button | Next                                                                                                                                     |

## Reset password

| Property Name                                | Default Value                                                                                     |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| reset\_password.title                        | Set new password                                                                                  |
| reset\_password.description                  | The new password must not use your profile information                                            |
| reset\_password.password.placeholder         | Password                                                                                          |
| reset\_password.confirm.password.placeholder | Confirm password                                                                                  |
| reset\_password.button.submit                | Set new password                                                                                  |
| reset\_password.success.title                | Reset password confirmation                                                                       |
| reset\_password.success.description          | We have reset your password. Go back to your application to login                                 |
| reset\_password.error.title                  | Reset password error                                                                              |
| reset\_password.error.description            | Please go back to your client application and try again, or contact the owner and ask for support |
| reset\_password.error.description.label      | Error description:                                                                                |

## OAuth 2.0 consent

| Property Name             | Default Value                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| oauth.consent.title       | Permissions requested                                                                       |
| oauth.consent.description | would like to                                                                               |
| oauth.disclaimer          | will be able to use your data in accordance to their terms of service and privacy policies. |
| oauth.button.accept       | Accept                                                                                      |
| oauth.button.cancel       | Cancel                                                                                      |

## Identifier first login

| Property Name                   | Default Value                                    |
| ------------------------------- | ------------------------------------------------ |
| identifier\_first.description   | Don’t have an account yet?                       |
| identifier\_first.button.submit | Sign in                                          |
| identifier\_first.passwordless  | Sign in with fingerprint, device or security key |
| identifier\_first.error         | Invalid user                                     |
| identifier\_first.signup        | Sign up!                                         |

## Registration confirmation

| Property Name                                           | Default Value                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| registration\_confirmation.title                        | Sign-up confirmation                                                                              |
| registration\_confirmation.description                  | Thanks for signing up, please complete the form to activate your account                          |
| registration\_confirmation.password.placeholder         | Password                                                                                          |
| registration\_confirmation.confirm.password.placeholder | Confirm password                                                                                  |
| registration\_confirmation.button.submit                | Confirm registration                                                                              |
| registration\_confirmation.success.title                | Account confirmation                                                                              |
| registration\_confirmation.success                      | Thanks for confirming your account. Go back to your application to login                          |
| registration\_confirmation.error.title                  | Account confirmation error                                                                        |
| registration\_confirmation.error.description            | Please go back to your client application and try again, or contact the owner and ask for support |
| registration\_confirmation.error.description.label      | Error description :                                                                               |
| registration\_confirmation.error.invalid.password       | Invalid password value. It does not comply with the password policy.                              |
| registration\_confirmation.error.invalid.user           | Invalid first name, last name or username.                                                        |
| registration\_confirmation.error.invalid.email          | Invalid email address.                                                                            |
| registration\_confirmation.error.information.missing    | Some information are missing or invalid.                                                          |

## Error

| Property Name     | Default Value                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| error.header      | Access error                                                                                      |
| error.description | Please go back to your client application and try again, or contact the owner and ask for support |
