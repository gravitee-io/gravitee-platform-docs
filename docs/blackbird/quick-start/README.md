# Quick Start

## Ambassador Blackbird Quick Start

Blackbird helps you accelerate your API development lifecycle by reducing the margin for errors and risk, improving consistency and reusability, decreasing time-to-market, and driving positive business outcomes.

Use Blackbird to quickly create dynamic or static mocks based on an OpenAPI specification, enabling you to get started on front-end development faster. You can also to generate boilerplate code, allowing you to focus more on developing the business logic rather than setting up repetitive code. Test and debug your code locally with Blackbird, or use its ephemeral environments to share your work and collaborate seamlessly with your team.

Use this page to set up your account, optionally download the command line interface (CLI), add an API, and create a mock.

If you have any questions about getting started, contact our [support.md](../support.md "mention") team.

### Before you begin

Before you get started with Blackbird, you need to create an account. If you prefer to work directly from a CLI, you can also download the CLI.

> **Note:** Blackbird offers several features that are only available using the Blackbird UI, including creating an API using AI and choosing a third-party API.

#### Create an account

Create an account using the [Blackbird UI](https://blackbird.a8r.io/dashboard) by signing in to your Google, GitHub, or Microsoft email address.

#### Download the CLI and log in (optional)

If you prefer to work directly in a CLI, download it and then log in.

{% tabs %}
{% tab title="GNU/Linux amd64" %}
```shell
# Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

# Install manually:
# 1. Create a directory if it doesn't exist:
sudo mkdir -p /usr/local/bin

# 2. Download the latest binary:
sudo curl -fL 'https://blackbird.a8r.io/api/download/cli/latest/linux/amd64' -o /usr/local/bin/blackbird

# 3. Make the binary executable:
sudo chmod a+x /usr/local/bin/blackbird
```
{% endtab %}

{% tab title="GNU/Linux arm64" %}
```shell
# Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

# Install manually:
# 1. Create a directory if it doesn't exist:
sudo mkdir -p /usr/local/bin

# 2. Download the latest binary:
sudo curl -fL 'https://blackbird.a8r.io/api/download/cli/latest/linux/arm64' -o /usr/local/bin/blackbird

# 3. Make the binary executable:
sudo chmod a+x /usr/local/bin/blackbird
```
{% endtab %}

{% tab title="macOS Intel (amd64)" %}
```shell
# Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

# Install manually:
# 1. Create a directory if it doesn't exist:
sudo mkdir -p /usr/local/bin

# 2. Download the latest binary:
sudo curl -fL 'https://blackbird.a8r.io/api/download/cli/latest/darwin/amd64' -o /usr/local/bin/blackbird

# 3. Make the binary executable:
sudo chmod a+x /usr/local/bin/blackbird
```
{% endtab %}

{% tab title="macOS M Series (arm64)" %}
```shell
# Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

# Install manually:
# 1. Create a directory if it doesn't exist:
sudo mkdir -p /usr/local/bin

# 2. Download the latest binary:
sudo curl -fL 'https://blackbird.a8r.io/api/download/cli/latest/darwin/arm64' -o /usr/local/bin/blackbird

# 3. Make the binary executable:
sudo chmod a+x /usr/local/bin/blackbird
```
{% endtab %}

{% tab title="Windows" %}
```powershell
# To install Blackbird CLI, run the following commands
# from PowerShell as Administrator.

# 1. Download the latest Windows zip containing blackbird.exe and its dependencies (~55 MB):
Invoke-WebRequest https://blackbird.a8r.io/api/download/cli/latest/windows/amd64 -OutFile blackbird.zip

# 2. Unzip the archive to a temp directory, then remove the zip file:
Expand-Archive -Path blackbird.zip -DestinationPath blackbirdInstaller/blackbird
Remove-Item 'blackbird.zip'
cd blackbirdInstaller/blackbird

# 3. Run the install script (installs to C:\\Program Files\\Ambassador-Blackbird by default):
powershell.exe -ExecutionPolicy Bypass -c " . '.\install-blackbird.ps1';"

# 4. Clean up the installer directory:
cd ../..
Remove-Item blackbirdInstaller -Recurse -Confirm:$false -Force
```
{% endtab %}
{% endtabs %}

After you download the CLI, run the following command in your terminal to open a browser tab you can use to log in.

```shell
blackbird login
```

### Add an API

To get started with Blackbird, upload your own OpenAPI specification, create one using AI, or choose a third-party API from our library of popular services.

#### Upload your own API

> **Note:** You can also use the CLI to upload your own API with Blackbird. For more information, see [apis.md](../usage-guides/apis.md "mention").

1. Open the [Blackbird UI](https://blackbird.a8r.io/dashboard).
2. In the left pane, choose **Dashboard** and then the **Add API** button.
3. Choose the **Upload API** tile.
4. On the **Upload API** page, either drag-and-drop your API file into the section or click the section to open a file explorer. Supported OpenAPI versions include 2.0 - 3.1, and supported file types include `.yaml`, `.yml`, and `.json`.
5. On the **Review Specification** page, review and edit the basic API details and use the **Mock Instance** toggle to choose whether you want to automatically create a mock instance of your API. If you don't want to create a mock now, you can create a mock later after you finish creating your API.
6. When you're ready, choose the **Create API** button.

#### Create an API using AI

1. Open the [Blackbird UI](https://blackbird.a8r.io/dashboard).
2. In the left pane, choose **Dashboard** and then the **Add API** button.
3. Choose the **Create API** tile.
4. On the **Create API** page, type a prompt with information about the API you want to create. For example, you could provide the following prompt for a payment processing API: `I want to create a new API for processing payments. Use OpenAPI 3.0.1. The service should have paths and operations related to accepting user payment requests, processing payments, and handling payment errors.`
5. Review the content of the API, and use prompts in the chatbot to make changes.
6. When you’re ready, choose the **Accept** button to review and edit the API details.
7. On the **Review Specification** page, review and edit the basic API details and use the **Mock Instance** toggle to choose whether you want to automatically create a mock instance of your API. If you don't want to create a mock now, you can create a mock later after you finish creating your API.
8. When you're ready, choose the **Create API** button.

#### Choose a third-party API

**To choose a third-party API:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/dashboard).
2. In the left pane, choose **Dashboard** and then the **Add API** button.
3. Choose the **Third Party API** tile.
4. On the **Choose Specification** page, select an API from the **External Service** drop-down menu. For example, use OpenAPI, Zoom API, or Google Analytics API.
5. Choose the **Accept** button to review and edit the API details.
6. On the **Review Specification** page, review and edit the basic API details and use the **Mock Instance** toggle to choose whether you want to automatically create a mock instance of your API. If you don't want to create a mock now, you can create a mock later after you finish creating your API.
7. When you're ready, choose the **Create API** button.

### Create a mock

If you didn't create a mock automatically while adding an API, you can now create a mock to start testing your API.

> **Note:** You can also use the CLI to create a mock with Blackbird. For more information, see [mock-instances.md](../usage-guides/mock-instances.md "mention").

1. Open the [Blackbird UI](https://blackbird.a8r.io/dashboard).
2. In the left pane, choose **APIs** under **Catalog**.
3. In the tile of the API for which you want to create a mock, choose the **Create Mock** button.
4. In the modal, provide a **custom name** or use the pre-populated name, and then choose the **Create** button.

After you have a mock, you can send requests to the mock to test the behavior.
