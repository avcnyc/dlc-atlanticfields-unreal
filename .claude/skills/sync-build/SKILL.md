---
name: sync-build
description: Pull latest, update submodules, build the summerlinEditor target, launch the editor, then build the Spool UI, start the Spool server, and open its dashboard in Chrome. Use when the user asks to sync and build, rebuild after fetching updates, or "pull 받고 빌드해서 에디터랑 spool 띄워줘". Aborts before building if the editor is already running, and never launches anything off a failed build.
---

# Sync & Build

One command for the "start of session / after someone else pushed" loop: pull → submodules → UE build → editor → Spool UI build → Spool server → Chrome.

## Purpose

Run these steps in strict order, stopping at the first failure:

1. `git pull`
2. `git submodule update --init --recursive`
3. `Build.bat summerlinEditor Win64 Development`
4. Launch `summerlin.uproject` in UE 5.7
5. `npm install` + `npm run build` in `Tools/spool/ui`
6. `python -m spool serve` (detached, port 8080)
7. Open `http://localhost:8080/` in Chrome

The value is in the gates, not the commands. The failure modes worth guarding: a UE build attempted while the editor holds the DLL, a pull over locally modified binary assets, and serving a Spool UI that failed to build.

The editor is launched at step 4 rather than at the end on purpose — it takes minutes to reach a loaded map, so it warms up while `npm` runs.

## Constants

- **Repo:** `D:\Github\summerlin-unreal`
- **Target:** `summerlinEditor Win64 Development`
- **Build.bat:** `C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat`
- **Editor:** `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe`
- **Submodules:** `Plugins/Scaffold`, `Tools/crate`
- **Spool:** `D:\Github\summerlin-unreal\Tools\spool` — Python package `spool`, Vue UI in `ui/`
- **Spool port:** `8080` (hardcoded in `spool/app.py`: `web.TCPSite(runner, "0.0.0.0", 8080)`)
- **Chrome:** `C:\Program Files\Google\Chrome\Application\chrome.exe`

Shell is PowerShell 5.1 — no `&&`, no `||`. Chain with `;`, or gate on `$LASTEXITCODE`.

## Step 0: Preflight — both checks must pass

**Is the editor running?**

```powershell
@(Get-Process | Where-Object { $_.Name -like 'UnrealEditor*' }).Count
```

If greater than 0, **stop before pulling.** The open editor holds the DLL and `Build.bat` fails with `Unable to build while Live Coding is active`. Report it and let the user pick: close the editor, or trigger the Live Coding rebuild in-editor with `Ctrl+Alt+F11` instead. Never kill the process — unsaved level edits die with it.

**Is the working tree dirty?**

```powershell
git -C D:\Github\summerlin-unreal status --porcelain
```

`.umap` and `.uasset` are binary — git cannot merge them, so a pull that touches a locally modified asset leaves a conflict that can only be resolved by picking one side wholesale. If any **tracked** file is modified, `git fetch` first and check whether the incoming commits actually touch those paths:

```powershell
git -C D:\Github\summerlin-unreal fetch; git -C D:\Github\summerlin-unreal diff --name-only HEAD..@{u}
```

No overlap means the pull is safe — proceed and say so. Overlap on a binary asset means stop and ask. Do not stash, checkout, or discard on your own. Untracked files (`??`) are harmless.

## Step 1: Pull

```powershell
git -C D:\Github\summerlin-unreal pull
```

Keep the commit list — the final report names what arrived. On conflict or a rejected non-fast-forward, stop and paste git's output verbatim; do not attempt a resolution.

## Step 2: Submodules

```powershell
git -C D:\Github\summerlin-unreal submodule update --init --recursive
```

`Tools/crate` authenticates with a PAT embedded in `.gitmodules`. If it fails with a 403/auth error the token has expired — report it and stop. That is not something to work around.

## Step 3: UE build

```powershell
& "C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat" summerlinEditor Win64 Development -Project="D:\Github\summerlin-unreal\summerlin.uproject" -WaitMutex -FromMsBuild
```

Pass `timeout: 600000`. An incremental build after a normal pull takes well under a minute. If the pull touched engine plugins or many headers, a full rebuild can exceed 10 minutes — on timeout, re-run with `run_in_background: true` and continue when the completion notification arrives.

Success is the **exit code**, not a grep for "succeeded" — a stale log line will lie to you. On failure, stop here, report the first real compiler/UBT error (not the tail of the log), and skip every remaining step. A binary that didn't build must not be opened.

