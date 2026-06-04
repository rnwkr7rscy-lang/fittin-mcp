"""
FITTIN MCP v0.1.2 — Security smoke tests (pytest style).
Run: python3 -m pytest fittin_mcp/tests/test_mcp_security.py -v
"""
import sys
import os
import io
import contextlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fittin_mcp.security import (
    sanitize_output,
    assert_no_banned_terms,
    is_safe_path,
    check_input_for_banned_terms,
    safe_log,
    DEFAULT_MCP_MODE,
    BANNED_TERMS,
)
from fittin_mcp.__main__ import handle_call_tool


# ── Mode ──────────────────────────────────────────────────────────────────────

def test_public_demo_only_mode():
    assert DEFAULT_MCP_MODE == "public_demo_only"


# ── Input guard ───────────────────────────────────────────────────────────────

def test_artworkout_blocked_in_input():
    assert check_input_for_banned_terms("ArtWorkout app") is not None

def test_artworkout_blocked_lowercase():
    assert check_input_for_banned_terms("project: artworkout") is not None

def test_collaborative_drawing_patent_blocked():
    assert check_input_for_banned_terms("collaborative_drawing_patent") is not None

def test_clean_input_passes():
    assert check_input_for_banned_terms("My SaaS project") is None


# ── sanitize_output ───────────────────────────────────────────────────────────

def test_sanitize_removes_artworkout():
    assert "ArtWorkout" not in sanitize_output("ArtWorkout app")

def test_sanitize_removes_artworkout_lowercase():
    assert "artworkout" not in sanitize_output("client: artworkout")

def test_sanitize_keeps_clean_text():
    assert sanitize_output("novelty score: 9/10") == "novelty score: 9/10"


# ── assert_no_banned_terms ────────────────────────────────────────────────────

def test_assert_raises_on_artworkout():
    import pytest
    with pytest.raises(ValueError):
        assert_no_banned_terms("analysis for ArtWorkout")

def test_assert_passes_on_clean_text():
    assert_no_banned_terms("IP strategy report ready")


# ── Path guard ────────────────────────────────────────────────────────────────

def test_nda_protected_path_blocked():
    assert not is_safe_path("knowledge_base/nda_protected/file.md")

def test_client_workspace_blocked():
    assert not is_safe_path("client_workspace/some/file.txt")

def test_knowledge_base_blocked():
    assert not is_safe_path("knowledge_base/internal/ref.md")


# ── Path traversal ────────────────────────────────────────────────────────────

def test_traversal_blocked():
    assert not is_safe_path("fittin_mcp/public_examples/../../knowledge_base/secret.md")

def test_absolute_system_path_blocked():
    assert not is_safe_path("/etc/passwd")

def test_absolute_nda_path_blocked():
    assert not is_safe_path(
        "/Users/andreirevkov/Documents/fittin-ip-pipeline/knowledge_base/nda_protected/file.md"
    )


# ── Safe roots ────────────────────────────────────────────────────────────────

def test_public_examples_allowed():
    assert is_safe_path("fittin_mcp/public_examples/demo.txt")

def test_demo_examples_allowed():
    assert is_safe_path("fittin_mcp/demo_examples/sample.json")


# ── Tool output ───────────────────────────────────────────────────────────────

def _tool_output_no_banned(tool_name):
    out = handle_call_tool(tool_name, {
        "email": "test@example.com",
        "description": "ArtWorkout collaborative_drawing_patent"
    })
    for term in BANNED_TERMS:
        assert term.lower() not in out.lower(), f"banned term '{term}' in output: {out}"

def test_fittin_patentability_blocks_banned_input():
    _tool_output_no_banned("fittin_patentability")

def test_fittin_invention_blocks_banned_input():
    _tool_output_no_banned("fittin_invention")

def test_fittin_protect_blocks_banned_input():
    _tool_output_no_banned("fittin_protect")

def test_fittin_report_blocks_banned_input():
    _tool_output_no_banned("fittin_report")


# ── Safe logging ──────────────────────────────────────────────────────────────

def test_safe_log_strips_sensitive_keys():
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        safe_log("test_event",
                 tool="fittin_patentability",
                 description="SECRET ArtWorkout data",
                 email="user@example.com")
    logged = buf.getvalue()
    assert "SECRET" not in logged
    assert "ArtWorkout" not in logged
    assert "test_event" in logged
