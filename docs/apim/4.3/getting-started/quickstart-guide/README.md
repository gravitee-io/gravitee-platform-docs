---
description: >-
  Gravitee 101 - Learn all the fundamentals to managing your APIs and
  message/event brokers in 30 minutes or less
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Quickstart Guide

Welcome to the Gravitee API Management (APIM) Quickstart Guide! This guide uses a hands-on approach to quickly introduce you to the core concepts of APIM.

These guides will switch between explaining APIM concepts and directing you to complete actions inside of your APIM instance. To make sure you don't miss any steps, all required actions are listed with an in-product image and instructions that follow the format below:

> * [x] Select **UI element**
> * [x] Enter your name under **UI element**

## Prerequisites

Before getting started, you'll need:

1. Basic familiarity with web APIs and/or message brokers
2. Gravitee APIM 4.0 or later up and running

{% hint style="info" %}
If you are new to both web APIs and message brokers, we recommend taking a look at the [Gravitee Essentials guide](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-core-concepts) before continuing.
{% endhint %}

To manage your own installations, check out our [APIM install guides](../install-and-upgrade-guides/) for install options to run APIM locally or in your own cloud infrastructure. If you don't have a strong preference, [Quick Install with Docker Compose](../install-and-upgrade-guides/installing-a-self-hosted-gravitee-api-management-platform/install-on-docker/quick-install-with-docker-compose.md) is the fastest self-managed installation for most users.

{% hint style="warning" %}
An enterprise license is required for all message broker functionality.
{% endhint %}

Regardless of how APIM is deployed, the next step is to access the APIM Console. The APIM Console is the easiest way to manage all of your APIs and the configuration for your Gravitee Gateway.

## Access APIM Console: Self-managed installation

How you access the APIM Console in a self-managed installation depends on your installation method and covered in that method's installation guide. The example provided below is for a Docker installation, but is similar to any self-managed installation.

For the default local Docker installation, navigate to `http://localhost:8084` in your browser, and you will be greeted with the following screen:

<figure><img src="broken-reference" alt=""><figcaption><p>APIM Console login screen</p></figcaption></figure>

> * [x] Navigate to `http://localhost:8084` in your browser

For a new installation, the default login is `admin` for both **Username** and **Password**. Logging in will take you to your APIM Console homescreen, which should look similar to this:

<figure><img src="broken-reference" alt=""><figcaption><p>APIM Console Dashboard</p></figcaption></figure>

> * [x] Log in to the APIM Console using `admin` for both **Username** and **Password**

{% hint style="success" %}
With access to the APIM Console, you'll be ready to dive straight into the Quickstart Guide. You should complete the 101 guides in order, as they build upon each other.
{% endhint %}

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td></td><td>Gateway APIs 101</td><td></td><td><a href="gateway-apis-101-traditional-and-message-proxies/">gateway-apis-101-traditional-and-message-proxies</a></td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>
