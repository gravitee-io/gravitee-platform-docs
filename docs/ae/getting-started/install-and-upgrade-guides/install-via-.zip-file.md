---
description: This article walks through how to install Gravitee Alert Engine via .ZIP file
---

# Install via .ZIP file

## Introduction and prerequisites

Your environment must meet the requirements listed below before you install Alert Engine (AE).

#### JDK

AE requires a Java version from 8 to the most recent Java 11 version. You can check your Java version as follows:

```
java -version
echo $JAVA_HOME
```

You can download the latest OpenJDK from the [OpenJDK Download Site](https://jdk.java.net/archive/).

### Download and extract the `.zip` archive

1.  Download the binaries from [here](https://download.gravitee.io/graviteeio-ae/components/gravitee-ae-engine-2.1.2.zip) or using the command line:

    {% code overflow="wrap" %}
    ```
    $ curl -L https://download.gravitee.io/graviteeio-ae/components/gravitee-ae-engine-2.1.2.zip -o gravitee-ae-standalone-2.1.2.zip
    ```
    {% endcode %}
2.  Extract the archive and place it in the required location (`$GRAVITEE_HOME`).

    ```
    $ unzip gravitee-ae-standalone-2.1.2.zip
    ```

### Check the installation

#### Run AE from the command line

By default, AE Engine runs in the foreground, prints its logs to the standard output (stdout), and can be stopped by pressing **Ctrl-C**.

Run AE from the command line as follows:

```
$ cd gravitee-ae-standalone-2.1.2
$ ./bin/gravitee
```

Once AE is running, you should see this log:

```
...
11:23:06.835 [main] [] INFO  i.g.ae.standalone.node.AlertEngineNode - Gravitee.io - Alert Engine - Engine id[92c03b26-5f21-4460-803b-265f211460be] version[2.1.2] pid[4528] build[${env.BUILD_NUMBER}#${env.GIT_COMMIT}] jvm[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/25.121-b13] started in 1860 ms.
...
```

#### Check AE is running

You can test that your AE node is running by sending an HTTP request to port `8072` on `localhost`:

```
$ curl -X GET http://localhost:8072/
```

You should receive an empty 401 response.

### Run AE as a daemon

To run AE as a daemon, specify `-d` at the command line and record the process ID in a file using option `-p`:

```
$ ./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

To shut down AE Engine, kill the process ID recorded in the `pid` file:

```
$ kill `cat /var/run/gio.pid`
```

### AE directory structure

The `$GRAVITEE_HOME` directory looks like this:

| Folder  | Description                                                 |
| ------- | ----------------------------------------------------------- |
| bin     | Startup/shutdown scripts                                    |
| config  | Configuration files                                         |
| lib     | Libraries (Gravitee.io libraries and third party libraries) |
| license | License for Enterprise Edition                              |
| logs    | Log files                                                   |
| plugins | Plugin files                                                |

\
