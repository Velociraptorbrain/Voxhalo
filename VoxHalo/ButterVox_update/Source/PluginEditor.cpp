#include "PluginEditor.h"
#include "Layout.h"
#include "BinaryData.h"

using namespace juce;

namespace
{
const Colour kInk     { 0xff4a2812 };
const Colour kChoc    { 0xff683c1c };
const Colour kButter  { 0xffffd960 };
const Colour kButterL { 0xffffee9c };
const Colour kButterD { 0xfff0be3c };
const Colour kCream   { 0xfffff7e0 };
const Colour kPeri    { 0xff7080e0 };

Rectangle<int> asInt (const skin::Rc& r) { return Rectangle<float> (r.x, r.y, r.w, r.h).toNearestInt(); }
}

static_assert (skin::kNumCtl == vh::kNumFloat, "Layout.h is out of date: run tools/build_skin.py");

//==============================================================================
ButterLookAndFeel::ButterLookAndFeel()
{
    setColour (Label::textColourId, kInk);
    setColour (TextButton::textColourOffId, kInk);
    setColour (TextButton::textColourOnId, kInk);
    setColour (ComboBox::textColourId, kInk);
    setColour (ComboBox::arrowColourId, kInk);
    setColour (PopupMenu::backgroundColourId, kCream);
    setColour (PopupMenu::textColourId, kInk);
    setColour (PopupMenu::highlightedBackgroundColourId, kButter);
    setColour (PopupMenu::highlightedTextColourId, kInk);
    setColour (TooltipWindow::backgroundColourId, kCream);
    setColour (TooltipWindow::textColourId, kInk);
    setColour (TooltipWindow::outlineColourId, kInk);
}

void ButterLookAndFeel::drawLinearSlider (Graphics& g, int x, int y, int w, int h, float sliderPos,
                                          float, float, Slider::SliderStyle style, Slider& s)
{
    if (style != Slider::LinearVertical)
    {
        LookAndFeel_V4::drawLinearSlider (g, x, y, w, h, sliderPos, 0.f, 0.f, style, s);
        return;
    }

    const bool faded = ! s.isEnabled();
    if (faded) g.beginTransparencyLayer (0.45f);

    const float cx = (float) x + (float) w * 0.5f;
    const float top = (float) y + 14.f, bot = (float) (y + h) - 14.f;
    const float pos = jlimit (top, bot, sliderPos);

    // groove, filled with melted butter up to the handle
    const Rectangle<float> groove (cx - 6.f, top, 12.f, bot - top);
    g.setColour (kInk);
    g.fillRoundedRectangle (groove.expanded (2.5f), 8.f);
    g.setColour (kChoc);
    g.fillRoundedRectangle (groove, 6.f);
    const Rectangle<float> fill (cx - 4.f, pos, 8.f, bot - pos - 2.f);
    g.setGradientFill (ColourGradient (kButterL, cx, pos, kButterD, cx, bot, false));
    g.fillRoundedRectangle (fill, 4.f);

    // the handle is a pat of butter
    const Rectangle<float> t (cx - 18.f, pos - 13.f, 36.f, 26.f);
    g.setColour (Colours::black.withAlpha (0.25f));
    g.fillRoundedRectangle (t.translated (1.5f, 2.5f), 6.f);
    g.setColour (kInk);
    g.fillRoundedRectangle (t, 6.f);
    g.setGradientFill (ColourGradient (kCream, t.getX(), t.getY(), Colour (0xffe9d3a0), t.getX(), t.getBottom(), false));
    g.fillRoundedRectangle (t.reduced (2.2f), 4.5f);
    g.setColour (Colour (0xffd8bd80));
    for (int k = 0; k < 2; ++k)
    {
        const float ry = t.getCentreY() + 2.f + (float) k * 4.5f;
        g.drawLine (t.getX() + 7.f, ry, t.getRight() - 7.f, ry, 1.f);
    }
    if (s.isMouseOverOrDragging())
    {
        g.setColour (Colours::white.withAlpha (0.28f));
        g.fillRoundedRectangle (t.reduced (2.2f), 4.5f);
    }

    if (faded) g.endTransparencyLayer();
}

