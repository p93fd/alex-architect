# Platform Design Characteristics (Designing for...)

Source: `.../designing-for-ios`, `-ipados`, `-macos`, `-watchos`, `-visionos` (also `-tvos`, `-games`, `-iphone-duo`, not detailed here — look them up in [hig-sitemap.md](hig-sitemap.md) when needed)

Every platform page follows the same framework: **Display / Ergonomics / Inputs / App interactions / System features**, followed by Best practices. When giving cross-platform design advice, apply this same framework to analyze what makes the target platform distinct.

## iOS (iPhone)

- **Display**: medium-size, high-resolution screen
- **Ergonomics**: held in one or both hands, switching freely between portrait and landscape, viewing distance typically within 1-2 feet
- **Inputs**: multi-touch gestures, virtual keyboard, voice control; often combined with personal data and gyroscope/accelerometer input
- **App interactions**: ranges from a few seconds of "checking in" to over an hour of immersive use; people routinely switch between multiple open apps
- **System features**: Widgets, Home Screen quick actions, Spotlight, Shortcuts, Activity views
- **Best practices**:
  - Limit onscreen controls so primary tasks/content hold attention, while keeping secondary details/actions discoverable without being distracting
  - Adapt seamlessly to orientation changes, Dark Mode, and Dynamic Type
  - Put frequently used controls in the middle-to-bottom of the screen — easiest to reach one-handed; support swipe-to-navigate-back and swipe actions in list rows
  - With permission, use platform capabilities (biometric payment authentication, location, etc.) to reduce manual data entry

## iPadOS (iPad)

- **Display**: large, high-resolution screen
- **Ergonomics**: held, or set on a surface/stand; viewing distance typically within about 3 feet
- **Inputs**: multi-touch, external keyboard/trackpad, Apple Pencil, voice — often combined
- **App interactions**: from a few quick actions to hours of content creation/productivity; people frequently keep multiple apps open, viewing more than one onscreen at once and relying on drag and drop between them
- **System features**: Multitasking, Widgets, drag and drop
- **Best practices**:
  - Use the large display to elevate the content people care about, minimize modal interfaces and full-screen transitions, and place controls where they're reachable but not in the way
  - Let viewing distance and input mode inform the size and density of onscreen content
  - Support multi-touch, a physical keyboard/trackpad, or Apple Pencil, and consider interactions that combine multiple input modes
  - Adapt seamlessly to orientation, multitasking modes, Dark Mode, Dynamic Type, and transition smoothly to running under macOS via Mac Catalyst

## macOS (Mac)

- **Display**: large, high-resolution screen, often extended with additional displays (including using an iPad as one)
- **Ergonomics**: typically used while stationary, viewing distance about 1-3 feet
- **Inputs**: physical keyboard, pointing devices (mouse/trackpad), game controllers, Siri — expect any combination
- **App interactions**: from a few minutes of quick tasks to hours of deep focus; multiple apps are frequently open at once, with expected smooth transitions between active/inactive states
- **System features**: the menu bar, file management, going full screen, Dock menus
- **Best practices**:
  - Leverage the large display to show more content with fewer nested levels and less modality, while keeping information density comfortable
  - Let people freely resize, hide, show, and move windows, and support full-screen mode for a distraction-free context
  - Use the menu bar to give people easy access to every command
  - Support high-precision input for pixel-perfect selection and editing
  - Handle keyboard shortcuts well to support keyboard-only workflows
  - Support personalization: customizable toolbars, configurable window views, and choice of interface colors/fonts

## watchOS (Apple Watch)

- **Display**: small but high-resolution, built for the wrist
- **Ergonomics**: viewing distance under a foot, typically interacted with by raising the wrist and using the other hand; Always On display lets people glance at information without raising their wrist
- **Inputs**: Digital Crown (consistent vertical navigation across watch face, Home Screen, and apps), standard gestures (tap, swipe, drag) usable even while moving, the Action button for triggering an action without looking at the screen, Shortcuts for routine tasks, plus device sensor data (GPS, blood oxygen, heart function, altimeter, accelerometer, gyroscope)
- **App interactions**: many sub-minute glances throughout the day; people often use a watchOS app's related experiences — complications, notifications, Siri — more than the app itself
- **System features**: Complications, Notifications, Always On, Watch faces
- **Best practices**:
  - Support quick, glanceable, single-screen interactions that deliver critical information succinctly and let people act with a gesture or two
  - Minimize navigation depth; use the Digital Crown for vertical navigation
  - Anticipate people's needs proactively and surface on-device data that's relevant right now or very soon
  - Use complications to put relevant, potentially dynamic data on the watch face, reachable with every wrist raise or tap
  - Use notifications to deliver timely, high-value information that lets people act without opening the app
  - Design the app to function independently, complementing notifications and complications rather than duplicating them

## visionOS (Apple Vision Pro)

- **Core concepts**: Space (an infinite 3D canvas), Immersion (levels ranging from the Shared Space, where multiple apps coexist, through a Full Space where one app runs alone, up to fully immersive experiences), Passthrough (live external-camera video), Spatial Audio, and Eyes and hands (indirect/direct gestures)
- **Ergonomics**: content is positioned relative to the wearer's head by default, independent of height or whether they're sitting, standing, or lying down; visual comfort is paramount since everything the person sees — real and virtual — comes through the device's cameras
- **Accessibility**: natively supports VoiceOver, Switch Control, Dwell Control, Guided Access, Head Pointer, and more
- **⚠️ Safety note**: not for use while driving or operating heavy machinery; not designed for moving through hazardous environments (balconies, streets, stairs); intended for people 13 years of age or older
- **Best practices**:
  - Lean into space, Spatial Audio, and immersion to bring an experience to life, while making passthrough and eye/hand input feel natural
  - Find the minimum immersion level suited to each key moment — don't assume every moment needs to be fully immersive
  - Use standard windows (floating planes in space) for UI-centric tasks; people can freely relocate windows, and the system's dynamic scaling keeps content legible near or far
  - Prioritize comfort:
    - Keep content within the person's field of view, positioned relative to their head — avoid requiring head turns or repositioning to interact
    - Avoid motion that's overwhelming, jarring, too fast, or lacking a stationary frame of reference
    - Support indirect gestures that let people interact with their hands resting in their lap or at their sides
    - If supporting direct gestures, keep interactive content within reach and avoid requiring extended interaction
    - Avoid encouraging excessive physical movement during a fully immersive experience
  - Use SharePlay for shared activities so participants' spatial Personas make it feel like everyone is together in the same space

## Cross-platform quick comparison

When designing a cross-platform feature or making a platform-adaptation decision, use these dimensions as a quick reference (see also [layout.md](layout.md) and [accessibility.md](accessibility.md)):

| Dimension | iOS | iPadOS | macOS | watchOS | visionOS |
|---|---|---|---|---|---|
| Primary navigation | Tab bar | Tab bar / sidebar, adaptive | Menu bar + sidebar | Digital Crown + lists | Floating tab bar / sidebar |
| Freely resizable windows | No | Yes (multitasking/split view) | Yes | N/A | Yes (movable, resizable windows) |

Per-platform **numbers** — default and minimum text sizes, default and minimum control sizes, contrast ratios — live in one place only: the Specifications tables in [accessibility.md](accessibility.md). Read them there rather than from a copy, and note that "default" and "minimum" are two different columns that are easy to conflate.
