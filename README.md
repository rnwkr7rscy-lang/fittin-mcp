# fittin-mcp

**Know what's protectable before competitors copy it.**

FITTIN is an AI-native startup protection and defensibility platform for founders and builders.
This MCP server connects Cursor and Claude to FITTIN so you can run a free Startup Protection Check
right from your editor — describe your project, get a structured analysis in ~2 minutes.

The moment your code ships, it's publicly disclosed. Most founders skip protection and discover the
risk only when a larger, better-funded company copies their product. FITTIN makes it a 2-minute check
before you launch.

---

## What FITTIN analyzes

- **Clone risk** — how easy is it for competitors to replicate your product?
- **Defensibility** — what parts of your stack, workflow, or architecture are hard to copy?
- **Startup moat** — what gives you sustainable competitive advantage?
- **Protectable features** — what can be patented, kept as trade secret, or documented as prior art?
- **Investor readiness** — does your IP position hold up in due diligence?
- **Pre-launch protection** — what to do before you ship to establish your priority date?

---

## Example prompts

Use these in Cursor Agent or Claude with FITTIN MCP installed:

```
Run a startup protection check on this project
Can competitors clone this SaaS?
How do I protect this startup before launch?
Does this AI product have a moat?
What parts of this workflow are defensible?
Can this startup become proprietary?
What should I protect before pitching investors?
Analyze this project for clone risk
Analyze this app for startup protection opportunities
What's the IP risk if I launch this product today?
How do I protect my AI workflow from being copied?
What trade secrets does this product have?
Run an IP audit on my project
What parts of my codebase are protectable?
```

---

## What you get free

- ✅ **Clone risk score** — how exposed your product is to competitive copying
- 🛡️ **Defensibility map** — which components are protectable and why
- 💡 **Patentable features** — specific innovations that may qualify for IP protection
- 📋 **Prior art signal** — whether the space is open or crowded
- 📄 **PDF + DOCX report** delivered to your inbox in ~2 minutes

---

## Upgrade: Full IP Portfolio Package — 6 Documents ($99)

One payment. Six separate professional documents for your IP portfolio — delivered as PDF + DOCX to your inbox.

- ✅ **Patentability Analysis** — deep novelty assessment and patentable features
- ⚔️ **Market & Competitor Prior Art** — who else is in your space and what they've filed
- 📋 **Patent Strategy for Counsel** — attorney-ready strategic recommendations
- 🗺️ **Technical Assignment & Next Steps** — step-by-step IP action plan
- 📝 **Preliminary Patent Application** — draft ready for attorney review and filing
- 🛡️ **IP Risk & Opportunity Report** — full risk landscape and investment readiness
- 🎙️ **Private Nadia Audio Briefing** — your personal AI IP strategist walks you through every finding in a private podcast-style episode

---

## Quick setup

```bash
pip install fittin-mcp
```

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "fittin": {
      "command": "python3",
      "args": ["-m", "fittin_mcp"],
      "env": {
        "FITTIN_EMAIL": "you@example.com"
      }
    }
  }
}
```

Restart Cursor. FITTIN tools appear in the MCP panel under Available Tools.

---

## Claude Desktop setup

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "fittin": {
      "command": "python3",
      "args": ["-m", "fittin_mcp"],
      "env": {
        "FITTIN_EMAIL": "you@example.com"
      }
    }
  }
}
```

---

## Who it's for

- **AI startup founders** building products they want to protect before launch
- **SaaS builders** worried about competitors copying their core workflow
- **Cursor / Claude / Lovable / Bolt / Replit developers** shipping fast and thinking about moat
- **Pre-seed and seed founders** preparing IP position for investor due diligence
- **Solo founders** who want professional IP intelligence without a $500/hour attorney

---

## Tools included

| Tool | What it does |
|------|-------------|
| `fittin_patentability` | Free Startup Protection Check — clone risk, defensibility, patentable features |
| `fittin_invention` | Invention Disclosure — novel technical contributions identified from your description |
| `fittin_protect` | IP Opportunity Map — prioritized list of protectable components |
| `fittin_report` | Full $99 Package — complete IP strategy report delivered to your email |

---

## Resources

- 🌐 [fittin.dev](https://fittin.dev) — main portal
- 🚀 [Free Startup Protection Check](https://fittin.dev/start)
- 📖 [IP Strategy Blog](https://fittin.dev/blog) — clone risk, moat, patent strategy guides
- 🔍 [Clone Risk Analysis](https://fittin.dev/for/clone-risk-analysis)
- 🤖 [AI Startup Protection](https://fittin.dev/for/ai-startup)
- 📧 [ip@fittin.ai](mailto:ip@fittin.ai)

---

FITTIN is not a law firm. Reports are strategic IP intelligence and startup protection analysis,
not legal advice. For patent filing decisions, consult a licensed USPTO-registered patent attorney.
