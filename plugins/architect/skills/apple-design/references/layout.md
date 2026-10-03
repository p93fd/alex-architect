# Layout

Source: `.../layout`

## Visual hierarchy

- **Order content by importance** — people generally read top-to-bottom and leading-to-trailing, so put the most important items near the top and leading edge. To support right-to-left languages, prefer standard system components that adapt direction automatically rather than hard-coding it
- **Align elements and use indentation to convey hierarchy** — alignment makes an interface look organized and easy to scan; people assume aligned items are related, and perceive indented items as subordinate to what precedes them
- **Group related items** using whitespace, container shapes, or separators to show what belongs together
- **Use progressive disclosure** — too much content and too many choices at once make things harder to find. Use disclosure triangles, menus, or nested views to hide secondary content initially, or scrollable sections for media-heavy apps (video, music, books)
- **Differentiate controls from content** — on platforms that support it, use Liquid Glass to make controls visually float above content. Instead of a solid/semi-opaque background under controls, use a scroll edge effect to elevate controls visually. Extend full-screen background content underneath sidebars, toolbars, and tab bars to fill the entire screen/window
- If scaling a background image to fill a window would cause components like sidebars or inspectors to cover important parts of it, use a background extension effect to mirror and blur the image beneath those components, giving the impression that the background extends underneath them

## Adaptability

Apps need to adapt to different display sizes, orientations, window sizes, and multitasking states. Common device/system characteristics to handle:

- Regular and compact horizontal/vertical size classes
- Different device screen sizes
- Different device orientations and aspect ratios
- System features like the Dynamic Island
- External display support, Display Zoom, resizable windows on iPad and Mac
- Text-size changes
- Locale-based internationalization: left-to-right/right-to-left layout, date/time/number formatting, font variation, text length

Even a locked-orientation app (e.g. a landscape-only game) still needs to resize well across devices and window sizes.

## Size classes (iOS / iPadOS)

Horizontal and vertical dimensions each have two levels — compact and regular — describing how much space is actually available:

- Horizontal size class: whether the app is narrow (compact) or wide (regular)
- Vertical size class: whether it's short (compact) or tall (regular)

The system sets size classes based on device type, window configuration, and multitasking state (full screen, Slide Over, iPhone Mirroring, etc.) — iPad apps can encounter every combination.

**Key principles**:
- **Design layout around size classes, not device type or orientation** — size classes describe actual available space, while orientation/idiom don't
- **Consider every combination of size classes** — a layout designed only for iPhone landscape (regular width/compact height) might waste the vertical space available when an iPad in landscape is resized to regular height, and vice versa
- **Keep functionality consistent as size classes change** — you can change how much functionality is visible, but not what the app can do. Take advantage of extra space to switch from a tab bar to a sidebar, or surface functionality that would otherwise sit in an overflow menu
- The app's idiom (the device type it's built for) doesn't change when size classes change — keep the layout recognizable and familiar to that platform even while resizing

## Guides and safe areas

- **Layout guide** — defines a rectangular region to help position, align, and space content. The system provides predefined guides (standard margins, readable text width) and you can also define custom ones
- **Safe area** — the part of a window not covered by a hardware feature or system UI (toolbar, tab bar, status bar, etc.). Respecting it is essential to avoid the Dynamic Island and similar features obscuring content

## Platform-specific notes

- **macOS**: avoid placing controls or critical information at the bottom of a window (people often drag windows so the bottom edge goes offscreen); avoid displaying content behind the camera housing at the top of the window
- **tvOS**: keep primary content inset from the screen's safe area — 60pt from top/bottom, 80pt from the sides — to accommodate TV compatibility settings and overscan cropping; focused elements enlarge, so leave enough spacing between focusable elements to avoid overlap
- **tvOS grid example**: for a two-column grid — unfocused content width 860pt, horizontal spacing 40pt, minimum vertical spacing 100pt (three- through nine-column grids have their own specs — check the original source for exact implementation values)

## Related resources

- Apple Design Resources provides layout templates and guides (see [resources.md](resources.md))
- Developer docs: `UILayoutGuide` / `NSLayoutGuide`, `SafeAreaRegions`, `backgroundExtensionEffect()`, `UIBackgroundExtensionView`, `UICollectionViewFlowLayout`
- Related pages: [materials-color.md](materials-color.md) (Liquid Glass and its relationship to the content layer), [typography-symbols.md](typography-symbols.md) (Dynamic Type's effect on layout)
