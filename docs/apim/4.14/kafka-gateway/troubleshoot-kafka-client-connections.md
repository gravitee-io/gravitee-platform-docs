---
description: Find why a Kafka client can't connect, produce, or consume through the Kafka Gateway, from the error the client receives and the Gateway log.
---

# Troubleshoot Kafka client connections

## Overview

When a Kafka client can't connect, produce, or consume through the Kafka Gateway, check two things. The error code that the client receives and the warnings in the Gateway log show where the connection failed. This page lists failures by what you see.

## Read the Gateway log

The start of these Gateway warnings says what failed, and the rest of the message gives the cause:

| Warning starts with | What failed |
| --- | --- |
| `Client authentication failed:` | The Gateway couldn't authenticate the client. |
| `Upstream broker authentication failed:` | The broker rejected the credentials in the endpoint's security configuration. |
| `Upstream broker SASL authentication failed:` | The endpoint delegates authentication to the broker, and authentication with the client's SASL credentials failed. |
| `Upstream broker failure:` | The Gateway couldn't connect to the broker. |
| `No Kafka endpoint for request:` | No endpoint of the API can take the connection on this Gateway. |
| `No Kafka acceptor found for SNI` | The Gateway can't match the connection to a Kafka API. |

Some failures don't log a warning. The following sections list them with what you see instead.

## The client can't connect

These failures stop the client from connecting.

