# policies-migrate

## Overview

This page explains how to migrate your existing API to Design Studio. It also summarizes the differences between the APIM Console **Design** function and Design Studio.

## Migrate an API

1. Log in to APIM Console.
2. Click **APIs**.
3.  Select your API and click **Design**.

    image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-policy-studio-before-migration.png %\}\[]
4.  Click the migrate button.

    image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-policy-studio-migration-button.png %\}\[]

    You are redirected to Design Studio.

    image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-policy-studio-migrated.png %\}\[]

## Differences between Design function and new Design Studio

With the **Design** function, HTTP methods were linked directly to policies. With Design Studio, HTTP methods are linked to a flow. This means that you could have a path with policies linked to different HTTP Methods. The migration transforms each "Path"-"HTTP methods"-"Policy" into one flow.

By default, the selection of a flow is based on the operator defined in the flow itself.

You can use the operator either to select a flow with a path which matches exactly, or when the start of the path matches. You can then use the **Best match** option to select the flow from the path that is closest.

image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-policy-studio-best-match.png %\}\[]
