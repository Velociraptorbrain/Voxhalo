#!/bin/bash
# Builds VoxHalo for macOS (AU + VST3 + Standalone app), then makes a .pkg installer and a .dmg.
# Requirements: Xcode + command line tools, CMake 3.22+, Git.   Usage: ./build_mac.sh
set -e
cd "$(dirname "$0")"
VER=1.0.0
ART=build/VoxHalo_artefacts/Release

cmake -S . -B build -G Xcode
cmake --build build --config Release

# Ad-hoc sign so the bundles load on Apple Silicon (replace "-" with your Developer ID to distribute)
for b in "$ART/VST3/VoxHalo.vst3" "$ART/AU/VoxHalo.component" "$ART/Standalone/VoxHalo.app"; do
  codesign --force --deep --sign - "$b"
done

# Stage the installer payload
rm -rf build/pkgroot dist && mkdir -p dist \
  build/pkgroot/Library/Audio/Plug-Ins/VST3 \
  build/pkgroot/Library/Audio/Plug-Ins/Components \
  build/pkgroot/Applications \
  "build/pkgroot/Library/Application Support/VoxHalo"
cp -R "$ART/VST3/VoxHalo.vst3"        build/pkgroot/Library/Audio/Plug-Ins/VST3/
cp -R "$ART/AU/VoxHalo.component"     build/pkgroot/Library/Audio/Plug-Ins/Components/
cp -R "$ART/Standalone/VoxHalo.app"   build/pkgroot/Applications/
cp docs/VoxHalo_User_Manual.pdf       "build/pkgroot/Library/Application Support/VoxHalo/"

pkgbuild --root build/pkgroot --identifier com.voxhalo.audio.pkg --version $VER \
         --install-location / build/VoxHalo-component.pkg
productbuild --package build/VoxHalo-component.pkg "dist/VoxHalo-$VER.pkg"

# DMG with a custom volume icon
rm -rf build/dmg && mkdir build/dmg
cp "dist/VoxHalo-$VER.pkg" build/dmg/
cp docs/VoxHalo_User_Manual.pdf build/dmg/
cp assets/voxhalo_installer.icns build/dmg/.VolumeIcon.icns
SetFile -a C build/dmg 2>/dev/null || true
hdiutil create -volname "VoxHalo $VER" -srcfolder build/dmg -ov -format UDZO "dist/VoxHalo-$VER.dmg"
echo "Done. See dist/"
