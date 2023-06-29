# Gravitee.io Cockpit

## Overview

Gravitee Cloud is a centralized, multi-environment tool for managing
all your Gravitee API Management and Access Management installations in
a single place.

image::{% link images/cockpit/cockpit-dashboard.png %}\[\]

## Gravitee Cloud hierarchy

Gravitee Cloud is based on a hierarchy of the following entity types:

image::{% link images/cockpit/entity-hierarchy.png %}\[\]

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Entity</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Additional information</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Account</p></td>
<td style="text-align: left;"><p>The top level entity, your company. One
user can have multiple accounts.</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Organization</p></td>
<td style="text-align: left;"><p>A logical part of your company in the
way that makes most sense in your setup, for example a region or
business unit. There can be multiple organizations linked to one
account.</p></td>
<td style="text-align: left;"><p>The organization and environment
entities defined in Gravitee Cloud are equivalent to the same entities in APIM
and AM, including the roles you can define for them (for example, the
<code>ORGNIZATION_OWNER</code> role exists in both APIM and AM).</p>
<p>Learn more about organizations and environments in link:{{
<em>/apim/3.x/apim_adminguide_organizations_and_environments.html</em></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>relative_url }}[APIM^] and link:{{
<em>/am/current/am_adminguide_organizations_and_environments.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[AM^].</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Environment</p></td>
<td style="text-align: left;"><p>An environment in an IT infrastructure,
such as development or production. There can be multiple environments
linked to one organization.</p></td>
<td style="text-align: left;"><p>Installation</p>
<p>Node</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>APIM and AM installations, linked to
environments in Cockpit. Each linked APIM and AM installation
automatically reports its REST API and Gateway nodes to
Cockpit.</p></td>
<td style="text-align: left;"><p>Nodes can belong to multiple
environments. You can configure the organizations and environments
associated with Gateway nodes in APIM and AM, by updating the Gateway
configuration files.</p>
<p>Only Gateway nodes are configurable in this way, not REST API
nodes.</p>
<p>Learn more about updating a Gateway configuration in the
<code>gravitee.yml</code> file in link:{{
<em>/apim/3.x/apim_installguide_gateway_configuration.html</em></p></td>
<td style="text-align: left;"><p>relative_url }}[APIM^] and link:{{
<em>/am/current/am_installguide_gateway_configuration.html</em></p></td>
</tr>
</tbody>
</table>

Each entity managed in Gravitee Cloud has some common properties:

-   ID: an internal ID that is never shown in the Gravitee Cloud UI, but that
    you can find if you look at the API responses.

-   HRID: a human readable ID of the entity. This ID is unique (no two
    environments in the same organization can have the same HRID), and
    they are used to provide readable URLs.

-   Name: the name of the entity.

-   Description: a description of the entity.

## Example hierarchy

The Gravitee Cloud hierarchy pictured below has the following setup:

-   One APIM installation, with two Gateway nodes and one REST API node.

-   One AM installation, with one Gateway node and one REST API node.

image::{% link images/cockpit/apim-am-nodes.png %}\[\]
