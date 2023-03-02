# policies-overview

## Overview

APIM is delivered with some default common _policies_, for standard APIM usage. You can also customize APIM by adding your own policies. The default APIM policies are described in this section.

You can configure these policies in two ways:

* Using the API **Design** function:

image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-old-studio-overview.png %\}\[]

* Using Design Studio (available from APIM 3.5.x):

image::\{% link images/apim/3.x/api-publisher-guide/policies/graviteeio-policy-studio-overview.png %\}\[]

You can migrate from the former **Design** function to Design Studio by following link:\{{ _/apim/3.x/apim\_policies\_migrate.html_ | relative\_url \}}\[this procedure].

## Ant notation

APIM frequently uses Ant notation for path matching:

* `?` matches one character
* `\*` matches zero or more characters
* `**` matches zero or more directories in a path

## See also

For details of how policies are defined and used in APIM, see also:

* link:\{{ _/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html_ | relative\_url \}}\[Plans and subscriptions^] in the API Publisher Guide to learn how to configure policies for API plans in APIM Console
* link:\{{ _/apim/3.x/apim\_publisherguide\_expression\_language.html_ | relative\_url \}}\[Expression Language^] in the API Publisher Guide to learn more about using the Gravitee Expression Language with policies
* link:\{{ _/apim/3.x/apim\_devguide\_policies.html_ | relative\_url \}}\[Policies^] in the Developer Guide to learn how to create custom policies
* link:\{{ _/apim/3.x/apim\_devguide\_plugins.html_ | relative\_url \}}\[Plugins^] in the Developer Guide to learn how to deploy plugins (of which policies are one type)
* link:\{{ _/apim/3.x/apim\_adminguide\_platform\_policies.html_ | relative\_url \}}\[Platform policies^] in the Admin Guide to learn how to use policies at the organization level

Before you use this reference, we recommend you read link:\{{ _/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html_ | relative\_url \}}\[Plans and subscriptions^] in the API Publisher Guide to understand how policies work in APIM.
