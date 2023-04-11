# Prerequisites

This page will walk you through all the prerequisites needed to install Gravitee API Management (APIM) on an Amazon instance. Once completed, you can elect to install all the APIM components individually or install the full APIM stack.

Alternatively, you can skip this page and follow the quick install guide to install all prerequisites and the full APIM stack at the same time.

## Provision an Amazon instance

{% hint style="warning" %}
Currently, Gravitee does not support the Amazon Linux 2023 image. Please select the Amazon Linux 2 image.
{% endhint %}

Provision and start an Amazon instance with the following minimum specifications:

* Instance Type: **t2.medium**
* Storage: Increase the root volume size to **40GB**
* Security Groups: **SSH** access is sufficient

## Setup Gravitee YUM repository

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



## Install Java 11

Running the Gravitee APIM components requires a Java 11 Java Runtime Environment (JRE). Follow the steps below to install the Java 11 JRE

1. Enable the repository that contains Java:

```sh
sudo amazon-linux-extras enable java-openjdk11
```

2. Install Java:

```sh
sudo yum install java-11-openjdk -y
```

3. Verify:

```sh
java -version
```

{% hint style="info" %}
You don’t have to install this particular build of OpenJDK.
{% endhint %}

## Install MongoDB

APIM uses MongoDB as its default repository to store global configurations. Follow the steps below to set up MongoDB. For further customization to the installation, more information can be found in the [MongoDB Installation documentation.](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-amazon/)

1. Create a file called `/etc/yum.repos.d/mongodb-org-3.6.repo` using the following command:

{% code title="/etc/yum.repos.d/mongodb-org-3.6.repo" %}
```sh
sudo tee -a /etc/yum.repos.d/graviteeio.repo <<EOF
[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc
EOF
```
{% endcode %}

2. Install MongoDB:

```sh
sudo yum install mongodb-org -y
```

3. Enable MongoDB on startup:

```sh
sudo systemctl daemon-reload

sudo systemctl enable mongod
```

4. Start MongoDB:

```sh
sudo systemctl start mongod
```

5. Verify:

```sh
sudo ss -lntp '( sport = 27017 )'
```

You should see that there’s a process listening on that port.

## Install Elasticsearch

APIM uses Elasticsearch as the default reporting and analytics repository. Follow the steps below to set up Elasticsearch. For further customization to the installation, more information can be found in the [Elasticsearch installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo).

### Instructions

1. Create a file called `/etc/yum.repos.d/elasticsearch.repo`using the following command:

{% code title="/etc/yum.repos.d/elasticsearch.repo" %}
```sh
sudo tee -a /etc/yum.repos.d/elasticsearch.repo <<EOF
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md
EOF
```
{% endcode %}

2. Install Elasticsearch:

```sh
sudo yum install --enablerepo=elasticsearch elasticsearch -y
```

3. Enable Elasticsearch on startup:

```sh
sudo systemctl daemon-reload

sudo systemctl enable elasticsearch.service
```

4. Start Elasticsearch:

```sh
sudo systemctl start elasticsearch.service
```

5. Verify:

```sh
sudo ss -lntp '( sport = 9200 )'
```

You should see that there’s a process listening on that port.

## Install Nginx

Both APIM user interfaces (management UI and developer portal) use Nginx as their webserver. Follow the steps below to set up Nginx. For further customization to the installation, more information can be found in the [Nginx Installation documentation.](https://nginx.org/en/linux\_packages.html#Amazon-Linux)

1. Create a file called `/etc/yum.repos.d/nginx.repo` using the following command:

{% code title="/etc/yum.repos.d/nginx.repo" %}
```sh
sudo tee -a /etc/yum.repos.d/nginx.repo <<EOF
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/amzn2/\$releasever/\$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF
```
{% endcode %}

2. Install Nginx:

```sh
sudo amazon-linux-extras install nginx1
```

3. Enable Nginx on startup:

```sh
sudo systemctl daemon-reload

sudo systemctl enable nginx
```

4. Start Nginx:

```sh
sudo systemctl start nginx
```

5. Verify:

```sh
sudo ss -lntp '( sport = 80 )'
```

You should see that there’s a process listening on that port.

## Next steps

You have completed all the prerequisites. The next step is either installing the [individual APIM components](apim-components-installation.md) or [installing the full APIM stack](../install-on-red-hat-and-centos/install-the-full-apim-stack.md) in one go.\


\
