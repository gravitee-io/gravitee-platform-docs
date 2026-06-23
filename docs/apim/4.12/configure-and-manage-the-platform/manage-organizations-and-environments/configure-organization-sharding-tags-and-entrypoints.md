# Configure Organization Sharding Tags and Entrypoints

## Gateway Configuration

1. In the Console, navigate to **Organization > Gateway > Entrypoints & Sharding Tags**.

2. Configure the default entrypoint values that will be displayed in the Developer Portal:
   * **Default HTTP entrypoint**: Enter the base URL (e.g., `https://api.company.com`)
   * **Default TCP port**: Enter the port number (e.g., `4082`)
   * **Default Kafka Bootstrap Domain Pattern**: Enter the domain pattern (e.g., `{apiHost}`)
   * **Default Kafka port**: Enter the Kafka port (e.g., `9092`)

    These values will be used according to the gateway configuration pattern shown in the helper text.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-06.png" alt="Organization settings page showing sharding tags table and entrypoint configuration fields"><figcaption></figcaption></figure>

3. Review the **Sharding Tags** section. The table displays existing sharding tags with their key, name, description, and restricted groups. Add the sharding tag's key to the API Gateway configuration file to manage API deployments.

4. To add a new sharding tag, click **+ Add a tag** in the Sharding Tags section.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-07.png" alt="Entrypoints and sharding tags page showing empty sharding tags table with add tag button"><figcaption></figcaption></figure>

5. Configure **Entrypoint Mappings** to define which entrypoint is displayed in the Developer Portal when an API has a given tag. Use **+ Add a mapping** to create new mappings between targets, entrypoints, sharding tags, and environments.
