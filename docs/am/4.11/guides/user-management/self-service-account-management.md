# Self-service Account Management

## Overview

AM self-service account management allows users to manage their accounts with the following capabilities :

* Read and manage their account information.
* List user activities.
* Request to change passwords.
* Manage Multi-factor Authentication (MFA) devices.
* Manage Passwordless credentials.

{% hint style="info" %}
By default, these actions are possible only during the login process, but in order to provide a **My Account** space for your end-users, AM includes a REST API to perform all these requests.
{% endhint %}

To access the online API reference, go to [the API reference](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.5.x/docs/self-service-account-api-descriptor.yml).

## Management API Endpoints

### Certificate Settings

Configure domain-level certificate settings using the Management API.

**Endpoint**: `PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`

**Required Permission**: `DOMAIN_SETTINGS[UPDATE]`

**Request Body**:

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `fallbackCertificate` | String | No | ID of the certificate to use as fallback when primary certificate fails |

**Response**: Returns the updated certificate settings object.

**Validation Rules**:
- Fallback certificate must exist in the domain's certificate repository
- Fallback certificate must belong to the same domain (unless domain is master)
- Fallback certificate ID cannot match the primary certificate ID

## Configure the self-service account management

By default, the self-service account management is **disabled** for every security domain.

{% hint style="info" %}
Self-service account API is deployed at `http(s)://AM_GW_HOST/{domain}/account/api/**` and secured with OAuth 2.0 protocol.
{% endhint %}

To configure the self-service account settings :

1. Log in to AM Console.
2. Select your security domain and click **Settings > Self-service account**.
3. Configure your settings and click **SAVE**.
