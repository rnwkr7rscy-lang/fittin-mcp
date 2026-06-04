"""
FITTIN MCP — security layer.
PUBLIC_DEMO_ONLY mode: tools operate only on user-provided text.
No internal client workspaces, NDA materials, or confidential references
are accessible through the public MCP interface.
"""

import json
import os
import re
from typing import Optional

DEFAULT_MCP_MODE = "public_demo_only"

# Terms that must never appear in any MCP output.
# Keep in sync with pipeline/knowledge_retriever.py :: NDA_BANNED_FILENAMES
BANNED_TERMS = [
    "artworkout",
    "ArtWorkout",
    "art_workout",
    "collaborative_drawing_patent",
    "client_workspace/artworkout",
    "collaborative artwork creation",   # unique phrase from NDA patent application
    "co-op drawing",                    # NDA-specific product term
]

# Path fragments that must never be accessed by MCP tools
BANNED_PATH_PARTS = [
    "artworkout",
    "ArtWorkout",
    "collaborative_drawing_patent",
    "client_workspace",
    "knowledge_base",
    "audio_briefings",
    "pipeline_outputs",
]

# Only these roots are allowed for any filesystem access
SAFE_PUBLIC_ROOTS = [
    "fittin_mcp/public_examples",
    "fittin_mcp/demo_examples",
]


def sanitize_output(text: str) -> str:
    """Replace any banned term in output with a safe generic label."""
    result = text
    for term in BANNED_TERMS:
        result = re.sub(re.escape(term), "[confidential client project]", result, flags=re.IGNORECASE)
    return result


def assert_no_banned_terms(text: str) -> None:
    """Raise ValueError if any banned term appears in text."""
    lower = text.lower()
    for term in BANNED_TERMS:
        if term.lower() in lower:
            raise ValueError("Security violation: banned term detected in MCP output.")


def is_safe_path(path: str) -> bool:
    """
    Return True only if path is within an allowed public root.
    Uses resolve() to block traversal and symlink bypass.
    """
    from pathlib import Path
    # String-level banned fragment check first
    normalized = os.path.normpath(path).replace("\\", "/")
    for banned in BANNED_PATH_PARTS:
        if banned.lower() in normalized.lower():
            return False
    # Resolve to absolute path to catch ../ traversal and symlinks
    try:
        resolved = Path(path).resolve()
    except Exception:
        return False
    for safe_root in SAFE_PUBLIC_ROOTS:
        try:
            safe_resolved = Path(safe_root).resolve()
            if resolved == safe_resolved or safe_resolved in resolved.parents:
                return True
        except Exception:
            continue
    return False


def safe_log(event_type: str, **metadata) -> None:
    """
    Structured safe logging — never logs raw descriptions, file paths,
    retrieved chunks, or embeddings. Only metadata is logged.
    Forbidden keys: description, text, content, path, chunk, embedding.
    """
    import sys
    FORBIDDEN_KEYS = {"description", "text", "content", "path", "chunk", "embedding", "idea_text"}
    safe_meta = {k: v for k, v in metadata.items() if k not in FORBIDDEN_KEYS}
    print(json.dumps({"event": event_type, **safe_meta}), file=sys.stderr, flush=True)


def check_input_for_banned_terms(text: str) -> Optional[str]:
    """Return an error string if input references banned NDA materials, else None."""
    lower = text.lower()
    for term in BANNED_TERMS:
        if term.lower() in lower:
            return (
                "No authorized client context provided. "
                "Please provide a public description or authorized client_id."
            )
    return None