void ButterLookAndFeel::drawRotarySlider (Graphics& g, int x, int y, int w, int h, float sliderPos,
                                          float startAngle, float endAngle, Slider& s)
{
    const bool faded = ! s.isEnabled();
    if (faded) g.beginTransparencyLayer (0.45f);

    const float r = jmin (w, h) * 0.5f - 6.f;
    const float cx = (float) x + (float) w * 0.5f, cy = (float) y + (float) h * 0.5f;
    const float angle = startAngle + sliderPos * (endAngle - startAngle);

    g.setColour (Colours::black.withAlpha (0.3f));
    g.fillEllipse (cx - r + 2.f, cy - r + 4.f, 2.f * r, 2.f * r);
    g.setColour (kInk);
    g.fillEllipse (cx - r, cy - r, 2.f * r, 2.f * r);
    g.setColour (kCream);
    g.fillEllipse (cx - r * 0.94f, cy - r * 0.94f, r * 1.88f, r * 1.88f);

    g.setColour (Colour (0xffe2c896));
    for (int i = 0; i < 24; ++i)
    {
        const float a = MathConstants<float>::twoPi * (float) i / 24.f;
        g.fillEllipse (cx + r * 0.82f * std::sin (a) - r * 0.035f, cy - r * 0.82f * std::cos (a) - r * 0.035f, r * 0.07f, r * 0.07f);
    }

    const float cr = r * 0.66f;
    g.setGradientFill (ColourGradient (Colour (0xffffe882), cx - cr * 0.4f, cy - cr * 0.5f, Colour (0xffe29618), cx + cr * 0.8f, cy + cr * 0.9f, true));
    g.fillEllipse (cx - cr, cy - cr, 2.f * cr, 2.f * cr);
    g.setColour (kInk);
    g.drawEllipse (cx - cr, cy - cr, 2.f * cr, 2.f * cr, 2.2f);
    g.setColour (Colours::white.withAlpha (0.6f));
    g.fillEllipse (cx - cr * 0.7f, cy - cr * 0.75f, cr * 0.5f, cr * 0.3f);

    Path p;
    p.startNewSubPath (cx, cy);
    p.lineTo (cx + r * 0.6f * std::sin (angle), cy - r * 0.6f * std::cos (angle));
    g.setColour (kInk);
    g.strokePath (p, PathStrokeType (3.5f, PathStrokeType::curved, PathStrokeType::rounded));
    g.fillEllipse (cx - 4.f, cy - 4.f, 8.f, 8.f);

    if (s.isMouseOverOrDragging())
    {
        g.setColour (Colours::white.withAlpha (0.18f));
        g.fillEllipse (cx - r, cy - r, 2.f * r, 2.f * r);
    }

    if (faded) g.endTransparencyLayer();
}

void ButterLookAndFeel::drawButtonBackground (Graphics& g, Button& b, const Colour&, bool over, bool down)
{
    const auto r = b.getLocalBounds().toFloat().reduced (1.5f);
    const String t = b.getButtonText();
    Colour fill = kButter;
    if (t == "TAP") fill = kPeri;
    else if (t == "SYNC") fill = b.getToggleState() ? kButter : kCream;
    if (over) fill = fill.brighter (0.12f);
    if (down) fill = fill.darker (0.12f);
    if (! b.isEnabled()) fill = fill.withAlpha (0.5f);

    const bool round = (t == "<" || t == ">");
    const float rad = round ? r.getHeight() * 0.5f : jmin (r.getHeight() * 0.5f, 14.f);
    g.setColour (kInk);
    g.fillRoundedRectangle (r, rad);
    g.setColour (fill);
    g.fillRoundedRectangle (r.reduced (3.f), jmax (1.f, rad - 3.f));
}

