# v4 Proxy API Entrypoints

## Configuration

To alter v4 Proxy API entrypoints, select your API, and then select **General** from the **Entrypoints** category in the left-hand nav.

<figure><img src="../../../../../../../.gitbook/assets/virtual host_on (1) (1).png" alt=""><figcaption><p>v4 proxy API entrypoint configuration</p></figcaption></figure>

From here, you can:

* Alter existing entrypoints by changing the context path
* Add a new entrypoint by clicking **Add context path** and then adding a new context path
* Delete existing entrypoints by clicking the <img src="../../../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.51.56 AM (1).png" alt="" data-size="line"> icon associated with the entrypoint that you want to delete
* Choose to enable or disable virtual hosts. Enabling virtual hosts requires you to define your virtual host and optionally enable override access.

When you are done, make sure to redeploy the API for your changes to take effect.
