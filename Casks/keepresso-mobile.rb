cask "keepresso-mobile" do
  version "0.4.3"
  sha256 "59cc0fd804ab8228b0e38c4c9eca7b9e57d409c8030dac3fe6415b72412768e5"

  url "https://github.com/gbettineschi/keepresso-mobile/releases/download/v#{version}/KeepressoMobile.zip"
  name "Keepresso Mobile"
  desc "Unofficial Keepresso phone companion for Mac"
  homepage "https://github.com/gbettineschi/keepresso-mobile"

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "KeepressoMobile.app", target: "Keepresso Mobile.app"

  uninstall quit: "local.keespresso.companion"

  caveats <<~EOS
    Personal build, provided as is. Ad-hoc signed and not notarized.
    If macOS blocks it, approve it in System Settings > Privacy & Security.
    Quit Keepresso Mobile before upgrading. Keep preferences and pairing data.
  EOS
end
