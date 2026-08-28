"""Basic unit tests for ste_writing_style package."""

from typer.testing import CliRunner

from manage import app
from ste_writing_style.core import (
    audit_sentence,
    generate_template_dictionary,
    load_document_frontmatter,
)
from ste_writing_style.models import STEDictionary, TechnicalName


runner = CliRunner()


def test_cli_info() -> None:
    """Test CLI info command."""
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "ste-writing-style" in result.stdout


def test_audit_sentence_length_violation() -> None:
    """Test detection of sentence length exceeding 20 words for instructions."""
    dictionary = STEDictionary()
    long_instruction = (
        "Before you start the server, make sure that all configuration files and "
        "certificates are populated in the storage location so that no errors happen."
    )
    violations = audit_sentence(
        sentence=long_instruction,
        line_number=1,
        dictionary=dictionary,
        is_instruction=True,
    )
    assert any(v.rule == "sentence-length" for v in violations)


def test_audit_sentence_unapproved_word() -> None:
    """Test detection of unapproved words."""
    dictionary = STEDictionary()
    text = "Utilize the CLI tool to run the process."
    violations = audit_sentence(
        sentence=text,
        line_number=1,
        dictionary=dictionary,
        is_instruction=False,
    )
    assert any(v.rule == "unapproved-vocabulary" for v in violations)


def test_frontmatter_override_resilience() -> None:
    """Test that frontmatter vocabulary overrides unapproved core rules."""
    doc = """---
ste_vocabulary:
  technical_names:
    - "payload"
  allowed_overrides:
    - word: "utilize"
---
Utilize the payload serializer.
"""
    frontmatter_vocab, body = load_document_frontmatter(doc)
    assert frontmatter_vocab is not None

    dictionary = STEDictionary(technical_names=[TechnicalName(term="payload")])
    violations = audit_sentence(
        sentence="Utilize the payload serializer.",
        line_number=1,
        dictionary=dictionary,
        frontmatter_vocab=frontmatter_vocab,
        is_instruction=False,
    )
    # Since utilize was in allowed_overrides, it should not trigger an unapproved-vocabulary violation
    assert not any(v.rule == "unapproved-vocabulary" for v in violations)


def test_generate_template_dictionary() -> None:
    """Test starter dictionary model creation."""
    d = generate_template_dictionary("TestProject")
    assert d.project == "TestProject"
    assert len(d.technical_names) > 0
    assert len(d.technical_verbs) > 0
