---
description: Documentation on policies and controls for limitations.
---

# Limitations

Shared policy groups have the following limitations:

* You cannot export a shared policy group. As a workaround, if you have a valid personal access token and the APIM\_HOST environment variable set, you can download the definition through the management API using the following command (editing environment variables and environment ID as needed):

```bash
curl --request GET \
  --url https://${MAPI_URL}/management/v2/environments/DEFAULT/shared-policy-groups/${GROUP_ID} \
  --header 'Accept: application/json' \
  --header 'Authorization: Basic ${PERSONAL_ACCESS_TOKEN}'

```

* You cannot import a shared policy group. As a workaround, if you have a valid personal access token and the APIM\_HOST environment variable set, you can create a shared policy group through the management API using the following command, with the `data` field containing the group definition:

```bash
curl --request POST \
  --url https://${MAPI_URL}/management/v2/environments/DEFAULT/shared-policy-groups \
  --header 'Accept: application/json' \
  --header 'Authorization: Basic ${PERSONAL_ACCESS_TOKEN}' \
  --header 'Content-Type: application/json' \
  --data '{
  "crossId": "5e2b3b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b",
  "name": "My Shared Policy Group",
  "description": "This is a shared policy group",
  "prerequisiteMessage": "The resource cache \"my-cache\" is required",
  "apiType": "MESSAGE",
  "phase": "REQUEST",
  "steps": [
    {
      "name": "string",
      "description": "string",
      "enabled": true,
      "policy": "string",
      "configuration": {},
      "condition": "string",
      "messageCondition": "string"
    }
  ]
}'
```

* If you import an API with a shared policy group reference that does not exist in the higher environment, the API executes with no issues. Future versions of Gravitee will allow the platform administrator to configure whether to allow APIs to run or be imported with missing shared policy groups.
