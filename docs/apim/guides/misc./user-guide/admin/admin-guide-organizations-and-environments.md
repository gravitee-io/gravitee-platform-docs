# Overview

Two concepts apply to the setup of **Gravitee.io API Management** (APIM)
installation. Organization and environment.

# Organization

A logical part of your company in the way that makes most sense in your
setup, for example a region or business unit. In the context of an APIM
installation it is the level at which shared configurations for
environments are managed, such as:

-   Users

-   Roles

-   Identity providers

-   Notification templates

It also allows operations across managed environments (like API
import/export).

You can update a gateway’s organization settings in APIM Console by
clicking **Organization settings** in the left-hand navigation.

# Environment

An environment in an IT infrastructure, such as development or
production. There can be multiple environments linked to one
organization. In the context of an APIM installation, it is the
workspace in which users can manage their APIs, applications and
subscriptions An environment handles its own categories, groups,
documentation pages and quality rules.

Examples of environments:

-   technical environments such as DEV / TEST / PRODUCTION

-   functional environments such as PRIVATE APIS / PUBLIC APIS /
    PARTNERSHIP

An environment belongs to one organization.

You can update a gateway’s environment settings in APIM Console by
clicking **Settings** in the left-hand navigation

By default, the OSS version of APIM comes with a default organization
and a default environment. For a multi-environment setup, you need an
integration with link:{% link pages/cockpit/overview/introduction.adoc
%}\[Cockpit\].
