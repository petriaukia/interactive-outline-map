---
name: interactive-outline-map
description: Turn long documents or over-iterated ideas into self-contained interactive HTML maps that support understanding and writing in the user’s own voice. Use for document synthesis, article planning, strategy maps, workshop notes, and other text-heavy “mind-map” requests; do not use when the user wants finished prose, a radial diagram image, or a full web application.
---

# Interactive Outline Map

Create a readable thinking surface, not a decorative diagram or a disguised article draft. The map is the handoff from machine-assisted exploration back to human understanding and authorship. Start from [assets/template.html](assets/template.html) for new maps. When editing an existing map, preserve its content and visual language unless the user explicitly requests a redesign.

## Choose the purpose

Use one of two modes, or combine them when the request genuinely requires both.

### Understand a long document

Compress the source into its main claims, supporting evidence, relationships, qualifications, and open questions. Preserve distinctions the source makes and attach page, section, or link references when available. The map should let the user reconstruct the document’s reasoning rather than merely remember its topic headings.

### Recover a path to the user’s own writing

Use this when an idea has been discussed or iterated with an LLM until the accumulated prose makes writing from scratch harder. Decompose drafts and conversation history into claims, tensions, examples, evidence, decisions, and unresolved questions.

- Stop one step before polished prose unless the user explicitly asks for a draft.
- Prefer compact propositions, prompts, contrasts, and anchor phrases over paragraphs that invite copy-paste.
- Do not treat fluent model-generated wording as the user’s voice.
- Preserve phrases the user identifies as their own or wants kept verbatim, and distinguish them visually from connective notes.
- Keep disagreements, uncertainty, and alternative structures visible instead of smoothing them into one synthetic narrative.

## Structure the material

- Put the main proposition or purpose in the root block.
- Use top-level branches for the major parts of the argument, process, or narrative.
- Keep interaction at the first outliner tier: top-level branches can be reordered and collapsed, while leaves and twigs remain content rather than independently manipulated objects.
- Use leaves for individual claims, observations, decisions, or actions.
- Use twigs only for genuine supporting detail; avoid deep nesting that makes the page hard to scan.
- Treat the current top-to-bottom branch order as meaningful. Renumber branches after reordering.
- Preserve wording the user identifies as exact, quoted, or otherwise fixed.
- In document-understanding mode, separate source claims from the map maker’s interpretation.
- In writing-recovery mode, reveal the argument’s structure without pre-empting the user’s final sentences.

## Build the artifact

Produce one offline-capable HTML file with its CSS and JavaScript embedded. Do not add CDNs, remote fonts, frameworks, analytics, network calls, or build tooling unless the user asks for them.

For a new map:

1. Copy the template to a descriptive output filename in the working directory.
2. Replace all sample content, the page title, the root, branch labels, notes, leaves, legend, and `data-map-key`.
3. Give every top-level branch a stable, unique ASCII `data-branch-id`. Do not derive identity from the visible sequence number.
4. Adapt the CSS color variables to the user’s brand or source material. Keep contrast and legibility at least as strong as the template.

For an existing HTML map, edit the exact file only when the user asks; otherwise create a clearly named sibling version.

## Preserve interaction invariants

- Clicking a branch heading collapses or restores the complete branch body.
- Enter and Space perform the same toggle when the heading has keyboard focus.
- Reordering starts only from the branch heading, not from a leaf.
- A completed drag must not also trigger the click-to-collapse action.
- The whole branch, including hidden children, moves as one unit.
- Visible branch numbers follow the current DOM order.
- Order and collapsed state persist in `localStorage`, with a safe fallback when storage is unavailable.
- “Open all”, “Hide all”, and “Restore order” controls remain available.
- Printing reveals all branch content and omits interaction-only controls.

## Visual decisions

- Prioritize reading speed over theme fidelity for text-heavy maps.
- Make global action buttons visibly different from branch headings.
- Render the drag affordance as a true dot grid with three columns and four rows, using even spacing; do not imitate it with font glyphs.
- Give horizontal and vertical leaf connectors the same broken-line rhythm and stroke weight. End each branch guide exactly at the center of its final leaf.
- Use color as a navigation cue, not as decoration on every element.
- Avoid nonfunctional menus, window controls, or other elements that look interactive.
- Keep the root, branch, leaf, and twig levels visually distinct even in grayscale.
- If a retro or branded treatment reduces legibility, retain it only as a restrained accent.

## Verify

Before delivery, check that:

- the HTML contains no unfinished sample text or duplicate branch IDs;
- the embedded JavaScript parses without errors;
- every branch can be opened, closed, and moved;
- numbering updates after a move;
- the three global controls still work;
- narrow screens wrap without horizontal scrolling; and
- the print stylesheet shows all content.

Return a clickable absolute link to the finished HTML and summarize only the meaningful design or behavior choices.
