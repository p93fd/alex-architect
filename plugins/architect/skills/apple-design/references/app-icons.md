# App Icons

Source: `.../app-icons`

The icon is a core part of an app's brand and user experience — it appears on the Home Screen, in search results, notifications, system settings, and share sheets, and needs to clearly and consistently convey your app's identity across every Apple platform.

## Layer design

Layered icons let the system apply dynamic visual effects that create depth:

- **iOS / iPadOS / macOS / watchOS**: a background layer plus one or more foreground layers; the system applies Liquid Glass properties (specular highlights, refraction, translucency) that scale automatically with icon size and may vary slightly across system versions
- **tvOS**: 2-5 layers; on focus, foreground content lifts toward the viewer with a slight sway and a sweeping highlight, creating parallax
- **visionOS**: a background layer plus 1-2 foreground layers forming a three-dimensional object that gently expands when looked at; the system adds shadows and uses the alpha channel of upper layers to create an embossed appearance

**Workflow**: build each foreground layer in any design tool, then import them into **Icon Composer** (bundled with Xcode, also downloadable separately from the Apple Developer site) — define the background layer, adjust foreground-layer placement, apply effects like specular highlights and refraction, annotate default/dark/mono appearance variants, preview and test across system versions, then export for Xcode. tvOS and visionOS icons are assembled directly as an image stack in Xcode, previewable with the **Parallax Previewer**.

**Design guidance**:
- Keep foreground-layer edges clean and well-defined — avoid soft/feathered edges, which look odd once the system applies its own highlights and shadows
- Varying opacity across foreground layers adds depth and vitality
- Design a background (solid color or gradient) that emphasizes the foreground and responds well to system lighting effects; prefer vector graphics (SVG/PDF) when importing into Icon Composer since they scale without loss, and use PNG (lossless) for gradients/raster art

## Icon shape

- iOS/iPadOS/macOS: square, masked into rounded corners matching device bezel curvature and other rounded interface elements
- tvOS: rectangular, with matching concentric rounded corners
- visionOS/watchOS: square, masked into a circle

**Always provide unmasked, appropriately shaped layers** and let the system apply the mask — pre-masking or pre-cropping interferes with specular highlight effects and can produce jagged edges. Keep primary content centered, especially for visionOS and watchOS, to avoid truncation from circular masking (use the grids in the app icon production templates for alignment help).

## Design principles

- **Embrace simplicity** — simple icons are easiest to recognize; too much detail looks busy once the system applies shadows/highlights, and can be hard to discern at small sizes. Find one concept that captures your app's essence and express it with a minimal set of shapes; keep the background simple (a solid color or gradient is enough — you don't need to fill the whole canvas)
- **Keep the design visually consistent across every platform you support**, so people don't mistake your app for a different one
- **Consider building around overlapping solid shapes** — paired with transparency and blur, this naturally produces a sense of depth
- **Include text only when essential** — text in icons doesn't support accessibility or localization, is often too small to read, and the app name is usually already shown nearby. If you do include text (like an initial), avoid non-essential words that tell people what to do ("Watch," "Play") or context-specific terms ("New," "For visionOS")
- **Prefer illustration over photography** and avoid replicating UI components — photos are full of detail that doesn't hold up across appearance modes, small sizes, or when split into layers; don't reproduce app screenshots or standard UI controls in an icon
- **Never reproduce Apple hardware products** (copyrighted) in an app icon

## Visual effects

- **Let the system handle blur and other effects** — you don't need to add specular highlights, drop shadows, beveled edges, blurs, or glows yourself; the system's effects are dynamic, while custom ones are static and can conflict. If you do add custom effects, test carefully in Icon Composer, a simulated device, or a physical device
- **Group layers to apply an effect to several at once** — system effects normally apply per-layer, but you can group layers in Icon Composer or your design tool, which unlocks additional Liquid Glass customization (specular highlights, refraction, translucency) at the group level

## Appearances

On iOS/iPadOS/macOS, people can choose their Home Screen icon appearance: **default / dark / clear / tinted** (e.g. to complement their wallpaper). You can design a variant for each, and the system auto-generates any you don't provide.

- Keep the icon's core features consistent across appearances — avoid swapping elements in and out between variants, which makes it harder to recognize your app after switching
- Dark and tinted/clear icons should be more subdued while remaining visible, legible, and recognizable
- Base your dark icon on the light one, choosing complementary colors and avoiding overly bright imagery — solid color backgrounds usually give the best contrast for dark icons
- Consider offering **alternate app icons** (supported on iOS, iPadOS, tvOS, and compatible visionOS apps), letting people choose a variant from settings — keep every alternate closely tied to your content/experience to avoid confusion with a different app

## Platform notes

- **tvOS**: keep a safe zone so content isn't cropped during focus animation — the safe zone varies with image size, layer depth, and motion, and foreground layers get cropped more than background layers
- **visionOS**: avoid adding a shape in the background layer that looks like a hole or concave area (the system already adds a similar effect)

## Related resources

- Tool: **Icon Composer** (bundled with Xcode, also available separately from the Apple Developer site)
- Apple Design Resources: per-platform icon production templates (Figma/Sketch/Photoshop/Illustrator), Parallax Previewer / Parallax Exporter plugins (see [resources.md](resources.md))
- Developer docs: `Creating your app icon using Icon Composer`, `Configuring your app icon using an asset catalog`
- Related pages: [materials-color.md](materials-color.md) (general Liquid Glass principles)
