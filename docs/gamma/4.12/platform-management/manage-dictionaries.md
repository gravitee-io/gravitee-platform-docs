---
description: >-
  Create, deploy, and manage the dictionaries that provide environment-scoped
  lookup data to API policies from the Dictionaries page in the Gamma console.
hidden: false
noIndex: false
---

# Manage dictionaries

Dictionaries hold key-value lookup data, called properties, scoped to an environment. API policies reference this data at runtime. The Dictionaries page in the Gamma console lets you view, create, and manage the dictionaries of the selected environment.

Every dictionary has one of two types, chosen at creation:

* **Manual**. You maintain the properties by hand and publish them to the gateways with the **Deploy** action.
* **Dynamic**. Gravitee polls an HTTP source at a configured interval and refreshes the properties automatically while the dictionary is started.

## View dictionaries

From the Gamma console sidebar, select **Platform Management**, and then navigate to **Dictionaries**.

The dictionaries table displays the following columns:

* **Name**. The dictionary name and its description. Select the name to open the dictionary's detail page.
* **Type**. Manual or Dynamic. For a dynamic dictionary, the current state, Started or Stopped, appears next to the type.
* **Properties**. The number of properties the dictionary holds.
* **Last Updated**. When the dictionary configuration last changed.
* **Last Deployed**. When a manual dictionary was last deployed. This column doesn't apply to dynamic dictionaries.
* **Actions**. A row menu that contains the **View Details**, **Edit**, and **Delete** actions.

Use the search bar to filter dictionaries by name, ID, or description. The table supports sorting and pagination.

## Create a dictionary

To create a dictionary, complete the following steps:

1. From the dictionaries list, select **Add Dictionary**.
2. Enter the dictionary details described in the following table:

    | Field           | Description                                                                                                                | Required |
    | --------------- | -------------------------------------------------------------------------------------------------------------------------- | -------- |
    | **Name**        | A human-readable name of 3 to 50 characters. A name that another dictionary in the environment already uses is rejected.   | Yes      |
    | **Description** | Freeform text describing the dictionary's purpose.                                                                          | No       |
    | **Type**        | **Manual** or **Dynamic**. The type is fixed after creation.                                                                | Yes      |

3. For a dynamic dictionary, configure the **Trigger** and **HTTP Provider** sections described in the following tables.

    The **Trigger** section defines how often the provider is polled to refresh the properties:

    | Field         | Description                                | Required |
    | ------------- | ------------------------------------------ | -------- |
    | **Interval**  | A whole number greater than 0.             | Yes      |
    | **Time Unit** | **Seconds**, **Minutes**, or **Hours**.    | Yes      |

    The **HTTP Provider** section defines the source of the properties:

    | Field                  | Description                                                                                                          | Required |
    | ---------------------- | -------------------------------------------------------------------------------------------------------------------- | -------- |
    | **HTTP Service URL**   | The `http` or `https` URL that returns the dictionary data.                                                          | Yes      |
    | **HTTP Method**        | GET, POST, PUT, PATCH, or DELETE. Defaults to GET.                                                                    | No       |
    | **Use system proxy**   | Whether to send provider requests through the system proxy.                                                           | No       |
    | **Request body**       | A body sent with each provider request.                                                                               | No       |
    | **Headers**            | Name and value pairs sent with each provider request. Select **Add** to add a header row.                             | No       |
    | **JOLT Specification** | A JOLT transform that converts the HTTP response into the dictionary's key-value properties. A default is pre-filled. | Yes      |

4. Select **Create**.

The console creates the dictionary and redirects you to its detail page. A new dynamic dictionary starts in the Stopped state and doesn't poll its provider until you start it.

## Add properties to a manual dictionary

To add properties to a manual dictionary, complete the following steps:

1. From the dictionaries list, select the dictionary name to open its detail page.
2. In the **Properties** section, select **Add Property**.
3. Enter the **Key** and the **Value**. Property keys are unique within a dictionary, and a duplicate key is rejected.
4. Select **Add**.

Edit or delete an existing property from its row in the properties table. Changes to the properties reach the gateways when you deploy the dictionary.

## Deploy a manual dictionary

Deploying publishes the current properties of a manual dictionary to the gateways. To deploy a manual dictionary, complete the following steps:

1. From the dictionaries list, select the dictionary name to open its detail page.
2. Select **Deploy**.

The **Last Deployed** timestamp updates. The **Deploy** action applies only to manual dictionaries: a dynamic dictionary publishes its properties automatically each time it refreshes them from the provider.

## Start and stop a dynamic dictionary

A dynamic dictionary refreshes its properties only while it's started. To start it, complete the following steps:

1. From the dictionaries list, select the dictionary name to open its detail page.
2. Select **Start**.

While the dictionary is started, Gravitee polls the HTTP provider at the configured interval. Each refresh updates the properties and publishes them to the gateways. The **Properties** section of a dynamic dictionary is read-only and fills once the dictionary is started.

Select **Stop** to halt the refresh cycle.

The detail page of a dynamic dictionary also shows a **Trigger & Provider** section. It summarizes the polling interval, the provider URL and method, the headers, the request body, and the JOLT specification.

## Edit a dictionary

To edit a dictionary, complete the following steps:

1. In the dictionary's row, open the actions menu.
2. Select **Edit**.
3. Update the name, the description, and, for a dynamic dictionary, the trigger and HTTP provider settings. The type is read-only.
4. Select **Save Changes**.

Edits to a started dynamic dictionary take effect without stopping it.

## Delete a dictionary

To delete a dictionary, complete the following steps:

1. In the dictionary's row, open the actions menu.
2. Select **Delete**.
3. In the confirmation dialog, select **Delete Dictionary**. Deleting a dictionary permanently removes all its properties and also removes it from the gateways.

## Next steps

* [Manage applications](manage-applications.md). Manage the consumer applications that subscribe to your API plans.
