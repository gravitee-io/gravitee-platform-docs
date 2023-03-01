---
title: APIM Installation Guide - Amazon Linux - Prerequisites - Setup Gravitee YUM repository
tags:
  - APIM
  - Installation
  - Prerequisites
  - Amazon
  - YUM repository
---

# Prerequisites - Setup Gravitee YUM repository

## Overview

Amazon Linux instances use the package manager `yum` to manage the softwares on the instances. Gravitee provides a repository with the major components of the API Manager. Follow below instructions to set up the access to that repository.

## Instructions

1.  Create a file called `/etc/yum.repos.d/graviteeio.repo`:

```
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

2.  Enable GPG signature handling (required by some of our RPM
    packages):

    ```
        sudo yum install pygpgme yum-utils -y
    ```

    !!! note

        These packages are already in place on most Amazon Linux instances.

3.  Refresh the local cache:

  ```
        sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
  ```

## Next steps

The next step is [installing a Java 11 jre](installation-guide-amazon-prerequisite-java.md).
