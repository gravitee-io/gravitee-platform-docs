---
description: Learn API management concepts with a demo application
---

# Tutorial: Demo Application

These tutorials do not assume any existing Gravitee API Management (APIM) knowledge and are designed for people who prefer to learn by doing. The techniques you’ll learn in the tutorial are fundamental to working with APIM. You will be working with a demo application that simulates how APIM might be used in a real-world use case. If you'd prefer to learn APIM's core concepts step by step, head over to our [Guides section](../../guides/prologue.md) to explore our detailed walkthroughs.

## Demo Application Overview

The demo app flow begins with the following steps:

1. APIM Trial is provisioned and ready
2. User opens APIM
3. APIM Pendo guide pop-up providing the user an option to explore on their own or learn with the demo app
   * If the user decides to explore on their own, they will still have another method to access the demo app
4. If the user decides to learn with the demo app, then a new tab will open with the demo app on the home page with the use cases detailed below. Selecting any of the use cases will open the relevant documentation with a written guide and a video.

### Use Case 1: Basic Security and Access Control

**Goal:** Rapidly demonstrate basic APIM functions and provide user with aha-moment

**Ideal time to complete:** 10 minutes

#### Steps:

1. Select the use case&#x20;
2. (Optional) Start the respective pendo walkthrough in APIM
3. Documentation opens to relevant section
4. Docs provide high-level overview of demo app architecture (i.e., todo actions are tied to REST endpoints)
5. Guide the user to the gateway API in their trial
6. Educate the user on the basics of gateway APIs
7. Return to the demo app and showcase basic todo functionality
8. Instruct user to add 2 todos and receive error on the 3rd (we make the quota to 2 calls only)
9. Instruct the user to archive a todo and receive error due to resource filtering
10. Return to APIM policy studio and educate user on policies
11. Guide the user to the plans page and educate user on plans
12. Explain the application is currently using the keyless plan but also access a "premium" plan with API key security
13. Guide the user to the Applications page to subscribe to the API key plan which will be set to auto-validate the subscription
14. Guide the user to return to the demo app to create more than 3 todos and use the archiving functionality
15. Return to the policy design studio to highlight how policies can be applied at the plan, API, or even the platform level with different methods (EL, paths, HTTP methods, etc.) of filtering
16. Invite the user to modify the existing policies and see how it impacts the application

### Use Case 2: Real-time Data and Protocol Mediation

**Goal:** Showcase Gravitee's main differentiator - event-native API management

**Ideal time to complete:** 15 minutes



### Use Case 3: Advanced Policies and Security

**Goal:** Require more involvement from the user and demonstrate security measures beyond a simple API key

**Ideal time to complete:** 20 minutes

## Prerequisites

These tutorials are designed to work seamlessly with our enterprise trial as they demonstrate a number of enterprise-only features. To get started with the free enterprise trial, simply follow the [instructions laid out here](../install-and-upgrade/free-trial.md). Setting up a new trial takes approximately five minutes and you can return here to select any of the following paths to experience the power of Gravitee API Management alongside our demo application:

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td></td><td><strong>Basic Security and Access Control</strong><br><br>This tutorial showcases Gravitee's core features which include securing a Gateway API, applying API access restrictions, and managing applications and subscriptions.<br><br><em>Gateway Architecture:</em> http-proxy<br><em>Entrypoint:</em> REST<br><em>Endpoint:</em> REST<br><em>Plan Security:</em> API Key<br><em>Policies:</em> Quota, Interrupt</td><td></td></tr><tr><td></td><td><strong>Real-time Data and Protocol Mediation</strong><br><br>This tutorial demonstrates Gravitee's ability to natively handle, and mediate between, both asynchronous and synchronous protocols.<br><br><em>Gateway Architecture:</em> message<br><em>Entrypoint:</em> Websocket<br><em>Endpoint:</em> Kafka<br><em>Plan Security:</em> None (temporary - shared API key support)<br><em>Policies:</em> Latency</td><td></td></tr><tr><td></td><td><strong>Advanced Policies and Security</strong><br><br>This tutorial details more advanced policies and security measures.<br><br><em>Gateway Architecture:</em> http-proxy<br><em>Entrypoint:</em> REST<br><em>Endpoint:</em> REST<br><em>Plan Security:</em> JWT<br><em>Policies:</em> Assign Metrics</td><td></td></tr></tbody></table>
