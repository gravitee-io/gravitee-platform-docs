# Manual install

{% hint style="warning" %}
* RPM install is not supported on distributions with old versions of RPM. For example, SLES 11 and CentOS 5 . If you use an old version of RPM, install Gravitee APIM with .zip instead. For more information about installing Gravitee APIM with .zip, see [install APIM with .zip](../.zip.md).
* This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Prerequisites

* Starting with Gravitee version 4.7, JDK 21 is mandatory.
* If you're running the Enterprise Edition of Gravitee, you need a license key. For more information about Enterprise Edition licensing, see [Enterprise Edition](../../overview/enterprise-edition.md).

### Prerequisites for installing Gravitee APIM on an Amazon instance

<details>

<summary>Prerequisites for installing Gravitee APIM on an Amazon instance</summary>

**NOTE:** Gravitee supports only the Amazon Linux 2 image.

You can run Gravitee APIM on Amazon EC2 instances. However, if you run Gravitee APIM on an Amazon instance, there are the following additional requirements:

* The EC2 instance type must be at least t2.medium.
* The root volume size must be at least 40GB.
* The security group must allow SSH connection to connect and install the Gravitee components.
* The security group must allow access to ports 8082, 8083, 8084, and 8085.

</details>

### Create a Gravitee YUM repository

Many enterprise Linux instances use the package manager `yum`. If you use an enterprise Linux-compatible operating system, you can create a YUM repository for Gravitee containing the APIM components.

<details>

<summary>Create a Gravitee YUM repository</summary>

1. Create a file called `/etc/yum.repos.d/graviteeio.repo` using the following command:

```sh
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
```

{% hint style="info" %}
Since APIM 4.7.5, RPM packages are signed with GPG. To verify the packages, use the `gpgcheck=1` configuration.
{% endhint %}

2. Refresh the local cache using the following command:

```sh
sudo yum --quiet makecache --assumeyes --disablerepo='*' --enablerepo='graviteeio'
```

</details>

### Install Nginx

You must install Nginx to run Gravitee APIM. To install Nginx, complete the following steps:

<details>

<summary>Install Nginx</summary>

1. Install Nginx using the following YUM commands:

```bash
sudo yum install epel-release
sudo yum install nginx
```

**Note:** If you use an Amazon Linux, install Nginx using the following:

```sh
sudo amazon-linux-extras install nginx1
```

2. Enable Nginx using the following commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nginx
```

3. Start Nginx using the following commands:

```sh
sudo systemctl start nginx
```

**Verification**

To verify that you installed Nginx correctly, verify that nginx is listening on port 80 using the following command:

```bash
sudo ss -lntp '( sport = 80 )'
```

**(Optional) Manually Adding Nginx Repository to YUM**

In some cases, you may need to manually add the Nginx repository to yum.

To manually add the Nginx repository to YUM, create a file called `/etc/yum.repos.d/nginx.repo` using the following command:

```sh
export OS_TYPE=rhel # types listed at https://nginx.org/packages/
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

The above commands to install and start Nginx will now run using this repository.

</details>

## Install the Gravitee API Management components

<details>

<summary>Install Java 21</summary>

To install Java 21, use either of the following commands depending on your operating system:

*   If you are running Gravitee APIM on an Amazon Linux, enable the repository that contains Java using the following command:


    ```sh
    sudo amazon-linux-extras enable java-openjdk21
    ```



-   If you are running APIM on any other operating system, install Java using the following the command:


    ```sh
    sudo yum install java-21-openjdk -y
    ```



**Verification**

Verify that you installed Java correctly using the following command:

```sh
java -version
```

</details>

<details>

<summary>Install MongoDB</summary>

Gravitee API Management uses MongoDB as its default repository to store global configurations.

1. To install MongoDB, use the following command:

```sh
sudo yum install mongodb-org -y
```

2. Enable MongoDB using the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl enable mongod
```

3. Start MongoDB using the following command:

```sh
sudo systemctl start mongod
```

**Verification**

To verify that you installed MongoDB correctly, verify that there is a process listening on port 27017 using the following command:

```sh
sudo ss -lntp '( sport = 27017 )'
```

**Manually Adding MongoDB Repository to YUM**

In some cases, you may need to manually add the MongoDB repository to yum. To manually add MongoDB repository to YUM, create a file called `/etc/yum.repos.d/mongodb-org-7.0.repo` using the following command:

```sh
export OS_TYPE=redhat # Replace redhat with amazon as needed
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

The above commands to install and start MongoDB will now run using this repository.

</details>

<details>

<summary>Install ElasticSearch</summary>

Gravitee API Management uses ElasticSearch as the default reporting and analytics repository.

1. To install ElasticSearch, use the following command:

```sh
sudo yum install --enablerepo=elasticsearch elasticsearch -y
sudo sed "0,/xpack.security.enabled:.*/s/xpack.security.enabled:.*/xpack.security.enabled: false/" -i /etc/elasticsearch/elasticsearch.yml
```

2. Enable ElasticSearch using the following command:

<pre class="language-sh"><code class="lang-sh"><strong>sudo systemctl daemon-reload
</strong><strong>sudo systemctl enable elasticsearch.service
</strong></code></pre>

3. Start ElasticSearch using the following command:

```sh
sudo systemctl start elasticsearch.service
```

**Verification**

To verify that you installed ElasticSearch correctly, verify that there is a process listening on port 9200 using the following command:

```sh
sudo ss -lntp '( sport = 9200 )'
```

**Manually Adding ElasticSearch Repository to YUM**

In some cases, you may need to manually add the ElasticSearch repository to yum.

To manually add ElasticSearch repository to YUM, create a file called `/etc/yum.repos.d/elasticsearch.repo` using the following command:

```sh
sudo tee -a /etc/yum.repos.d/elasticsearch.repo <<EOF
[elasticsearch]
name=Elasticsearch repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
```

The above commands to install and start ElasticSearch will now run using this repository.

</details>

<details>

<summary>Install Gravitee API Management components</summary>

Depending on your environment's configuration, you can install only the APIM components that you want for your environment.

1. You can install the components that you want for your environment by using any combination of the following commands:

```sh
sudo yum install -y graviteeio-apim-gateway-4x
sudo yum install -y graviteeio-apim-rest-api-4x
sudo yum install -y graviteeio-apim-management-ui-4x
sudo yum install -y graviteeio-apim-management-ui-4x
```

2. (Optional) For each component, you can configure that component to start automatically when the server loads. To configure the component to start automatically, use the following commands, replacing the component with the desired one:

```sh
export AUTOSTART_COMPONENT="graviteeio-apim-gateway-4x"
sudo systemctl daemon-reload
sudo systemctl enable $AUTOSTART_COMPONENT
```

The Management API log files are located in `/opt/graviteeio/apim/rest-api/logs/`. When `systemd` logging is enabled, the logging information is available using the `journalctl` commands. The same `journalctl` commands can be used for each APIM component.

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

## **Verification**

To verify that you installed Gravitee APIM correctly, send four API calls using the following commands on the machine hosting APIM:

{% hint style="info" %}
If needed, change the hostnames
{% endhint %}

```bash
curl -X GET http://localhost:8082/
curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
curl -X GET http://localhost:8085/
```
