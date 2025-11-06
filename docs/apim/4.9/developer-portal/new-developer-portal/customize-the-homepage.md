# Customize the homepage

## Overview

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

In the New Developer Portal, you can customize the homepage of your Developer Portal with standard Markdown and Gravitee Markdown (GMD). Gravitee Markdown is standard Markdown enriched with custom Gravitee components.

You can edit the homepage with a Markdown editor. A preview appears next to the Markdown editor.

<figure><img src="../../../4.8/.gitbook/assets/C8F30709-7053-491F-B74E-ED0FD990C109_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Prerequisites

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Customize the homepage

To customize the homepage, complete the following steps:

1. [#access-the-homepage-editor](customize-the-homepage.md#access-the-homepage-editor "mention")
2. [#edit-the-homepage](customize-the-homepage.md#edit-the-homepage "mention")

### Access the Homepage editor

1. Sign in to your APIM Console.
2.  From the **Dashboard**, click **Settings**.\\

    <figure><img src="../../../4.8/.gitbook/assets/76D66FB4-4D8E-467D-AADE-543FC7813158_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Settings** menu, navigate to the **Portal** section, and then click **Settings**.\\

    <figure><img src="../../../4.8/.gitbook/assets/601A31D5-D722-4B6B-AC99-72E0D9D5E765_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Navigate to the **New Developer Portal** section of the page, and then click **Open Settings**. The settings open in a new tab.\\

    <figure><img src="../../../4.8/.gitbook/assets/8F20A23D-0B5B-4863-B454-6AA244B820AC_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  In the New Developer Portal settings menu, click **Homepage**.\\

    <figure><img src="../../../4.8/.gitbook/assets/9C598C3F-9360-464F-95A7-562E2081F60F_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

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

1.  In the Markdown editor, enter your Markdown or GMD to customize the homepage.For more information about the GMD components that you can enter to customize the homepage, see [#gravitee-markdown-components](customize-the-homepage.md#gravitee-markdown-components "mention").\\

    \{% hint style="info" %\} To view the GMD components in the Markdown editor, press option and the space bar at the same time, and then type the component the name of the component that you want to use. For example, Grid. \{% endhint %\}

    <figure><img src="../../../4.8/.gitbook/assets/FF5F9BA4-70DA-4E07-B90A-7E321A6260B6_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **Save**. \\

    <figure><img src="../../../4.8/.gitbook/assets/406DBE86-4767-4B3F-B7B4-D048AC25B9F8_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Verification

*   To verify that you updated your Developer Portal, click **Open Website**. Your Developer Portal opens in a new tab.\\

    <figure><img src="../../../4.8/.gitbook/assets/4FABA433-1720-44BD-BB04-71931137CA69_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Unpublish the homepage

1.  To unpublish the homepage, click **Unpublish**.\\

    <figure><img src="../../../4.8/.gitbook/assets/A9BD4556-F502-4F49-8795-1AADC7EFCC33_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **Unpublish page?** pop-up window, click **Unpublish.**\\

    <figure><img src="../../../4.8/.gitbook/assets/A3F78550-AA9D-4D97-9EF9-5E173B78A6FC (1).jpeg" alt=""><figcaption></figcaption></figure>

### Verification

If the page unpublished successfully, you receive the following pop-up message:

<figure><img src="../../../4.8/.gitbook/assets/C8E492D0-4A52-4531-8F4B-A60727E453FA_4_5005_c (1).jpeg" alt=""><figcaption></figcaption></figure>

## Gravitee Markdown components

Here are available Gravitee Markdown components:

* [#block](customize-the-homepage.md#block "mention")
* [#button](customize-the-homepage.md#button "mention")
* [#card](customize-the-homepage.md#card "mention")
* [#grid](customize-the-homepage.md#grid "mention")

### Block

This block component is a wrapper for Markdown content in Gravitee's Markdown system. With this component, you can add standard Markdown content within Gravitee Markdown components.

Here is an example of the block component with Markdown:

```markdown
<gmd-md>
  # Hello World
  
  This is a **markdown** block with:
  - Lists
  - **Bold text**
  - [Links](https://gravitee.io)
</gmd-md>
```

### Button

The button component has the following three appearances that all support internal and external links:

{% tabs %}
{% tab title="Filled" %}
This style has a solid background with white text. By default, the color is the primary color of the Developer Portal theme. For more information about the Developer Portal theme, see [broken-reference](broken-reference/ "mention").

**Examples**

Filled button Markdown:

```markdown
<gmd-button appearance="filled">Save Changes</gmd-button>
```

Filled button with an internal link:

{% hint style="info" %}
* Internal links must start with a backslash ( / ).
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="filled" link="/dashboard">Dashboard</gmd-button>
```

Filled button with an external link:

{% hint style="info" %}
* External links must be the full URL. For example, [https://example.com"](https://example.com").
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="filled" link="https://gravitee.io" target="_blank">Visit Gravitee</gmd-button>
```
{% endtab %}

{% tab title="Outlined" %}
This style is a transparent background with a colored border and text. By default, the button color is blue (#1976d2), the border color is light gray (#CDD7E1), the button label text is the primary color of the Developer portal theme. For more information about the Developer Portal theme, see [broken-reference](broken-reference/ "mention").

**Examples**

Outlined button:

```markdown
<gmd-button appearance="outlined">Cancel</gmd-button>
```

Outlined button with an internal link:

{% hint style="info" %}
* Internal links must start with a backslash ( / ).
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="outlined" link="/settings">Settings</gmd-button>
```

Outlined button with an external link:

{% hint style="info" %}
* External links must be the full URL. For example, [https://example.com"](https://example.com").
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="outlined" link="https://docs.gravitee.io" target="_blank">Documentation</gmd-button>
```
{% endtab %}

{% tab title="Text" %}
This style is a transparent background with colored text only. By default, the color is primary color of the Developer Portal theme. For information about the Developer Portal theme, see [broken-reference](broken-reference/ "mention").

**Examples**

Text button:

```markdown
<gmd-button appearance="text">Learn More</gmd-button>
```

Text button with an internal link:

{% hint style="info" %}
* Internal links must start with a backslash ( / ).
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button> appearance="text" link="/profile">Profile</gmd-button>
```

Text button with an external link:

{% hint style="info" %}
* External links must be the full URL. For example, [https://example.com"](https://example.com").
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button> appearance="text" link="https://github.com/gravitee-io" target="_blank">GitHub</gmd-button>
```
{% endtab %}
{% endtabs %}

### Card

The card component displays structured content. It uses a token-based theming system with CSS custom properties and input properties. The card consists of the following elements:

* Container. The main card wrapper.
* Title. The main title of the card.
* Subtitle. The subtitle of the card.
* Content. The content contains the markdown content blocks.

The card component provides the following benefits:

* Flexible content structure
* Customizable styling
* Input-based overrides
* Responsive design
* Markdown support with Gravitee Markdown components

You can customize the following elements of the card:

* Background color
* Text color

Here are examples of Markdown that you can use for your card

{% tabs %}
{% tab title="Basic card" %}
```markdown
<gmd-card>
  <gmd-md>
    This is a simple card with markdown content.
  </gmd-md>
</gmd-card>
```
{% endtab %}

{% tab title="Card with title" %}
```markdown
<gmd-card>
  <gmd-card-title>Card Title</gmd-card-title>
  <gmd-md>
    This card has a title and content.
  </gmd-md>
</gmd-card>
```
{% endtab %}

{% tab title="Card with title and subtitle" %}
```markdown
<gmd-card>
  <gmd-card-title>Card Title</gmd-card-title>
  <gmd-card-subtitle>Card Subtitle</gmd-card-subtitle>
  <gmd-md>
    This card has both a title and subtitle.
  </gmd-md>
</gmd-card>
```
{% endtab %}

{% tab title="Card with custom colors" %}
```markdown
<gmd-card [backgroundColor]="'#ffffff'" [textColor]="'#333333'">
  <gmd-card-title>Custom Styled Card</gmd-card-title>
  <gmd-card-subtitle>Version: 2.0</gmd-card-subtitle>
  <gmd-md>
    This card has custom background and text colors.
  </gmd-md>
</gmd-card>
```
{% endtab %}
{% endtabs %}

Here are some use case examples:

{% tabs %}
{% tab title="String values" %}
```markdown
<gmd-card backgroundColor="'#ff0000'" textColor="'#ffffff'">
  <gmd-card-title>Red Card</gmd-card-title>
  <gmd-md>This card has a red background with white text.</gmd-md>
</gmd-card>]
```
{% endtab %}

{% tab title="CSS color functions" %}
```markdown
<gmd-card backgroundColor="'rgb(0, 102, 204)'" textColor="'white'">
  <gmd-card-title>Blue Card</gmd-card-title>
  <gmd-md>This card uses RGB color values.</gmd-md>
</gmd-card>

```
{% endtab %}

{% tab title="CSS custom properties" %}
```markdown
<gmd-card backgroundColor="'var(--my-custom-color)'" textColor="'var(--my-text-color)'">
  <gmd-card-title>Themed Card</gmd-card-title>
  <gmd-md>This card uses CSS custom properties.</gmd-md>
</gmd-card>
```
{% endtab %}

{% tab title="Multiple cards" %}
```markdown
<gmd-grid columns="3">
  <gmd-cell>
    <gmd-card backgroundColor="'#ffffff'">
      <gmd-card-title>First Card</gmd-card-title>
      <gmd-md>Content for the first card.</gmd-md>
    </gmd-card>
  </gmd-cell>
  <gmd-cell>
    <gmd-card backgroundColor="'#f0f0f0'">
      <gmd-card-title>Second Card</gmd-card-title>
      <gmd-md>Content for the second card.</gmd-md>
    </gmd-card>
  </gmd-cell>
  <gmd-cell>
    <gmd-card backgroundColor="'#e0e0e0'">
      <gmd-card-title>Third Card</gmd-card-title>
      <gmd-md>Content for the third card.</gmd-md>
    </gmd-card>
  </gmd-cell>
</gmd-grid>
```
{% endtab %}
{% endtabs %}

### Grid

The grid component provides a flexible layout for organizing content with columns.

To add content to to your Grid, you must specify the number of columns with the `columns=` attribute, and then use either the `cell` component or any GMD component.

Also, you can style the grid with CSS Grid by targeting the `.grid-container` class and its responsive variants.

The component adjusts to the following screens sizes:

* Small screens with less than 768px. The component stacks the content in a single column.
* Medium screen with a minimum of 768px and a maximum of 1200px. The component reduces the columns.
* Large screens with more than 1200px. The component uses the specified number of columns.

Here are some use cases examples:

{% tabs %}
{% tab title="Basic Grid" %}
```markdown
<gmd-grid columns="2">
  <gmd-cell>Left content</gmd-cell>
  <gmd-cell>Right content</gmd-cell>
</gmd-grid>
```
{% endtab %}

{% tab title="Three column layout" %}
```markdown
<gmd-grid columns="3">
  <gmd-cell>Column 1</gmd-cell>
  <gmd-cell>Column 2</gmd-cell>
  <gmd-cell>Column 3</gmd-cell>
</gmd-grid>
```
{% endtab %}

{% tab title="Grid with a card component" %}
```markdown
<gmd-grid columns="2">
  <gmd-card>Left content</gmd-card>
  <gmd-card>Right content</gmd-card>
</gmd-grid>
```
{% endtab %}

{% tab title="Grid with a button component" %}
```
<gmd-grid columns="2">
  <gmd-button>Left content</gmd-button>
  <gmd-button>Right content</gmd-button>
</gmd-grid>
```
{% endtab %}
{% endtabs %}
