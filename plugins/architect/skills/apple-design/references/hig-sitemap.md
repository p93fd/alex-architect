# Full Human Interface Guidelines Sitemap

This file lists the complete page structure and URLs for Apple's Human Interface Guidelines (HIG), as of the iOS/iPadOS/macOS 27, watchOS 26, visionOS 26 era. When the condensed summaries in [SKILL.md](../SKILL.md) or the other `references/` files aren't enough, or you need the latest complete official text for a specific component or pattern, open the matching URL here — that's how a claim becomes *grounded* (see SKILL.md).

Every URL below is rooted at `https://developer.apple.com/design/human-interface-guidelines/` — only the `<slug>` is listed.

## Entry points

- `getting-started` — the main hub, indexing Design principles and the per-platform Designing for pages
- `foundations` / `patterns` / `components` / `inputs` / `technologies` — the index pages for the five top-level categories

## Getting started (intro and platform overviews)

- `design-principles` — design principles (see [principles.md](principles.md))
- `designing-for-ios`
- `designing-for-ipados`
- `designing-for-macos`
- `designing-for-tvos`
- `designing-for-visionos`
- `designing-for-watchos`
- `designing-for-games`
- `designing-for-iphone-duo`

(These platform pages are summarized in [platforms.md](platforms.md))

## Foundations

- `accessibility` (see [accessibility.md](accessibility.md))
- `app-icons` (see [app-icons.md](app-icons.md))
- `branding`
- `color` (see [materials-color.md](materials-color.md))
- `dark-mode`
- `icons`
- `images`
- `immersive-experiences`
- `inclusion`
- `layout` (see [layout.md](layout.md))
- `materials` (see [materials-color.md](materials-color.md))
- `motion`
- `privacy`
- `right-to-left`
- `sf-symbols` (see [typography-symbols.md](typography-symbols.md))
- `spatial-layout`
- `typography` (see [typography-symbols.md](typography-symbols.md))
- `writing`

## Patterns (common tasks and experience patterns)

- `charting-data`
- `collaboration-and-sharing`
- `drag-and-drop`
- `entering-data`
- `feedback`
- `file-management`
- `going-full-screen`
- `launching`
- `live-viewing-apps`
- `loading`
- `managing-accounts`
- `managing-notifications`
- `modality`
- `multitasking`
- `offering-help`
- `onboarding`
- `playing-audio`
- `playing-haptics`
- `playing-video`
- `printing`
- `ratings-and-reviews`
- `searching`
- `settings`
- `undo-and-redo`
- `workouts`

## Components (system components, by subcategory)

### Content
`charts` · `image-views` · `text-views` · `web-views`

### Layout and organization
`boxes` · `collections` · `column-views` · `disclosure-controls` · `labels` · `lists-and-tables` (see [components.md](components.md)) · `lockups` · `outline-views` · `split-views` · `tab-views`

### Menus and actions
`activity-views` · `buttons` (see [components.md](components.md)) · `context-menus` · `dock-menus` · `edit-menus` · `home-screen-quick-actions` · `menus` · `ornaments` · `pop-up-buttons` · `pull-down-buttons` · `the-menu-bar` · `toolbars` (see [components.md](components.md))

### Navigation and search
`path-controls` · `search-fields` · `sidebars` (see [components.md](components.md)) · `tab-bars` (see [components.md](components.md)) · `token-fields`

### Presentation
`action-sheets` · `alerts` · `page-controls` · `panels` · `popovers` · `scroll-views` · `sheets` · `windows`

### Selection and input
`color-wells` · `combo-boxes` · `digit-entry-views` · `image-wells` · `pickers` · `segmented-controls` · `sliders` · `steppers` · `text-fields` · `toggles` · `virtual-keyboards`

### Status
`activity-rings` · `gauges` · `progress-indicators` · `rating-indicators`

### System experiences
`app-shortcuts` · `complications` · `controls` · `live-activities` · `notifications` · `snippets` · `status-bars` · `top-shelf` · `watch-faces` · `widgets`

## Inputs

`action-button` · `apple-pencil-and-scribble` · `camera-control` · `digital-crown` · `eyes` · `focus-and-selection` · `game-controls` · `gestures` (see [patterns-gestures.md](patterns-gestures.md)) · `gyroscope-and-accelerometer` · `keyboards` · `nearby-interactions` · `pointing-devices` · `remotes`

## Technologies (integrating specific Apple technologies)

`airplay` · `always-on` · `app-clips` · `apple-pay` · `augmented-reality` · `carekit` · `carplay` · `game-center` · `generative-ai` · `healthkit` · `homekit` · `icloud` · `id-verifier` · `imessage-apps-and-stickers` · `in-app-purchase` · `live-photos` · `mac-catalyst` · `machine-learning` · `maps` · `nfc` · `photo-editing` · `researchkit` · `shareplay` · `shazamkit` · `sign-in-with-apple` · `siri` · `tap-to-pay-on-iphone` · `voiceover` · `wallet`

## How to use this file

1. Start with SKILL.md and the condensed summaries in `references/` — they answer most design decisions.
2. For a specific component the summaries don't cover (context menus, popovers, segmented controls, etc.), look up the slug above and open the URL directly, e.g.:
   `https://developer.apple.com/design/human-interface-guidelines/context-menus`

SKILL.md's "Grounded, or guessing" section covers when a fetch is required and how to get the body out of these JavaScript-rendered pages.
