cask "tetherbug-personal" do
  version "0.1.12"
  sha256 "6cdc17cdcbf2771484b29588219bd99bad065568d58f9b6755bac5f58f534e7a"

  url "https://github.com/gbettineschi/Tetherbug/releases/download/v#{version}/Tetherbug-v#{version}.zip"
  name "Tetherbug (gbettineschi's version)"
  desc "Personal Android hotspot companion"
  homepage "https://github.com/gbettineschi/Tetherbug"

  conflicts_with cask: "tetherbug"
  depends_on macos: :sonoma

  app "Tetherbug.app"
  binary "#{appdir}/Tetherbug.app/Contents/MacOS/Tetherbug", target: "tetherbug"

  uninstall quit: "ie.xav.tetherbug", launchctl: "ie.xav.tetherbug.agent"

  caveats <<~EOS
    Personal build, provided as is. Signed with a retained project certificate; not notarized.
    If macOS blocks it, approve it in System Settings > Privacy & Security.
    Quit Tetherbug (gbettineschi's version) before upgrading. Keep preferences and pairing data.
  EOS
end
