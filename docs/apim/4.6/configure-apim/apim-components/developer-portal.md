---
description: An overview about developer portal.
---

# Developer Portal

## Overview

The Developer Portal is a web application that provides a simplified, user-friendly interface tailored to the API consumption process. It acts as a centralized catalog where internal and external API consumers can find and subscribe to APIs that are developed, managed, and deployed by API publishers.

API consumers can easily discover and explore APIs, read documentation, test API endpoints, generate access tokens, view API analytics, and manage their API subscriptions in a single location. Additionally, administrators have significant control over the look and feel of the Developer Portal to deliver an accessible and on-brand experience to external API consumers.

## Access the Developer Portal

Enterprise trial users should be able to immediately access the Developer Portal from the APIM Console by selecting the **Developer Portal** link in the top left of the Console's nav bar.

<figure><img src="broken-reference" alt=""><figcaption><p>Access Developer Portal from APIM Console</p></figcaption></figure>

This will bring you to the home screen of the Developer Portal.

<figure><img src="broken-reference" alt=""><figcaption><p>Your default Developer Portal</p></figcaption></figure>

From here, you can begin searching for APIs using the Developer Portal's full-context[^1] search. However, you will not be able to subscribe to any APIs until you create an application.

## Self-managed installation: Adding a Developer Portal link

The Developer Portal host of self-managed installations can easily be modified. You can manually add the **Portal URL** to see the Developer Portal link in the Console UI.

Your Developer Portal URL will depend on your deployment, so please reference the respective installation docs. For example, with the default Docker installation, you can access the Developer Portal at `http://localhost:8085` in your browser.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

1. Click **Settings** in the left nav
2. Click **Settings** in the inner left nav
3. Scroll down to **Portal** settings and provide a **Portal URL** based on your deployment configuration
4. Scroll to the bottom of the page and click **Save**

[^1]: Full-context meaning it searches through the definition and metadata of all published APIs that you have access to
