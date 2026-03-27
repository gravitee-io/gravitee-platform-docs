# gravitee-platform-docs

The [Gravitee platform documentation](https://documentation.gravitee.io/platform-overview/) is intended for both business stakeholders and developers as an introduction to the core concepts and technologies comprising Gravitee’s best-in-class API management solution. Gravitee’s standalone and integrated products position customers to easily adopt and maintain complex API architectures and communication in a versatile and innovative ecosystem.

The UX of the docs site is structured to promote intuitive navigation and an informative exploration of platform features and capabilities. The fundamental functionality of each Gravitee product is presented in the context of satisfying the business needs of real-world use cases. The complementary relationships between and extensibility of individual platform components demonstrate a centralized, comprehensive approach to API management that is compatible with a wide variety of customer roadmaps and infrastructures. Exhaustive implementation details organized into user guides and reference materials provide clarified guidance with which to harness the potential of Gravitee’s flexible, customizable, and sophisticated feature sets. 

When browsing the documentation, please pay special attention to the following:
- **Hints:** This style element is reserved for clarifications or supplemental information to resolve ambiguity and provide additional context.
- **Cautions:** This style element is reserved for caveats and exceptions to draw attention to necessary criteria or dangerous assumptions.
- **Compatibility matrices:** Verify that specific documentation is applicable to particular Gravitee installations.
- **API definitions and phases:** Different versions of the Gravitee API definition support different features and functionality.
- **Links:** Links offer easy access to information that is related, prerequisite, or consequent to the current concept or component.

## Vale linting

This repo uses [Vale](https://vale.sh/) to enforce writing style rules on documentation files (`.md` and `.mdx`). Vale runs as a GitHub Actions workflow on pull requests, but **only when the `vale integration` label is attached**.

### How it works

1. Open a PR that changes files under `docs/`.
2. Vale does **not** run automatically — no noise on draft or pipeline-generated PRs.
3. When the PR is ready for style review, add the **`vale integration`** label from the PR sidebar (under "Labels").
4. Vale runs and posts inline review comments via [reviewdog](https://github.com/reviewdog/reviewdog).
5. If you push new commits while the label is attached, Vale re-runs automatically.
6. To stop Vale from running on subsequent pushes, remove the label.

### Adding the label

In the GitHub PR sidebar, click the gear icon next to **Labels** and select `vale integration`:

![vale integration label](https://img.shields.io/badge/label-vale%20integration-0E8A16)

### Local usage

To run Vale locally before pushing:

```bash
# Install Vale (see https://vale.sh/docs/topics/installation/ for other OSes)
brew install vale

# Sync Vale packages
vale sync

# Lint a specific file
vale docs/apim/4.11/path/to/file.md

# Lint all changed docs files
git diff --name-only main -- '*.md' '*.mdx' | xargs vale
```
