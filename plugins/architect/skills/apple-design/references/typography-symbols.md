# Typography and SF Symbols

Source: `.../typography`, `.../sf-symbols`

## System font families

Apple provides two typeface families spanning a wide range of weights, sizes, styles, and languages. **Prefer system fonts over embedding your own**:

- **San Francisco (SF)** — sans serif, including SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian, SF Hebrew, SF Mono, plus rounded variants for pairing with soft/rounded UI or a different typographic voice
- **New York (NY)** — a serif family designed to work well on its own or alongside SF

Both ship as **variable fonts** supporting continuous optical-size interpolation — the system automatically interpolates between weights/widths for the current point size, so you generally don't need to pick discrete Text/Display optical sizes manually.

Per-platform system fonts: iOS/iPadOS/macOS/tvOS/visionOS use SF Pro (Mac Catalyst apps can also use NY); watchOS uses SF Compact (SF Compact Rounded in complications).

## Text Styles and Dynamic Type

The system defines a set of "text styles" (Large Title, Title, Headline, Body, Caption, etc.), each bundling a weight/size/leading combination into a typographic hierarchy. **Prefer built-in text styles** — doing so gets you Dynamic Type support for free, so text scales when people adjust the system-wide text size.

Use symbolic traits to tweak a built-in style when needed (e.g. `bold()` for emphasis), and adjust leading if necessary (loose leading suits wide columns/long passages; tight leading suits constrained spaces, but avoid overly tight leading once you have three or more lines).

### Sizes, weight, and legibility

The per-platform default and minimum type sizes live in the Specifications table in [accessibility.md](accessibility.md) — the single source for every number in this skill.

- Font weight also affects legibility: bump size up for thin weights
- **Generally avoid Ultralight/Thin/Light weights**, which are hard to read especially at small sizes; prefer Regular/Medium/Semibold/Bold
- Custom fonts need to implement their own Dynamic Type support and accessibility behaviors (like responding to Bold Text)

### Designing for Dynamic Type

- Layouts need to adapt at every text size: side-by-side elements may need to stack vertically at larger sizes; single-line list/table rows may need to grow to multiple lines instead of clipping
- Scale up meaningful icons alongside larger text sizes (SF Symbols scale automatically with Dynamic Type)
- Minimize truncation — avoid truncating text in scrollable regions unless people can open a separate view for the full content
- In horizontally constrained contexts, reduce multi-column layouts to fewer columns as text size increases
- Keep the relative hierarchy of primary elements consistent regardless of text size

## SF Symbols

A library of thousands of configurable symbols that integrate seamlessly with the San Francisco system font, automatically matching text at any weight or size. Use symbols anywhere an interface icon can appear: toolbars, tab bars, context menus, inline in text.

⚠️ **Important restriction**: SF Symbols' terms of use explicitly prohibit using symbols (or confusingly similar imagery) as app icons, logos, or in any other trademark-related use.

### Rendering modes

Symbols organize their paths into layers (primary/secondary/tertiary). Four rendering modes control how color is applied:

- **Monochrome** — one color across all layers
- **Hierarchical** — one color applied at varying opacities per layer, creating depth
- **Palette** — two or more colors assigned across layers
- **Multicolor** — some symbols carry intrinsic semantic colors (e.g. `leaf` is green, `trash.slash` is red to signal data loss)

Using system-provided colors ensures symbols automatically adapt to accessibility settings, vibrancy, and Dark Mode.

### Weights and scales

- **9 weights** (ultralight → black), matching San Francisco's font weights for precise weight-matching between symbols and adjacent text
- **3 scales** (small / medium default / large), defined relative to San Francisco's cap height, letting you emphasize a symbol relative to nearby text without breaking weight-matching at the same point size

### Design variants

- **Outline** (most common) — no filled areas, reads like text
- **Fill** — solid interior shapes, more visual emphasis — good for iOS tab bars and swipe actions where accent color communicates selection
- **Slash / Enclosed** — combine with outline/fill; slash signals "unavailable," enclosing shapes (circle/square) improve legibility at small sizes
- Some symbols also provide script-specific variants (Arabic, Hebrew, Hindi, Thai, CJK, Cyrillic, Devanagari, and several Indic numeral systems) that switch automatically with device language

### Gradients (SF Symbols 7+)

Generate a smooth linear gradient from a single source color, usable across all rendering modes and both system and custom colors/symbols — looks best at larger sizes.

### Variable color

Represents a value that changes over time (signal strength, volume) by coloring different layers as thresholds are crossed. **Use it to communicate change, not depth** (use Hierarchical rendering for depth).

### Animations (SF Symbols 4+, expanding over time)

- **Appear / Disappear** — fade in/out
- **Bounce** — a single elastic scale to signal that an action happened or is needed
- **Scale** — resizes and holds until explicitly changed or removed
- **Pulse** — cycles opacity to indicate ongoing activity
- **Variable color animation** — colors layers progressively to show progress/connecting/playing; layouts are either open loop (linear, ends don't meet) or closed loop (ends meet, e.g. a circular progress ring)
- **Replace** — transitions between two symbols, in down-up / up-up / off-up configurations
- **Magic Replace** — a smart transition between shape-related symbols (e.g. a slash animates on/off)

## Related resources

- Download SF Pro / SF Compact / New York fonts: Apple Design Resources (see [resources.md](resources.md))
- SF Symbols app (browse and export symbols): see [resources.md](resources.md)
- Developer docs: `Font.Design` (SwiftUI — don't embed system font files, use this API instead), `Symbols`, `SymbolEffect`
