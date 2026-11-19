# Architecture Overview - ste-writing-style

## System Overview

`ste-writing-style` provides tools, rules, and AI assistant skills for writing, auditing, and managing technical documentation in compliance with the **ASD-STE100 (Simplified Technical English)** standard.

## Component Boundaries

- `skills/`: Packaged AI assistant skills:
  - `skills/ste-writing-style/`: Core refactoring, rule reference, and dictionary schema.
  - `skills/ste-audit/`: Rule-by-rule STE compliance auditor.
  - `skills/ste-dictionary-generate/`: Extensible dictionary generator cross-referenced with `information-architecture`.
- `src/ste_writing_style/`: Python library implementing vocabulary parsing, frontmatter resolution, and audit validation logic.
- `manage.py`: Typer + Rich unified CLI entrypoint.
- `external/`: Submodules container for third-party integrations and rules banks.
- `docs/`: Technical and operational documentation.
