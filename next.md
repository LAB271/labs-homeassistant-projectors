# Next

> **State:** WIP HA custom integration. Up-to-spec pass landed on `up-to-spec/2026-04-29` (branch pushed, not yet merged). Visibility intentionally still PRIVATE (public flip deferred per TODO.md).
> **Last updated:** 2026-04-29
> **Source of truth:** ~/Developer/labs-infra-overview/CONVENTIONS.md

## Pending

- [ ] Merge `up-to-spec/2026-04-29` into `main` (PR or fast-forward — solo maintainer's call).
- [ ] Flip visibility to public — deferred in TODO.md until the lab is up to spec; do this after the branch above is merged and the lab-wide gate clears.
- [ ] Branch protection on `main` — **SKIPPED this pass.** GitHub Free plan returns 403 on `gh api .../branches/main/protection` for private repos. Will become available for free once the repo flips public; revisit then. Same constraint applies to every private Lab271 repo on the current plan.

## Decisions needed

(items that block progress and require the user's call — do NOT decide them yourself)

- **Q:** Flip-to-public timing — is the lab "up to spec" enough yet?
  **Context:** TODO.md defers public flip "until the lab is up to spec". This repo individually is publish-ready once `up-to-spec/2026-04-29` lands on `main`, but the deferral is a lab-wide gate, not a per-repo one.

## Recently done

- [x] 2024-11-21 — Local clone flattened (was nested at `labs-homeassistant-projectors/ha-vivitek/`); folder + remote URL aligned with canonical name (per [TODO.md:58](../labs-infra-overview/TODO.md#L58)).
- [x] 2026-04-29 — README rewritten on disk with all 7 standard sections from CONVENTIONS plus a Rename history section (`ha-vivitek` → `labs-homeassistant-projectors`). Committed in `d73e117`.
- [x] 2026-04-29 — `.github/CODEOWNERS` written with `* @LAB271`. Committed in `d73e117`.
- [x] 2026-04-29 — Pre-public secrets audit run on full tree + all 11 commits. No tokens, SSIDs, staff names, MACs, or internal hostnames; author identity is GitHub no-reply, public-safe. Sole finding (internal IP in `config_flow.py`) addressed below.
- [x] 2026-04-29 — Replaced internal IP default `10.32.8.10` in [custom_components/vivitek/config_flow.py:19](custom_components/vivitek/config_flow.py#L19) with `192.0.2.10` (RFC 5737 TEST-NET-1). **Fix-forward only — no history rewrite.** Commit `b47f7f6`.
- [x] 2026-04-29 — Updated stale `LAB271/ha-vivitek` URLs in [custom_components/vivitek/manifest.json:4-5](custom_components/vivitek/manifest.json#L4-L5) (`documentation`, `issue_tracker`) to the new repo name. Commit `c84d546`.
- [x] 2026-04-29 — Added `.gitignore` (`.DS_Store`, `__pycache__/`, `*.pyc`, `.venv/`, `.env`) and `git rm --cached`'d the two tracked `.DS_Store` files at repo root and `custom_components/`. Commits `ed6a8a1` and `d73e117` respectively.
- [x] 2026-04-29 — GitHub topics fixed: dropped `av` (this is HA, not AV), and `status-active` → `status-wip` to match README. Topics now: `homeassistant`, `infrastructure`, `lab271`, `status-wip`.
- [x] 2026-04-29 — GitHub description updated from *"Home Assistant Integration for a Vivitek Projector"* to *"Home Assistant custom integration for networked projectors (Vivitek today, multi-vendor by design)."*

## Deviations from spec / notes

- **Branch protection skipped** — GitHub Free plan does not allow protection rules on private repos. Documented above; no workaround applied this pass.
- **Internal IP not scrubbed from history** — fixed forward only. Commit `2a71022` still contains `10.32.8.10`. Discloses RFC1918 space only; no public-internet target inferable. Acceptable per the up-to-spec call.
- **Org casing (`Lab271` vs `LAB271`) skipped** — out of scope this pass.
- **Public flip deferred** per TODO.md lab-wide gate.

## Notes

- Naming, remote URL, and default branch are all correct: folder `labs-homeassistant-projectors`, remote `https://github.com/LAB271/labs-homeassistant-projectors.git`, branch `main`.
- All work for this pass committed on `up-to-spec/2026-04-29` (4 commits: `d73e117`, `c84d546`, `b47f7f6`, `ed6a8a1`) and pushed to origin.
