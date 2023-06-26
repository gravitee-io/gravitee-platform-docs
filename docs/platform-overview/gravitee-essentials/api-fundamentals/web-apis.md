# Web APIs

To further clarify web API structure and functionality, this section addresses:

* [Internet vs world wide web](web-apis.md#internet-vs-world-wide-web)
* [shift to microservices](web-apis.md#shift-to-microservices)
* [API protocols](web-apis.md#protocols-4)
* [API architectures/patterns](web-apis.md#architectural-stylespatterns-5)
* [API specifications](web-apis.md#specifications-6)
* [Data-interchange formats](web-apis.md#data-interchange-formats-7)

## Internet vs world wide web

A web API is an API that is accessible over a network. Although the type of network is not specified, common usage of "web API" presumes the combination of the internet and the world wide web.

The internet is the [physically interconnected](https://theconversation.com/in-our-wi-fi-world-the-internet-still-depends-on-undersea-cables-49936) global network of computers along which information travels. Much of this information is in the form of hypermedia (e.g., web pages) and organized in a construct known as the world wide web, which is essentially an application running on the internet infrastructure. However, the world wide web, or web, is only one way to access or manage information on the internet. For example, Voice over Internet Protocol (VoIP) enables calls over the internet without interacting with the web.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5b31e8183ce2abee47d7194607538270bde34bc3_2_690x492.png" alt=""><figcaption><p>Photo of the underwater cables connecting the internet from this <a href="https://www.weforum.org/agenda/2015/11/how-can-we-protect-the-internets-undersea-cables/">blog</a></p></figcaption></figure>

{% hint style="info" %}
For a quick history lesson and a bit more detail about the relationship between the internet and the world wide web, [watch this excellent video](https://www.youtube.com/watch?v=eHp1l73ztB8\&t=189s).
{% endhint %}

## Shift to microservices

The popularity of web APIs is largely due to the [shift from monolithic applications to microservices](https://www.gravitee.io/blog/what-are-microservices-how-do-they-enhance-web-applications). To summarize, microservices are replacing monoliths because not all aspects of a project scale in parallel. Microservices enable cloud-native applications through the functional separation and independent scaling of each runtime, and web APIs establish standardized contracts for network interfacing and provide distributed architectures with reliable communication.

The underlying framework powering web APIs is quite complicated. Web APIs rely on communication protocols to deliver information to intended recipients, and network data must be serialized into data-interchange format for transport. In addition, API design and documentation should adhere to both an architecture and a specification.&#x20;

API protocols, data-interchange formats, architectures, and specifications are often insufficiently defined and differentiated. For example, the REST architectural style is inaccurately used as a proxy for the HTTP application layer protocol. The following sections offer high-level clarifications.

## Protocols <a href="#protocols-4" id="protocols-4"></a>

APIs are categorized by their architectural style or the application layer protocol they use to communicate over the network (e.g., an HTTP API). Protocol terminology is based on the [layered networking model](https://www.quora.com/What-is-the-difference-between-HTTP-protocol-and-TCP-protocol/answer/Daniel-Miller-7?srid=nZLo), which conceptualizes communication within and between computers at different abstractions and with respect to different functionality. The transport layer and the application layer contain the protocols most relevant to APIs.&#x20;

### Transport layer

The two most widely used transport layer protocols are the user datagram protocol (UDP) and the transmission control protocol (TCP) which both support [packet-based messaging.](https://www.cloudflare.com/learning/network-layer/what-is-a-packet/) The main differentiator is that UDP is more lightweight at the expense of error checking and does not guarantee packet integrity, delivery, or order of delivery. UDP is suitable if data loss results in minor artifacts (e.g., real-time video calls) but not for use cases that demand high accuracy (e.g., routing banking information).

The need for accurate and reliable data factors heavily into why many application layer protocols are built on top of TCP. TCP provides robust error checking to ensure packets are not lost, corrupted, duplicated, or delivered out of order.

### Application layer

The application layer is the top layer of the layered network model and contains many recognizable protocols, such as those shown in the table below. Protocol network communication is either synchronous or asynchronous and can differ between versions of the same protocol.

<table><thead><tr><th width="347">Name</th><th width="135">Abbreviation</th><th>Communication Type</th></tr></thead><tbody><tr><td>Hypertext Transfer Protocol</td><td>HTTP</td><td>Sync/Async</td></tr><tr><td>Hypertext Transfer Protocol Secure</td><td>HTTPS</td><td>Sync/Async</td></tr><tr><td>Websocket</td><td>N/a</td><td>Async</td></tr><tr><td>Server Sent Events</td><td>SSE</td><td>Async</td></tr><tr><td>File Transfer Protocol</td><td>FTP</td><td>Sync</td></tr><tr><td>Message Queuing Telemetry Transport</td><td>MQTT</td><td>Async</td></tr><tr><td>Advanced Message Queuing Transport</td><td>AMQP</td><td>Async</td></tr><tr><td>Kafka’s Custom Binary Protocol</td><td>N/a</td><td>Async</td></tr><tr><td>Google Remote Procedure Call</td><td>gRPC</td><td>Sync/Async </td></tr><tr><td>Simple Object Access Protocol</td><td>SOAP</td><td>Sync/Async </td></tr><tr><td>Simple Mail Transfer Protocol</td><td>SMTP</td><td>Sync</td></tr><tr><td>Domain Name Service</td><td>DNS</td><td>Sync/Async </td></tr><tr><td>Extensible Messaging and Presence Protocol</td><td>XMPP</td><td>Async</td></tr></tbody></table>

{% hint style="info" %}
**Is Webhook an application layer protocol?**

"Webhook API" is a misnomer. APIs are often categorized by the application layer protocol they employ, but although Webhook uses HTTP, it is not an application layer protocol itself. Compounding this misconception, Webhooks are not APIs. Webhooks are essentially functionality that can be added to existing APIs, as explained in [this excerpt](https://www.redhat.com/en/topics/automation/what-is-a-webhook):

> “Webhooks are often referred to as reverse APIs or push APIs, because they put the responsibility of communication on the server, rather than the client. Instead of the client sending HTTP requests—asking for data until the server responds—the server sends the client a single HTTP POST request as soon as the data is available. Despite their nicknames, webhooks are not APIs; they work together. An application must have an API to use a webhook.”
{% endhint %}

Application layer protocols define how independent programs and services communicate over networks and share information. While the other protocol layers focus on delivering data to a destination, the application layer protocols are responsible for establishing communication standards that dictate how that data is accessed and consumed. Specifically, the application layer provides the programs at each end of a communication link with interface methods to ensure that the request and response are understood and managed correctly. The role the application layer plays in defining interface conventions explains why an API type and its protocol are often synonymous.

### A working example

Modern web browsers are applications that communicate over the HTTP/HTTPS protocol (HTTPS is HTTP with encryption and verification) but often truncate the visible website address to omit the protocol and subdomain. This is evidenced by visiting a site such as [Google](https://google.com/) and double-clicking the URL.

<div>

<figure><img src="../../.gitbook/assets/google_shortened.png" alt=""><figcaption><p>Shortened URL</p></figcaption></figure>

 

<figure><img src="../../.gitbook/assets/google_expanded.png" alt=""><figcaption><p>Expanded URL</p></figcaption></figure>

</div>

The graphic below clarifies the structure and individual components of a web address, which concatenate to form the broader uniform resource locator (URL), uniform resource identifier (URI), and uniform resource name (URN).

<figure><img src="../../.gitbook/assets/uri_diagram1.png" alt=""><figcaption><p><a href="https://hanseul-lee.github.io/2020/12/24/20-12-24-URL/">URI vs URL vs URN</a></p></figcaption></figure>

A communication link between two applications requires that each endpoint is defined by a network socket, which is a combination of transport layer protocol, domain (which resolves to an IP address), and port number that uniquely and completely resolves the web address of a client request to a web server.

{% hint style="info" %}
Web browsers communicate over HTTP, which is built on top of TCP, so the transport layer protocol is assumed. However, this will be [changing with HTTP/3](https://www.cloudflare.com/learning/performance/what-is-http3/), which is built on top of UDP.
{% endhint %}

When `google.com` is typed in a web browser, it is expanded to `https://www.google.com:443`, where `www.google.com` is the fully qualified domain name that is resolved into an IP address through [domain name system (DNS) resolution](https://serverfault.com/questions/643506/how-does-the-http-get-method-work-in-relation-to-dns-protocol/643511#643511) and 443 is the port reserved for HTTPS on every network (port 80 is reserved for HTTP). The browser’s request is directed to Google’s web server using the HTTPS application layer protocol, in particular the GET [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods), and Google’s web server interprets the request and responds with the Google homepage.&#x20;

HTTP includes standard status codes to qualify the state of every network communication. For example, if the requested [resource](https://restful-api-design.readthedocs.io/en/latest/resources.html) does not exist, Google’s web server will respond with a 404.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5243c9b089b8754b37695dedcf1450bace820b90_2_690x262.png" alt=""><figcaption><p>HTTPS error response example</p></figcaption></figure>

### Endpoints

The route portion of a URL combined with an HTTP method constitutes an HTTP API endpoint, and each resource is accessible through a unique endpoint. For example, `GET http://foo.com/api/user/1` and `GET http://foo.com/api/user/2` contain different routes and correspond to distinct resources. `GET http://foo.com/api/user/1` and `POST http://foo.com/api/user/1` are also considered unique endpoints due to the change in HTTP method.

In this example, all resources, and all therefore endpoints tied to this API, exist under a single API entry point of `http://foo.com/api`. The entry point can be viewed as a special type of endpoint: as the gateway to the API, it’s a resource that exists outside of any other collection and contains all other collections of resources.

Path parameters allow variable values to be passed along the URL path of a request. In a typical API route, the path is divided into segments separated by slashes ("/"). Path parameters are denoted by a placeholder or variable name within curly braces ("{}"). When a request is made, the actual value for the parameter is substituted in place of the placeholder. The above example could represent an endpoint as `GET http://foo.com/api/user/{id}` where {id} is the path parameter.

### Protocol types

Despite sitting at the same layer of the networking model, application layer protocols can be dependent on one another, and many depend on HTTP/HTTPS. For example, SOAP effectively tunnels over HTTP, which is a strategy employed by many protocols, including modern asynchronous protocols like WebSocket.

{% hint style="info" %}
To clarify, the WebSocket protocol [handshake](https://www.baeldung.com/cs/handshakes) uses HTTP, but HTTP is not involved past that point. Learn more about this distinction [here](https://stackoverflow.com/a/47085864).
{% endhint %}

Although SOAP can be designed to function over raw TCP, HTTP leverages the existing web ecosystem and offers advantages. HTTP is fundamental to web communication and there has been substantial, global investment in server and client-side infrastructure (i.e., web browsers) designed around HTTP/HTTPS. In addition, security provisions such as firewalls tend to admit network traffic targeted for ports 80/443, meaning that applications built on HTTP are much more likely to work out of the box.

Networks, including the internet, support many application layer protocols that are in no way tied to HTTP. Most of the other application layer protocols relevant to this guide are built on top of raw TCP. For example, [Kafka implements a custom binary application protocol over TCP](https://kafka.apache.org/protocol.html) due to performance concerns when using HTTP to deliver massive amounts of real-time data.

To summarize, APIs depend on many protocols. The ideal protocol stack, just like the ideal application stack, is completely context-dependent and subject to considerations such as application environment, security concerns, payload, network quality, etc.

## Architectural styles/patterns <a href="#architectural-stylespatterns-5" id="architectural-stylespatterns-5"></a>

Web API architectural styles are completely separate from the underlying protocols that power APIs. The architectures focus on guiding API design, to which both developers and business logic stakeholders actively contribute.

{% hint style="info" %}
Design-first methodology, which is [an API development technique with purported benefits](https://www.gravitee.io/api-first), attempts to satisfy both technical criteria and business interests and is [recommended by the OpenAPI initiative](https://learn.openapis.org/best-practices.html#use-a-design-first-approach).
{% endhint %}

### REST

Although popular usage of "REST API" might imply that REST is a web API protocol, it is actually an architectural style that stands for “representational state transfer." REST APIs employ the HTTP application protocol (a practical implementation rather than an explicit REST requirement) and must adhere to six [design principles](https://www.ibm.com/topics/rest-apis): uniform interface, client-server decoupling, statelessness, cacheability, layered system architecture, and (optional) code on demand.&#x20;

{% hint style="info" %}
Many APIs that claim to be REST APIs, or RESTful, are not fully compliant with REST architecture and are more accurately referred to as REST-like.
{% endhint %}

REST APIs and their associated architectural constraints originated with Roy Fielding's iconic Ph.D. dissertation “Architectural Styles and the Design of Network-based Software Architectures.” Their explosion in popularity is due to many factors, in particular that [statelessness enables scalability](https://www.metaswitch.com/blog/how-stateless-processing-enables-massive-scalability) and fault tolerance. The request of each completely independent request-response cycle can be handled by an arbitrary server instance and unlocks essentially limitless horizontal scaling.

The structure of REST APIs forms the basis of their uniform interface by requiring that each resource is identified by a single URL and that the actions on that resource are managed by HTTP verbs (GET, POST, etc.), request headers, and the request body. For each client request, the server modifies the resource, if requested, then transfers a representation of the state of the resource back to the client, hence the designation "representational state transfer." Statelessness ensures that each request contains all of the information necessary for it to be processed without relying on a session state stored by the server.

### RPC

Another major architectural style that predates REST is the remote procedure call, or RPC. RPC-based APIs utilize several different application layer protocols such as HTTP, SOAP, and gRPC. The main differentiator between REST and RPC is that REST URLs are resource-centric (`http://foo/user/1`) while RPC URLs are action-centric (`http://foo/getUser`). A remote procedure call essentially calls a function the chosen programming language remotely, or over a network.

Unlike REST, RPC architecture does not clearly designate a set of constraints. Both REST and RPC are architectural styles and real-world implementations don’t often fully align with either. This has led to implementations such as GraphQL (an architectural style, an API [query language](https://www.techopedia.com/definition/3948/query-language), and a runtime for fulfilling those queries) which proponents describe as essentially RPC, but borrowing heavily from the REST community.

{% hint style="info" %}
Deep-dive [REST vs RPC](https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/) via implementation examples that highlight the strengths and weaknesses of both styles.
{% endhint %}

### Network communication models

In general, an API implemented with a REST, RPC, or a GraphQL architectural style executes synchronous network communication via the request-response model, where the client computer makes a request directly to the server computer and the server responds by returning data or a service. While the client and server applications are decoupled and function independently, synchronous communication is inherently tightly coupled.

The request-response model was instrumental in the development of the modern web and  has dominated network communication until recently, when an asynchronous network communication model known as event streaming, or message streaming, rose to prominence. In this context, an event is any change in the state of a resource. In the event streaming model, clients publish messages to or subscribe to receive messages from a computer known as the event broker.

One popular architectural style that implements event streaming is the publish/subscribe (pub/sub) pattern. Similar to RPC, it is fairly generalized without many rigid architectural constraints. The core tenet of the pub/sub pattern is that communication between information producers, or publishers, must be decoupled from information consumers, or subscribers, through the event broker. Consequently, publishers and subscribers are not aware of one another. This loose coupling greatly simplifies communication (i.e., the publisher has a single target, the broker) which enables the design of more scalable and flexible event-driven systems. APIs following the pub/sub pattern utilize many different application layer protocols such as MQTT, AMQP, and the Kafka custom binary protocol.

{% hint style="info" %}
**Events vs messages**

Although often used synonymously, there is a distinction between an event and a message. This guide adopts the high-level disambiguation that a message is the directed carrier of an event while the event is the actual change in observable state, but there is a [deeper technical distinction](https://developer.lightbend.com/docs/akka-guide/concepts/message-driven-event-driven.html).
{% endhint %}

## Specifications <a href="#specifications-6" id="specifications-6"></a>

The architectural styles that govern the client-server interactions do not dictate API usage such as available endpoints, permissible actions, authentication options, parameters to pass, etc. Documentation of this information must be clear, intuitive, comprehensive, and updated with bug fix or iteration. API specifications such as OpenAPI alleviate the overhead associated with documentation by providing a template.



for all users of your API. And after documenting several APIs, you would begin to realize how repetitive the process of API documentation can become. On top of that, you would quickly realize how difficult it is to ensure your documentation has 100%, comprehensive coverage of your API. Finally, even if you manage to pull this off, your work is never truly complete as the documentation must be updated with every change and bug fix associated with your API. Keeping this from becoming a massive migraine is where API specifications come in. Let’s start with the OpenAPI specification defined below:

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

## Data-interchange formats <a href="#data-interchange-formats-7" id="data-interchange-formats-7"></a>

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

## Categ <a href="#categorizing-web-apis-8" id="categorizing-web-apis-8"></a>
