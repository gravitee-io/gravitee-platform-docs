---
description: >-
  This article walks through how to create APIs using the Gravitee v2API
  defintion
---

# V2 API definition creation wizard

{% @arcade/embed flowId="kApsIRtoWrfIFRzd7DQj" url="https://app.arcade.software/share/kApsIRtoWrfIFRzd7DQj" fullWidth="true" %}

## Introduction

In Gravitee, your API definition is a JSON representation of your Gateway API. Gravitee currently supports two different API definitions: v2 and v4. API definition v2 supports HTTP-based APIs and will only allow you to use the legacy version of the Policy Studio. This article walks through how to create APIs in Gravitee using the v2 API creation wizard.

## Access the API creation wizard

To create a v2 API in Gravitee, select the **APIs** tab in the left-hand nav. Then, select **+ Add API** in the top-right corner of the UI.&#x20;

Choose Create a v2 API from scratch. You'll then be brought into the API creation wizard for v2 APIs.

## Step 1: General

The first step is to define your API's general details. Give your API a:

* Name
* Version
* Description
* Context path: this is just the path where the API is exposed

Optionally, you use the Advanced mode by selecting the Advanced mode hyperlink in the top right corner of the General page. This will enable you to define whether or not to use a group as the primary owner of the API, define that primary owner group, and then also optionally define a list of groups that will have access to, but not own, that API.&#x20;

## Step 2: Gateway

Here, all you'll need to do is&#x20;
