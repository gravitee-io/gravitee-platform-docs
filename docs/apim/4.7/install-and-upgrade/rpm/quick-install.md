---
description: Setup instructions and guidance for quick install.
---

# Quick install

{% hint style="warning" %}
* This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
* RPM install is not supported on distributions with old versions of RPM. For example, SLES 11 and CentOS 5 . If you use an old version of RPM, install Gravitee APIM with .zip instead. For more information about installing Gravitee APIM with .zip, see [install APIM with .zip](../.zip.md).
{% endhint %}

## Prerequisites

* Starting with Gravitee version 4.7, JDK 21 is mandatory.
* If you're running the Enterprise Edition of Gravitee, you need a license key. For more information about Enterprise Edition licensing, see [Enterprise Edition](../../overview/enterprise-edition.md).

## Install APIM

To install Gravitee's APIM stack, use the following command:

```bash
curl -L https://bit.ly/install-apim-4x | bash
```

To verify that you installed Gravitee APIM correctly, send four API calls using the following commands on the machine hosting APIM:

{% hint style="info" %}
If needed, change the host names
{% endhint %}

```bash
curl -X GET http://localhost:8082/
curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
curl -X GET http://localhost:8085/
```
