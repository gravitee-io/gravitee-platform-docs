---
description: Dictionaries let platform administrators manage values across API Management 4.13 APIs, beyond per-API properties, and encrypt sensitive values. Learn how they work.
---

# Dictionaries

## Overview

While API publishers can create properties for their own APIs, dictionaries provide a way to manage properties independent of individual APIs, making it possible to apply them across APIs and maintain them globally with a different user profile, such as an administrator.

Dictionary properties are based on key-value pairs. You can create two types of dictionaries: manual and dynamic.

{% hint style="info" %}
You can encrypt the value of a dictionary property that holds a sensitive value. A dictionary can hold encrypted and unencrypted properties side by side. For more information, see [Encrypt dictionary properties](dictionaries.md#encrypt-dictionary-properties).
{% endhint %}

Dictionaries need to be deployed to the API Gateway before you can use them. You can see the date and time the dictionary was last deployed in the dictionary list:

<figure><img src="../../.gitbook/assets/dictionaries-screenshot-1.png" alt="The Dictionaries page, listing a manual dictionary with one property and a stopped dynamic dictionary with none, each with their last updated and deployment times."><figcaption></figcaption></figure>

{% hint style="info" %}
**How are dictionaries used?**

You can use dictionaries anywhere in APIM where [Gravitee Expression Language](services.md) is supported, such as when defining policies for API flows.

Access a dictionary property with `{#dictionaries['<dictionary-id>']['<property-key>']}`, where `<dictionary-id>` identifies the dictionary and `<property-key>` is the name of the property. For example, if a dictionary with the ID `countries` holds a property `FR` set to `France`, then `{#dictionaries['countries']['FR']}` resolves to `France`. The identifier is the dictionary's key if one is set, and otherwise its ID.
{% endhint %}

## Reference a dictionary property in the Expression Language

You reference manual and dynamic dictionaries the same way. After a dictionary is deployed to the Gateway, read any of its properties in policy configuration, or anywhere else [Gravitee Expression Language](services.md) is supported, with:

`{#dictionaries['<dictionary-id>']['<property-key>']}`

You reference a dynamic dictionary by its ID, the same as a manual one. A dynamic dictionary refreshes its properties from an HTTP source on the schedule you define, and exposes each returned key as a property.

For example, a dynamic dictionary with the ID `partner-routing` is refreshed every few minutes from an internal service and holds these properties:

| Property key | Value |
| --- | --- |
| `acme-host` | `https://acme.api.internal` |
| `acme-tier` | `premium` |
| `maintenance` | `false` |

Reference its properties anywhere Expression Language is supported:

* **Read a value.** `{#dictionaries['partner-routing']['acme-host']}` resolves to `https://acme.api.internal`. Use it to set a backend target or build a URL from a centrally managed value.
* **Set a header.** In a header transformation policy, set the `X-Backend-Tier` header to `{#dictionaries['partner-routing']['acme-tier']}`.
* **Drive a flow condition.** Run a flow only during maintenance with the condition `{#dictionaries['partner-routing']['maintenance'] == 'true'}`.
* **Look up a value with a request attribute.** Build the property key from the request. For a dictionary `tenant-config` keyed by tenant ID, `{#dictionaries['tenant-config'][#request.headers['X-Tenant-Id'][0]]}` reads the value stored under the incoming tenant ID.

The outer key is the dictionary's ID, or its key if one is set. The inner key is the property name. Each expression resolves to the current value held for that property, so a dynamic dictionary serves the latest values it has retrieved from the source.

Deploy the dictionary to the Gateway before you reference it.

## Create a new dictionary

To create a new dictionary, select **Settings** in the left hand nav, then select **Dictionaries.**

<figure><img src="../../.gitbook/assets/2023-06-28_10-17-24 (1).gif" alt="An animation that navigates from the home board to the environment&#x27;s Dictionaries page, which lists manual and dynamic dictionaries with their property counts and update times."><figcaption><p>Access dictionary settings</p></figcaption></figure>

Select the <img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.18.10 AM.png" alt="A round dark blue button with a white plus sign, used to add a new item." data-size="line">icon. You'll be brought to the **Create a new dictionary** page. Here, you'll need to define the **Name, Description,** and **Type.** You'll have two options for **Dictionary type**:

* **Manual**: These dictionaries are made up of static properties defined manually at dictionary creation time
* **Dynamic**: These dictionaries are made up of properties that are updated continuously, based on a schedule and source URL defined at dictionary creation time

### Create a manual dictionary

To create a manual dictionary, choose **Manual** as the **Type**, then click **Create.** You'll be brought to a page where you can define the static properties for your dictionary. To create a property, select the <img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.22.56 AM.png" alt="A round dark blue button with a white plus sign, used to add a new item." data-size="line">icon and give your property a name and value.

<figure><img src="../../.gitbook/assets/dictionaries-screenshot-2.png" alt="The New property dialog open over a dictionary&#x27;s settings, with empty name and value fields above a properties table holding one key and value pair."><figcaption><p>Add properties to your dictionary</p></figcaption></figure>

Select **Add**, and then **Save Properties** when you are done defining your key-value pairs. To start and deploy your dictionary, select **Deploy.**

### Create a dynamic dictionary

To create a dynamic dictionary, choose **Dynamic** as the **Type**. **Trigger** and **Provider** sections will then appear.

{% tabs %}
{% tab title="Define trigger settings" %}
The **Trigger** defines the schedule for which dynamic properties will be created. Define the **Interval** and the **Time Unit** (seconds, minutes, hours).

<figure><img src="../../.gitbook/assets/dictionaries-screenshot-trigger-1.png" alt="The Trigger section of a dynamic dictionary, with an interval of 24 and the time unit dropdown open on Seconds, Minutes, and Hours."><figcaption><p>Define your trigger (for how often to retrieve properties from the 3rd-party service)</p></figcaption></figure>
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

Example Screenshot:

<figure><img src="../../.gitbook/assets/dictionaries-screenshot-provider-1.png" alt="The Provider section of a dynamic dictionary, with a custom HTTP provider, a local management API URL, the GET method, an Authorization bearer header, a content type header, and a JOLT transformation below."><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

When you're done, click **Create**, then **Start**. Gravitee APIM will begin to retrieve the properties at the defined intervals and list them in the **Properties** section.

You can select any properties you want to delete and/or select **Deploy** to deploy your Dictionary to your Gravitee API Gateway.

<details>

<summary>Example</summary>

The following example creates a list of properties based on extracting the names and versions from the JSON at the defined URL and assigning them to the property keys and values:

<img src="../../.gitbook/assets/configure-dict-dynamic-property-def.png" alt="The Provider section of a dynamic dictionary, with a custom HTTP provider, a service URL, the GET method, and a JOLT transformation specification." data-size="original">

When you select **Start**, the properties are added to the list according to the defined schedule:

<img src="../../.gitbook/assets/configure-dict-dynamic-property-list.png" alt="The Properties list of a dictionary, showing the key and value pairs fetched from the provider across several pages." data-size="original">

</details>

## Encrypt dictionary properties

When you encrypt a dictionary property, APIM stores its value encrypted. The APIM Console and the Management API don't show the value again. They show `••••••••••••` in its place.

The Gateway decrypts the value when the dictionary is deployed. An expression such as `{#dictionaries['<dictionary-id>']['<property-key>']}` resolves to the original value, so you reference an encrypted property the same way as an unencrypted one.

The **Characteristic** column of the **Properties** table shows the state of each property:

* **Encrypted on save**: the property is marked for encryption. APIM encrypts its value when you save the properties.
* **Encrypted**: the value is stored encrypted.
* **Unencrypted**: the value is stored as plain text.

{% hint style="warning" %}
Dictionary properties are encrypted with the same secret as encrypted API properties, `api.properties.encryption.secret`. Set the same custom secret on the Management API and the Gateway. The Gateway can fail to decrypt a value, for example when its secret differs from the one the Management API used. In that case, the Gateway logs an error and the expression resolves to the encrypted value. For more information, see [Property Encryption](../../prepare-a-production-environment/production-best-practices/general-recommendations/property-encryption.md).
{% endhint %}

### Add an encrypted property to a manual dictionary

1. Open **Settings**.
2. Click **Dictionaries**.
3. Click the manual dictionary that you want to update.
4. Click the <img src="../../.gitbook/assets/Screen Shot 2023-06-28 at 10.22.56 AM.png" alt="A round dark blue button with a white plus sign, used to add a new item." data-size="line"> icon.
5. In the **New property** dialog, enter a **Name** and a **Value**.
6. Turn on **Encrypt**.
7. Click **Add**. The property shows the **Encrypted on save** badge.
8. Click **Save properties**.
9. Click **Deploy**.

### Encrypt an existing property

You can encrypt an existing property in a manual dictionary or a dynamic dictionary.

1. Open **Settings**.
2. Click **Dictionaries**.
3. Click the dictionary that you want to update.
4. In the **Properties** table, click the lock icon of the property. The property shows the **Encrypted on save** badge. To cancel before you save, click the clear icon of the property.
5. Click **Save properties**.
6. For a manual dictionary, click **Deploy**.

### Replace the value of an encrypted property

You can't edit the value of an encrypted property in place. In a manual dictionary, replace it with a new value:

1. Open **Settings**.
2. Click **Dictionaries**.
3. Click the manual dictionary that you want to update.
4. In the **Properties** table, click the replace icon of the property.
5. In the **Edit property** dialog, enter the new **Value**.
6. Click **Save**.
7. Click **Save properties**.
8. Click **Deploy**.

The new value is encrypted when you save the properties.

### Encrypt the fetched values of a dynamic dictionary

A dynamic dictionary can encrypt every value that it fetches from its provider.

1. Open **Settings**.
2. Click **Dictionaries**.
3. Click the dynamic dictionary that you want to update.
4. In the **Encryption** section, select **Encrypt fetched values**.
5. Click **Update**.

Existing plain text values are encrypted the next time they're fetched. Values that are already encrypted aren't changed. If you clear **Encrypt fetched values**, APIM doesn't decrypt the values that are already stored.

### Encrypted property behavior

* **Encryption can't be undone.** APIM doesn't decrypt a stored value. To store a manual dictionary property as plain text again, delete the property, click **Save properties**, and then add the property again without **Encrypt**.
* **Encrypted properties of a dynamic dictionary stay encrypted.** When a refresh fetches a new value for an encrypted property, APIM encrypts the new value. This applies whether **Encrypt fetched values** is selected or cleared.
* **Audit entries don't contain encrypted values.** When a change involves an encrypted property, the audit entry doesn't record the property's value.

### Declare encrypted properties with the Automation API

In a manual dictionary manifest for the Automation API, declare encrypted properties under `manual.encryptedProperties`, and unencrypted properties under `manual.properties`. For example:

```json
{
  "hrid": "mixed-dict",
  "name": "Mixed Dictionary",
  "description": "A dictionary with one plain and one encrypted property",
  "type": "MANUAL",
  "deployed": false,
  "manual": {
    "properties": {
      "url": "https://backend"
    },
    "encryptedProperties": {
      "apiKey": {
        "value": "my secret API key"
      }
    }
  }
}
```

* Each entry of `encryptedProperties` takes the plain text `value` to encrypt on save.
* The Automation API never returns the values of encrypted properties. A client that compares a `GET` response with its manifest doesn't see a difference on those values.
* A key can't appear in both `properties` and `encryptedProperties`.
* Moving a key from `encryptedProperties` to `properties` doesn't decrypt it. The property stays encrypted, and its new value is encrypted on save.
* For a dynamic dictionary, set `dynamic.encryption.encryptOnFetch` to `true` to encrypt every fetched value. The default is `false`.

## Verification

To verify that a dictionary property is encrypted, follow these steps:

1. Open **Settings**.
2. Click **Dictionaries**.
3. Click the dictionary.
4. In the **Properties** table, find the property. Its value shows `••••••••••••` and its **Characteristic** column shows the **Encrypted** badge.
