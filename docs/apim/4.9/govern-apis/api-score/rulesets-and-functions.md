---
description: An overview about rulesets and functions.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/govern-apis/api-score/rulesets-and-functions
---

# Rulesets and Functions

{% hint style="warning" %}
API Score is a technology preview. This feature is not recommended for production environments.
{% endhint %}

## Overview

API Score rulesets contain the rules that are used by API Score to rate your API. Under the hood, Gravitee uses an open source linting tool called [Spectral](https://github.com/stoplightio/spectral) to power the API Score capability.

Rulesets can analyze all of the assets that make up your Gravitee APIs, including the Gravitee API definition and any attached OpenAPI or AsyncAPI pages.

Gravitee provides default rulesets out of the box for OpenAPI and AsyncAPI doc pages. If the default rulesets do not fit your use case, you can create custom rulesets. For more information about custom rulesets, see [#custom-rulesets](rulesets-and-functions.md#custom-rulesets "mention").

## Rulesets

### Default rulesets

Spectral provides default rulesets for both OpenAPI and AsyncAPI.

For more information on OpenAPI default rulesets, see [OpenAPI Rules](https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules). For more information on AsyncAPI default rulesets, see [AsyncAPI Rules](https://docs.stoplight.io/docs/spectral/1e63ffd0220f3-async-api-rules).

{% hint style="info" %}
Spectral's default rulesets only apply to OpenAPI and AsyncAPI doc pages in your API. You must use custom rulesets for Gravitee API definitions. For more information about Custom rulesets, see [#custom-rulesets](rulesets-and-functions.md#custom-rulesets "mention").
{% endhint %}

### Custom rulesets

Custom rulesets allow you to define the rules that API Score will use to evaluate the quality your APIs. To create a custom rule, the following attributes must be defined:

* **description:** A human readable description of the rule.
* **message:** The message shown to the user in case the rule fails.
* **severity:** A weighted value that affects your API score. From least to most severe, possible values are: hint, info, warn, error.
* **given:** The JSON Path expression that points to the part of the document that should be used for scoring.
* **then:** This describes the functions that should be applied to evaluate the rule.

{% hint style="info" %}
For more information about Spectral's rulesets, go to [Rulesets.](https://docs.stoplight.io/docs/spectral/e5b9616d6d50c-rulesets)
{% endhint %}

#### Example

The following custom ruleset includes a single rule for checking that the API has at least one **label**. First, the rule checks that the **labels** attribute exists using the **truthy** function provided by Spectral. Next, it uses Spectral's built-in **length** function to check that the length of the **labels** array is at least **1**.

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

When you import a custom ruleset, you need to specify to which type of API or asset the ruleset applies. You can import the following ruleset formats:

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

1.  Log in to your APIM Console, then click **API Score**.

    <figure><img src="../../.gitbook/assets/image (211).png" alt=""><figcaption></figcaption></figure>
2.  Click **Rulesets & Functions**.

    <figure><img src="../../.gitbook/assets/image (212).png" alt=""><figcaption></figcaption></figure>
3.  Click **Import**.

    <figure><img src="../../.gitbook/assets/image (213).png" alt=""><figcaption></figcaption></figure>
4.  In **Asset Format**, choose the format for your ruleset.

    <figure><img src="../../.gitbook/assets/image (214).png" alt=""><figcaption></figcaption></figure>
5. In **Ruleset Information**, type the name of your ruleset.
6. (Optional) Type a description for your ruleset.
7. Attach the ruleset file. You can attach a file in the following formats:
   * .YML
   * .YAML
   * JSON
8. Click **Import**.

### Editing Rulesets

Once you've uploaded a ruleset, you can edit its name and description. If you want to modify the ruleset itself, you need to delete it and upload it again.

To edit a ruleset:

1.  Log in to your APIM Console, then click **API Score**.

    <figure><img src="../../.gitbook/assets/image (215).png" alt=""><figcaption></figcaption></figure>
2.  Click **Rulesets & Functions**.

    <figure><img src="../../.gitbook/assets/image (216).png" alt=""><figcaption></figcaption></figure>
3. In **Rulesets**, navigate to the ruleset that you want to edit.
4. Click the ruleset.
5.  Click **Edit**. You can now edit the ruleset.

    <figure><img src="../../.gitbook/assets/image (217).png" alt=""><figcaption></figcaption></figure>

## Functions

Spectral provides built-in functions that can be used to define custom rules. To go beyond what Spectral provides out of the box, you can write custom functions in JavaScript to define virtually any rule you can imagine.

### Default functions

{% hint style="info" %}
Spectral's functions can only be applied to OAS/AsyncAPI definitions. You must use custom functions for Gravitee API Definitions. For more information about Custom functions, see [#custom-functions](rulesets-and-functions.md#custom-functions "mention").
{% endhint %}

Spectral provides functions that you can use to score your API. For more information about Spectral's built-in functions, go to [Core functions](https://docs.stoplight.io/docs/spectral/cb95cf0d26b83-core-functions).

### Custom functions

Custom functions expand the capabilities of API Score by using your custom logic as part of the rules in your custom ruleset. A custom function is JavaScript code that takes part of your API definition, OpenAPI spec, or AsyncAPI spec as an input and determines based on its contents whether or not the rule is met. This allows you to implement virtually any rule, as arbitrarily as you'd like.

The example below shows a custom function that checks if an API's `lastUpdated` date is more recent than 1 year. If not, the rule fails and recommends that the user investigate whether or not this API is in need of maintenance.

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

To use a custom function from a custom ruleset, you first need to declare the custom function at the top of your ruleset. The name used to declare the custom function must be the same as the name of the file that contains the custom function.

Next, you can invoke the custom function from one of your rules. Be sure to use the **given** statement in your custom rule to pass the right document to your custom function.

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

In the custom ruleset above, the **updatedAt-recent** rule uses the **lastUpdated** custom function. The **given** statement is used to pass the API's last updated date to the function.
