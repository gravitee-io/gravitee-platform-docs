---
description: Configuration guide for Configure AM Console.
---

# Configure AM Console

You can configure AM Console with a file named `constants.json`.

The only mandatory values in the `constants.json` file are:

```sh
$ cd gravitee-am-webui-3.21.0
$ vi constants.json

{
  "baseURL": "gravitee_am_management_api_url"
}
```

It describes where AM API lives, so that AM console can send requests to it.
