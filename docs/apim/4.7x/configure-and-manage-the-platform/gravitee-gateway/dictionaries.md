# Dictionaries

## Overview

While API publishers can create properties for their own APIs, dictionaries provide a way to manage properties independent of individual APIs, making it possible to apply them across APIs and maintain them globally with a different user profile, such as an administrator.

Dictionary properties are based on key-value pairs. You can create two types of dictionaries: manual and dynamic.

Dictionaries need to be deployed to the API Gateway before you can use them. You can see the date and time the dictionary was last deployed in the dictionary list:

<figure><img src="../../.gitbook/assets/image (139).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**How are dictionaries used?**

You can use dictionaries anywhere in APIM where [Gravitee Expression Language](../../gravitee-expression-language.md) is supported, such as when defining policies for API flows. You can access dictionary properties with the Expression Language statement `#dictionaries`.
{% endhint %}

## Create a new dictionary

To create a new dictionary, select **Settings** in the left hand nav, then select **Dictionaries.**

<figure><img src="../../.gitbook/assets/2023-06-28_10-17-24 (1).gif" alt=""><figcaption><p>Access dictionary settings</p></figcaption></figure>

Select the <img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.18.10 AM.png" alt="" data-size="line">icon. You'll be brought to the **Create a new dictionary** page. Here, you'll need to define the **Name, Description,** and **Type.** You'll have two options for **Dictionary type**:

* **Manual**: These dictionaries are made up of static properties defined manually at dictionary creation time
* **Dynamic**: These dictionaries are made up of properties that are updated continuously, based on a schedule and source URL defined at dictionary creation time

### Create a manual dictionary

To create a manual dictionary, choose **Manual** as the **Type**, then click **Create.** You'll be brought to a page where you can define the static properties for your dictionary. To create a property, select the <img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.22.56 AM.png" alt="" data-size="line">icon and give your property a name and value.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.24.08 AM.png" alt=""><figcaption><p>Add properties to your dictionary</p></figcaption></figure>

Select **Add**, and then **Save Properties** when you are done defining your key-value pairs. To start and deploy your dictionary, select **Deploy.**

### Create a dynamic dictionary

To create a dynamic dictionary, choose **Dynamic** as the **Type**. **Trigger** and **Provider** sections will then appear.

{% tabs %}
{% tab title="Define trigger settings" %}
The **Trigger** defines the schedule for which dynamic properties will be created. Define the **Interval** and the **Time Unit** (seconds, minutes, hours).

<figure><img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.28.44 AM.png" alt=""><figcaption><p>Define your trigger</p></figcaption></figure>
{% endtab %}

{% tab title="Define provider settings" %}
In the **Provider** section, specify the details of the source of the properties:

* A **Type** of **Custom (HTTP)**.
* **HTTP Service URL**: the URL and method of the API providing the properties
* Enable or disable **Use system proxy**
* The **HTTP Methods**
* The request body
* One or more HTTP headers
* The transformation to apply to the response, in JOLT format
{% endtab %}
{% endtabs %}

When you're done, click **Create**, then **Start**. Gravitee APIM will begin to retrieve the properties at the defined intervals and list them in the **Properties** section.

You can select any properties you want to delete and/or select **Deploy** to deploy your Dictionary to your Gravitee API Gateway.

<details>

<summary>Example</summary>

The following example creates a list of properties based on extracting the names and versions from the JSON at the defined URL and assigning them to the property keys and values:

<img src="https://docs.gravitee.io/images/apim/3.x/installation/configuration/configure-dict-dynamic-property-def.png" alt="" data-size="original">

When you select **Start**, the properties are added to the list according to the defined schedule:

<img src="https://docs.gravitee.io/images/apim/3.x/installation/configuration/configure-dict-dynamic-property-list.png" alt="" data-size="original">

</details>
