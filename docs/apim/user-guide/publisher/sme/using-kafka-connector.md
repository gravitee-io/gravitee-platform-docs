# Overview

This section describes the basic usage of the Kafka connector -
producing and consuming messages.

## Producing messages

Using the HTTP `POST` command to the example endpoint
`https://api.company.com/kafka/messages`, you can send a message with
the following structure:

    https://api.company.com/kafka/messages
    {
      "messages": [
        {
          "key": "key",
          "value": {
            "val1": "hello"
          }
        }
      ]
    }

## Consuming messages

Using the HTTP `GET` command to the example endpoint
`https://api.company.com/kafka/messages`, you can receive any available
messages.
