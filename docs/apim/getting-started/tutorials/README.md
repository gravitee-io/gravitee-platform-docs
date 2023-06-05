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

**Goal:** Rapidly demonstrate basic APIM functions (policies, plans, applications, subscriptions, etc.) and provide user with aha-moment

**Ideal time to complete:** 5-10 minutes

#### Steps:

1. Select the use case&#x20;
2. (Optional) Start the respective pendo walkthrough in APIM
3. Documentation opens to relevant section
4. Docs provide high-level overview of demo app architecture (i.e., todo actions are tied to REST endpoints with mongodb backend)
5. Showcase basic todo functionality
6. Instruct user to add 2 todos and receive error on the 3rd due to quota policy
7. Instruct the user to archive a todo and receive error due to resource filtering policy
8. Return to APIM and guide the user to the gateway API in their trial and educate the user on the basics of gateway APIs from the perspective of an API publisher
9. Guide user to policy design studio and educate user on policies focusing on the pre-seeded quota and resource filtering policies
10. Guide the user to the plans page and educate user on plans
11. Explain the demo application is currently using the keyless plan but can also subscribe to a "premium" plan with API key security
12. Guide the user to the applications page to subscribe to the API key plan which will be set to auto-validate the subscription
13. Copy the API key and add it to the demo app
14. Instruct the user to create more than 3 todos and use the archiving functionality
15. Return to the policy design studio to highlight how policies can be applied at the plan (keyless vs API key), API, or even the platform level, all with different methods (EL, paths, HTTP methods, etc.) of filtering
16. Invite the user to modify the existing policies and see how it impacts the application

### Use Case 2: Real-time Data and Protocol Mediation

**Goal:** Showcase Gravitee's main differentiator - event-native API management

**Ideal time to complete:** 10-15 minutes

1. Select the use case&#x20;
2. (Optional) Start the respective pendo walkthrough in APIM
3. Documentation opens to the relevant section
4. Docs provide high-level overview of demo app architecture (i.e., detail different protocols involved and kafka backend)
5. Guide the user to the gateway API in their trial and explain that we created a new gateway API because we are employing a new backend API (kafka vs mongodb)
6. Detail event-native API management and the power to manage APIs and different backend resources regardless of protocol employed. Gravitee allows you to work with kafka without ever setting up a kafka client which allows you to use consumer-friendly protocols like http and websocket
7. If the user did not complete use case 1, we will provide them a default api key they can copy and paste into the application to get around the basic plan subscription limitations
8. Instruct the user to duplicate the demo app tab. One tab will be the todo page and one tab will be the analytics page
9. Instruct the user to complete some todo actions (create, complete, archive, or delete) and watch one websocket graph update in real-time while the other responds with a five second delay
10. Guide the user back to APIM's policy design studio to review the latency policy employed which can be used for monetization use cases to restrict access to real-time data
11. Instruct user to modify the policy, redeploy the API, and test the impacts to the demo app
12. For users familiar with Kafka, explain how there is only one consumer group per subscription and how to create a new consumer group
13. Guide the user through creating a platform policy that creates a new consumer group every time the user refreshes the page
14. Educate the user on how and when different policies are applied across different phases

### Use Case 3: Advanced Security and Developer Portal

**Goal:** Require more involvement from the user, demonstrate security measures beyond a simple API key, and detail the developer portal

**Ideal time to complete:** 20-25 minutes

1. Select the use case&#x20;
2. (Optional) Start the respective pendo walkthrough in APIM
3. Documentation opens to relevant section
4. Docs provide high-level overview of demo app architecture (i.e., todo actions are tied to REST endpoints)
5. Explain sample monetization use case where we would like to charge the user per todo action (create, complete, archive, or delete) which requires more robust security then an API key
6. Guide the user to the gateway API in their trial (i.e., reference use case 1 which covers the basics of this gateway API)
7. Guide the user through creating a JWT plan with general conditions which contains pricing for each todo action. The user will simply generate the public/private key pair locally instead of involving an IdP
8. Guide the user to the dev portal and provide a brief overview. Detailed walkthrough of API consumer subscription process including methods of providing the applications client ID and agreeing to general conditions
9. Guide user to validate subscription in the dev portal. Educate user on options for managing subscriptions
10. Guide user to copy the JWT and configure it in the application
11. Guide user to policy design studio and walk them through adding and configuring the transform headers and assign metrics policy on the JWT plan
12. Guide the user through creating a custom graph based on the assign metrics policy.
13. Guide the user back to the demo app and instruct the user to complete some todo actions (create, complete, archive, or delete)&#x20;
14. Guide the user back to APIM to view their custom analytics graph. Educate the user on how this data could be integrated with an invoicing provider by taking advantage of the mAPI

## Prerequisites

These tutorials are designed to work seamlessly with our enterprise trial as they demonstrate a number of enterprise-only features. To get started with the free enterprise trial, simply follow the [instructions laid out here](../install-guides/free-trial.md). Setting up a new trial takes approximately five minutes and you can return here to select any of the following paths to experience the power of Gravitee API Management alongside our demo application:

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td></td><td><strong>Basic Security and Access Control</strong><br><br>This tutorial showcases Gravitee's core features which include securing a Gateway API, applying API access restrictions, and managing applications and subscriptions.<br><br><em>Gateway Architecture:</em> http-proxy<br><em>Entrypoint:</em> REST<br><em>Endpoint:</em> REST<br><em>Plan Security:</em> API Key<br><em>Policies:</em> Quota, Interrupt</td><td></td></tr><tr><td></td><td><strong>Real-time Data and Protocol Mediation</strong><br><br>This tutorial demonstrates Gravitee's ability to natively handle, and mediate between, both asynchronous and synchronous protocols.<br><br><em>Gateway Architecture:</em> message<br><em>Entrypoint:</em> Websocket<br><em>Endpoint:</em> Kafka<br><em>Plan Security:</em> None (temporary - shared API key support)<br><em>Policies:</em> Latency</td><td></td></tr><tr><td></td><td><strong>Advanced Policies and Security</strong><br><br>This tutorial details more advanced policies and security measures.<br><br><em>Gateway Architecture:</em> http-proxy<br><em>Entrypoint:</em> REST<br><em>Endpoint:</em> REST<br><em>Plan Security:</em> JWT<br><em>Policies:</em> Assign Metrics</td><td></td></tr></tbody></table>
