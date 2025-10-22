# Configure the New Portal

{% hint style="warning" %}
This feature is in tech preview.&#x20;
{% endhint %}

## Overview

Gravitee allows you to run either the classic or new Developer Portal, depending on your preference. You can configure Gravitee to use the new Developer Portal by enabling a setting. Gravitee launches the classic Developer Portal by default, but you can set the default to the new Developer Portal using environment variables.&#x20;

## Enable the new Developer Portal

To configure Gravitee to use the new Developer Portal:

1. Log in to your APIM Console.
2.  From the home page, click **Settings**.\


    <figure><img src="../../.gitbook/assets/image (268).png" alt=""><figcaption></figcaption></figure>
3.  In the **Portal** section of the settings menu, click **Settings**.\


    <figure><img src="../../.gitbook/assets/image (269).png" alt=""><figcaption></figcaption></figure>
4.  Navigate to the **New Developer Portal** section, and then turn on the **Enable the New Developer Portal** toggle.\


    <figure><img src="../../.gitbook/assets/image (270).png" alt=""><figcaption><p>New Developer Portal section</p></figcaption></figure>

To verify that the new theme is enabled, click the **Open Website** button. The new Developer Portal should launch.&#x20;

## Use the new Developer Portal by default

You also have the option to enable the new Developer Portal by default. This is done by setting environment variables.

To configure Gravitee to default to the new Developer Portal, complete the following steps for your installation type:

{% tabs %}
{% tab title="Docker" %}
In your `docker.yml` file, you must set the following environment variables:

1. Navigate to `management_ui`, and then set the following environment variable: `DEFAULT_PORTAL=next`.&#x20;
2. Navigate to `portal_ui`, and then set the following environment variable: `DEFAULT_PORTAL=next`.
{% endtab %}

{% tab title="Kubernetes" %}
Kubernetes&#x20;

* In your `values.yml` file, set the following environment variable, navigate to `portal`, and then set the following environment variable: `defaultPortal: "next"`.
{% endtab %}

{% tab title="Cloud" %}
* In the your `values.yaml`, set the following, add the following environment variable: `defaultPortal: "next"`.
{% endtab %}
{% endtabs %}