Font ButterLookAndFeel::getTextButtonFont (TextButton&, int buttonHeight)
{
    return Font ((float) jmin (16, buttonHeight * 6 / 10), Font::bold);
}

void ButterLookAndFeel::drawComboBox (Graphics& g, int w, int h, bool, int, int, int, int, ComboBox& box)
{
    if (box.getName() != "div")
        return;   // the preset menu sits on the recipe card artwork, so it draws nothing itself

    const auto r = Rectangle<float> (0.f, 0.f, (float) w, (float) h).reduced (1.5f);
    g.setColour (kInk);
    g.fillRoundedRectangle (r, 12.f);
    g.setColour (kCream);
    g.fillRoundedRectangle (r.reduced (3.f), 9.f);
    Path tri;
    const float ax = (float) w - 14.f, ay = (float) h * 0.5f;
    tri.addTriangle (ax - 4.f, ay - 2.f, ax + 4.f, ay - 2.f, ax, ay + 3.f);
    g.setColour (kInk);
    g.fillPath (tri);
}

Font ButterLookAndFeel::getComboBoxFont (ComboBox& box)
{
    return box.getName() == "div" ? Font (13.f, Font::bold) : Font (22.f, Font::bold | Font::italic);
}

void ButterLookAndFeel::positionComboBoxText (ComboBox& box, Label& label)
{
    label.setBounds (1, 1, box.getWidth() - (box.getName() == "div" ? 18 : 2), box.getHeight() - 2);
    label.setFont (getComboBoxFont (box));
    label.setJustificationType (Justification::centred);
}

