# Virtual Company System

Virtual Company System is a schema-enforced organizational operating system.

Structure is law.
Hierarchy is enforced.
Roles are constrained.
Outputs are consistent.
Evolution is controlled.

## System purpose

This repository provides a deterministic, file-structured, CI-enforced framework for defining a virtual company. Every role is represented through required files, validated metadata, and hierarchy rules.

## Role hierarchy rules

A role is valid only if it resolves to an IC anchor, has a valid managed role unless it is the anchor, has no cycles, and belongs to a family with at least one anchor.

## Naming rules

All identifiers must be lowercase snake_case with no numbers, no spaces, and no special characters.

Valid example

`software_engineer_staff`

Invalid examples

`softwareEngineer1`

`software-engineer`

`software engineer`

## File structure

Each company project contains these root folders.

- `roles/`
- `shared/`
- `org/`
- `templates/`
- `inputs/`
- `outputs/`

Each role must contain these required files.

- `ROLE_META.yaml`
- `CONTEXT.txt`
- `DIRECTIVES.txt`
- `ROLE_SPEC.txt`

The founder role must also contain these required files.

- `ROLE_CREATION_TEMPLATE.txt`
- `FOUNDER_INIT_PROMPT.txt`

## How to create roles

Use the CLI.

```bash
vc create-role my_company --spec path/to/role_request.yaml
```

Role creation is template-driven. Generated files are validated before they are written.

## How validation works

`vc validate <company>` runs file validation and organization validation.

File validation checks required files, template headings, and empty files.

Organization validation checks enums, naming rules, unique role ids, references, cycle detection, IC resolution, anchor rules, and family anchor coverage.

## How CI enforces rules

The GitHub workflow runs tests and validators on every push and pull request. Any violation fails the pipeline. No merge should proceed without a passing workflow.
