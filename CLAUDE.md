# PanelWeaver

Before doing anything, read **`docs/BUILD_GUIDE.md`** (start here), then the two documents it names in the repo root (the master spec and the Risk & Concerns Register), then `docs/PROGRESS.md` if it exists.

**Which setup am I in?**
- **On the Windows PC** (`D:\Projects\PanelWeaver`): edit code here, and run everything else in the codespace through `scripts/cs` (guide §3.2). Start with `scripts/cs sync`. Install nothing heavy on the PC.
- **Inside the codespace** (`/workspaces/PanelWeaver`, usually opened from a phone): work directly, `git pull` first.

The rules that matter most (details in the guide):

- **Never use the Claude Code login, or any company key, as the pipeline's runtime model.** Pipeline model calls use the owner's personal free-tier keys from Codespaces secrets. Never commit keys.
- **This repo is public.** Manga pages, panels, audio and renders stay in `workspace/` and `renders/` (git-ignored). Ask before downloading any source material.
- **Week 0 before pipeline code:** the register's blocking measures 1–4 come first (guide M0).
- **Codespace = development. GitHub Actions = lint, tests, tiny QA fixtures only**, never rendering.
- **Done = verified output** (frames looked at, audio checked), not "it ran". Commit and push small steps often, and log progress in `docs/PROGRESS.md`.
- Ask before downloading sources, spending more than ~$3 of GPU credits, adding anything paid, or creating a claude.ai Artifact.
- End each session: push, update `docs/PROGRESS.md`, clean `pull/`, `scripts/cs stop`.
