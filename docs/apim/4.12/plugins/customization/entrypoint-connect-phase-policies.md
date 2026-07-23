# Policies for the Entrypoint Connect phase

## Overview

The Entrypoint Connect phase runs as soon as a client opens a connection to a native Kafka API entrypoint, before authentication and before any message processing. This article describes how a custom policy interrupts a connection during that phase. To configure the phase on an API, see [Entrypoint Connect phase](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/entrypoint-connect-phase.md).

## Interrupt a connection

A policy interrupts the connection by calling `interrupt(String reason)` on the execution context that the Gateway passes to the Entrypoint Connect phase. Call it to reject a connection before the client authenticates.

When a policy interrupts the connection:

1. The Gateway doesn't attempt any upstream connection.
2. The Gateway terminates the client connection.
3. The Gateway skips all downstream message-phase policies for that connection.

## Error logging

The Gateway logs interrupting errors at `DEBUG` level. It logs non-interrupting errors at `WARN` level and continues execution.
