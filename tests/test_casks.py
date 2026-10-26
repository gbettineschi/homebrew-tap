import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("casks", Path(__file__).parents[1] / "scripts/update-cask.py")
casks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(casks)


class CaskTests(unittest.TestCase):
    def test_only_known_packages_and_version_tags(self):
        for tag in ("main", "v1.2", "v1.2.3/../../foo", "v1.2.3\n", "v01.2.3"):
            with self.assertRaises(ValueError):
                casks.render("agent-handler", tag, "a" * 64)
        with self.assertRaises(ValueError):
            casks.render("../cliprelay", "v1.2.3", "a" * 64)
        with self.assertRaises(ValueError):
            casks.render("agent-handler", "v1.2.3", "not-a-checksum")

    def test_exact_release_and_architecture_per_package(self):
        for package in casks.PACKAGES:
            result = casks.render(package, "v1.2.3", "a" * 64)
            self.assertIn(f'cask "{package}" do', result)
            self.assertIn('/releases/download/v#{version}/', result)
            self.assertIn('sha256 "' + "a" * 64 + '"', result)
            self.assertNotIn("latest/download", result)
            self.assertEqual('depends_on arch: :arm64' in result, package == "keepresso-mobile")
        result = casks.render("crisp-personal", "v1.2.3", "a" * 64)
        self.assertIn('conflicts_with cask: "crisp"', result)
        self.assertIn('binary "#{appdir}/Crisp.app/Contents/MacOS/crispctl"', result)
        self.assertIn('target: "Keepresso Mobile.app"', casks.render("keepresso-mobile", "v1.2.3", "a" * 64))

    def test_retries_cannot_downgrade_or_change_published_version(self):
        old = casks.render("agent-handler", "v1.2.3", "a" * 64)
        self.assertFalse(casks.should_update(old, old))
        self.assertTrue(casks.should_update(old, casks.render("agent-handler", "v1.2.4", "b" * 64)))
        for version, digest in (("v1.2.2", "a" * 64), ("v1.2.3", "b" * 64)):
            with self.assertRaises(ValueError):
                casks.should_update(old, casks.render("agent-handler", version, digest))


if __name__ == "__main__":
    unittest.main()
