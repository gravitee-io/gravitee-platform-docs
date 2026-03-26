---
description: An overview about default ai flows overview.
---

# Default AI flows overview

By default, Gravitee APIM 4.5 has three shared policy groups that empowers AI use cases. These policy groups can be chained together to support LLM proxy use cases. For example, prompt templating, prompt security, and LLM rate limiting.

Here are the default shared policy groups:

* **Rate Limit & Request token limit**: This policy limits the number of requests and number of tokens sent in a request. To use this policy, set context attributes prompt, maxTokens, and maxRequests.
* **Prompt Templating Example**: Uses the Assign Content policy to create and enhance a prompt from external data.
  * In this example, the shared policy group takes an input field of **ip** in the request body and adds it as an attribute.
  * It runs an HTTP Callout policy to find the IP address set in the context attribute and return its country and city as context attributes.
  * From the context attributes, it crafts a prompt in the Assign Attributes policy.
* **Redirect to HuggingFace**: This policy group crafts the body of a request to HuggingFace, which includes model parameters and options, and then it sends that request to a Dynamic Routing policy that redirects to HuggingFace.

You can use these shared policy groups together to build an LLM proxy for prompt templating and rate limiting. Also, you can edit these shared policy groups to match your needs.

You can delete these shared policy groups if you do not wish to have them. If you delete them, they will not return in that environment.

\\
