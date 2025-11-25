---
description: Overview of Define.
---

# Define an APIM service account for GKO

The best way to provide credentials for GKO to connect to your APIM installation through a ManagementContext is to create a service account in the Gravitee API Management console dedicated to GKO.

To do this, head to the organisation settings in APIM, create a new user, and choose **Service Account**.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

The service account email is optional.

Next, ensure that this service account has the ADMIN role on the organization, and the API\_PUBLISHER role on the desired environment. This will provide GKO with the minimum set of required permissions in order to be able to manage APIs, applications, and other required assets in APIM.

<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

The screenshot below shows the environment-level permissions included in the API\_PUBLISHER role.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

From the newly created service account, scroll to the **Tokens** section at the bottom of the page and create a new token:

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

Make sure to immediately copy your new personal access token as you won’t be able to see it again.

You can now use this token as credentials in a `ManagementContext` like so:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-mgmt-ctx
spec:
  baseUrl: http://localhost:8083
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    bearerToken: xxxx-yyyy-zzzz
```
