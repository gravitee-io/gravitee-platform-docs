# Overview

This section explains how to install APIM on Red Hat Enterprise Linux,
CentOS Linux or Oracle Linux using the `yum` package manager.

RPM install is not supported on distributions with old versions of RPM,
such as SLES 11 and CentOS 5 — in this case, you need to link:{{
*/apim/3.x/apim\_installguide\_gateway\_install\_zip.html* |
relative\_url }}\[install API Management with .zip\] instead.

# Configure the package management system (`yum`)

1.  Create a file called `graviteeio.repo` in location
    `/etc/yum.repos.d/` so that you can install APIM directly using
    `yum`:

        [graviteeio]
        name=graviteeio
        baseurl=https://packagecloud.io/graviteeio/rpms/el/7/$basearch
        gpgcheck=0
        enabled=1
        gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey
        sslverify=1
        sslcacert=/etc/pki/tls/certs/ca-bundle.crt
        metadata_expire=300

2.  Enable GPG signature handling, which is required by some of our RPM
    packages:

        sudo yum install pygpgme yum-utils

3.  Before continuing, you may need to refresh your local cache:

        sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'

Your repository is now ready to use.

# Install the APIM components

You can choose to install the full APIM stack or install the components
one by one:

-   link:{{ */apim/3.x/apim\_installguide\_redhat\_stack.html* |
    relative\_url }}\[Install the full APIM stack\] (includes all
    components below)

-   link:{{ */apim/3.x/apim\_installguide\_redhat\_gateway.html* |
    relative\_url }}\[Install APIM Gateway\]

-   link:{{ */apim/3.x/apim\_installguide\_redhat\_management\_api.html*
    | relative\_url }}\[Install APIM API\]

-   link:{{ */apim/3.x/apim\_installguide\_redhat\_management\_ui.html*
    | relative\_url }}\[Install APIM Console\]

-   link:{{ */apim/3.x/apim\_installguide\_redhat\_portal.html* |
    relative\_url }}\[Install APIM Portal\]
