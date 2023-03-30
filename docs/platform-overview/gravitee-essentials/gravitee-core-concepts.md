---
description: Introduction to the Gravitee ecosystem
---

# Gravitee Core Concepts

### Introduction

The **API lifecycle** includes aspects such as API design, development, testing, deployment, troubleshooting, monitoring, and security. The need to manage the full API lifecycle is why comprehensive API management solutions like Gravitee were developed.

We want to give a quick introduction to what Gravitee is all about, including some Gravitee jargon you may not be familiar with. We promise to try and keep it brief. And then we’ll be on to actually getting our hands dirty with some code so you can stop fighting the urge to go take a nap. If you’re already intimate with Gravitee or just eager to start using the product, jump ahead to [Part 3: Getting Started](https://community.gravitee.io/t/part-3-getting-started/1460) to start implementing and using Gravitee features.

### Overview <a href="#overview-2" id="overview-2"></a>

Gravitee was started by 4 freelance developers who met back in 2015 while working on API strategy and implementation. They decided to build a complete API lifecycle toolset which later became the Gravitee we know and love today. So what all does Gravitee’s toolset offer? We thought it would be fun to hop on the latest trend and ask our soon to be AI overlords over at [ChatGPT](https://openai.com/blog/chatgpt/):

> Gravitee is an open-source API management platform that helps organizations design, deploy, and manage APIs. It provides a set of tools and features for building, testing, and securing APIs, as well as for managing the API lifecycle and monitoring API performance.
>
> Gravitee offers a range of capabilities, including:
>
> **API gateway**: A reverse proxy that sits in front of your APIs and helps route requests to the appropriate backend service. The gateway can also perform various tasks such as rate limiting, authentication, and transformation of requests and responses.\
> **API portal**: A web-based interface that allows developers to discover, test, and consume APIs. The portal provides documentation, interactive console, and code snippets to make it easy for developers to get started with your APIs.\
> **API analytics**: Gravitee provides detailed metrics and insights into the usage and performance of your APIs, including traffic patterns, error rates, and response times.\
> **API security**: Gravitee offers various security features such as OAuth 2.0, JWT, and mutual SSL to help protect your APIs from unauthorized access.
>
> Overall, Gravitee is a comprehensive platform for managing APIs, and it can be a useful tool for organizations looking to build and maintain a robust API strategy.

Not bad at all! However, there may still be hope for us mere mortals as ChatGPT missed a few key items.

First off, one of Gravitee’s core differentiators is the fact that it is an **event-native** API solution. This means Gravitee was built on an event-driven architecture implemented with reactive programming to handle asynchronous, event-driven APIs while still fully supporting synchronous request/response style APIs, and can even mediate between sync and async application layer protocols. For those who read [Part 1: The Essentials](https://community.gravitee.io/t/part-1-the-essentials/1458), isn’t it nice knowing what that buzz-wordified sentence actually means?

Gravitee was founded as an open-source project and a large part of the overall platform remains so to this day. However, additional functionality such as the Gravitee Cockpit is not open source but has a free-to-use version in the **Gravitee Community Edition**. Additionally, there is also a [Gravitee Enterprise Edition](https://www.gravitee.io/pricing) that adds additional capabilities targeting commercial end users through offerings like Alert Engine, a no-code API Designer with unlimited data models, monetization capabilities, and advanced protocol mediation options.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) _**Open Core product**_
>
> ***
>
> Technically, Gravitee is what is known as an open core product and you can read more [about that here](https://thenewstack.io/a-standard-pricing-model-for-open-core/). It is summarized well in this excerpt:
>
> > “The difference between open core and proprietary software is that open core produces a substantial amount of open source software, whereas solely proprietary software produces none. They both offer open source maintainers a way to get paid for their work, but open core contributes back to open source. Source available carries more advantages to the user than closed source. Most open core companies put a lot of effort toward maintaining the core. Therefore, open core is better than proprietary software for all of these reasons. The argument isn’t open core over open source, it’s open core instead of proprietary.”

Beyond this Gravitee Key Concepts and Core Offerings section, the dev guide will purely focus on the open-source offerings so anyone can follow along and get started using Gravitee today.

### Key Concepts <a href="#key-concepts-3" id="key-concepts-3"></a>

Like any software product, Gravitee has some jargon. Some of these terms are common throughout the API management industry while others are specific to Gravitee. We want to take a minute to decode some of the high-level concepts and terminology from the outset so you have a solid frame of reference as we continue to dive deeper into the product.

#### Gravitee Global Architecture <a href="#gravitee-global-architecture-4" id="gravitee-global-architecture-4"></a>

[![AM-APIM-Architecture](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/b/b014429c2135257d51371e103e78eda7e306277d\_2\_486x500.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/b/b014429c2135257d51371e103e78eda7e306277d.png)[![AE-Architecture](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/f6c37ddcbccccb7ea649a5fee08edebb7f3c4070\_2\_690x330.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/f6c37ddcbccccb7ea649a5fee08edebb7f3c4070.png)

When starting on your Gravitee journey, it can be difficult to understand how all the different pieces of the ecosystem fit together. These two architecture diagrams provide an excellent 10,000ft view to help you begin to conceptualize the Gravitee offering. The first diagram shows Gravitee’s API management ecosystem (APIM) and how it interacts with the access management ecosystem (AM). The second diagram highlights the function of Gravitee’s alert engine (AE). We’ll be working with each of the components in detail in future tutorials. In the meantime, here’s a few important things to note about the architecture diagrams:

* API publishers make requests to the management API from either the management console’s GUI or by using CLI tools. The management API is focused on two major areas:
  * Creating and deploying APIs to the gateway which determine how requests are proxied from end-users to backend APIs
  * Exposing backend APIs in a developer portal to be accessed by API consumers
* As shown, a single Gravitee APIM instance is composed of several core Gravitee components
* An AM instance is deployed separately from APIM which can be linked together or used as standalone products
* Each APIM and AM instance is attached to a Gravitee Cockpit environment
* Cockpit has a hierarchy with three entity types:
  * The top level is an _account_ (typically corresponding to a company)
  * The next level is an _organization_ (typically corresponding to a logical part of the company in the particular company context, such as a region or business unit)
  * The lowest level is an _environment_ (typically corresponding to an environment in an IT infrastructure, such as a development or production environment)

[![Screen Shot 2023-01-24 at 11.26.38 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/7bf3116daf4855840784ef9a860641ddf335f924\_2\_690x230.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/7/7bf3116daf4855840784ef9a860641ddf335f924.png)

#### API Gateway: Policies and Plugins <a href="#api-gateway-policies-and-plugins-5" id="api-gateway-policies-and-plugins-5"></a>

API Management encompasses API design, API security and access management, API reliability, API delivery, and API productization. At the core of this sphere of responsibility sits the API Gateway which, as ChatGPT pointed out, is a reverse proxy that sits in front of your APIs and helps route requests to the appropriate backend service while also performing various tasks such as rate limiting, authentication, and transformation of requests and responses. Typically, the main method of enforcing security, reliability, and the proper movement of data are **policies**.

Policies are rules or logic that can be executed by the API gateway during the request or the response of an API call. By default, the Gravitee comes with a [large number of policies available for use](https://docs.gravitee.io/apim/3.x/apim\_policies\_overview.html) to control how an API is consumed. This control can manifest in a variety of ways, and policies can be used for all sorts of reasons and objectives, ranging from making APIs more secure to making them reliable to making them profit-drivers in the case of API Monetization. Here is a list of common kinds of API policies that you might execute at the gateway level:

* Traffic shaping policies: use a Gateway to strip, shape, or otherwise alter network traffic so to make consumption of APIs and the movement of data more secure, reliable, performant, or efficient
  * For example, you could strip certain information as data is brokered and sent to the client application so as to keep sensitive data from the client application and/or make a message leaner given a client application that might not need that specific set of stripped information
* Authentication policies: use a Gateway to enforce certain authentication methods to ensure that an API consumer is in fact authenticated to ask for information from your backend
  * For example, you could use an API key authentication policy to limit API consumption to a set of client applications that are able to pass a specific, unique API key with each request
* Rate limiting policies: policies that limit and/or throttle the the number of requests over a set time period
  * For example, you could use a rate limiting policy to limit your API to a maximum of 100 calls/min/consumer
* Dynamic routing policies: policies that are used to dispatch inbound calls to different targets / endpoints or to rewrite URIs
  * For example, you could use a dynamic routing policy to redirect requests from `http://gateway/apis/store/12/info` to `http://backend_store12/info`

Another Gravitee term you’ll often hear mentioned is **plugins**. [Plugins](https://docs.gravitee.io/apim/3.x/apim\_devguide\_plugins.html) are components that additional functionality by _plugging into_ the Gravitee ecosystem. Policies are simply a type of plugin. In other words, policies are a feature or function that are enabled through the functionality known as plugins. Check out the [plugin marketplace](https://www.gravitee.io/plugins) to see what plugins are currently available from both Gravitee and the community. For now, that’s all you need to know, but we’ll take a deeper dive in a future tutorial where we’ll be getting familiar with using, and eventually building, plugins/policies!

#### API Developer Portals & API Productization <a href="#api-developer-portals-api-productization-6" id="api-developer-portals-api-productization-6"></a>

One of the other critical components of API management is the ability to expose APIs to your various consumers. These consumers can take many forms, as outlined by the following table:

| Consumer                       | Use case and/or strategic initiative                                                                                                                                                                                                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Internal Developer             | Organizations that are using APIs as internal tools to build products and services might be using APIs to connect systems, data sources, etc. The typical consumer of an API here would be the internal developer at your organization that needs to access and use that API to build the application that they are responsible for. |
| External Developer as Customer | This use case is very similar to the internal developer use case. However, instead of a developer at your company using your API as an internal tool, your API can be exposed to developers at other companies that could use your API in their product instead of building that functionality on their own.                         |
| Partner                        | Organizations that have technical partnerships that require integrations between certain products and/or feature sets might expose sets of APIs to those partners.                                                                                                                                                                   |

The best way to expose these APIs to your consumers is through an **API developer portal**. An API developer portal is a centralized catalog where internal API consumers and/or external API consumers can discover, find, subscribe, and manage subscriptions to APIs that are developed, managed, and deployed by API publishers.

For example, a developer at a FinTech company could create a “stock price fetcher” API that could be used to present real-time stock prices. This API could be published to a portal for other developers at that FinTech company to use when creating various banking applications that rely on visualizing stock prices in a UI. The developer portal ensures all other developers at the company have awareness of, and secure access to, that API so they don’t have to build that functionality themselves.

Another important facet of exposing APIs to fellow developers is API documentation. To borrow Stoplight’s definition, “API docs, or API description documents, are the collection of references, tutorials, and examples that help developers use your API. Your API’s documentation is the primary resource for explaining what is possible with your API and how to get started.”

It is crucial to include high-quality, up-to-date documentation with your APIs in your developer portal so that developers and other consumers have an easy time knowing how to consume your APIs. Otherwise, your teams will have spent valuable time and effort developing APIs only so that they go unused, or at the very least, don’t reach their consumption potential.

Finally, a growing use case for API developer portals is API monetization. API monetization allows you to turn APIs into self-serve, revenue-generating products with plans that govern how consumers can pay to access/consume your APIs. For example, you could charge delivery companies a set amount per message for a “track packages in real-time" API.

#### API Access Management <a href="#api-access-management-7" id="api-access-management-7"></a>

Access management can exist outside of the realm of API management, but API-security-forward organizations are beginning to implement API access management as a part of their larger API security and/or API management strategies.

**API access management** is essentially what it sounds like: applying typical access management practices to the API level. For example, you could use API access management to implement step-up authentication, an authentication method that is defined by adding extra factors of authentication in front of certain APIs or features in your application that might contain/move sensitive data. Let’s take an example of a banking application. In this example, instead of just enforcing multi-factor authentication (MFA) at the log-in level, maybe you’d choose to enforce an extra factor of authentication (such as facial recognition or fingerprint) when a client app or consumer tries to call a “payments API” that is responsible for brokering bank and routing numbers so that you can make or receive in-app payments.

Implementing access management at the API level is important for security-forward organizations because APIs are the ultimate brokers of data, both sensitive and non-sensitive. API-level access management allows for more fine-tuned access control in areas of applications where sensitive data exists. This allows you to further secure your applications and/or APIs by verifying that the consumer is who they claim to be while also fine-tuning the customer experience by only adding the friction of access control where sensitive data might exist.

#### API Design-First <a href="#api-design-first-8" id="api-design-first-8"></a>

Not always considered a part of every organization’s API management strategy, API design is the stage where you plan and make intentional architectural decisions around how and why your API interacts with client and backend (or, in east/west use cases, service and service).

API design is becoming increasingly important for organizations that are implementing API design-first methodology. **API design-first** is defined as organizations choosing to approach development decisions and planning by first starting with an API design or data model and then generating the API specification. This makes it easier for teams to include less technical, business users and build APIs that are more “fit for purpose” as they pertain to business value.

#### Gravitee API Definitions <a href="#gravitee-api-definitions-9" id="gravitee-api-definitions-9"></a>

In Part 1 of the dev guide, we covered API architectural styles and specifications in depth. In the world of Gravitee, there is a similar sounding term known as an **API definition**. An API definition is very similar to an API specification except it is a specification _for your Gravitee gateway._ It’s a JSON representation of everything that the Gravitee gateway needs to know in order for it to proxy, apply policies to, create plans for, etc. your APIs and their traffic.

Each [Gravitee API definition brings with it certain capabilities](https://www.gravitee.io/blog/gravitee-api-definitions) which you can read about further in the linked article. The key thing you need to note is that **latest API definition is v4** and is still in beta as of the Gravitee 3.20 release. The v4 definition allows for advanced protocol mediation (i.e. fronting Kafka with a Webhook, Websocket, HTTP API, etc.) and the ability to apply Gravitee policies (i.e. authentication, traffic shaping, etc.) to asynchronous API traffic–[at the message level.](https://community.gravitee.io/t/gravitee-3-20-release-tutorials-http-post-over-mqtt-websocket-over-mqtt-and-more/1427) This is done by decoupling what is known as the gateway **entrypoints** and **endpoints**.

To keep things simple:

* Gateway Entrypoint: how the consumer “calls” or “subscribes” to the gateway. This essentially defines how a consumer will end up consuming data from a producer/provider
* Gateway Endpoint: the datasource from/to which the gateway will fetch/post data for/from the consumer that calls or subscribes to the gateway

So, for example, if you wanted to make it possible for an API consumer to consume events from a Kafka topic over a Websocket connection, you would choose a “Websocket” entrypoint and a “Kafka” endpoint when creating your API in Gravitee. If you wanted to make it possible for an API consumer to POST data onto a Kafka topic via a HTTP API, you would use the Gravitee HTTP POST entrypoint and Kafka endpoint.

As of Gravitee 3.20, the v4 definition must be [manually enabled](https://docs.gravitee.io/apim/3.x/v4\_new\_policy\_execution\_engine\_introduction.html#how\_to\_enable\_and\_disable\_the\_new\_engine) and is only available via the management API (management console/UI support coming soon).

#### Gravitee API Deployment Options <a href="#gravitee-api-deployment-options-10" id="gravitee-api-deployment-options-10"></a>

When it comes to Gravitee, there are two major components that can be deployed: the APIs themselves and the Gravitee infrastructure, which include the API gateway and management console among other components. While Part 3 of the dev guide will dive into how to actually deploy and use Gravitee infrastructure, we want to provide a quick overview of the different ways you can deploy APIs with Gravitee.

For Gravitee to be able to support [infrastructure as code (IaC)](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac) use cases, deployment needs to be able to be handled “as code,” and APIs need to be able to be pushed to/deployed to the API Gateway, tested, and then promoted across environments (test, dev, prod, etc.) without ever having to step a digital foot into a UI.

Many of our customers are already implementing an IaC practice using Gravitee. Some customers start off this way (i.e. customers who are already mature when it comes to GitOps, Kubernetes, etc.), but at least ⅓-½ of our customers gradually work their way into an IaC-compatible approach. We describe this process through the lens of API “deployment maturity.”

> **Note**: the term “maturity” here is not morally valenced or judgemental. We simply use the term to describe the sequential process that we see _most_ of our customers move through. There are many reasons for and benefits associated with each of the deployment styles mentioned below.

Traditionally, Gravitee customers progress through three levels of API “deployment maturity”:

**Gravitee Console/UI**

Gravitee comes with an easy-to-use, self-serve UI that is often used for development (we estimate that ⅓-½ of our customers use this UI for development).

**Gravitee Management API**

Every action in the Gravitee UI is tied a REST API that makes up the Gravitee management API. The management API exposes a complete set of endpoints and is [documented using the OpenAPI spec](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_documentation.html#apim\_console\_api\_reference). As a result, everything you can do in the UI can be done via REST API calls for developers wanting to script some part of APIM administration. Typically, as customers start to move into a GitOps world and moving things across higher environments, they use things like GitLab, Jenkins, Bitbucket, GitHub Actions, etc. to manage everything in a data serialization format like JSON or YAML.

**Kubernetes-native using the Gravitee Kubernetes Operator**

This approach moves beyond relying on the console/UI and the underlying management API. If you deploy APIs in a Kubernetes cluster, you can describe your API as an API extension of Kubernetes using CRDs (custom resource definitions). Essentially, this means that when you deploy something natively to your K8s cluster, there’s an operator there that can deploy that API to the Gravitee gateway without relying on a proprietary UI or REST API. This is powered by the Kubernetes API and the Gravitee Kubernetes Operator. This is the preferred method of deployment if your organization is set on using Kubernetes.

> **Note:** When you deploy the Kubernetes YAML file and everything deployed to the Gravitee Gateway and is up and running, you can still see the API and API definition in the Gravitee console and complete actions like deploying that API to the developer portal. However, as an administrator, there are some components of the API that you cannot change, as the source of truth is the Kubernetes YAML file. While this may seem like a restriction, this is a feature, not a bug. When implementing IaC, a key principle is to never change something in the “live form,” and instead change it in the code and observe the changes as they manifest in the front end.

### Core Offerings <a href="#core-offerings-14" id="core-offerings-14"></a>

#### Gravitee Community Edition <a href="#gravitee-community-edition-15" id="gravitee-community-edition-15"></a>

Gravitee’s Community Edition is comprised of Gravitee’s open source offerings, plus Gravitee’s free-to-use versions of Gravitee-managed enterprise products. The Gravitee Community edition includes access to the following:

* **API Gateway**: reverse proxy layer that brokers, secures, and hardens access to APIs and data streams; natively supports both synchronous and asynchronous APIs
* **API Developer Portal**: build an API catalog and marketplace for API consumers fit with documentation, API analytics, and more
* **API Management Console**: a UI that teams can use to configure their Gateway, design and create APIs, design policies, and publish documentation. Every action in the API management console is tied to a REST API that can be accessed outside the console
* **Management API**: REST API that can be used to configure and manage APIs and various Gravitee resources
* **Community Cockpit**: centrally manage Gravitee environments and installations and promote APIs across various environments; the community version is limited to one managed environment
* **Community API Designer**: design, document, and publish API data models; the community version is limited to one data model
* **API Access Management (AM)**: apply identity and access management (multi-factor authentication, biometric, etc.) at the API and application levels
* **Kubernetes Operator**: manage APIs and Gravitee components via custom resource definitions
* **Hosting**: for the open source products, you are limited to self-hosted instances; Gravitee hosts the free versions of Cockpit and API Designer

For more information on the differences between Gravitee Community and OSS products vs Gravitee enterprise edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).

#### Gravitee Enterprise Edition <a href="#gravitee-enterprise-edition-16" id="gravitee-enterprise-edition-16"></a>

Built on top of our open-source foundations, the enterprise event-native API Management platform enables organizations to fully manage, secure, monitor, and govern their entire API ecosystem. Enterprise gets you everything in the community version, plus:

* **Advanced support for asynchronous APIs**: The Gravitee community edition supports various forms of protocol mediation and asynchronous API support; the enterprise edition includes this, plus quality of service for supported backend event brokers, advanced message-level policies, and more
* **Enterprise API Designer**: design, document, and publish an unlimited amount of API data models
* **Enterprise Plugins** various functionality that can be added to both Gravitee API Management and Gravitee Access Management as plugins, such as certain message-level policies, API monetization features, and more
* **Alert Engine**: monitor API consumption and configure alerts based on anomalous traffic, reliability incidents, etc.
* **Hosting**: You can self-host Gravitee APIM and AM, choose a hybrid deployment where Gravitee manages certain components and you manage others, or a fully-managed Gravitee deployment where Gravitee hosts all components in its cloud
* **CSM and support**: Dedicated Customer Success Manager and team of Support Engineers
* **Direct access to Gravitee leadership**: speak directly with Gravitee leadership around roadmap, feature requests, and more

For more information on the differences between Gravitee Community and OSS products vs Gravitee enterprise edition, [please refer to this document](https://www.gravitee.io/hubfs/Datasheets/Gravitee-OSS-vs-Enterprise.pdf).

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) _**Gravitee APIM Instance**_
>
> ***
>
> You will often hear references to a Gravitee API Management (APIM) instance, but you probably noticed none of the core offerings are actually called APIM. APIM is just an umbrella term that encompasses Gravitee’s gateway, developer portal, management API, and management UI.

This should be a decent mental framework for you to refer back to as we do a deep dive into each of Gravitee’s components. If this caused further confusion or you have some questions, just shoot us a reply to let us know!
