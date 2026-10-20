# VoxHalo (macOS)

Vocal chain + hybrid echo plug-in (Audio Unit, VST3, Standalone) built with JUCE 7.

Chain: Input, Low Cut, De-Ess, Squash (compressor), Drive, Air, Echo (sync, ping-pong, modulation, filtered feedback), Halo reverb, Mix, Output.

## Build on a Mac
1. Install Xcode (with command line tools), CMake 3.22+ and Git.
2. Run `./build_mac.sh`
3. Find `dist/VoxHalo-1.0.0.pkg` and `dist/VoxHalo-1.0.0.dmg`.

The first run downloads JUCE automatically. The script signs ad-hoc for local use.
To share with others, replace `-` in the codesign line with your Developer ID and notarize the pkg.

## No Mac handy?
Push the folder to GitHub. `.github/workflows/build-mac.yml` builds on a macOS runner and uploads the pkg and dmg as a downloadable artifact.

## Layout
- `Source/Params.h`  every parameter, range, default and tooltip
- `Source/Presets.h` generated from `tools/presets_data.py` (edit there, run `tools/gen_presets_header.py`)
- `tools/make_icons.py`, `tools/make_manual.py` regenerate the icons and the PDF manual

JUCE is dual licensed (GPLv3 or commercial). Check the terms before selling the plug-in.
