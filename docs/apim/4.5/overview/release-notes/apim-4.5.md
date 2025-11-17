# APIM 4.5.x

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

Gravitee API Management 4.5 improves the management of sync and async APIs across their entire lifecycle, including APIs from other API gateways or event brokers. Here's a summary of the highlights:

* New APIM policies for request/response validation and caching
* New Shared Policy Groups feature
* A new mTLS plan type
* More customization options for the new Developer Portal
* Three new federation agents, such that we now support discovery & ingestion of APIs and event streams from AWS API Gateway, Azure API Management, Apigee X, IBM API Connect , Solace, and Confluent Platform
* Federation discovery process improvements
* New API Score feature preview, for automated governance&#x20;

## Shared Policy Groups

Shared Policy Groups let you define a collection of policies in a central location and use them across multiple APIs. This makes it easier to implement similar policies across multiple APIs without introducing the risk of human error through repeated manual input. It also improves governance, by enabling you to ensure that all APIs implement certain policies that are critical to your organization.

<figure><img src="../../.gitbook/assets/image (131).png" alt=""><figcaption></figcaption></figure>

For example, you can use this feature to:

* Define a standard set of policies to shape traffic&#x20;
* Enforce security standards&#x20;
* Transform messages

The lifecycle of shared policy groups is independent from the deployment lifecycle of the APIs that they are used in. If you update the shared policy group, and then deploy it to the gateway, all APIs will pick up the changes without requiring a restart of the APIs.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXcoKhPtTopSLkMfTjumJh45pfl1YHyQaldlRED2s9yi9K--mScz9gjxLfFo8OLK_jUfFMr6wKgzcMFCIAikIuBAXr7aq2y1LvRZO6JZQKlRQ_5T2MzQyjtCFil39nezPbfQf5OdtIj09EJEuPgmd_oAf-OA?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

For more information about Shared Policy Groups, See [Shared Policy Groups](../../using-the-product/using-the-gravitee-api-management-components/general-configuration/shared-policy-groups/README.md).

## mTLS Plans

The new mTLS plan relies on mutual TLS to authenticate a consuming application with the Gravitee Gateway. This works by allowing you to set a client certificate at the application level and use that certificate as the credential for the API plan. You can still use mTLS plans even if you don't want to terminate SSL on your gateway, for instance if TLS is already terminated by your Kubernetes ingress.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXeUxuu-YcJTVfs8X0SHdpewdTF9CKwd15g8rG6i2pE9ebl6glHbHQhEPImNxfl6GWeu5EjEEpDiorQSXiKc9AnR9p83n39Ds3Rgc1Wr8f3tXydneG9UhTsdey-hPRjG8efAJkZATw6Gz1uFN6W4oTId_BsT?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>



Before this update, you could set up the Gravitee gateway to require client authentication for all incoming requests, and then use the gateway truststore to verify that only authorized clients are allowed to connect to the Gateway.&#x20;

With this update, the mTLS plan enhances this authentication by using the client certificate to authorize requests to APIs using the plan.

For more information about mTLS Plans, see [mTLS Plans](../../using-the-product/managing-your-apis/preparing-apis-for-subscribers/plans/mtls/README.md).

## Developer Portal enhancements

{% hint style="info" %}
The new developer portal is in tech preview. Tech preview features are fully supported for Gravitee’s enterprise customers. The Tech Preview label indicates that the feature is under development, and further changes may occur in an upcoming release.
{% endhint %}

You can now customize the new Gravitee developer portal with ease, matching your branding and fonts by means of a dedicated application.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXc2S2cGIxguBfgooGccff4MpbgfKO9YjOGu6T283bqREzXi4faaMICWgAZNvrxpHFnx7SmA1f0auY5WVpaiawCugz4ZRkkeF6sdfqvG30evbGGipak-734EEBco3yZBUsyrbwHl05xdW6dEM-ozL7dBy74?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

With this update, we have added the following features:

* Support for subscriptions to all plan types
* A dedicated UI for customization and configuration
* Application-level logs for subscribed APIs that can be filtered and analyzed
* Customizable menu links and an optional banner with additional links.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXdmAhCXYftgHnJzYP6K0oH9Fdw0mvQAWmFIsFisP1vTHL9WPCnH3n4yMy-JpzA539b8mS3W59LgrnMlPfc4faw93O5fcJZxG6B9ZfV926XWHiUpwyV7fAXkpQyK-p2_rRnhgDIyaBxnOpW2cW0F_9cVrTPF?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

## v4 API Documentation enhancements

