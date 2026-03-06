### Updating API Product Membership

To modify the APIs included in an API Product:

1. Retrieve the current product definition by sending a GET request to `/api-products/{productId}`.
2. Modify the `apiIds` array in the response to add or remove API IDs. All APIs must be V4 HTTP Proxy APIs with `allowedInApiProducts = true`.
3. Submit a PUT request to `/api-products/{productId}` with the updated `apiIds` array in the request body.
4. The system validates API eligibility and updates the `api_product_apis` table. The `updatedAt` timestamp is refreshed.

{% hint style="info" %}
Removing an API from a product does not invalidate existing subscriptions. New subscriptions will only grant access to the updated API set.
{% endhint %}
