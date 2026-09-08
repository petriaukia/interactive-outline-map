# Interactive Outline Map

An experimental Codex skill for turning long documents and over-iterated ideas into self-contained interactive HTML maps you can understand, rearrange and write from.

## Why this exists

LLMs are good at expanding an idea, challenging it and producing one more polished iteration. After enough rounds, that fluency becomes a trap: the conversation contains so much finished-sounding prose that writing the piece yourself is suddenly harder than it was at the beginning. The easy next step is to share the model’s text. Your own voice quietly disappears from the process.

Interactive Outline Map stops one step earlier.

It turns the accumulated material into a manipulable structure of claims, evidence, tensions, examples, decisions and open questions. The result is deliberately not a finished article. It is a handoff from machine-assisted thinking back to human authorship.

The skill has two primary uses:

1. **Understand a long document.** Compress a paper, report or other source into a map that preserves its reasoning, evidence, qualifications and relationships.
2. **Recover your own writing path.** Take an idea that has been iterated with an LLM and strip away the false finality of generated prose, leaving a structure you can use to write the piece in your own style.

I've intentionally limited this experimental skill to the first tier of an outliner. The point is to get you writing, not to pull you into the minutiae of outlining.

The generated maps are designed for thinking and editing rather than presentation alone:

- click a branch heading to hide or restore its contents;
- drag a heading to reorder the complete branch;
- keep the chosen order and open/closed state between visits;
- print the complete map even when branches are hidden on screen; and
- customize the visual system through a small set of CSS variables.

## Install

Clone the skill directly into your personal Codex skills directory:

```sh
git clone https://github.com/petriaukia/interactive-outline-map.git ~/.codex/skills/interactive-outline-map
```

Restart Codex after installation so the new skill is discovered.

## Use with Codex

Place this directory under your personal Codex skills directory and invoke:

```text
$interactive-outline-map Turn this article outline into an interactive HTML map.
```

For document understanding:

```text
$interactive-outline-map Turn this report into a map of its claims, evidence and open questions.
```

For writing recovery:

```text
$interactive-outline-map We have iterated this idea for too long. Reduce it to a structure I can write from in my own voice; do not draft the article.
```

The skill can also adapt an existing HTML map while preserving its content and visual style.

## Examples

1. [Attention Is All You Need](examples/attention-is-all-you-need.html) maps the 2017 Transformer paper into six movable and collapsible branches: motivation, architecture, attention, positional information, training and results. The text is a compact original summary linked to the NeurIPS publication and arXiv record.
2. [A Room of One's Own](examples/a-room-of-ones-own.html) maps Virginia Woolf's 1929 essay into seven movable and collapsible branches: method, material conditions, the missing archive, literary tradition, external scrutiny, the undivided mind and the future Woolf asks readers to make. The map paraphrases the essay and links to a full-text source.

## Repository status

Early and usable. The single-file template deliberately has no framework, remote dependency, analytics or build step. The current work is focused on finding the right boundary between useful synthesis and unwanted ghostwriting.

## License

[MIT](LICENSE)
