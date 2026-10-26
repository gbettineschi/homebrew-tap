# My Homebrew tap

Mac builds from my own projects and personal forks. My changes are 100% vibe-coded, made for personal use, and provided as is. No warranty or promised support. Original authors retain their licences and credits.

```sh
brew tap gbettineschi/tap
brew install --cask gbettineschi/tap/agent-handler
```

| Package | Project |
| --- | --- |
| `agent-handler` | [Agent Handler](https://github.com/gbettineschi/agent-handler) |
| `tetherbug-personal` | [Tetherbug personal fork](https://github.com/gbettineschi/Tetherbug) |
| `crisp-personal` | [Crisp personal fork](https://github.com/gbettineschi/Crisp) |
| `keepresso-mobile` | [Keepresso Mobile](https://github.com/gbettineschi/keepresso-mobile), development preview |

Crisp and Keepresso become available here after their first Mac release finishes. Application source and downloads stay in the linked repositories. This repository contains installation recipes only. Private ClipRelay is not distributed here.

## Updates

```sh
brew update
brew upgrade --cask gbettineschi/tap/agent-handler
```

Replace the last name for another app. Quit that app before upgrading. These commands do not create a background update schedule. The builds are ad-hoc signed and not notarized; macOS may require **Open Anyway**. Keep existing app data and pairing records.

## Release maintenance

Each app's release workflow calls `.github/workflows/publish.yml` with its package and `vX.Y.Z` tag. The workflow downloads that release's exact Mac archive, computes its SHA-256 and commits the matching recipe here. No polling or manual cask editing is needed. Tetherbug's locally signed release triggers this step after publication; its Android signing key stays local.

Each source repository has a separate `TAP_DEPLOY_KEY` Actions secret, paired with a write-enabled deploy key for this tap only. No personal GitHub token is copied into Actions. Regenerate the key pair and replace both entries if a key is lost or revoked.

To retry a catalog update, run **Update Homebrew tap** in the app repository with the published tag. Re-running the same version is safe; downgrades and changed checksums for an existing version are refused. A failed catalog job can be retried without rebuilding or replacing the release.
