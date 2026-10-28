cask "tetherbug-personal" do
  version "0.1.9"
  sha256 "8be5e00a02856731d8bf5625a6e4148431c82557081ebe99ddef81360e57472e"

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
