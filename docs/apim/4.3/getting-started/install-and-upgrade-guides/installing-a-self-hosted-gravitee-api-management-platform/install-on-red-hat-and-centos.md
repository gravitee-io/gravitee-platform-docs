# Installing Gravitee API Management using RPM Packages

## Introduction

You can install Gravitee API Management (APIM) on Red Hat Enterprise Linux, CentOS Linux, or Oracle Linux using the `yum` package manager.

{% hint style="warning" %}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5 — in this case, you need to [install APIM with .zip](install-with-.zip.md) instead.
{% endhint %}

* [Configure the package management system (`yum`)](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
* [Install APIM](install-on-red-hat-and-centos.md#install-apim)
* [Upgrade APIM](install-on-red-hat-and-centos.md#upgrade-apim)
* [Enterprise Edition licensing](install-on-red-hat-and-centos.md#enterprise-edition-licensing)

## Configure the package management system (`yum`)

Amazon Linux instances use the package manager `yum`. The steps below show how to use `yum` to set up access to Gravitee's repository containing the APIM components.

1.  Create a file called `/etc/yum.repos.d/graviteeio.repo` using the following command:

    ```sh
    sudo tee -a /etc/yum.repos.d/graviteeio.repo <<EOF
    [graviteeio]
    name=graviteeio
    baseurl=https://packagecloud.io/graviteeio/rpms/el/7/\$basearch
    gpgcheck=0
    enabled=1
    gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey
    sslverify=1
    sslcacert=/etc/pki/tls/certs/ca-bundle.crt
    metadata_expire=300
    EOF
    ```
2.  Enable GPG signature handling (required by some of Gravitee's RPM packages) by installing the following packages. In many cases, these packages will already be installed on your Amazon Linux instance.

    ```sh
    sudo yum install pygpgme yum-utils -y
    ```
3.  Refresh the local cache:

    {% code overflow="wrap" %}
    ```sh
    sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
    ```
    {% endcode %}

## Install APIM

Choose to either:

* [Install the full APIM stack](install-on-red-hat-and-centos.md#install-the-full-apim-stack) (includes all components)
* [Install components one-by-one](install-on-red-hat-and-centos.md#install-the-components-one-by-one)

{% hint style="warning" %}
An SELinux configuration issue can prevent Nginx from opening on ports 8084/8085. To correct this:

1.  Validate that the port is not listed here:&#x20;

    {% code overflow="wrap" %}
    ```sh
    # semanage port -l | grep http_port_t
    http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
    ```
    {% endcode %}
2.  Add the port to bind to, e.g., 8084:

    ```sh
    # semanage port -a -t http_port_t  -p tcp 8084
    ```
3.  Validate that the port is listed:&#x20;

    {% code overflow="wrap" %}
    ```sh
    # semanage port -l | grep http_port_t
    http_port_t                    tcp      8084, 80, 81, 443, 488, 8008, 8009, 8443, 9000
    ```
    {% endcode %}
4. Restart Nginx
{% endhint %}

### Install the full APIM stack

<details>

<summary>Install the full APIM stack</summary>

### Prerequisites

Before you install the full APIM stack, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum)](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
2.  Install Nginx by running the following commands:

    ```sh
    sudo yum install epel-release
    sudo yum install nginx
    ```

### Install the APIM stack without dependencies

To install the APIM package only, run the following command:

```sh
sudo yum install graviteeio-apim-4x
```

### Install the APIM stack with dependencies

The following command installs both the APIM package and third-party repositories:

```sh
curl -L https://bit.ly/install-apim-4x | bash
```

### Run APIM with `systemd`

To start up the APIM components, run the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl start graviteeio-apim-gateway graviteeio-apim-rest-api
sudo systemctl restart nginx
```

### Check the APIM components are running

When all components are started, you can run a quick test by checking these URLs:

* **APIM Gateway:** `http://localhost:8082/`
* **APIM API:** `http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis`
* **APIM Management:** `http://localhost:8084/`
* **APIM Portal:** `http://localhost:8085/`

</details>

### Install components one-by-one

{% hint style="info" %}
**Gravitee dependencies**

Gravitee's [Installation & Upgrade Guides](../README.md) provide information on how to install Gravitee components. For prerequisite documentation on third-party products such as [MongoDB](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-red-hat/) or [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/8.11/rpm.html), please visit their respective websites.
{% endhint %}

<details>

<summary>Install APIM Gateway</summary>

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)

### Install the APIM Gateway package

To install the last stable version of the Gravitee API Management (APIM) Gateway, run the following command:

```sh
sudo yum install -y graviteeio-apim-gateway-4x
```

### Run APIM Gateway

These steps assume that you are using the default settings.

To configure APIM Gateway to start automatically when the system boots up, run the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl enable graviteeio-apim-gateway
```

To start and stop APIM Gateway, run the following commands:

```sh
sudo systemctl start graviteeio-apim-gateway
sudo systemctl stop graviteeio-apim-gateway
```

These commands provide no feedback as to whether APIM Gateway started successfully. This information is written to the log files located in `/opt/graviteeio/apim/gateway/logs/`.

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the APIM Gateway service, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-gateway
```

To list journal entries for the APIM Gateway service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-gateway --since  "2020-01-30 12:13:14"
```

</details>

<details>

<summary>Install Management API</summary>

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)

### Install the Management API package

To install the last stable version of the management API, run the following command:

```sh
sudo yum install -y graviteeio-apim-rest-api-4x
```

### Run the management API

These steps assume that you are using the default settings.

To configure the Management API to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable graviteeio-apim-rest-api
```

To start and stop the management API, run the following commands:

```sh
$ sudo systemctl start graviteeio-apim-rest-api
$ sudo systemctl stop graviteeio-apim-rest-api
```

These commands provide no feedback as to whether the Management API started successfully. This information is written to the log files located in `/opt/graviteeio/apim/rest-api/logs/`.

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Management API service, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api
```

To list journal entries for the Management API service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api --since  "2020-01-30 12:13:14"
```

</details>

<details>

<summary>Install Management Console</summary>

### Prerequisites

Before you install the Management Console, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](install-on-red-hat-and-centos.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

### Install the Management Console package

To install the last stable version of the Management Console, run the following command:

```sh
$ sudo yum install -y graviteeio-apim-management-ui-4x
```

### Run the Management Console

The Management Console is based on Nginx.

To configure the Management Console to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
```

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Nginx service, run the following command:

```sh
sudo journalctl --unit nginx
```

To list journal entries for the Nginx service starting from a given time, run the following command:

```sh
sudo journalctl --unit nginx --since  "2020-01-30 12:13:14"
```

</details>

<details>

<summary>Install Developer Portal</summary>

### Prerequisites

Before you install the Developer Portal, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](install-on-red-hat-and-centos.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

### Install the Developer Portal package

To install the last stable version of The Developer Portal , run the following command:

```sh
sudo yum install -y graviteeio-apim-portal-ui-4x
```

### Run the Developer Portal

The Developer Portal is based on Nginx.

To configure the Developer Portal to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
```

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Nginx service, run the following command:

```sh
sudo journalctl --unit nginx
```

To list journal entries for the Nginx service starting from a given time, run the following command:

```sh
sudo journalctl --unit nginx --since  "2020-01-30 12:13:14"
```

</details>

## Upgrade APIM

For version 4.1.4 and above, you can upgrade and restart APIM to perform an `rpm` upgrade of APIM components.

{% hint style="warning" %}
Refer to the [changelog](../../../overview/changelog/apim-4.3.x.md) to follow potential breaking changes.
{% endhint %}

The appropriate upgrade process depends on the type of installation. Choose to either:

* [Upgrade the full APIM stack ](install-on-red-hat-and-centos.md#upgrade-the-full-apim-stack)(includes all components)
* [Upgrade components one-by-one](install-on-red-hat-and-centos.md#upgrade-components-one-by-one)

### Upgrade the full APIM stack

To upgrade your APIM installation, perform the package upgrade, then restart APIM:

```sh
sudo yum upgrade -y graviteeio-apim-4x
sudo systemctl daemon-reload
sudo systemctl restart graviteeio-apim-gateway graviteeio-apim-rest-api nginx
```

### Upgrade components one-by-one

To upgrade an APIM component, you can perform a `yum` upgrade and restart APIM.

*   **Upgrade the APIM Gateway package:**

    ```sh
    sudo yum upgrade -y graviteeio-apim-gateway-4x
    sudo systemctl restart graviteeio-apim-gateway
    ```
*   **Upgrade the Management API package:**

    ```sh
    sudo yum upgrade -y graviteeio-apim-rest-api-4x
    sudo systemctl restart graviteeio-apim-rest-api
    ```
*   **Upgrade the Management Console package:**

    ```sh
    sudo yum upgrade -y graviteeio-apim-management-ui-4x
    sudo systemctl restart nginx
    ```
*   **Upgrade the Developer Portal package:**

    ```sh
    sudo yum upgrade -y graviteeio-apim-portal-ui-4x
    sudo systemctl restart nginx
    ```

## Enterprise Edition licensing

To install the Enterprise Edition of APIM requires a license key.&#x20;

{% hint style="info" %}
For information on obtaining a license key, visit the [Gravitee pricing page](https://www.gravitee.io/pricing).&#x20;
{% endhint %}

Users can directly provide the base64-encoded enterprise license with the `GRAVITEE_LICENSE_KEY` environment variable.&#x20;

The default location of the EE license file `license.key` is the `GRAVITEE_HOME/license/license.key` directory. To override this with a different location, provide the absolute path to the license file using the  `-Dgravitee.license` property in the `gravitee.yml` file, e.g., `gravitee_license: /path/to/my/own_license.key`.

To locate the `license.key`, both the `Gateway` and `Management API` components use the following search sequence:

1. The component will first look for the `GRAVITEE_LICENSE_KEY` environment variable
2. If it cannot find the `GRAVITEE_LICENSE_KEY` environment variable, the component will look for an absolute path to the license file in the `license` property of `gravitee.yml`
3. If the license property is not set in the `gravitee.yml` file, the component will try to retrieve the key from the default location `GRAVITEE_HOME/license/license.key`
