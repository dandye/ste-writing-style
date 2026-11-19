# GEMINI.md

This file provides guidance to Gemini Code Assist and AI pair programmers working in this repository.

## Code Style and Communication

**CRITICAL: Never use emojis. Anywhere. Ever.**
- No emojis in code comments
- No emojis in commit messages
- No emojis in pull request descriptions
- No emojis in code review comments
- No emojis in documentation
- Emojis are unprofessional and must not be used in any context

## Shell and Environment Variables

- In code and shell examples, define environment variables first (e.g. `PROJECT_ID="..."`) and then reference them as `$PROJECT_ID`.

## Git Worktree and Path Conventions

- This repository adheres to the `<project_name>__worktrees/` convention.
- Primary clone with `.git/` is located at `<project_name>__worktrees/main`.
- Linked worktrees exist as sibling folders (e.g., `<project_name>__worktrees/<branch_name>`).
- Always resolve internal paths relative to `BASE_DIR = Path(__file__).resolve().parent` to maintain portability across sibling worktrees.
- If removing a worktree containing git submodules under `external/`, deinitialize submodules first: `git submodule deinit --all -f` before removing the worktree.

## Project Structure

```text
.
├── .env.example                               # Environment variable template
├── .gitignore                                 # Git ignore configuration
├── GEMINI.md                                  # AI coding instructions and repo guidelines
├── AGENTS.md                                  # Agent instructions for Antigravity agents
├── justfile                                   # Task runner (setup, install, test, lint, format, clean, audit)
├── manage.py                                  # Typer + Rich unified CLI
├── pyproject.toml                             # PEP 621 dependencies & tool configurations
├── README.md                                  # Repository overview & usage documentation
├── gemini-extension.json                      # Extension manifest
├── LICENSE                                    # MIT License
├── docs/                                      # Technical documentation & architecture notes
│   ├── architecture.md
│   └── setup.md
├── external/                                  # Git submodules container (MCP servers, external packages)
├── scripts/                                   # Helper & deployment automation scripts
│   └── setup_env.sh
├── skills/                                    # Packaged AI assistant skills (OKF 2.0 compliant)
│   ├── ste-writing-style/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── examples/
│   ├── ste-audit/
│   │   └── SKILL.md
│   └── ste-dictionary-generate/
│       └── SKILL.md
├── src/
│   └── ste_writing_style/
│       ├── __init__.py
│       ├── py.typed                           # PEP 561 marker
│       ├── models.py                          # Pydantic models for STE dictionary & frontmatter
│       └── core.py                            # Vocabulary parser & audit logic
└── tests/
    ├── __init__.py
    ├── conftest.py                            # Pytest fixtures
    └── test_basic.py                          # Basic unit tests
```

---

## Simplified Technical English (ASD-STE100) Skills

A collection of skills for writing, auditing, and managing technical documentation in accordance with **ASD-STE100 (Simplified Technical English)**.

### Available Skills

- **[ste-writing-style](skills/ste-writing-style/SKILL.md)**
  Guide technical documentation creation and refactoring into ASD-STE100 STE. Enforces controlled vocabulary, strict grammar rules (active voice, max 20-word instructions, simple tenses), and extensible project-specific dictionaries.

- **[ste-audit](skills/ste-audit/SKILL.md)**
  Audit existing technical documentation for ASD-STE100 compliance. Evaluates sentence length limits, passive voice, noun stacks (>3), and unapproved vocabulary, outputting a detailed compliance report.

- **[ste-dictionary-generate](skills/ste-dictionary-generate/SKILL.md)**
  Automatically generate a project-specific Extensible STE Dictionary (`.ste-dictionary.yaml`) by extracting domain terms from codebases using the [`information-architecture`](https://github.com/dandye/information-architecture) skill suite.

---

## Commands

| Command | Description | Target Skill |
| :--- | :--- | :--- |
| `/ste:write` / `/ste:rewrite` | Refactor prose into ASD-STE100 Simplified Technical English. | [ste-writing-style](skills/ste-writing-style/SKILL.md) |
| `/ste:audit` | Audit documentation for STE compliance and produce a detailed report. | [ste-audit](skills/ste-audit/SKILL.md) |
| `/ste:dict-gen` | Auto-generate `.ste-dictionary.yaml` from project source files/docs. | [ste-dictionary-generate](skills/ste-dictionary-generate/SKILL.md) |

---

## Vocabulary Resolution Hierarchy

When reviewing or writing documentation, vocabulary is resolved in the following priority order:

1. **Document-Level Frontmatter (`ste_vocabulary:`)**: Per-file inline vocabulary overrides.
2. **Project Repository Dictionary (`.ste-dictionary.yaml`)**: Shared repository Technical Names & Technical Verbs.
3. **Core ASD-STE100 Dictionary**: Standard general controlled English words.
