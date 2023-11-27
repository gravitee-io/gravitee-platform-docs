---
description: 30 minute advanced tutorial
---

# Advanced: Kafka

## Overview

This tutorial showcases Gravitee's event-native API management capabilities that can manage, secure, and mediate between both asynchronous and synchronous protocols.

At this point, you should already be familiar with the basics of Gateway APIs and policies. This intermediate tutorial is focused on Gravitee's event-native capabilities, security, plans, applications, and subscriptions.

For those who are unfamiliar, event-native means that Gravitee is built on an event-driven architecture implemented with reactive programming to natively manage asynchronous, event-driven APIs. Gravitee fully supports synchronous (request/response) APIs management alongside asynchronous APIs in a centralized control plane, and can even mediate between synchronous and asynchronous protocols.

This tutorial shows how to test these capabilities with the trial app. Unlike the beginner tutorial, this tutorial goes further in-depth and requires additional configuration of Gravitee API Management (APIM).&#x20;

### Trial app access

Before beginning, you must ensure you have access to the trial application. The trial app can be accessed in the APIM trial's sidebar with the **Open trial app** button:

{% hint style="warning" %}
Some ad blockers disable the **Open trial app** button. Please whitelist Gravitee products to avoid this.
{% endhint %}

<figure><img src="../../../.gitbook/assets/Screenshot 2023-08-31 at 6.28.06 PM.png" alt=""><figcaption><p>Open the trial app from the top nav</p></figcaption></figure>

The trial application will not function properly if you do not access it from directly inside the Gravitee API Management enterprise trial.

## Trial app architecture

Each tutorial takes advantage of different aspects of the trial app. This section provides an overview of the relevant trial app functionality and architecture to help you get the most out of this tutorial. The next step of the tutorial will show you how to configure Gravitee API management (APIM) and how it augments the trial app architecture detailed here.&#x20;

{% hint style="info" %}
&#x20;For the curious, you can explore the application code in the [open-source, public repository](https://github.com/gravitee-io-labs/trial-sample-app).
{% endhint %}

This tutorial is built around the todo list page. The todo list page functions as a simple task manager built on the MERN stack. A MERN application is a type of web application that uses four main technologies:
