---
description: >-
  You control the installation of the prerequisites that you need to run API
  Management (APIM). Also, you control the installation of the individual
  components of the APIM stack.
---

# Installing Gravitee APIM on an Amazon instance with Manual Install

## Before you begin

{% hint style="warning" %}
Gravitee supports only the Amazon Linux 2 image.
{% endhint %}

* Provision an Amazon instance, and then start the Amazon instance. Your Amazon instance must meet the following minimum requirements:
  * The instance type must be at least t2.medium.
  * The root volume size must be at least 40GB.
  * The security group must allow SSH connection to connect and install the Gravitee components.
  * The security group must be open to the following ports:
    * Port 8082
    * Port 8083
    * Port 8084
    * Port 8085

### Installing the prerequisites for Gravitee API Management

To install the prerequisites for Gravitee API Management (APIM), complete the following steps:

<details>

<summary>Creating a Gravitee YUM repository</summary>

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
2.  (Optional) Enable GPG signature handling by installing the following packages using the following command:

    ```sh
    sudo yum install pygpgme yum-utils -y
    ```
3.  Refresh the local cache using the following command:

    {% code overflow="wrap" %}
    ```sh
    sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
    ```
    {% endcode %}

</details>

<details>

<summary>Installing  Java 17</summary>

1.  Enable the repository that contains Java:

    ```sh
    sudo amazon-linux-extras enable java-openjdk17
    ```
2.  Install Java using the following the command:

    ```sh
    sudo yum install java-17-openjdk -y
    ```
3.  Verify that you installed Java correctly using the following command:

    ```sh
    java -version
    ```

</details>

<details>

<summary>Install MongoDB</summary>

Gravitee API Management uses MongoDB as its default repository to store global configurations. To install MongoDB, complete the following steps:

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
2.  Install MongoDB using the following command:

    ```sh
    sudo yum install mongodb-org -y
    ```
3.  Enable MongoDB using the following commands:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable mongod
    ```
4.  Start MongoDB using the following command:

    ```sh
    sudo systemctl start mongod
    ```
5.  To verify that you installed MongoDB correctly, verify that there is a process listening on port 27017 using the following command:

    ```sh
    sudo ss -lntp '( sport = 27017 )'
    ```

</details>

<details>

<summary>Install ElasticSearch</summary>

Gravitee API Management uses ElasticSearch as the default reporting and analytics repository. To install ElasticSearch, complete the following steps:

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
2.  Install ElasticSearch using the following command:

    ```sh
    sudo yum install --enablerepo=elasticsearch elasticsearch -y
    sudo sed "0,/xpack.security.enabled:.*/s/xpack.security.enabled:.*/xpack.security.enabled: false/" -i /etc/elasticsearch/elasticsearch.yml
    ```
3.  Enable ElasticSearch using the following command:

    <pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
    </strong><strong>$ sudo systemctl enable elasticsearch.service
    </strong></code></pre>
4.  Start ElasticSearch using the following command:

    ```sh
    sudo systemctl start elasticsearch.service
    ```
5.  To verify that you installed ElasticSearch correctly, ensure that there is a process listening on port 9200 using following command:

    ```sh
    sudo ss -lntp '( sport = 9200 )'
    ```

</details>

<details>

<summary>Install Nginx</summary>

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
2.  Install Nginx using the following command:

    ```sh
    sudo amazon-linux-extras install nginx1
    ```
3.  Enable Nginx by using the following commands:

    <pre class="language-sh"><code class="lang-sh">$ sudo systemctl daemon-reload
    <strong>$ sudo systemctl enable nginx
    </strong></code></pre>
4.  Start Nginx using the following command:

    ```sh
    sudo systemctl start nginx
    ```
5.  Verify that there is process listening on port 80 using the following command:

    ```sh
    sudo ss -lntp '( sport = 80 )'
    ```

</details>

## Installing Gravitee API Management

To install Gravitee's API Management (APIM), you can use two installation methods:&#x20;

* [Installing the full API Management stack. ](manual-install.md#installing-the-full-api-management-stack)You install all of the API Management components.
* [Installing the individual API Management components](manual-install.md#installing-the-individual-apim-components). You install only the API Management components that you want for your environment.

## Installing the full API Management stack

<details>

<summary>Install the full API Management (APIM) stack</summary>

1.  Install Gravitee’s APIM components using the following command:

    ```sh
    sudo yum install graviteeio-apim-4x -y
    ```
2.  Enable the Gateway and the Management API using the following commands:

    <pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
    </strong>$ sudo systemctl enable graviteeio-apim-gateway
    $ sudo systemctl enable graviteeio-apim-rest-api
    </code></pre>
3.  Start the Gateway and the Management API using the following command:

    ```sh
    $ sudo systemctl start graviteeio-apim-gateway
    $ sudo systemctl start graviteeio-apim-rest-api
    ```
4.  Restart Nginx using the following command:

    ```sh
    sudo systemctl restart nginx
    ```

Verification

To verify that you installed the full APIM stack, complete the following steps:

1. Verify that you installed the prerequisites correctly using the following command:

```sh
sudo journalctl -f
```

2. Verify that there are processes listening on the correct ports using the following commands:

```sh
$ sudo ss -lntp '( sport = 8082 )'
$ sudo ss -lntp '( sport = 8083 )'
$ sudo ss -lntp '( sport = 8084 )'
$ sudo ss -lntp '( sport = 8085 )'
```

3. Send three API calls to ensure that you installed the APIM stack using the following sub-steps:

&#x20;       a.  Send a GET request using the following command:

```bash
$ curl -X GET http://localhost:8082/
```

If you installed the APIM stack correctly, the API call returns the following message: ‘No context-path matches the request URI’.       &#x20;

&#x20;       b. Send two GET requests using the following commands:

```bash
$ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
$ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

