# Install on Red Hat and CentOS

This section explains how to install Gravitee API Management (APIM) on Red Hat Enterprise Linux, CentOS Linux, or Oracle Linux using the `yum` package manager.

{% hint style="warning" %}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5 — in this case, you need to [install APIM with .zip](https://docs.gravitee.io/apim/3.x/apim\_installguide\_gateway\_install\_zip.html) instead.
{% endhint %}

## Configure the package management system (`yum`)

Amazon Linux instances use the package manager `yum`. The steps below show how to use `yum` to set up access to Gravitee's repository containing the APIM components.&#x20;

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

* [Install the full APIM stack](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_stack.html) (includes all components below)
* Install APIM Components
  * [Install APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_gateway.html)
  * [Install APIM API](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_api.html)
  * [Install APIM Console](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_ui.html)
  * [Install APIM Portal](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_portal.html)

\
