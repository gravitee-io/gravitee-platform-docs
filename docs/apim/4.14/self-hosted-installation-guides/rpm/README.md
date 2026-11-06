---
description: Install API Management 4.13 on RPM-based Linux such as Red Hat, CentOS, or Oracle. Follow the steps for your distribution.
metaLinks:
  alternates:
    - ./
---

# Self-host with RPM

## Overview

This guide explains how to install Gravitee APIM on RPM-based Linux distributions like Red Hat, CentOS, and Oracle. To install APIM, you must verify prerequisites, create repositories, and start services.

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Prerequisites

Before you install APIM with RPM packages, complete the following steps:

* Install an RPM-based Linux operating system.

## Install APIM with RPM packages

To install APIM with RPM packages, complete the following steps:

* [#create-a-yum-repository](./#create-a-yum-repository "mention")
* [#install-nginx](./#install-nginx "mention")
* [#install-java-25](./#install-java-25 "mention")
* [#install-mongodb](./#install-mongodb "mention")
* [#install-elasticsearch](./#install-elasticsearch "mention")
* [#install-and-start-gravitee-api-management-components](./#install-and-start-gravitee-api-management-components "mention")

### Create a YUM repository

*   Create a YUM repository using the following commands:

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

### Install Nginx

1. Install Nginx using either of the following methods:
   *   Install Nginx automatically using the following commands:

       ```bash
       sudo yum install epel-release -y
       sudo yum install nginx -y
       sudo systemctl daemon-reload
       sudo systemctl enable nginx
       sudo systemctl start nginx
       ```
   *   Manually add nginx to your repository using the following commands:

       ```bash
       export OS_TYPE=rhel
       sudo tee -a /etc/yum.repos.d/nginx.repo <<EOF
       [nginx-stable]
       name=nginx stable repo
       baseurl=http://nginx.org/packages/$OS_TYPE/\$releasever/\$basearch/
       gpgcheck=1
       enabled=1
       gpgkey=https://nginx.org/keys/nginx_signing.key
       module_hotfixes=true
       priority=9
       EOF
       ```
2.  Verify that you installed Nginx correctly using the following command:

    ```bash
    sudo ss -lntp "( sport = 80 )"
    ```

### Install Java 25

The Gateway and the Management API require Java 25. The Console and the Developer Portal are static files and don't need Java.

* Install Java 25 using one of the following commands:
  *   (**Red Hat Enterprise Linux 9 and 10, and compatible distributions**) To install Java 25, use the following commands:

      ```bash
      sudo yum install java-25-openjdk-headless -y
      java -version
      ```
  *   (**Amazon Linux 2023**) To install Java 25, use the following commands:

      ```bash
      sudo dnf install java-25-amazon-corretto-headless -y
      java -version
      ```

{% hint style="warning" %}
Red Hat Enterprise Linux 8 doesn't provide a Java 25 package. Its repositories stop at `java-21-openjdk`, which can't run APIM 4.13. Red Hat Enterprise Linux 9 and 10 provide `java-25-openjdk-headless`. Amazon Linux 2 doesn't provide a Java 25 package either.
{% endhint %}

{% hint style="info" %}
If another Java version is already installed, `java -version` can still report it after you install Java 25. To make Java 25 the default, run `sudo alternatives --config java` and select the Java 25 entry.
{% endhint %}

### Install MongoDB

{% hint style="info" %}
You can use other databases to store configuration management data (see [JDBC repositories](../../prepare-a-production-environment/repositories/README.md)).
{% endhint %}

1. Install MongoDB using either of the following methods:
   *   Install MongoDB automatically using the following commands:

       ```bash
       sudo yum install mongodb-org -y
       sudo systemctl daemon-reload
       sudo systemctl enable mongod
       sudo systemctl start mongod
       ```
   *   Manually add MongoDB to your repository using the following commands:

       ```bash
       export OS_TYPE=redhat # or amazon
       case "`uname -i`" in
       x86_64|amd64)
         baseurl=https://repo.mongodb.org/yum/$OS_TYPE/2/mongodb-org/7.0/x86_64/;;
       aarch64)
         baseurl=https://repo.mongodb.org/yum/$OS_TYPE/2/mongodb-org/7.0/aarch64/;;
       esac

       sudo tee -a /etc/yum.repos.d/mongodb-org-7.0.repo <<EOF
       [mongodb-org-7.0]
       name=MongoDB Repository
       baseurl=${baseurl}
       gpgcheck=1
       enabled=1
       gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
       EOF
       ```
2.  Verify that you installed MongoDB correctly using the following command:

    ```bash
    sudo ss -lntp "( sport = 27017 )"
    ```

### Install Elasticsearch

1.  Install Elasticsearch using the following commands:

    ```bash
    sudo yum install --enablerepo=elasticsearch elasticsearch -y
    sudo sed "0,/xpack.security.enabled:.*/s//xpack.security.enabled: false/" -i /etc/elasticsearch/elasticsearch.yml
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch.service
    sudo systemctl start elasticsearch.service
    ```
2.  Verify that you installed Elasticsearch correctly using one of the following commands:

    ```bash
    curl -X GET --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:<YOUR_ELASTIC_PASSWORD> "https://localhost:9200/?pretty"
    # OR (dev only):
    curl -X GET --insecure -u elastic:<YOUR_ELASTIC_PASSWORD> "https://localhost:9200/?pretty"
    ```

    * Replace `<YOUR_ELASTIC_PASSWORD>` with your Elastic password.

### Install and start Gravitee API Management components

*   Install the Gravitee APIM components using the following command:

    ```bash
    sudo yum install graviteeio-apim-gateway-4x graviteeio-apim-rest-api-4x graviteeio-apim-management-ui-4x graviteeio-apim-portal-ui-4x -y
    ```
*   Initialize the Gravitee APIM components using the following commands:

    ```bash
    # Enable and start
    sudo systemctl daemon-reload
    sudo systemctl enable graviteeio-apim-gateway
    sudo systemctl start graviteeio-apim-gateway

    sudo systemctl enable graviteeio-apim-rest-api
    sudo systemctl start graviteeio-apim-rest-api
    ```

## Verification

{% hint style="info" %}
The services may take a few minutes to initialise.
{% endhint %}

To verify that Gravitee API Management is installed and running as expected, follow these steps:

1.  Confirm that the APIM Gateway service is active using the following command:

    ```bash
    sudo systemctl status graviteeio-apim-gateway
    ```

    The command reports `Active: active (running)`.<br>
2.  Confirm that the APIM Management API service is active using the following command:

    ```bash
    sudo systemctl status graviteeio-apim-rest-api
    ```

    The command reports `Active: active (running)`.<br>
3.  Confirm that the four APIM component ports are listening using the following command:

    ```bash
    sudo ss -lntp "( sport = 8082 or sport = 8083 or sport = 8084 or sport = 8085 )"
    ```

    The output lists one listening socket on each of the following ports:

    * `8082` — APIM Gateway
    * `8083` — APIM Management API
    * `8084` — APIM Management Console (served by Nginx)
    * `8085` — Developer Portal (served by Nginx)<br>
4. Open the APIM Management Console in a web browser at `http://<YOUR_HOST>:8084`, and sign in with the default credentials `admin` / `admin`. The Management Console home page appears.<br>
5. Open the Developer Portal in a web browser at `http://<YOUR_HOST>:8085`. The Developer Portal home page appears.
