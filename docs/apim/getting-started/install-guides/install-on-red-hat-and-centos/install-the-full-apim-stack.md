# Install the Full APIM Stack

This section describes how to install the full APIM stack, including all the components and, optionally, dependencies (MongoDB, Elasticsearch).

* [Install APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_gateway.html)
* [Install APIM API](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_api.html)
* [Install APIM Console](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_ui.html)
* [Install APIM Portal](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_portal.html)

## Prerequisites

Before you install the full APIM stack, you must complete the following configuration.

### Install Nginx

To install Nginx, run the following commands:

```
sudo yum install epel-release
sudo yum install nginx
```

### Configure your package management system

Ensure you have configured your package management system, as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)

### Install the APIM package (no dependencies)

To install the APIM package only, run the following command:

```
sudo yum install graviteeio-apim-3x
```

### Install the APIM package with dependencies

#### Configure dependency repositories

Before you install the APIM package, you may need to add third-party repositories.

**MongoDB**

|   | For guidance on installing and configuring MongoDB, see the [MongoDB Installation documentation](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-red-hat/). |
| - | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

```
echo "[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc" | sudo tee /etc/yum.repos.d/mongodb-org-3.6.repo > /dev/null

sudo yum install -y mongodb-org
sudo systemctl start mongod
```

**Elasticsearch 7.x**

|   | For guidance on installing and configuring Elasticsearch, see the [Elasticsearch Installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/rpm.html#rpm-repo). |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

```
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

#### Install APIM

```
curl -L https://bit.ly/install-apim-3x | bash
```

### Run APIM with `systemd`

To start up the APIM components, run the following commands:

```
sudo systemctl daemon-reload
sudo systemctl start graviteeio-apim-gateway graviteeio-apim-rest-api
sudo systemctl restart nginx
```

### Check the APIM components are running

When all components are started, you can run a quick test by checking these URLs:

| Component       | URL                                                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Gateway    | [http://localhost:8082/](http://localhost:8082/)                                                                                                                     |
| APIM API        | [http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis](http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis) |
| APIM Management | [http://localhost:8084/](http://localhost:8084/)                                                                                                                     |
| APIM Portal     | [http://localhost:8085/](http://localhost:8085/)                                                                                                                     |

\
