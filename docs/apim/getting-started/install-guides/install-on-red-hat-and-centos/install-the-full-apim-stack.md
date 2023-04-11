# APIM Full Stack Installation

This section describes how to install the full Gravitee API Management (APIM) stack, including all the components and, optionally, dependencies (MongoDB, Elasticsearch).&#x20;

Alternatively, you can install the APIM components individually as detailed on the [APIM Components page.](apim-components-installation.md)

## Prerequisites

Before you install the full APIM stack, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)
2. Install Nginx by running the following commands:

```sh
sudo yum install epel-release

sudo yum install nginx
```

## Install the APIM stack without dependencies

To install the APIM package only, run the following command:

```sh
sudo yum install graviteeio-apim-3x
```

## Install the APIM stack with dependencies

Before you install the APIM package, you may need to add third-party repositories.

### **MongoDB**

{% hint style="info" %}
For guidance on installing and configuring MongoDB, see the [MongoDB Installation documentation](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-red-hat/).
{% endhint %}

{% code overflow="wrap" %}
```sh
echo "[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc" | sudo tee /etc/yum.repos.d/mongodb-org-3.6.repo > /dev/null

sudo yum install -y mongodb-org

sudo systemctl start mongod
```
{% endcode %}

### **Elasticsearch 7.x**

{% hint style="info" %}
For guidance on installing and configuring Elasticsearch, see the [Elasticsearch Installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/rpm.html#rpm-repo).
{% endhint %}

```sh
echo "[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md" | sudo tee /etc/yum.repos.d/elasticsearch.repo > /dev/null

sudo yum install -y elasticsearch

sudo systemctl start elasticsearch
```

### Install APIM stack

```sh
curl -L https://bit.ly/install-apim-3x | bash
```

## Run APIM with `systemd`

To start up the APIM components, run the following commands:

```sh
sudo systemctl daemon-reload

sudo systemctl start graviteeio-apim-gateway graviteeio-apim-rest-api

sudo systemctl restart nginx
```

## Check the APIM components are running

When all components are started, you can run a quick test by checking these URLs:

| Component       | URL                                                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Gateway    | [http://localhost:8082/](http://localhost:8082/)                                                                                                                     |
| APIM API        | [http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis](http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis) |
| APIM Management | [http://localhost:8084/](http://localhost:8084/)                                                                                                                     |
| APIM Portal     | [http://localhost:8085/](http://localhost:8085/)                                                                                                                     |

{% hint style="success" %}
Congratulations, you have a fully functional Gravitee APIM!
{% endhint %}
