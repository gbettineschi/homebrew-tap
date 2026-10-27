cask "tetherbug-personal" do
  version "0.1.8"
  sha256 "364f0428525d481334590f741e1fad23e98066837fcfcebbe0c5e5b6ea4a3e6b"

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
