# Integrations

Gravitee Alert Engine works both within and outside the Gravitee ecosystem. Keep reading to learn more.

## Gravitee platform integrations

AE can be layered on top of:

* Gravitee API Management (APIM): bolster your existing Gravitee APIM implementation with advanced API monitoring and alerting capabilities. To learn more about how Alert Engine makes APIM better, please refer to the [APIM alerting documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-alerts-and-notifications#configure-alerts).&#x20;
* Gravitee Access Management: bolster your API Security strategy by using AE to notify teams when API consumption becomes suspicious. This looks like alerts sent when Gravitee Access Management notices potentially risky user profiles and/or consumption patterns. To learn more, refer to the [Gravitee Access Management documentation](https://documentation.gravitee.io/am).

## Integrating with third party solutions

You can also plug AE into your own backends and benefit from all the same features. You can use WebSocket or HTTP endpoints to create triggers and send events later in time.

### Requirements

Before using AE with your existing backend infrastructure, you must already have AE available as already deployed in your infrastructure, or, by running it with docker:

`docker run -t -v "${PWD}/licence.key:/opt/graviteeio-alert-engine/license/license.key:ro" -p 8072:8072 graviteeio/ae-engine:latest`

{% hint style="info" %}
**Enterprise functionality requires an enterprise license key**

Note that we use a `licence.key` file that you must have in the current directory (update the CLI as you need)
{% endhint %}

For running the Javascript scripts below, we use `node version v18.7.0`.

### WebSocket connection

You can send triggers through a WebSocket connection, as shown in the Javascript implementation example below.

To test this script:

1. bootstrap a javascript project with `npm init`
2. add `ws` dependency with `npm install --save ws`
3. create the `trigger.js` file with the content below.
4. run that script with `node trigger.js`

```
const WebSocket = require('ws');
const wsTrigger = new WebSocket("ws://localhost:8072/ws/triggers", {
    headers : {
        "Authorization": "Basic base64(username:password)"
    }
});

wsTrigger.onopen = () => {
  console.log("Trigger connection opened");
};

wsTrigger.onmessage = (event) => {
    console.log("Received message:", event.data.toString());
};

wsTrigger.onerror = (error) => {
  console.log("An error has occurred:", error);
};

wsTrigger.onclose = (event) => {
  console.log("Trigger WebSocket connection closed:", event.code, event.reason);
};

//Later in code
// A trigger example with a webhook notifier
const trigger = {
      "id": "response-time-threshold-id",
      "name" : "Response time Threshold",
      "source" : "my-source", // source of the event to handle
      "enabled" : true,
      "conditions" : [{
        "type" : "THRESHOLD",
        "property" : "response.response_time",
        "operator" : "LT",
        "threshold" : 1500.0
      }],
      "dampening" : {
        "mode" : "STRICT_COUNT",
        "trueEvaluations" : 1
      },
      "notifications": [
          {
              "type" : "webhook-notifier",
              "configuration" : {
                    "url":  "http://localhost:8080/alert/webhook",
                    "method":"POST",
                    "useSystemProxy":false,
                    "body": "${alert.id} - ${alert.name} - ${alert.source} - ${alert.description} - ${alert.severity} - ${notification.message}"
              }
          }
      ]
 };

if (wsTrigger.readyState === WebSocket.OPEN) {
    // You can send a single trigger
    wsTrigger.send(JSON.stringify(trigger));

    // Or an array of triggers
    // ws.send(JSON.stringify([...trigger]));
}
```

Same goes with events:

```
const WebSocket = require('ws');

const wsEvent = new WebSocket("ws://localhost:8072/ws/events", {
    headers : {
        "Authorization": "Basic base64(username:password)"
    }
});

wsEvent.onopen = () => {
  console.log("Trigger connection opened");
};

wsEvent.onerror = (error) => {
  console.log("An error has occurred:", error);
};

wsEvent.onclose = (event) => {
  console.log("Trigger WebSocket connection closed:", event.code, event.reason);
};

// Later in code

const event = {
  "id": "event-id",
  "timestamp": Date.now(),
  "type": "my-source", // Same value as the Trigger `source` property
  "context": { // context of your event, can be reused in the notifier
      "node.host": "my-host",
      "node.environment": "my-env"
  },
  "properties": { // What will be evaluated by the condition in the trigger
      "response.response_time" : 500
  }
}

if (wsEvent.readyState === WebSocket.OPEN) {
    // You can send a single trigger
    wsEvent.send(JSON.stringify(event));

    // Or an array of events
    // ws.send(JSON.stringify([...event]));
}
```

A new Alert Engine log line should appear to confirm a new WebSocket is opened.

And on the `trigger.js` run you should see something like:

```
Received message: {"action":"CHANGE","member":"428998e2-fe84-4dfd-82a6-7966d6883073","endpoint":"http://172.20.0.2:8072","id":"8a4a158c-4f31-4a59-8a15-8c4f31aa5902","type":"NODE_DISCOVERY"}
```

### HTTP Endpoint

You can also submit triggers via HTTP:

```
$ curl \
    -H "Authorization: Basic base64(username:password)" \
    -XPOST http://localhost:8072/http/triggers -d '{
      "id": "response-time-threshold-id",
      "name" : "Response time Threshold",
      "source" : "my-source",
       "enabled" : true,
      "conditions" : [{
        "type" : "THRESHOLD",
        "property" : "response.response_time",
        "operator" : "LT",
        "threshold" : 1500.0
      }],
      "dampening" : {
        "mode" : "STRICT_COUNT",
        "trueEvaluations" : 1
      },
      "notifications": [
          {
              "type" : "webhook-notifier",
              "configuration" : {
                    "url":  "http://localhost:8080/alert/webhook",
                    "method":"POST",
                    "useSystemProxy":false,
                    "body": "${alert.id} - ${alert.name} - ${alert.source} - ${alert.description} - ${alert.severity} - ${notification.message}"
              }
          }
      ]
 }'
```

Same with events:

```
$ curl \
    -H "Authorization: Basic base64(username:password)" \
    -XPOST http://localhost:8072/http/events -d '{
      "id": "event-id",
      "timestamp": 1670343913325,
      "type": "my-source",
      "context": {
          "node.host": "my-host",
          "node.environment": "my-env"
      },
      "properties": {
          "response.response_time" : 500
      }
    }'
```
