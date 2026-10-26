cask "tetherbug-personal" do
  version "0.1.6"
  sha256 "c261a9c04920a1e26064a1e984fd8d5595e5967b8d2028263816cbc5be9f2562"

  url "https://github.com/gbettineschi/Tetherbug/releases/download/v#{version}/Tetherbug-v#{version}.zip"
  name "Tetherbug Personal"
  desc "Personal Android hotspot companion"
  homepage "https://github.com/gbettineschi/Tetherbug"

  conflicts_with cask: "tetherbug"
  depends_on macos: :sonoma

  app "Tetherbug.app"
  binary "#{appdir}/Tetherbug.app/Contents/MacOS/Tetherbug", target: "tetherbug"

  uninstall quit: "ie.xav.tetherbug", launchctl: "ie.xav.tetherbug.agent"

  caveats <<~EOS
    Personal build, provided as is. Ad-hoc signed and not notarized.
    If macOS blocks it, approve it in System Settings > Privacy & Security.
    Quit Tetherbug Personal before upgrading. Keep preferences and pairing data.
  EOS
end
