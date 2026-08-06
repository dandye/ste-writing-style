# Simplified Technical English (ASD-STE100) Skills for Gemini & Antigravity Agents

A collection of skills for writing, auditing, and managing technical documentation in accordance with **ASD-STE100 (Simplified Technical English)**.

## Available Skills

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

1. 🥇 **Document-Level Frontmatter (`ste_vocabulary:`)**: Per-file inline vocabulary overrides.
2. 🥈 **Project Repository Dictionary (`.ste-dictionary.yaml`)**: Shared repository Technical Names & Technical Verbs.
3. 🥉 **Core ASD-STE100 Dictionary**: Standard general controlled English words.
