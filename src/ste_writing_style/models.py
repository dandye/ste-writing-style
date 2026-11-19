"""Data models for ASD-STE100 dictionaries and document frontmatter."""

from typing import Any

from pydantic import BaseModel, Field


class TechnicalName(BaseModel):
    """Domain-specific Technical Name (TN)."""

    term: str
    part_of_speech: str = "noun"
    category: str = "software"
    definition: str = ""
    forbidden_synonyms: list[str] = Field(default_factory=list)


class TechnicalVerb(BaseModel):
    """Domain-specific Technical Verb (TV)."""

    term: str
    part_of_speech: str = "verb"
    definition: str = ""
    approved_usage: str = ""
    forbidden_synonyms: list[str] = Field(default_factory=list)


class ForbiddenProjectWord(BaseModel):
    """Project-specific forbidden word with mandatory replacement."""

    word: str
    replacement: str


class AllowedOverride(BaseModel):
    """Document-level allowed override."""

    word: str
    reason: str = ""
    replacement: str = ""


class STEDictionary(BaseModel):
    """Extensible STE Project Dictionary (.ste-dictionary.yaml)."""

    version: str = "1.0"
    project: str = "Default"
    description: str = ""
    technical_names: list[TechnicalName] = Field(default_factory=list)
    technical_verbs: list[TechnicalVerb] = Field(default_factory=list)
    forbidden_project_words: list[ForbiddenProjectWord] = Field(default_factory=list)


class DocumentFrontmatterVocabulary(BaseModel):
    """Document YAML frontmatter vocabulary overrides (ste_vocabulary:)."""

    technical_names: list[str | dict[str, Any]] = Field(default_factory=list)
    technical_verbs: list[str | dict[str, Any]] = Field(default_factory=list)
    allowed_overrides: list[AllowedOverride | str] = Field(default_factory=list)


class AuditViolation(BaseModel):
    """A detected violation of ASD-STE100 rules."""

    line_number: int
    rule: str
    severity: str = "warning"
    sentence: str
    issue: str
    suggestion: str


class AuditReport(BaseModel):
    """Summary of an ASD-STE100 compliance audit."""

    target_path: str
    total_sentences: int = 0
    compliant_sentences: int = 0
    compliance_score: float = 100.0
    violations: list[AuditViolation] = Field(default_factory=list)