| What you see | Cause | What to do |
| --- | --- | --- |
| The client gets no answer from the Gateway, and the Gateway logs `No Kafka acceptor found for SNI <host> and serverId <id>`. | The Gateway can't match the connection to a Kafka API deployed on it. With host-based routing, the host name that the client connects to belongs to no API. With port-based routing, the port belongs to no API. | Check the host names, or the ports, that the client connects to: the bootstrap server, and the broker host names that the Gateway advertises. See [Bootstrap server domain](configure-the-kafka-client-and-gateway.md#bootstrap-server-domain) and [Configure Kafka Port Routing (Gateway and Console)](configuring-kafka-port-routing-gateway-and-console.md). |
| The connection closes, and the Gateway logs `Client IP <ip> is not allowed to access the API`. | The Native IP Filtering policy refused the client's IP address. | Check the IP addresses in the policy. |
| The connection closes, and the Gateway logs `Upstream broker failure: <cause>`. | The Gateway couldn't connect to the broker: the connection was refused, the broker host didn't resolve or was unreachable, or the connection timed out. The Gateway connects to the broker for every client connection, including the first one. | Check the bootstrap servers of the API's endpoint, and that the Gateway can reach the brokers on the network. |
| The connection closes, and the Gateway logs `No Kafka endpoint for request: <cause>`. | No endpoint of the API can serve this Gateway, for example because no endpoint matches the Gateway's tenant. | Check the tenants of the API's endpoints. See [Multi-tenant endpoint support](create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#multi-tenant-endpoint-support). |

## Authentication fails

These failures happen while the client authenticates, and they end the connection.

| What you see | Cause | What to do |
| --- | --- | --- |
| The client receives an authentication error, and the Gateway logs `Client authentication failed: <cause>`. | None of the API's plans accepted the client's credentials. | Check that the client uses the credentials of a plan that its application subscribes to. See [Native Kafka API plans](plans.md). |
| The Gateway logs `Client authentication failed: <cause>`, and the cause is a timeout. | While the client authenticated, the broker took more than 10 seconds to answer the Gateway. | Check the broker's response time, and that the Gateway can reach the broker. |
| The Gateway logs `Unable to execute the security chain`. | Checking the client's credentials against the API's plans failed, or took more than 20 seconds. | Check the security configuration of the plan, and the response time of any server that it uses to check credentials. |
| The client receives `UNSUPPORTED_SASL_MECHANISM`, and the endpoint doesn't delegate authentication to the broker. | No plan of the API accepts the client's SASL mechanism. OAuth2 and JWT plans accept `OAUTHBEARER`. By default, API Key plans accept `PLAIN`, `SCRAM-SHA-256`, and `SCRAM-SHA-512`. | Set the client's SASL mechanism to one that a plan of the API accepts. |
| The client receives `UNSUPPORTED_SASL_MECHANISM`, and the Gateway logs `Gateway doesn't support <mechanism> sasl mechanism for delegate to broker authentication.` | The endpoint delegates authentication to the broker, which works with the `PLAIN` and `AWS_MSK_IAM` mechanisms only. | Set the client's SASL mechanism to `PLAIN` or `AWS_MSK_IAM`. See [SASL mechanisms](create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#sasl-mechanisms). |
| The client receives `ILLEGAL_SASL_STATE`. | The endpoint delegates authentication to the broker, and the client sent another request before it authenticated with SASL. | Configure the client to authenticate with SASL. |
| The endpoint delegates authentication to the broker, and the client receives an authentication error from the broker. | The broker rejected the client's credentials. The Gateway passes the broker's answer to the client. | Check the client's credentials on the broker. |
| The Gateway logs `Upstream broker SASL authentication failed: <cause>`. | The endpoint delegates authentication to the broker, and authentication with the client's SASL credentials failed. | Check the client's SASL credentials and mechanism. |
| The Gateway logs `Upstream broker authentication failed: <cause>`. | The broker rejected the credentials in the endpoint's security configuration. | Check the security configuration of the API's endpoint. See [Security protocols](create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#security-protocols). |

For mTLS plans, see [Certificate validation errors](plans.md#certificate-validation-errors).

## Producing or consuming fails or times out

These failures happen after the client's first connection to the bootstrap server works.

| What you see | Cause | What to do |
| --- | --- | --- |
| The client reaches the bootstrap server, but it can't produce or consume. | After the first connection, the client connects to each broker through a host name that the Gateway advertises. By default, this host name combines a prefix, the broker ID, the API's host, and the Gateway's domain. The client can't resolve or reach one of these host names. | Make sure that every broker host name resolves to the Gateway. See [Broker mapping](configure-the-kafka-client-and-gateway.md#broker-mapping). For a Virtual Cluster, see [Virtual Cluster Broker Addressing](virtual-cluster-broker-addressing.md#troubleshooting). |
| A request times out on the client, and the Gateway logs `Unable to correlate the received response with its corresponding request. Ignoring`. | The broker answered after the Gateway's request timeout, which is 35 seconds by default. The Gateway drops the late answer. | Check the broker's response time. For the Gateway's request timeout, see [Deploy the Kafka Gateway for High Availability](deploy-the-kafka-gateway-for-high-availability.md). |

For the idle timeout of a load balancer in front of the Gateway, see [Deploy the Kafka Gateway for High Availability](deploy-the-kafka-gateway-for-high-availability.md).

## Access is refused

When the Kafka ACL policy or the broker refuses a request, the client gets an error code for that request, and the connection stays open. A producer that doesn't wait for acknowledgments is the exception.

| What you see | Cause | What to do |
| --- | --- | --- |
| The client receives `TOPIC_AUTHORIZATION_FAILED`, `GROUP_AUTHORIZATION_FAILED`, or `TRANSACTIONAL_ID_AUTHORIZATION_FAILED`, and the API has a Kafka ACL policy. | No ACL in the policy grants the operation on that topic, group, or transactional ID. | Add an ACL that grants the operation on the resource. See [Kafka ACL](../create-and-configure-apis/apply-policies/policy-reference/kafka-acl.md). |
| The client receives `CLUSTER_AUTHORIZATION_FAILED`, and the API has a Kafka ACL policy. | The policy has no ACL, no ACL grants the operation that the request needs, or the policy doesn't support the type of request, which it refuses whatever its ACLs. | Add the ACLs that the client needs. |
| A topic is missing from the list of topics that the client receives. | The Kafka ACL policy leaves out the topics that the client isn't allowed to describe. | Add an ACL that grants the **Describe** operation on the topic. |
| A producer that doesn't wait for acknowledgments gets no error, but its messages don't reach the topic. | The Kafka ACL policy refused the produce request. A producer set to `acks=0` gets no answer, so it never sees the error. | Add an ACL that grants the **Write** operation on the topic. |
| The client receives an authorization error, and the Kafka ACL policy grants the operation, or the API has no Kafka ACL policy. | The broker refused the request. The broker authorizes the identity that the Gateway connects with: the credentials in the endpoint's security configuration, or the client's own credentials when the endpoint delegates authentication to the broker. | Check the ACLs on the broker for that identity. |

For the other policies that can interrupt a request, see [Policy failures](create-and-configure-kafka-apis/configure-kafka-apis/policies.md#policy-failures).
