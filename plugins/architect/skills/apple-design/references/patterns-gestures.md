# Gestures and Common Interaction Patterns

Source: `.../gestures`; other pattern pages (Onboarding, Searching, Undo and redo, Modality, Multitasking, Loading, Settings, etc.) aren't summarized individually here — look up the slug under the Patterns category in [hig-sitemap.md](hig-sitemap.md).

## Gesture general principles

- **Never assume a user can only complete a task with one specific gesture** — voice, keyboard, and Switch Control are equally common input methods, see [accessibility.md](accessibility.md)
- **Gesture behavior should match expectations** — "tap" should always mean activate/select; don't repurpose a common gesture (tap, swipe) for something unrelated, and don't invent a custom gesture for a standard operation (activating a button, scrolling a long view)
- **Respond to gestures responsively** — provide feedback during the interaction so people can predict the outcome, and if necessary indicate how much motion is needed to complete the action
- **Clearly indicate when a gesture isn't available** — without a clear signal, people may think the app has frozen or that they're performing the gesture wrong — e.g. dragging a locked object, or tapping an unavailable button, both need a visibly distinct state

### Custom gestures

Only add a custom gesture when a task is high-frequency and no existing standard gesture covers it (e.g. a drawing app or game), and make sure it is: **discoverable, easy to perform, distinct from other gestures, and not the only way to perform an important action**. Use shortcut gestures to supplement standard gestures, not replace them — e.g. an app supporting hierarchical navigation should still keep a Back button in the top toolbar, even if it also offers an edge-swipe shortcut.

Avoid conflicts with gestures that access system UI (like watchOS edge swipes or the visionOS palm-flip gesture for system overlays).

### Standard gesture quick reference by platform

| Platform | Gesture | Common action |
|---|---|---|
| iOS/iPadOS | Three-finger swipe | Undo (swipe left) / Redo (swipe right) |
| iOS/iPadOS | Three-finger pinch | Copy (pinch in) / Paste (pinch out) |
| iPadOS | Four-finger swipe | Switch between apps |
| iOS/iPadOS | Shake | Undo / Redo |
| visionOS (indirect) | Look at an object + pinch fingers | Focus and select/activate |
| visionOS (direct) | Touch / touch-and-hold / drag / double-touch / swipe | Select or activate / open a contextual menu / move / preview or select a word / reveal actions, dismiss, or scroll |
| visionOS (direct, two hands) | Pinch and drag apart/together, or in a circular motion | Zoom / rotate |

- **macOS**: primarily keyboard and mouse, plus standard gestures on a Magic Trackpad/Magic Mouse or a game controller with a touch surface
- **tvOS**: standard gestures via a compatible remote (including Siri Remote) or a game controller with a touch surface
- **visionOS**: two gesture categories — "indirect" (look at a target, then manipulate it from a distance with your hands — comfortable at any distance, good for quickly switching focus between objects) and "direct" (physically touch a virtual object — best within reach, since raised arms tire quickly with extended use). Support both where possible, favoring standard components (like buttons) that work either way

### Designing custom gestures for visionOS

- Requires running in a Full Space and requesting permission to access hand information
- Prioritize comfort — avoid requiring extended raised-arm poses, and avoid repetitive similar movements that stress muscles/joints
- Be cautious with complex gestures requiring multiple fingers or both hands — people may not always have both hands free; offer a lower-effort alternative for a complex gesture
- Avoid gestures that require a specific hand — this adds cognitive load and can be less welcoming to people with strong hand-dominance or limb differences

## Other common patterns, quick list (see the original pages for detail)

These pages aren't summarized in depth in this skill, but are worth reading in full (URLs in [hig-sitemap.md](hig-sitemap.md)) before designing the related functionality, to avoid a flow that doesn't match platform conventions:

- **Onboarding** — how to design a first-run experience, and when a guided flow is (or isn't) warranted
- **Searching** — platform conventions for search fields, suggestions, and result presentation
- **Undo and redo** — how to implement consistent undo across platforms
- **Modality** — when a modal view (which interrupts the current flow) is appropriate
- **Multitasking** — design guidance for multi-window/split-screen scenarios on iPadOS/macOS
- **Loading** — choosing the right loading indicator and timing
- **Settings** — how to organize an in-app settings screen
- **Feedback** — how to communicate action results and system state
- **Drag and drop** — designing cross-app/cross-window drag-and-drop interactions
- **Managing notifications** — designing local/push notifications and their pacing

## Related resources
- Developer docs: `Standard gestures`, `Setting up access to ARKit data` (visionOS custom gesture permissions)
- Related pages: [platforms.md](platforms.md) (per-platform Inputs characteristics), [accessibility.md](accessibility.md) (accessible alternatives to gestures)
