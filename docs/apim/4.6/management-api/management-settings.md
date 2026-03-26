---
description: Configuration guide for management settings.
---

# Management Settings

## Management configuration

You can configure various management settings in the APIM Console **Settings** page with environment variables. For a complete list of these settings, see [Management settings list](management-settings.md#management-settings-list) below. Once you override these properties with environment variables, APIM Console configures them as read-only to prevent you from overwriting the new values in the interface.

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
