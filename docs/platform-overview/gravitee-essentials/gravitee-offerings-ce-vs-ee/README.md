---
description: Gravitee's core products
---

# Gravitee Offerings: CE vs EE

Gravitee was founded as an open-source project and our open-source roots are part of what makes us great - we own our entire stack, and we believe that Gravitee's **Community Edition (CE)** powers the best open-source API Management products**.**

Gravitee also offers an [**Enterprise Edition**](https://www.gravitee.io/pricing) **(EE)** that adds capabilities targeting commercial end users. The EE includes everything from the CE and offers additional features like Alert Engine, a no-code API Designer with unlimited data models, monetization capabilities, and advanced protocol mediation options.

{% hint style="info" %}
**Open Core Product**

Technically, Gravitee is what is known as an open core product, and you can read more [about that here](https://thenewstack.io/a-standard-pricing-model-for-open-core/). It is summarized well in this excerpt:

> “The difference between open core and proprietary software is that open core produces a substantial amount of open source software, whereas solely proprietary software produces none. They both offer open source maintainers a way to get paid for their work, but open core contributes back to open source. Source available carries more advantages to the user than closed source. Most open core companies put a lot of effort toward maintaining the core. Therefore, open core is better than proprietary software for all of these reasons. The argument isn’t open core over open source, it’s open core instead of proprietary.”
{% endhint %}

## Gravitee Community Edition <a href="#toc-h3-gravitee-community-edition" id="toc-h3-gravitee-community-edition"></a>

Gravitee’s Community Edition comprises Gravitee’s open-source offerings, plus the free-to-use versions of Gravitee-managed enterprise products. The Gravitee Community Edition includes access to the following products and services:

* [**Gravitee API Management (APIM)**](https://www.gravitee.io/platform/api-management)
  * **Gravitee API Gateway:** A reverse proxy layer that brokers, secures, and hardens access to APIs and data streams. It natively supports both synchronous and asynchronous APIs.
  * **Gravitee Management API:** Configure and manage APIs and various Gravitee resources.
  * **Gravitee Management UI:** Configure gateways, create APIs, design policies, and publish documentation. Every action in the APIM Management UI is tied to a REST API that can be accessed outside of the interface.
  * [**Gravitee API Developer Portal**](https://www.gravitee.io/platform/api-developer-portal)**:** Build an API catalog and marketplace for API consumers. Feature-rich with documentation generation, API analytics, etc.
* [**Gravitee Cloud (GC)**](https://www.gravitee.io/platform/cockpit)**:** Centrally manage Gravitee installations and promote APIs across various environments. The community version is limited to one managed environment.&#x20;
* [**Gravitee API Designer (APID)**](https://www.gravitee.io/platform/api-designer)**:** Design, document, and publish API data models with a no-code tool that enables accelerated and elegant API design and implements a design-first approach to reduce overhead when translating business requirements into high-quality API definitions. The community version is limited to one data model.&#x20;
* [**Gravitee Access Management (AM)**](https://www.gravitee.io/platform/access-management)**:** Apply identity and access management (MFA, biometrics, etc.) at the API and application levels.
* **Gravitee Kubernetes Operator:** Manage APIs and Gravitee components via K8s custom resource definitions.
* **Hosting:** Open-source products are limited to self-hosted instances with the exception of the free versions of Gravitee Cloud and Gravitee API Designer, which are hosted by Gravitee.

For more information on the differences between Gravitee Community Edition and Gravitee Enterprise Edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).

## Gravitee Enterprise Edition <a href="#gravitee-enterprise-edition-16" id="gravitee-enterprise-edition-16"></a>

The enhanced version of Gravitee's open-source and event-native API management platform, the Enterprise Edition enables organizations to fully manage, secure, monitor, and govern their entire API ecosystem. Focused on the needs of our commercial end users, EE buys you everything in the CE, plus:

* **Advanced support for asynchronous APIs:** The Gravitee Community Edition provides various forms of protocol mediation and asynchronous API support. The Enterprise Edition includes this, plus quality-of-service for supported backend event brokers, advanced message-level policies, and more.
* **Enterprise APID:** Design, document, and publish an unlimited amount of API data models.
* **Enterprise Plugins:** Functional extensions to Gravitee API Management and Gravitee Access Management such as certain message-level policies, API monetization features, and more.
* [**Gravitee Alert Engine (AE)**](https://www.gravitee.io/platform/api-observability)**:** Monitor API consumption and prevent incidences such as SLA breaches or traffic spikes via customized alerts based on anomalous traffic, reliability incidents, etc.&#x20;
* **Hosting:** Options include self-hosted Gravitee APIM and AM, a hybrid deployment where Gravitee manages certain components and you manage others, or a fully-managed Gravitee deployment where Gravitee hosts all components in its cloud.
* **CSM and support:** Dedicated Customer Success Manager (CSM) and team of Support Engineers (SEs).
* **Direct access to Gravitee leadership:** Speak directly with Gravitee leadership to discuss roadmap, feature requests, and more.

For more information on the differences between Gravitee Community Edition and Gravitee Enterprise Edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).

## CE vs EE - capability matrices

The Gravitee Enterprise Edition includes everything in the Community Edition plus additional modules, plugins, capabilities, and unlocked options as indicated below.

### Gravitee API Management

<table><thead><tr><th width="216">Capability</th><th width="58" data-type="checkbox">CE</th><th width="56" data-type="checkbox">EE</th><th>Notes</th></tr></thead><tbody><tr><td>API Gateway</td><td>true</td><td>true</td><td></td></tr><tr><td>API Management UI</td><td>true</td><td>true</td><td></td></tr><tr><td>Developer Portal</td><td>true</td><td>true</td><td></td></tr><tr><td>Environments per installation</td><td>true</td><td>true</td><td>CE: Limited to 1 env per installation<br>EE: Multiple depending on plan</td></tr><tr><td>Service management ecosystem</td><td>true</td><td>true</td><td>CE: Limited future AsyncAPI connectors<br>EE: Unlimited future AsyncAPI connectors</td></tr><tr><td>Kafka connector</td><td>false</td><td>true</td><td></td></tr><tr><td>Protocol mediation</td><td>false</td><td>true</td><td></td></tr><tr><td>Baked-in policies</td><td>true</td><td>true</td><td></td></tr><tr><td>Plugins</td><td>true</td><td>true</td><td></td></tr><tr><td>API management support</td><td>true</td><td>true</td><td>CE: Community support<br>EE: Enterprise-grade 24/7 support</td></tr><tr><td>Message-level policy support</td><td>false</td><td>true</td><td>Applies to asynchronous and event-driven APIs</td></tr><tr><td>Async and event-driven API support</td><td>false</td><td>true</td><td>Includes MQTT, Webhook, Websocket, and SSE</td></tr><tr><td>Engineer-to-engineer support</td><td>false</td><td>true</td><td>Applies to both production and non-production gateways</td></tr><tr><td>Customer Success services</td><td>false</td><td>true</td><td></td></tr></tbody></table>

### Gravitee Access Management

<table><thead><tr><th width="216">Capability</th><th width="58" data-type="checkbox">CE</th><th width="56" data-type="checkbox">EE</th><th>Notes</th></tr></thead><tbody><tr><td>Plugins</td><td>true</td><td>true</td><td></td></tr><tr><td>Basic MFA</td><td>true</td><td>true</td><td></td></tr><tr><td>AM support</td><td>true</td><td>true</td><td>CE: Community support<br>EE: Enterprise-grade 24/7 support</td></tr></tbody></table>

### Gravitee API Designer

<table><thead><tr><th width="216">Capability</th><th width="58" data-type="checkbox">CE</th><th width="56" data-type="checkbox">EE</th><th>Notes</th></tr></thead><tbody><tr><td>Drag-and-drop API Design tool</td><td>true</td><td>true</td><td>CE: Limited to one active design<br>EE: <a href="https://www.gravitee.io/contact-us">Contact us</a> to enable multiple designs</td></tr><tr><td>One-click publishing</td><td>true</td><td>true</td><td>CE: Limited to one active design<br>EE: <a href="https://www.gravitee.io/contact-us">Contact us</a> to enable multiple designs</td></tr></tbody></table>

### Gravitee Cloud

<table><thead><tr><th width="216">Capability</th><th width="58" data-type="checkbox">CE</th><th width="56" data-type="checkbox">EE</th><th>Notes</th></tr></thead><tbody><tr><td>Centrally manage all APIM/AM envs </td><td>true</td><td>true</td><td>CE: Limited to one environment per user<br>EE: <a href="https://www.gravitee.io/contact-us">Contact us</a> to enable multiple envs</td></tr></tbody></table>

## Offerings exclusive to EE

The following features and functionality are exclusive to Gravitee Enterprise Edition and require an [EE license](https://docs.gravitee.io/ee/ee\_licensing.html).&#x20;

{% hint style="info" %}
**EE installation**

Each EE capability, module, or plugin that requires an EE license is not part of the APIM or AM main distribution bundle and must be downloaded separately. See the [EE Installation page](https://docs.gravitee.io/ee/ee\_installation.html) for details.
{% endhint %}

<details>

<summary>Alert Engine</summary>

To activate Alert Engine in APIM or AM, apply an [EE license](https://docs.gravitee.io/ee/ee\_licensing.html) to an APIM/AM installation. Alert Engine includes the following capabilities:

* Implement true API-level observability and monitoring
* Configure custom alerting mechanisms
* Enable adaptive alerting
* (AM feature only) Trigger adaptive MFA to fine-tune alerting

</details>

<details>

<summary>Advanced environment management</summary>

* Connect unlimited Gravitee APIM environments and installations under one umbrella
* Promote APIs across various environments
* Oversee availability and health of Gravitee deployments and Gateways

</details>



### API security

* Advanced anomaly detection
* OpenAPI spec compliance&#x20;
* API inventory and lineage&#x20;
* Security ratings&#x20;

### APIM plugins

* [Data Logging Masking Policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_data\_logging\_masking.html)
* [Assign Metrics Policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_assign\_metrics.html)

### AM plugins

* [HTTP Flow Identity Provider](https://docs.gravitee.io/am/current/am\_userguide\_mfa\_factors\_http.html)
* [CAS Identity Provider](https://docs.gravitee.io/am/current/am\_userguide\_enterprise\_identity\_provider\_cas.html)&#x20;
* [Kerberos Identity Provider](https://docs.gravitee.io/am/current/am\_userguide\_enterprise\_identity\_provider\_kerberos.html)&#x20;
* [SAML 2.0 Identity Provider](https://docs.gravitee.io/am/current/am\_userguide\_enterprise\_identity\_provider\_saml2.html)
* [Gateway Handler SAML IDP - Enable SAML 2.0 Identity Provider support](https://docs.gravitee.io/am/current/am\_devguide\_protocols\_saml2\_configuration.html)
* [MFA with FIDO2](https://docs.gravitee.io/am/current/am\_userguide\_mfa\_factors\_fido2.html)
* [Risk-based MFA](https://docs.gravitee.io/am/current/am\_userguide\_mfa\_risk\_based.html)
* [Resource HTTP Factor](https://github.com/gravitee-io/gravitee-am-resource-http-factor) (no public documentation available yet - an [EE license](https://docs.gravitee.io/ee/ee\_licensing.html) is required to access this private repository)
* [Factor OTP Sender](https://github.com/gravitee-io/gravitee-am-factor-otp-sender) (no public documentation available yet - an [EE license](https://docs.gravitee.io/ee/ee\_licensing.html) is required to access this private repository)
