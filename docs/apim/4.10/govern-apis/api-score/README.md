---
description: An overview about api score.
metaLinks:
  alternates:
    - ./
---

# API Score

{% hint style="warning" %}
API Score is a tech preview. This feature is not recommended for production environments.
{% endhint %}

<table data-view="cards"><thead><tr><th data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="enable-api-score.md">enable-api-score.md</a></td></tr><tr><td><a href="view-api-scores.md">view-api-scores.md</a></td></tr><tr><td><a href="rulesets-and-functions.md">rulesets-and-functions.md</a></td></tr><tr><td><a href="types-of-assets.md">types-of-assets.md</a></td></tr></tbody></table>

## Overview

API Score is Gravitee’s automated governance capability. It lets you score your APIs based on criteria like security, documentation, and consistency. As a static tool, API Score evaluates how your APIs are configured and designed, but does not perform tests on the data plane.

The API Score feature uses rulesets to score APIs. Gravitee provides default rulesets, but you can also create your own custom rulesets.

API Score is a technology preview, meaning that it is deactivated by default and you must opt-in to use it.

## How API Score works

When you evaluate an API’s score, any relevant piece of information about your API’s design and settings is sent to the scoring service. Specifically, the scoring service receives the Gravitee API definition, as well as any OpenAPI or AsyncAPI documentation pages attached to your API.

Virtually any setting or configuration that is part of your API can be used for scoring. This lets you use API Score to verify that your APIs comply with your organization’s standards and policies related to documentation, security, and more. For example, you can use API Score to verify the following aspects of your API:

* Is the API properly documented, with descriptions and Markdown pages?
* Are the RBACs properly set?
* Is the API exposed to consumers using a secure mechanism like JWT or OAuth 2.0?
* Does the API include specific policies, such as rate limiting or topic mapping?

When API Score scores your API, it returns issues in the form of errors, warnings, infos, and hints for you to investigate. It also generates a scoring percentage based on the number and severity of issues raised.

## How your API score is calculated

Your API's score is calculated using the following formula:&#x20;

`100 · e^−0.1·(1.0·nbErrors + 0.5·nbWarnings + 0.2·nbInfos + 0.1·nbHints)` which is the same as `nbErrors + 0.5·nbWarnings + 0.2·nbInfos + 0.1·nbHints` .

Your API's score is projected onto a function that has the following shape:&#x20;

<figure><img src="../../.gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>

For example, if your API has 1 error, 0 warnings, 2 infos, and 1 hint, the score is calculated as follows:

`math.exp(-.1*(1e + .5 w + .2i + .1h)) * 100`&#x20;

This formula results in a score of `22.31%`.
