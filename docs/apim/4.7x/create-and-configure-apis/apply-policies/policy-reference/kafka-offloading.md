# Kafka Offloading

## Overview

With the Kafka Offloading policy, you can configure the delegation of Kafka message content to storage. You have the option to activate message offloading based on the content size of the message. This policy is particularly useful for decreasing the load on Kafka and optimizing processing performance.

{% hint style="info" %}
* This policy is not included by default in the APIM product and must be installed manually.\
  You can download it from [Gravitee Policy Plugins](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/).
* This policy requires a Storage Resource plugin. Currently, the only compatible resource is Azure Storage Resource, which must be installed separately. To download the Azure Storage Resource, go to [Gravitee Resource Plugins](https://download.gravitee.io/#graviteeio-apim/plugins/resources/).
{% endhint %}

## Usage

1.  Configure the Azure Blob Storage Resource by adding the following information:

    * Provide the **Azure connection string**.
    * Specify the **container name**.

    <figure><img src="../../../.gitbook/assets/image (2) (3).png" alt=""><figcaption></figcaption></figure>
2.  In the Policy Studio, configure the policy with the following information:

    * Select the **"Event Messages"** tab for your API.
    * Add the policy **twice**: once in the **Publish** phase and once in the **Subscribe** phase.
    * Link the policy to the configured **Azure Storage Resource**.

    <figure><img src="../../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>
3. Deploy and Start the API. With the default configuration, the offloading policy completes the following actions:
   * **Offload** each published message to Azure Blob Storage.
   * **Retrieve** the message from Azure Blob Storage when subscribing.

## Compatibility matrix <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 1.0.x          | 4.8.x to latest |

## Examples

### **Example 1: I only want to offload large messages**

You can configure the policy in the Publish phase to activate only if the message content exceeds a certain size. This allows selective offloading based on message volume.

### **Example 2: I want to customize the offload key for better organization in Azure**

You can override the default offload key using the Header Value configuration. This field supports Expression Language.

For example, to use the format `<topic_name>/YYYY-MM-DD/<timestamp>_<uuid>`, you can write:

```
{ #message.topic + "/" +  new java.text.SimpleDateFormat("yyyy-MM-dd").format(new java.util.Date()) + "/" + new java.util.Date().getTime() + "_" + T(java.util.UUID).randomUUID() }
```

You could also use a Kafka header value to define the key dynamically and overwrite the default key used in Azure.

### **Example 3: I want to use different Azure containers (Location Names)**

The "Location name" option in the policy allows you to override the container name defined in the Azure Storage Resource configuration.

This field also supports Expression Language, making it possible to route messages to different containers dynamically.
