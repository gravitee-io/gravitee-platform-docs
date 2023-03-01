# Overview

You can use response templates to override the default values sent in
response to consumer calls to an API.

Response template overrides are triggered by *error keys*, which are
specific to policies. Each response template defines the new values to
be returned for one or more status codes when the template is triggered.

For the full list of policy error keys for which you can override the
values, see the [???](#Policy error keys you can override) table below.

## Global response templates

As well as creating templates associated with a specific error key, you
can create two types of global templates for an API:

-   Templates with a template key of `DEFAULT`, which are always
    triggered, regardless of the error key

-   Templates with one of a set of error keys which are not
    policy-specific and are triggered in specific circumstances, such as
    an invalid request or response (designated in
    [???](#Policy error keys you can override) as applying to all
    policies)

# Before you begin

Before you can define response templates for your API, you need to know:

-   which policies are defined in the API plans associated with your API
    (see link:{{
    */apim/3.x/apim\_publisherguide\_plans\_subscriptions.html* |
    relative\_url }}\[Plans and subscriptions^\])

-   which error keys you can override for the policies associated with
    your API plans (see [???](#Policy error keys you can override))

# Configure a response template

You can define:

-   multiple templates for one API (for multiple policies and/or
    multiple error keys sent by the same policy)

-   multiple template definitions for the same error key in a single
    template (for different content types or status codes)

To configure a response template:

1.  link:{{ */apim/3.x/apim\_quickstart\_console\_login.html* |
    relative\_url }}\[Log in to APIM Console^\].

2.  Click **APIs** and select the API.

3.  Click **Proxy &gt; Response Templates**.

4.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] to add a new template.

5.  Select the **Template key**. This can be either:

    -   one of the error keys associated with the policy (see the
        [???](#Policy error keys you can override) table below for more
        details)

    -   `DEFAULT`, applying to all errors returned (as long as they
        correspond to the content type specified in the next step)

    -   one of the global error keys (keys described as applying to all
        policies in the [???](#Policy error keys you can override)
        table)

        image:{% link
        images/apim/3.x/api-publisher-guide/response-templates/template-key.png
        %}\[\]

6.  To send the template override values only for JSON or XML requests,
    specify `JSON` or `XML` as the **Content type**. The default value
    `\*/*` applies to all content types.

7.  Specify the status code for which the new values are sent.

8.  Specify the override values to send to the API consumer, which can
    be one or more of the following:

    -   one or more HTTP headers to include in the response

    -   body of the response

    image:{% link
    images/apim/3.x/api-publisher-guide/response-templates/template-vals.png
    %}\[\]

9.  Click **ADD A NEW REPONSE TEMPLATE** to add more templates for the
    same error key, then repeat the previous three steps.

10. Click **SAVE**.

11. Click the **deploy your API** link with the changes.

    image:{% link
    images/apim/3.x/api-publisher-guide/response-templates/template-deploy.png
    %}\[\]

The next time a call triggering the error associated with your template
is sent to the API, the consumer will see the override values.

# Policy error keys you can override

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Key</p></td>
<td style="text-align: left;"><p>Policy</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>API_KEY_MISSING</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_apikey.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[API key]</p></td>
<td style="text-align: left;"><p><code>API_KEY_INVALID</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_apikey.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[API key]</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>QUOTA_TOO_MANY_REQUESTS</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_rate_limiting.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[Rate limiting]</p></td>
<td
style="text-align: left;"><p><code>RATE_LIMIT_TOO_MANY_REQUESTS</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_rate_limiting.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Rate limiting]</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>REQUEST_CONTENT_LIMIT_TOO_LARGE</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_request_content_limit.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[Request content
limit]</p></td>
<td
style="text-align: left;"><p><code>REQUEST_CONTENT_LIMIT_LENGTH_REQUIRED</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_request_content_limit.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Request content
limit]</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>REQUEST_TIMEOUT</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_mock.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[Mock], link:{{
<em>/apim/3.x/apim_policies_callout_http.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Callout HTTP], link:{{
<em>/apim/3.x/apim_policies_request_validation.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[Request
validation]</p></td>
<td
style="text-align: left;"><p><code>REQUEST_VALIDATION_INVALID</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_request_validation.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Request
validation]</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>RESOURCE_FILTERING_METHOD_NOT_ALLOWED</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_resource_filtering.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[Resource
filtering]</p></td>
<td
style="text-align: left;"><p><code>RBAC_INVALID_USER_ROLES</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_role_based_access_control.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Role-based access
control]</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>RESOURCE_FILTERING_FORBIDDEN</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_resource_filtering.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[Resource
filtering]</p></td>
<td style="text-align: left;"><p><code>RBAC_FORBIDDEN</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_role_based_access_control.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[Role-based access
control]</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>RBAC_NO_USER_ROLE</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_role_based_access_control.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[Role-based access
control]</p></td>
<td
style="text-align: left;"><p><code>OAUTH2_MISSING_SERVER</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>OAUTH2_MISSING_HEADER</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
<td
style="text-align: left;"><p><code>OAUTH2_MISSING_ACCESS_TOKEN</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>OAUTH2_INVALID_ACCESS_TOKEN</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
<td
style="text-align: left;"><p><code>OAUTH2_INSUFFICIENT_SCOPE</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>OAUTH2_INVALID_SERVER_RESPONSE</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
<td
style="text-align: left;"><p><code>OAUTH2_SERVER_UNAVAILABLE</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_oauth2.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[OAuth2]</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>HTTP_SIGNATURE_INVALID_SIGNATURE</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_http_signature.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[HTTP
Signature]</p></td>
<td style="text-align: left;"><p><code>JWT_MISSING_TOKEN</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_jwt.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[JWT]</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>JWT_INVALID_TOKEN</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_jwt.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[JWT]</p></td>
<td
style="text-align: left;"><p><code>JSON_INVALID_PAYLOAD</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_json_validation.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[JSON
validation]</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>JSON_INVALID_FORMAT</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_json_validation.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[JSON
validation]</p></td>
<td
style="text-align: left;"><p><code>JSON_INVALID_RESPONSE_PAYLOAD</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_json_validation.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[JSON
validation]</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>JSON_INVALID_RESPONSE_FORMAT</code></p></td>
<td style="text-align: left;"><p>link:{{
<em>/apim/3.x/apim_policies_json_validation.html</em></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>relative_url }}[JSON
validation]</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_INVALID_REQUEST</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_INVALID_RESPONSE</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_OAUTH2_ACCESS_DENIED</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_OAUTH2_SERVER_ERROR</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_OAUTH2_INVALID_CLIENT</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_MISSING_SECURITY_PROVIDER</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_PLAN_UNRESOLVABLE</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>All</p></td>
<td
style="text-align: left;"><p><code>GATEWAY_POLICY_INTERNAL_ERROR</code></p></td>
</tr>
</tbody>
</table>
