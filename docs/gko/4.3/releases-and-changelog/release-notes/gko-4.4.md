# GKO 4.4

## Gravitee Kubernetes Operator 4.4 release notes

With the release of Gravitee 4.4, we’ve pushed some important updates to the Gravitee Kubernetes Operator (GKO:

* Introducing V4 API support with GKO
  * V4 API groups and members
  * V4 API docs pages
  * V4 API categories
  * V4 API CRD export
* Expanded V2 API support
  * V2 API doc pages
  * V2 API categories

We’ll just cover the new support for v4 APIs in these release notes, as both v2 API enhancements to the GKO offer the same functionality and benefits as their correlates in v4.&#x20;

## New support for v4 APIs

The Gravitee v4 API definition offers Gravitee customers the most modern, advanced API functionality within the Gravitee platform. For example, v4 APIs enable users to create APIs that expose everything from REST, to TCP services, to event brokers as APIs, and even APIs from other API Gateways.

The v2 API definition is our legacy API definition and only supports more traditional SOAP and HTTP proxying.&#x20;

Historically, the GKO only supported v2 APIs. Now, v4 APIs are also supported.

{% hint style="info" %}
**Dedicated CRDs**

v2 and v4 APIs will each have a dedicated CRD. 

{% endhint %}

As of Gravitee 4.4, you can use the GKO for the following kinds of v4 API configuration:

* **API groups and members**: define various groups and members that can create, review, update, and/or delete v4 APIs
* **API documentation**: create and upload API documentation for your v4 APIs&#x20;
* **Categories**: define categories for your APIs, so that your API consumers can better sort through and discover the APIs that they need

You can also now export an existing V4 API in Gravitee API Management as a GKO custom resource definition (CRD) so that you can start using the GKO to manage any APIs that you may have already created using Gravitee. This is great for teams that might want to start in the Management console GUI and then move towards a more GitOps-oriented approach, which is where the GKO really shines.


The GKO user documentation has also undergone a major rework to improve quality and coverage, and it now occupies its own space at the root of the Gravitee user documentation alongside its siblings like APIM and AM.

## Wrapping up

With new support for both v4 and v2 APIs, as well as documentation pages, groups and members, you’re one step closer to using Gravitee for your GitOps API Management initiatives. For information on the GKO, feel free to browse the brand new GKO documentation, or reach out to your CSM or a [Gravitee Engineer](https://www.gravitee.io/demo).
