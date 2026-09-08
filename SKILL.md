---
name: interactive-outline-map
description: Turn long documents or over-iterated ideas into self-contained interactive HTML maps that support understanding and writing in the user’s own voice. Use for document synthesis, article planning, strategy maps, workshop notes, and other text-heavy “mind-map” requests; do not use when the user wants finished prose, a radial diagram image, or a full web application.
---

# Interactive Outline Map

Create a readable thinking surface, not a decorative diagram or a disguised article draft. The map is the handoff from machine-assisted exploration back to human understanding and authorship. Start from [assets/template.html](assets/template.html) for new maps. When editing an existing map, preserve its content and visual language unless the user explicitly requests a redesign.

## Choose the purpose

Use one of two modes, or combine them when the request genuinely requires both.

### Understand a long document

Compress the source into its main claims, supporting evidence, relationships, qualifications, and open questions. Preserve distinctions the source makes.

Most leaves in this mode are your compression of the source, and they stay unmarked. Use `class="leaf source"` for the minority that has to stay **traceable** — a quotation, a figure, a number, a named parameter — and carry the locator in the leaf itself (`(§3.2.2)`, `(Table 2)`, a page). A map of a numbered paper whose numbers carry no locators is not yet a reading map. Where the source exists in several versions that disagree, say which one the map follows.

### Recover a path to the user’s own writing

Use this when an idea has been discussed or iterated with an LLM until the accumulated prose makes writing from scratch harder. Decompose drafts and conversation history into claims, tensions, examples, decisions, and unresolved questions.

- Stop one step before polished prose unless the user explicitly asks for a draft.
- **Keep every leaf under about twenty words, and do not write full paragraphs.** A leaf that reads as a finished sentence invites copy-paste, and copy-paste is the failure this skill exists to prevent.
- Do not treat fluent model-generated wording as the user’s voice.
- Mark phrases the user wants kept verbatim with `class="leaf own"`. **Never put that class on a sentence you wrote.** The class asserts the words are the user's, and the flag invites them to lift it into their piece unchanged — so using it on your own wording puts your sentence in their mouth under their name. That is the exact failure this skill exists to prevent, and it is easy to commit, because the sentences a model is proudest of are the ones it will offer. If the user has not said those words, the leaf is plain.
- **Give the map at least one branch of unresolved material** — open questions, tensions, or the decision that has not been made. Mark its leaves `class="leaf question"`. A recovery map with no open questions has smoothed the problem away instead of showing it.

## Structure the material

- Put the main proposition or purpose in the root block.
- Use **four to seven top-level branches**, each with **three to six leaves**. Fewer than four branches usually means the material has not been decomposed; more than seven exhausts both the palette and the reader.
- Keep interaction at the first outliner tier: top-level branches can be reordered and collapsed, while leaves and twigs remain content rather than independently manipulated objects.
- Use leaves for individual claims, observations, decisions, or actions.
- Use twigs only for genuine supporting detail; avoid deep nesting that makes the page hard to scan.
- Treat the current top-to-bottom branch order as meaningful.
- Give each branch **at most one** `leaf highlight`. It is the sentence the branch rests on, not general emphasis.
- Preserve wording the user identifies as exact, quoted, or otherwise fixed.

### The four leaf kinds

Every leaf is plain by default. Four classes name a kind, and each draws its own node colour and a small caps flag. Do not invent a fifth kind or add ad hoc styling to a leaf.

**Wine means one thing on the page: these words are the writer's own.** It is the strongest colour the palette has, and `leaf own` is the only kind that carries it. A key idea is your judgement about the material and is drawn in navy; a sentence you wrote is never wine, because wine is the reader's signal that a human, not a model, chose those words.

| Class | Flag | Use for |
|---|---|---|
| `leaf highlight` | key idea | the one claim the branch rests on |
| `leaf source` | from the source | a quotation, figure or number that must stay traceable, with its locator |
| `leaf question` | open question | a tension, an unresolved decision, a gap |
| `leaf own` | your words | wording the user has supplied and wants kept; wine and italic, the strongest mark the page has |

### Deciding which words are the user's

The prohibition above is easy to state and easy to break, because a model has no
native sense of who wrote what. Use the test, not your judgement.

1. **The source test.** In recovery mode the input is a conversation. A phrase is
   the user's if it appears in a turn the user wrote — their message, a draft
   they pasted, a transcript of them speaking. A phrase from an assistant turn is
   not theirs, however the idea originated.
2. **Approval is not authorship.** "That's good, keep that" makes a sentence
   approved, not written. An approved sentence is at most a `leaf highlight`.
   This is where the rule is broken in practice, because approval feels like a
   handover.
3. **The edit limit.** Case, punctuation and truncation preserve authorship.
   Changing a word does not. If you altered the wording, the leaf is plain.
4. **The default is none.** With no conversation to draw on — a fresh brief, a
   document to compress — a map carries **zero** `own` leaves. An absent class is
   the normal result, not a gap to fill. Most maps have none.
5. **Ask rather than guess.** When the line is unclear, list the candidates and
   ask which are the user's. One question costs less than one wrong attribution.
6. **Name them on delivery.** Say which leaves you marked `own` and where each
   came from, so the user can overrule you before the words reach their piece
   under their name.

