# Policies

## Overview

Policies in Access Management (AM) define specific actions or validations to be executed at various stages in the authentication and user management process. Each policy serves a distinct function, from security checks to user experience improvements.

{% hint style="warning" %}
Policies labeled as (EE) are only available in the [Enterprise Edition (EE)](../../../overview/open-source-vs-enterprise-am/README.md) of Gravitee.
{% endhint %}

## Policy list

The following is the list of policies that can be used in AM:

* **Account Linking (EE):** Links an external Identity Provider (IdP) user account to an existing local user account. This is useful in federated authentication scenarios. Use this Policy in the Connect flow.
* **Enrich Authentication Flow:** Allows injection of custom data into the authentication process. This is useful for advanced customizations.
* **Enrich User Profile:** Adds to user profile attributes during authentication or registration.
* **Enroll MFA:** Enroll MFA factors are based on user profile information and skip the interactive MFA enrollment step. [Functions that use Gravitee Expression Language](../../am-expression-language.md#functions) can pull information from user profiles. MFA flows let you use multiple MFA for authentication.
* **Groovy:** Executes custom Groovy scripts. This enables the implementation of custom logic not covered by built-in policies.
* **HTTP Callout:** Calls external HTTP endpoints to perform additional checks or actions (e.g., external validation, enrichment).
* **IPFiltering:** Allows or blocks access based on the user's IP address.
* **Latency:** Introduces artificial delay into a flow.
* **MFA Challenge (EE):** Enforces users to confirm their identity by using another factor. [Functions that use Gravitee Expression Language](../../am-expression-language.md#functions) can pull information from user profiles. MFA flows let you use multiple MFA for authentication.
* **Rate Limit:** Configures the number of requests allowed over a limited period of time (seconds, minutes).
* **Send Email:** Sends an email as part of the flow (e.g., for notifications, verifications).
* **Validate Request:** Validates incoming HTTP requests according to defined criteria (e.g., required fields, values).
