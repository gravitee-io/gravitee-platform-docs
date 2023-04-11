# Install With .ZIP

Installing Gravitee from .zip files is a straightforward process that can be completed in a few simple steps. This method is particularly useful for those with limited internet connectivity, those needing customization or control over versioning, or those working in non-standard server environments.

In this documentation, we will guide you through the process of installing Gravitee from the provided .zip files. We will cover the prerequisites for installation, how to download and extract the files, and the necessary configuration steps. By following these instructions, you will be able to set up a functional instance of Gravitee on your server and begin taking advantage of its robust API management capabilities.

## Install APIM Gateway

### Prerequisites

Your environment must meet the requirements listed below before you install APIM gateway.

#### JDK

APIM Gateway requires at least Java 11. You can check your Java version as follows:

```sh
$ java -version
$ echo $JAVA_HOME
```

{% hint style="info" %}
You can download the latest OpenJDK from the [OpenJDK Download Site](https://jdk.java.net/archive/).
{% endhint %}

#### MongoDB and Elasticsearch

The default APIM Gateway distribution requires [MongoDB](https://docs.gravitee.io/apim/3.x/apim\_installguide\_repositories\_mongodb.html) to poll environment configuration and [Elasticsearch](https://docs.gravitee.io/apim/3.x/apim\_installguide\_repositories\_elasticsearch.html) for reporting and analytics. See the vendor documentation for supported versions.

{% hint style="info" %}
You can download MongoDB from [MongoDB Download Site](https://www.mongodb.org/downloads#production) and Elasticsearch from [Elastic Download Site](https://www.elastic.co/downloads/elasticsearch)
{% endhint %}

### Download and extract the `.zip` archive

{% hint style="info" %}
Note that the archive includes the binaries for all the APIM components, so if you previously downloaded it to install another component, you do not need to download it again.
{% endhint %}

1. Download the binaries [here](https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full-3.20.0.zip) or from the [Gravitee downloads page](https://gravitee.io/downloads/api-management).

{% code overflow="wrap" %}
```sh
curl -L https://download.gravitee.io/graviteeio-apim/distributions/graviteeio-full-3.20.0.zip -o gravitee-standalone-distribution-3.20.0.zip
```
{% endcode %}

2. Extract the desired directory from the archive and place it in the required location. For example, if you wanted the `graviteeio-apim-gateway-3.20.0` directory, then use the following commands:

```sh
$ unzip gravitee-standalone-distribution-3.20.0.zip
$ cp -r graviteeio-full-3.20.0/graviteeio-apim-gateway-3.20.0 [DESTINATION_FOLDER]/
```

### Check the installation

#### Run APIM Gateway from the command line

By default, APIM Gateway runs in the foreground, prints its logs to standard output (stdout), and can be stopped by pressing **Ctrl-C**.

Run APIM Gateway from the command line as follows:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-gateway-3.20.0
$ ./bin/gravitee
```

Once APIM Gateway is running, you will see this log:

```
...
11:01:53.162 [gravitee] [] INFO  i.g.g.standalone.node.GatewayNode - Gravitee.io - Gateway id[2e05c0fa-8e48-4ddc-85c0-fa8e48bddc11] version[3.20.0] pid[24930] build[175] jvm[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/25.121-b13] started in 15837 ms.
...
```

#### Check APIM Gateway is running

You can test that APIM Gateway is running by sending an HTTP request to port `8082` on `localhost`:

```
$ curl -X GET http://localhost:8082/
```

You will receive a response something like this:

```
No context-path matches the request URI.
```

### Run APIM Gateway as a daemon

To run APIM Gateway as a daemon, specify `-d` on the command line and record the process ID in a file using option `-p`:

```
$ ./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down APIM Gateway, kill the process ID recorded in the `pid` file:

```
$ kill `cat /var/run/gio.pid`
```

### APIM Gateway directory structure

The `.zip` (and `.tar.gz`) package is entirely self-contained. All files and directories are, by default, contained within `$GRAVITEE_HOME`, the directory created when extracting the archive.

| Location | Description                                                 |
| -------- | ----------------------------------------------------------- |
| bin      | Binary scripts including `gravitee` to start a node         |
| config   | Configuration files including `gravitee.yml`                |
| lib      | Libraries (Gravitee.io libraries and third party libraries) |
| logs     | Log files                                                   |
| plugins  | Plugin files                                                |

\


## Install Management API



## Install Management UI



## Install Developer Portal
