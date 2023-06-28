# Categorizing Web APIs

Web APIs are categorized as synchronous or asynchronous and stateless or stateful. Although they can be differentiated into separate categorizations, these concepts are often subject to cross-pollination. Their respective details and relationships are further explored below in [asynchronous vs asynchronous](categorizing-web-apis.md#synchronous-vs-asynchronous-9) and [stateful vs stateless web APIs](categorizing-web-apis.md#stateful-vs-stateless-web-apis-13).

## Synchronous vs Asynchronous <a href="#synchronous-vs-asynchronous-9" id="synchronous-vs-asynchronous-9"></a>

Synchronous (sync) vs asynchronous (async) web APIs represent a demarcation and paradigm shift in API communication consequent to event streaming complementing the request-response network communication model. The following sections broadly introduce synchronous and asynchronous patterns before applying these concepts to web APIs.

### **Sync vs async programming**

Synchronous programming is the linear, sequential execution of tasks, where the completion of each task blocks the start of the following task. Asynchronous programming is the concurrent execution of tasks, where tasks can be performed partially or totally out of order but rapid task-switching (multitasking) is not equivalent to [parallelism](https://en.wikipedia.org/wiki/Parallel\_computing), which is the simultaneous execution of two or more tasks. Concurrency does not imply parallelism, as managing multiple tasks simultaneously is different from performing multiple tasks simultaneously. Although the high-level differentiator is clear-cut, it can be difficult to [disambiguate concurrency and parallelism](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism) due to functional overlap and contextual terminology.

The following functions demonstrate sync vs async programming at the expense of implementation logic. By design, Javascript inhibits synchronous, blocking code, but it's used for the examples below because it is the [single-threaded language](https://medium.com/swlh/what-does-it-mean-by-javascript-is-single-threaded-language-f4130645d8a9) that powers the web and asynchronous programming is core to much of its functionality.&#x20;

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

This simple example sets synchronous function calls that block execution of the main thread for specified durations. the passed string indicates either a web API call or actions executed locally and the script returns a total run time of approximately 7 seconds.

```
// Console Output:

// Web API Work Complete
// Local Work 1 Complete
// Local Work 2 Complete
// Local Work 3 Complete
// Sync time: 7001.510986328125 ms
```

The synchronous call to the web API requires the main thread to wait for a return value from a remote party. The following code modifies the same program to implement an asynchronous call to the same web API.

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

Changing the synchronous web API call to an asynchronous API call reduces the total run time to approximately 4 seconds.

```
// Console Output:

// Local Work 1 Complete
// Local Work 2 Complete
// Local Work 3 Complete
// Web API Work Complete
// Async time: 4002.68212890625 ms
```

The asynchronous implementation of the simulated API call allows the main thread to defer execution and continue with subsequent tasks. Once the web API has completed its work, it is added to a task queue for the main thread to return to once the call stack is empty. This is why the asynchronous call to the web API is the last function to return a value, and the overall program completes in approximately 4 seconds instead of 7.

{% hint style="info" %}
Core to Javascript, [event loop](https://www.youtube.com/watch?v=8aGhZQkoFbQ) functionality enables asynchronous programming.
{% endhint %}

Though contrived, the above example effectively illustrates the power of asynchronous programming. Both `simulateSyncWork("Web API Work", 3000)` and `simulateAsyncWork("Web API Work", 3000)` represent calls to the same web API, but asynchronous programming enabled a change in response as further clarified by the following graphics.

<figure><img src="../../.gitbook/assets/IOBound.png" alt=""><figcaption><p>Diagram of synchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Asyncio.png" alt=""><figcaption><p>Diagram of asynchronous calls to a web API from <a href="https://realpython.com/python-concurrency/">blog</a></p></figcaption></figure>

### **Sync vs async web APIs**

The concepts of sync vs async programming and sync vs async APIs are related. Just like asynchronous programming breaks up the linear, sequential execution flow of a program, an asynchronous web API breaks up the linear, sequential communication between information producers and consumers. This is achieved via the event streaming network communication model.&#x20;

Asynchronous API clients do not initiate communication beyond expressing initial interest in a data stream. Instead, communication is triggered by events, which are changes in state. In async communication, a client subscribes to a particular data stream, a change of state occurs, a broker delivers this change of state to all subscribed clients, and each client processes the data for a particular end use. Entire systems built around this flow employ what is broadly termed event-driven architecture (EDA). EDA is an architectural style that exists at the system level instead of the API level.

To demonstrate the benefits of EDA, consider an example use case where an IoT device tracks real-time temperature changes. Assuming an application must be alerted immediately if the temperature falls below 32F/0C degrees, an HTTP API adhering to the request-response model would need to continuously poll the server hosting the temperature data. Alternatively, an event-driven architecture built around asynchronous APIs following the pub/sub architectural style would allow a subscription to the broker’s temperature topic. For each temperature change, the broker would instantly push data to the topic, allowing subscribers to develop business logic around the data stream and react to threshold crossings. The publisher of the temperature data would not need to be aware of how or when the data is processed.

For use cases that focus on real-time applications, event-driven architecture and asynchronous APIs enable communication that is significantly more efficient. EDA is a novel way to structure an application and can lead to both internal and external integration challenges. The decision to use async communication is context-dependent and a single system often leverages both synchronous and asynchronous APIs.&#x20;

{% hint style="info" %}
Generally, the HTTP application protocol is conceptualized and discussed as a synchronous protocol. However, there are different versions of HTTP such as HTTP/1.1 (currently the most widely used version), HTTP/2.0, and HTTP/3.0. HTTP/2.0 functionality like multiplexing begins to break down the strict request/response model because multiple requests can be bundled together returned in any order. The [evolution of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics\_of\_HTTP/Evolution\_of\_HTTP) serves to caution against oversimplifying protocol classifications.
{% endhint %}

### **Sync vs async reactive programming**

To implement EDA at the component or service level, programmers typically employ a technique known as reactive programming, where events are the main orchestrators of application flow and program logic is built around asynchronous communication to manipulate operate on data streams. This reactive approach is a transition to stream processing.



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
