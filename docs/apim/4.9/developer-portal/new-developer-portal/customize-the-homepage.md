---
description: An overview about customize the homepage.
---

# Customize the homepage

## Overview

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

In the New Developer Portal, you can customize the homepage of your Developer Portal with standard Markdown and Gravitee Markdown (GMD). Gravitee Markdown is standard Markdown enriched with custom Gravitee components. For more information about Gravitee Markdown, see [gravitee-markdown-components.md](gravitee-markdown-components.md "mention").

You can edit the homepage with a Markdown editor. A preview appears next to the Markdown editor.

<figure><img src="../../.gitbook/assets/C8F30709-7053-491F-B74E-ED0FD990C109_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Customize the homepage

To customize the homepage, complete the following steps:

1. [#access-the-homepage-editor](customize-the-homepage.md#access-the-homepage-editor "mention")
2. [#edit-the-homepage](customize-the-homepage.md#edit-the-homepage "mention")

### Access the Homepage editor

1. Sign in to your APIM Console.
2.  From the **Dashboard**, click **Settings**.

    <figure><img src="../../.gitbook/assets/76D66FB4-4D8E-467D-AADE-543FC7813158_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Settings** menu, navigate to the **Portal** section, and then click **Settings**.

    <figure><img src="../../.gitbook/assets/601A31D5-D722-4B6B-AC99-72E0D9D5E765_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Navigate to the **New Developer Portal** section of the page, and then click **Open Settings**. The settings open in a new tab.

    <figure><img src="../../.gitbook/assets/8F20A23D-0B5B-4863-B454-6AA244B820AC_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  In the New Developer Portal settings menu, click **Homepage**.

    <figure><img src="../../.gitbook/assets/9C598C3F-9360-464F-95A7-562E2081F60F_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

### Edit the homepage

By default, the Developer Portal homepage has the following content :

```markdown
<gmd-grid>
    <gmd-md class="homepage-title">
        # Welcome to the Developer Portal
        Access all APIs, documentation, and tools to build your next integration.
    </gmd-md>
    <gmd-cell style="text-align: center; margin: auto;">
        <gmd-button link="/catalog">Explore all APIs</gmd-button>
        <gmd-button link="/guides" appearance="outlined" style="--gmd-button-outlined-label-text-weight: 700; --gmd-button-outlined-label-text-color: black;"
        >Get started</gmd-button>
    </gmd-cell>
    <img class="homepage-cover-photo" src="assets/homepage/desk.png" title="Homepage picture"/>
</gmd-grid>

### Your toolkit for building

<gmd-grid columns="3">
    <gmd-md>
        ![book](./assets/homepage/book.svg "Book icon")
        #### API catalog
        Browse and test all available APIs in one place.
    </gmd-md>
    <gmd-md>
        ![laptop](./assets/homepage/laptop.svg "Laptop icon")
        #### Interactive docs
        Explore clear, structured documentation with code samples.
    </gmd-md>
    <gmd-md>
        ![vector](./assets/homepage/vector.svg "Vector icon")
        #### Usage analytics
        Track API usage, error rates, and performance metrics.
    </gmd-md>
    <gmd-md>
        ![group](./assets/homepage/group.svg "Group icon")
        #### API catalog
        Browse and test all available APIs in one place.
    </gmd-md>
    <gmd-md>
        ![support](./assets/homepage/support.svg "Support icon")
        #### Interactive docs
        Explore clear, structured documentation with code samples.
    </gmd-md>
    <gmd-md>
        ![support](./assets/homepage/service.svg "Service icon")
        #### Usage analytics
        Track API usage, error rates, and performance metrics.
    </gmd-md>
</gmd-grid>

### Get started in minutes

<gmd-grid columns="3">
    <gmd-card backgroundColor="none">
        <gmd-card-title>Your first API call</gmd-card-title>
        <gmd-md>Learn how to make a basic request and receive a response.Learn how to make a basic request and receive a response.</gmd-md>
        <div class="flex-container">
            <gmd-button link="/guides" appearance="outlined" class="get-started-card__button"
            >Read <img src="assets/homepage/arrow-right.svg" alt="arrow right icon" title="Arrow right icon"/></gmd-button>
        </div>
    </gmd-card>
    <gmd-card backgroundColor="none">
        <gmd-card-title>Authentication walkthrough</gmd-card-title>
            <gmd-md>A step-by-step guide to generating and managing API keys.</gmd-md>
            <div class="flex-container">
                <gmd-button link="/guides" appearance="outlined" class="get-started-card__button"
                >Read <img src="assets/homepage/arrow-right.svg" alt="arrow right icon" title="Arrow right icon"/></gmd-button>
            </div>
        </gmd-card>
    <gmd-card backgroundColor="none">
        <gmd-card-title>Integrating SDK into your project</gmd-card-title>
        <gmd-md>Use our official library to simplify your code.</gmd-md>
        <div class="flex-container">
            <gmd-button link="/guides" appearance="outlined" class="get-started-card__button"
            >Read <img src="assets/homepage/arrow-right.svg" alt="arrow right icon" title="Arrow right icon"/></gmd-button>
        </div>
    </gmd-card>
</gmd-grid>
<style>
  .homepage-title {
    display: flex;
    flex-direction: column;
    max-width: 100%;
    text-align: center;
    margin: auto;
  }

  .homepage-cover-photo {
    display: flex;
    max-width: 100%;
    margin: 80px auto;
  }
  
  .get-started-card__button {
    --gmd-button-outlined-label-text-weight: 700;
    --gmd-button-outlined-label-text-color: black;
    margin-top: auto;
    padding-top: 12px;
  }

  .flex-container {
    display: flex;
    flex-direction: column;
    height: 100%
  }
</style>
```

To edit the homepage, complete the following steps:

1.  In the Markdown editor, enter your Markdown or GMD to customize the homepage.For more information about the GMD components that you can enter to customize the homepage, see [#gravitee-markdown-components](customize-the-homepage.md#gravitee-markdown-components "mention").

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>To view the GMD components in the Markdown editor, press option and the space bar at the same time, and then type the component the name of the component that you want to use. For example, Grid.</p></div>

    <figure><img src="../../.gitbook/assets/FF5F9BA4-70DA-4E07-B90A-7E321A6260B6_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **Save**.

    <figure><img src="../../.gitbook/assets/406DBE86-4767-4B3F-B7B4-D048AC25B9F8_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

### Verification

*   To verify that you updated your Developer Portal, click **Open Website**. Your Developer Portal opens in a new tab.

    <figure><img src="../../.gitbook/assets/4FABA433-1720-44BD-BB04-71931137CA69_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Unpublish the homepage

1.  To unpublish the homepage, click **Unpublish**.

    <figure><img src="../../.gitbook/assets/A9BD4556-F502-4F49-8795-1AADC7EFCC33_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **Unpublish page?** pop-up window, click **Unpublish.**

    <figure><img src="../../.gitbook/assets/A3F78550-AA9D-4D97-9EF9-5E173B78A6FC (1).jpeg" alt=""><figcaption></figcaption></figure>

### Verification

If the page unpublished successfully, you receive the following pop-up message:

<figure><img src="../../.gitbook/assets/C8E492D0-4A52-4531-8F4B-A60727E453FA_4_5005_c (1).jpeg" alt=""><figcaption></figcaption></figure>
