### Creating an API Product

To create an API Product:

1. Verify the product name is unique within the environment by sending a POST request to `/api-products/_verify` with the following JSON body:

   ```json
   {
     "name": "string"
   }
   ```

   The endpoint returns:

   ```json
   {
     "ok": boolean,
     "reason": "string"
   }
   ```

2. Ensure all APIs you plan to include are V4 HTTP Proxy APIs with `allowedInApiProducts` set to `true`. Only APIs meeting these criteria can be added to API Products.

3. Send a POST request to `/api-products` with a JSON body containing the following fields:

   ```json
   {
     "name": "string",          // Required, must be unique within environment
     "version": "string",       // Required
     "description": "string",   // Optional
     "apiIds": ["string"]       // Optional, list of API IDs
   }
   ```

   The system assigns a unique `id` and sets `createdAt` and `updatedAt` timestamps.

4. The product appears in the API Products navigation list.

5. Configure plans for the product using the plans API with `referenceType` set to `API_PRODUCT` and `referenceId` set to the product ID.

### Creating a Subscription to an API Product

Consumers subscribe to API Products through the application subscription workflow:

1. Navigate to the application and initiate subscription creation.
2. Select the API Product from the subscription dialog. Products are labeled "API Product" in the reference type column.
3. Choose a plan associated with the product.
4. Submit the subscription request. The system creates a subscription with `referenceType` set to `API_PRODUCT` and `referenceId` set to the product ID.
5. If the plan uses API Key security, the system generates keys linked to the product subscription.
6. The subscription grants access to all APIs bundled in the product.
