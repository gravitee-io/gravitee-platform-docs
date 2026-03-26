---
description: Concepts and architecture for Design Interface.
---

# Design Interface

## Overview

The design interface is the core of the API Designer. Initially, the interface supplies several defaults in an intuitive mind map-like structure where API details can be added as needed. Three elements are visible:

* **root:** The starting point of a design containing the settings. You can add resources to it using the (+) buttons branching away to the left or right (to align with your visual preference).
* **resource:** The anchor points of the API that conceptually map to a set of entities.
* **attribute:** The data carriers of the API.

<div align="center"><figure><img src="https://docs.gravitee.io/images/cockpit/apid_design_default.png" alt="" width="563"><figcaption></figcaption></figure></div>

Each element can be expanded (+). To remove an element, right-click it and select delete.

{% hint style="warning" %}
If you delete an element, all underlying elements will also be deleted.
{% endhint %}

There are three design phases: **define**, **expose** and **refine**. First, broadly define resources and attributes. How you expose them depends on your use case. Next, refine the attributes.

## Define <a href="#define" id="define"></a>

The key part of a resource definition is the name. The name will appear in the request path.

The datatype of an attribute definition matters most. It can be an integer, number, string, boolean, or a list of one of these.

Both resources and attributes can be exposed in the API’s documentation.

## Expose <a href="#expose" id="expose"></a>

The [operations](design-interface.md#operations) allowed on a resource can be specified. You can also specify whether or not the resource is searchable with query parameters.

You can determine the visibility of an attribute in requests and responses. You can also add it as a filter for and/or result of searches. An attribute can only be added if the parent resource or attribute is added.

An attribute can be expanded. This will automatically change its type to Object. If you want to turn an attribute into a resource, it must be a list.

## Refine <a href="#refine" id="refine"></a>

To refine an attribute, you can:

* Provide a sample value to use in mock responses
* Determine whether or not the attribute is required
* Provide an extra description

## Operations mapping <a href="#operations" id="operations"></a>

<table><thead><tr><th width="123">Operation</th><th width="342">Description</th><th>Triggered by</th></tr></thead><tbody><tr><td>GET</td><td>Retrieves all entities of the requested resource</td><td>Resource is searchable</td></tr><tr><td>GET</td><td>Retrieves one entity (via ID) of the requested resource</td><td>Resource is readable</td></tr><tr><td>DELETE</td><td>Deletes one entity (via ID) of the requested resource</td><td>Resource is deletable</td></tr><tr><td>POST</td><td>Creates an entity of the requested resource</td><td>Resource is creatable</td></tr><tr><td>PUT</td><td>Updates one entity (via ID) of the requested resource</td><td>Resource is updatable</td></tr><tr><td>PATCH</td><td>Updates specific attributes of one entity (via ID) of the requested resource</td><td>Resource is partially updatable</td></tr></tbody></table>
