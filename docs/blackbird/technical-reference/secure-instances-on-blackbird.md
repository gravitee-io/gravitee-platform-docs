---
noIndex: true
---

# Secure Instances on Blackbird

By default, all mock, code run, code debug, and deployment instances are publicly available. To secure your endpoints, you can use API keys. An API key is a unique identifier used to authenticate requests made to an API using a key value pair. When you send a request to an API endpoint, the API key is included in the request to verify that the request is coming from an authorized source. You can create and manage your API keys from the Blackbird CLI, and you can give the API key any value. If a mock, code run, code debug, or deployment instance has an enabled API key, you’ll see it in the Blackbird UI or CLI details.

## Creating a Secure Key

First step is to create an secure APIKey. **Note**: Please make sure you save the APIKey header value since you won't be able to view them after creation.

```shell
blackbird apikey create <HeaderKey> <HeaderValue>
```

Once the APIKey is created, we can double check that creation was successful with the list command.

```shell
blackbird apikey list
```

## Enabling a Secure Key

There are two ways to enable an APIKey. The first is with the `enable` command and the second is on creation of an instance.

### Security on an Existing Instance

If we already have an instance that is created, we want to use the APIKey enable command for security.

```shell
blackbird apikey enable <HeaderKey> <InstanceName>
```

### Enabling Security on Instance Creation

If we don't have an instance yet, we can enable and create an secure APIKey upon creation of an instance. Please read the [mock-instances.md](../usage-guides/mock-instances.md "mention") and [deployments.md](../usage-guides/deployments.md "mention") documentation for further assistance.

```shell
blackbird mock create --api-name <slug-name> --apikey-header <HeaderKey>
```

At this point you will be prompted to enter a value for the APIKey header.

## Disabling a Secure Key

To disable an secure APIKey, we can use the `disable` command

```shell
blackbird apikey disable <HeaderKey> <InstanceName>
```

## Deleting a Secure Key

```shell
blackbird apikey delete <HeaderKey>
```
