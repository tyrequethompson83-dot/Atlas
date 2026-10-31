# ATLAS v0 foundation

## Purpose

Adapt OpenClaw into ATLAS by using OpenClaw's existing agent runtime, native sessions, streaming, provider layer, workspace files, and skill loader. Do not create a second agent runtime alongside it.

## Added in this foundation step

- **atlas-workspace/**: ATLAS persona, operating rules, neutral user-context template, memory guidance, and one source-evidence skill.
- **scripts/install-atlas-workspace.ps1**: Windows PowerShell installer for the workspace pack. Existing files with the same names are backed up under **~/.openclaw/backups/atlas-workspace-<timestamp>/** before replacement; identical files are left unchanged.
- **config/atlas-xkiro.example.json5** and **docs/ATLAS_XKIRO_PROVIDER.md**: an opt-in xKiro/Qwen3.8 Omni Flash profile and its activation/verification notes. This example is not active by itself.
- This document records the scope and remaining verification gates.

## Install the workspace pack on Windows

From the root of this Atlas checkout, run:

    .\scripts\install-atlas-workspace.ps1

If the active agent workspace is not the default **~/.openclaw/workspace**, pass its actual path:

    .\scripts\install-atlas-workspace.ps1 -WorkspacePath 'C:\path\to\your\workspace'

The script does not edit openclaw.json, create provider credentials, configure messaging channels, or run the Gateway. Review the workspace path before installing. Existing persona files are backed up before being replaced.

## Deliberate v0 boundaries

This step does **not** add or enable:

- MT5, live charts or quotes, broker/account/positions access, or trade execution;
- market-news connectors, research pipelines, strategy/backtesting interfaces, or scheduled market watchers;
- voice, realtime Live Mode, a holographic presence, or a separate custom chat frontend;
- a custom provider automatically applied without an authenticated runtime test.

The xKiro profile is opt-in and documents the settings to test; creating it does not establish that requests from this machine/account work. These capabilities remain future, separately reviewed integrations. In particular, no credentials belong in the repository, and no original forex_jarvis functionality should be ported until the user has chosen from a source-grounded inventory.

## Verification status

The files in this step were authored against the workspace, skill, and custom-provider conventions in the checked-in OpenClaw documentation. The repository integration environment cannot run the Gateway or execute scripts on the user's Windows workstation, so this change must not be described as a successful local build, first-start, provider test, or end-to-end acceptance run.

The next technical gates are: install frozen dependencies in the local checkout; start the Gateway/Control UI; verify a real model reply, streaming, tool use, and session persistence with the selected BYOK provider. Keep credentials local and untracked.
