# Design Principles

Source: `https://developer.apple.com/design/human-interface-guidelines/design-principles`

Apple frames its design principles as eight complementary values, not a rigid rulebook — they're thinking tools for weighing tradeoffs and making design decisions, not a checklist to tick off. When advising a user, cite one of these to explain *why* something works better, rather than just saying "Apple recommends this."

## 1. Purpose — Make something meaningful
Design starts with intention. Get clear on what genuinely matters to the people you're designing for, then focus your effort there.
- Create real value rather than chasing novelty or trends
- Focus on the most important few features and make those great, instead of spreading thin across everything
- Avoid reinventing the wheel: study existing solutions and figure out what makes your product genuinely different

## 2. Agency — Let people do things their own way
An interface exists to help people accomplish their goals, not to be the goal itself.
- Stay out of the way: get people directly to the task or content they came for, and keep guided flows skippable
- Give people the freedom to explore instead of locking them into a fixed path
- Make mistakes cheap: undo and recoverability give people the confidence to explore

## 3. Responsibility — Act in people's best interest
Your work has a real impact on people's lives.
- Be fully transparent about your product's intentions from the very first interaction
- Give a clear rationale when requesting permissions, and be clear about what data you collect and how it's used
- Collect only what your product actually needs, and proactively guard against misuse and unintended harm

## 4. Familiarity — Build on what people know
People bring knowledge of the real world and other software into every new experience.
- Draw on concepts people already understand to make your interface feel immediately at home
- Once you establish a visual or interaction behavior, keep it consistent throughout — consistency helps people learn faster and trust that new interactions will behave as expected
- Give clear, timely feedback about what's happening — whether a control is available, or content has changed

## 5. Flexibility — Adapt to diverse contexts and needs
People use your software in ways as unique as they are.
- Treat accessibility as a day-one priority, not something bolted on afterward
- Preserve people's sense of context as your design adapts across platforms and configurations; use natural animation to ease transitions
- Support as many input methods as reasonably possible
- Give every platform you support the same level of care — don't shortchange one

## 6. Simplicity — Be clear and direct
Simplicity isn't the same as minimalism.
- Include just what's necessary, keeping the important things close at hand and letting the rest fall away
- Be concise — the fewest, most exact words to convey a concept or label a control
- Establish a clear hierarchy: when form and function are obvious, people naturally know how to get where they're going

## 7. Craft — Care about every detail
The quality of your design reflects how much you care.
- Every decision is worth the extra thought: visuals, motion, wording, and audio all deserve craft
- Prototype early, iterate fast, and be willing to throw away what doesn't work
- Shipping isn't the finish line — keep up with new platform capabilities and keep raising the bar

## 8. Delight — Make it human
People remember how software makes them *feel*.
- Know what emotion you want to evoke: a fitness app might energize, a meditation app might calm
- Treat every interaction — even a single button tap or an error message — as a chance to express character
- Don't mistake delight for decoration — delight should serve the task, never upstage it

---

## How to apply these principles in your advice

- When a user asks how to design a specific interaction, first figure out which principle(s) are in tension (e.g. "should this show a confirmation dialog?" is often an Agency-vs-Responsibility tradeoff), then give concrete advice.
- The same principles work well for reviewing an existing design — walk through them one by one and flag places where the design clearly violates one (e.g. making a destructive action the default, prominently highlighted button violates the Agency guidance about helping people recover from mistakes).
- Don't cite a principle's name as if it were the explanation on its own ("because this is the Simplicity principle" explains nothing) — spell out what that principle actually means in the specific situation at hand.
