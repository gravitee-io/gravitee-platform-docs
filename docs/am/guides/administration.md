# Administration

## Overview

Two concepts apply to the setup of **Gravitee Access Management** (AM) installation. Organization and environment.

### Organization

A logical part of your company in the way that makes most sense in your setup, for example a region or business unit. In the context of an AM installation it is the level at which shared configurations for environments are managed, such as:

* User permissions to access the AM console
* Roles
* Identity providers to access the AM console

### Environment

An environment in an IT infrastructure, such as development or production. There can be multiple environments linked to one organization. In the context of an AM installation, it is the workspace in which users can manage their security domains and applications.

Examples of environments:

* technical environments such as DEV / TEST / PRODUCTION
* functional environments such as PRIVATE DOMAINS / PUBLIC DOMAINS / PARTNERSHIP

An environment belongs to one organization.

{% hint style="info" %}
By default, the OSS version of AM comes with a default organization and a default environment. For a multi-environment setup, you need an integration with [Gravitee Cloud](https://docs.gravitee.io/cockpit/3.x/cockpit\_overview\_introduction.html).
{% endhint %}