//==============================================================================
class VoxHaloEditor::Content : public Component, private Timer
{
public:
    explicit Content (VoxHaloProcessor& p) : proc (p)
    {
        bg = ImageCache::getFromMemory (BinaryData::skin_bg_png, BinaryData::skin_bg_pngSize);

        for (int k = 0; k < skin::kNumCtl; ++k)
        {
            const auto& c = skin::kCtl[k];
            auto& s = strips[(size_t) c.param];
            const auto& info = vh::kParams[c.param];

            if (c.knob)
            {
                s.slider.setSliderStyle (Slider::RotaryHorizontalVerticalDrag);
                s.slider.setRotaryParameters (MathConstants<float>::pi * 1.25f, MathConstants<float>::pi * 2.75f, true);
                const float hh = c.r + 6.f;
                s.slider.setBounds (Rectangle<float> (c.cx - hh, c.cy - hh, 2.f * hh, 2.f * hh).toNearestInt());
            }
            else
            {
                s.slider.setSliderStyle (Slider::LinearVertical);
                s.slider.setBounds (Rectangle<float> (c.cx - 22.f, c.top - 14.f, 44.f, (c.bot - c.top) + 28.f).toNearestInt());
            }

            s.slider.setTextBoxStyle (Slider::NoTextBox, false, 0, 0);
            s.slider.setTooltip (String (info.tip) + "\n(Double-click to reset)");
            addAndMakeVisible (s.slider);

            s.value.setJustificationType (Justification::centred);
            s.value.setFont (Font (11.5f, Font::bold));
            s.value.setColour (Label::textColourId, kInk);
            s.value.setInterceptsMouseClicks (false, false);
            s.value.setBounds (Rectangle<float> (c.vx - c.vw * 0.5f, c.vy, c.vw, c.vh).toNearestInt());
            addAndMakeVisible (s.value);

            Slider* sp = &s.slider;
            Label* lp = &s.value;
            s.slider.onValueChange = [sp, lp] { lp->setText (sp->getTextFromValue (sp->getValue()), dontSendNotification); };

            s.att = std::make_unique<AudioProcessorValueTreeState::SliderAttachment> (proc.apvts, info.id, s.slider);
        }

        syncBtn.setButtonText ("SYNC");
        syncBtn.setClickingTogglesState (true);
        syncBtn.setTooltip (vh::kSyncTip);
        syncBtn.setBounds (asInt (skin::kSync));
        addAndMakeVisible (syncBtn);
        syncAtt = std::make_unique<AudioProcessorValueTreeState::ButtonAttachment> (proc.apvts, "sync", syncBtn);

        divBox.setName ("div");
        divBox.addItemList (vh::kDivisions, 1);
        divBox.setTooltip (vh::kDivTip);
        divBox.setBounds (asInt (skin::kDiv));
        addAndMakeVisible (divBox);
        divAtt = std::make_unique<AudioProcessorValueTreeState::ComboBoxAttachment> (proc.apvts, "division", divBox);

        tapBtn.setButtonText ("TAP");
        tapBtn.setColour (TextButton::textColourOffId, Colours::white);
        tapBtn.setTooltip ("Tap the beat. Four taps or so set the echo time, and Sync switches off.");
        tapBtn.setBounds (asInt (skin::kTap));
        tapBtn.onClick = [this] { tap(); };
        addAndMakeVisible (tapBtn);

        StringArray names;
        for (int i = 0; i < vh::kNumPresets; ++i)
            names.add (vh::kPresets[i].name);
        presetBox.addItemList (names, 1);
        presetBox.setTooltip ("Pick one of the 20 recipe presets.");
        presetBox.setBounds (asInt (skin::kPreset));
        presetBox.setSelectedItemIndex (proc.getCurrentProgram(), dontSendNotification);
        presetBox.onChange = [this] { proc.setCurrentProgram (presetBox.getSelectedItemIndex()); };
        addAndMakeVisible (presetBox);

        prevBtn.setButtonText ("<");
        nextBtn.setButtonText (">");
        prevBtn.setTooltip ("Previous preset");
        nextBtn.setTooltip ("Next preset");
        prevBtn.setBounds (asInt (skin::kPrev));
        nextBtn.setBounds (asInt (skin::kNext));
        prevBtn.onClick = [this] { step (-1); };
        nextBtn.onClick = [this] { step (1); };
        addAndMakeVisible (prevBtn);
        addAndMakeVisible (nextBtn);

        lcdArea = asInt (skin::kLcd);
        meterArea = Rectangle<float> (skin::kMeter.x - skin::kMeter.w - 8.f, skin::kMeter.y - skin::kMeter.w - 8.f,
                                      2.f * skin::kMeter.w + 16.f, skin::kMeter.w + 24.f).toNearestInt();

        setSize (skin::kW, skin::kH);
        refreshValues();
        refreshState();
        startTimerHz (30);
    }

    void paint (Graphics& g) override
    {
        g.setImageResamplingQuality (Graphics::highResamplingQuality);
        g.drawImage (bg, getLocalBounds().toFloat(), RectanglePlacement::stretchToFit);

        // echo display
        const bool sync = proc.apvts.getRawParameterValue ("sync")->load() > 0.5f;
        const int div = jlimit (0, vh::kDivisions.size() - 1, (int) proc.apvts.getRawParameterValue ("division")->load());
        const float ms = proc.apvts.getRawParameterValue ("time")->load();
        const String main = sync ? vh::kDivisions[div] : String (roundToInt (ms)) + " ms";
        g.setColour (Colour (0xffffd45a));
        g.setFont (Font (28.f, Font::bold));
        g.drawText (main, lcdArea, Justification::centred);
        g.setColour (Colour (0xffe0a040));
        g.setFont (Font (10.f, Font::bold));
        g.drawText (sync ? "SYNC" : "FREE", lcdArea.withHeight (16).translated (0, 3), Justification::centred);

        // VU needle
        const float db = Decibels::gainToDecibels (meterSmooth, -60.f);
        const float frac = jlimit (0.f, 1.f, jmap (db, -36.f, 3.f, 0.f, 1.f));
        const float a = degreesToRadians (-50.f + 100.f * frac);
        const float px = skin::kMeter.x, py = skin::kMeter.y, len = skin::kMeter.w;
        g.setColour (kInk);
        g.drawLine (px, py, px + len * std::sin (a), py - len * std::cos (a), 2.5f);
        g.fillEllipse (px - 4.5f, py - 4.5f, 9.f, 9.f);
    }

private:
    struct Strip
    {
        Slider slider;
        Label value;
        std::unique_ptr<AudioProcessorValueTreeState::SliderAttachment> att;
    };

