# Manual install

## Introduction

Manual installation requires the following:

* [Install all prerequisites](manual-install.md#prerequisites)
* [Install the full APIM stack](manual-install.md#install-the-apim-full-stack) or [install the individual APIM components](manual-install.md#install-the-individual-apim-components)

## Prerequisites

<details>

<summary>Provision an Amazon instance</summary>

Currently, Gravitee does not support the Amazon Linux 2023 image. Please select the Amazon Linux 2 image.

Provision and start an Amazon instance with the following minimum specifications:

* Instance Type: **t2.medium**
* Storage: Increase the root volume size to **40GB**
* Security Groups: **SSH** access is sufficient

</details>

<details>

<summary>Set up Gravitee YUM repository</summary>

Amazon Linux instances use the package manager `yum`. To use `yum` to set up access to Gravitee's repository containing the APIM components:

1.  Create a file called `/etc/yum.repos.d/graviteeio.repo` using the following command:

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
2.  Enable GPG signature handling (required by some of Gravitee's RPM packages) by installing the following packages. In many cases, these packages will already be installed on your Amazon Linux instance.

    ```sh
    sudo yum install pygpgme yum-utils -y
    ```
3.  Refresh the local cache:

    {% code overflow="wrap" %}
    ```sh
    sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
    ```
    {% endcode %}

</details>

<details>

<summary>Install Java 17</summary>

Running the Gravitee APIM components requires a Java 17 Java Runtime Environment (JRE). Install the Java 17 JRE (this particular build of OpenJDK is not required):

1.  Enable the repository that contains Java:

    ```sh
    sudo amazon-linux-extras enable java-openjdk17
    ```
2.  Install Java:

    ```sh
    sudo yum install java-17-openjdk -y
    ```
3.  Verify:

    ```sh
    java -version
    ```

</details>

<details>

<summary>Install MongoDB</summary>

APIM uses MongoDB as its default repository to store global configurations. Follow the steps below to set up MongoDB. For further customization of the installation, refer to the [MongoDB Installation documentation](https://docs.mongodb.com/v3.6/tutorial/install-mongodb-on-amazon/).

1.  Create a file called `/etc/yum.repos.d/mongodb-org-7.0.repo` using the following command:

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
2.  Install MongoDB:

    ```sh
    sudo yum install mongodb-org -y
    ```
3.  Enable MongoDB on startup:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable mongod
    ```
4.  Start MongoDB:

    ```sh
    sudo systemctl start mongod
    ```
5.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 27017 )'
    ```

</details>

<details>

<summary>Install ElasticSearch</summary>

APIM uses ElasticSearch as the default reporting and analytics repository. Follow the steps below to set up ElasticSearch. For further customization to the installation, refer to the [ElasticSearch installation documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo).

1.  Create a file called `/etc/yum.repos.d/elasticsearch.repo` using the following command:

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
2.  Install ElasticSearch:

    ```sh
    sudo yum install --enablerepo=elasticsearch elasticsearch -y
    sudo sed "0,/xpack.security.enabled:.*/s/xpack.security.enabled:.*/xpack.security.enabled: false/" -i /etc/elasticsearch/elasticsearch.yml
    ```
3.  Enable ElasticSearch on startup:

    <pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
    </strong><strong>$ sudo systemctl enable elasticsearch.service
    </strong></code></pre>
4.  Start ElasticSearch:

    ```sh
    sudo systemctl start elasticsearch.service
    ```
5.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 9200 )'
    ```

</details>

<details>

<summary>Install Nginx</summary>

Both APIM user interfaces (Management Console and Developer Portal) use Nginx as their web server. Follow the steps below to set up Nginx. For further customization of the installation, refer to the [Nginx Installation documentation](https://nginx.org/en/linux_packages.html#Amazon-Linux).

1.  Create a file called `/etc/yum.repos.d/nginx.repo` using the following command:

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
2.  Install Nginx:

    ```sh
    sudo amazon-linux-extras install nginx1
    ```
3.  Enable Nginx on startup:

    <pre class="language-sh"><code class="lang-sh">$ sudo systemctl daemon-reload
    <strong>$ sudo systemctl enable nginx
    </strong></code></pre>
4.  Start Nginx:

    ```sh
    sudo systemctl start nginx
    ```
5.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 80 )'
    ```

</details>

## Install the APIM full stack

<details>

<summary>Install the APIM full stack</summary>

1.  Install all Gravitee APIM components:

    ```sh
    sudo yum install graviteeio-apim-4x -y
    ```
2.  Enable Gateway and Management API on startup:

    <pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
    </strong>$ sudo systemctl enable graviteeio-apim-gateway
    $ sudo systemctl enable graviteeio-apim-rest-api
    </code></pre>
3.  Start Gateway and Management API:

    ```sh
    $ sudo systemctl start graviteeio-apim-gateway
    $ sudo systemctl start graviteeio-apim-rest-api
    ```
4.  Restart Nginx:

    ```sh
    sudo systemctl restart nginx
    ```
5.  Verify, if any of the prerequisites are missing, you will receive errors during this step (the same logs appear in `/opt/graviteeio/apim/gateway/logs/gravitee.log` and `/opt/graviteeio/apim/rest-api/logs/gravitee.log`):

    ```sh
    sudo journalctl -f
    ```
6.  Verify that there are processes listening on these ports:

    ```sh
    $ sudo ss -lntp '( sport = 8082 )'
    $ sudo ss -lntp '( sport = 8083 )'
    $ sudo ss -lntp '( sport = 8084 )'
    $ sudo ss -lntp '( sport = 8085 )'
    ```
7.  As a final verification, if the installation was successful, then the first API call returns: "No context-path matches the request URI". The final two API calls should return a JSON payload in the response.

    ```sh
    $ curl -X GET http://localhost:8082/
    $ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
    $ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
    ```

</details>

## Install the individual APIM components

<details>

<summary>Install APIM Gateway</summary>

1.  Install Gateway:

    ```sh
    sudo yum install graviteeio-apim-gateway-4x -y
    ```
2.  Enable Gateway on startup:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable graviteeio-apim-gateway
    ```
3.  Start Gateway:

    ```sh
    sudo systemctl start graviteeio-apim-gateway
    ```
4.  Verify that, if any of the prerequisites are missing, you will receive errors during this step (the same logs appear in `/opt/graviteeio/apim/gateway/logs/gravitee.log`):

    ```sh
    sudo journalctl -f
    ```
5.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 8082 )'
    ```
6.  As a final verification, if the installation was successful, then this API call should return "No context-path matches the request URI":

    ```sh
    curl -X GET http://localhost:8082/
    ```

</details>

<details>

<summary>Install Management API</summary>

1.  Install Management API:

    ```sh
    sudo yum install graviteeio-apim-rest-api-4x -y
    ```
2.  Enable Management API on startup:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable graviteeio-apim-rest-api
    ```
3.  Start REST API:

    ```sh
    sudo systemctl start graviteeio-apim-rest-api
    ```
4.  Verify that, if any of the prerequisites are missing, you will receive errors during this step (the same logs appear in `/opt/graviteeio/apim/rest-api/logs/gravitee.log`):

    ```sh
    sudo journalctl -f
    ```
5.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 8083 )'
    ```
6.  As a final verification, if the installation was successful, then both of these API requests will return a JSON document:

    ```sh
    $ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
    $ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
    ```

</details>

<details>

<summary>Install Management Console</summary>

1.  Install Management Console:

    ```sh
    sudo yum install graviteeio-apim-management-ui-4x -y
    ```
2.  Restart Nginx:

    ```sh
    sudo systemctl restart nginx
    ```
3.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 8084 )'
    ```

The Management Console package does not provide its own service. It provides:

* A JavaScript application that can be found at `/opt/graviteeio/apim/management-ui`
* An Nginx configuration that can be found at `/etc/nginx/conf.d/graviteeio-apim-management-ui.conf`

</details>

<details>

<summary>Install Developer Portal</summary>

The Developer Portal package does not provide its own service. It provides:

* A JavaScript application that can be found at `/opt/graviteeio/apim/portal-ui`
* An Nginx configuration that can be found at `/etc/nginx/conf.d/graviteeio-apim-portal-ui.conf`

1.  Install Developer Portal:

    ```sh
    sudo yum install graviteeio-apim-portal-ui-4x -y
    ```
2.  Restart Nginx:

    ```sh
    sudo systemctl restart nginx
    ```
3.  Verify that there’s a process listening on this port:

    ```sh
    sudo ss -lntp '( sport = 8085 )'
    ```

</details>
