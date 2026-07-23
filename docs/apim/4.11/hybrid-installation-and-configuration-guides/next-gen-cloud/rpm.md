---
description: An overview about RPM.
---

# RPM

## Overview

This guide explains how to install the Gravitee Hybrid Gateway using the RPM package. This installation type is suitable for Linux distributions and flexible deployments.

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Prerequisites

Before you install a Hybrid Gateway, complete the following steps:

* Ensure that Java 21 is available in the `$PATH`.
* Ensure that you have outbound internet access to Gravitee Cloud Gate (`eu.cloudgate.gravitee.io` or `us.cloudgate.gravitee.io`) over HTTPS (443).
* Install Redis.
* Complete the steps in [#prepare-your-installation](./#prepare-your-installation "mention").

## Install Gravitee APIM

1.  Create a YUM repository for Gravitee packages using the following commands:

    ```bash
    sudo tee -a /etc/yum.repos.d/graviteeio.repo <<EOF
    [graviteeio]
    name=graviteeio
    baseurl=https://packagecloud.io/graviteeio/rpms/el/7/\$basearch
    gpgcheck=1
    repo_gpgcheck=1
    enabled=1
    gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey,https://packagecloud.io/graviteeio/rpms/gpgkey/graviteeio-rpms-319791EF7A93C060.pub.gpg
    sslverify=1
    sslcacert=/etc/pki/tls/certs/ca-bundle.crt
    metadata_expire=300
    EOF

    sudo yum --quiet makecache --assumeyes --disablerepo='*' --enablerepo='graviteeio'
    ```
2.  Install the Hybrid Gateway using the following command. This installs the Gateway at `/opt/graviteeio/apim/graviteeio-apim-gateway`.

    ```bash
    sudo yum install graviteeio-apim-gateway-4x -y
    ```
3. Configure the Gateway section of your `gravitee.yml` file:
   1.  To access your `gravitee.yml` file, use the following command:

       ```bash
       sudo vi /opt/graviteeio/apim/graviteeio-apim-gateway/config/gravitee.yml
       ```
   2.  Use the following configuration in the Gateway section of `gravitee.yml`:

       ```yaml
       management:
         type: http

       cloud:
         token: <YOUR-CLOUD-TOKEN>

       ratelimit:
         type: none

       license:
         key: <YOUR-LICENSE-KEY>
       ```

       * Replace `<YOUR-CLOUD-TOKEN>` with your Cloud Token.
       * Replace `<YOUR-LICENSE-KEY>` with your License Key.
4.  Start the Gateway using the following command:

    ```bash
    sudo systemctl start graviteeio-apim-gateway
    ```
5.  (Optional) To enable the service on boot, use the following command:

    ```bash
    sudo systemctl enable graviteeio-apim-gateway
    ```

## Verification

To verify that the installation was successful, complete the following steps:

1.  Open the logs for the installation using the following command:

    ```bash
    sudo tail -f /opt/graviteeio/apim/graviteeio-apim-gateway/logs/gravitee.log
    ```
2. Navigate to the `/sync` and `/reports` endpoints. If these endpoints have synced successfully, your installation is correct.

## Package location

To find the package for your version, browse the full list of packages in the Gravitee repository on packagecloud at [https://packagecloud.io/graviteeio/rpms](https://packagecloud.io/graviteeio/rpms). Select the `graviteeio-apim-gateway-4x` package and the version you need.
