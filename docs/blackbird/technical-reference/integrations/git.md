# Git

Blackbird integrates with Git to simplify how you discover, generate, and manage your APIs. When you connect your GitHub repositories, Blackbird can automatically scan your code to detect OpenAPI and Swagger definitions or generate new specifications by analyzing your routes, handlers, and service patterns. Using this data, Blackbird creates a project, which is a container for one or more API specifications that are imported or generated from a specific GitHub repository. With projects, you can organize and test your individual specifications in a centralized location.

Key features include:

* **Discover API specifications** – Scan a private or public GitHub repository for existing OpenAPI and Swagger specifications, and then import the definitions you choose into Blackbird. Blackbird keeps the imported definitions up to date with changes made in the repository, so your definitions stay current as your APIs evolve. The sync only works one way, so changes made in Blackbird won’t update your GitHub repository.
* **Generate new API specifications** – Analyze a repository for services and generate new OpenAPI specifications for each of them based on your routes, handlers, and service patterns. Blackbird provides a specification that includes the endpoints, routes, methods (GET, POST, etc.), parameters, expected responses, and documentation you need to get started.

Using the integration, you can access any public repositories associated with your GitHub organization. If you want to access private repositories, you must have access permissions. If you don't have permissions, your GitHub administrator must approve adding the Blackbird app before you can access those repositories. We'll request the necessary permissions for you when you install the Blackbird app in GitHub.

## Prerequisites

Before configuring the Git integration, ensure you meet the following requirements:

* You have a GitHub account.
* For access to private repositories, you have access permissions.

## Discover API specifications

After you meet the prerequisites, use the following procedure to discover existing OpenAPI and Swagger specifications.

**To discover API specifications:**

1. Log into the [Blackbird UI](https://blackbird.a8r.io).
2. In the left pane, choose **APIs**.
3. Choose the **Add API** button.
4.  Choose the **Connect with GitHub** link to allow Blackbird to discover your public APIs in GitHub.

    > **Note:** For access to private repositories, choose the **add our Blackbird GitHub app** link. If you aren’t a GitHub administrator for your private repositories, Blackbird will submit a permissions request to your administrator.
5.  Choose the **repository** you want to analyze.

    > **Note:** Each repository can only be linked to one project in Blackbird. You can't analyze a repository that's already connected to another project. If you want to analyze a repository that already exists in Blackbird, remove the existing project.
6. Choose the **branch** you want to analyze. The default is your main branch.
7. Choose the **Discover (Design First)** toggle.
8. Choose the **Analyze** button. Blackbird analyzes your repository for API definitions. If Blackbird is unable to find a specification, try refreshing the page or choose a different repository.
9. Use the checkboxes to choose **one or more API files** you want to import into Blackbird, and then choose **Continue**. Blackbird imports the API definitions.
10. Choose the **View Project** button.

    > **Note:** You can choose this button at any time without interrupting the process.

    Your new project opens, displaying a list of the APIs associated with the project. It also shows the repository details (i.e., name, branch name, time, date and time of your last commit, the commit SHA, and whether your webhook is active or inactive) and a job event log that displays real-time updates for in-progress jobs.

## Generate API specifications

After you meet the prerequisites, use the following procedure to generate API specifications from your code.

**To generate API specifications:**

1. Log into the [Blackbird UI](https://blackbird.a8r.io).
2. In the left pane, choose **APIs**.
3. Choose the **Add API** button.
4.  Choose the **Connect with GitHub** link to allow Blackbird to discover your public APIs in GitHub.

    > **Note:** For access to private repositories, choose the **add our Blackbird GitHub app** link. If you aren’t a GitHub administrator for your private repositories, Blackbird submits a permissions request to your administrator.
5.  Choose the **repository** you want to analyze.

    > **Note:** Each repository can only be linked to one project in Blackbird. You can't analyze a repository that's already connected to another project. If you want to analyze a repository that already exists in Blackbird, remove the existing project.
6. Choose the **branch** you want to analyze. The default is your main branch.
7. Choose the **Create (Code First)** toggle.
8. Choose the **Analyze** button. Blackbird analyzes your repository and displays a message if no services are found.
9. Choose the **Analyze Code And Create Specification** button to create new API specifications based on the code in your selected repository. You won’t see APIs populate the project until Blackbird is done analyzing your repository. You can check the notification bell in the top-right corner of the UI for process updates. When Blackbird is done analyzing your repository, new API specifications populate the project.

## Next steps

Now that your project includes one or more APIs, you can take one of the following next steps:

* To view the API’s endpoints and details, choose the **View API** (eye) icon.
* To edit an API specification, choose the **View API** (eye) icon for the API you want to edit, and then choose **Edit API Specification** under API Actions.
* To generate a mock instance of your API to simulate its behavior in a controlled testing environment, choose **Create Mock**.
* To add or remove APIs from the project, navigate to **Projects** in the left pane. Find the project you want to edit, select the **three vertical dots** on its tile, and choose **Edit APIs**. Select or deselect the files you want to use in Blackbird.
* To remove a project from Blackbird, navigate to **Projects** in the left pane. Find the project you want to delete, select the **three vertical dots** on its tile, and choose **Remove**. If the project is the only one linked to a GitHub repository with a webhook, Blackbird removes the webhook and disassociates any related APIs and mocks. All related APIs and mocks remain available in your catalog.
