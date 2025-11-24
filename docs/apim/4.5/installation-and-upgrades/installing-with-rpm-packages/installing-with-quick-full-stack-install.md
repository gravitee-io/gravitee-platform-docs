---
description: An overview about quick install.
---

# Quick install

{% hint style="warning" %}
* RPM install is not supported on distributions with old versions of RPM. For example, SLES 11 and CentOS 5 . If you use an old version of RPM, install Gravitee APIM with .zip instead. For more information about installing Gravitee APIM with .zip, see [install APIM with .zip](../install-with-.zip.md).
* If you use Enterprise Edition of Gravitee, you need a license key. For more information about Enterprise Edition Licensing Licensing, see [Enterprise Edition Licensing.](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing)
{% endhint %}

1. To install Gravitee's APIM stack, use the following command:

```bash
curl -L https://bit.ly/install-apim-4x | bash
```

**Verification**

* To verify that you installed Gravitee APIM correctly, send four API calls using the following commands on the machine hosting APIM:

{% hint style="info" %}
If needed, change the hostnames.
{% endhint %}

```bash
curl -X GET http://localhost:8082/
curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
curl -X GET http://localhost:8085/
```