Gravitee  continues to bring the latest version of its API functionality to full parity and provides enhancements along the way. With this update, we have added the ability to fetch a page from a remote source like GitHub, GitLab, or a remote URL on a configured cadence.&#x20;

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXdQ9ratbE1eK71AiL_86Z1nIcaZNT7iNtbu6Q-x4fpw9xwJTRW9p_emI3SFz8_gGjqlLpkC7OTb3eQWjcacwHOUD5ppxhz3SKu_CVlDKdKrCysq7pKkfP-LNXEKDtmuBpxsKhE3PAa5L0uZGz8q8yJhY6O5?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

Also, we have set aside the homepage for an API into its own configuration section so that it is easier to create and maintain. Pages fetched from a remote location are now provided in read-only mode with an on-demand preview option, so changes are applied consistently from the source.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXdKdQy5b9PYmA_LEOvwpIF1mtQGMPP772JuhYZN8Rpwa9pYc8o5nSfapuLxbOcttwl_76WHv74vLSdY2KTGbzZpAnk3mpjyVfLGz_JLWahHiCfQUYx7QWeld3kPLgxn6zSAmoLSIuZo8MD583f5FS7C3zpG?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

## OAS Validation Policy

You can use the OAS Validation policy to validate a request to an API or the response from the backend against the OpenAPI specification. You can enforce that requests follow the specification, and provide many options for the elements can be validated. For example, headers, body, and parameters Also, during the creation workflow, you can also add the policy to all flows automatically when importing an OpenAPI Specification as a v4 API.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXfdJX7iMRI4_bbilxyDv1SFoBDNpZR9DaGwYNRWcZ7tp5-XD-OYVLMn36whF_5c-WVmDgfr2BLb3Z697eiOWgmjSd4UfKMgbL-AOSGHeDbk9ygkIxbfPiZUDj5JwL1xbKsq1JpjvgxVsyuheiMfATr1xPyd?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

## Azure, IBM, and Confluent federation providers

Federation enables the creation of a unified catalog and developer portal for APIs and event streams from any 3rd-party platform.&#x20;

<figure><img src="../../.gitbook/assets/image (132).png" alt=""><figcaption></figcaption></figure>

With 4.5, we’re excited to announce that federation is now generally available and includes multiple enhancements:

* New providers for Azure API Management, IBM API Connect, and Confluent Platform. You can ingest APIs and event streams from these different providers into Gravitee. For Confluent, Gravitee will create one API per discovered Kafka topic, and will associate an AsyncAPI definition to each API based on the topic and associated schemas from the schema registry
* User permissions on integrations - use groups and roles to determine what actions users can or cannot complete with integrations in APIM.
* Enhancements to API discovery - when running the discovery process for an integration, you see a preview of all the APIs that were discovered and manage updates to existing ingested APIs.
* Improvements to the AWS, Solace and Apigee providers - additional metadata is ingested into Gravitee.

## API Score preview

API Score is a new automated governance feature that will provide a quality score for each of your APIs based on your company's quality, security, and consistency criteria. Whether your APIs are deployed to Gravitee, synchronous or asynchronous, or discovered from external providers like AWS, Azure, Apigee, IBM, Solace or Confluent, API score will provide you with a dashboard that provides instant feedback about the level of conformance of APIs across your environment.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXdLcbQjWdXWbsq2Dz0LfM9rFj0l52jR1ij1Ealve34-sSzgE76PU9Dj_doD_MzAxNGM6s2aP-6pbgJrzFLXZ1Fod44TyUUT02Yq4xnXLC5k9ynrrhugRGLek-y9YnwvQwnRDIy23N9Z1Y8IqEr1Qr41cNRm?key=jMTPU2NFoSjiJjsY4xlu6w" alt=""><figcaption></figcaption></figure>

You can specify your own custom rules that will be used to evaluate the OAS and AsyncAPI specifications attached to your APIs in Gravitee.&#x20;

Because this feature is a technical preview, we asked that you reach out to the Gravitee team in order to activate it on your environment.&#x20;

{% hint style="info" %}
API Score is a new service that requires a Gravitee Cloud account and an APIM instance that is connected to Gravitee Cloud.
{% endhint %}

## Updates to the APIM v2-v4 Comparison Matrix

With APIM 4.5, we’ve continued to reduce the delta between our functionality on previous API versions and the latest version. The latest matrix of comparison between the versions is as follows:

