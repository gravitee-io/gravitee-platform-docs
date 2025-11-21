# RPM

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
* [#install-java-21](./#install-java-21 "mention")
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

### Install Java 21

* Install Java 21 using either of the following commands:
  *   (**Red Hat, CentOS, and Ubuntu only**) To install Java21, use the following command:

      ```bash
      sudo yum install java-21-openjdk -y
      java -version
      ```
  *   (**Amazon only**) To install Java21, use the following command:

      ```bash
      sudo amazon-linux-extras enable java-openjdk21
      ```

### Install MongoDB

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
    sudo yum install graviteeio-apim-gateway graviteeio-apim-management-api graviteeio-apim-portal graviteeio-apim-console -y
    ```
*   Initialize the Gravitee APIM components using the following commands:

    ```bash
    # Enable and start
    sudo systemctl daemon-reload
    sudo systemctl enable graviteeio-apim-gateway
    sudo systemctl start graviteeio-apim-gateway

    sudo systemctl enable graviteeio-apim-management-api
    sudo systemctl start graviteeio-apim-management-api

    sudo systemctl enable graviteeio-apim-portal
    sudo systemctl start graviteeio-apim-portal

    sudo systemctl enable graviteeio-apim-console
    sudo systemctl start graviteeio-apim-console
    ```

## Verification

{% hint style="info" %}
The services may take a few minutes to initialize.
{% endhint %}

{% include "../../.gitbook/includes/verify-console-and-portal-access.md" %}
