cask "keepresso-mobile" do
  version "0.6.12"
  sha256 "5bb619d6c21349b55018ba3f96a4476cc0a08d1c8a6a3c60892bff7b20f31eee"

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
