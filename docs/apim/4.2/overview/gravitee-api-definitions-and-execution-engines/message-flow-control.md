# Message Flow Control

## Overview

Gravitee APIM Gateway allows events to be consumed or produced from or to a variety of brokers such as Kafka, MQTT5, and Solace. In addition, the Gateway can dynamically apply a flow control mechanism to manage slow consumers and avoid becoming overwhelmed.

The following sections discuss both generalized flow control concepts and Gravitee's implementation.

* [What is flow control?](message-flow-control.md#what-is-flow-control)
* [Flow control in Gravitee APIM Gateway](message-flow-control.md#flow-control-in-gravitee-apim-gateway)
* [Flow control over the network](message-flow-control.md#flow-control-over-the-network)
* [Gateway TCP flow control](message-flow-control.md#gateway-tcp-flow-control)
* [Quality of Service](message-flow-control.md#quality-of-service)
* [Flow control in action](message-flow-control.md#flow-control-in-action)

## What is flow control?

At one end of an event-native communication channel is a subscriber, and at the other, a publisher. These are not required to employ the same message processing capabilities. For example, the diagram below shows a publisher that can produce more elements than the subscriber can process.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/EnYu-G1xgfxjnIPeqDYjW08G.png" alt=""><figcaption><p>Faster publisher</p></figcaption></figure>

In this situation, the subscriber can become overwhelmed if it is unable to process the flow of elements quickly enough. Worst case, memory issues will cause it to crash.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/_sDO4uk4LxRTUzVt8ZhsKXTj.png" alt=""><figcaption><p>Subscriber overflow error</p></figcaption></figure>

Flow control provides a standardized way for the subscriber to dynamically ask the publisher to adapt the flow of elements. In the diagram below, a slow subscriber requests the exact amount of elements it can process. The publisher is aware of this request and adapts the volume of elements produced.

{% hint style="info" %}
The concept of flow control originates with the Reactive Foundation. Flow control is implemented by many libraries, including `RxJava`, which is the basis for the Gravitee Gateway.
{% endhint %}

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/E0BAD8zoCKHTwBmzeMK6jZfB.png" alt=""><figcaption><p>Subscriber request</p></figcaption></figure>

## Flow control in Gravitee APIM Gateway

Gravitee terminology refers to the entrypoint and the endpoint of an API. These act as the subscriber and publisher, respectively. The Gravitee APIM Gateway employs a flow control mechanism so that the endpoint can adapt the volume of messages produced to the amount requested by the entrypoint. [For example](message-flow-control.md#flow-control-in-action), this is implemented when an API consumer calls an API exposing an SSE entrypoint to consume messages from a Kafka endpoint.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/isYWmsCnn0-yl84wke5wcq_T.png" alt=""><figcaption><p>Gateway internal flow control</p></figcaption></figure>

## Flow control over the network

The `RxJava` library allows flow control to operate internally in the Gateway, but the Gateway also needs to manage flow control with the end-user application.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/5avybcxjjeVD4kvENMyfgT5V.png" alt=""><figcaption><p>Flow control over the network</p></figcaption></figure>

This is possible using the TCP layer of the network model, where TCP stores the data it needs to send in the _send buffer_ and the data it receives in the _receive buffer_. When the application is ready, it reads data from the receive buffer.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/DFKJw2dO2pnypqTfItns_8Ic.png" alt=""><figcaption><p>End-user application flow control via TCP</p></figcaption></figure>

TCP flow control consists of ensuring an application doesn’t send additional packets when the receive buffer is full (i.e., the receiver is not able to handle them).&#x20;

The TCP protocol allows for transmitting the receive window, which corresponds to the free space remaining in the receive buffer, to notify the sender. The sender is then able to adapt the flow.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/bozgHpk1hSAywC9sGFKwVOpS.png" alt=""><figcaption><p>Receive window</p></figcaption></figure>

## Gateway TCP flow control

The Gateway's internal, `RxJava`-based implementation of flow control and the TCP protocol's flow control mechanism must combine to provide flow control between the Gravitee APIM Gateway and the end-user application.

To achieve this, the APIM Gateway uses Vertx, which provides seamless integration with `RxJava` at the network level. When the TCP layer advertises that the receive window has fallen to 0, the I/O socket is considered to be not writable. This has an immediate impact on the amount of elements requested from the endpoint.

{% hint style="info" %}
This is a simplified explanation of what occurs at the TCP level. In reality, how TCP decides to send additional packets is more complex and involves sliding windows.
{% endhint %}

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/klohIwWYtwgpfPKy0EojPQw6.png" alt=""><figcaption><p>Complete flow control</p></figcaption></figure>

## Quality of Service

Quality Of Service (QoS) depends on how the client application handles message acknowledgment. Message acknowledgment over HTTP is not possible, but Gravitee offers a certain level of QoS based on the entrypoint:

* **None**: Allows for high throughput and good performance, but does not guarantee delivery.
* **Auto (0 or N)**: Any message can be delivered zero, one, or multiple times. This offers a trade-off between performance and guaranteed delivery.
* **At-Most-Once (0 or 1)**: Any message can be delivered zero times or once without any duplication.
* **At-Least-Once (1 or N)**: Any message is delivered once or more than once.

For example, if an application using SSE slows down until it crashes, the messages pending in the TCP stack will not be redelivered when the application reconnects, but using an appropriate QoS can provide flexibility:

* **SSE with Kafka:** At-Least-Once can be configured to provide the latest message ID (HTTP header `Last-Event-ID`) to restart consumption when the API is called again.
* **HTTP GET with Kafka:** At-Least-Once can be configured to use a `cursor` query parameter to restart consumption when the API is called again.

## Flow control in action

To explore flow control, we can create a v4 message API with a Kafka endpoint and an SSE entrypoint. Next, to simulate a client application that consumes the SSE API very slowly, we will use the `curl` command and pause it after a few seconds to observe what happens on the network using `Wireshark`. At the same time, we will check the APIM Gateway heap to verify that messages are not stacked in memory and the flow control has paused message consumption.

{% hint style="info" %}
A Mock endpoint and/or WebSocket entrypoint can be used in lieu of Kafka and/or SSE.
{% endhint %}

### Setup

1. Import [this SSE-Kafka API](https://slabstatic.com/prod/uploads/6lql0jy7/posts/attachments/uHCG\_mgqWRBdrJZzGWfg7gSv.json) into your local running APIM instance and deploy it.
2. Start feeding your Kafka topic (e.g., `topic-users`) via the following script:

```yaml
import json
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         ssl_check_hostname=True,
                         security_protocol='PLAINTEXT',
                         bootstrap_servers='localhost:9092'
                         )

id=0
while True:
	id+=1
	producer.send('topic-users', key=bytes(str(uuid.uuid4()), 'utf-8'), value={
	    "id": id,
	    "message": "Hello"
	})
	producer.flush()
```

3. Run the following curl command to call your SSE API:

```yaml
curl -H "Accept: text/event-stream" http://localhost:8082/sse-kafka

event: message
data: {"id": 1, "message": "Hello"}

event: message
data: {"id": 2, "message": "Hello"}

event: message
data: {"id": 3, "message": "Hello"}

...
```

### Look at the network

1. Run Wireshark and start capturing the local network (Loopback: lo0). In this example, we want to filter the Gateway traffic by applying the following filter:

```yaml
tcp.port == 8082 && ip.addr == 127.0.0.1 && http
```

2. Restart the SSE curl command above to see it appear in Wireshark.&#x20;

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/5yxioH7jsvNMC3ZEWmRv6c7K.png" alt=""><figcaption></figcaption></figure>

3. Follow the HTTP stream to view the TCP packets exchanged. Wireshark shows every TCP packet, so pay attention to the current window size!

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/KXYST4VJ9NyRoyqdq9nQvS0q.png" alt=""><figcaption></figcaption></figure>

4. Pause the curl command by typing `CTRL+Z`. In the span of a few seconds, the window size will decrease until it reaches 0.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/xmzt-p6tSU3PiId5i5z2N6II.png" alt=""><figcaption></figcaption></figure>

### Look at the Gateway memory

1. We can use Visual VM to view the current APIM Gateway memory. The consumption of the messages should have stopped since the curl command is  paused.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/gnXYThJ_vcyWrl-KB4RJ4l7N.png" alt=""><figcaption></figcaption></figure>

2. Internally, the Gateway creates a `DefaultMessage` instance for each Kafka message it receives. We can make several Heap Dumps to verify that the number of message instances in memory remains unchanged.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/2GSgj5iVDHEqcQge9oS2MOLK.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The Gateway applied a flow control and stopped consuming Kafka messages while the consumer application could not process the flow of messages.
{% endhint %}