    void step (int dir)
    {
        const int n = vh::kNumPresets;
        presetBox.setSelectedItemIndex ((proc.getCurrentProgram() + dir + n) % n, sendNotificationSync);
    }

    void tap()
    {
        const double now = Time::getMillisecondCounterHiRes();
        if (! taps.empty() && now - taps.back() > 2500.0)
            taps.clear();
        taps.push_back (now);
        if (taps.size() > 5)
            taps.erase (taps.begin());
        if (taps.size() < 2)
            return;

        double sum = 0.0;
        for (size_t i = 1; i < taps.size(); ++i)
            sum += taps[i] - taps[i - 1];
        const float ms = jlimit (vh::kParams[vh::pTime].lo, vh::kParams[vh::pTime].hi, (float) (sum / (double) (taps.size() - 1)));

        if (auto* pt = proc.apvts.getParameter ("time"))
            pt->setValueNotifyingHost (pt->convertTo0to1 (ms));
        if (auto* ps = proc.apvts.getParameter ("sync"))
            ps->setValueNotifyingHost (0.f);
    }

    void refreshValues()
    {
        for (auto& s : strips)
            s.value.setText (s.slider.getTextFromValue (s.slider.getValue()), dontSendNotification);
    }

    void refreshState()
    {
        const bool sync = proc.apvts.getRawParameterValue ("sync")->load() > 0.5f;
        strips[(size_t) vh::pTime].slider.setEnabled (! sync);
        divBox.setEnabled (sync);
    }

    void timerCallback() override
    {
        meterSmooth = jmax (proc.meterLevel.exchange (0.f), meterSmooth * 0.88f);
        refreshValues();
        refreshState();
        if (presetBox.getSelectedItemIndex() != proc.getCurrentProgram())
            presetBox.setSelectedItemIndex (proc.getCurrentProgram(), dontSendNotification);
        repaint (lcdArea);
        repaint (meterArea);
    }

    VoxHaloProcessor& proc;
    Image bg;
    std::array<Strip, vh::kNumFloat> strips;
    TextButton syncBtn, tapBtn, prevBtn, nextBtn;
    ComboBox divBox, presetBox;
    std::unique_ptr<AudioProcessorValueTreeState::ButtonAttachment> syncAtt;
    std::unique_ptr<AudioProcessorValueTreeState::ComboBoxAttachment> divAtt;
    std::vector<double> taps;
    Rectangle<int> lcdArea, meterArea;
    float meterSmooth = 0.f;
};

//==============================================================================
VoxHaloEditor::VoxHaloEditor (VoxHaloProcessor& p) : AudioProcessorEditor (&p)
{
    setLookAndFeel (&laf);
    content = std::make_unique<Content> (p);
    addAndMakeVisible (*content);

    setResizable (true, true);
    setResizeLimits (kW / 2, kH / 2, kW * 2, kH * 2);
    getConstrainer()->setFixedAspectRatio ((double) kW / (double) kH);
    setSize (kW, kH);
}

VoxHaloEditor::~VoxHaloEditor()
{
    content.reset();
    setLookAndFeel (nullptr);
}

void VoxHaloEditor::resized()
{
    if (content != nullptr)
    {
        content->setTransform ({});
        content->setBounds (0, 0, kW, kH);
        content->setTransform (AffineTransform::scale ((float) getWidth() / (float) kW));
    }
}
