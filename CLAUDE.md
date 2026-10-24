# PanelWeaver

Before doing anything, read **`docs/BUILD_GUIDE.md`** (how we build it, start here), then the spec in the repo root (`PanelWeaver — AI Comic-to-Video Production System _ Initial Master Project Specification v0.1.md`), then `docs/PROGRESS.md` if it exists.

The rules that matter most (details in the guide):

- **Never use the Claude Code login, or any company key, as the pipeline's runtime model.** Pipeline model calls use the owner's personal free-tier keys from Codespaces secrets. Never commit keys.
- **This repo is public.** Manga pages, panels, audio and renders stay in `workspace/` and `renders/` (git-ignored). Ask before downloading any source material.
- **Codespace = development. GitHub Actions = lint and tests only**, never rendering.
- **The owner is on a phone.** Short messages, run commands yourself, show results as frames, contact sheets, or files on port 8000.
- **Done = verified output** (frames looked at, audio checked), not "it ran". Commit and push small steps often, and log progress in `docs/PROGRESS.md`.
- Ask before downloading sources, spending more than ~$3 of GPU credits, or adding anything paid.
