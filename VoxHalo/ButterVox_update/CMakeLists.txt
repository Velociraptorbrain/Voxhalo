cmake_minimum_required(VERSION 3.22)

# Universal binary: runs natively on Apple Silicon and Intel Macs
set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "")
set(CMAKE_OSX_DEPLOYMENT_TARGET "11.0" CACHE STRING "")

project(ButterVox VERSION 1.0.0)

include(FetchContent)
FetchContent_Declare(JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 8.0.11
    GIT_SHALLOW ON)
FetchContent_MakeAvailable(JUCE)

# The baked interface artwork is compiled into the plug-in
juce_add_binary_data(ButterVoxAssets SOURCES assets/skin_bg.png)

juce_add_plugin(ButterVox
    COMPANY_NAME "Butter Vox Audio"
    PLUGIN_MANUFACTURER_CODE Bttr
    PLUGIN_CODE Bvox
    FORMATS AU VST3 Standalone
    PRODUCT_NAME "Butter Vox"
    ICON_BIG "${CMAKE_CURRENT_SOURCE_DIR}/assets/icon_512.png"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    VST3_CATEGORIES Fx Delay
    AU_MAIN_TYPE kAudioUnitType_Effect
    BUNDLE_ID com.buttervox.audio.buttervox
    COPY_PLUGIN_AFTER_BUILD FALSE)

target_sources(ButterVox PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp)

target_compile_definitions(ButterVox PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0)

target_link_libraries(ButterVox
    PRIVATE
        ButterVoxAssets
        juce::juce_audio_utils
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags)
