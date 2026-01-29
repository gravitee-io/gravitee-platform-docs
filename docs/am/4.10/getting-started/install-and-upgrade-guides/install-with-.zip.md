# Install with .ZIP

## Prerequisites

Your environment must meet the requirements listed below before you install AM distribution.

### JDK

AM Gateway & AM Management are supporting Java version 17. You can check your Java version as follows:

<pre class="language-sh"><code class="lang-sh"><strong>$ java -version
</strong>$ echo $JAVA_HOME
</code></pre>

{% hint style="info" %}
You can download the latest OpenJDK from the [OpenJDK download site](https://jdk.java.net/archive/) or by using the package management system of your operating system.
{% endhint %}

### Database

Default AM distribution requires **MongoDB** to store data. You can download MongoDB from the [MongoDB download site](https://www.mongodb.org/downloads#production).

{% hint style="info" %}
SQL database such as PostgreSQL, MySQL, MariaDB, Microsoft SQL Server can also be used to run your AM distribution.
{% endhint %}

### HTTP Server

AM Management Console is a client-side Angular application that can be deployed on any HTTP server, such as [Apache](https://httpd.apache.org/) or [Nginx](http://nginx.org/).

## Full installation

A full .zip distribution with all the components can be downloaded by clicking [here](https://download.gravitee.io/graviteeio-am/distributions/graviteeio-am-full-4.0.0.zip).

## Install AM Gateway

### Download and extract the `.zip` archive

1. Download the binaries [here](https://download.gravitee.io/graviteeio-am/components/gravitee-am-gateway/gravitee-am-gateway-standalone-4.0.0.zip) or from the [Gravitee download site](https://gravitee.io/downloads/access-management).

{% code overflow="wrap" %}
```sh
curl -L https://download.gravitee.io/graviteeio-am/components/gravitee-am-gateway/gravitee-am-gateway-standalone-4.0.0.zip -o gravitee-am-gateway-standalone-4.0.0.zip
```
{% endcode %}

2. Unpack the archive and place the folders in the required location.

```sh
unzip gravitee-am-gateway-standalone-4.0.0.zip
```

### Check the installation

Run AM Gateway from the command line as follows:

```sh
$ cd gravitee-am-gateway-standalone-4.0.0
$ ./bin/gravitee
```

By default, AM Gateway runs in the foreground, prints its logs to the standard output (stdout), and can be stopped by pressing **Ctrl-C**.

Once AM Gateway is running, you will see this log:

{% code overflow="wrap" %}
```
...
11:23:06.835 [main] [] INFO  i.g.am.gateway.node.GatewayNode - Gravitee - Access Management - Gateway id[92c03b26-5f21-4460-803b-265f211460be] version[4.0.0] pid[4528] build[${env.BUILD_NUMBER}#${env.GIT_COMMIT}] jvm[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/25.121-b13] started in 1860 ms.
...
```
{% endcode %}

### Check AM Gateway is running

You can test that your AM Gateway node is running by sending an HTTP request to port `8092` on `localhost`:

```sh
curl -X GET http://localhost:8092/
```

You should receive an empty 404 response (nho security domain matches the request URI).

### Run AM Gateway as a daemon

To run AM Gateway as a daemon, specify `-d` on the command line and record the process ID in a file using the `-p` option:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down AM Gateway, kill the process ID recorded in the `pid` file:

```sh
kill `cat /var/run/gio.pid`
```

### AM Gateway directory structure

The following files and folders are in the `$GRAVITEE_HOME` directory, created when extracting the archive:

| Folder  | Description                                   |
| ------- | --------------------------------------------- |
| bin     | Startup/shutdown scripts                      |
| config  | Configuration files                           |
| lib     | Libraries (both AM and third party libraries) |
| logs    | Gateway log files                             |
| plugins | Gateway plugins                               |

## Install AM Management API

AM API is required to run AM Console UI. You must install AM API first before you can use AM Console.

### Download and extract the `.zip` archive

1. Download the binaries [here](https://download.gravitee.io/graviteeio-am/components/gravitee-am-management-api/gravitee-am-management-api-standalone-4.0.0.zip) or from the [Gravitee download site](https://gravitee.io/downloads/access-management).

{% code overflow="wrap" %}
```sh
curl -L https://download.gravitee.io/graviteeio-am/components/gravitee-am-management-api/gravitee-am-management-api-standalone-4.0.0.zip -o gravitee-am-management-api-standalone-4.0.0.zip
```
{% endcode %}

2. Unpack the archive and place the folders in the required location.

```sh
unzip gravitee-am-management-api-standalone-4.0.0.zip
```

### Check the installation

Run AM API from the command line as follows:

```sh
$ cd gravitee-am-management-api-standalone-4.0.0
$ ./bin/gravitee
```

By default, AM API runs in the foreground, prints its logs to the standard output (stdout), and can be stopped by pressing **Ctrl-C**.

Once AM API is running, you will see this log:

{% code overflow="wrap" %}
```
...
16:21:01.995 [gravitee] [] INFO  o.e.jetty.server.AbstractConnector - Started ServerConnector@1e1232cf{HTTP/1.1,[http/1.1]}{0.0.0.0:8093}
16:21:01.996 [gravitee] [] INFO  org.eclipse.jetty.server.Server - Started @19214ms
16:21:01.996 [gravitee] [] INFO  i.g.am.management.api.jetty.JettyHttpServer - HTTP Server is now started and listening on port 8093
...
```
{% endcode %}

### Check that AM API is running

You can test that your AM API node is running by sending an HTTP request to port `8093` on `localhost`:

```sh
curl -X GET http://localhost:8093/management/domains/
```

### Run AM API as a daemon

To run AM API as a daemon, specify `-d` on the command line and record the process ID in a file using the `-p` option:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down AM API, kill the process ID recorded in the `pid` file:

```sh
kill `cat /var/run/gio.pid`
```

### AM API directory structure

The following files and folders are in the `$GRAVITEE_HOME` directory, created when extracting the archive:

| Folder  | Description                                   |
| ------- | --------------------------------------------- |
| bin     | Startup/shutdown scripts                      |
| config  | Configuration files                           |
| lib     | Libraries (both AM and third party libraries) |
| logs    | AM API log files                              |
| plugins | AM API plugins                                |

## Install AM Console

### Download and extract the .zip archive

1. Download the binaries [here](https://download.gravitee.io/graviteeio-am/components/gravitee-am-webui/gravitee-am-webui-4.0.0.zip) or from the [Gravitee download site](https://gravitee.io/downloads/access-management).

{% code overflow="wrap" %}
```sh
curl -L https://download.gravitee.io/graviteeio-am/components/gravitee-am-webui/gravitee-am-webui-4.0.0.zip -o gravitee-am-webui-4.0.0.zip
```
{% endcode %}

2. Unpack the archive and place the folders in the required location.

```sh
unzip gravitee-am-webui-4.0.0.zip
```

### Deploy or run AM Console

AM Console is a client-side Angular application and can be deployed on any HTTP server, such as [Apache](https://httpd.apache.org/) or [Nginx](http://nginx.org/).

{% hint style="info" %}
AM Console uses HTML5 mode and requires server-side rewrites to make it work, such as in the Apache and Nginx examples below.
{% endhint %}

#### Apache

```
<VirtualHost *:80>
    ServerName my-app

    DocumentRoot /path/to/app

    <Directory /path/to/app>
        RewriteEngine on

        # Don't rewrite files or directories
        RewriteCond %{REQUEST_FILENAME} -f [OR]
        RewriteCond %{REQUEST_FILENAME} -d
        RewriteRule ^.*$ - [L]

        # Rewrite everything else to index.html to allow html5 state links
        RewriteRule ^ index.html [L]
    </Directory>
</VirtualHost>
```

#### Nginx

```
server {
    server_name my-app;

    index index.html;

    root /path/to/app;

    location / {
        try_files $uri $uri/ /index.html;
    }
}she
```
