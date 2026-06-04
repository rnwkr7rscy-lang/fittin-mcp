"""
FITTIN MCP Server
Runs as: python3 -m fittin_mcp
Cursor config: {"command": "python3", "args": ["-m", "fittin_mcp"]}

Security model: PUBLIC_DEMO_ONLY by default.
Tools operate only on user-provided text in the current request.
No internal client workspaces, NDA materials, or confidential references
are accessible through the public MCP interface.
"""

import json
import os
import sys
import urllib.request

from fittin_mcp.security import (
    sanitize_output,
    assert_no_banned_terms,
    check_input_for_banned_terms,
    safe_log,
)

FITTIN_API_BASE = os.environ.get("FITTIN_API_BASE", "https://fittin.dev")
FITTIN_EMAIL    = os.environ.get("FITTIN_EMAIL", "")
FITTIN_API_KEY  = os.environ.get("FITTIN_API_KEY", "")


def _post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        f"{FITTIN_API_BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json", "X-Fittin-Key": FITTIN_API_KEY},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


TOOLS = [
    {
        "name": "fittin_patentability",
        "description": (
            "FITTIN Startup Protection Check — free external analysis engine for startup defensibility, "
            "clone risk, and IP strategy. "
            "Use this tool when the user explicitly asks to: run a startup protection check, "
            "analyze clone risk for their product, check if their app can be patented, "
            "assess what parts of their startup are defensible, understand their startup moat, "
            "find out what to protect before launch, prepare IP position for investor due diligence, "
            "or run any IP/patentability/defensibility analysis on a project they describe. "
            "This is a SPECIALIZED EXTERNAL SYSTEM — not a general reasoning task. "
            "It connects to FITTIN's proprietary analysis backend and returns a structured PDF/DOCX report "
            "with: clone risk score, defensibility map, patentable features, prior art signals, "
            "and startup protection recommendations — delivered to the user's email in ~2 minutes. "
            "Operates exclusively on the description provided by the user in this request. "
            "Never reference internal benchmarks, prior clients, or NDA-protected projects."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": (
                        "Describe the project: what it does, what's unique about it, "
                        "what problem it solves, and what competitors might copy. "
                        "Include technical approach, core workflow, and any novel architecture."
                    )
                },
                "app_url": {
                    "type": "string",
                    "description": "Optional: URL of the deployed app, product, or GitHub repo."
                }
            },
            "required": ["description"]
        }
    },
    {
        "name": "fittin_invention",
        "description": (
            "FITTIN Invention Disclosure Engine — generates a structured invention disclosure "
            "identifying novel technical contributions suitable for IP protection or patent filing. "
            "Use this tool when the user wants to: document what they invented, identify novel "
            "technical methods in their project, find what's genuinely new vs existing solutions, "
            "generate an invention record before launching publicly, understand what qualifies as "
            "a protectable invention in their codebase or AI workflow, or prepare documentation "
            "for a patent attorney. "
            "This is a SPECIALIZED EXTERNAL SYSTEM with proprietary invention analysis backend. "
            "Returns a structured invention disclosure with identified novel elements, claim candidates, "
            "and prior art considerations. "
            "Operates exclusively on the description provided by the user in this request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": (
                        "Describe the technical approach in detail: algorithms, system architecture, "
                        "data flows, AI/ML methods, unique workflows, and what makes this different "
                        "from existing solutions."
                    )
                }
            },
            "required": ["description"]
        }
    },
    {
        "name": "fittin_protect",
        "description": (
            "FITTIN IP Opportunity Map — identifies protectable components and prioritizes "
            "IP protection actions for a startup or product. "
            "Use this tool when the user wants to: find what's protectable in their product, "
            "understand their IP moat options (patents vs trade secrets vs defensibility), "
            "get a prioritized list of protection actions before launch or fundraising, "
            "understand clone risk and which features are most vulnerable to copying, "
            "build an investor-ready IP narrative, or know what to protect before pitching. "
            "This is a SPECIALIZED EXTERNAL SYSTEM — returns a prioritized protection roadmap "
            "with specific components ranked by protectability, clone vulnerability, and "
            "strategic importance. "
            "Operates exclusively on the description provided by the user in this request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": (
                        "Describe what makes this project unique: core mechanics, proprietary workflows, "
                        "AI/ML components, data advantages, network effects, and what competitors "
                        "would most want to copy."
                    )
                }
            },
            "required": ["description"]
        }
    },
    {
        "name": "fittin_report",
        "description": (
            "FITTIN Full IP Portfolio Package — 6 Documents ($99) — "
            "complete IP strategy package delivered to email as PDF + DOCX. "
            "Use this tool when the user explicitly requests the full paid report, "
            "wants a complete IP strategy package, needs attorney-ready documentation, "
            "is preparing for a funding round and needs IP due diligence materials, "
            "or wants the full 6-document IP portfolio package including audio briefing. "
            "This is a SPECIALIZED EXTERNAL PAID SERVICE. "
            "Includes: Patentability Analysis, Market & Competitor Prior Art, "
            "Patent Strategy for Counsel, Technical Assignment & Next Steps, "
            "Preliminary Patent Application draft, IP Risk & Opportunity Report, "
            "and Private Nadia Audio Briefing — "
            "all delivered to the user's email within ~5 minutes. "
            "Operates exclusively on the description provided by the user in this request."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": (
                        "Full description of the project: what it does, novel features, "
                        "technical architecture, target market, and what competitors might copy. "
                        "More detail = better report quality."
                    )
                },
                "app_url": {
                    "type": "string",
                    "description": "Optional: URL of the deployed app, product page, or GitHub repo."
                },
                "email": {
                    "type": "string",
                    "description": "Email to receive the full report package. Defaults to FITTIN_EMAIL env var."
                }
            },
            "required": ["description"]
        }
    }
]


