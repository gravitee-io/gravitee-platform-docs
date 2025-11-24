---
description: Configuration guide for User and Management Configuration.
---

# User and Management Configuration

## Introduction

The following sections discuss user and management configuration.

## User configuration

You can configure various user options:

* `user.login.defaultApplication`: `boolean` (default: `true`): Creates a new application for all new users
* `user.creation.token.expire-after`: `number` (default: `86400`): Number of seconds before the user registration token expires
* `user.reference.secret`: `32 characters` (default: `s3cR3t4grAv1t33.1Ous3D4R3f3r3nc3`): Secret used to generate a unique anonymous reference to a user; **You must change this value**
* `user.anonymize-on-delete:enabled`: `boolean` (default: `false`): If true, the user's first name, last name, and email are anonymized when a user is deleted

## Management configuration

You can configure various management settings in the APIM Console **Settings** page with environment variables. For a complete list of these settings, see [Management settings list](user-and-management-configuration.md#management-settings-list) below. Once you override these properties with environment variables, APIM Console configures them as read-only to prevent you from overwriting the new values in the interface.

{% hint style="info" %}
For array properties, separate your environment variable properties with a comma. For example: `my_var=item1,item2,item3`.
{% endhint %}

For example, you can override the analytics client timeout with either of the following environment variables:

```
gravitee_analytics_client_timeout=15000
gravitee.analytics.client.timeout=15000
```

### Management settings list

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-rest-api/gravitee-apim-rest-api-model/src/main/java/io/gravitee/rest/api/model/parameters/Key.java" %}