If you installed the APIM with the default configurations, both API calls return a JSON payload response.

</details>

## Installing the individual APIM components

Depending on your environment's configuration, you can install only the APIM components that you want for your environment. Here are the components that you can install:

<details>

<summary>Installing the API Management Gateway</summary>

1.  Install the APIM Gateway using the following command:

    ```sh
    sudo yum install graviteeio-apim-gateway-4x -y
    ```
2.  Enable the Gateway using the following commands:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable graviteeio-apim-gateway
    ```
3.  Start the APIM Gateway using the following command:

    ```sh
    sudo systemctl start graviteeio-apim-gateway
    ```

Verification&#x20;

Verify that you installed the APIM Gateway correctly by completing the following steps:

1.  Verify that you installed the prerequisites correctly using the following command:

    ```sh
    sudo journalctl -f
    ```

<!---->

2. Ensure that there is a process listening on the 8082 port using the following command:

```sh
sudo ss -lntp '( sport = 8082 )'
```

3. Send a GET request to the APIM Gateway by using the following command:

```sh
curl -X GET http://localhost:8082/
```

</details>

<details>

<summary>Installing the Management API</summary>

1.  Install the Management API using the following command:

    ```sh
    sudo yum install graviteeio-apim-rest-api-4x -y
    ```
2.  Enable the Management API using the following commands:

    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable graviteeio-apim-rest-api
    ```
3.  Start the REST API using the following command:

    ```sh
    sudo systemctl start graviteeio-apim-rest-api
    ```

Verification

To verify that you installed the APIM gateway correctly, complete the following steps:

1.  Verify that you installed the prerequisites using the following command:

    ```sh
    sudo journalctl -f
    ```
2.  Verify that there is a process listening on the 8083 port:

    ```sh
    sudo ss -lntp '( sport = 8083 )'
    ```
3. To ensure that you installed the APIM COnsole and the APIM Portal correctly, send two GET requests using the following commands:

```sh
$ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
$ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

</details>

<details>

<summary>Installing the Management Console</summary>

**Note:** The Management Console provides the following configurations:&#x20;

* A JavaScript application. You can find the JavaScript application at the following file location: `/opt/graviteeio/apim/management-ui`.&#x20;
* A Nginx configuration. You can find the Nginx configuration at the following file location: `/etc/nginx/conf.d/graviteeio-apim-management-ui.conf`

1.  Install the Management Console using the following command:

    ```sh
    sudo yum install graviteeio-apim-management-ui-4x -y
    ```
2.  Restart Niginx using the following command:

    ```sh
    sudo systemctl restart nginx
    ```

Verification

1.  Verify that there is a process listening on port 8084 using the following command:

    ```sh
    sudo ss -lntp '( sport = 8084 )'
    ```

</details>

<details>

<summary>Install Developer Portal</summary>

**Note:** The Developer Portal provides the following configurations:

* A JavaScript application. You can find the JavaScript application at the following file location: `/opt/graviteeio/apim/management-ui`.
* A Nginx configuration. You can find the Nginx configuration at the following file location: `/etc/nginx/conf.d/graviteeio-apim-management-ui.conf`.

1.  Install the Developer Portal by using the following the command:

    ```sh
    sudo yum install graviteeio-apim-portal-ui-4x -y
    ```
2.  Restart Nginx by using the following command:

    ```sh
    sudo systemctl restart nginx
    ```

Verification

* To verify that you installed the Developer Portal correctly, ensure that there is a process listening on the 8085 port using the following command:

```sh
sudo ss -lntp '( sport = 8085 )'
```

</details>
