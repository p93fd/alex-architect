# Apple Design Resources (Tools and Downloads)

Source: `https://developer.apple.com/design/resources/`, `https://developer.apple.com/design/get-started/`

When a user is ready to start producing actual design work, point them to these official resources instead of having them redraw every standard control from scratch — Apple ships official UI Kits and templates that update with each system release and stay pixel-accurate to system components.

## UI Kits (one per platform, rebuilt yearly alongside the major OS releases)

| Platform | Formats | Notes |
|---|---|---|
| iOS & iPadOS | Figma, Sketch | Official UI Kit + app icon template (Figma/Sketch/Photoshop/Illustrator) |
| macOS | Figma, Sketch | Official UI Kit |
| watchOS | Figma, Sketch | Official UI Kit |
| visionOS | Figma, Sketch | Official UI Kit + design templates |
| tvOS | Sketch | UI Kit (Sketch Library) + design templates + production templates (Sketch/Photoshop) |

⚠️ These kits get rebuilt around each WWDC (typically June) — always grab the latest version rather than relying on an older kit's component styles, which may be outdated (especially since Liquid Glass in 2025 rebuilt the iOS/iPadOS/macOS kits from scratch).

## Technology-specific templates

App Clips, Apple Pay, Live Activities, Messages/iMessage, Sign in with Apple (logo and buttons, in Figma/Sketch/PNG/PDF/SVG), Siri & App Shortcuts, Tap to Pay on iPhone, TipKit, Wallet, Camera Control (Sketch) — all ship Figma/Sketch templates to keep your integration visually on-brand with the system.

## Glyphs and icon assets

Official glyphs (PNG/PDF/SVG) for Add to Apple Watch Face, AirPlay, ARKit badges, Apple Health, Games and Game Center, HomeKit, Siri icons, etc. — used to correctly represent these system capabilities in marketing pages or in-app UI. Brand-related glyph usage terms (Apple Health, Wallet, Music, Pay, etc.) are covered separately at `/licensing-trademarks/`.

## Fonts

| Font | Use |
|---|---|
| SF Pro | System font for iOS / iPadOS / macOS / tvOS |
| SF Compact | System font for watchOS |
| SF Mono | Monospace font for contexts like Xcode |
| New York (NY) | Reading/display serif face, pairs with SF |
| SF Arabic / SF Armenian / SF Georgian / SF Hebrew | System fonts for the corresponding scripts |

See [typography-symbols.md](typography-symbols.md) for details.

## SF Symbols

The symbol library — 7,000+ symbols, 9 weights, 3 scales, with a new major version each WWDC (SF Symbols 7 added gradient rendering and Draw animations). Check the download page for the current version and its macOS requirement. See [typography-symbols.md](typography-symbols.md) for details.

## Other tools

- **Icon Composer** — builds layered, Liquid-Glass-capable app icons for multiple platforms; bundled with Xcode, also downloadable separately. See [app-icons.md](app-icons.md)
- **Parallax Previewer** — previews the parallax effect for tvOS/visionOS icons (Mac app)
- **Pass Designer** — creates and previews Apple Wallet passes (Mac app)
- **Reality Composer Pro** — previews and prepares 3D content (relevant to visionOS)

## Product bezels (device mockup frames)

Photoshop/PNG device bezels for building App Store assets and demo images: Apple TV, Apple Watch, iPad, iPhone, and Mac (Studio Display/iMac/MacBook line). Apple refreshes these after each hardware announcement, so grab the current set rather than reusing last year's frames.

## A suggested path from getting started to shipping (from the Get Started page)

1. **Understand the design principles** — start with the official "Principles of great design" video series and [principles.md](principles.md)
2. **Get familiar with the HIG's structure** — Getting started → Foundations → Patterns → Components → Inputs → Technologies, see [hig-sitemap.md](hig-sitemap.md)
3. **Build your toolbox** — download the relevant UI Kit, fonts, and SF Symbols for your platform, and use them as the basis for your designs instead of redrawing standard controls
4. **Prototype and validate** — Apple recommends validating ideas as cheaply as possible (fake prototyping, 60-second rapid prototyping, SwiftUI prototypes), catching problems early instead of waiting until the visuals are finished to test whether the interaction actually works
5. **Look to the community for inspiration** — Apple Design Award winners and developer interviews are a good source of ideas

## Related links

- Human Interface Guidelines: `https://developer.apple.com/design/human-interface-guidelines/`
- Design Resources: `https://developer.apple.com/design/resources/`
- SF Symbols app download page: `https://developer.apple.com/sf-symbols/`
- Design-related videos: `https://developer.apple.com/videos/design`
- Apple Design Awards: `https://developer.apple.com/design/awards/`
