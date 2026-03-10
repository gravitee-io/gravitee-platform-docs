# AWS CloudHSM plugin

## Overview

This page explains how to load a key pair within a domain using AWS CloudHSM.

{% hint style="info" %}
The AWS CloudHSM plugin is an EE plugin and requires a license containing the _**enterprise-secret-manager**_ pack.
{% endhint %}

{% hint style="warning" %}
AWS CloudHSM client requires a native library which is not compatible with Alpine images. To be able to use this plugin, specific Docker images have to be used for the Gateway and Management API. To download these images, add the suffix `-noble` to the regular tag, e.g.,`graviteeio/am-gateway:4.6.0-noble` or `graviteeio/am-management-api:4.6.0-noble` .
{% endhint %}

## Prerequisites

Before configuring the plugin within AM:

* Create a key pair in AWS CloudHSM service
* Get the HSM CA certificate

## Deployment

### Overview

The Cloud HSM plugin is available on [download.gravitee.io](https://download.gravitee.io/#graviteeio-ee/plugins/certificates/gravitee-am-certificate-hsm-aws/).

{% hint style="warning" %}
In addition to the plugin, you need a CloudHSM JCE Provider, which is not licensed under Apache. You must install the [JCE Provider](https://docs.aws.amazon.com/cloudhsm/latest/userguide/java-library-install_5.html) that embeds a native library specific to your processor architecture to get the correct JAR file.

For example, for a Linux host using x86\_64 processor architecture, download the `apt` or `rpm` file and install it. In the `/opt/cloudhsm/java/` directory, you will find a JAR file named `cloudhsm-jce-<version>.jar`.

This JAR file needs to be deployed in the `plugins/ext/aws-hsm-am-certificate` directory of both your Management API and Gateway instances.
{% endhint %}

### Deployment within kubernetes

The graviteeio/am Helm Chart offers a mechanism to deploy additional plugins and external dependencies. To begin, identify the version of the Gravitee plugin you wish to deploy on [download.gravitee.io](https://download.gravitee.io/#graviteeio-ee/plugins/certificates/gravitee-am-certificate-hsm-aws/) before updating your `values.yaml` file. Follow these steps:

* Copy the download link in the additionalPlugins section of the Gateway and Management API.
* Define an extra Volume and VolumeMount to contain the CloudHSM JCE jar file
* Define an initContainer to copy the CloudHSM JCE jar file into the extra volume

{% hint style="info" %}
The method by which the init container retrieves the CloudHSM plugin will depend on your dependency management strategy. You can either use a custom Docker image that includes the CloudHSM JCE installation or expose the JAR file via an HTTP server, allowing it to be downloaded using a `curl` or `wget` command.

In the example below, we are using an Ubuntu Docker image with the AWS installation, ensuring that the JAR file is already available in the init container under the path `/tmp/cloudhsm-jce.jar`.
{% endhint %}

#### Management API

```yaml
api:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/plugins/certificates/gravitee-am-certificate-hsm-aws/gravitee-am-certificate-hsm-aws-1.0.0.zip

  extraInitContainers: |
    - command:
      - sh
      - -c
      - cp /tmp/cloudhsm-jce.jar /tmp/plugins-ext/ext/aws-hsm-am-certificate/
      image: container-repository/am-init-cloudhsm:latest
      name: get-cloudhsm-jce
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
      volumeMounts:
        - mountPath: /tmp/plugins-ext/ext/aws-hsm-am-certificate
          name: gravitee-am-certificate-hsm-aws
          
  extraVolumeMounts: |
    - name: am-license
      mountPath: /opt/graviteeio-am-management-api/license
      readOnly: true
    - name: gravitee-am-certificate-hsm-aws
      mountPath: /opt/graviteeio-am-management-api/plugins-ext/ext/aws-hsm-am-certificate
  extraVolumes: |
    - name: am-license
      secret:
        secretName: am-license-v4
    - name: gravitee-am-certificate-hsm-aws
      emptyDir: {}
```

#### Gateway <a href="#create-a-new-certificate-with-am-console" id="create-a-new-certificate-with-am-console"></a>

```yaml
gateway:
  additionalPlugins:
  - https://download.gravitee.io/graviteeio-ee/plugins/certificates/gravitee-am-certificate-hsm-aws/gravitee-am-certificate-hsm-aws-1.0.0.zip

  extraInitContainers: |
    - command:
      - sh
      - -c
      - cp /tmp/cloudhsm-jce.jar /tmp/plugins-ext/ext/aws-hsm-am-certificate/
      image: container-repository/am-init-cloudhsm:latest
      name: get-cloudhsm-jce
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
      volumeMounts:
        - mountPath: /tmp/plugins-ext/ext/aws-hsm-am-certificate
          name: gravitee-am-certificate-hsm-aws
          
  extraVolumeMounts: |
    - name: am-license
      mountPath: /opt/graviteeio-am-gateway/license
      readOnly: true
    - name: gravitee-am-certificate-hsm-aws
      mountPath: /opt/graviteeio-am-gateway/plugins-ext/ext/aws-hsm-am-certificate
  extraVolumes: |
    - name: am-license
      secret:
        secretName: am-license-v4
    - name: gravitee-am-certificate-hsm-aws
      emptyDir: {}
```

## Create a new certificate with AM Console <a href="#create-a-new-certificate-with-am-console" id="create-a-new-certificate-with-am-console"></a>

1. Log in to AM Console
2. Click **Settings > Certificates**
3. Click the plus icon ![plus icon](https://documentation.gravitee.io/~gitbook/image?url=https%3A%2F%2Fdocs.gravitee.io%2Fimages%2Ficons%2Fplus-icon.png\&width=300\&dpr=4\&quality=100\&sign=d153b85e\&sv=1)
4. Choose the AWS Cloud HSM type and click **Next**
5. Give your certificate a name, then enter the AWS settings details to retrieve the key pair
6. Click **Create**
