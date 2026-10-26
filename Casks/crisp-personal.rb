cask "crisp-personal" do
  version "1.7.1"
  sha256 "89a2cd28f4d6422e34c3eed45151695834d11d6979b4d534fdba8f468beb6087"

  url "https://github.com/gbettineschi/Crisp/releases/download/v#{version}/Crisp-personal.zip"
  name "Crisp Personal"
  desc "Personal display scaling and brightness tools"
  homepage "https://github.com/gbettineschi/Crisp"

  conflicts_with cask: "crisp"
  depends_on macos: :sonoma

  app "Crisp.app"
  binary "#{appdir}/Crisp.app/Contents/MacOS/crispctl"

  uninstall quit: "com.crisp.app"

  caveats <<~EOS
    Personal build, provided as is. Ad-hoc signed and not notarized.
    If macOS blocks it, approve it in System Settings > Privacy & Security.
    Quit Crisp Personal before upgrading. Keep preferences and pairing data.
  EOS
end
