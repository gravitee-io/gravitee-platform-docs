# Introduction to Gravitee Access Management (AM)

Gravitee Access Management (AM) is a flexible, lightweight, and easy-to-use open source Identity and Access Management (IAM) solution. It offers a centralized authentication and authorization service to deliver secure access to your applications and APIs from any device.

With its intuitive design and seamless integration with our API Management product, Access Management is the natural Identity and Access Management platform choice for our customers.

This article describes the use case for AM and gives a high-level overview of its core components, concepts, and authorization mechanisms.

## Use cases

Here are some common AM use cases:

* You’ve built a new application and you want to add user authentication and authorization
* You want your new frontend, mobile, or web application to securely access your APIs
* You’re using Gravitee API Management to manage your APIs and you want to implement a seamless authorization flow
* You want the flexibility to log in users either with a username and password or with their social media accounts
* You have a group of applications for which you want to implement single sign-on
* You want to focus on developing apps and leave the headache of password and user management to an external solution
* You have multiple user directories (database, web service, LDAP, AD) that you want to federate
* You want to rely on standard protocols to ensure interoperability with your enterprise tools

## Core components

Gravitee AM is composed of three main components: the AM Gateway, the AM Management API, and the AM Management Console.

* **AM Gateway**\
  AM Gateway is the core component of the AM platform. It acts as a trust broker with your identity providers and provides an authentication and authorization flow for your users.\

*   **AM Management API**\
    These RESTful APIs expose services to:

    * Manage and configure the AM platform
    * Manage users and user sessions
    * Manage the authorization flow for OAuth 2.0, OpenID Connect, UMA 2.0, and SCIM 2.0 protocols

    All exposed services are restricted by authentication and authorization rules. You can find more information in the [Auth Protocols](guides/auth-protocols/) section.\

* **AM Management Console**\
  This web UI acts as a graphical interface to the AM Management API functionality.

## Core AM Concepts

The concepts below are central to using AM.

*   **Organization**\
    An organization is internal data space that is provisioned by AM to hold all the resources that handle user authentication.\


    {% hint style="info" %}
    The Community Edition version of AM comes with a single default organization
    {% endhint %}


*   **Environment**\
    An environment is a logical workspace in which administrative users can manage security domains.\


    {% hint style="info" %}
    The Community Edition version of AM comes with a single default environment
    {% endhint %}


* **Security domain**\
  A security domain:
  * Gives you access to all the AM resources, such as applications, users, and identity providers
  * Exposes authentication and authorization URLs
  * Gathers analytics and reporting\

*   **Application**\
    An application can be any type of application, for example:

    * Web Application (PHP, Java, Node.js)
    * Single App (JavaScript)
    * Native App (iOS, Android)
    * Backend App (Job, CLI)

    Applications use AM to sign in and make requests to the Gateway Authorization Server. They can be used by end users (B2C) or autonomously (B2B).\

*   **Identity provider**\
    An identity provider brokers trust with external user providers such as:

    * LDAP / Active Directory
    * Database
    * Web services
    * Social providers
    * OpenID Connect providers
    * SAML v2 IDP
    * Custom providers

    It is used during the login process to verify user credentials and retrieve profile information.\

* **Flow**\
  A flow allows you to build your own custom authentication and authorization journey by executing policies during specific phases of the authentication flow. Flows can be used to:
  * Enrich user profiles
  * Notify 3rd party systems
  * Add extra authorization rules (such as verify users or enforce MFA)

## Authorization in AM

AM acts as an identity provider broker and is based on the OAuth2 / OpenID Connect and SAML 2.0 protocols.

*   **OAuth2**\
    OAuth2 is an authorization framework that allows applications acting on behalf of the end user to obtain limited access to HTTP services. [OAuth 2 RFC](https://tools.ietf.org/html/rfc6749) defines two endpoints:

    * The **authorization endpoint** used to interact with the resource owner and obtain an authorization grant via user-agent redirection.
    * The **token endpoint** used by the client to obtain an access token by presenting its authorization grant.\


    {% hint style="info" %}
    For further information about OAuth2, view the [RFC page](https://tools.ietf.org/html/rfc6749).
    {% endhint %}


*   **OpenID Connect**\
    OpenID Connect is an identity layer on top of the OAuth 2.0 protocol. It enables clients to verify the identity of the end user via an Authorization Server to authenticate and obtain basic profile information about the end user.\


    {% hint style="info" %}
    For further information about OpenID Connect, view the [OpenID Connect specifications](http://openid.net/specs/openid-connect-core-1_0.html).
    {% endhint %}


*   **SAML 2.0**\
    The Security Assertion Markup Language (SAML) protocol is an open-standard, XML-based framework for the authentication and authorization of users. Gravitee AM can act as SAML IdP for applications, as well as federate with SAML-based identity providers for protocol mediation.\


    {% hint style="info" %}
    For further information about SAML 2.0, view the [SAML Tech Overview 2.0](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html).
    {% endhint %}
