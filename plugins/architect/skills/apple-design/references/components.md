# Common Component Best Practices

Covers Buttons, Tab bars, Sidebars, Lists and tables, and Toolbars — the five most frequently needed components. For other components (Alerts, Sheets, Popovers, Context menus, Segmented controls, etc.), look up the matching slug in [hig-sitemap.md](hig-sitemap.md) and read the original page — their design logic follows the same pattern used here (clear roles/hierarchy plus platform-specific differences).

## Buttons

A button is defined by three attributes working together:
- **Style** — a visual style based on size, color, and shape
- **Content** — a symbol, text label, or both, conveying the button's purpose
- **Role** — a system-defined semantic role that can affect appearance: `Normal` (no specific meaning) / `Primary` (the default button, the one people are most likely to choose) / `Cancel` (cancels the current action) / `Destructive` (an action that can result in data loss)

**Best practices**:
- Hit target at least **44×44pt** (**60×60pt** on visionOS), with enough surrounding space to visually separate the button from neighboring content and controls. This matches the *default* control size in [accessibility.md](accessibility.md); the much smaller *minimum* control size in that table is an absolute floor for controls in general, not a target for buttons
- Always include a press state for a custom button — without one, it can feel unresponsive
- Keep **one or two** prominent-style buttons per view at most — too many increases cognitive load; use style (not size) to distinguish the preferred option among a set of choices
- **Assign the Primary role to the button people are most likely to choose** (it responds to Return, making quick confirmation easy), but **never assign Primary to a destructive action**, even if it's the most likely choice — people sometimes tap a visually prominent button without reading it, so keep Primary reserved for non-destructive actions
- Copy should start with a verb, using title-style capitalization, e.g. "Add to Cart"
- If the app's content layer is already colorful, avoid similar button-label colors; prefer the default monochrome appearance
- macOS has several button types of its own: Push buttons (the standard type, can display text/symbol/icon/image, can act as the view's default button and be tinted), Square buttons (icon-only, used inline within a view rather than a toolbar/status bar), and Help buttons (a circular question-mark button that opens contextual help documentation, at most one per window)

## Tab bars

Used to navigate between **top-level areas** of an app (not for placing actions — that's what a toolbar is for).

**Best practices**:
- Keep the tab bar visible while navigating between sections (a modal view temporarily covering it is the exception)
- Keep the number of tabs restrained — fewer tabs are easier to navigate; complex apps might use a sidebar, or iPadOS's adaptive "tab bar ↔ sidebar" switching
- Avoid overflow tabs — when horizontal space runs out, the trailing tab collapses into a "More" list, making that content harder to reach, so keep the total tab count low enough to avoid this
- Don't disable/hide a tab just because its section is temporarily empty — that makes the interface feel unstable; explain within the section why content is unavailable instead
- Pair tabs with text labels (single words when possible), and prefer SF Symbols' filled variant for platform consistency
- Use a badge (a red oval with white text or an exclamation point) sparingly, reserved for information that truly needs attention
- **If the app's content layer is already colorful** (e.g. gradient cards or colorful photos), avoid tab-label colors that clash with it — keep the default monochrome appearance, or choose an accent color with clearly more contrast. Full Liquid Glass color rationale is in the "Liquid Glass color rules" section of [materials-color.md](materials-color.md)
- **iOS**: the tab bar floats above content at the bottom of the screen with a Liquid Glass background that lets content peek through beneath it; can be paired with an attached accessory (like a mini player) that collapses on scroll; can include a dedicated search tab at the trailing end
- **iPadOS**: the tab bar sits near the top of the screen, can be fixed, or convertible to a sidebar with one tap; complex apps should offer the sidebar-conversion option; if letting people customize their tabs, aim for a default list of five or fewer
- **visionOS**: the tab bar is always vertical, floating fixed at the window's leading edge; it expands with text labels when looked at; a deep app hierarchy can nest a sidebar within a tab for secondary navigation (but selections in that sidebar shouldn't change the currently open tab)
- Not supported as a top-level navigation component on macOS; not supported on watchOS

## Sidebars

Used to navigate between **areas** or **top-level content collections** (folders, playlists, etc.), and needs substantial horizontal and vertical space — a tab bar is usually better when space is limited. Many apps don't need to choose one or the other, and instead use an adaptive style that switches between a tab bar and sidebar.

**Best practices**:
- Visually rich content can extend beneath the sidebar (paired with a background extension effect) to reinforce the sense of the sidebar floating above content
- Where possible, let people customize sidebar contents and ordering
- Use disclosure controls to collapse deep hierarchies and keep the sidebar from growing too tall
- Prefer SF Symbols for icons; icon color defaults to the app's accent color (which follows the user's global accent-color choice on macOS), and should only be fixed to a specific color when it's meaningful (e.g. Mail's VIP indicator uses yellow to stand out)
- Keep sidebar hierarchy to two levels or fewer; beyond that, consider a three-pane split view with a content list between the sidebar and detail view
- Let people hide/show the sidebar following platform conventions (iPadOS edge swipe, macOS menu command, etc.); don't hide it by default, or it loses discoverability
- **macOS**: avoid placing critical information/actions at the bottom of a sidebar (windows are often dragged so the bottom edge goes offscreen); a shrinking window can auto-collapse the sidebar