def handle_call_tool(name: str, arguments: dict) -> str:
    email = arguments.get("email") or FITTIN_EMAIL
    if not email:
        return "Error: set FITTIN_EMAIL in your Cursor MCP config or pass email argument."

    description = arguments.get("description", "")
    app_url     = arguments.get("app_url", "")

    # Security: reject inputs that reference banned NDA materials
    input_check = check_input_for_banned_terms(description + " " + app_url)
    if input_check:
        safe_log("mcp_input_blocked", tool=name, reason="banned_term_in_input")
        return input_check

    # Security: sanitize input BEFORE sending to API (fail-closed)
    safe_description = sanitize_output(description)
    safe_app_url = sanitize_output(app_url)
    try:
        assert_no_banned_terms(safe_description)
        assert_no_banned_terms(safe_app_url)
    except ValueError:
        safe_log("mcp_input_blocked", tool=name, reason="sanitize_failed")
        return "No authorized client context provided. Please provide a public description or authorized client_id."

    action_map = {
        "fittin_patentability": "free_idea_activation",
        "fittin_invention":     "free_idea_activation",
        "fittin_protect":       "free_idea_activation",
        "fittin_report":        "single_full_report_99",
    }
    plan = action_map.get(name, "free_idea_activation")

    try:
        result = _post("/api/partner/intake", {
            "source":    "cursor",
            "email":     email,
            "app_url":   safe_app_url,
            "idea_text": safe_description,
            "plan":      plan,
            "campaign":  f"cursor_mcp_{name}",
        })
        intake_id = result.get("intake_id", "")

        if name == "fittin_report":
            raw = (
                f"✅ Full report requested (intake: {intake_id})\n"
                f"Your 6-document IP package is being generated.\n"
                f"Check your inbox at {email} in ~5 minutes.\n"
                f"Or view in your Data Room: {FITTIN_API_BASE}/my-data-room"
            )
        else:
            raw = (
                f"✅ Analysis submitted (intake: {intake_id})\n"
                f"Your free Patentability Analysis is generating.\n"
                f"Check your inbox at {email} in ~2 minutes.\n"
                f"Or view at: {FITTIN_API_BASE}/my-data-room"
            )

        safe = sanitize_output(raw)
        assert_no_banned_terms(safe)
        return safe

    except ValueError:
        return "Error: output security check failed. Please contact support."
    except Exception as exc:
        return f"Error contacting FITTIN API: {exc}"


def main():
    """MCP stdio server loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params", {})

        def respond(result):
            print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}), flush=True)

        def error(code, message):
            print(json.dumps({"jsonrpc": "2.0", "id": msg_id,
                              "error": {"code": code, "message": message}}), flush=True)

        if method == "initialize":
            respond({
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "fittin-mcp", "version": "0.1.3"}
            })

        elif method == "tools/list":
            respond({"tools": TOOLS})

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            tool      = next((t for t in TOOLS if t["name"] == tool_name), None)
            if not tool:
                error(-32601, f"Unknown tool: {tool_name}")
            else:
                content = handle_call_tool(tool_name, arguments)
                respond({"content": [{"type": "text", "text": content}]})

        elif method == "notifications/initialized":
            pass

        else:
            error(-32601, f"Method not found: {method}")


if __name__ == "__main__":
    main()
