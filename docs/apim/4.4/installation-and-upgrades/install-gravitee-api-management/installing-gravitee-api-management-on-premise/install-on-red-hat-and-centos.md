---
description: >-
  You can install Gravitee’s API Management (APIM) on a Linux operating system
  using the YUM package manager.
---

# Installing Gravitee API Management using RPM Packages

## Before you begin

{% hint style="warning" %}
* RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5 — in this case, you need to [install APIM with .zip](install-with-.zip.md) instead.
* If you use Enterprise Edition of Gravitee, you need a license key. For more information about Enterprise Edition Licensing Licensing, see [Enterprise Edition Licensing.](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing)
{% endhint %}

Amazon Linux instances use the package manager, `yum`. If you use an Amazon Linux operating system, you must configure access to Gravitee’s repository that contains the APIM components.

To establish access to Gravitee’s repository using `yum`, complete the following steps:

1.  Create a file called `/etc/yum.repos.d/graviteeio.repo` using the following command:

    ```sh
    sudo tee -a /etc/yum.repos.d/graviteeio.repo <<EOF
    [graviteeio]
    name=graviteeio
    gpgcheck=1
    repo_gpgcheck=1
    enabled=1
    gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey,https://packagecloud.io/graviteeio/rpms/gpgkey/graviteeio-rpms-319791EF7A93C060.pub.gpg
    sslverify=1
    sslcacert=/etc/pki/tls/certs/ca-bundle.crt
    metadata_expire=300
    EOF
    ```

{% hint style="info" %}
Since APIM 4.4.27, RPM packages are signed with GPG. To verify the packages, use the `gpgcheck=1` configuration.
{% endhint %}

2. Refresh the local cache using the following command:

{% code overflow="wrap" %}
````
```sh
sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
```
````
{% endcode %}

## Installing Gravitee’s API Management

There are two methods that you can use to install Gravitee’s API Management (APIM):

* Quick install. You install all the prerequisites that you need to run Gravitee’s APIM and the full APIM stack.&#x20;
* Manual install. You control the installation of the prerequisites that you need to run APIM. Also, you control the installation of the individual components of the APIM stack

{% hint style="warning" %}
An SELinux configuration issue can prevent Nginx from opening on ports 8084/8085. To correct this:

1. Validate that the port is not listed here:

{% code overflow="wrap" %}
````
```sh
# semanage port -l | grep http_port_t
http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
```
````
{% endcode %}

2.  Add the port to bind to, e.g., 8084:

    ```sh
    # semanage port -a -t http_port_t  -p tcp 8084
    ```
3. Validate that the port is listed:

{% code overflow="wrap" %}
````
```sh
# semanage port -l | grep http_port_t
http_port_t                    tcp      8084, 80, 81, 443, 488, 8008, 8009, 8443, 9000
```
````
{% endcode %}

4. Restart Nginx
{% endhint %}

### Install the full APIM stack

<details>

<summary>Installing Gravitee API Management on Linux with Quick install</summary>

#### Prerequisites

Before you install the full APIM stack, you must complete the following configuration.

1. Install Nginx using the following commands:

```bash
sudo yum install epel-release
sudo yum install nginx
```

2. You can install Gravitee’s APIM stack with dependencies or without dependencies. To install Gravitee’s APIM with dependencies or without dependencies complete the following steps:

* To install Gravitee’s APIM stack without dependencies, use the following command:

```bash
sudo yum install graviteeio-apim-4x
```

* To install Gravitee’s APIM stack with dependencies, use the following command:

```bash
curl -L https://bit.ly/install-apim-4x | bash
```

3. Enable the APIM components using the following commands:

```bash
sudo systemctl daemon-reload
sudo systemctl start graviteeio-apim-gateway graviteeio-apim-rest-api
sudo systemctl restart nginx
```

#### Verification

To verify that you installed Gravitee’s APIM correctly, send four API calls using the following commands:

```bash
$ curl -X GET http://localhost:8082/
$ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
$ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
$ curl -X GET http://localhost:8085/
```

</details>

### Installing Gravitee's API Management components on Linux using Manual install

{% hint style="info" %}
**Gravitee dependencies**

Gravitee's [Installation & Upgrade Guides](../) provide information about how you install Gravitee components. For prerequisite documentation on third-party products like [MongoDB](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-red-hat/) or [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/8.11/rpm.html), please visit their respective websites.
{% endhint %}

Depending on your environment's configuration, you can install only the APIM components that you want for your environment. Here are the components that you can install individually:&#x20;

<details>

<summary>Installing the API Management Gateway</summary>

1. Install the API Management Gateway using the following command:

```sh
sudo yum install -y graviteeio-apim-gateway-4x
```

2. Enable the Gateway using the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl enable graviteeio-apim-gateway
```

3. Start the API Management Gateway, and then stop the API Management gateway using the following commands:

```sh
sudo systemctl start graviteeio-apim-gateway
sudo systemctl stop graviteeio-apim-gateway
```

</details>

<details>

<summary>Install Management API</summary>

#### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)

#### Install the Management API package

To install the last stable version of the management API, run the following command:

```sh
sudo yum install -y graviteeio-apim-rest-api-4x
```

#### Run the management API

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

#### View the logs

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

#### Prerequisites

Before you install the Management Console, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](install-on-red-hat-and-centos.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

#### Install the Management Console package

To install the last stable version of the Management Console, run the following command:

```sh
$ sudo yum install -y graviteeio-apim-management-ui-4x
```

#### Run the Management Console

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

#### View the logs

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

#### Prerequisites

Before you install the Developer Portal, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](install-on-red-hat-and-centos.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](install-on-red-hat-and-centos.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

#### Install the Developer Portal package

To install the last stable version of The Developer Portal , run the following command:

```sh
sudo yum install -y graviteeio-apim-portal-ui-4x
```

#### Run the Developer Portal

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

#### View the logs

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
