"""Exercise the actual workflow publish loop against a local bare Git remote."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def test_first_package_is_committed_and_retry_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            remote, checkout, commands = root / "remote.git", root / "checkout", root / "bin"
            commands.mkdir()
            checkout.mkdir()
            (checkout / "scripts").mkdir()
            (checkout / "Casks").mkdir()
            shutil.copyfile(ROOT / "scripts/update-cask.py", checkout / "scripts/update-cask.py")
            def git(*args, cwd=checkout):
                return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
            git("init", "--bare", "--initial-branch=main", str(remote), cwd=root)
            git("init", "-b", "main")
            git("config", "user.name", "Test publisher")
            git("config", "user.email", "test@example.invalid")
            git("add", ".")
            git("commit", "-m", "Initial catalog")
            git("remote", "add", "origin", str(remote))
            git("push", "-u", "origin", "main")
            # A controlled release API and download; no network or GitHub credentials.
            asset = root / "AgentHandler.zip"
            asset.write_bytes(b"deterministic release fixture")
            release = {"tag_name": "v1.2.3", "draft": False, "assets": [{
                "name": asset.name, "digest": "sha256:" + hashlib.sha256(asset.read_bytes()).hexdigest()}]}
            fake_gh = commands / "gh"
            fake_gh.write_text("#!/usr/bin/env python3\nimport json,os,pathlib,shutil,sys\n"
                               "if sys.argv[1] == 'api': print(os.environ['TEST_RELEASE'])\n"
                               "else: shutil.copyfile(os.environ['TEST_ASSET'], pathlib.Path(sys.argv[sys.argv.index('--dir')+1])/'AgentHandler.zip')\n")
            fake_gh.chmod(0o755)
            env = {**os.environ, "PATH": str(commands) + os.pathsep + os.environ["PATH"],
                   "PACKAGE": "agent-handler", "TAG": "v1.2.3", "TEST_RELEASE": json.dumps(release),
                   "TEST_ASSET": str(asset)}
            workflow = (ROOT / ".github/workflows/publish.yml").read_text().splitlines()
            start = next(i for i, line in enumerate(workflow) if line.strip().startswith("for attempt in "))
            loop = "set -euo pipefail\n" + textwrap.dedent("\n".join(workflow[start:]))
            for attempt in range(2):
                result = subprocess.run(["bash", "-c", loop], cwd=checkout, env=env, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                remote_cask = git("show", "main:Casks/agent-handler.rb", cwd=remote)
                self.assertIn('version "1.2.3"', remote_cask)
                # Initial catalog + exactly one publication, even after retry.
                self.assertEqual(git("rev-list", "--count", "main", cwd=remote), "2")
