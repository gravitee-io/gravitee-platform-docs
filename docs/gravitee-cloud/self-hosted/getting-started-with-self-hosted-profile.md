---
description: >-
  Welcome, you are here because you want to run Gravitee completely self-hosted?
  Perfect, we will make your journey as smooth as possible!
---

# Getting started with Self-hosted Profile

To use Gravitee Cloud where you connect your own fully self-hosted installations, you need to select "Self-hosted" as profile when setting up your account.

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption><p>Gravitee Cloud account set up page with Self-hosted deployment option chosen.</p></figcaption></figure>

With Gravitee Cloud Self-hosted profile you can:

* Add and manage various Gravitee API Management installations and environments
* Add and manage various Gravitee Access Management installations and environments
* Promote APIs across higher and lower environments

{% hint style="info" %}
Want to run Gravitee in the easiest and most secure way? Maybe Gravitee Cloud is what you are looking for? Click [here](../README.md) to read more on how to start your Gravitee Cloud journey!
{% endhint %}

## Gravitee Cloud self-hosted hierarchy

Gravitee Cloud self-hosted is based on a hierarchy of the following entity types:

<figure><img src="../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

| Entity                    | Description                                                                                                                                                                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Account                   | The top level entity, your company. One user can have multiple accounts.                                                                                                                                                                                                     |
| Organization              | A logical part of your company in the way that makes most sense in your setup. For example a region or business unit. There can be multiple organizations linked to one account.                                                                                             |
| Environment               | An environment in an IT infrastructure, such as development or production. There can be multiple environments linked to one organization.                                                                                                                                    |
| APIM and AM installations | <p>Nodes can belong to multiple environments. You can configure the organizations and environments associated with Gateway nodes in APIM and AM, by updating the Gateway configuration files.</p><p>Only Gateway nodes are configurable in this way, not REST API nodes.</p> |

Each entity managed in Gravitee Cloud has some common properties:

* **ID:** an internal ID that is never shown in the Gravitee Cloud UI, but that you can find if you look at the API responses.
* **HRID**: a human readable ID of the entity. This ID is unique (no two environments in the same organization can have the same HRID), and they are used to provide readable URLs.
* **Name:** the name of the entity.
* **Description**: a description of the entity.

## Example hierarchy

The Gravitee Cloud hierarchy pictured below has the following setup:

* One APIM installation, with two Gateway nodes and one REST API node.
* One AM installation, with one Gateway node and one REST API node.

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>
