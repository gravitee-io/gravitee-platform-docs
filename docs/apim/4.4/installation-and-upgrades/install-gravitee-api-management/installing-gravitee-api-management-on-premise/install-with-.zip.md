# Installing Gravitee API Management With .ZIP

## Before you begin&#x20;

Your environment must be the following requirements:

* You must install at least Java17.&#x20;
* You must install MongoDB and Elasticsearch.
* You must download the binaries of the Gravitee 4.x.x version that you plan to use. For more information about downloading the binaries, see[ Gravitee's download page](https://www.gravitee.io/downloads).

{% hint style="info" %}
If you previously downloaded the binaries, you do not need to download the binaries again.
{% endhint %}

## Installing the components of the API Management

To use Gravitee’s API Management (APIM), you must install the following components:

{% tabs %}
{% tab title="APIM Gateway" %}
1\. Extract the `.zip` archive using the following commands:

```sh
$ unzip gravitee-standalone-distribution-4.x.0.zip
$ cp -r graviteeio-full-4.x.0/graviteeio-apim-gateway-4.x.0 [DESTINATION_FOLDER]/
```

* Replace \[DESTINATION\_FOLDER] with the folder where you want to store the archive.



2. From the command line, run the APIM gateway using the following commands:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-gateway-4.x.0
$ ./bin/gravitee
```

* Replace \[DESTINATION\_FOLDER] with the folder location from step 1.

If you installed the APIM gateway correctly, you see the logs.&#x20;

3. To ensure that the APIM Gateway is running correctly, send a GET request using the following command:

```sh
curl -X GET http://localhost:8082/
```

If you installed the APIM Gateway correctly, the request returns the following message: `No context-path matches the request URI.`

4.  To run the APIM gateway as a daemon, complete the following sub-steps:

    a.  On the command line, specify \`-d\`, and then record the process ID in a file using the following command:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

You can find log messages in the `$GRAVITEE_HOME/logs/` directory.

&#x20;       b. To stop the APIM Gateway, kill the process that is recorded in the `pid` file using the following command:&#x20;

```sh
kill `cat /var/run/gio.pid`
```

### API Management Gateway directory structure

The `.zip` and `.tar.gz` packages are entirely self-contained. By default, all files and directories are contained within `$GRAVITEE_HOME`. You created this directory created when extracting the archive.

| Location | Description                                                 |
| -------- | ----------------------------------------------------------- |
| bin      | Binary scripts including `gravitee` to start a node         |
| config   | Configuration files including `gravitee.yml`                |
| lib      | Libraries (Gravitee.io libraries and third party libraries) |
| logs     | Log files                                                   |
| plugins  | Plugin files                                                |
{% endtab %}

{% tab title="Management API" %}
1. Extract the `.zip` archive using the following commands:

```sh
$ unzip gravitee-standalone-distribution-4.x.0.zip
$ cp -r graviteeio-full-4.x.0/graviteeio-apim-rest-api-4.x.0 [DESTINATION_FOLDER]/
```

* Replace \[DESTINATION\_FOLDER] with the folder where you want to store the archive.



2. From the command line, run the APIM API using the following command:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-rest-api-4.x.0
$ ./bin/gravitee
```

* Replace \[DESTINATION\_FOLDER] with the folder location from step 1.

{% hint style="info" %}
By default, both Management API nodes run at the same time. To configure APIM to run one node, see [General configuration](https://documentation.gravitee.io/apim/getting-started/configuration/apim-management-api/general-configuration).
{% endhint %}

3. To ensure that the Management API node is running correctly, send an API request using the following command:

<pre class="language-sh"><code class="lang-sh"><strong>curl -X GET http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis
</strong></code></pre>

4. To ensure that the Developer Portal API node is running correctly, send an API request using the following command:

```sh
curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

You will receive a response similar to the following example:

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

5.  To run the APIM gateway as a daemon, complete the following sub-steps:

    a.  On the command line, specify `-d`, and then record the process ID in a file using the following command:

```sh
./bin/gravitee -d -p=/var/run/gio.pid
```

6. To stop the Management API, kill the process that is recorded in the `pid` file using the following command:

```sh
kill `cat /var/run/gio.pid`
```

### Management API directory structure

The `.zip` and `.tar.gz` packages are entirely self-contained. By default, all files and directories are contained within `$GRAVITEE_HOME`. You created this directory created when extracting the archive.

| Location  | Description                                                 |
| --------- | ----------------------------------------------------------- |
| bin       | Binary scripts including `gravitee` to start a node         |
| config    | Configuration files including `gravitee.yml`                |
| lib       | Libraries (Gravitee.io libraries and third party libraries) |
| logs      | Log file location                                           |
| plugins   | Plugin file location                                        |
| data      | Search engine metadata                                      |
| templates | API templates                                               |
{% endtab %}

{% tab title="Management Console" %}
### Prerequisites

You must install the Management API. To install the Management API, switch to the Management API tab.

### Installing the Management Console

1. Extract the `.zip` archive using the following commands:

```sh
$ unzip gravitee-standalone-distribution-4.x.0.zip
$ cp -r graviteeio-full-4.x.0/graviteeio-apim-console-ui-4.x.0 [DESTINATION_FOLDER]/
```

* Replace \[DESTINATION\_FOLDER] with the folder where you want to store the archive.



2. You can deploy the Management Console or you can run the Management Console by completing the following sub steps:

&#x20;        a. To deploy the Management Console, use any HTTP server. For example, Apache or        Nginx.

&#x20;        b. Run the Management Console with Python using the following command:

```sh
$ cd [DESTINATION_FOLDER]/graviteeio-apim-console-ui-4.x.0
$ python3 -m http.server
```

* Replace \[DESTINATION\_FOLDER] with the folder location from step 1.

&#x20;        c. Run the Management Console with Node.js with the following request:

```bash
$ npm install http-server -g
$ cd [DESTINATION_FOLDER]/graviteeio-apim-console-ui-4.x.0
$ http-server
```

* Replace \[DESTINATION\_FOLDER] with the folder location from step 1.
{% endtab %}

{% tab title="Developer Portal" %}
### Prerequisites

You must install the Management API. To install the Management API, switch to the  Management API tab.

### Installing the Developer Portal

1. Extract the `.zip` archive using the following commands:

```sh
$ unzip gravitee-standalone-distribution-4.x.0.zip
$ cp -r graviteeio-full-4.1.0/graviteeio-apim-portal-ui-4.x.0 [DESTINATION_FOLDER]/
```

* Replace \[DESTINATION\_FOLDER] with the folder where you want to store the archive.



2. You can deploy or run the Developer Portal using the following steps:

&#x20;       a.  Deploy the Developer Portal using any HTTP server. For example, Apache or Nginx.

&#x20;       b.  Run the Developer Portal with Node.js using the following command:

```sh
$ npm install angular-http-server -g
$ cd [DESTINATION_FOLDER]/graviteeio-apim-portal-ui-4.x.0
$ angular-http-server
```

* Replace \[DESTINATION\_FOLDER] with the folder location from step 1.
{% endtab %}
{% endtabs %}