| Functionality                                                     | Supported in v2 proxy APIs | Supported for v4 proxy APIs | Supported for v4 message APIs |
| ----------------------------------------------------------------- | -------------------------- | --------------------------- | ----------------------------- |
| User Permissions                                                  | ✅                          | ✅                           | ✅                             |
| Properties                                                        | ✅                          | ✅                           | ✅                             |
| Resources                                                         | ✅                          | ✅                           | ✅                             |
| Notifications                                                     | ✅                          | ✅                           | ✅                             |
| Categories                                                        | ✅                          | ✅                           | ✅                             |
| Audit Logs                                                        | ✅                          | ✅                           | ✅                             |
| Response Templates                                                | ✅                          | ✅                           | ✅                             |
| CORS                                                              | ✅                          | ✅                           | ✅                             |
| Virtual Hosts                                                     | ✅                          | ✅                           | ✅                             |
| Failover                                                          | ✅                          | ✅                           | ⚠️ Depends on use case        |
| Health Check                                                      | ✅                          | ✅                           | 🚫                            |
| Health Check Dashboard                                            | ✅                          | 🚫                          | 🚫                            |
| Service Discovery                                                 | ✅                          | 🚫                          | 🚫                            |
| Improved Policy Studio                                            | 🚫                         | ✅                           | ✅                             |
| Debug Mode                                                        | ✅                          | 🚫                          | 🚫                            |
| Plans                                                             | ✅                          | ✅                           | ✅                             |
| Subscriptions                                                     | ✅                          | ✅                           | ✅                             |
| Messages / Broadcasts                                             | ✅                          | ✅                           | ✅                             |
| Documentation - Markdown                                          | ✅                          | ✅                           | ✅                             |
| Documentation - OAS                                               | ✅                          | ✅                           | ✅                             |
| Documentation - AsyncAPI                                          | ✅                          | ✅                           | ✅                             |
| Documentation - AsciiDoc                                          | ✅                          | 🚫                          | 🚫                            |
| Documentation - Home Page                                         | ✅                          | ✅                           | ✅                             |
| Documentation - Metadata                                          | ✅                          | ✅                           | ✅                             |
| Documentation - Translations                                      | ✅                          | 🚫                          | 🚫                            |
| Documentation - Group Access Control                              | ✅                          | ✅                           | ✅                             |
| Documentation - Role Access Control                               | ✅                          | 🚫                          | 🚫                            |
| Documentation - Swagger vs. Redoc Control                         | ✅                          | ✅                           | ✅                             |
| Documentation - Try It Configuration                              | ✅                          | ✅                           | ✅                             |
| Documentation - Nested Folder Creation                            | ✅                          | ✅                           | ✅                             |
| Terms & Conditions on a Plan                                      | ✅                          | ✅                           | ✅                             |
| Tenants                                                           | ✅                          | 🚫                          | 🚫                            |
| Sharding Tags                                                     | ✅                          | ✅                           | ✅                             |
| Deployment History                                                | ✅                          | ✅                           | ✅                             |
| Rollback                                                          | ✅                          | ✅                           | ✅                             |
| Compare API to Previous Versions                                  | ✅                          | ✅                           | ✅                             |
| Analytics                                                         | ✅                          | ⚠️ WIP                      | ⚠️ WIP                        |
| Custom Dashboards                                                 | ✅                          | 🚫                          | 🚫                            |
| Path Mappings                                                     | ✅                          | 🚫                          | 🚫                            |
| Logs                                                              | ✅                          | ✅                           | ✅                             |
| API Quality                                                       | ✅                          | ⚠️ Replaced by API score    | ⚠️ Replaced by API score      |
| API Review                                                        | ✅                          | ✅                           | ✅                             |
| Export API as Gravitee def (+options)                             | ✅                          | ✅                           | ✅                             |
| Export API as GKO spec                                            | ✅                          | ✅                           | ✅                             |
| Import API from Gravitee def (+options)                           | ✅                          | ✅                           | ✅                             |
| Import API from OAS                                               | ✅                          | ✅                           | NA                            |
| Import API from OAS and automatically add policies for validation | ✅                          | ✅                           | <p>NA</p><p><br></p>          |
| Import API from WSDL                                              | ✅                          | 🚫                          | NA                            |
| Add docs page on import of API from OAS                           | ✅                          | ✅                           | NA                            |
| APIs show in platform-level dashboards                            | ✅                          | 🚫                          | 🚫                            |
| APIs show in platform-level analytics                             | ✅                          | 🚫                          | 🚫                            |
| APIs alerts                                                       | ✅                          | 🚫                          | 🚫                            |

## Wrapping Up

We’re extremely proud of this release at Gravitee and we look forward to hearing your feedback! Don’t hesitate to contact us with any questions or feedback.&#x20;

\


\
\
