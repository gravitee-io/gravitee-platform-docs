# Overview

{% hint style="info" %}
API Score is a technology preview. This feature is not recommended for production environments.&#x20;
{% endhint %}



<table data-view="cards"><thead><tr><th></th><th data-hidden data-type="content-ref"></th></tr></thead><tbody><tr><td>Enable API score</td><td><a href="broken-reference">Broken link</a></td></tr><tr><td>Rulesets and Functions</td><td><a href="broken-reference">Broken link</a></td></tr><tr><td>Types of Assets</td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

API score is Gravitee’s automated governance capability that lets you score your APIs based on criteria like security, documentation, and consistency. API Score is a static tool that looks at how your APIs are configured and designed, but does not perform tests on the data plane.&#x20;

The API score feature uses rulesets to score APIs. Gravitee provides default rulesets, but you can also create your own custom rulesets.&#x20;

Note that because it is a technical preview, API score is deactivated by default and requires an opt-in in order to use it.

## How API Score works

When you evaluate an API’s score, any relevant piece of information about your API’s design and settings are sent to the scoring service. Specifically, the Gravitee API definition for the API, as well as any OpenAPI or AsyncAPI documentation pages that you have attached to your API, are all sent to the scoring service.&#x20;

This means that virtually and setting or configuration that is part of your API can be used for scoring. This way, you can use API score to verify that your APIs comply with your organization’s standards and policies related to documentation, security, and more. For example, you can use API Score to verify the following aspects of your APIs:

* Is the API properly documented, with descriptions and markdown pages?
* Are the RBACs properly set on my API?
* Is my API exposed to consumers using a secure mechanism like JWT or OAuth 2.0?
* Does my API include specific policies, such as rate limiting or topic mapping?

When API Score scores your API, it returns issues in the form of errors, warnings, infos, and hints for you to investigate.  It also generates a percentage based on the number and severity of issues raised.&#x20;