## Step 4: Launch the editor — only on a successful build

```powershell
Start-Process "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe" -ArgumentList '"D:\Github\summerlin-unreal\summerlin.uproject"'
```

Launching `UnrealEditor.exe` directly pins UE 5.7; `Start-Process` on the `.uproject` itself would route through whatever version `UnrealVersionSelector` has associated. It returns immediately — do not wait on it. Confirm the process exists and move on to step 5; the map loads while `npm` works.

## Step 5: Build the Spool UI

```powershell
Push-Location D:\Github\summerlin-unreal\Tools\spool\ui
npm install
$installed = $LASTEXITCODE
if ($installed -eq 0) { npm run build }
$built = $LASTEXITCODE
Pop-Location
"install=$installed build=$built"
```

Gate on `$LASTEXITCODE`, not `$?` — npm writes warnings to stderr and `$?` is unreliable for native executables here.

`vite.config.ts` builds to `../spool/static` with `emptyOutDir: true`, so the build **wipes the directory the server serves from**. A failed build therefore leaves Spool with no UI at all. If either command exits non-zero, stop: do not start the server, do not open Chrome, and say that `spool/static` may now be empty.

## Step 6: Start the Spool server

The port is hardcoded, so a second instance cannot bind. Check first:

```powershell
@([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | Where-Object { $_.Port -eq 8080 }).Count
```

Use this listener query rather than `Get-NetTCPConnection` — the latter raises a non-terminating error when nothing matches, which surfaces as a failed command.

If something is already listening, **do not start another one** and do not kill it: the freshly built UI is served from disk, so a reload in Chrome picks it up. Report that the existing server was reused and skip to step 7.

Otherwise start it detached, from the package root so `spool.app` imports:

```powershell
Start-Process python -ArgumentList '-m','spool','serve' -WorkingDirectory 'D:\Github\summerlin-unreal\Tools\spool' -WindowStyle Minimized
```

A minimized window rather than a hidden one, so the user can see the Shuttle traffic and close it when done. Then wait for the port, bounded:

```powershell
$ready = $false
foreach ($i in 1..20) {
  Start-Sleep -Milliseconds 500
  if (@([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | Where-Object { $_.Port -eq 8080 }).Count -gt 0) { $ready = $true; break }
}
"ready=$ready"
```

If it never comes up within those 10 seconds, re-run `python -m spool serve` in the **foreground** once to capture the traceback (missing deps from `requirements.txt` is the usual cause), report it, and skip Chrome.

## Step 7: Open Chrome — only once the port is listening

```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList 'http://localhost:8080/'
```

Opens in the user's existing Chrome session as a new tab. Do not substitute the default browser — Chrome is the target.

## Step 8: Report

Short and factual:

- Commits pulled (count + subjects), or "already up to date"
- Submodule updates, if any
- UE build result and roughly how long it took
- Editor launched (PID)
- Spool UI build result; server started fresh or existing one reused
- Chrome opened, or the step that stopped the run and why

## Common Pitfalls

- ❌ Building UE with the editor open → ✅ Step 0 process check first, always
- ❌ Stashing or discarding modified `.umap`/`.uasset` to clear the way for a pull → ✅ Check whether incoming commits even touch them, then ask
- ❌ Opening the editor after a failed build → ✅ Step 4 is gated on exit code 0
- ❌ Reading "Build succeeded" out of the log → ✅ Trust the exit code
- ❌ Starting `spool serve` after a failed `npm run build` → ✅ `emptyOutDir` already wiped `spool/static`; serving it shows a blank page
- ❌ A second `spool serve` on top of a running one → ✅ Listener check; reuse, never double-bind or kill
- ❌ Opening Chrome before the port is up → ✅ Bounded readiness loop, then open
- ❌ `git pull && git submodule update`, `npm install && npm run build` → ✅ PowerShell 5.1 has no `&&`
- ❌ Gating npm on `$?` → ✅ `$LASTEXITCODE`
- ❌ Waiting for the editor to finish loading → ✅ Fire and forget

## Re-runs

If a previous run stopped at step 0 and the user has since closed the editor, start over from step 0 — the pull may or may not have happened. `git status` and `git log -1` tell you where you actually are; don't assume.

Steps 5–7 are safe to re-run on their own when only the Spool UI changed: rebuild, reuse the running server, reload the tab.
