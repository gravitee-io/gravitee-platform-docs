# Rulesets and functions

{% hint style="warning" %}
API Score is a technology preview. This feature is not recommended for production environments.&#x20;
{% endhint %}

## Overview

API Score rulesets contain the rules that are used by API Score to rate your API. Rulesets can analyse all of the assets that make up your Gravitee APIs, including the Gravitee API definition itself, as well as any attached OpenAPI or AsyncAPI pages.

\
Under the hood, Gravitee uses an open source linting tool called [Spectral](https://github.com/stoplightio/spectral) to power the API Score capability.

\
Gravitee provides default rulesets out of the box for OpenAPI and AsyncAPI doc pages. But if the default rulesets do not fit your use case, you can create custom rulesets. For more information about custom rulesets, see [#custom-rulesets](rulesets-and-functions.md#custom-rulesets "mention").

## Rulesets

### Default rulesets

{% hint style="info" %}
Spectral's default rulesets only apply to OpenAPI and AsyncAPI doc pages in your API. You must use custom rulesets for Gravitee API Definitions. For more information about Custom rulesets, see [#custom-rulesets](rulesets-and-functions.md#custom-rulesets "mention").
{% endhint %}

### Custom rulesets

Custom rulesets allow you to define the rules that API Score will use to evaluate the quality your APIs.\
To create a custom rule, the following attributes must be defined:

* **description:** This is a human readable description of the rule.
* **message:** This is the message shown to the user in case the rule fails\`;&#x20;
* **severity:** Here are the following severity levels that have different weights that effect your API, in order from highest to lowest severity:
  * error
  * warn
  * info
  * hint
* **given:** JSON Path expression that points to the part of the document that should be used for scoring.
* **then:** describes the functions that should be applied to evaluate the rule.&#x20;

{% hint style="info" %}
For more information about Spectral's rulesets, go to [Rulesets.](https://docs.stoplight.io/docs/spectral/e5b9616d6d50c-rulesets)
{% endhint %}

Here is an example of a custom ruleset that includes a single rule for checking that the API has at least one **label**. To achieve this, the rule first checks that the **labels** attribute exists using the **truthy** function provided by Spectral. Then, it checks that the length of the **labels** array is at least **1**, using Spectral's built-in **length** function.&#x20;

{% code lineNumbers="true" %}
```yaml
rules:
  has-labels:
    description: "The API should have at least one label."
    message: "This API does not have any labels. We recommend using labels to better document your APIs."
    severity: "warn"
    given: "$.api"
    then:
      - field: "labels"
        function: "truthy"
      - field: "labels"
        function: "length"
        functionOptions:
          min: 1
```
{% endcode %}

### Importing rulesets

When importing a custom ruleset, you'll need to specify to which type of API or what type of asset this ruleset should apply. You can import the following ruleset formats:&#x20;

* OpenAPI
* AsyncAPI
* Gravitee Proxy API
* Gravitee Message API
* Gravitee Native Kafka
* Gravitee Federated API
* Gravitee v2 API

{% hint style="info" %}
If you import a custom OpenAPI or AsyncAPI ruleset, this ruleset overrides Spectral's default rulesets.
{% endhint %}

To import custom rulesets, complete the following steps:

1. From your homepage, click **API Score**.

<figure><img src=".gitbook/assets/image (211).png" alt=""><figcaption></figcaption></figure>

2. Click **Rulesets & Functions.**

<figure><img src=".gitbook/assets/image (212).png" alt=""><figcaption></figcaption></figure>

2. Click **Import.**

<figure><img src=".gitbook/assets/image (213).png" alt=""><figcaption></figcaption></figure>

2. In **Asset Format**, choose the format for your ruleset.&#x20;

<figure><img src=".gitbook/assets/image (214).png" alt=""><figcaption></figcaption></figure>

3. In **Ruleset Information**, type the name of your ruleset.
4. (Optional) Type a description for your ruleset.
5. Attach the ruleset file. You can attach a file in the following formats:
   1. .YML
   2. .YAML
   3. JSON
6. Click **Import**.

### Editing Rulesets

Once you've uploaded a ruleset, you can edit its name and description. If you want to modify the ruleset itself, you'll need to delete it and upload it again.&#x20;

1. From the homepage, click **API Score**.&#x20;

<figure><img src=".gitbook/assets/image (215).png" alt=""><figcaption></figcaption></figure>

2. Click **Rulesets & Functions**

<figure><img src=".gitbook/assets/image (216).png" alt=""><figcaption></figcaption></figure>

2. In **Rulesets**, navigate to the ruleset that you want to edit.&#x20;
3. Click the ruleset.&#x20;
4. Click **Edit**. You can now edit the ruleset.

<figure><img src=".gitbook/assets/image (217).png" alt=""><figcaption></figcaption></figure>

## Functions

Spectral provides built-in functions that can be used to define custom rules. But in order to go beyond what Spectral provides out of the box, you can write custom functions in JavaScript. This lets you define virtually any rule you can imagine.

### Default functions

{% hint style="info" %}
Spectral's functions can be applied to only OAS/AsyncAPI definitions. You must use custom functions for Gravitee API Definitions. For more information about Custom functions, see [#custom-functions](rulesets-and-functions.md#custom-functions "mention").
{% endhint %}

Spectral provides functions that you can use to score your API. For more information about Spectral's built-in functions, go to [Core functions](https://docs.stoplight.io/docs/spectral/cb95cf0d26b83-core-functions).

### Custom functions&#x20;

Custom functions expand the capabilities of API Score by writing your own custom logic as part of the rules in your custom ruleset. A custom function is a piece of JavaScript code that takes as an input a piece of your API definition, OpenAPI spec, or AsyncAPI spec, and determines based on its contents whether or not the rule is met. This allows you to implement virtually any rule that you would like, as arbitrary as you'd like.&#x20;

In [the example below](https://graviteeio.slack.com/archives/D07GJ0SF30T/p1740655301357519), I've written a custom function that checks that the API's lastUpdated date is more recent than 1 year. If not, the rule fails and recommends that the user should investigate whether or not this old API is in need of maintenance.

```javascript
function lastUpdated(jsonInput) {
  
  const lastUpdatedDate = new Date(jsonInput);
  const currentDate = new Date();
  const twelveMonthsAgo = new Date(currentDate.setMonth(currentDate.getMonth() - 12));

  if (lastUpdatedDate < twelveMonthsAgo) {
    return [
      {
        message: `This API has not been updated in 12 months.`,
      },
    ];
  }
}

export default lastUpdated;
```

To use this custom function from a custom ruleset, you first need to declare the custom function at the top of your ruleset. The name used to declare the custom function must be the same as the name of file that contains the custom function.

Then, you can invoke the custom function from one of your rules. Be sure to use the **given** statement in your custom rule to pass the right document to your custom function.

```yaml
functions:
  - lastUpdated

rules:
  
  has-categories:
    description: "The API should be part of at least one category."
    message: "This API is not part of any category. We recommend using categories to better organize your APIs."
    severity: "warn"
    given: "$.api"
    then:
      - field: "categories"
        function: "truthy"
      - field: "categories"
        function: "length"
        functionOptions:
          min: 1

  updatedAt-recent:
    description: "The updatedAt date should not be older than 12 months."
    message: "This API might may to be reviewed or archived because it was last updated more than 12 months ago."
    severity: "warn"
    given: "$.api.updatedAt"
    then:
      function: "lastUpdated"
```

In the custom ruleset above, you can see that the **updatedAt-recent** rule uses the **lastUpdated** custom function. The **given** statement is being used to pass the API's last updated date to the function.
