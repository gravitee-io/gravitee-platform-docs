# Upgrade Guide

## Overview

If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

{% hint style="warning" %}
Make sure to run scripts on the correct database since `gravitee-am` is not always the default database! Check your db name by running `show dbs`.
{% endhint %}

## Upgrade to 3.20

### Certificate Rotation

Starting from AM 3.20, the certificate generated during the domain creation is marked as a "system" certificate. This is useful for the new "Certificate Rotation" feature that enables you to generate a new system certificate and then assign this certificate to the applications that are using the previous system certificate.

When the Management API of AM 3.20 is about to start for the first time, the upgrader process will try to mark existing certificates as "system", based on the certificate name (which should be "Default") and the creation date (which should be the same as the domain creation date). If no "system" certificate can be determined, the domain and the application will continue to work without issues.

## Upgrade to 3.19.3

### User Registration and ResetPassword

From AM version 3.19.3, when a custom callback URL is defined for registration or password reset, the query parameters provided during the form post will be propagated to the custom callback URL.

You can disable this behavior by defining this setting in the `gravitee.yaml`:

{% code title="gravitee.yaml" %}
```yaml
legacy:
  registration:
    keepParams: false
  resetPassword:
    keepParams: false
```
{% endcode %}

Another option is to disable it using environment variables, as shown below:

```sh
$ export gravitee_legacy_registration_keepParams = false
$ export gravitee_legacy_resetPassword_keepParams = false
```
