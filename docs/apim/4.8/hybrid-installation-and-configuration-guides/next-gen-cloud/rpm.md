---
description: An overview about rpm.
---

# RPM

## Overview

This guide explains how to install the Gravitee Hybrid Gateway using either the RPM package or ZIP archive. This installation type is suitable for Linux distributions and flexible deployments.

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Prerequisites

Before you install a Hybrid Gateway, complete the following steps:

* Ensure that Java 17 is available in the `$PATH`.
* Ensure that you have outbound internet access to Gravitee Cloud Gate (`eu.cloudgate.gravitee.io` or `us.cloudgate.gravitee.io`) over HTTPS (443).
* Install Redis.
* Complete the steps in [#prepare-your-installation](./#prepare-your-installation "mention").

## Install Gravitee APIM

1.  Install the RPM package using the following command. This installs the Gateway at `/opt/graviteeio-apim-gateway`.

    ```bash
    sudo rpm -i https://download.gravitee.io/gateway/4.x/rpm/graviteeio-apim-gateway-latest.rpm
    ```
2. Configure the Gateway section of your `gravitee.yml` file:
   1.  To access your `gravitee.yml` file, use the following command:

       ```bash
       sudo vi /opt/graviteeio-apim-gateway/config/gravitee.yml
       ```
   2.  Use the following configuration in the Gateway section of `gravitee.yml`:

       ```yaml
       management:
         type: http

       cloud:
         token: <YOUR-CLOUD-TOKEN>

       ratelimit:
         type: none
          redis:
            host: localhost
            port: 6379

       license:
         key: <YOUR-LICENSE-KEY>
       ```

       * Replace `<YOUR-CLOUD-TOKEN>` with your Cloud Token.
       * Replace `<YOUR-LICENSE-KEY>` with your License Key.
3.  Start the Gateway using the following command:

    ```bash
    sudo systemctl start graviteeio-apim-gateway
    ```
4.  (Optional) To enable the service on boot, use the following command:

    ```bash
    sudo systemctl enable graviteeio-apim-gateway
    ```

## Verification

To verify that the installation was successful, complete the following steps:

1.  Open the logs for the installation using the following command:

    ```bash
    sudo tail -f /opt/graviteeio-apim-gateway/logs/gravitee.log
    ```
2. Navigate to the `/sync` and `/reports` endpoints. If these endpoints have synced successfully, your installation is correct.