## Lists and tables

Present data as rows, supporting grouping/hierarchy and interactions like selecting, adding, removing, and reordering.

**Best practices**:
- Lists/tables are best suited for **text content**; for widely varying image sizes or large numbers of images, consider a Collection instead
- Supporting reordering (even without add/remove) is appreciated (iOS/iPadOS requires entering edit mode first)
- Selection feedback should match the context: a table used for hierarchical navigation typically keeps the selected row persistently highlighted; a table listing options usually briefly highlights a row, then shows an icon (like a checkmark) for the selected state
- Keep row text succinct to minimize truncation/wrapping — for large amounts of text per item, show only a title and reveal full content in a detail view
- Use short noun-phrase column headings, title-style capitalization, no trailing punctuation, in multicolumn tables
- **iOS/iPadOS/visionOS**: use an info button only to reveal more details about a row's content — it doesn't support hierarchical navigation (use a disclosure indicator for that); avoid an index alongside trailing-edge controls like disclosure indicators, since both compete for the same area and can cause mis-taps
- **macOS**: support click-to-sort column headers (re-click to reverse), support resizable columns, and consider alternating row colors in wide multicolumn tables; use an outline view (with disclosure triangles) instead of a plain table view for hierarchical data
- **watchOS**: keep row counts limited for scannability; if supporting vertical page-based navigation between detail views, keep those detail views short (once a detail view scrolls, page-based swiping between rows no longer works)

## Toolbars

Provide convenient access to frequently used commands, controls, navigation, and search — arranged horizontally along the top or bottom edge, grouped into three content types: the current view's title, navigation controls (back/forward, search), and actions (buttons, menus). In iOS, a navigation-specific toolbar is also called a navigation bar.

**Best practices**:
- Choose items deliberately to avoid crowding; the system automatically adds an overflow menu on macOS/iPadOS when items no longer fit — don't add your own, and don't design a layout that overflows by default
- Use less custom background tinting on toolbars — let content-layer color show through naturally, and use a `ScrollEdgeEffectStyle` to distinguish the toolbar area, rather than fighting the system's own background effects
- If the content layer is already colorful, avoid similar colors for toolbar item labels — prefer the default monochrome appearance
- Prefer standard components (buttons, text fields, headers, footers) with corner radii concentric with the bar's own corners
- Give each window a useful title (a word or short phrase under 15 characters); leave it empty if a title would be redundant, and never use the app's own name as a window title
- Use the standard Back and Close buttons/symbols rather than a text label
- Prefer simple, recognizable symbols over text for actions (except cases like "edit" that don't map well to a symbol); prefer unbordered system symbols
- Use `.prominent` style for a key action like Done or Submit, keep only one such primary action, and place it at the trailing edge
- Position items across three zones: **leading edge** (back, sidebar show/hide, title, document menu — not customizable, to guarantee availability), **center** (common controls, customizable on macOS/iPadOS, collapses into the system overflow menu as the window shrinks), and **trailing edge** (important persistent items, inspector buttons, an optional search field, the More menu, and the primary action — always visible regardless of window size)

## Related resources
- Developer docs: `ListStyle` (SwiftUI), `TabView`/`NavigationSplitView`/`sidebarAdaptable` (SwiftUI), `UITableView`/`NSTableView`, `backgroundExtensionEffect()`
- Related pages: [materials-color.md](materials-color.md) (how Liquid Glass shows up on these components), [layout.md](layout.md) (how size classes drive component switching, e.g. tab bar ↔ sidebar)
