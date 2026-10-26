cask "keepresso-mobile" do
  version "0.4.7"
  sha256 "72274f68eaf7d604028ccf50496afcf10a1483aee835bab23817f1001030afc8"

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
