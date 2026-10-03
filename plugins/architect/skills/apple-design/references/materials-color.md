# Materials, Liquid Glass, and Color

Source: `.../materials`, `.../color`

## What is a Material

A material is a visual effect that creates a sense of depth, layering, and hierarchy — it separates foreground elements (text, controls) from background elements (content, solid colors), with background color bleeding through into the foreground to help people retain a sense of place. Apple platforms have two kinds of materials:

1. **Liquid Glass** — the dynamic material introduced in 2025 that unifies the design language across platforms
2. **Standard materials** — used for visual differentiation *within* the content layer (blur, vibrancy, blend modes, etc.)

## Liquid Glass: when and how to use it

Liquid Glass forms a distinct functional layer for **controls and navigation elements** (tab bars, sidebars) that floats above the content layer — content can scroll and peek through beneath it, creating a sense of dynamism and depth while keeping controls legible.

**Core rules**:
- **Don't use Liquid Glass in the content layer.** Its value comes from clearly separating "interactive controls" from "content"; using it in the content layer (e.g. app backgrounds) muddies the hierarchy. Use standard materials there instead. Exception: transient interactive controls in the content layer (sliders, toggles) may briefly take on a Liquid Glass appearance when activated, to emphasize interactivity.
- **Use it sparingly.** Standard system components pick up Liquid Glass appearance and behavior automatically. If you apply it manually to a custom control, reserve it for your most important functional elements — overusing it distracts from the underlying content.
- **Two variants, different purposes**:
  - **Regular**: blurs and adjusts the luminosity of background content to keep foreground text/elements legible; a scroll edge effect further blurs and reduces the opacity of background content. Most system components use this. Best when background content risks legibility issues, or the component has significant text (alerts, sidebars, popovers).
  - **Clear**: highly translucent, prioritizing visibility of rich underlying content. Use only for components floating over visually rich media backgrounds (photos, video). Decide whether to add a dimming layer: if the underlying content is bright, add a 35%-opacity dark dimming layer behind it; if the underlying content is already sufficiently dark, or you're using AVKit's own media-playback controls with a built-in dimming layer, skip it.

### Standard materials

Use blur, vibrancy, and blend modes to convey structure within the content layer. Choose a material based on **semantic meaning and recommended usage**, not the color it happens to render — because system settings can change its appearance and behavior. Thicker materials are more opaque and give better contrast for fine text; thinner materials are more translucent and help people retain a visible reminder of the background content.

iOS/iPadOS provide 4 thickness levels: `ultraThin` / `thin` / `regular` (default) / `thick`, each paired with matching vibrancy values for labels, fills, and separators (label/secondaryLabel/tertiaryLabel/quaternaryLabel, etc.).

### Platform differences

- **iOS / iPadOS**: 4 standard material thicknesses plus matching vibrancy values; avoid `quaternary` vibrancy on `thin`/`ultraThin` materials (contrast is too low)
- **macOS**: several standard materials with defined purposes, and vibrant versions of every system color; two background blend modes — behind window / within window
- **tvOS**: Liquid Glass appears in navigation elements, Top Shelf, Control Center, and other system experiences; images/buttons pick it up when focused
- **visionOS**: windows default to a system-defined material called `glass` (not customizable), letting light, the current Environment, virtual content, and physical surroundings show through. **visionOS has no separate Dark Mode** — `glass` automatically adapts to ambient luminance. Prefer translucency over opaque solid backgrounds to avoid a boxed-in feeling
- **watchOS**: materials are commonly used in full-screen modal views to establish hierarchy and orientation; don't remove or replace the system's default modal-sheet background material

## Liquid Glass color rules

Liquid Glass has **no inherent color by default** — it tints itself from whatever content sits behind it. You can apply color to some Liquid Glass elements to create a "stained glass" effect — commonly used to emphasize a control (e.g. a primary call-to-action, which is how the system styles prominent buttons like Done). Symbols or text on Liquid Glass controls can also carry color.

- Small elements (toolbars, tab bars): the system adapts Liquid Glass between light and dark appearance based on the underlying content; symbols and text default to a monochrome scheme (darker on light content, lighter on dark content)
- Large elements (sidebars): Liquid Glass becomes more opaque to preserve legibility over complex backgrounds
- **Use color sparingly** — reserve it for elements that genuinely benefit from emphasis (status indicators, primary actions), and prefer tinting the **background** over symbols/text
- If your app's content layer is already colorful, avoid using a similar color for toolbar/tab bar labels — it'll clash and become hard to read; prefer a monochrome scheme or an accent color with more contrast

## The Color system

### Core principles
- **Keep a color's meaning consistent** throughout the interface, especially when it communicates status or interactivity
- **Test in light, dark, and increased-contrast modes** — system colors adjust contrast automatically for these; custom colors need light/dark variants plus a higher-contrast variant for each — provide both light and dark variants even for a single-appearance app, to support Liquid Glass adaptivity
- **Don't redefine the semantic meaning of a system color** (e.g. don't use a separator color as a text color)
- **Never rely on color alone** to convey information — people with color blindness may not distinguish red/green or blue/orange combinations, so pair color with text labels or shape cues
- **Consider cultural context** — the same color can carry opposite meanings across cultures (Stocks shows gains in green for English but red for Chinese)
- **Don't hard-code system color values** — use color APIs (like `Color`) so values can evolve across releases

### Wide color
Displays supporting the P3 gamut can render richer, more saturated colors than sRGB. Use Display P3 (16-bit/channel) for photos, video, and data visualizations where appropriate, and check P3 gradients for banding when viewed on sRGB screens.

### Semantic system colors, quick reference (iOS example; see the original for other platforms)
iOS defines two dynamic background color sets (system / grouped), each with primary/secondary/tertiary levels expressing hierarchy: primary for the overall view, secondary for grouping within it, tertiary for sub-grouping within secondary. Foreground content maps to semantic colors like label / secondaryLabel / tertiaryLabel / quaternaryLabel / placeholderText / separator / opaqueSeparator / link. macOS defines a larger set of dynamic colors (control text, selection, highlight, grid lines, etc.) — check the original `.../color` page for exact values and API names when precision matters.

## Related resources

- Developer docs: `glassEffect(_:in:)` (SwiftUI), `Material` (SwiftUI), `UIVisualEffectView` (UIKit), `NSVisualEffectView` (AppKit)
- Videos: "Meet Liquid Glass," "Get to know the new design system"
- Related pages: [accessibility.md](accessibility.md) (contrast requirements), Dark Mode (not detailed here, see [hig-sitemap.md](hig-sitemap.md))
