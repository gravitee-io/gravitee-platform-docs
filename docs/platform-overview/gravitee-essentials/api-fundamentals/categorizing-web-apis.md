# Categorizing Web APIs

Web APIs are categorized as synchronous or asynchronous and stateless or stateful. Although they can be differentiated into separate categorizations, these concepts are often subject to cross-pollination. Their respective details and relationships are further explored below in [asynchronous vs asynchronous](categorizing-web-apis.md#synchronous-vs-asynchronous-9) and [stateful vs stateless web APIs](categorizing-web-apis.md#stateful-vs-stateless-web-apis-13).

### Synchronous vs Asynchronous <a href="#synchronous-vs-asynchronous-9" id="synchronous-vs-asynchronous-9"></a>

Synchronous (sync) vs asynchronous (async) web APIs represent a demarcation and paradigm shift in API communication consequent to event streaming complementing the request-response network communication model. The following sections broadly introduce synchronous and asynchronous patterns before applying these concepts to web APIs.

#### **Synchronous vs Asynchronous: Programming**

Synchronous programming is the linear, sequential execution of tasks, where the completion of each task blocks the start of the following task. Asynchronous programming is the concurrent execution of tasks, where tasks can be performed partially or totally out of order. Multitasking, or rapid task-switching, is not equivalent to [parallelism](https://en.wikipedia.org/wiki/Parallel\_computing), which computer science defines as the simultaneous execution of two or more tasks. Concurrency does not imply parallelism, as managing multiple tasks simultaneously is different from performing multiple tasks simultaneously. Although the high-level differentiator is clear-cut, it can be difficult to [disambiguate concurrency and parallelism](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism) due to functional overlap and contextual terminology.

Javascript is chosen for the following examples because it is the [single-threaded language](https://medium.com/swlh/what-does-it-mean-by-javascript-is-single-threaded-language-f4130645d8a9) that powers the web and asynchronous programming is core to much of its functionality. It is important to note that the implementation logic in the functions below is _not_ the focus. In fact, it can be a source of confusion. Javascript by design makes it difficult to implement synchronous, blocking code so the functions themselves are a bit hacky. For these examples, just focus on what the functions represent.

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

<figure><img src="../../.gitbook/assets/IOBound.png" alt=""><figcaption><p>Diagram of synchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Asyncio.png" alt=""><figcaption><p>Diagram of asynchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

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
