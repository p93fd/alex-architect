# Accessibility

Source: `.../accessibility`

**This file holds the authoritative specs tables for the whole skill** — type sizes, control sizes, and contrast ratios. Other files link here instead of copying the numbers. Note the two distinct columns in each table: *default* is the design target, *minimum* is the absolute floor.

Accessibility isn't an "extra feature" — it's what lets more people actually use your product, which directly echoes the Flexibility principle in [principles.md](principles.md). An accessible interface should be:

- **Intuitive** — uses familiar, consistent interactions that make tasks straightforward
- **Perceivable** — doesn't depend on a single sensory channel; content and interaction should work through sight, hearing, speech, or touch
- **Adaptable** — supports system-level accessibility features and lets people personalize settings to their needs

Use **Accessibility Inspector** during design to catch accessibility issues, and communicate your app's support level to users via App Store Connect's **Accessibility Nutrition Labels**.

## Vision

- **Support larger text sizes** — ideally let people enlarge text/icons by at least 200% (140% on watchOS), through custom UI or by adopting Dynamic Type
- **Use the recommended defaults for custom type sizes**, matching the table below:

  | Platform | Default size | Minimum size |
  |---|---|---|
  | iOS, iPadOS | 17pt | 11pt |
  | macOS | 13pt | 10pt |
  | tvOS | 29pt | 23pt |
  | visionOS | 17pt | 12pt |
  | watchOS | 16pt | 12pt |

- **Meet minimum contrast standards** — Apple uses WCAG Level AA as the basis for Accessibility Inspector's contrast checks:

  | Text size | Weight | Minimum contrast ratio |
  |---|---|---|
  | ≤17pt | Any | 4.5:1 |
  | 18pt | Any | 3:1 |
  | Any | Bold | 3:1 |

  If your default palette doesn't meet this, at minimum provide a higher-contrast palette when the system's Increase Contrast setting is on, and check contrast separately for Dark Mode.
- **Prefer system-defined colors** — they carry their own accessible variants that automatically adjust for Increase Contrast and light/dark appearance
- **Never rely on color alone** — people with red-green or blue-orange color blindness may not distinguish certain combinations, so pair color with shapes or icons
- **Describe your interface and content for VoiceOver** — VoiceOver is a screen reader that lets people use your app without seeing the screen, which requires meaningful labels and hints on interactive elements

## Hearing

- **Provide text-based alternatives for audio/video** — dialogue and critical information should never depend on audio alone. Choose the right format for the context:
  - **Captions** — the text equivalent of audible information, synced live, good for game cutscenes and video clips
  - **Subtitles** — translated onscreen dialogue, good for film/TV
  - **Audio descriptions** — spoken narration inserted into natural pauses to describe visual-only information
  - **Transcripts** — a full text description (audio + visual), good for long-form media like podcasts and audiobooks
- **Pair audio cues with haptics** — success chimes, error sounds, or game feedback should have a matching haptic for people who can't perceive audio or have it off
- **Augment audio cues with visual cues** — especially important in games and spatial apps where important events might occur off screen

## Mobility

- **Make controls large enough**:

  | Platform | Default control size | Minimum control size |
  |---|---|---|
  | iOS, iPadOS | 44×44pt | 28×28pt |
  | macOS | 28×28pt | 20×20pt |
  | tvOS | 66×66pt | 56×56pt |
  | visionOS | 60×60pt | 28×28pt |
  | watchOS | 44×44pt | 28×28pt |

- **Spacing between controls matters as much as size** — around 12pt of padding for bezeled elements, about 24pt for non-bezeled elements, to reduce mis-taps
- **Support simple gestures for common interactions** — avoid custom multi-finger/multi-hand gestures as the only way to perform something frequent
- **Offer alternatives to gestures** — e.g. a "swipe to delete" action should also have an "edit mode, then tap to delete" path
- **Support Voice Control** — let people fully drive the device by speaking commands (perform gestures, interact with screen elements, dictate/edit text), which requires well-labeled interface elements
- **Integrate with Siri and Shortcuts** — let people automate frequent tasks via voice, the Action button, or Home Screen/Control Center shortcuts
- **Support mobility-related assistive technologies** — test with VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, and Switch Control, and make sure interface elements are labeled appropriately

## Speech

- **Support full keyboard-only navigation** — Full Keyboard Access should let people navigate and interact using only a physical keyboard; don't override system-defined accessibility keyboard shortcuts
- **Support Switch Control** — an assistive technology letting people control the device via external hardware, a game controller, or sounds (like a click), performing selection, tapping, typing, and drawing

## Cognitive

- **Keep actions simple and intuitive** — prefer system gestures and familiar behaviors over custom gestures people have to learn
- **Minimize time-boxed interface elements** — views/controls that auto-dismiss on a timer can be a problem for people who need more time to process information

## Related resources

- Tool: Accessibility Inspector (audit your interface's accessibility issues)
- Developer docs: `Voice Control`, `Switch Control`, `Selecting subtitles and alternative audio tracks`, `Support Full Keyboard Access in your iOS app`
- Related pages: [typography-symbols.md](typography-symbols.md) (Dynamic Type), [materials-color.md](materials-color.md) (contrast and color), [platforms.md](platforms.md) (visionOS's list of accessibility technologies)
