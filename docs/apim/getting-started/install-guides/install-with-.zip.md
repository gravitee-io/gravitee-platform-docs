# Install With .ZIP

Installing Gravitee API Management (APIM) from .zip files is a straightforward process that can be completed in a few simple steps. This method is particularly useful for those with limited internet connectivity, those needing customization or control over versioning, or those working in non-standard server environments.

In this documentation, we will guide you through the process of installing Gravitee from the provided `.zip` files. We will cover the prerequisites for installation, how to download and extract the files, and the necessary configuration steps. By following these instructions, you will be able to set up a functional instance of APIM on your server and begin taking advantage of its robust API management capabilities.

## Prerequisites

Your environment must meet the requirements listed below before you install any of the APIM components.

### JDK

APIM Gateway requires at least Java 17. You can check your Java version as follows:

```sh
$ java -version
$ echo $JAVA_HOME
```

{% hint style="info" %}
You can download the latest OpenJDK from the [OpenJDK Download Site](https://jdk.java.net/archive/).
{% endhint %}

### MongoDB and Elasticsearch

The default APIM Gateway distribution requires [MongoDB](https://docs.gravitee.io/apim/3.x/apim\_installguide\_repositories\_mongodb.html) to poll environment configuration and [Elasticsearch](https://docs.gravitee.io/apim/3.x/apim\_installguide\_repositories\_elasticsearch.html) for reporting and analytics. See the vendor documentation for supported versions.

{% hint style="info" %}
You can download MongoDB from [MongoDB Download Site](https://www.mongodb.org/downloads#production) and Elasticsearch from [Elastic Download Site](https://www.elastic.co/downloads/elasticsearch)
{% endhint %}

## Download the binaries

{% hint style="info" %}
Note that the archive includes the binaries for all the APIM components, so if you previously downloaded it to install another component, you do not need to download it again.
{% endhint %}

Download the binaries [here](https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full-3.20.0.zip) or from the [Gravitee downloads page](https://gravitee.io/downloads/api-management).

{% code overflow="wrap" %}
```sh
curl -L https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full-3.20.0.zip -o gravitee-standalone-distribution-3.20.0.zip
```
{% endcode %}

## Install APIM gateway

### Extract the `.zip` archive

Extract the desired directory from the archive and place it in your `DESTINATION_FOLDER`. For example, if you wanted the `graviteeio-apim-gateway-3.20.0` directory, then use the following commands:

```sh
$ unzip gravitee-standalone-distribution-3.20.0.zip
$ cp -r graviteeio-full-3.20.0/graviteeio-apim-gateway-3.20.0 [DESTINATION_FOLDER]/
```

### Run APIM gateway from the command line

By default, APIM gateway runs in the foreground, prints its logs to standard output (stdout), and can be stopped by pressing **Ctrl-C**.

Run APIM Gateway from the command line as follows:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-gateway-3.20.0
$ ./bin/gravitee
```

Once APIM gateway is running, you will see this log:

```sh
...
11:01:53.162 [gravitee] [] INFO  i.g.g.standalone.node.GatewayNode - Gravitee - Gateway id[2e05c0fa-8e48-4ddc-85c0-fa8e48bddc11] version[3.20.0] pid[24930] build[175] jvm[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/25.121-b13] started in 15837 ms.
...
```

### Check APIM gateway is running

You can test that APIM gateway is running by sending an HTTP request to port `8082` on `localhost`:

```sh
curl -X GET http://localhost:8082/
```

You will receive a response similar to the following:

```sh
No context-path matches the request URI.
```

### Run APIM gateway as a daemon

To run APIM gateway as a daemon, specify `-d` on the command line and record the process ID in a file using option `-p`:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down APIM gateway, kill the process ID recorded in the `pid` file:

```sh
kill `cat /var/run/gio.pid`
```

### APIM gateway directory structure

The `.zip` (and `.tar.gz`) package is entirely self-contained. All files and directories are, by default, contained within `$GRAVITEE_HOME`, the directory created when extracting the archive.

| Location | Description                                                 |
| -------- | ----------------------------------------------------------- |
| bin      | Binary scripts including `gravitee` to start a node         |
| config   | Configuration files including `gravitee.yml`                |
| lib      | Libraries (Gravitee.io libraries and third party libraries) |
| logs     | Log files                                                   |
| plugins  | Plugin files                                                |

## Install Management API

The management API includes nodes for both of the UI components (management UI and developer portal). You must install the relevant management API node before you can use the corresponding UI component.

This section describes how to install management API and verify the nodes are running.

### Extract the `.zip` archive

Extract the desired directory from the archive and place it in your `DESTINATION_FOLDER`. For example, if you wanted the `graviteeio-apim-rest-api-3.20.0` directory, then use the following commands:

```sh
$ unzip gravitee-standalone-distribution-3.20.0.zip
$ cp -r graviteeio-full-3.20.0/graviteeio-apim-rest-api-3.20.0 [DESTINATION_FOLDER]/
```

### Run management API from the command line

You start APIM API from the command line as follows:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-rest-api-3.20.0
$ ./bin/gravitee
```

By default, APIM API runs in the foreground, prints its logs to standard output (stdout), and can be stopped by pressing **Ctrl-C**.

{% hint style="info" %}
Both the management API nodes run by default. You can configure APIM to run only one or the other, as described in the [management API configuration](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html) section.
{% endhint %}

Once the management API is running, you will see a log such as this one:

```sh
...
11:01:53.162 [main] INFO  i.g.r.a.s.node.GraviteeApisNode - Gravitee - Rest APIs id[2e05c0fa-8e48-4ddc-85c0-fa8e48bddc11] version[3.20.0] pid[24930] build[175] jvm[AdoptOpenJDK/OpenJDK 64-Bit Server VM/12.0.1+12] started in 8042 ms.
...
```

### Check management API is running

You can test that your management API node is running by sending an HTTP request to port `8083` on `localhost`:

```sh
curl -X GET http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis
```

You will receive a response similar to the following:

```sh
[]
```

### Check developer portal API is running

You can test that your developer portal API node is running by sending an HTTP request to port `8083` on `localhost`:

```sh
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

You will receive a response similar to the following:

```sh
{
  "data" : [ ],
  "metadata" : {
    "data" : {
      "total" : 0
    }
  }
}
```

### Run management API as a daemon

To run the management API as a daemon, specify `-d` on the command line and record the process ID in a file using option `-p`:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down the management API, kill the process ID recorded in the `pid` file:

```sh
kill `cat /var/run/gio.pid`
```

### Management API directory structure

The `.zip` and (`.tar.gz`) package is entirely self-contained. All files and directories are, by default, contained within `$GRAVITEE_HOME`, the directory created when extracting the archive.

| Location  | Description                                                 |
| --------- | ----------------------------------------------------------- |
| bin       | Binary scripts including `gravitee` to start a node         |
| config    | Configuration files including `gravitee.yml`                |
| lib       | Libraries (Gravitee.io libraries and third party libraries) |
| logs      | Log file location                                           |
| plugins   | Plugin file location                                        |
| data      | Search engine metadata                                      |
| templates | API templates                                               |

## Install Management UI

### Prerequisites

Before you begin, ensure the management API is installed and running.

### Extract the `.zip` archive

Extract the desired directory from the archive and place it in your `DESTINATION_FOLDER`. For example, if you wanted the `graviteeio-apim-console-ui-3.20.0` directory, then use the following commands:

```sh
$ unzip gravitee-standalone-distribution-3.20.0.zip
$ cp -r graviteeio-full-3.20.0/graviteeio-apim-console-ui-3.20.0 [DESTINATION_FOLDER]/
```

### Deploy or run the management UI

#### Deploy

The management UI is a client-side-only AngularJS application and can be deployed on any HTTP server, such as [Apache](https://httpd.apache.org/) or [Nginx](http://nginx.org/).

#### Run with Python

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-console-ui-3.20.0
$ python3 -m http.server
```

#### Run with Node.js

```sh
$ npm install http-server -g
$ cd [DESTINATION_FOLDER]/graviteeio-apim-console-ui-3.20.0
$ http-server
```

## Install Developer Portal

### Prerequisites

Before you begin, ensure the management API is installed and running.

### Extract the `.zip` archive

Extract the desired directory from the archive and place it in your `DESTINATION_FOLDER`. For example, if you wanted the `graviteeio-apim-portal-ui-3.20.0` directory, then use the following commands:

```sh
$ unzip gravitee-standalone-distribution-3.20.0.zip
$ cp -r graviteeio-full-3.20.0/graviteeio-apim-console-ui-3.20.0 [DESTINATION_FOLDER]/
```

### Deploy or run the developer portal

The developer portal is a client-side-only Angular application and can be deployed on any HTTP server like [Apache](https://httpd.apache.org/) or [Nginx](http://nginx.org/).

#### Run with Node.js

```sh
$ npm install angular-http-server -g
$ cd [DESTINATION_FOLDER]/graviteeio-apim-portal-ui-3.20.0
$ angular-http-server
```

