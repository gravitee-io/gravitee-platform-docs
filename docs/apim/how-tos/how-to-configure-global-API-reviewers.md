# How to configure global API reviewers

## Overview

This document describes how you can easily configure a group of global reviewers instead of manually adding reviewers as a member of each API.

## API reviews

In the APIM Console, you can configure API reviewers. They can check various aspects of the API, such as:

* Documentation
* Versioning
* Endpoints

API reviews can be requested by the API owner. When their review is complete, reviewers can accept or reject the API. If reviewers reject the API, its owner knows the API needs some changes.

API reviewers must have access rights to an API to review it.

## Prerequisites

You first need to enable the **Enable API review** option in the APIM Console in **Settings > API Quality**.

You also need a `REVIEWER` role with at least the following permissions:

* **Scope**: API
* Permissions:
  * **ALERT**: READ
  * **DEFINITION**: READ
  * **DISCOVERY**: READ
  * **DOCUMENTATION**: READ
  * **GATEWAY\_DEFINITION**: READ
  * **METADATA**: READ
  * **NOTIFICATION**: READ, UPDATE
  * **PLAN**: READ
  * **QUALITY\_RULE**: CREATE, READ, UPDATE
  * **REVIEWS**: CREATE, READ, UPDATE, DELETE

APIM comes with a default `REVIEWER` role that includes all these conditions.

## Configuration

1. In APIM Console, click **Settings > Groups** and click the plus icon ![](../../../images/icons/plus-icon.png) to create a new group: ![Create a group](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/graviteeio-how-to-configure-global-api-reviewers-configuration-1.png)
2. Give it a name (for example, **Global Reviewers**).
3. Select the **Associate automatically to every new API** option.
4. Click **CREATE**.
5. Give a name to the group: ![Give a name to the group](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/graviteeio-how-to-configure-global-api-reviewers-configuration-2.png).
6. Select a reviewer role in the **Default API role** dropdown list (e.g. `REVIEWER`).
7. Click **UPDATE**.
8. Choose default API role: ![Choose default API role](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/graviteeio-how-to-configure-global-api-reviewers-configuration-3.png)
9. Click **ASSOCIATE TO EXISTING APIS**: ![Associate group to existing APIs](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/graviteeio-how-to-configure-global-api-reviewers-configuration-4.png)
10. In the **Dependents** section, click the plus icon followed by the users icon to add users to the group, checking that their API role is correct. ![Add users](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/add-users.png) ![Add users](../../../images/apim/3.x/how-tos/configure-global-API-reviewers/graviteeio-how-to-configure-global-api-reviewers-configuration-5.png)
11. Click **UPDATE**.

## Result

With this configuration:

* Your new group is attached to all existing APIs.
* Your new group will be attached to every new API.
* All the reviewers in this group (with a configured email address) are notified by email when a review is requested on an API.

You do not need to add new reviewers to every API or add every reviewer to new APIs.

You can still add specific reviewers to a specific API. They will also be notified by email when a review is requested on this API.
