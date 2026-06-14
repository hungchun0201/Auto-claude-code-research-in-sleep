# Reviewer Routing

## Default Reviewer Contract

All reviewer-heavy Codex base skills use the same default contract:

- executor: current Codex main agent
- reviewer: second Codex reviewer
- reasoning effort: `xhigh`
- round 1: `spawn_agent`
- follow-up rounds: `send_input`

This is the base default for `skills/skills-codex/`. No effort level or unrelated parameter changes it.

> 🛑 **If `spawn_agent` / `send_input` are unavailable (e.g. local Codex CLI 0.13x):
> NEVER substitute a recursive codex call.** Do NOT call any `mcp__codex` tool, any
> MCP server named `codex`, or `codex mcp-server` from inside a Codex session —
> codex-in-codex deadlocks at an un-forwardable approval gate with no timeout
> (openai/codex#6664, #11816; caused a 6.5h hang on 2026-06-10). Degrade instead, in
> this order:
> 1. one-shot subprocess with stdin closed and a hard timeout:
>    `timeout 3600 codex exec --sandbox read-only ... - < /tmp/reviewer_prompt.txt`
>    (writing the prompt to a file first; stdin MUST reach EOF or codex exec hangs — openai/codex#20919)
> 2. perform the review in the current context, clearly labeled as NOT independent.

> ⚠️ **Same-family by default — Type-A only, NOT a cross-family verdict.** The executor here is Codex (GPT family) and this default reviewer is a *second Codex agent* — same family. That is a valid **Type-A** review (it finds omissions, ranks weaknesses, drives the fix loop), but it is **NOT** the cross-model **Type-B acquittal** ARIS's invariant requires — one model family judging itself voids the verdict (mainline `acceptance-gate.md`). For a Type-B cross-family verdict, install the **`skills-codex-claude-review`** or **`skills-codex-gemini-review`** overlay (the only genuinely cross-family reviewers for a Codex executor). Note `oracle-pro` (gpt-5.x-pro) is **also GPT family**, so it does NOT cross the family boundary for a Codex executor either.

## Default Pattern

Single-round review:

```text
spawn_agent:
  model: gpt-5.5
  reasoning_effort: xhigh
  message: |
    [role + task]
    Read the listed files directly.
```

Multi-round review:

```text
spawn_agent:
  model: gpt-5.5
  reasoning_effort: xhigh
  message: |
    [initial review prompt]
```

Save the returned reviewer id, then continue with:

```text
send_input:
  target: <saved reviewer id>
  message: |
    [follow-up materials only]
```

## Oracle Pro Override

When the user explicitly passes `--reviewer: oracle-pro`, switch only the reviewer route:

- default reviewer remains Codex xhigh if no reviewer is specified
- `oracle-pro` is optional, not the base default

Routing rule:

```text
If reviewer is omitted or reviewer=codex:
  use spawn_agent / send_input with Codex reviewer at xhigh

If reviewer=oracle-pro:
  check Oracle MCP availability
  if available:
    call mcp__oracle__consult with:
      engine: browser
      model:  gpt-5.5-pro
      browserModelStrategy: current
    (do NOT set browserThinkingTime; do NOT use preset chatgpt-pro-heavy)
  if unavailable:
    print a clear warning
    fall back to the default Codex xhigh reviewer
```

### oracle-pro setup (verified 2026-06-14, no OpenAI API key)

Browser engine on a ChatGPT Pro subscription. Prereqs:

1. **oracle ≥ 0.14.0** (`npm i -g @steipete/oracle@latest`). 0.13.0's login probe hits the
   Cloudflare-blocked `/backend-api/me` and falsely times out ("manual login mode timed out
   waiting for ChatGPT session"); 0.14 uses `/api/auth/session`.
2. **`ORACLE_BROWSER_PROFILE_DIR=~/.oracle/browser-profile`** in the oracle MCP server env
   (`~/.claude.json` → `mcpServers.oracle.env`). A non-empty value flips oracle into
   manual-login mode → reuse the signed-in persistent profile and SKIP copying cookies from
   the system Chrome (the original "No ChatGPT cookies were applied" failure). Restart Claude
   Code so the MCP server picks up the env.
3. In that profile's ChatGPT UI, select **"Pro Extended"** once (it persists). `browserModelStrategy:
   current` then resolves to Pro Extended (`resolved=Pro Extended; status=already-selected`).

**Pitfall — do NOT force the thinking time.** Current ChatGPT exposes "Pro Extended" as one
combined picker item; passing `--browser-thinking-time extended` (or MCP `preset:
chatgpt-pro-heavy`, which sets `thinkingTime=extended`) makes oracle hunt for a separate Pro
thinking submenu, fail to find it, and *refuse to submit*. Use `browserModelStrategy: current`
with Pro Extended pre-selected instead. Also never `--browser-hide-window` (breaks login detection).

Equivalent CLI (degraded / no MCP):
`oracle --engine browser --browser-manual-login --browser-manual-login-profile-dir ~/.oracle/browser-profile -m gpt-5.5-pro --browser-model-strategy current -s three-word-slug-here -p "..."`

Note: oracle-pro (gpt-5.x-pro) is **still GPT family** → Type-A only, not a cross-family Type-B verdict.

## Invariants

- Base skills do not use the legacy Codex MCP thread path as the default reviewer route.
- Reviewer independence still applies: pass file paths and task framing, not executor summaries.
- Overlay packages may replace only the reviewer route.
- Overlay packages do not change executor semantics.
- Browser-based Oracle review is acceptable for one-shot stress tests, not ideal for tight multi-round loops.

## Skills That Commonly Benefit From `oracle-pro`

- `research-review`
- `auto-review-loop`
- `experiment-audit`
- `proof-checker`
- `rebuttal`
- `idea-creator`
- `research-lit`
