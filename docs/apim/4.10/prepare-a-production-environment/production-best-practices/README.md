---
description: >-
  These configuration settings and recommendations are critical to the security
  of your production environment
metaLinks:
  alternates:
    - ./
---

# Production Best Practices

## Overview

The default settings created during APIM installation can be useful for testing your new instance. However, some may not be suitable for a production environment, where security is more of a consideration. This guide highlights the APIM settings that require special attention when migrating to a production environment.

## Security checklist

The following high-level checklist links to the details of how and why you would enforce each list item.

{% hint style="info" %}
The objective is not to apply all of the recommendations, but to ensure that all configurations have been made with caution.
{% endhint %}

<details>

<summary>Security checklist</summary>

1. Internal APIs

* [ ] [Disable or enforce the security of the internal API](internal-apis.md)

2. Deployment

* [ ] [Review the exposition of the console and developer portal to the outside world](deployments.md#console-and-portal-apis)
* [ ] [Ensure the console and developer portal rest APIs are accessible through HTTPS](deployments.md#enable-https)

3. Authentication

* [ ] [Configure authentication using an identity provider](authentication.md#identity-providers)
* [ ] [Enable authentication to access the Developer Portal](authentication.md#developer-portal-authentication)
* [ ] [Remove all the default users](authentication.md#default-users)
* [ ] [Remove the admin user or enforce the admin user password](authentication.md#admin-user)
* [ ] [Disable user self-registration for bot console and portal](authentication.md#user-self-registration)
* [ ] [Disable auto-validation of self-registered users (if self-registration is enabled)](authentication.md#user-self-registration)
* [ ] [Change the user session signing secret and validity duration](authentication.md#user-session)
* [ ] [Disable default application creation](authentication.md#other-user-options)
* [ ] [Set the registration link validity to 1 day](authentication.md#other-user-options)
* [ ] [Change the user reference secret](authentication.md#other-user-options)

4. Brute-force and browser protection

* [ ] [Configure brute force protection](protections.md) ([ReCaptcha](protections.md) or [Fail2ban](protections.md))
* [ ] [Enable CSRF protection](protections.md)
* [ ] [Configure CORS for Console and Portal REST APIs](protections.md)

5. Configuration settings

* [ ] [Change the property encryption secret](general-recommendations/property-encryption.md)
* [ ] [Enable documentation page sanitizer](general-recommendations/documentation-sanitizer.md#documentation-sanitizer)
* [ ] [Disable Webhook notifier or configure an authorized list of URLs](general-recommendations/notifiers.md)

6. APIM best practices

* [ ] [Apply best practices when designing and deploying APIs](general-recommendations/api-design.md)

7. Advanced caching strategies

* [ ] [Configure semantic caching for LLM and AI workloads](#semantic-caching-for-llm-and-ai-workloads)

</details>

## Semantic caching for LLM and AI workloads

When deploying LLM Proxy APIs, semantic caching can significantly reduce latency and costs by reusing responses for semantically similar requests. The AI Semantic Caching policy uses vector embeddings to match incoming prompts against cached responses.

### Best practices

* **Use JSONPath for prompt extraction**: Extract only the relevant content from complex payloads (e.g., `{#jsonPath(#request.content, '$.messages[-1:].content')}` for chat completions)
* **Set appropriate cache conditions**: Cache only successful responses (e.g., `{#response.status >= 200 && #response.status < 300}`)
* **Encode sensitive metadata**: Use `encode: true` for parameters containing PII or sensitive data to hash values using MurmurHash3
* **Scope cache appropriately**: Use metadata parameters to scope caching per API, plan, or user context
* **Configure similarity thresholds**: Adjust vector store similarity thresholds to balance cache hit rate versus accuracy

For detailed configuration options and examples, see the <a data-mention href="../create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md">AI Semantic Caching policy reference</a>.

{% hint style="warning" %}
**Configuring APIM**

APIM includes many other configuration options and every environment is unique. However you configure new settings (via the `gravitee.yml` file, APIM Console, or environment and system variables) it is important to understand that one configuration type can override another.
{% endhint %}
