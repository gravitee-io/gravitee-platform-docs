# Configure API Product Deployment

## Creating API Product Deployment Configuration

Navigate to **API Product → Deployment** to assign sharding tags to an API Product. The Deployment tab controls where the product is deployed by selecting one or more organization-level sharding tags.

1. Open the **Sharding Tags** dropdown. The dropdown lists all organization-level sharding tags with their names and optional descriptions.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-01.png" alt="API deployment configuration page showing sharding tags dropdown with 'shared' tag selected"><figcaption></figcaption></figure>

2. Select one or more tags from the dropdown. Only tags the current user is allowed to assign appear enabled—unrestricted tags for all users, and group-restricted tags only for members of those groups.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-04.png" alt="API Product deployment page showing sharding tags dropdown with 'external, internal' tags selected"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-06.png" alt="API Product deployment page showing sharding tags dropdown with 'internal' tag selected"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-07.png" alt="API Product deployment configuration page showing 'dit' tag selected in sharding tags dropdown"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-08.png" alt="Deployment configuration form with sharding tags dropdown showing 'internal' selected"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-09.png" alt="Deployment configuration form with sharding tags dropdown showing 'shared' selected"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-13.png" alt="Deployment configuration form with sharding tags dropdown expanded showing all three tag options selected"><figcaption></figcaption></figure>

3. If you select a restricted tag that you are not authorized to use, the system displays a validation error at the bottom of the page.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-03.png" alt="API Product deployment page showing restricted sharding tag selected with validation error message"><figcaption></figcaption></figure>

4. After selecting valid tags, click **Save** to persist the tags on the API Product definition. The system displays an unsaved changes notification until you save.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-14.png" alt="Deployment configuration page showing sharding tags dropdown with unsaved changes notification"><figcaption></figcaption></figure>

5. Once saved, a success message appears confirming the configuration was saved.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-11.png" alt="Deployment configuration page showing success message after saving configuration"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-16.png" alt="Deployment configuration page showing sharding tags dropdown with selected tag and success notification"><figcaption></figcaption></figure>

Saving tags marks the API Product as out of sync until deployed. An orange banner appears at the top of the page indicating "This API Product is out of sync."

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-02.png" alt="API Product deployment configuration page showing empty sharding tags dropdown with out of sync warning"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-12.png" alt="Deployment configuration form showing out of sync warning and multiple sharding tags selected"><figcaption></figcaption></figure>

6. To synchronize the updated tags and published plans to gateway instances, click **Deploy API Product** in the banner or header. A confirmation dialog appears.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-05.png" alt="Deploy API Product confirmation dialog with cancel and deploy buttons"><figcaption></figcaption></figure>

7. Click **Deploy** to complete the deployment. Gateway instances index and serve the product only when the product's tags match their configured sharding tags.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-10.png" alt="Deployment configuration form with empty sharding tags dropdown"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-15.png" alt="API Deployment configuration page showing empty sharding tags dropdown"><figcaption></figcaption></figure>

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding Tags** | Organization-level sharding tags assigned to the API Product. Dictates which gateway instances index and serve the product. | `eu`, `us-west` |

Member APIs linked to the product may become deployable on a gateway even when the API's own tags do not match, as long as the product and at least one published plan are eligible on that gateway.

Users with the `API_PRODUCT_DEFINITION:READ` permission can view the Deployment tab but cannot modify tags. Users without `API_PRODUCT_DEFINITION:UPDATE` permission see the sharding tag selector disabled.
