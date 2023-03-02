# Overview

Platform flows are executed before and after any API flows of the
organization. They can be defined in the organization settings and are
automatically deployed on every change.

image:{% link images/apim/3.x/adminguide/platform-flows.png %}\[\]

# Execution flow

Platform flows are encapsulating API flows as follows:

-   Platform flow request policies are executed **before** API flow
    request policies

-   Platform flow response policies are executed **after** API flow
    response policies

# Typical use cases

You can use platform flows to enforce policies at the organization level
such as:

-   reporting - e.g. Metrics Reporter

-   security - e.g. IPFiltering

# Known limitations

Platform flows do currently not support conditional policies.
