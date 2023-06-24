---
description: >-
  A robust conceptual framework to understand how the system works without
  necessarily knowing how to build it
---

# API Fundamentals

The following sections comprise a high-level overview of core concepts and functionality essential to Gravitee and dispel pervasive API myths, misconceptions, and misunderstandings.

## API Basics <a href="#api-basics-2" id="api-basics-2"></a>

An application programming interface, or API, is a set of publicly exposed definitions and protocols that enable the creation and integration of application software. These conventions comprise a software intermediary that allows computer programs or applications to communicate.&#x20;

While "API" and "web API" are often used interchangeably, web APIs are a specific subset of API that operate over a network. "API" has much broader implications and includes every method or function called in programming, whether built into a language or made available by a 3rd party package or module.&#x20;

Consider the following Python snippet:

```python
from datetime import datetime

date_str = "12/25/1996"
date_object = datetime.strptime(date_str, "%m/%d/%Y")
```

Importing the `datetime` module provides access to public methods, or APIs, like `strptime` to convert a `string` into a `datetime` object. Although not network-related, this API still imposes a software contract, which guarantees the stability of the API with respect to the current software version. The contract allows the programmer to have confidence in the API's expected behavior without understanding how the input data is transformed.&#x20;

{% hint style="info" %}
Respecting API contracts is the basis for **semantic versioning** in software. Check out [this article](https://blog.webdevsimplified.com/2020-01/semantic-versioning/) this article for an introduction to semantic versioning and to learn how API contracts are managed as software is continuously updated.
{% endhint %}

APIs enable the trusted layers of abstraction that are critical programming. For example, most developers prefer to use a high-level programming language like Python as opposed to a [low-level assembly language](https://www.investopedia.com/terms/a/assembly-language.asp). Numerous abstractions allow a Python print statement to look like this:

```python
print('Hello, World')
```

instead of this:

```asm6502
; hello-DOS.asm - single-segment, 16-bit "hello world" program
;
; assemble with "nasm -f bin -o hi.com hello-DOS.asm"

    org  0x100        ; .com files always start 256 bytes into the segment

    ; int 21h is going to want...

    mov  dx, msg      ; the address of or message in dx
    mov  ah, 9        ; ah=9 - "print string" sub-function
    int  0x21         ; call dos services

    mov  ah, 0x4c     ; "terminate program" sub-function
    int  0x21         ; call dos services

    msg  db 'Hello, World!', 0x0d, 0x0a, '$'   ; $-terminated message
```

Beyond developer experience and productivity, abstraction remains critical. For example, the vast majority of people don’t understand how email works, just that there are inputs (i.e., interface conventions): recipients, subject, message body, the send button, etc., and output: a rapid form of text-based communication. Abstractions, and therefore APIs, are necessary for efficiency and innovation.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/a8a51b9365a05b24e391d475f37a6fb6408d9150.png" alt=""><figcaption><p>Abstraction meme posted on <a href="https://www.reddit.com/r/ProgrammerHumor/comments/orerw4/abstraction/">reddit</a>.</p></figcaption></figure>

{% hint style="warning" %}
Gravitee uses the terms "web API" and "API" synonymously. An API that does not communicate over a network is explicitly referred to as a local API.
{% endhint %}

## Web APIs <a href="#web-apis-protocols-architectures-specifications-and-data-serialization-formats-3" id="web-apis-protocols-architectures-specifications-and-data-serialization-formats-3"></a>

To further clarify web API structure and functionality, this section addresses:

* [Internet vs world wide web](api-fundamentals.md#internet-vs-world-wide-web)
* [shift to microservices](api-fundamentals.md#shift-to-microservices)
* [API protocols](api-fundamentals.md#protocols-4)
* [API architectures/patterns](api-fundamentals.md#architectural-stylespatterns-5)
* [API specifications](api-fundamentals.md#specifications-6)
* [Data-interchange formats](api-fundamentals.md#data-interchange-formats-7)

### Internet vs world wide web

A web API is an API that is accessible over a network. Although the type of network is not specified, common usage of "web API" presumes the combination of the internet and the world wide web.

The internet is the [physically interconnected](https://theconversation.com/in-our-wi-fi-world-the-internet-still-depends-on-undersea-cables-49936) global network of computers along which information travels. Much of this information is in the form of hypermedia (e.g., web pages) and organized in a construct known as the world wide web, which is essentially an application running on the internet infrastructure. However, the world wide web, or web, is only one way to access or manage information on the internet. For example, Voice over Internet Protocol (VoIP) enables calls over the internet without interacting with the web.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5b31e8183ce2abee47d7194607538270bde34bc3_2_690x492.png" alt=""><figcaption><p>Photo of the underwater cables connecting the internet from this <a href="https://www.weforum.org/agenda/2015/11/how-can-we-protect-the-internets-undersea-cables/">blog</a></p></figcaption></figure>

{% hint style="info" %}
For a quick history lesson and a bit more detail about the relationship between the internet and the world wide web, [watch this excellent video](https://www.youtube.com/watch?v=eHp1l73ztB8\&t=189s).
{% endhint %}

### Shift to microservices

The popularity of web APIs is largely due to the [shift from monolithic applications to microservices](https://www.gravitee.io/blog/what-are-microservices-how-do-they-enhance-web-applications). To summarize, microservices are replacing monoliths because not all aspects of a project scale in parallel. Microservices enable cloud-native applications through the functional separation and independent scaling of each runtime, and web APIs establish standardized contracts for network interfacing and provide distributed architectures with reliable communication.

The underlying framework powering web APIs is quite complicated. Web APIs rely on communication protocols to deliver information to intended recipients, and network data must be serialized into data-interchange format for transport. In addition, API design and documentation should adhere to both an architecture and a specification.&#x20;

API protocols, data-interchange formats, architectures, and specifications are often insufficiently defined and differentiated. For example, the REST architectural style is inaccurately used as a proxy for the HTTP application layer protocol. The following sections offer high-level clarifications.

### Protocols <a href="#protocols-4" id="protocols-4"></a>

APIs are categorized by their architectural style or the application layer protocol they use to communicate over the network (e.g., an HTTP API). Protocol terminology is based on the [layered networking model](https://www.quora.com/What-is-the-difference-between-HTTP-protocol-and-TCP-protocol/answer/Daniel-Miller-7?srid=nZLo), which conceptualizes communication within and between computers at different abstractions and with respect to different functionality. The transport layer and the application layer contain the protocols most relevant to APIs.&#x20;

#### Transport layer

The two most widely used transport layer protocols are the user datagram protocol (UDP) and the transmission control protocol (TCP) which both support [packet-based messaging.](https://www.cloudflare.com/learning/network-layer/what-is-a-packet/) The main differentiator is that UDP is more lightweight at the expense of error checking and does not guarantee packet integrity, delivery, or order of delivery. UDP is suitable if data loss results in minor artifacts (e.g., real-time video calls) but not for use cases that demand high accuracy (e.g., routing banking information).

The need for accurate and reliable data factors heavily into why many application layer protocols are built on top of TCP. TCP provides robust error checking to ensure packets are not lost, corrupted, duplicated, or delivered out of order.

#### Application layer

The application layer is the top layer of the layered network model and contains many recognizable protocols, such as those shown in the table below. Protocol network communication is either synchronous or asynchronous and can differ between versions of the same protocol.

<table><thead><tr><th width="347">Name</th><th width="135">Abbreviation</th><th>Communication Type</th></tr></thead><tbody><tr><td>Hypertext Transfer Protocol</td><td>HTTP</td><td>Sync/Async</td></tr><tr><td>Hypertext Transfer Protocol Secure</td><td>HTTPS</td><td>Sync/Async</td></tr><tr><td>Websocket</td><td>N/a</td><td>Async</td></tr><tr><td>Server Sent Events</td><td>SSE</td><td>Async</td></tr><tr><td>File Transfer Protocol</td><td>FTP</td><td>Sync</td></tr><tr><td>Message Queuing Telemetry Transport</td><td>MQTT</td><td>Async</td></tr><tr><td>Advanced Message Queuing Transport</td><td>AMQP</td><td>Async</td></tr><tr><td>Kafka’s Custom Binary Protocol</td><td>N/a</td><td>Async</td></tr><tr><td>Google Remote Procedure Call</td><td>gRPC</td><td>Sync/Async </td></tr><tr><td>Simple Object Access Protocol</td><td>SOAP</td><td>Sync/Async </td></tr><tr><td>Simple Mail Transfer Protocol</td><td>SMTP</td><td>Sync</td></tr><tr><td>Domain Name Service</td><td>DNS</td><td>Sync/Async </td></tr><tr><td>Extensible Messaging and Presence Protocol</td><td>XMPP</td><td>Async</td></tr></tbody></table>

Application layer protocols define how independent programs and services communicate over networks and share information. While the other protocol layers focus on delivering data to a destination, the application layer protocols are responsible for establishing communication standards that dictate how that data is accessed and consumed. Specifically, the application layer provides the programs at each end of a communication link with interface methods to ensure that the request and response are understood and managed correctly. The role the application layer plays in defining interface conventions explains why an API type and its protocol are often synonymous.

#### A working example

Modern web browsers are applications that communicate over the HTTP/HTTPS protocol (HTTPS is HTTP with encryption and verification) but often truncate the visible website address to omit the protocol and subdomain. This is evidenced by visiting a site such as [Google](https://google.com/) and double-clicking the URL.

<div>

<figure><img src="../.gitbook/assets/google_shortened.png" alt=""><figcaption><p>Shortened URL</p></figcaption></figure>

 

<figure><img src="../.gitbook/assets/google_expanded.png" alt=""><figcaption><p>Expanded URL</p></figcaption></figure>

</div>

The graphic below clarifies the structure and individual components of a web address, which concatenate to form the broader uniform resource locator (URL), uniform resource identifier (URI), and uniform resource name (URN).

<figure><img src="../.gitbook/assets/uri_diagram1.png" alt=""><figcaption><p><a href="https://hanseul-lee.github.io/2020/12/24/20-12-24-URL/">URI vs URL vs URN</a></p></figcaption></figure>

A communication link between two applications requires that each endpoint is defined by a network socket, which is a combination of transport layer protocol, domain (which resolves to an IP address), and port number that uniquely and completely resolves the web address of a client request to a web server.

{% hint style="info" %}
Web browsers communicate over HTTP, which is built on top of TCP, so the transport layer protocol is assumed. However, this will be [changing with HTTP/3](https://www.cloudflare.com/learning/performance/what-is-http3/), which is built on top of UDP.
{% endhint %}

When `google.com` is typed in a web browser, it is expanded to `https://www.google.com:443`, where `www.google.com` is the fully qualified domain name that is resolved into an IP address through [domain name system (DNS) resolution](https://serverfault.com/questions/643506/how-does-the-http-get-method-work-in-relation-to-dns-protocol/643511#643511) and 443 is the port reserved for HTTPS on every network (port 80 is reserved for HTTP). The browser’s request is directed to Google’s web server using the HTTPS application layer protocol, in particular the GET [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods), and Google’s web server interprets the request and responds with the Google homepage.&#x20;

HTTP includes standard status codes to qualify the state of every network communication. For example, if the requested [resource](https://restful-api-design.readthedocs.io/en/latest/resources.html) does not exist, Google’s web server will respond with a 404.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5243c9b089b8754b37695dedcf1450bace820b90_2_690x262.png" alt=""><figcaption><p>HTTPS error response example</p></figcaption></figure>

#### Endpoints

The route portion of a URL combined with an HTTP method constitutes an HTTP API endpoint, and each resource is accessible through a unique endpoint. For example, `GET http://foo.com/api/user/1` and `GET http://foo.com/api/user/2` contain different routes and correspond to distinct resources. `GET http://foo.com/api/user/1` and `POST http://foo.com/api/user/1` are also considered unique endpoints due to the change in HTTP method.

In this example, all resources, and all therefore endpoints tied to this API, exist under a single API entry point of `http://foo.com/api`. The entry point can be viewed as a special type of endpoint: as the gateway to the API, it’s a resource that exists outside of any other collection and contains all other collections of resources.

Path parameters allow variable values to be passed along the URL path of a request. In a typical API route, the path is divided into segments separated by slashes ("/"). Path parameters are denoted by a placeholder or variable name within curly braces ("{}"). When a request is made, the actual value for the parameter is substituted in place of the placeholder. The above example could represent an endpoint as `GET http://foo.com/api/user/{id}` where {id} is the path parameter.

#### Protocol types

Application layer protocols have the ability to stack, which has resulted in numerous protocols with an HTTP/HTTPS dependency.&#x20;



Let’s take the SOAP application layer protocol as an example. SOAP sits at the same layer of the network model as HTTP, but SOAP is also dependent on another application layer protocol, typically, but not always, HTTP, in order to function. But why do this? Well, as we’ve pointed out, HTTP is _the_ application layer protocol of the web. This means there has been a huge, global investment in infrastructure, both server and client-side (i.e., web browsers), designed around HTTP/HTTPS. Additionally, security provisions such as firewalls tend to let in network traffic targeted for ports 80/443 which makes applications that build on top of the HTTP protocol much more likely to work out of the box.

So the SOAP protocol effectively tunnels over HTTP. This is a strategy employed by many protocols, including some more modern asynchronous protocols like WebSocket, but more on that [later](broken-reference).

{% hint style="info" %}
**WebSocket clarification**

To be fair, Websocket is not a perfect example here. The WebSocket protocol [handshake](https://www.baeldung.com/cs/handshakes) uses HTTP, but HTTP is not involved past that point. You can read a bit more about this distinction [here](https://stackoverflow.com/a/47085864).
{% endhint %}

However, the internet, or any network for that matter, supports many application layer protocols that are in no way tied to HTTP. Most of the other application layer protocols we care about in the context of this guide are built on top of raw TCP. For example, [Kafka implements a custom binary application protocol](https://kafka.apache.org/protocol.html) over TCP due to performance concerns with the text-based HTTP protocol when delivering massive amounts of real-time data. Additionally, even a protocol like SOAP can be made to function over raw TCP although this is something you’ll rarely see in practice for the aforementioned reasons.

That about wraps up our macroscopic discussion on protocols. The key takeaway here is that APIs are dependent on protocols, a lot of protocols, in the network stack. The ideal protocol stack, just like the ideal application stack, is completely context-dependent and is subject to many considerations such as application environment, security concerns, payload considerations, network quality, etc.

{% hint style="info" %}
**Is Webhook an application layer protocol?**

Due to their ever-growing popularity, you may stumble across mentions of Webhook APIs. Since APIs are often categorized by the application layer protocol employed, this can quickly lead to a misunderstanding. Webhook uses the HTTP protocol and is not an application layer protocol itself. In fact, Webhooks are not even APIs. Webhooks are essentially a functionality that can be added to your existing APIs. This excerpt [from Redhat](https://www.redhat.com/en/topics/automation/what-is-a-webhook) explains it well:

> “Webhooks are often referred to as reverse APIs or push APIs, because they put the responsibility of communication on the server, rather than the client. Instead of the client sending HTTP requests—asking for data until the server responds—the server sends the client a single HTTP POST request as soon as the data is available. Despite their nicknames, webhooks are not APIs; they work together. An application must have an API to use a webhook.”
{% endhint %}

### Architectural styles/patterns <a href="#architectural-stylespatterns-5" id="architectural-stylespatterns-5"></a>

Some of you might be wondering why we left the quintessential web API protocol, the REST API, out of the mix. Well that’s because REST is not a type of protocol at all, it’s an architectural style! REST stands for “representational state transfer”, and we’ll dive into what that means in a bit. REST APIs use the HTTP application protocol (not a REST requirement, but practically speaking, REST APIs always employ the HTTP protocol) and must adhere to several architectural constraints to be considered a REST or RESTful API:

> * **Uniform interface**. All API requests for the same resource should look the same, no matter where the request comes from. The REST API should ensure that the same piece of data, such as the name or email address of a user, belongs to only one uniform resource identifier (URI). Resources shouldn’t be too large but should contain every piece of information that the client might need.
> * **Client-server decoupling**. In REST API design, client and server applications must be completely independent of each other. The only information the client application should know is the URI of the requested resource; it can’t interact with the server application in any other ways. Similarly, a server application shouldn’t modify the client application other than passing it to the requested data via HTTP.
> * **Statelessness**. REST APIs are stateless, meaning that each request needs to include all the information necessary for processing it. In other words, REST APIs do not require any server-side sessions. Server applications aren’t allowed to store any data related to a client request.
> * **Cacheability**. When possible, resources should be cacheable on the client or server side. Server responses also need to contain information about whether caching is allowed for the delivered resource. The goal is to improve performance on the client side, while increasing scalability on the server side.
> * **Layered system architecture**. In REST APIs, the calls and responses go through different layers. As a rule of thumb, don’t assume that the client and server applications connect directly to each other. There may be a number of different intermediaries in the communication loop. REST APIs need to be designed so that neither the client nor the server can tell whether it communicates with the end application or an intermediary.
> *   **Code on demand (optional)**. REST APIs usually send static resources, but in certain cases, responses can also contain executable code (such as Java applets). In these cases, the code should only run on-demand.
>
>     [— From IBM’s “What is a REST API” blog](https://www.ibm.com/topics/rest-apis)

REST APIs and their associated architectural constraints came about from Roy Fieldings' now iconic Ph.D. dissertation “Architectural Styles and the Design of Network-based Software Architectures.” Their explosion in popularity is due to many factors, but a major contributor is how they enabled scale and fault tolerance through their _stateless nature_. Because each request-response cycle is completely independent, each request can be handled by an arbitrary server instance allowing essentially limitless horizontal scaling.

REST APIs are structured to where each resource is identified by a single URL and the actions on that resource are managed by the HTTP verbs (GET, POST, etc.), the request headers, and the request body. This structure forms the basis of the required uniform interface. For each request from the client, the server makes any modifications requested by the client and transfers a _representation of the state_ of the requested resource to the client, hence the name, representational state transfer. The key here is the statelessness of REST APIs. Each request contains all of the information necessary to be processed by the server, rather than be dependent on the server for storing the session state.

{% hint style="info" %}
**Stateless processing enables massive scalability**

For more details on how statelessness enables scale, check out [this excellent article](https://www.metaswitch.com/blog/how-stateless-processing-enables-massive-scalability).
{% endhint %}

As you continue surfing the world wide web, you’ll begin to notice that REST has become the ultimate buzzword, and just about every API under the sun claims to be _RESTful_. Unfortunately, these claims often just mean that the API has been designed according to some, but not all, of the architectural constraints listed above. These APIs are sometimes and more accurately referred to as _REST-like_ APIs.

Preceding the inception of REST, another major architectural style you’ll come across is the **remote procedure call** or RPC. RPC-based APIs utilize several different application layer protocols such as HTTP, SOAP, and gRPC. The main differentiator you should be aware of is REST URLs are resource-centric (`http://foo/user/1`) while RPC URLs are action-centric (`http://foo/getUser`). You can think of a remote procedure call as essentially being the same as calling a function in your programming language of choice, only remotely over a network.

Unlike REST, there is not a clearly designated set of architectural constraints for an API to be considered RPC-based. Again, both REST and RPC are styles and real-world implementations often don’t fit neatly into either bucket. This has led to implementations such as GraphQL (an architectural style, a [query language](https://www.techopedia.com/definition/3948/query-language) for APIs, and a runtime for fulfilling those queries) where proponents of GraphQL often bill it as “GraphQL is essentially RPC, with a lot of good ideas from the REST community tacked in.”

![Barbossa quote](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/7/76f171dfa488be51a8a398df8d79013e90564480.png)

{% hint style="info" %}
**Deep dive on RPC vs REST**

If the RPC/REST waters are still muddy, [this article](https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/) is highly recommended as it provides some great implementation examples that highlight the strengths and weaknesses of both styles.
{% endhint %}

Now, generally speaking, any API implemented with a REST, RPC, or a GraphQL architectural style, will follow a synchronous network communication model known as the _client-server_ or the **request-response model**. In our documentation, we prefer to use the request-response model nomenclature as client and server are broad terms used in almost all network communication models which can lead to confusion. We’ll go into more details later, but simply put, in this model the client computer makes a request directly to the server computer which responds by _serving_ data or a service. So while the client and server applications are decoupled and function independently, synchronous _communication_ is inherently tightly coupled.

Historically, the request-response network communication model has dominated and is one of the foundations of the modern web. However, more recently, an asynchronous network communication model known as **event streaming** or _message streaming_ has risen to prominence. An event in this context is any change in the state of a resource. In the event streaming model, there is a computer known as the **event broker** which allows clients to _publish_ messages to the broker or _subscribe_ to receive messages from the broker.

Several architectural styles implement event streaming but we’ll mostly be focused on the popular publish/subscribe, or pub/sub, pattern. Similar to RPC, pub/sub is a fairly general pattern without a lot of tight architectural constraints. The core tenet of the pub/sub pattern is decoupling communication between information producers, or **publishers**, from information consumers, or **subscribers**, through the aforementioned broker; therefore, the publishers and subscribers remain ignorant of each other. This loose coupling greatly simplifies communication (i.e., the publisher has a single target, the broker) which can allow you to design a more scalable and flexible event-driven system. APIs following the pub/sub pattern utilize many different application layer protocols such as MQTT, AMQP, and the aforementioned custom Kafka binary protocol. Again, more on the distinctions between the request-response and event-streaming network communications models in the sections to come.

{% hint style="info" %}
**Events vs messages**

Although often used synonymously, you can draw a distinction between an event and a message. Sometimes people will say a message is the directed carrier of the event, while the event is the actual change in state to be observed. Or that events are a specific type of message. But these terms have a deeper, technical distinction which you can [read about here](https://developer.lightbend.com/docs/akka-guide/concepts/message-driven-event-driven.html). However, for our documentation, we will continue to use the high-level distinction of the message being the directed carrier of the event.
{% endhint %}

So to recap, web API architectural styles are completely separate from the underlying protocols that are powering the API. The architectures are focused on guiding the API designer which, generally, is a mixture of you, the developer, and other stakeholders more focused on the high-level business logic.

{% hint style="info" %}
**Design-first methodology**

This mixture of technical and business interests around APIs is why you’ll often hear the benefits of API design-first development touted. To better understand the design-first methodology and the purported benefits, check out [this in-depth blog post](https://www.gravitee.io/api-first) from Gravitee. Still not sold? It’s worth noting that the OpenAPI Initiative (detailed in the following section) also [recommends a design-first approach](https://oai.github.io/Documentation/best-practices.html#use-a-design-first-approach) to building APIs.
{% endhint %}

### Specifications <a href="#specifications-6" id="specifications-6"></a>

So, as detailed in the previous section, architectural styles essentially add additional constraints regarding how the client and server interact with each other. But this still leaves a lot of leeway when it comes to how to use a particular API, whether REST, RPC, or a mixture. What endpoints are available? What actions can I perform? How do I authenticate? What parameters can I pass?

If you’re mumbling to yourself, just check the documentation, then you my friend, are spot on. However, even attempting to document the most basic of APIs can be quite an arduous and time-consuming investment. You need to be sure your documentation is clear and intuitive for all users of your API. And after documenting several APIs, you would begin to realize how repetitive the process of API documentation can become. On top of that, you would quickly realize how difficult it is to ensure your documentation has 100%, comprehensive coverage of your API. Finally, even if you manage to pull this off, your work is never truly complete as the documentation must be updated with every change and bug fix associated with your API. Keeping this from becoming a massive migraine is where API specifications come in. Let’s start with the OpenAPI specification defined below:

> The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs, which allows both humans and computers to discover and understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic. When properly defined via OpenAPI, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. Similar to what interface descriptions have done for lower-level programming, the OpenAPI Specification removes guesswork in calling a service.
>
> [— From OpenAPI Specification v3.1.0](https://spec.openapis.org/oas/latest.html)

Sound nice? It really is and API specifications open a whole new range of possibilities when it comes to API design such as documentation generation, code generation, validation and linting, mock servers, and much more. They should also appeal to your sharply-honed, developer instincts around the do not repeat yourself, or DRY principle, which has likely been repeatedly hammered into your psyche. API specifications ensure you can scratch that itch by keeping a single source of truth in what is known as your **API description file**.

So how do you go about building an API using a specification like OpenAPI? Well, that is a bit beyond the scope of the article, and honestly, a waste of our time. As you might expect for a documentation-focused end product, [OpenAPI’s documentation](https://oai.github.io/Documentation/specification.html) is quite excellent. Read through that guide and you’ll have a clear grasp on implementation in no time. Or if you just want a quick overview of how the specification is structured, check out [this sweet interactive mind map](https://openapi-map.apihandyman.io/).

It is important to note that OpenAPI is not the only API specification in town. Far from it in fact. There are loads of other specifications such as OData, RAML, GraphQL (a query language with its own specification), WSDL, and AsyncAPI, to name just a few. Some of these serve a unique role such as WSDL serving SOAP APIs or the GraphQL specification serving GraphQL APIs, while others have plenty of overlap such as RAML and OpenAPI both serving HTTP APIs.

For your API management journey, it is in no way essential to learn all these specifications and their nuances right out of the gate. We simply want to acknowledge their purpose and recognize that most of them focus primarily on **synchronous APIs**. We still haven’t really defined what this means, but for now, just know there are two major API communication paradigms: synchronous and asynchronous. And when it comes to asynchronous APIs, the [AsyncAPI specification](https://www.asyncapi.com/) is king.

{% hint style="info" %}
**AsyncAPI vs CloudEvents**

At some point, you’ll likely stumble upon someone comparing AsyncAPI to CloudEvents. CloudEvents is yet another specification but is really in a separate category from the specifications previously discussed. Specifications like AsyncAPI are focused on the overall application and the channels it uses to communicate while CloudEvents defines an envelope for your application’s actual data.

As a questionable metaphor, let's look at the postal service. You can think of AsyncAPI as being responsible for defining what constitutes a complete address and the means of routing the actual mail. Meanwhile, CloudEvents would be focused on defining the envelope specifications such as your envelope can be a maximum of 11-1/2" long x 6-1/8" high. However, the letter you actually send, or the **payload**, does not fall under the jurisdiction of either specification.

If this distinction is not clear, read [this article](https://www.asyncapi.com/blog/asyncapi-cloud-events) for a more in-depth comparison. We’ll be defining and discussing much of the article’s terminology around events later in this guide so consider this a sneak preview.
{% endhint %}

### Data-interchange formats <a href="#data-interchange-formats-7" id="data-interchange-formats-7"></a>

So far, we’ve covered the protocols that power every API as well as the frameworks that support the design and development of various implementations of APIs. Now we want to take a moment to zoom in and talk about the API **payload**: the actual data being transported by the API.

Let’s kick off this section with a quick example. Take a look at the Javascript object below:

```javascript
const sampleObject = {
  numberOneGateway: "gravitee",
  numberTwoGateway: "kong",
};
```

For the sake of our example, we’ll say “sampleObject” is our API payload. There are two key items for us to consider:

1. the data needs to be encoded into a universal format
2. the data needs to be placed into a self-contained chunk or stream

For the first item, how can we ensure any client using our API can receive the payload in a usable format? The client is certainly not guaranteed to be using Javascript to develop their application which means they might not be able to parse this object. Clearly, some type of conversion needs to take place before the payload is delivered to the client.

For the second item, at first glance, it seems to already be resolved. Our entire object is assigned to the variable “sampleObject.” However, Javascript is another high-level programming language that abstracts away a lot of magic that is going on under the hood. The short version is that objects generally do not directly contain their data in the same contiguous block of memory; in reality, objects store references to that data which is housed in a separate block of memory. Therefore, a single object with numerous properties could be spread all over the memory of a running process.

So how can we prep this object for transport?

Thankfully, **serialization** solves both of these concerns. Serialization is the process of converting an object in memory to a stream of bytes for storage or transport. Once serialized, the data can easily be transferred over a network, and upon reaching its destination, the data can be deserialized, which is simply the inverse operation. Data-interchange format and serialization format can be used synonymously.

The key here is that the object is encoded in a universal format of which there are two major types: **text-based** formats and **binary** formats. These formats, of which there are many, help ensure the data can be easily deserialized by any client. When it comes to the web, the JavaScript Object Notation format, or JSON, currently dominates.

{% hint style="info" %}
**Data serialization format comparison**

For a quick comparison of some other common formats, check out [this blog post](https://blog.mbedded.ninja/programming/serialization-formats/a-comparison-of-serialization-formats/).
{% endhint %}

As you might have guessed by the name, Javascript has first-class support for JSON:

```javascript
const serializedData = JSON.stringify(sampleObject);
console.log(serializedData);
typeof serializedData;
// Console Output:
// {"numberOneGateway":"gravitee","numberTwoGateway":"kong"}
// 'string'

const deserializedData = JSON.parse(serializedData);
console.log(deserializedData);
console.log(typeof deserializedData);
// Console Output:
// {numberOneGateway: 'gravitee', numberTwoGateway: 'kong'}
// 'object'
```

If you’ve never seen it before, this transformation probably looks quite unremarkable. And it is unremarkable on the surface. But that’s simply because JSON borrowed quite heavily from Javascript’s object literal notation. Again, hence the name. However, the data did change as the object keys were transformed into strings and the object itself became a primitive string that contains all the data from the original object in a self-contained chunk. And despite the name, JSON is a widely used and supported format that can be parsed by most programming languages. Here’s a quick example of serializing data with JavaScript, saving it to disk, and loading it into memory with Python.

```javascript
import fs from "fs";

const sampleObject = {
  numberOneGateway: "gravitee",
  numberTwoGateway: "kong",
};
const serializedObject = JSON.stringify(sampleObject);

fs.writeFileSync("./serialized_data.json", serializedObject);
```

```python
import json

with open("./serialized_data.json", "r") as file:
    deserialized_data = json.loads(file.read())

print(deserialized_data)
print(type(deserialized_data))

# Console Output:
# {'numberOneGateway': 'gravitee', 'numberTwoGateway': 'kong'}
# <class 'dict'>
```

Nice, so while not web APIs, we used the local APIs built into the JavaScript and Python programming languages to serialize an object to JSON, save it to local storage, read from storage, and deserialize the JSON string into a Python dictionary. All possible thanks to the JSON data-interchange format. And all quite simple thanks to JavaScript and Python’s local APIs.

When it comes to web APIs, the serialization format is often dependent on the application layer protocol you employ. For example, SOAP APIs prescribe XML as the one and only serialization format while HTTP APIs are encoding agnostic allowing you to select from a [plethora of options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics\_of\_HTTP/MIME\_types) including HTML, JSON, XML, CSV, binary formats, or even implementing your own custom serialization format. Besides all the HTML used to structure web pages, JSON continues to dominate over other formats due to its universality, lightweight format, and human-readable text.

However, there is never a one-size fits all solution, and binary formats are where JSON sees its stiffest competition. In situations where you are transferring a high volume of data and performance is critical, binary formats are preferred over JSON. This is why [Apache Avro is recommended for Kafka](https://www.confluent.io/blog/avro-kafka-data/) even though Kafka also supports JSON. Additionally, by default JSON is schema-less and does not enforce [type safety](https://levelup.gitconnected.com/what-is-type-safety-705b1813e0bb) which you can view as prioritizing flexibility over validation and error-checking. This is why some binary formats such as [protocol buffers](https://developers.google.com/protocol-buffers), or protobufs, have surged in popularity by correcting the aforementioned issues around performance and validation.

{% hint style="info" %}
**Validation for JSON?**

At some point, you may have heard of JSON Schema which is essentially a tool to allow users to opt-in to JSON structure validation. You can read more about [it here](https://json-schema.org/understanding-json-schema/about.html) and get a crash course on schemas and data types.
{% endhint %}

## Categorizing Web APIs <a href="#categorizing-web-apis-8" id="categorizing-web-apis-8"></a>

Humans love to put things in categories. It’s our way of making sense of this chaotic, confusing world and allows us to function under the notion of structure, order, and purpose. So now we’re going to take a deeper look at two important and _separate_ categorizations for web APIs: **Synchronous vs Asynchronous** and **Stateless vs Stateful**.

Before proceeding, it’s important to note that there is often cross-pollination between these two concepts; but on the contrary, they are entirely independent concepts as we will make clear in the following sections.

### Synchronous vs Asynchronous <a href="#synchronous-vs-asynchronous-9" id="synchronous-vs-asynchronous-9"></a>

Synchronous vs Asynchronous web APIs, or sync vs async as they are often referred to, represent an essential demarcation point between APIs. The two approaches represent a paradigm shift in how APIs communicate. Earlier, we touched on this topic when comparing the request-response network communication model to event streaming, and now we’re going to do a much deeper dive. But before we look specifically at APIs, let’s look at the synchronous vs asynchronous concepts from a much broader perspective.

#### **Synchronous vs Asynchronous: Programming**

Humans [can’t multitask](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7075496/) when it comes to high-level functions. This is to say, we can only carry a single train of thought. And although we often try to emulate multitasking by rapidly task-switching, this is a far cry from what is known as [parallelism](https://en.wikipedia.org/wiki/Parallel\_computing), which in computer science, is the simultaneous execution of two or more tasks. In terms of our metaphor, parallel computing would require two minds. Please let us know immediately if you achieve this state. For the rest of us, when you eat and watch a movie, you’re really just violently pinging your attention between Lord of the Rings and that delicious slice of pizza. This limitation becomes crystal clear if you attempt more cognitively demanding tasks. Trying to solve two math problems simultaneously provides definitive evidence humans can not parallel compute.

This underlying truth leads humans to plan in a manner akin to **synchronous programming**: a _linear, sequential execution_ of tasks. First complete task A then B then C, where each task blocks the execution of the following task. For example, you might make a plan to call your car insurance provider and then finish your report. Of course, insurance puts you on hold for 30 minutes and you sit there listening to low-fi classical music (if you’re lucky) twiddling your thumbs. So what to do about this major productivity killer?

Enter **asynchronous programming**: a _concurrent execution_ of tasks. While the insurance agent digs through your records, you wisely decide to begin working on your report thereby providing you a method to complete two high-level functions at once. Of course, this is dependent on the involvement of a third party, the insurance agent. From your perspective, you are still limited to a single train of thought; you talk to the insurance agent, switch to working on your report, and then switch back to the insurance task when you’re taken off of hold. We have simply broken up the _linear and sequential_ execution flow of tasks. This superpower is a type of [concurrency](https://en.wikipedia.org/wiki/Concurrency\_\(computer\_science\)).

The key concept to keep in mind is that concurrency is about _dealing with_ lots of things at once. Parallelism is about _doing_ lots of things at once. So yes, very loosely speaking, you could consider concurrency a broader term that also encompasses parallelism (this is not perfectly accurate but good enough for our mental model). A common saying is _concurrency does not imply parallelism_.

So, while humans may often think and plan in a synchronous fashion, we function asynchronously. Think about how many tasks you actually juggle between when you go out to eat at a restaurant: placing your order, socializing, eating, taking a quick call, responding to a text, etc. You are always _dealing with_ lots of things at once, but _on your own_, you are never actually _doing_ lots of things at once. But once you introduce a third party, functioning asynchronously allows humans to be significantly more productive. We may not be able to parallel compute, but we are still masters of concurrency.

{% hint style="info" %}
**Concurrency vs parallelism**

These are two really tricky concepts to disambiguate, largely due to how similar they are and all the terminology (e.g., processes, threads, tasks, etc.) that can have slightly different meanings in different contexts. If you’re interested in developing a more intuitive understanding, our recommendation is to take a personal deep dive until you find an explanation that clicks. This [stack overflow thread](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism) is a great starting place.
{% endhint %}

To finally move beyond our metaphor, let’s exit the purely conceptual realm and look at some actual code. We’ll be looking at Javascript examples as it is the [single-threaded language](https://medium.com/swlh/what-does-it-mean-by-javascript-is-single-threaded-language-f4130645d8a9) that powers the web and asynchronous programming is core to much of its functionality. It is important to note that the implementation logic in the functions below is _not_ the focus. In fact, it can be a source of confusion. Javascript by design makes it difficult to implement synchronous, blocking code so the functions themselves are a bit hacky. For these examples, just focus on what the functions represent.

```javascript
const simulateSyncWork = function (work, ms) {
  const end = new Date().getTime() + ms;
  while (new Date().getTime() < end) {
    /* do nothing */
  }
  return console.log(`${work} Complete`);
};

console.time("Sync time");

simulateSyncWork("Web API Work", 3000);

simulateSyncWork("Local Work 1", 1000);
simulateSyncWork("Local Work 2", 2000);
simulateSyncWork("Local Work 3", 1000);

setTimeout(() => console.timeEnd("Sync time"), 1);
```

This example is quite simple. We have a set of synchronous function calls that block execution of the main thread for the specified amount of time. The string passed specifies the kind of work being simulated: either a web API call or work being executed locally on the machine. For this synchronous programming example, the difference is negligible. The script executes exactly as you would anticipate, and at the end, returns a total run time of approximately 7 seconds.

```
// Console Output:

// Web API Work Complete
// Local Work 1 Complete
// Local Work 2 Complete
// Local Work 3 Complete
// Sync time: 7001.510986328125 ms
```

For the synchronous call to the web API, the time spent waiting is akin to our initial car insurance metaphor. In essence, the main thread is “twiddling its thumbs” while it waits for a return value from a remote party. Now let’s use the same program but implement an asynchronous call to the _same_ web API.

```javascript
const simulateAsyncWork = function (work, ms) {
  return setTimeout(() => console.log(`${work} Complete`), ms);
};
const simulateSyncWork = function (work, ms) {
  const end = new Date().getTime() + ms;
  while (new Date().getTime() < end) {
    /* do nothing */
  }
  return console.log(`${work} Complete`);
};

console.time("Async time");

simulateAsyncWork("Web API Work", 3000);

simulateSyncWork("Local Work 1", 1000);
simulateSyncWork("Local Work 2", 2000);
simulateSyncWork("Local Work 3", 1000);

setTimeout(() => console.timeEnd("Async time"), 1);
```

Again, the only change is the asynchronous call to the web API. The web API itself has not changed and you can imagine it is a long-running HTTP GET request in both cases. Can you predict the output?

```
// Console Output:

// Local Work 1 Complete
// Local Work 2 Complete
// Local Work 3 Complete
// Web API Work Complete
// Async time: 4002.68212890625 ms
```

Here, the asynchronous implementation of the simulated API call allows the main thread to defer execution and continue working. Once the web API has completed its work, it is added to a task queue for the main thread to return to once the call stack is empty. This is why the asynchronous call to the web API is the last function to return a value, and the overall program completes in approximately 4 seconds instead of 7.

{% hint style="info" %}
**The event loop**

In Javascript, asynchronous programming is possible due to what is known as the event loop. While certainly not necessary for understanding web APIs, the event loop is core to javascript itself and quite interesting to learn about if you have never been exposed before. And we can think of no better introduction than [this video](https://www.youtube.com/watch?v=8aGhZQkoFbQ).
{% endhint %}

While certainly a contrived example, it still effectively illustrates the power of asynchronous programming. However, it is here we must again muddy the waters and remind you, that nothing about the actual web API changed. As previously mentioned, both `simulateSyncWork("Web API Work", 3000)` and `simulateAsyncWork("Web API Work", 3000)` are met to represent a call to the same web API. Just like in our car insurance metaphor, both the synchronous and asynchronous programming examples deal with the same insurance agent. Asynchronous programming just allowed us to change our behavior in response to that agent. Perhaps the graphics below will provide some clarity:

<figure><img src="../.gitbook/assets/IOBound.png" alt=""><figcaption><p>Diagram of synchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

<figure><img src="../.gitbook/assets/Asyncio.png" alt=""><figcaption><p>Diagram of asynchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

All of this is to say that synchronous vs asynchronous programming is a related, but different concept than synchronous vs asynchronous web APIs.

#### **Synchronous vs Asynchronous Programming: Web APIs**

Just like asynchronous programming breaks up the linear, sequential _execution flow_ of a program, an asynchronous web API breaks up the linear, sequential _communication_ between information producers and consumers. This is done by following the event streaming network communication model we introduced earlier as opposed to the request-response model implemented by synchronous APIs.

So if we have asynchronous programming in our tool belt, why should we care enough about asynchronous APIs to potentially uproot our existing implementations and system architectures? First off, it is important to note that like most system architecture decisions, the decision to use asynchronous APIs is context-dependent. There is no one size fits all solution. Secondly, it is quite common to make use of both synchronous and asynchronous APIs in one system.

Now, as for the benefits of asynchronous APIs, they can be numerous in the right application. Remember, we’re no longer talking about a programming paradigm but a communication paradigm. With asynchronous APIs, clients no longer initiate communication beyond expressing initial interest in a data stream. The events themselves, which are simply changes in state, are the first mover. So the pattern is a client subscribes to a particular data stream, a change of state occurs, a broker then delivers this change of state to all subscribed clients, and each client is then responsible for actually processing this data for whatever its particular end use happens to be. Entire systems built around this asynchronous communication style employ what is broadly known as **event-driven architecture** (EDA). Yes, yet another architectural style, but at the system level, instead of the API level.

These benefits may still seem a little abstract. So systems employing event-driven architecture are natively built around asynchronous APIs where the event itself initiates a communication event. Okay, but what does that actually allow you to do? Well, let’s take a closer look at a hypothetical use case. We’ll use the classic example of internet of things (IoT) devices. Say you have an IoT device tracking real-time changes in temperature. Crucially, your system/application needs to know as soon as the lower threshold of 32F/0C degrees is crossed. An HTTP API following the more traditional request-response communication model would need to continuously poll the server hosting the temperature data. However, you could also build out an event-driven architecture around asynchronous APIs, specifically APIs built on the pub/sub architectural style, which would allow a simple subscription to a broker’s temperature _topic_. The broker would immediately push data to all subscribers whenever there is a change in temperature, thereby allowing the subscribers to build their business logic around this data stream and react as soon as the threshold is crossed. The publisher of the temperature data does not need to know or care, how or when the temperature data is being processed.

For similar use cases with a focus on real-time applications, event-driven architecture is a significantly more efficient way to communicate. It also is a completely different way to think about structuring an application’s architecture which can cause a number of challenges both internally and externally when it comes to integration. Although one could make the argument we are moving rapidly towards a more asynchronous world, synchronous APIs are certainly not going anywhere. Most systems will require significant interplay between both categories of APIs.

{% hint style="info" %}
**The curious case of HTTP**

Generally, the HTTP application protocol is thought of and talked about as a synchronous protocol. However, there are different versions of HTTP such as HTTP/1.1, which is currently the most widely employed HTTP version, HTTP/2.0, and HTTP/3.0. HTTP/2.0 enabled functionality like multiplexing that begins to break down the strict request/response model as multiple requests are bundled together and can be returned in any order. This is yet another reminder that these categories and distinctions are not always perfectly clear. If you’re interested in digging further into the history and future of HTTP, [this is a great starter resource](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics\_of\_HTTP/Evolution\_of\_HTTP).
{% endhint %}

#### **Synchronous vs Asynchronous: Reactive Programming**

At this point, we would be surprised if you did not have trouble clearly differentiating all these overlapping terms. You have protocols everywhere. You have architectural styles at the API and system level. You have sync and async APIs as well as sync and async programming. Let’s take a quick step back, and walk through the core points in a nice, clean list:

1. First, we discussed a shift from monolithic applications to microservices. This was all about decoupling application components and interfacing through web APIs. Generally, these web APIs were initially synchronous and adhered tightly to the request-response network communication model.
2. However, just because these components talked synchronously, does not mean the actual execution flow of our applications had to be synchronous. This is why a single-threaded language like Javascript is an inherently asynchronous programming language. Since it powers the web, the main execution thread could not afford to be blocked whenever it needed to communicate synchronously through a web API.
3. Next, we said let's take things a step further and also enable asynchronous communication that decouples information producers from information consumers. This shift enables powerful functionality but also requires a restructuring of your application logic from the backend to the UI. It’s an entirely different system architectural style referred to as event-driven architecture.

Now, as you might be imagining, implementing event-driven architecture is easier said than done. It’s a whole different way of thinking. And it’s a way of thinking that does _not_ come naturally to our brains that like to plan in a linear, synchronous fashion. It’s much easier to reason about code that progresses sequentially from top to bottom.

This is why to implement EDA at the component or service level, programmers typically make use of a programming style known as **reactive programming**. Reactive programming is all about making **asynchronous data streams the spine** of your application. Events are now the _main orchestrators of your application’s flow_. The reactive programmer manages the logic around manipulating and performing operations on the data streams.

Okay, so the data streams drive the flow and the programmer builds the business logic which can be seen as the _reaction to the event_. But what superpowers does this approach unlock? Well, in large, it’s about the transition to **stream processing**.

Traditionally, message processing worked with **queues** and was about applying simple computations to individual, or sometimes batches of, messages. This approach quickly runs into some limitations when looking at a distributed streaming system like [Kafka](https://www.confluent.io/what-is-apache-kafka/). Kafka stores an ordered sequence of events in a data structure known as a **log** and refers to them as **topics**. Unlike traditional messaging queues, topics also allow you to pull historical event data. This quickly opens the door to a massive amount of input streams that can be joined, aggregated, filtered, etc. This is stream processing. It’s less about the data being real-time and more about the complex processing applied across an array of input streams.

{% hint style="info" %}
**Detailed introduction to reactive programming**

This was a very high-level overview of reactive programming. Mostly because an entire guide could be written about just this topic. Luckily, Andre Medeiros already did! [This guide](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754) is an excellent introduction to reactive programming for those looking to take a deeper dive.
{% endhint %}

### Stateful vs Stateless Web APIs <a href="#stateful-vs-stateless-web-apis-13" id="stateful-vs-stateless-web-apis-13"></a>

Okay, just one more categorization to tackle. Typically, synchronous APIs are presented as being synonymous with stateless APIs while asynchronous APIs are seen as being synonymous with stateful APIs. This is not always the case. But first, let’s define what we mean by stateless vs stateful.

The stateless vs stateful label is all about the perspective of the server/broker. A stateless API means the server does not store any information about the client making the request. In other words, the **session** is stored on the client where the session is an encapsulation of a particular client and server interaction. Each client request is self-contained and provides all the information that the server needs to respond including any necessary authentication tokens. The independent nature of each request is core to any stateless API.

As previously detailed, an API implemented following the REST architecture should always be stateless. But the very fact that this architectural constraint exists should be providing you a strong signal that statelessness is in no way inherent to synchronous APIs.

Many early web applications were built on stateful, synchronous APIs. They are generally easier to build and therefore, cut back on costs. There is also nothing inherently wrong with this approach, even for modern web applications, at smaller scales. However, when a single server can no longer handle the load, you quickly start running into issues. Every request from a client needs to be routed to the server that is currently storing that particular client’s session data, or you need a method to share session data between all of your servers. This limitation on the horizontal scaling of an application’s server-side infrastructure is a major driver of the popularity of REST and REST-like APIs.

Now, looking at asynchronous APIs, in the pub/sub pattern the broker is responsible for pushing data to any subscribers; therefore, the broker must maintain the session data and is inherently stateful. This is why asynchronous APIs are almost always referred to as stateful.

It is important to note, however, that even these waters can be muddied. [Pulsar](https://pulsar.apache.org/docs/2.10.x/concepts-overview/) is another messaging platform that implements a two-layer architecture resulting in a [stateless layer of brokers](https://pulsar.apache.org/docs/2.10.x/concepts-architecture-overview/#brokers) and a stateful persistence layer. But we’ll save that deep dive for another day. For now, just remember that state is always being persisted somewhere, and stateful vs stateless is just about _where the state is stored_.
