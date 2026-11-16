cask "keepresso-mobile" do
  version "0.6.10"
  sha256 "24fdc2b51751bbf3353dc17aa767520f5523980c4e7eca414bfe222e6c71cf1c"

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
