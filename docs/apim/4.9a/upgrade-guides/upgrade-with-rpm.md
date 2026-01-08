---
description: An overview about upgrade with rpm.
metaLinks:
  alternates:
    - upgrade-with-rpm.md
---

# Upgrade with RPM

## Overview

This page describes how to upgrade your API Management if you installed your API Management with RPM packages.

For versions 4.1.4 of Gravitee and above, you can upgrade and restart Gravitee API Management (APIM) to perform an rpm upgrade of the APIM components.

{% hint style="info" %}
Refer to the Breaking changes and deprecated functionality to follow potential breaking changes.
{% endhint %}

To upgrade your RPM installation, choose the upgrade process depending on your installation:

* Upgrade the full APIM stack (includes all components)
* Upgrade components one-by-one

## Prerequisites

### Backup Configuration Files

The following configuration files will be overwritten during the RPM upgrade process. You must back them up before proceeding:

* `gravitee.yml` or your single configuration file if everything is consolidated
* `constants.json`
* `config.json` for the Developer Portal
* `conf.d` NGINX configuration directory

{% hint style="danger" %}
Failure to backup these files will result in loss of your custom configurations.
{% endhint %}

### Java Version Requirement

Starting in version 4.7, Gravitee APIM requires **Java 21**. If you are deploying APIM with RPM or using the distribution bundle, please ensure you upgrade your Java version before proceeding with the APIM upgrade.

## Upgrade the full APIM stack

To upgrade your APIM installation, perform the package upgrade, and then restart APIM using the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-4x
sudo systemctl daemon-reload
sudo systemctl restart graviteeio-apim-gateway graviteeio-apim-rest-api nginx
```

## Upgrade the individual components

To upgrade an APIM component, you can perform a yum upgrade, and then restart the APIM. You can upgrade the following components:

### Upgrade the APIM Gateway package

To upgrade the APIM Gateway package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-gateway-4x
sudo systemctl restart graviteeio-apim-gateway
```

### Upgrade the Management API package

To upgrade the Management API package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-rest-api-4x
sudo systemctl restart graviteeio-apim-rest-api
```

### Upgrade the Management Console package

To upgrade the Management Console package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-management-ui-4x
sudo systemctl restart nginx
```

### Upgrade the Developer Portal package

```bash
sudo yum upgrade -y graviteeio-apim-portal-ui-4x
sudo systemctl restart nginx
```