## Build the artifact

Produce one offline-capable HTML file with its CSS and JavaScript embedded. Do not add CDNs, remote fonts, frameworks, analytics, network calls, or build tooling unless the user asks for them.

For a new map:

1. Copy the template to a descriptive output filename in the working directory.
2. Replace all sample content: the page title, the root, branch labels, notes, leaves, and `data-map-key`. **`data-map-key` must be replaced** — while the placeholder is in place, every map in the same browser shares one storage key.
3. Give every top-level branch a stable, unique ASCII `data-branch-id`. Do not derive identity from the visible sequence number.
4. Set the eyebrow to name **what stage the map is at**, not what the map is. A map is the point where the planning stops and the work starts, and the eyebrow is where that is said. The template's default is *Just write it!* — a nudge, because a map that is finished is a page that is not yet written; a document map may instead name its source (*Paper map · Vaswani et al. · NeurIPS 2017*). Do not spend the eyebrow, the title and a subtitle on explaining how the page works — the page shows that by itself.
5. **Write the whole page in the user’s language**, chrome included: `<html lang>`, `<title>`, the `.eyebrow`, the `.hint`, the four button labels and the `aria-label` on `.tools`. The strings owned by the CSS and the script are overridden without touching either:
   - flags: `:root{--flag-key-idea:"ydinlause";--flag-source:"lähteestä";--flag-question:"avoin kysymys";--flag-own:"omin sanoin"}`
   - script strings, as attributes on `<body>`: `data-heading-hint`, `data-node-hint`, `data-hidden-label` (`"{n} kätkettyä"`), `data-move-status` (`"Haara {n}/{total}"`), `data-copied-label`, `data-copy-failed-label`.
6. Adapt the CSS colour variables to the user’s brand or source material. Branch colours come from `--navy`, `--slate`, `--petrol`, `--petrol-700`, `--wine` and `--amber-700`; give adjacent branches different colours and repeat only when a map has more branches than colours. Keep contrast and legibility at least as strong as the template.
7. Do not hand-write the legend. The script generates it from the branches, so it cannot drift out of order or out of wording.

For an existing HTML map, edit the exact file only when the user asks; otherwise create a clearly named sibling version.

## Preserve interaction invariants

- The dot grid at the left of a branch heading is the drag handle. Dragging it reorders the branch; the rest of the heading is not draggable, so text in the map stays selectable.
- Clicking a branch heading collapses or restores the whole branch, and the circle at its right end shows the state as a drawn bar, not a typeset glyph.
- A collapsed branch shows cards stacked behind its heading: one card when a single leaf is folded away, two when there are more. A branch with no leaves shows no state control at all and does not respond to a click.
- Enter and Space collapse and restore from the keyboard, and Alt with the arrow keys moves the focused branch. The number of hidden leaves is announced to a screen reader.
- Reordering works with a mouse, a touch screen or a pen: it runs on pointer events, not on HTML5 drag and drop.
- The whole branch, including hidden children, moves as one unit.
- Visible branch numbers and the legend follow the current DOM order.
- Order and collapsed state persist in `localStorage`, with a safe fallback when storage is unavailable. A stored order is discarded once the file’s own branch order has changed, so regenerating the map beats a reader’s earlier drag.
- “Open all”, “Hide all”, “Restore order” and “Copy as outline” remain available. Copy hands the current order back as Markdown — the map is a step towards writing, so the structure has to be able to leave it.
- Printing reveals all branch content and omits interaction-only controls, including the stack behind a collapsed heading — on paper nothing is hidden, so nothing should suggest it is. Branch guides are measured even while a branch is hidden, so a printed map that was collapsed on screen still ends each guide in the right place.

## Visual decisions

- Prioritize reading speed over theme fidelity for text-heavy maps.
- Make global action buttons visibly different from branch headings.
- Render the drag affordance as a true dot grid with three columns and four rows, using even spacing; do not imitate it with font glyphs.
- Give horizontal and vertical leaf connectors the same broken-line rhythm and stroke weight. End each branch guide exactly at the center of its final leaf.
- Use color as a navigation cue, not as decoration on every element. Each leaf kind has its own colour: wine for the user's words, navy for a key idea, petrol for a traceable source, amber for an open question.
- Avoid nonfunctional menus, window controls, or other elements that look interactive.
- Keep the root, branch, leaf, and twig levels visually distinct even in grayscale.
- If a retro or branded treatment reduces legibility, retain it only as a restrained accent.

## Verify

Run `scripts/check.sh <file.html>` before delivery. It catches the mechanical failures: leftover template text, duplicate or missing branch IDs, an unreplaced `data-map-key`, a missing `lang`, remote dependencies, and a script that does not parse.

Then check by hand what a script cannot see:

- every branch opens, closes and moves, and the numbering and the legend follow;
- the guide line under each branch ends at the centre of its last leaf;
- narrow screens wrap without horizontal scrolling;
- the print view shows all content;
- no branch carries more than one `leaf highlight`; and
- in recovery mode, no leaf reads as a finished sentence ready to be pasted.

Return a clickable absolute link to the finished HTML and summarize only the meaningful design or behaviour choices.
