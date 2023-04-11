# Install on Red Hat and CentOS

This section explains how to install Gravitee API Management (APIM) on Red Hat Enterprise Linux, CentOS Linux, or Oracle Linux using the `yum` package manager.

{% hint style="warning" %}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5 — in this case, you need to [install APIM with .zip](https://docs.gravitee.io/apim/3.x/apim\_installguide\_gateway\_install\_zip.html) instead.
{% endhint %}

## Configure the package management system (`yum`)

1. Create a file called `graviteeio.repo` in location `/etc/yum.repos.d/` so that you can install APIM directly using `yum`:

{% code title="/etc/yum.repos.d/graviteeio.repo" %}
```
[graviteeio]
name=graviteeio
baseurl=https://packagecloud.io/graviteeio/rpms/el/7/$basearch
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
```
{% endcode %}

2. Enable GPG signature handling, which is required by some of our RPM packages:

```sh
sudo yum install pygpgme yum-utils
```

3. Before continuing, you may need to refresh your local cache:

```sh
sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
```

Your repository is now ready to use.

## Install APIM

You can choose to install the full APIM stack or install the components one by one:

* [Install the full APIM stack](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_stack.html) (includes all components below)
* Install APIM Components
  * [Install APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_gateway.html)
  * [Install APIM API](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_api.html)
  * [Install APIM Console](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_ui.html)
  * [Install APIM Portal](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_portal.html)

\
