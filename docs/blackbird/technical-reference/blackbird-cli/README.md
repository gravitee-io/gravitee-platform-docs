---
noIndex: true
---

# Blackbird CLI

The Ambassador Blackbird Command-Line Interface (CLI) is a versatile command-line tool you can use to streamline your API development process. This document includes installation instructions, command syntax, and usage examples to help you efficiently integrate the CLI into your workflow. It includes CLI details related to the following:

* [general.md](general.md "mention"): Log in, log out, view version information, and more.
* [api.md](api.md "mention"): Create and manage APIs in the Blackbird catalog.
* [api-key.md](api-key.md "mention"): Create and manage API keys to secure your endpoints.
* [mock.md](mock.md "mention"): Create and manage mock instances to test your API specification.
* [code.md](code.md "mention"): Generate, run, and debug your API specification code.
* [cluster.md](cluster.md "mention"): Connect to a cluster, intercept a cluster, and more.
* [deployment.md](deployment.md "mention"): Manage your deployments.
* [mcp.md](mcp.md "mention"): Deploy and manage Model Context Protocol Servers within Blackbird.
* [organization.md](organization.md "mention"): Manage users and organizations.
* [token.md](token.md "mention"): Create and manage tokens for headless authentication.

Consider the following when using this reference:

* The CLI is available on Linux, macOS, and Windows.
* Running `blackbird --help` outputs the entire list of commands.
* All commands also have the flags `--help` or `-h`, which display available flags, arguments, and subcommands.
* All examples use an API named Simple API, which has a slug name of simple-api.

## Getting started with the Blackbird CLI

The Blackbird CLI is available to install in Windows, macOS, and Linux environments. After you finish the installation, log in to begin using the Blackbird CLI.

### Install the CLI

Use Powershell or the Windows Command Prompt (CMD) to install the CLI.

{% tabs %}
{% tab title="GNU/Linux amd64" %}
```shell
#Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

#Install manually:
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
#Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

#Install manually:
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
#Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

#Install manually:
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
#Install using Homebrew:
brew install datawire/blackbird/blackbird

# OR

#Install manually:
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

### Log into Blackbird

After you download the CLI, run the following command in Powershell or the Windows Command Prompt (CMD) to open a browser tab you can use to log in.

```shell
blackbird login
```
