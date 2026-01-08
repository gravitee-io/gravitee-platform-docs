# Gravitee Markdown components

## Overview

You can customize the New Developer Portal with Gravitee Markdown, which is standard Markdown enriched with dynamic components.

Here are available Gravitee Markdown components:

* [#block](gravitee-markdown-components.md#block "mention")
* [#button](gravitee-markdown-components.md#button "mention")
* [#card](gravitee-markdown-components.md#card "mention")
* [#grid](gravitee-markdown-components.md#grid "mention")

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
This style has a solid background with white text. By default, the color is the primary color of the Developer Portal theme. For more information about the Developer Portal theme, see [layout-and-theme.md](layout-and-theme.md "mention").

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
* External links must be the full URL. For example, `https://example.com`.
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="filled" link="https://gravitee.io" target="_blank">Visit Gravitee</gmd-button>
```
{% endtab %}

{% tab title="Outlined" %}
This style is a transparent background with a colored border and text. By default, the button color is blue (#1976d2), the border color is light gray (#CDD7E1), the button label text is the primary color of the Developer portal theme. For more information about the Developer Portal theme, see [broken-reference](../../../4.9/developer-portal/new-developer-portal/broken-reference/ "mention").

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
* External links must be the full URL. For example, `https://example.com`.
* The default target is `_self` , which opens the link in the same tab. To open the link in a new tab, set `target` to `target="_blank"` .
{% endhint %}

```markdown
<gmd-button appearance="outlined" link="https://docs.gravitee.io" target="_blank">Documentation</gmd-button>
```
{% endtab %}

{% tab title="Text" %}
This style is a transparent background with colored text only. By default, the color is primary color of the Developer Portal theme. For information about the Developer Portal theme, see [broken-reference](../../../4.9/developer-portal/new-developer-portal/broken-reference/ "mention").

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
* External links must be the full URL. For example, `https://example.com`.
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
