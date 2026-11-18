cask "keepresso-mobile" do
  version "0.6.11"
  sha256 "614c57d2958b1838666f07cae87f80b7330dbecf68099bf334465fd54151ea67"

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
