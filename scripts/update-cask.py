#!/usr/bin/env python3
"""Publish a checksum-pinned cask for an existing release of an allowed app."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

PACKAGES = {
    "agent-handler": ("agent-handler", "Agent Handler", "AgentHandler.zip", "Agent Handler.app", "dev.gbettineschi.agent-handler", "Agent questions and approvals from the menu bar or notch"),
    "tetherbug-personal": ("Tetherbug", "Tetherbug Personal", "Tetherbug-v{version}.zip", "Tetherbug.app", "ie.xav.tetherbug", "Personal Android hotspot companion"),
    "crisp-personal": ("Crisp", "Crisp Personal", "Crisp-personal.zip", "Crisp.app", "com.crisp.app", "Personal display scaling and brightness tools"),
    "keepresso-mobile": ("keepresso-mobile", "Keepresso Mobile", "KeepressoMobile.zip", "KeepressoMobile.app", "local.keespresso.companion", "Unofficial Keepresso phone companion for Mac"),
}
ROOT = Path(__file__).resolve().parents[1]
TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def version(tag):
    if not TAG.fullmatch(tag):
        raise ValueError("Use a version tag vX.Y.Z with no leading zeroes.")
    return tag[1:]


def render(package, tag, digest):
    if package not in PACKAGES:
        raise ValueError("Unknown package.")
    ver = version(tag)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Invalid SHA-256.")
    repo, name, asset, app, bundle, desc = PACKAGES[package]
    asset = asset.format(version="#{version}")
    lines = [f'cask "{package}" do', f'  version "{ver}"', f'  sha256 "{digest}"', "",
             f'  url "https://github.com/gbettineschi/{repo}/releases/download/v#{{version}}/{asset}"',
             f'  name "{name}"', f'  desc "{desc}"', f'  homepage "https://github.com/gbettineschi/{repo}"', ""]
    if package in ("crisp-personal", "tetherbug-personal"):
        lines.append(f'  conflicts_with cask: "{package.removesuffix("-personal")}"')
    if package == "keepresso-mobile":
        lines.append("  depends_on arch: :arm64")
    lines.extend(["  depends_on macos: :sonoma", ""])
    target = ', target: "Keepresso Mobile.app"' if package == "keepresso-mobile" else ""
    lines.append(f'  app "{app}"{target}')
    if package == "crisp-personal":
        lines.append('  binary "#{appdir}/Crisp.app/Contents/MacOS/crispctl"')
    if package == "tetherbug-personal":
        lines.append('  binary "#{appdir}/Tetherbug.app/Contents/MacOS/Tetherbug", target: "tetherbug"')
        lines.extend(["", f'  uninstall quit: "{bundle}", launchctl: "ie.xav.tetherbug.agent"'])
    else:
        lines.extend(["", f'  uninstall quit: "{bundle}"'])
    lines.extend(["", "  caveats <<~EOS", "    Personal build, provided as is. Ad-hoc signed and not notarized.",
                  "    If macOS blocks it, approve it in System Settings > Privacy & Security.",
                  f"    Quit {name} before upgrading. Keep preferences and pairing data.",
                  "  EOS", "end", ""])
    return "\n".join(lines)


def should_update(current, candidate):
    if current == candidate:
        return False
    if not current:
        return True
    def get_ver(content):
        match = re.search(r'^  version "([0-9]+\.[0-9]+\.[0-9]+)"$', content, re.M)
        if not match:
            raise ValueError("Cannot read existing cask version.")
        return tuple(map(int, match[1].split(".")))
    old, new = get_ver(current), get_ver(candidate)
    if new < old:
        raise ValueError("Refusing to downgrade the tap. A newer release is already published.")
    if new == old:
        # Recipe maintenance is safe; replacing the versioned download is not.
        sha = r'^  sha256 "([0-9a-f]{64})"$'
        old_sha, new_sha = re.search(sha, current, re.M), re.search(sha, candidate, re.M)
        if not old_sha or not new_sha or old_sha[1] != new_sha[1]:
            raise ValueError("A published version must keep its original checksum.")
    return True


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", choices=PACKAGES)
    parser.add_argument("tag")
    args = parser.parse_args()
    ver = version(args.tag)
    repo, _, asset, *_ = PACKAGES[args.package]
    repo = f"gbettineschi/{repo}"
    asset = asset.format(version=ver)
    release = json.loads(gh("api", f"repos/{repo}/releases/tags/{args.tag}"))
    if release["draft"] or release["tag_name"] != args.tag:
        raise ValueError("The tagged release must be published first.")
    matches = [item for item in release["assets"] if item["name"] == asset]
    if len(matches) != 1:
        raise ValueError(f"Release must contain exactly one {asset}.")
    with tempfile.TemporaryDirectory() as scratch:
        subprocess.run(["gh", "release", "download", args.tag, "--repo", repo,
                        "--pattern", asset, "--dir", scratch], check=True)
        with (Path(scratch) / asset).open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
    api_digest = matches[0].get("digest")
    if api_digest and api_digest != f"sha256:{digest}":
        raise ValueError("Download checksum differs from GitHub's asset digest.")
    candidate = render(args.package, args.tag, digest)
    path = ROOT / "Casks" / f"{args.package}.rb"
    if should_update(path.read_text() if path.exists() else "", candidate):
        path.write_text(candidate)
        print(f"Updated {args.package} to {ver} ({digest}).")
    else:
        print(f"{args.package} {ver} is already current.")


if __name__ == "__main__":
    main()
