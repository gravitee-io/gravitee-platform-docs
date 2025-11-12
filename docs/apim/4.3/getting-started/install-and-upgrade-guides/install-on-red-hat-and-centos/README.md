# Install on Red Hat and CentOS

This section explains how to install Gravitee API Management (APIM) on Red Hat Enterprise Linux, CentOS Linux, or Oracle Linux using the `yum` package manager.

{% hint style="warning" %}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5 — in this case, you need to [install APIM with .zip](docs/apim/4.3/getting-started/install-and-upgrade-guides/installing-a-self-hosted-gravitee-api-management-platform/install-with-.zip.md) instead.
{% endhint %}

## Configure the package management system (`yum`)

Amazon Linux instances use the package manager `yum`. The steps below show how to use `yum` to set up access to Gravitee's repository containing the APIM components.

1. Create a file called `/etc/yum.repos.d/graviteeio.repo` using the following command:

{% code title="/etc/yum.repos.d/graviteeio.repo" %}
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
{% endcode %}

2. Enable GPG signature handling (required by some of Gravitee's RPM packages) by installing the following packages. In many cases, these packages will already be installed on your Amazon Linux instance.

```sh
sudo yum install pygpgme yum-utils -y
```

3. Refresh the local cache:

{% code overflow="wrap" %}
```sh
sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
```
{% endcode %}

## Install APIM

You can choose to install the full APIM stack or install the components one by one:

* [Install the full APIM stack](apim-full-stack-installation.md) (includes all components below)
* Install APIM Components
  * [Install APIM Gateway](apim-components-installation.md#install-apim-gateway)
  * [Install APIM Management API](apim-components-installation.md#install-management-api)
  * [Install APIM Console](apim-components-installation.md#install-management-console)
  * [Install APIM Developer Portal](apim-components-installation.md#install-developer-portal)

## Upgrade APIM

For version 4.1.4 and above, you can upgrade and restart APIM to perform an `rpm` upgrade of APIM components.

{% hint style="warning" %}
Refer to the [changelog](docs/apim/4.3/overview/changelog/apim-4.3.x.md) to follow potential breaking changes.
{% endhint %}

The appropriate upgrade process depends on the type of installation:

* [Upgrade the full APIM stack](apim-full-stack-installation.md#upgrade)
* Upgrade APIM Components
  * [Upgrade APIM Gateway](apim-components-installation.md#upgrade-the-apim-gateway-package)
  * [Upgrade APIM Management API](apim-components-installation.md#upgrade-the-management-api-package)
  * [Upgrade APIM Console](apim-components-installation.md#upgrade-the-management-console-package)
  * [Upgrade APIM Developer Portal](apim-components-installation.md#upgrade-the-developer-portal-package)

## Enterprise Edition licensing

To install the Enterprise Edition of APIM requires a license key.&#x20;

{% hint style="info" %}
For information on obtaining a license key, visit the [Gravitee pricing page](https://www.gravitee.io/pricing).&#x20;
{% endhint %}

The default location of the EE license file `license.key` is the `GRAVITEE_HOME/license/license.key` directory. To override this with a different location, provide the absolute path to the license file using one of the following:

* The `GRAVITEE_LICENSE_KEY` environment variable, e.g., `export GRAVITEE_LICENSE_KEY="/path/to/my/own_license.key"`
* The  `license` property in the `gravitee.yml` file, e.g., `gravitee_license: /path/to/my/own_license.key`

To locate the `license.key`, both the `Gateway` and `Management API` components use the following search sequence:

1. The component will first look for the `GRAVITEE_LICENSE_KEY` environment variable
2. If it cannot find the `GRAVITEE_LICENSE_KEY` environment variable, the component will look for an absolute path to the license file in the `license` property of `gravitee.yml`
3. If the license property is not set in the `gravitee.yml` file, the component will try to retrieve the key from the default location `GRAVITEE_HOME/license/license.key`
