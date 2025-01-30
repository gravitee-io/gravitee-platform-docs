# Define an APIM service account for GKO

<<<<<<< HEAD
The best way to provide credentials for GKO to connect to your APIM installation through a ManagementContext is to create a service account in the Gravitee API Management console dedicated to GKO.

To do this, head to the organisation settings in APIM, create a new user, and choose **Service Account**.

<<<<<<<< HEAD:docs/gko/4.6/guides/define-an-apim-service-account-for-gko.md
<figure><img src="../../4.4/.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>
========
<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>
>>>>>>>> parent of 87f43e23 (GitBook: No commit message):docs/gko/4.x/guides/define-an-apim-service-account-for-gko.md

The service account email is optional.

Next, ensure that this service account has the ADMIN role on the organization, and the API\_PUBLISHER role on the desired environment. This will provide GKO with the minimum set of required permissions in order to be able to manage APIs, applications, and other required assets in APIM.

<<<<<<<< HEAD:docs/gko/4.6/guides/define-an-apim-service-account-for-gko.md
<figure><img src="../../4.4/.gitbook/assets/image (15) (1).png" alt=""><figcaption></figcaption></figure>

The screenshot below shows the environment-level permissions included in the API\_PUBLISHER role.

<figure><img src="../../4.4/.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

From the newly created service account, scroll to the **Tokens** section at the bottom of the page and create a new token:

<figure><img src="../../4.4/.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>
========
=======
The best way to provide credentials for GKO to connect to your APIM installation through a ManagementContext is to create a service account in the Gravitee API Management console dedicated to GKO.&#x20;

To do this, head to the organisation settings in APIM, create a new user, and choose **Service Account**.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

The service account email is optional.&#x20;

Next, ensure that this service account has the ADMIN role on the organization, and the API\_PUBLISHER role on the desired environment. This will provide GKO with the minimum set of required permissions in order to be able to manage APIs, applications, and other required assets in APIM.

>>>>>>> parent of 87f43e23 (GitBook: No commit message)
<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

The screenshot below shows the environment-level permissions included in the API\_PUBLISHER role.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

From the newly created service account, scroll to the **Tokens** section at the bottom of the page and create a new token:

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>
<<<<<<< HEAD
>>>>>>>> parent of 87f43e23 (GitBook: No commit message):docs/gko/4.x/guides/define-an-apim-service-account-for-gko.md
=======
>>>>>>> parent of 87f43e23 (GitBook: No commit message)

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
