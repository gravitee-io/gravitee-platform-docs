---
hidden: false
noIndex: true
---

# Upload skills

Skills are reusable packages that agents consume as structured capabilities. Cataloging skills in Gamma makes them governable — you can reference them in authorization policies and compose them into Composite MCP Servers through MCP Studio.

## What a skill is

A skill is a package containing structured instructions, examples, and resources that an agent uses to perform a specific task. Skills are exposed to agents as MCP resources using the **FastMCP Skills-as-Resources** pattern — the agent reads the skill as context, then executes the task using available tools.

## Skill package structure

A skill ships as a `.zip` file containing a required manifest and optional supporting directories:

```text
skill-name/
├── SKILL.md      Required: metadata + instructions
├── scripts/      Optional: executable code
├── references/   Optional: documentation
├── assets/       Optional: templates, resources, visuals
└── ...           Optional: any additional files or folders
```

## Upload a skill

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to the **Catalog** → **Skills** list.
3. Select **Upload Skill**.
4. Under **Skill zip**, upload a `.zip` file containing your `SKILL.md` manifest and supporting files.
5. Select **Add skill to catalog**.

The skill is extracted, analyzed, and added to the Catalog. It becomes available in MCP Studio's palette as an MCP resource.

## Next steps

* **Compose into a Studio** — Include skills as resources in a Composite MCP Server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/catalog/skills/UploadSkillPage.tsx -->
