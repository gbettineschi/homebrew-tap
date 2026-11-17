cask "tetherbug-personal" do
  version "0.1.10"
  sha256 "560dc5281ab5db3afadd51b04658f24c0c57d1ed02d2a46126fd1ec6e651bfb0"

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
