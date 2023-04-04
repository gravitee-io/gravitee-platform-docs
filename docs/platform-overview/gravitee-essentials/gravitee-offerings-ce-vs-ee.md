---
description: The Gravitee basics
---

# Gravitee Offerings: CE vs EE

Gravitee was founded as an open-source project and a large part of the overall platform remains so to this day. However, additional functionality such as the Gravitee Cockpit is not open source but has a free-to-use version in the **Gravitee Community Edition**. Additionally, there is also a [**Gravitee Enterprise Edition**](https://www.gravitee.io/pricing) that adds additional capabilities targeting commercial end users through offerings like Alert Engine, a no-code API Designer with unlimited data models, monetization capabilities, and advanced protocol mediation options.

{% hint style="info" %}
**Open Core Product**

Technically, Gravitee is what is known as an open core product and you can read more [about that here](https://thenewstack.io/a-standard-pricing-model-for-open-core/). It is summarized well in this excerpt:

> “The difference between open core and proprietary software is that open core produces a substantial amount of open source software, whereas solely proprietary software produces none. They both offer open source maintainers a way to get paid for their work, but open core contributes back to open source. Source available carries more advantages to the user than closed source. Most open core companies put a lot of effort toward maintaining the core. Therefore, open core is better than proprietary software for all of these reasons. The argument isn’t open core over open source, it’s open core instead of proprietary.”
{% endhint %}

#### Gravitee Community Edition <a href="#toc-h3-gravitee-community-edition" id="toc-h3-gravitee-community-edition"></a>

Gravitee’s Community Edition is comprised of Gravitee’s open source offerings, plus Gravitee’s free-to-use versions of Gravitee-managed enterprise products. The Gravitee Community edition includes access to the following products and services:

* **Gravitee API Management (APIM)**
  * **Gateway**: reverse proxy layer that brokers, secures, and hardens access to APIs and data streams; natively supports both synchronous and asynchronous APIs
  * **Developer portal**: build an API catalog and marketplace for API consumers fit with documentation, API analytics, and more
  * **Management UI**: a UI that teams can use to configure their Gateway, design and create APIs, design policies, and publish documentation. Every action in the API management console is tied to a REST API that can be accessed outside the console
  * **Management API**: REST API that can be used to configure and manage APIs and various Gravitee resources
* **Gravitee Cloud (GC)**: centrally manage Gravitee environments and installations and promote APIs across various environments; the community version is limited to one managed environment
* **Gravitee API Designer (APID)**: design, document, and publish API data models; the community version is limited to one data model
* **Gravitee API Access Management (AM)**: apply identity and access management (multi-factor authentication, biometric, etc.) at the API and application levels
* **Kubernetes operator**: manage APIs and Gravitee components via custom resource definitions
* **Hosting**: for the open source products, you are limited to self-hosted instances; Gravitee hosts the free versions of Cockpit and API Designer

For more information on the differences between Gravitee Community and OSS products vs Gravitee enterprise edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).

#### Gravitee Enterprise Edition <a href="#gravitee-enterprise-edition-16" id="gravitee-enterprise-edition-16"></a>

Built on top of our open-source foundations, the enterprise event-native API Management platform enables organizations to fully manage, secure, monitor, and govern their entire API ecosystem. The Enterprise Edition focuses on the needs of our commercial end users. Enterprise gets you everything in the community version, plus:

* **Advanced support for asynchronous APIs**: The Gravitee community edition supports various forms of protocol mediation and asynchronous API support; the enterprise edition includes this, plus quality of service for supported backend event brokers, advanced message-level policies, and more
* **Enterprise APID**: design, document, and publish an unlimited amount of API data models
* **Enterprise Plugins** various functionality that can be added to both Gravitee API Management and Gravitee Access Management as plugins, such as certain message-level policies, API monetization features, and more
* **Gravitee Alert Engine (AE)**: monitor API consumption and configure alerts based on anomalous traffic, reliability incidents, etc.
* **Hosting**: You can self-host Gravitee APIM and AM, choose a hybrid deployment where Gravitee manages certain components and you manage others, or a fully-managed Gravitee deployment where Gravitee hosts all components in its cloud
* **CSM and support**: Dedicated Customer Success Manager and team of Support Engineers
* **Direct access to Gravitee leadership**: speak directly with Gravitee leadership around roadmap, feature requests, and more

For more information on the differences between Gravitee Community and OSS products vs Gravitee enterprise edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).
