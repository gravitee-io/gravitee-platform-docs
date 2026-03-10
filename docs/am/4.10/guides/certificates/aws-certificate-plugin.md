# AWS Certificate plugin

## Overview

This page explain how to load certificate within a Domain using AWS Secret Manager.

{% hint style="info" %}
The AWS Certificate plugin is an EE plugin and requires a license containing the _**enterprise-secret-manager**_ pack. To make it works, the **AWS Secret Provider** plugin is also needed.

Those plugins are provided by the default bundler but they can be downloaded from [download.gravitee.io](https://download.gravitee.io/#graviteeio-ee/plugins/)
{% endhint %}

## Prerequisites

Before configuring the plugin within AM, you have to create a secret in AWS Secret Manager service.

This secret will have to contains the following entries:

* **storepass**: the passphrase for the certificate store
* **keypass**: the passphrase for the private key
* **alias**: the alias name of the certificate
* **certificate**: the certificate using PCKS12 store format

## Create a new certificate with AM Console <a href="#create-a-new-certificate-with-am-console" id="create-a-new-certificate-with-am-console"></a>

1. Log in to AM Console.
2. Click **Settings > Certificates**.
3. Click the plus icon ![plus icon](https://documentation.gravitee.io/~gitbook/image?url=https%3A%2F%2Fdocs.gravitee.io%2Fimages%2Ficons%2Fplus-icon.png\&width=300\&dpr=4\&quality=100\&sign=d153b85e\&sv=1).
4. Choose the AWS certificate type and click **Next**.
5. Give your certificate a name, then enter the details of AWS settings to retrieve the secret.
   1. secret name
   2. region
   3. provide authentication credentials
6. Click **Create**.
