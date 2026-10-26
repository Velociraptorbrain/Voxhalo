#!/bin/bash
# Builds Butter Vox for macOS (AU + VST3 + Standalone app), then makes a .pkg installer and a .dmg.
# Requirements: Xcode + command line tools, CMake 3.22+, Git.   Usage: ./build_mac.sh
set -e
cd "$(dirname "$0")"
VER=1.0.0
ART=build/ButterVox_artefacts/Release

cmake -S . -B build -G Xcode
cmake --build build --config Release

# Ad-hoc sign so the bundles load on Apple Silicon (replace "-" with your Developer ID to distribute)
for b in "$ART/VST3/Butter Vox.vst3" "$ART/AU/Butter Vox.component" "$ART/Standalone/Butter Vox.app"; do
  codesign --force --deep --sign - "$b"
done

# Stage the installer payload
rm -rf build/pkgroot dist && mkdir -p dist \
  build/pkgroot/Library/Audio/Plug-Ins/VST3 \
  build/pkgroot/Library/Audio/Plug-Ins/Components \
  build/pkgroot/Applications \
  "build/pkgroot/Library/Application Support/Butter Vox"
cp -R "$ART/VST3/Butter Vox.vst3"        build/pkgroot/Library/Audio/Plug-Ins/VST3/
cp -R "$ART/AU/Butter Vox.component"     build/pkgroot/Library/Audio/Plug-Ins/Components/
cp -R "$ART/Standalone/Butter Vox.app"   build/pkgroot/Applications/
cp docs/ButterVox_User_Manual.pdf        "build/pkgroot/Library/Application Support/Butter Vox/"

pkgbuild --root build/pkgroot --identifier com.buttervox.audio.pkg --version $VER \
         --install-location / build/ButterVox-component.pkg
productbuild --package build/ButterVox-component.pkg "dist/ButterVox-$VER.pkg"

# DMG with a custom volume icon
rm -rf build/dmg && mkdir build/dmg
cp "dist/ButterVox-$VER.pkg" build/dmg/
cp docs/ButterVox_User_Manual.pdf build/dmg/
cp assets/buttervox_installer.icns build/dmg/.VolumeIcon.icns
SetFile -a C build/dmg 2>/dev/null || true
hdiutil create -volname "Butter Vox $VER" -srcfolder build/dmg -ov -format UDZO "dist/ButterVox-$VER.dmg"
echo "Done. See dist/"
