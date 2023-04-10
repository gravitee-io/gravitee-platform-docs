# Prerequisites

This page will walk you through all the prerequisites needed to install Gravitee API Management (APIM) on an Amazon instance. Once completed, you can elect to install all the APIM components individually or install the full APIM stack.

Alternatively, you can skip this page and follow the quick install guide to install all prerequisites and the full APIM stack at the same time.

## Provision an Amazon instance

Provision and start an Amazon instance with the following minimum specifications:

* Instance Type: **t2.medium**
* Storage: Increase the root volume size to **40GB**
* Security Groups: **SSH** access is sufficient

## Setup Gravitee YUM repository

Amazon Linux instances use the package manager `yum`. The steps below show how to use `yum` to set up access to Gravitee's repository containing the components of APIM.&#x20;

1.  Create a file called `/etc/yum.repos.d/graviteeio.repo`:

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
2.  Enable GPG signature handling (required by some of Gravitee's RPM packages):

    ```sh
    sudo yum install pygpgme yum-utils -y
    ```


3.  Refresh the local cache:

    ```sh
    sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
    ```

this\
