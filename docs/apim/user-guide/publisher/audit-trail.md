# Overview

You can use the APIM audit trail for monitoring the behaviour of your
API and platform over time. For example, you can use it in conjunction
with the analytics feature to identify a point at which your API
behavior changed, view the configuration which caused the change and
roll back to an earlier configuration if required.

See also: link:{{
*/apim/3.x/apim\_publisherguide\_logging\_analytics.html* |
relative\_url }}\[Logging and analytics\]

APIM Console provides audit trails at two levels of granularity:

-   A platform-wide audit trail, which you can view with the **Audit**
    menu option:

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/global-audit.png %}\[\]

-   An API-specific audit trail, which you can view with the API
    **Audit** menu option in APIM Console:

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/api-audit.png %}\[\]

The sections below focus on the API audit trail.

# API audit trail

You can use the API audit trail to:

-   view a list of API events, filtered by event type and date, with a
    toggle to show and hide the JSON associated with the event

-   view a history of API deployments, including details of the
    configuration each deployment, a diff feature for comparing
    deployments and a rollback feature for rolling back the API to an
    earlier stage

-   view a visual map of API events

# API history

You can use the history feature of the audit trail to view the different
stages of the API lifecycle and their associated configuration.

Each stage corresponds to a new deployment of the API, with a number and
a label (if specified at deployment time) identifying the deployment:

image:{% link
images/apim/3.x/api-publisher-guide/audit/history-overview.png %}\[\]

## View the details of an API deployment

1.  In the API **Audit** page, click **History**.

2.  Select the API deployment to see more details.

3.  Select a flow and click through the tabs to see its configuration
    details. In the **DESIGN** tab, you can select a policy to view
    details of the policy configuration.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-history-details.png
    %}\[\]

4.  To view the deployment configuration in JSON format, toggle **Mode**
    to **Definition**.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-definition-mode.png
    %}\[\]

5.  To copy the deployment configuration in JSON format, click **COPY TO
    CLIPBOARD**. You can do this in either definition or design mode.

6.  To view a diff of the deployment configuration, click **DIFF** and
    select another deployment stage to view the difference between the
    two deployments. If this is not the latest deployment, you can also
    click **DIFF WITH PUBLISHED API** to view the difference with the
    latest deployment. The numbers in green and red at the top indicate
    the number of additions to and subtractions from the definition.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-history-diff.png
    %}\[\]

## Roll back your API to an earlier deployment

You can roll back to an earlier deployment of your API. This does not
remove the later deployments, it adds a new deployment in the history
with a configuration which corresponds to the deployment selected for
rollback.

1.  Open the API history as described above.

2.  Click the API deployment to roll back to.

3.  Click **ROLLBACK** and confirm in the prompt.

4.  To complete the rollback, select the new rollback deployment and
    click **DEPLOY**.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-history-rollback.png
    %}\[\]

    To view a diff of the deployment before deploying, you can use the
    diff feature as described above.

5.  (Optional) Add a deployment label to identify to the new deployment.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-history-rollback-deployment-label.png
    %}\[\]

6.  Click **OK**.

    APIM adds a new deployment to the history.

    image:{% link
    images/apim/3.x/api-publisher-guide/audit/audit-history-rollback-deployment.png
    %}\[\]
