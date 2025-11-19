# Prerequisites

This page describes how to install the prerequisites required to run Gravitee API Management (APIM) on an Amazon instance.

## Provision an Amazon instance

{% hint style="warning" %}
Currently, Gravitee does not support the Amazon Linux 2023 image. Please select the Amazon Linux 2 image.
{% endhint %}

Provision and start an Amazon instance with the following minimum specifications:

* Instance Type: **t2.medium**
* Storage: Increase the root volume size to **40GB**
* Security Groups: **SSH** access is sufficient

## Set up Gravitee YUM repository

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

## Install Java 17

Running the Gravitee APIM components requires a Java 17 Java Runtime Environment (JRE). Follow the steps below to install the Java 17 JRE:

1. Enable the repository that contains Java:

```sh
sudo amazon-linux-extras enable java-openjdk17
```

2. Install Java:

```sh
sudo yum install java-17-openjdk -y
```

3. Verify:

```sh
java -version
```

{% hint style="info" %}
You don’t have to install this particular build of OpenJDK.
{% endhint %}

## Install MongoDB

APIM uses MongoDB as its default repository to store global configurations. Follow the steps below to set up MongoDB. For further customization of the installation, refer to the [MongoDB Installation documentation.](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-amazon/)

1. Create a file called `/etc/yum.repos.d/mongodb-org-7.0.repo` using the following command:

{% code title="/etc/yum.repos.d/mongodb-org-7.0.repo" %}
```sh
case "`uname -i`" in
    x86_64|amd64)
        baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/7.0/x86_64/;;
    aarch64)
        baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/7.0/aarch64/;;
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
{% endcode %}

2. Install MongoDB:

```sh
sudo yum install mongodb-org -y
```

3. Enable MongoDB on startup:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable mongod
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

## Install ElasticSearch

APIM uses ElasticSearch as the default reporting and analytics repository. Follow the steps below to set up ElasticSearch. For further customization to the installation, more information can be found in the [ElasticSearch installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo).

### Instructions

1. Create a file called `/etc/yum.repos.d/elasticsearch.repo`using the following command:

{% code title="/etc/yum.repos.d/elasticsearch.repo" %}
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
{% endcode %}

2. Install ElasticSearch:

```sh
sudo yum install --enablerepo=elasticsearch elasticsearch -y
sudo sed "0,/xpack.security.enabled:.*/s/xpack.security.enabled:.*/xpack.security.enabled: false/" -i /etc/elasticsearch/elasticsearch.yml
```

3. Enable ElasticSearch on startup:

<pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
</strong><strong>$ sudo systemctl enable elasticsearch.service
</strong></code></pre>

4. Start ElasticSearch:

```sh
sudo systemctl start elasticsearch.service
```

5. Verify:

```sh
sudo ss -lntp '( sport = 9200 )'
```

You should see that there’s a process listening on that port.

## Install Nginx

Both APIM user interfaces (Management Console and Developer Portal) use Nginx as their webserver. Follow the steps below to set up Nginx. For further customization of the installation, refer to the [Nginx Installation documentation.](https://nginx.org/en/linux_packages.html#Amazon-Linux)

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
priority=9
EOF
```
{% endcode %}

2. Install Nginx:

```sh
sudo amazon-linux-extras install nginx1
```

3. Enable Nginx on startup:

<pre class="language-sh"><code class="lang-sh">$ sudo systemctl daemon-reload
<strong>$ sudo systemctl enable nginx
</strong></code></pre>

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

You have completed all the prerequisites. The next step is to either [install the individual APIM components](apim-components-installation.md) or [install the full APIM stack](gravitee-components.md).
